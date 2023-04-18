"""This application is the shore leave use case.

The shore leave use case provides the user with some wisdom and entertainment.

Example Usage:

    GET /shoreleave?user=cr7thegoat
"""


from flask import Flask, jsonify, request
import requests, flask_cors


app = Flask(__name__)
flask_cors.CORS(app)


def get_quotes():
    """Get quotes.

    This functions calls the quotes endpoint of the wisdom service and returns the quotes.

    Returns:
        The quotes or an explanatory string if no quotes information could be retrieved.
    """

    url = "http://wisdom:5000/wisdom/quotes"
    response = requests.get(url)
    if response.status_code != 200:
        return "No quotes found. "
        # jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()
    answer = "Here are some famous quotes: "
    for quote in data:
        answer += (
            "The quote " + quote["quote"] + " by the author " + quote["author"] + ". "
        )

    return answer


def get_nasa_apod():
    """Get NASA fact of the day.

    This functions calls the apod endpoint of the wisdom service and returns a NASA fact of the day.

    Returns:
        The NASA fact of the day or an explanatory string if no fact could be retrieved.
    """

    url = "http://wisdom:5000/wisdom/apod"
    response = requests.get(url)
    if response.status_code != 200:
        return "No NASA fact of the day found. "
        # jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()
    answer = "Here is your NASA fact of the day: "
    answer += data["explanation"] + " "

    return answer


def get_random_facts():
    """Get random facts.

    This functions calls the random_facts endpoint of the wisdom service and returns random facts.

    Returns:
        The random facts or an explanatory string if no facts could be retrieved.
    """

    url = "http://wisdom:5000//wisdom/random_facts"
    response = requests.get(url)
    if response.status_code != 200:
        return "No random facts found. "
        # jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()
    answer = "Here are some random facts that might be interesting for you: "
    for fact in data:
        answer += fact["fact"]
        answer += " "

    return answer


def get_books(book_genre):
    """Get books best sellers list.

    This functions calls the books endpoint of the wisdom service and returns the best sellers list of a given genre.

    Args:
        book_genre: The genre of the books to be retrieved. Only one genre can be selected.

    Returns:
        Information about the resepctive best sellers list or an explanatory string if no books could be retrieved.
    """

    genres = {
        "Non-Fiction": "combined-print-and-e-book-nonfiction",
        "Fiction": "combined-print-and-e-book-fiction",
        "Picture Books": "picture-books",
        "Miscellaneous": "advice-how-to-and-miscellaneous",
    }

    url = "http://books:5000/books"
    params = {"genre": genres[book_genre]}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "No best sellers list found for the provided genre. "
        # jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()
    if not data:
        return "The best sellers list for your favorite genre is currently empty. "
    answer = "Here are some books that might be interesting for you: "
    for book in data:
        answer += book["title"] + " by the author " + book["author"] + ". "
        answer += "This is the description: " + book["description"] + " "

    return answer


def get_user_preferences(user):
    """Get user preferences.

    This functions calls the user endpoint of the database service and returns the user preferences.

    Args:
        user: The username of the user. Only one username can be selected.

    Returns:
        The user preferences.
    """

    url = "http://db:5000/users/" + user
    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting user preferences"}), 500

    data = response.json()

    return data


@app.route("/shoreleave")
def get_shoreleave():
    """Shore leave endpoint.

    This endpoint provides the shore leave use case logic.

    Args:
        user: The username of the user. Only one username can be selected.

    Returns:
        The shore leave information containing quotes, NASA fact of the day, random facts and books best sellers list.
    """

    if not request.args.get("user"):
        return jsonify({"error": "Missing parameters"}), 400

    user = request.args.get("user")

    user_preferences = get_user_preferences(user)
    book_genre = user_preferences["books"].split(",")[0]

    quotes = get_quotes()
    nasa_fact = get_nasa_apod()
    random_facts = get_random_facts()
    books = get_books(book_genre)
    name = "shoreleave"
    return jsonify(
        {
            "_name": name,
            "quotes": quotes,
            "nasa_fact": nasa_fact,
            "random_facts": random_facts,
            "books": books,
        }
    )


if __name__ == "__main__":
    app.run()
