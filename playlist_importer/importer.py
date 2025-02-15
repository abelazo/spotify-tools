import csv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
import os
import requests
import urllib.parse
import uvicorn
import time

from .domain import Playlist, Song

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client_id = os.environ["SPOTIFY_CLIENT_ID"]
client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
redirect_uri = os.environ["SPOTIFY_REDIRECT_URI"]
playlists_folder = os.environ["PLAYLISTS_FOLDER"]
project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
working_folder = f"{project_root_dir}/{playlists_folder}"

playlist: Playlist

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
    playlist_name = "TW_Basf"
    with open(f"{working_folder}/{playlist_name}.csv") as csv_file:
        global playlist
        playlist = Playlist(name=playlist_name, songs=[])
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                logging.info(f'Column names are {", ".join(row)}')
            else:
                song = Song(title=row[0], album=row[1], artist=row[2])
                playlist.songs.append(song)
            line_count += 1

    logging.info(f"Playlist read: {playlist}")

    scope = ["playlist-modify-private", "playlist-modify-public"]
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={' '.join(scope)}"
    return HTMLResponse(content=f'<a href="{auth_url}">Import</a>')


#     for filename in os.listdir(working_folder):
#         f = os.path.join(working_folder, filename)
#         # checking if it is a file
#         if os.path.isfile(f):
#             logging.info(f"Playlist read: {f}")
#     return HTMLResponse(content=f'Done')


def post_with_retry(url, headers, params):
    response = requests.post(url=url, headers=headers, params=params)

    if response.status_code == 429:
        retry_after = int(response.headers["Retry-After"])
        logger.warning(f"Rate limit exceeded for POST. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)

    return post_with_retry(url, headers, params)


def get_with_retry(url, headers):
    response = requests.get(url=url, headers=headers)

    if response.status_code == 429:
        retry_after = int(response.headers["Retry-After"])
        logger.warning(f"Rate limit exceeded for GET. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)

    return get_with_retry(url, headers)


@app.get("/callback")
async def callback(code):
    headers = get_access_token(code)
    response = get_with_retry("https://api.spotify.com/v1/me", headers=headers)
    user_id = response.json()["id"]

    name = playlist.name
    description = f"{playlist.name}"

    params = {
        "name": name,
        "description": description,
        "public": False,
    }

    # Create playlist
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = post_with_retry(url=url, headers=headers, params=params)
    playlist_id = response.json()["id"]

    # Add all songs in the file
    for working_song in playlist.songs:
        # 1. Search for a song
        query = f"track:{working_song.title} artist:{working_song.artist} album:{working_song.album}"
        params = {"q": urllib.parse.quote_plus(query), "type": "track"}
        logger.debug(f"Search parameters: {urllib.parse.urlencode(params)}")
        url = f"https://api.spotify.com/v1/search?{urllib.parse.urlencode(params)}"
        response = get_with_retry(url, headers=headers)

        # 2. Add song to playlist
        try:
            spotify_url = response.json()["tracks"]["items"][0]["external_urls"]["spotify"]
            logger.info(f"Adding track {working_song}: {spotify_url}")

            result_album = response.json()["tracks"]["items"][0]["album"]["name"]
            if result_album != working_song.album:
                logger.warning(f"Album '{result_album}' does not match with expected album '{working_song.album}'")

            track_uri = response.json()["tracks"]["items"][0]["uri"]
            response = post_with_retry(
                url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
                headers=headers,
                params={"uris": [track_uri]},
            )
        except KeyError:
            logger.error(f"Search results were empty. Could not add song {working_song} to the playlist")

    return {"message": "Playlist added successfully!"}


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)
