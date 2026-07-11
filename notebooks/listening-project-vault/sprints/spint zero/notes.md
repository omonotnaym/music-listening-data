# spotify api
this sections will note the ins and outs of the spotify api that's relevant to the project and this is a review as well so that i catch up to what i knew when i had started this project. for this sections i will be referencing the [spotify api website](https://developer.spotify.com/documentation/web-api).

# OAuth flow
spotify uses the [OAuth 2.0 authorization framework](https://developer.spotify.com/documentation/web-api/concepts/authorization) and within this framework, i have opted to use the [authorization code flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow) because i will store the client secret strictly locally on my computer.
## authorization code flow
### 1. requesting user authorization
- when getting user authorization, you're making a **get** request to https://accounts.spotify.com/api/authorize
### 2. requesting access tokens
### 3. refreshing tokens

# api calls
