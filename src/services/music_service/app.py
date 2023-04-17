"""This application is the music service.

This service provides an endpoint to play music.
A Spotify account is required and the Spotify device must be open.
The functionality is based on the Spotify API.

Typical endpoints usage:

    GET /music?artist=RIN&track=Sternenstaub
    GET /music?artist=RIN
    GET /music?track=Sternenstaub
"""

from flask import Flask, jsonify, request
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from pprint import pprint
import dotenv
import os

app = Flask(__name__)

dotenv.load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")


@app.route("/music")
def get_music():
    """Music endpoint.

    This endpoint plays the requested track on the Spotify device.

    Args:
        artist: The artist of the track.
        track: The track name. Either artist or track must be given.
        prod: If True, the production spotipy object is used. Otherwise the test spotipy object is used.

    Returns:
        Acknowledgement message.
    """

    if not request.args.get("artist") and not request.args.get("track"):
        return jsonify({"error": "Missing parameters"}), 400

    scope = "user-read-playback-state,user-modify-playback-state"
    sp_oauth = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
        )
    )

    invalid, tracklist = invalid_music_parameters(request.args, sp_oauth)

    if invalid:
        return jsonify({"error": "Invalid parameters"}), 400

    res = sp_oauth.devices()
    pprint(res)

    # check if there is a device available
    if len(res["devices"]) == 0:
        return (
            jsonify(
                {"error": "No device available. Please open Spotify on your device."}
            ),
            400,
        )

    track_id = tracklist["tracks"]["items"][0]["uri"]

    sp_oauth.start_playback(uris=[track_id], device_id=res["devices"][0]["id"])
    return jsonify({"message": "Playing music"})


def invalid_music_parameters(args, sp):
    """Check if the music parameters are invalid.

    The parameters are invalid if no song is found.

    Args:
        args: The music parameters.
        sp: The spotipy object.

    Returns:
        True if the parameters are invalid, otherwise False and the tracklist.
    """

    if args.get("artist") and args.get("track"):
        tracklist = sp.search(
            q=f"artist:{args.get('artist')} track:{args.get('track')}", type="track"
        )
    elif args.get("artist"):
        tracklist = sp.search(q=f"artist:{args.get('artist')}", type="track")
    elif args.get("track"):
        tracklist = sp.search(q=f"track:{args.get('track')}", type="track")

    if len(tracklist["tracks"]["items"]) == 0:
        return True, None
    else:
        return False, tracklist
