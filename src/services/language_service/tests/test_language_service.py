import pytest
from flask import json
from language_service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.parametrize(
    "transcript, expected_response",
    [
        (
            "tell me about the latest news",
            {
                "intent": "scuttlebutt",
                "date_time": "2023-04-30T10:30:00",
                "artist": None,
                "service": "news",
            },
        ),
        (
            "play some music",
            {
                "intent": "racktime",
                "date_time": "2023-04-30T10:30:00",
                "artist": "drake",
                "service": "music",
            },
        ),
        (
            "tell me some interesting quotes",
            {
                "intent": "shoreleave",
                "date_time": "2023-04-30T10:30:00",
                "artist": None,
                "service": "wisdom",
            },
        )(
            "what events can i go to",
            {
                "intent": "lookoutduty",
                "date_time": "2023-04-30T10:30:00",
                "artist": "Avril Lavigne",
                "service": "event",
            },
        ),
    ],
)
def test_get_intent(client, transcript, expected_response):
    """Test the intent recognition endpoint

    This test checks if the intent recognition web app returns the correct intent and correct parameters
    """
    response = client.get(f"/dialogflow/get_intent?transcript={transcript}")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert json.loads(response.data) == expected_response
