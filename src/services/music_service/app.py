"""This application is the music service.

This service provides an endpoint to play music.
The functionality is based on the Spotify API.

Typical endpoints usage:

    GET /music?track=track_id
"""

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route("/music")
def get_music():
    """Music endpoint.
    
    This endpoint plays the requested track.

    Args:
        track: The id of the track to be played.
    """
    
        