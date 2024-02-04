import csv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import requests
import uvicorn


class Playlist:
    def __init__(self, name, songs):
        self.name = name
        self.songs = songs

    def __str__(self):
        print(f"{self.name} = [{str(self.songs)}]")


class Song:
    def __init__(self, title, album, artist):
        self.title = title
        self.album = album
        self.artist = artist

    def __str__(self):
        print(f"{self.title},{self.album},{self.artist}")


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

playlist = None

app = FastAPI()


def get_access_token(auth_code: str):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
        },
        auth=(client_id, client_secret),
    )
    access_token = response.json()["access_token"]
    return {"Authorization": "Bearer " + access_token}


@app.get("/")
async def auth():
    print(client_id)
    print(client_secret)
    print(redirect_uri)

    playlist_name = "Beatles"
    with open(f"{playlist_name}.csv") as csv_file:
        playlist = Playlist(name=playlist_name, songs=[])
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                song = Song(title=row[0], album=row[1], artist=row[2])
                playlist.songs.append(song)
            line_count += 1

    print(f"Playlist {str(playlist)} processed.")

    scope = ["playlist-modify-private", "playlist-modify-public"]
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={' '.join(scope)}"
    return HTMLResponse(content=f'<a href="{auth_url}">Authorize</a>')


@app.get("/callback")
async def callback(code):
    headers = get_access_token(code)
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    user_id = response.json()["id"]

    name = "Test playlist"
    description = "Test playlist"

    params = {
        "name": name,
        "description": description,
        "public": False,
    }

    # Create playlist
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = requests.post(url=url, headers=headers, json=params)
    playlist_id = response.json()["id"]

    # For list of songs

    # 1. Search for a song
    # https://api.spotify.com/v1/search?q=track%3AXXXXXX%2520artist%3AYYYYY%2520YYYYYY&type=track
    # f"spotify:track:{tracks.items[0].id}"

    # 2. Add song to playlist
    track_uri = "spotify:track:319eU2WvplIHzjvogpnNc6"
    response = requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json={"uris": [track_uri]},
    )
    if response.status_code == 201:
        return {"message": "Track added successfully!"}
    else:
        return {"error": response.json()}


def start():
    uvicorn.run(app)
