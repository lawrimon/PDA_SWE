"""Thhe following tests run only with Docker containers running."""

import pytest
from shoreleave.app import app, get_books, get_quotes, get_nasa_apod, get_random_facts


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


def test_get_quotes():
    """Test the get_quotes function.

    This test checks if the get_quotes function returns the expected result.
    """

    quote = get_quotes()
    assert isinstance(quote, str)


def test_get_nasa_apod():
    """Test the get_nasa_apod function.

    This test checks if the get_nasa_apod function returns the expected result.
    """

    nasa_fact = get_nasa_apod()
    assert isinstance(nasa_fact, str)


def test_get_random_facts():
    """Test the get_random_facts function.

    This test checks if the get_random_facts function returns the expected result.
    """

    random_facts = get_random_facts()
    assert isinstance(random_facts, str)


def test_get_books():
    """Test the get_books function.

    This test checks if the get_books function returns the expected result.
    """

    correct_result = get_books("combined-print-and-e-book-nonfiction")
    incorrect_result = get_books("sadsaassddsa")
    assert isinstance(correct_result, str)
    assert incorrect_result == "No best sellers list found for the provided genre. "


@pytest.mark.parametrize(
    "user, expected_status_code, expected_error",
    [
        ("test_user", 200, None),
        ("None", 400, "Missing parameters"),
    ],
)
def test_get_shoreleave(client, user, expected_status_code, expected_error):
    """Test the shore leave endpoint.

    This test checks if the shore leave endpoint returns the correct status code and error message for a given user. If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get("/shoreleave", query_string={"user": user})
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        data = response.json
        assert isinstance(data["_name"], str)
        assert isinstance(data["quotes"], str)
        assert isinstance(data["nasa_fact"], str)
        assert isinstance(data["random_facts"], str)
        assert isinstance(data["books"], str)
    else:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
