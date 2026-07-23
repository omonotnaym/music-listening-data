# what didnt work this sprint: 
- when changing things about the design of the application i really didnt think to change my obsidian notes to match the change. i should really stop and think when changing the design for where i need to reflect these changes elsewhere. 
- also i perhaps should have shown claude my code more during this sprint just to keep myself safe for the future, which leads into my next point: 
# what worked this sprint: 
- i was not on auto pilot this sprint. when writing code i was walking through the logic carefully and when faced with a bug about the code i ran to claude SIGNIFICANTLY less. printing and following the bugs and logic really helped me keep things bug free
- the habit of trying to do a minimum of 3 hours everyday really helps me get into flows where i end up doing double that time in work. there were some days where i did 8 hours as if i were a full time software engineer.
# velocity
i did little to no work on sunday (i have no idea how many hours), i know i did at least 3 hours monday, i think i did under 3 on tuesday, i did like 8+ on wednesday, and then i did like 8+ yesterday too. so like let's just assume 25 hours for 4 tasks. id say that's pretty safe. 
# findings
i learned that a song's played_at value only gets input when you move to the next song in some cases. if you were to play the song, pause and then come back after an extended period of time to resume, that will count as a pick which is not intended but is a limitation we know. sprint two needs to start with a sort for get_recently_played_tracks_details(), and the tracking of the current player is much more emphasized since the recently played tracks is quite limited in data and there's more guessing of user behavior than would be with continuous tracking.