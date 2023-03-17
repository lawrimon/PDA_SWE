"""This application is the database service.

The database service provides endpoints to store and retrieve user preferences in the Redis database.

Typical endpoints usage:

    POST /preferences/<user_id>'
    GET /preferences/<user_id>'
"""

from flask import Flask, request, jsonify
from flask_redis import FlaskRedis
from flask_cors import CORS

app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://redis:6379/0'
redis_store = FlaskRedis(app)
CORS(app)

@app.route('/preferences/<user_id>', methods=['GET', 'POST'])
def manage_preferences(user_id):
    """
    This function handles both GET and POST requests.
    When a POST request is received, it stores the preferences for the given user in Redis.
    When a GET request is received, it retrieves all preferences for the given user from Redis and returns them as a JSON object.
    """

    allowed_keys = ['language', "football_club", "username" ,"password","stocks", "artists", "spotify_link", "calendar_link"]
    if request.method == 'POST':
        data = request.json
        for key, value in data.items():
            if key in allowed_keys:
                redis_store.hset(user_id, key, value)
        return jsonify({'status': 'success'})
    else:
        keys = redis_store.hkeys(user_id)
        preferences = {}
        if keys:
            for key in keys:
                preferences[key.decode()] = redis_store.hget(user_id, key).decode()
            return jsonify(preferences)
        else:
            return jsonify({"error": "Error getting preferences"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0")