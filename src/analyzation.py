import pandas, json, time, datetime


def detect_recently_played_track_first_picks(tracks):
    previous_track = None
    first_picks = 0
    for track in tracks:
        if not previous_track:
            previous_track = track
        else:
            if int(track["played_at"]) + (int(previous_track["played_at"]) + int(previous_track["duration_in_milliseconds"]))



def detect_recently_played_track_picks(tracks):
    pass


def get_recently_played_track_details(pages):
    tracks = []
    for page in pages.keys():
        for item in items:
            track_name = item["track"]["name"]
            track_duration_in_milliseconds = item["track"]["duration_ms"]
            track_played_at = datetime.datetime.fromisoformat(
                item["track"]["played_at"]
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
    return tracks
