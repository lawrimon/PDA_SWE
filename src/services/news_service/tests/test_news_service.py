import pytest
from news_service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


@pytest.mark.parametrize(
    "ressort,regions,expected_status_code, expected_error",
    [
        ("ausland", "1", 200, None),
        (None, None, 400, "Missing parameters"),
        ("BRO", "Bo", 400, "Invalid parameters"),
    ],
)
def test_get_tagesschau(client, ressort, regions, expected_status_code, expected_error):
    """Test the quotes endpoint.

    This test checks if the quotes endpoint returns the correct status code and error message.
    If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get(
        "/news/tagesschau/here", query_string={"regions": regions, "ressort": ressort}
    )
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
    else:
        pass


@pytest.mark.parametrize(
    "category,expected_status_code,expected_error",
    [
        ("science", 200, None),
        (None, 400, "Missing parameters"),
        ("123", 400, "Invalid parameters"),
    ],
)
def test_get_nytimes(client, category, expected_status_code, expected_error):
    """Test the news endpoint.

    This test checks if the news endpoint returns the correct status code and error message.
    If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get("/news/nytimes", query_string={"category": category})
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
