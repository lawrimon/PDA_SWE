# import pytest
# from fakeredis import FakeStrictRedis
# from database.app import app

# @pytest.fixture
# def client():

#     """Create a test client for the app."""

#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         with app.app_context():
#             yield client

# @pytest.mark.parametrize("user_id, data, expected_response", [
#     ("user1", {"language": "en", "stocks": "AAPL"}, {'language': 'en', 'stocks': 'AAPL'}),
#     ("user2", {"language": "fr", "spotify_link": "https://open.spotify.com/"}, {'language': 'fr', 'spotify_link': 'https://open.spotify.com/'}),
#     ("user3", {"password": "mypassword"}, {"error": "Error getting preferences"})
# ])

# def test_manage_preferences(client, user_id, data, expected_response):
#     # POST request to set preferences
#     response = client.post(f'/preferences/{user_id}', json=data)
#     assert response.status_code == 200
#     assert response.json == {'status': 'success'}

#     # GET request to retrieve preferences
#     response = client.get(f'/preferences/{user_id}')
#     assert response.status_code == 200
#     assert response.json == expected_response







import pytest
from fakeredis import FakeStrictRedis
from database.app import app

@pytest.fixture
def client():

    """Create a test client for the app."""

    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def fake_redis(monkeypatch):
    """Replace the redis_store with a fake redis instance."""
    redis = FakeStrictRedis()
    monkeypatch.setattr('database.app.redis_store', redis)
    return redis

# @pytest.mark.parametrize("user_id, data, expected_response","code_expected", [
#     ("user1", {"language": "en", "stocks": "AAPL"}, {'language': 'en', 'stocks': 'AAPL'}, 200),
#     ("user2", {"language": "fr", "spotify_link": "https://open.spotify.com/"}, {'language': 'fr', 'spotify_link': 'https://open.spotify.com/'}, 200),
#     ("user3", {"invalidKey": "mypassword"}, {"error": "Error getting preferences. No preferences found"}, 200),
#     ("user4", {"password": "mypassword"}, {"error": "Error getting preferences. No preferences found"}, 200)
# ])

@pytest.mark.parametrize("user_id, data, expected_response, code_expected", [
    ("user1", {"language": "en", "stocks": "AAPL"}, {'language': 'en', 'stocks': 'AAPL'}, 200),
    ("user2", {"language": "fr", "spotify_link": "https://open.spotify.com/"}, {'language': 'fr', 'spotify_link': 'https://open.spotify.com/'}, 200),
    ("user3", {"invalidKey": "mypassword"}, {"error": "Error getting preferences. No preferences found"}, 500),
    ("user4", {"password": "mypassword"}, {"error": "Error getting preferences. No preferences found"}, 500)
])
def test_manage_preferences(client, fake_redis, user_id, data, expected_response, code_expected):
    # POST request to set preferences
    if user_id != "user4":
        response = client.post(f'/preferences/{user_id}', json=data)  
        assert response.status_code == 200
        assert response.json == {'status': 'success'}
    

    # GET request to retrieve preferences
    response = client.get(f'/preferences/{user_id}')
    assert response.status_code == code_expected
    assert response.json == expected_response