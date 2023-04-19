"""The following tests run only with Docker containers running."""

import pytest
from scuttlebutt.app import (
    app,
    get_weather,
    get_news,
    get_stock_symbols,
    get_stock_news,
)


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


def test_get_weather():
    """Test the get_weather function.

    This test checks if the get_weather function returns the expected result.
    """

    correct_weather = get_weather("48.213121,5.123123")
    incorrect_weather = get_weather("sadsaassddsa")
    assert isinstance(correct_weather, str)
    assert (
        incorrect_weather
        == "No weather information found for the provided coordinates. "
    )


def test_get_news():
    """Test the get_news function.

    This test checks if the get_news function returns the expected result.
    """

    correct_news = get_news("International")
    incorrect_news = get_news("Incorrect Category")
    assert isinstance(correct_news, str)
    assert incorrect_news == "No news found for the provided categories. "


@pytest.mark.parametrize(
    "stocks, expected_result",
    [
        (["Apple", "Microsoft"], "AAPL,MSFT"),
        (["Apple", "Microsoft", "Fake Stock"], "AAPL,MSFT,None"),
        (["Fake Stock"], "None"),
    ],
)
def test_get_stock_symbols(stocks, expected_result):
    """Test the get_stock_symbols function.

    This test checks if the get_stock_symbols function returns the correct stock symbols for a given list of stock names.
    """

    assert get_stock_symbols(stocks) == expected_result


def test_get_stock_news():
    """Test the get_stock_news function.

    This test checks if the get_stock_news function returns the expected result.
    """

    correct_news = get_stock_news(["Apple", "Microsoft"])
    incorrect_news = get_stock_news(["Fake Stock"])
    assert isinstance(correct_news, str)
    assert incorrect_news == "No news found for the provided stocks. "


@pytest.mark.parametrize(
    "user, expected_status_code, expected_error",
    [
        ("test_user", 200, None),
        (None, 400, "Missing parameters"),
    ],
)
def test_get_scuttlebutt(client, user, expected_status_code, expected_error):
    """Test the scuttlebutt endpoint.

    To run this test a user called "test_user" must be present in the database.

    This test checks if the scuttlebutt endpoint returns the correct status code and error message for a given user. If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get("/scuttle", query_string={"user": user})
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        data = response.json
        assert isinstance(data["weather"], str)
        assert isinstance(data["news"], str)
        assert isinstance(data["stock_news"], str)
        assert isinstance(data["_name"], str)
    else:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
