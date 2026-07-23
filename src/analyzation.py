import json, time, datetime


def detect_all_recently_played_tracks_picks(tracks: list):
    """
    takes the tracks given to it and determines what songs are session starts (aka first picks) or early cut transitions (regular picks) and non-picks (neither of the other two)
    a session start is determined as an hour since the last song was fully played (3600 + duration)
    an early cut is determined when the end time of the song transitioned to minus the end time of the song transitioned from is less than the transitioned to song's duration
    """
    previous_track = None
    first_picks = dict(total_picks=0)
    picks = dict(total_picks=0)
    non_picks = dict(total=0)
    is_pick = False

    for track in tracks:
        if not previous_track:
            previous_track = track
            continue
        elif (
            track["played_at"] - previous_track["played_at"]
            >= 3600 + track["duration_in_milliseconds"] / 1000
        ):
            first_picks["total_picks"] += 1
            if track["name"] in first_picks:
                first_picks[track["name"]] += 1
            else:
                first_picks[track["name"]] = 1
        elif (
            track["played_at"] - previous_track["played_at"]
            < track["duration_in_milliseconds"] / 1000
        ) and not is_pick:
            non_picks["total"] += 1
            if track["name"] in non_picks:
                non_picks[track["name"]] += 1
            else:
                non_picks[track["name"]] = 1
            is_pick = True
        elif is_pick:
            picks["total_picks"] += 1
            if track["name"] in picks:
                picks[track["name"]] += 1
            else:
                picks[track["name"]] = 1
        else:
            non_picks["total"] += 1
            if track["name"] in non_picks:
                non_picks[track["name"]] += 1
            else:
                non_picks[track["name"]] = 1

        if not (
            track["played_at"] - previous_track["played_at"]
            < track["duration_in_milliseconds"] / 1000
        ):
            is_pick = False

        previous_track = track
    return (first_picks, picks, non_picks)


def get_recently_played_tracks_details(pages: dict):
    """
    takes the pages unfiltered and filters them for the two functions that analyze recently played tracks picks
    also does some slight formatting with changing iso format strings to time in seconds since the epoch
    """
    tracks = []
    for page in pages.keys():
        for item in pages[page]["items"]:
            try:
                track_name = item["track"]["name"]
                track_duration_in_milliseconds = item["track"]["duration_ms"]
                track_played_at = datetime.datetime.fromisoformat(
                    item["played_at"]
                ).timestamp()
                # ^firstly create a datetime object using the iso format given by the played_at key by using .fromisoformat()
                # |then covert it into seconds since the epoch using .timestamp() so that it can be used for logic
                # |
                tracks.append(
                    dict(
                        name=track_name,
                        duration_in_milliseconds=track_duration_in_milliseconds,
                        played_at=track_played_at,
                    )
                )
            except KeyError:
                print("key error")
    tracks.sort(key=lambda track: track["played_at"])
    return tracks


def combine_recently_played_tracks_picks(
    first_picks: dict, picks: dict, non_picks: dict
):
    """
    takes the two types of picks that can be detected (as of v1) and combines the numbers to give overall picks
    and pick percentages per song.
    """
    aggregation = {}
    total_picks = first_picks["total_picks"] + picks["total_picks"]
    total_non_picks = non_picks["total"]

    for key in [*first_picks.keys(), *picks.keys()]:
        if key != "total_picks":
            if key in aggregation:
                if key in first_picks:
                    aggregation[key] += first_picks[key] / total_picks * 100
                else:
                    aggregation[key] += picks[key] / total_picks * 100
            else:
                if key in first_picks:
                    aggregation[key] = first_picks[key] / total_picks * 100
                else:
                    aggregation[key] = picks[key] / total_picks * 100

    for key in aggregation.keys():
        aggregation[key] = round(aggregation[key], 1)

    return {
        "total_picks": total_picks,
        "picks": {**aggregation},
        "non_picks": {**non_picks},
    }
