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
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

app = Flask(__name__)


@app.route("/music")
def get_music():
    """Music endpoint.

    This endpoint plays the requested track on the Spotify device.

    Args:
        artist: The artist of the track.
        track: The track name. Either artist or track must be given.

    Returns:
        Acknowledgement message.
    """

    scope = "user-read-playback-state,user-modify-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # check if parameters are given, either artist or track must be given
    if not request.args.get("artist") and not request.args.get("track"):
        return jsonify({"error": "Missing parameters."}), 400

    # check for valid parameters
    if request.args.get("artist") and request.args.get("track"):
        tracklist = sp.search(
            q=f"artist:{request.args.get('artist')} track:{request.args.get('track')}",
            type="track",
        )
    elif request.args.get("artist"):
        tracklist = sp.search(
            q=f"artist:{request.args.get('artist')}", type="track"
        )
    elif request.args.get("track"):
        tracklist = sp.search(q=f"track:{request.args.get('track')}", type="track")

    if len(tracklist["tracks"]["items"]) == 0:
        return jsonify({"error": "Invalid parameters."}), 400

    res = sp.devices()
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

    sp.start_playback(uris=[track_id], device_id=res["devices"][0]["id"])
    return jsonify({"message": "Playing music"})
