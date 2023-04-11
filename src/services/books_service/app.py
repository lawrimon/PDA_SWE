"""This application is the books service.

This service provides an endpoint to get the books of best sellers lists based on the user's genre preferences.
The functionality is based on the New York Times API.

Typical endpoints usage:

    GET /books?genre=fiction
"""

from flask import Flask, jsonify, request
import requests
import dotenv
import os

app = Flask(__name__)

dotenv.load_dotenv()
NYTIMES_API_KEY = os.getenv("NYTIMES_API_KEY")


@app.route("/books")
def get_books():
    """Books endpoint.

    This endpoint provides the books of best sellers lists based on the user's genre preferences.

    Args:
        genre: The genre of the best sellers list. Only one genre can be selected. Can be "combined-print-and-e-book-fiction", "combined-print-and-e-book-nonfiction", "advice-how-to-and-miscellaneous", "picture-books".

    Returns:
        Information about the books on the requested best sellers list.
    """

    if not request.args.get("genre"):
        return jsonify({"error": "Missing parameters"}), 400
    
    genres = [
        "combined-print-and-e-book-fiction",
        "combined-print-and-e-book-nonfiction",
        "advice-how-to-and-miscellaneous",
        "picture-books",
   ]

    if request.args.get("genre") not in genres:
        return jsonify({"error": "Invalid parameters"}), 400
    
    genre = request.args.get("genre")

    url = f"https://api.nytimes.com/svc/books/v3/lists.json"
    params = {
        "list": genre,
        "api-key": NYTIMES_API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Error getting books information"}), 500

    data = response.json()

    books = []
    for book in data["results"]:
        books.append(
            {
                "title": book["book_details"][0]["title"],
                "author": book["book_details"][0]["author"],
                "description": book["book_details"][0]["description"],
                "publisher": book["book_details"][0]["publisher"],
                "rank": book["rank"],
                "weeks_on_list": book["weeks_on_list"],
            }
        )

    return jsonify(books)