import pytest
from books_service.app import app

@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()

@pytest.mark.parametrize(
    "genre, expected_status_code, expected_error",
    [
        ("combined-print-and-e-book-fiction", 200, None),
        (None, 400, "Missing parameters"),
        ("123", 400, "Invalid parameters"),
    ],
)
def test_get_books(client, genre, expected_status_code, expected_error):
    """Test the books endpoint.

    This test checks if the books endpoint returns the correct status code and error message.
    """

    response = client.get("/books", query_string={"genre": genre})
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
    else:
        data = response.json
        assert len(data) > 0
        assert isinstance(data[0]["title"], str)
        assert isinstance(data[0]["author"], str)
        assert isinstance(data[0]["description"], str)
        assert isinstance(data[0]["rank"], int)
        assert isinstance(data[0]["weeks_on_list"], int)
        assert isinstance(data[0]["publisher"], str)

    