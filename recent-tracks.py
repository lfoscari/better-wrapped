import requests, os, json, time, shelve
from datetime import date, datetime

def get_year():
    try:
        year = int(input("Download data from year > "))
        if not 2010 <= year <= date.today().year: raise ValueError
    except ValueError:
        print(f"Insert a valid year from 2010 to {date.today().year}")
        exit(-1)

    after = date.fromisoformat(f"{year}-01-01")
    after = int(time.mktime(after.timetuple()) * 1000) - 1

    before = date.fromisoformat(f"{year}-12-31")
    before = int(time.mktime(before.timetuple()) * 1000) - 1

    return after, before

def load_oauth(file = "spotify_oauth"):
    try:
        return open(file).read().strip()
    except FileNotFoundError as e:
        print("You need to create a file called 'spotify_oauth' with the Spotify OAuth token\n\
            Navigate to https://developer.spotify.com/console/get-recently-played and click 'Get token'")
        exit(-1)

def tracks_played_between(after, before, spotify_oath):
    url = "https://api.spotify.com/v1/me/player/recently-played"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + spotify_oath,
    }

    params = {
        "limit": 50,
        "before": before
    }

    data = {}
    tracks = []

    while True:
        print("CALL")
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(response.status_code)

        data = json.loads(response.content)
        tracks += data["items"]

        if data["next"] is None:
            print("NO MORE")
            break

        last = datetime.fromisoformat(data["items"][-1]["played_at"])
        last = int(datetime.timestamp(last))

        if last < after:
            print("TOO LATE", last, after)
            break
        
        params["before"] = last

    return tracks

def main():
    spotify_oath = load_oauth()
    after, before = get_year()

    print(f"{after=} {before=}")

    with shelve.open("tracks.shelve") as d:
        # TODO: insert directly into the database
        d["tracks"] = tracks_played_between(after, before, spotify_oath)

if __name__ == "__main__":
    main()