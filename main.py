from fastapi import FastAPI, Query
from musicxmatch_api import MusixMatchAPI

app = FastAPI()
mx = MusixMatchAPI()

@app.get("/")
def home():
    return {"status": "Musixmatch API running"}

# 🔍 Search track
@app.get("/search")
def search_track(q: str):
    data = mx.search_track(q=q)
    return data

# 🎵 Get track details
@app.get("/track")
def get_track(track_id: int):
    data = mx.get_track(track_id=track_id)
    return data

# 📜 Get lyrics
@app.get("/lyrics")
def get_lyrics(track_id: int):
    data = mx.get_track_lyrics(track_id=track_id)
    return data

# 🎤 Artist details
@app.get("/artist")
def get_artist(artist_id: int):
    data = mx.get_artist(artist_id=artist_id)
    return data

# 💿 Album details
@app.get("/album")
def get_album(album_id: int):
    data = mx.get_album(album_id=album_id)
    return data

# 📈 Charts (top songs)
@app.get("/charts")
def charts(country: str = "in"):
    data = mx.get_chart_tracks(country=country)
    return data

# 🔥 Trending artists
@app.get("/trending-artists")
def trending_artists(country: str = "in"):
    data = mx.get_chart_artists(country=country)
    return data