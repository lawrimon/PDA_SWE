import pytest
from fakeredis import FakeStrictRedis
from database.app import app
import json


@pytest.fixture
def client():
    """Create a test client for the app."""

    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def fake_redis(monkeypatch):
    """Replace the redis_store with a fake redis instance."""
    redis = FakeStrictRedis()
    monkeypatch.setattr("database.app.redis_store", redis)
    return redis


@pytest.mark.parametrize(
    "user_id, preferences",
    [
        ("user1", {"language": "en", "football_club": "Real Madrid"}),
        ("user2", {"username": "johndoe", "password": "password123"}),
    ],
)
def test_add_user(client, fake_redis, user_id, preferences):
    response = client.post("/users", json={"user_id": user_id, **preferences})
    assert response.status_code == 200
    assert json.loads(response.data) == {"status": "success, user added"}

    # check if the user was added to Redis with correct preferences
    for key, value in preferences.items():
        assert fake_redis.hget(user_id, key).decode() == str(value)


@pytest.mark.parametrize(
    "user_id, initial_preferences, updated_preferences, expected_preferences",
    [
        (
            "user1",
            {"language": "en", "football_club": "Real Madrid"},
            {"language": "es", "football_club": "Barcelona"},
            {"language": "es", "football_club": "Barcelona"},
        ),
        (
            "user2",
            {"username": "johndoe", "password": "password123"},
            {"password": "newpassword"},
            {"username": "johndoe", "password": "newpassword"},
        ),
    ],
)
def test_update_user(
    client,
    fake_redis,
    user_id,
    initial_preferences,
    updated_preferences,
    expected_preferences,
):
    # add user to Redis with initial preferences
    for key, value in initial_preferences.items():
        fake_redis.hset(user_id, key, value)

    response = client.put(f"/users/{user_id}", json=updated_preferences)
    assert response.status_code == 200
    assert json.loads(response.data) == {"status": "success, user updated"}

    # check if the user preferences were updated in Redis
    for key, value in expected_preferences.items():
        assert fake_redis.hget(user_id, key).decode() == str(value)


@pytest.mark.parametrize(
    "user_id, preferences",
    [
        ("user1", {"language": "en", "football_club": "Real Madrid"}),
        ("user2", {"username": "johndoe", "password": "password123"}),
    ],
)
def test_get_user(client, fake_redis, user_id, preferences):
    # add user to Redis with preferences
    for key, value in preferences.items():
        fake_redis.hset(user_id, key, value)

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert json.loads(response.data) == preferences


@pytest.mark.parametrize("user_id", ["user1", "user2"])
def test_delete_user(client, fake_redis, user_id):
    # add user to Redis
    fake_redis.hset(user_id, "language", "en")

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert json.loads(response.data) == {"status": "success, user deleted"}

    # check if the user was deleted from Redis
    assert not fake_redis.exists(user_id)
