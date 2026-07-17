import json, time, datetime


def detect_recently_played_tracks_first_picks(tracks):
    """
    takes the tracks given to it and determines what songs are session starts (aka first picks)
    a session start is determined as an hour since the last song was fully played
    """
    previous_track = None
    all_first_picks = dict(total_picks=0)
    for track in tracks:
        if not previous_track:
            previous_track = track
            all_first_picks["total_picks"] += 1
            all_first_picks[track["name"]] = 1
        else:
            if (
                int(track["played_at"])
                - (
                    int(previous_track["played_at"])
                    + int(previous_track["duration_in_milliseconds"] / 1000)
                )
                >= 3600
            ):
                all_first_picks["total_picks"] += 1
                try:
                    all_first_picks[track["name"]] += 1
                except KeyError:
                    all_first_picks[track["name"]] = 1
            previous_track = track
    return all_first_picks


def detect_recently_played_tracks_picks(tracks):
    """
    takes the tracks given to it and determines what songs are early cut transitions
    this is determined when the start time of the song transitioned to is played before the song transitioned from would end
    """
    previous_track = None
    all_picks = dict(total_picks=0)
    for track in tracks:
        if not previous_track:
            previous_track = track
        else:
            if int(track["played_at"]) < (
                int(previous_track["played_at"])
                + int(previous_track["duration_in_milliseconds"] / 1000)
            ):
                all_picks["total_picks"] += 1
                try:
                    all_picks[track["name"]] += 1
                except KeyError:
                    all_picks[track["name"]] = 1
        previous_track = track
    return all_picks


def get_recently_played_tracks_details(pages):
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
                tracks.insert(
                    0,
                    dict(
                        name=track_name,
                        duration_in_milliseconds=track_duration_in_milliseconds,
                        played_at=track_played_at,
                    ),
                )
            except KeyError:
                pass
    return tracks


def combine_recently_played_tracks_picks(first_picks: dict, picks: dict):
    """
    takes the two types of picks that can be detected (as of v1) and combines the numbers to give overall picks
    and pick percentages per song.
    """
    aggregation = {}
    total_picks = first_picks["total_picks"] + picks["total_picks"]
    first_picks_set = set([*first_picks.keys()])
    picks_set = set([*picks.keys()])
    differences = [  # get all of the differences between the sets
        *first_picks_set.difference(picks_set),
        *picks_set.difference(first_picks_set),
    ]
    all_picks_keys = first_picks_set.intersection(picks_set).difference(
        {"total_picks"}
    )  # just have the songs as the keys, not total picks
    if all_picks_keys:
        for key in all_picks_keys:
            aggregation[key] = (first_picks[key] + picks[key]) / total_picks * 100
    for difference in differences:
        if difference in first_picks_set:
            aggregation[difference] = first_picks[difference] / total_picks * 100
        else:
            aggregation[difference] = picks[difference] / total_picks * 100
    return {"total_picks": total_picks, "picks": {**aggregation}}
