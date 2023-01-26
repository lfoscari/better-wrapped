import shelve, os

with shelve.open("tracks.shelve") as database:
    for track in database["tracks"][-10:]:
        print(track["played_at"])

    print(f"Total tracks: {len(database['tracks'])}")
    print(f"Total size: {os.path.getsize('tracks.shelve') / 1_000}KB")