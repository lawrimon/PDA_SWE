"""This application is the coding service.

This service provides an endpoint to get the open issues assigned to a user.
The functionality is based on the GitHub API.

Typical endpoints usage:

    GET /issues?username=octocat
"""

from flask import Flask, jsonify, request
import requests
import dotenv
import os
from pprint import pprint

app = Flask(__name__)

dotenv.load_dotenv()
CODING_API_KEY = os.getenv("CODING_API_KEY")


@app.route("/issues")
def get_issues():
    """Issues endpoint.

    This endpoint provides the open issues assigned to a user.

    Args:
        username: The username of the user. Only one username can be selected.

    Returns:
        Information about the open issues assigned to the user.
    """

    if not request.args.get("username"):
        return jsonify({"error": "Missing parameters"}), 400

    # check if user exists
    check_user_url = f"https://api.github.com/users/{request.args.get('username')}"
    check_user_headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {CODING_API_KEY}",
    }
    check_user_response = requests.get(check_user_url, headers=check_user_headers)
    if check_user_response.status_code != 200:
        print(check_user_response.json())
        return jsonify({"error": "Invalid parameters"}), 400

    username = request.args.get("username")

    url = f"https://api.github.com/search/issues"
    params = {
        "q": f"assignee:{username} is:open",
        "sort": "updated",
        "order": "desc",
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {CODING_API_KEY}",
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print(response.json())
        return jsonify({"error": "Error getting issues information"}), 500

    issues = []
    for issue in response.json()["items"]:
        issues.append(
            {
                "title": issue["title"],
                "url": issue["html_url"],
                "state": issue["state"],
                "repository_url": issue["repository_url"],
                "repository": issue["repository_url"].split("/")[-1],
                "assignee": issue["assignee"]["login"],
                "created_at": issue["created_at"],
                "updated_at": issue["updated_at"],
                # "description": issue["body"],
                # "labels": [label["name"] for label in issue["labels"]],
            }
        )
        if issue["body"]:
            issues[-1]["description"] = issue["body"]
        else:
            issues[-1]["description"] = "No description provided"
        if issue["labels"]:
            issues[-1]["labels"] = [label["name"] for label in issue["labels"]]
        else:
            issues[-1]["labels"] = ["No labels provided"]

    return jsonify(issues)
