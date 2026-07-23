this is a poller that will hit the /recently-played endpoint.
# interval

this poller will get called every 20 minutes. going with the worst case scenario of the user skipping as soon as it would be logged into their recently played tracks, we would want to be able to catch this pattern 50 times since this endpoint is limited to only the last 50 plays of the user. so 30s * 50 plays = 1500s = 25m. i will give it a 5 minute margin to be safe so we end up being at 20m.

# runner

i will use cron to run this in the background at the rate specified

# dedupe

what will make two plays the same play is identical played_at timestamps. it's nearly impossible to play two songs at the same time intentionally, so unintentionally those odds are even lower

# token ownership

the poller can just call is_refresh_token_expired() in spotify requests and when reauth is required, log the details of the failure and move onto the next

# storage

i will be implementing a database before shipping either poller, so that storage is not tedious with files.