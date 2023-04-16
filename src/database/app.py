"""This application is the database service.

The database service provides endpoints to store and retrieve user preferences in the Redis database.

Typical endpoints usage:

    POST /users
    GET /users/<user_id>'
    PUT /users/<user_id>'
"""

from flask import Flask, request, jsonify
from flask_redis import FlaskRedis
from flask_cors import CORS

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://redis:6379/0"
redis_store = FlaskRedis(app)
CORS(app)
allowed_keys = [
    "language",
    "football_club",
    "username",
    "password",
    "stocks",
    "artists",
    "spotify_link",
    "calendar_link",
    "news",
    "location",
    "books",
    "coordinates",
    "github",
    "event_location",
    "transportation"
]


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    This function retrieves the preferences for the given user from Redis and returns them as a JSON object.

    Args:
        user_id: The ID of the user whose preferences should be retrieved.

    Returns:
        A JSON object containing the preferences for the specified user.
    """

    if not redis_store.exists(user_id):
        return jsonify({"error": "Error getting user. User or password incorrect"}), 404
    else:
        keys = redis_store.hkeys(user_id)
        preferences = {}
        for key in keys:
            preferences[key.decode()] = redis_store.hget(user_id, key).decode()
        return jsonify(preferences)


@app.route("/users", methods=["POST"])
def add_user():
    """
    This function adds a new user and their preferences to Redis, provided that the user does not already exist.

    Args:
        user_id: The ID of the user to be added.
        preferences: A dictionary of the user's preferences.
        Payload: {"user_id":"user1", "password": "myPassword", "username": "username2", "football_club": "Real Madrid"}
    Returns:
        A JSON object indicating whether the operation was successful.
    """
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Error adding user. Missing user_id field"}), 400
    if redis_store.exists(user_id):
        return jsonify({"error": "Error adding user. User already exists"}), 409
    for key, value in data.items():
        if key in allowed_keys:
            redis_store.hset(user_id, key, value)
    return jsonify({"status": "success, user added"})


@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """
    This function updates the preferences for the given user in Redis, provided that the user exists.

    Args:
        user_id: The ID of the user whose preferences should be updated.
        preferences: A dictionary of the new preferences.
        Payload: {"password": "myPassword", "username": "username2", "football_club": "Real Madrid"}

    Returns:
        A JSON object indicating whether the operation was successful.
    """
    if not redis_store.exists(user_id):
        return jsonify({"error": "Error updating user. User not found"}), 404

    data = request.json
    for key, value in data.items():
        if key in allowed_keys:
            redis_store.hset(user_id, key, value)
    return jsonify({"status": "success, user updated"})


@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    This function deletes the preferences for the given user from Redis, provided that the user exists.

    Args:
        user_id: The ID of the user whose preferences should be deleted.

    Returns:
        A JSON object indicating whether the operation was successful.
    """
    if not redis_store.exists(user_id):
        return jsonify({"error": "Error deleting user. User not found"}), 404
    redis_store.delete(user_id)
    return jsonify({"status": "success, user deleted"})


@app.route("/allusers", methods=["GET"])
def get_all_users():
    """
    This function retrieves all user IDs from Redis and returns them as a JSON array.

    Returns:
        A JSON array containing all the user IDs.
    """
    user_ids = redis_store.keys("*")
    return jsonify([user_id.decode() for user_id in user_ids])


if __name__ == "__main__":
    app.run(host="0.0.0.0")
