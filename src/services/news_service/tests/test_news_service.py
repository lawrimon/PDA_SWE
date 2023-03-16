import pytest
from news_service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


@pytest.mark.parametrize(
    "regions, topics, expected_status_code, expected_error",
    [
        ("1", "ausland", 200, None),
        (None, None, 400, "Missing parameters"),
        ("wrong", "ausland", 400, "Invalid parameters"),
        ("1", "wrong", 400, "Invalid parameters"),
    ],
)
def test_get_tagesschau_here(client, topics, regions, expected_status_code, expected_error):
    """Test the tagesschau news endpoint.

    This test checks if the tagesschau news endpoint returns the correct status code and error message.
    """

    response = client.get(
        "/news/tagesschau/here", query_string={"regions": regions, "topics": topics}
    )
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error 


def test_get_tagesschau_homepage(client):
    """Test the tagesschau homepage endpoint.

    This test checks if the tagesschau homepage endpoint returns the correct status code and error message.
    """

    response = client.get("/news/tagesschau/homepage")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "category,expected_status_code,expected_error",
    [
        ("science", 200, None),
        (None, 400, "Missing parameters"),
        ("123", 400, "Invalid parameters"),
    ],
)
def test_get_nytimes(client, category, expected_status_code, expected_error):
    """Test the nytimes endpoint.

    This test checks if the nytimes endpoint returns the correct status code and error message.
    """

    response = client.get("/news/nytimes", query_string={"category": category})
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
