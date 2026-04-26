from fastapi import FastAPI, Query
import requests
import time
from musicxmatch_api import MusixMatchAPI

app = FastAPI()
mx = MusixMatchAPI()

# -------------------------
# ✅ Helper: Safe request
# -------------------------
def safe_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    for _ in range(3):  # retry 3 times
        try:
            response = requests.get(url, headers=headers, timeout=10)

            # 🔥 Prevent JSON crash
            if "application/json" not in response.headers.get("Content-Type", ""):
                return {
                    "error": "Non-JSON response (likely blocked)",
                    "status_code": response.status_code,
                    "preview": response.text[:300]
                }

            return response.json()

        except Exception as e:
            time.sleep(1)

    return {"error": "Request failed after retries"}


# -------------------------
# 🏠 Home
# -------------------------
@app.get("/")
def home():
    return {"status": "Musixmatch API running"}


# -------------------------
# 🔍 Search track
# -------------------------
@app.get("/search")
def search_track(q: str):
    try:
        return mx.search_track(q=q)
    except Exception as e:
        return {"error": str(e)}


# -------------------------
# 🎵 Track details
# -------------------------
@app.get("/track")
def get_track(track_id: int):
    try:
        return mx.get_track(track_id=track_id)
    except Exception as e:
        return {"error": str(e)}


# -------------------------
# 📜 Lyrics (FIXED)
# -------------------------
@app.get("/lyrics")
def get_lyrics(track_id: int):
    url = f"https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id={track_id}"

    data = safe_request(url)

    # If blocked or failed
    if "error" in data:
        return data

    try:
        lyrics = (
            data.get("message", {})
                .get("body", {})
                .get("lyrics", {})
                .get("lyrics_body")
        )

        if not lyrics:
            return {"error": "Lyrics not found"}

        return {"lyrics": lyrics}

    except Exception as e:
        return {"error": str(e)}


# -------------------------
# 🎤 Artist details
# -------------------------
@app.get("/artist")
def get_artist(artist_id: int):
    try:
        return mx.get_artist(artist_id=artist_id)
    except Exception as e:
        return {"error": str(e)}


# -------------------------
# 💿 Album details
# -------------------------
@app.get("/album")
def get_album(album_id: int):
    try:
        return mx.get_album(album_id=album_id)
    except Exception as e:
        return {"error": str(e)}


# -------------------------
# 📈 Charts
# -------------------------
@app.get("/charts")
def charts(country: str = "in"):
    try:
        return mx.get_chart_tracks(country=country)
    except Exception as e:
        return {"error": str(e)}


# -------------------------
# 🔥 Trending artists
# -------------------------
@app.get("/trending-artists")
def trending_artists(country: str = "in"):
    try:
        return mx.get_chart_artists(country=country)
    except Exception as e:
        return {"error": str(e)}


# -------------------------
# 🧪 Debug endpoint (VERY IMPORTANT)
# -------------------------
@app.get("/debug")
def debug(track_id: int):
    url = f"https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id={track_id}"
    return safe_request(url)