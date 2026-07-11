import requests, inspect, time, base64, json, sys, os, dotenv, fastapi, urllib

dotenv.load_dotenv() #injects the key=value pairs from the projects .env file into os.environ

client_id = os.getenv("SPOTIFY_CLIENT_ID") #gets the value that spotify client id holds from os.environ
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET") #gets the value that spotify client secret holds from os.environ
client_credentials = client_id + ":" + client_secret #merges both client id and secret because they're needed for (INSERT REASON WHEN COVERED)
b64_app_credentials_header = { #tbd
    "Authorization": "Basic " + str(base64.b64encode(client_credentials.encode()).decode()),
    #  firstly encode the credentials into a bytes object with the base python .encode() function,
    #  then encode it into a base64 encoded string per the spotify api's requirements using the .b64encode() function from base 64 for your completed header
    "Content-Type": "application/x-www-form-urlencoded",
}
redirect_uri = "http://127.0.0.1:8000/callback"
current_access_token = None 

class NotAuthorizedError(Exception):
    pass

def check_request(request):
    """
    takes a request of any kind and checks whether or not the request was successful.
    if it was not successful, raise an exception and print what function call to the exact line caused the exception and the code given other than 200
    """
    failed_status_code = None #to store any code other than 200
    try:
        if request.status_code == 200:
            return request #give the request we're inspecting back to where it cameget_user_authorization() from if all is well
        else:
            failed_status_code = str(request.status_code) #we want to know what the code was since it wasn't 200 (therefore, stringify for printing)
            raise requests.HTTPError #anything that's not 200 is not ok so we halt the program
    except requests.HTTPError:
        print(request) #tbd
        print(request.json()) #tbd
        print(
            "request attempt failed on line "
            + str(inspect.stack()[1].lineno) #gets the line number of the function that most recently called check_request for inspection and debugging
            + ". response was "
            + failed_status_code
            + " instead of 200."
        )


def make_authorization_url():
    """
    redirects the user to the spotify authorization website with the correct query string for what we want
    """
    global redirect_uri
    data = {
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "playlist-read-private playlist-read-collaborative user-top-read user-read-recently-played user-library-read user-read-email",
        }
    return "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(data)
    
def get_access_token(authorization_code, redirect_uri, header):
    """
    uses the authorization code from our get_user_authorization function to get the initial access code so that we can get refresh tokens and 
    access the necessary information.
    """
    initial_request = check_request(
        requests.request(
            "POST",
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": redirect_uri,
            },
            headers=header,
        ),
    )
    set_last_response_body(initial_request)


def get_refresh_token():
    """
    gets a new refresh_token and stores the entire response from the request. 
    if the json file in which the last response was stored has lost vital information, calls function which initializes everything again
    """
    try:
        last_response_body = get_last_response_body()
        last_refresh_token = last_response_body["refresh_token"]
        refresh_request = check_request(
            requests.request(
                "POST",
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "refresh_token", 
                    "refresh_token": last_refresh_token,
                    },
                headers=b64_app_credentials_header,
            ),
        )
        set_last_response_body(refresh_request)
    except KeyError:
        raise NotAuthorizedError

def is_refresh_token_expired():
    """
    checks to see if the refresh token is expired and, if so, calls function to get new refresh token.
    also reinitializes if vital data within the json file, that would prevent the checking of an expired refresh token, has been compromised.
    """
    try:
        if int(time.time()) - get_last_response_body()['time_of_response'] >= 3600: 
            get_refresh_token() #if the difference of the current time in seconds since 1970 and the time of the last response, get a new refresh token
        else:
            pass
    except (KeyError, NotAuthorizedError):
        raise NotAuthorizedError

def does_token_file_exist():
    try:
        with open("access_token_stuff.json", "r") as f: #access_token_stuff is a json object with 5 fields: access_token, token_type, expires_in, scope, and time_of_response
            last_response_body = json.load(f) #turns parses access_token_stuff into a dict
        return True
    except (FileNotFoundError, json.JSONDecodeError): #if the file doesn't exist or if the file is empty
        return False

def get_last_response_body():
    if does_token_file_exist():
        with open("access_token_stuff.json", "r") as f:
            last_response_body = json.load(f)
        return last_response_body
    else:
        raise NotAuthorizedError

def set_last_response_body(response):
    """
    intakes a response and stores the json of the response in the dedicated json file.
    also creates new key value pair for the time at which this response was stored for refresh token logic.
    reformats the key-value pairs within the json file to have double quotes instead of single quotes to maintain json format.
    """
    last_response_body = response.json() #get the body of the last response recieved in json format
    last_response_body["time_of_response"] = int(time.time()) #set the time of the response to the current time in seconds since 1970
    with open("access_token_stuff.json", "w") as jsonfile:
        json.dump(last_response_body, jsonfile, indent=2) #translates the python object of the last_response_body into json and then prints it to access_token_stuff.json

# def bearer_header_constructor():
#     global current_access_token
#     current_access_token = last_response_body['access_token']
#     return {"Authorization": "Bearer " + current_access_token, "Content-Type": "application/x-www-form-urlencoded"}
