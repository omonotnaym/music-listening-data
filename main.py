import fastapi
from src import spotify_requests

app = fastapi.FastAPI()

@app.get("/authorize")
def get_user_authorization():
    return fastapi.responses.RedirectResponse(spotify_requests.make_authorization_url())

@app.get("/callback")
def callback_function(code: str = None):
    """
    displays the html for after the user authorizes and then calls the appropriate functions for token handling to begin
    with the authorization code in the response.
    """
    #h
    #t
    #m
    #l
    #stub
    if code:
        spotify_requests.get_access_token(
            code, 
            spotify_requests.redirect_uri, 
            spotify_requests.b64_app_credentials_header,
            )
    else:
        #html for the denial of access
        pass

@app.get("/")
def home_function():
    """
    displays the html for my home page and also will check for whether or not the tokens need to be refreshed
    """
    #h
    #t
    #m
    #l
    #stub
    try:
        spotify_requests.is_refresh_token_expired()
    except spotify_requests.NotAuthorizedError:
        #display some html that tells the user what could have happened/went wrong
        #display html that will prompt them to click something that will redirect them to the authorize enpoint
        pass