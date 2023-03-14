import pytest
from stock_market_service.app import app

@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()

@pytest.mark.parametrize(
    "symbols,expected_status_code,expected_error",
    [
        ("IBM,MSFT,GOOG", 200, None),
        (None, 400, "Missing parameters"),
        ("IBM,MSFT,GOOG,123", 400, "Invalid parameters"),
    ],
)
def test_get_quotes(client, symbols, expected_status_code, expected_error):
    """Test the quotes endpoint.

    This test checks if the quotes endpoint returns the correct status code and error message.
    If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get("/quotes", query_string={"symbols": symbols})
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
    else:
        data = response.json
        assert "IBM" in data
        assert "MSFT" in data
        assert "GOOG" in data
        assert "currency" in data["IBM"]
        assert "bid_price" in data["IBM"]
        assert "ask_price" in data["IBM"]

@pytest.mark.parametrize(
    "symbols,expected_status_code,expected_error",
    [
        ("IBM,MSFT,GOOG", 200, None),
        (None, 400, "Missing parameters"),
        ("IBM,MSFT,GOOG,123", 400, "Invalid parameters"),
    ],
)
def test_get_news(client, symbols, expected_status_code, expected_error):
    """Test the news endpoint.

    This test checks if the news endpoint returns the correct status code and error message.
    If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get("/news", query_string={"symbols": symbols})
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
    else:
        data = response.json
        assert "IBM" in data
        assert "MSFT" in data
        assert "GOOG" in data  