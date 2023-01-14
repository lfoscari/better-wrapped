import requests, os, json, shelve, time

# The goal of this daemon is to call periodically the Spotify API to
# get the recently played tracks and store them in a JSON database
# locally

def load_oauth(file = "spotify_oauth"):
    try:
        return open(file).read().strip()
    except FileNotFoundError as e:
        print("You need to create a file called 'spotify_oauth' with the Spotify OAuth token\n\
            Navigate to https://developer.spotify.com/console/get-recently-played and click 'Get token'")
        exit(-1)

def get_recently_played(spotify_oath, after=None, url="https://api.spotify.com/v1/me/player/recently-played"):
    if url is None: return []

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + spotify_oath,
    }

    params = {}

    if after is not None:
        params = {
            "limit": "50",
            "after": after
        }

    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise RuntimeError(response.status_code)

    data = json.loads(response.content)
    return data["items"] + get_recently_played(spotify_oath, url=data["next"])

def main():
    spotify_oath = load_oauth()

    with shelve.open("tracks.shelve") as d:
        if "tranks" not in d:
            d["tracks"] = []

        if "current_time" not in d:
            d["current_time"] = int(time.time())

        new_tracks = get_recently_played(spotify_oath, after=d["current_time"] - 1)
        print(f"Added {len(new_tracks)}")

        d["tracks"] += new_tracks
        d["current_time"] = int(time.time())

if __name__ == "__main__":
    main()