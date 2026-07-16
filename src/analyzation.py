import json, time, datetime

fake_set = {
    "page 1": {
        "items": [
            {
                "track": {"name": "song A", "duration_ms": 120000},
                "played_at": "2026-07-15T12:28:59.0Z",
            },
            {
                "track": {"name": "song C", "duration_ms": 120000},
                "played_at": "2026-07-15T12:26:59.0Z",
            },
            {
                "track": {"name": "song B", "duration_ms": 120000},
                "played_at": "2026-07-15T12:24:59.0Z",
            },
            {
                "track": {"name": "song A", "duration_ms": 120000},
                "played_at": "2026-07-15T12:22:59.0Z",
            },
            {
                "track": {"name": "song C", "duration_ms": 120000},
                "played_at": "2026-07-15T12:22:59.0Z",
            },
            {
                "track": {"name": "song B", "duration_ms": 120000},
                "played_at": "2026-07-15T12:20:59.0Z",
            },
            {
                "track": {"name": "song A", "duration_ms": 120000},
                "played_at": "2026-07-15T12:18:59.0Z",
            },
            {
                "track": {"name": "song C", "duration_ms": 120000},
                "played_at": "2026-07-15T12:18:59.0Z",
            },
            {
                "track": {"name": "song B", "duration_ms": 120000},
                "played_at": "2026-07-15T11:16:59.0Z",
            },
            {
                "track": {"name": "song A", "duration_ms": 120000},
                "played_at": "2026-07-15T11:15:00.0Z",
            },
        ]
    }
}


def detect_recently_played_tracks_first_picks(tracks):
    previous_track = None
    all_first_picks = dict(total_picks=0)
    for track in tracks:
        if not previous_track:
            previous_track = track
            all_first_picks["total_picks"] += 1
            all_first_picks[track["name"]] = 1
        else:
            print(int(track["played_at"]))
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
    tracks = []
    for page in pages.keys():
        for item in pages[page]["items"]:
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
    return tracks


print(
    detect_recently_played_tracks_first_picks(
        get_recently_played_tracks_details(fake_set)
    )
)
print(detect_recently_played_tracks_picks(get_recently_played_tracks_details(fake_set)))
