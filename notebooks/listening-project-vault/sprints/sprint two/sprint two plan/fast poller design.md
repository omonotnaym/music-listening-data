this is a fast poller that will hit the /player and /player/queue endpoints

# polling behavior

this poller will be called every 30s when the user is not playing anything. this is because im limited by the rate limits of spotify with the starting limit being ~100 requests per minute overall for my app. when the poller hits and the user is playing something we then will start using our [[fast poller design#^a2e65e|interval during playback]].

# runner

i will be using cron to run this poller as well


# token ownership

the poller can just call is_refresh_token_expired() in spotify requests and when reauth is required, log the details of the failure, try once more and if failure occurs again change the frequency to every 5 minutes until the user authorizes again


# storage

i will be implementing a database before shipping either poller, so that storage is not tedious with files.


# interval during playback

^a2e65e

during playback we will poll every 5 seconds. the worst case scenario of a user doing rapid skips back to back can be caught by looking at the queue, since we want to know what's being skipped. this interval will also help us stay within our rate limit for the 30 second rolling window