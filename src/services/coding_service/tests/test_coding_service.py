import pytest
from coding_service.app import app

@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()

@pytest.mark.parametrize(
    "username, expected_status_code, expected_error",
    [
        ("maxkie1", 200, None),
        (None, 400, "Missing parameters"),
        ("adssasaddsddsadsdsadas", 400, "Invalid parameters"),
    ],
)
def test_get_issues(client, username, expected_status_code, expected_error):
    """Test the issues endpoint.

    This test checks if the issues endpoint returns the correct status code and error message.
    """

    response = client.get("/issues", query_string={"username": username})
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
    else:
        data = response.json
        if len(data) > 0:
            assert isinstance(data[0]["title"], str)
            assert isinstance(data[0]["url"], str)
            assert isinstance(data[0]["updated_at"], str)
        else:
            assert data == []

