import pytest
from sports_service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


@pytest.mark.parametrize(
    "team,expected_status_code,expected_error",
    [
        ("33", 200, None),
        (None, 400, "Missing parameters"),
        ("abc", 400, "Invalid parameters"),
    ],
)
def test_get_football_fixture(client, team, expected_status_code, expected_error):
    """Test the football fixture endpoint.

    This test checks if the football fixture endpoint returns the correct status code and error message.
    If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get("/football/fixture", query_string={"team": team})
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
    else:
        data = response.json
        assert "venue" in data
        assert "league" in data
        assert "time" in data
        assert isinstance(data["time"]["timestamp"], int)
        assert isinstance(data["time"]["date"], str)
        assert isinstance(data["time"]["timezone"], str)
        assert isinstance(data["league"]["name"], str)
        assert isinstance(data["league"]["country"], str)
        assert isinstance(data["venue"]["name"], str)
        assert isinstance(data["venue"]["city"], str)
        assert isinstance(data["home_team"], str)
        assert isinstance(data["away_team"], str)


def test_get_formulaone_fixture(client):
    """Test the Formula 1 fixture endpoint.

    This test checks if the Formula 1 fixture endpoint returns a status code of 200 and the correct data.
    """

    response = client.get("/formulaone/fixture")
    assert response.status_code == 200
    data = response.json
    assert "venue" in data
    assert "time" in data
    assert isinstance(data["name"], str)
    assert isinstance(data["type"], str)
    assert isinstance(data["time"]["date"], str)
    assert isinstance(data["time"]["timezone"], str)
    assert isinstance(data["venue"]["name"], str)
    assert isinstance(data["venue"]["city"], str)
    assert isinstance(data["venue"]["country"], str)
