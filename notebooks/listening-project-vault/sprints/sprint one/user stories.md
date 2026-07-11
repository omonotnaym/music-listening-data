# user stories
## pick rate
- as a music lover, i want to be able to analyze my [[product goal#first time pick rates|first time pick rates]] for songs over 30 days so that i can make sense of my preferences.

# acceptance criteria
the pick rates for songs are analyzed via looking at the time signatures in the listening data. right now i know that the listening data gives the time, in seconds since 1970, at which a song starts playing; i will just call this the time signature. with the third type of detection (non-sequential smooth transition) to be added in a later version, we will determine a pick, for now, to be one of the following:
- when the time signature + length of the previously played song is greater than the time signature of the current song
- when the time signature of the current song - (when the time signature + length of the previously played song) is greater than or equal to 3600 (this will be first time pick rate for now while i wait to implement the idea of music sessions)
for each pick we'll just take the percentage by doing song picks/total picks.
output is a returned json via an api endpoint
if the user has no listening data then in the results just say "no data to analyze" (this is the only edge case i came up with on my own for now i cant think of anything else)
if there is no "previous song" then the current song will be considered the first pick of the session
if needed data is missing, multiple attempts will be made and if all attempts fail we will ignore the pick and try and find the next
if zero picks are detected the user will get a smooth sailor achievement for this rare occasion and they will be greeted with a congratulations message and an explanation of the findings.