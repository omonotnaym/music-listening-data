import fastapi, json
from src import spotify_requests, analyzation

app = fastapi.FastAPI()


@app.get("/authorize")
def authorize():
    """
    strictly for redirecting users to the spotify authorize endpoint to get permissions
    """
    return fastapi.responses.RedirectResponse(spotify_requests.get_authorization_url())


@app.get("/callback")
def callback(code: str = None):
    """
    displays the html for after the user authorizes and then calls the appropriate functions for token handling to begin
    with the authorization code in the response.
    """
    # h
    # t
    # m
    # l
    # stub
    if code:
        spotify_requests.request_access_token(code)
    else:
        # html for the denial of access
        pass


@app.get("/")
def home():
    """
    displays the html for my home page and alsAnd I Toldo will check for whether or not the tokens need to be refreshed
    """
    # h
    # t
    # m
    # l
    # stub
    try:
        spotify_requests.is_refresh_token_expired()
    except spotify_requests.NotAuthorizedError:
        # display some html that tells the user what could have happened/went wrong
        # display html that will prompt them to click something that will redirect them to the authorize enpoint
        pass


@app.get("/listening-history")
def listening_history():
    """
    gets the listening history of the user from the past 30 days (for now) and shows them the tracks
    """
    try:
        spotify_requests.request_recently_played()
    except spotify_requests.NoRecentlyPlayedTracksError:
        # display html saying something like: "when pulling for your recently played tracks, we didnt find any data"
        pass
    # h
    # t
    # m
    # l
    # stub


@app.get("/listening-history/pick-rates")
def listening_history_pick_rates():
    """
    gives the user the resulting picks rates of their recently played tracks
    """

    with open("recently_played_tracks.json", "r") as f:
        recently_played_tracks = json.load(f)
    picks = analyzation.combine_recently_played_tracks_picks(
        analyzation.detect_recently_played_tracks_first_picks(
            analyzation.get_recently_played_tracks_details(recently_played_tracks)
        ),
        analyzation.detect_recently_played_tracks_picks(
            analyzation.get_recently_played_tracks_details(recently_played_tracks)
        ),
    )
    if picks:
        return picks
    return {
        "message": "we detected no picks with your data! this could be an error so please try to request your listening history again and return to get your picks once more"
    }
