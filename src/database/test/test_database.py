import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.mark.parametrize("user_id, preferences, expected_response", [
    ("user1", {"language": "english", "football_club": "Barcelona"}, {"language": "english", "football_club": "Barcelona"}),
    ("user2", {"password": "123456", "stocks": "AAPL"}, {"stocks": "AAPL"}),
    ("user3", {"username": "johndoe", "password": "mypassword", "calendar_link": "https://mycalendar.com"}, {"username": "johndoe", "calendar_link": "https://mycalendar.com"}),
    ("user4", {}, {"error": "Error getting preferences"}),
    ])

def test_manage_preferences(client, user_id, preferences, expected_response):
    res = client.post(f"/preferences/{user_id}", json=preferences)
    assert res.status_code == 200
    assert res.json == expected_response

    res = client.get(f"/preferences/{user_id}")
    assert res.status_code == 200
    assert res.json == preferences