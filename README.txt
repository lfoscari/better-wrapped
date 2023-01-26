https://community.spotify.com/t5/Spotify-for-Developers/Now-that-users-can-view-their-recently-played-tracks-in-the-apps/td-p/5181981

Apparently the recently-played-tracks endpoint of the Spotify API only returns
the last 50 songs, no matter what. If a song is roughly 3 minutes long, that
means we have to query the API every 3 * 50 = 150 minutes or 2.5 hours.
