import requests, os, json, time, shelve
from datetime import datetime
from itertools import takewhile

def get_access_token(auth_code: str):
    url = "https://accounts.spotify.com/api/token"

    paylpad = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
    }

    auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

    response = requests.post(url, data = payload, auth = auth)
    return response.json()["access_token"]



def load_oauth(file = "spotify_oauth"):
    try:
        return open(file).read().strip()
    except FileNotFoundError as e:
        print("You need to create a file called 'spotify_oauth' with the Spotify OAuth token\n\
            Navigate to https://developer.spotify.com/console/get-recently-played and click 'Get token'")
        exit(-1)


def save_last_tracks(spotify_oath, database):
    url = "https://api.spotify.com/v1/me/player/recently-played"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + spotify_oath,
    }

    params = {
        "limit": 50,
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(response.status_code)

    data = json.loads(response.content)

    if database["tracks"] == []:
        new_tracks = data["items"][::-1]
    else:
        new_tracks = [track for track in data["items"][::-1]
            if datetime.fromisoformat(track["played_at"]) >
                datetime.fromisoformat(database["tracks"][-1]["played_at"])
        ]

    print(f"Added {len(new_tracks)} tracks")
    database["tracks"].extend(new_tracks)


if __name__ == "__main__":
    spotify_oath = load_oauth()

    with shelve.open("tracks.shelve") as database:
        if "tracks" not in database:
            database["tracks"] = []
            
        save_last_tracks(spotify_oath, database)
