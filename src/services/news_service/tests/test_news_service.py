import pytest
from news_service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


@pytest.mark.parametrize(
    "regions, topic, expected_status_code, expected_error",
    [
        ("1", "ausland", 200, None),
        (None, None, 400, "Missing parameters"),
        ("wrong", "ausland", 400, "Invalid parameters"),
        ("1", "wrong", 400, "Invalid parameters"),
    ],
)
def test_get_tagesschau_here(
    client, regions, topic, expected_status_code, expected_error
):
    """Test the Tagesschau news endpoint.

    This test checks if the tagesschau news endpoint returns the correct status code and error message.
    """

    response = client.get(
        "/tagesschau/news", query_string={"regions": regions, "topic": topic}
    )
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error


def test_get_tagesschau_homepage(client):
    """Test the Tagesschau homepage endpoint.

    This test checks if the tagesschau homepage endpoint returns the correct status code and error message.
    """

    response = client.get("/tagesschau/homepage")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "topic, expected_status_code, expected_error",
    [
        ("science", 200, None),
        (None, 400, "Missing parameters"),
        ("123", 400, "Invalid parameters"),
    ],
)
def test_get_nytimes(client, topic, expected_status_code, expected_error):
    """Test the NY Times endpoint.

    This test checks if the NY Times endpoint returns the correct status code and error message.
    """

    response = client.get("/nytimes", query_string={"topic": topic})
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
