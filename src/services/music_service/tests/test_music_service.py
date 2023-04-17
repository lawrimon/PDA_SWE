import pytest
from music_service.app import app

@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()

@pytest.mark.parametrize(
    "artist,track,expected_status_code,expected_error",
    [
        ("RIN", "Sternenstaub", 400, "No device available. Please open Spotify on your device."),
        ("RIN", None, 400, "No device available. Please open Spotify on your device."),
        (None, "Sternenstaub", 400, "No device available. Please open Spotify on your device."),
        (None, None, 400, "Missing parameters"),
        ("12123213213121", "2131313113123", 400, "Invalid parameters"),
    ],
)
def test_get_music(client, artist, track, expected_status_code, expected_error):
    """Test the music endpoint.

    This test checks if the music endpoint returns the correct status code and error message.
    If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get("/music", query_string={"artist": artist, "track": track})
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
    else:
        data = response.json
        assert "message" in data
        assert data["message"] == "Playing music"