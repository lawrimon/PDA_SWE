import pytest
from src.app import app, is_valid_coordinates_string


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


def test_get_user_location(client):
    """Test the user location endpoint.

    This test checks if the user location endpoint returns a status code 200 and the correct data.
    """

    response = client.get("/user_location")
    assert response.status_code == 200
    data = response.json
    assert "lat" in data
    assert "lon" in data
    assert isinstance(data["lat"], float)
    assert isinstance(data["lon"], float)


@pytest.mark.parametrize(
    "origin,destination,mode,expected_status_code,expected_error",
    [
        (
            "52.370216,4.895168",
            "53.23445344722573,5.622244185533128",
            "driving",
            200,
            None,
        ),
        (None, None, None, 400, "Missing parameters"),
        (
            "52.370216,4.895168",
            "53.23445344722573,5.622244185533128",
            "invalid",
            400,
            "Invalid parameters",
        ),
    ],
)
def test_get_route(
    client, origin, destination, mode, expected_status_code, expected_error
):
    """Test the route endpoint.

    This test checks if the route endpoint returns the correct status code and error message based on the parameters.
    If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get(
        "/route",
        query_string={"origin": origin, "destination": destination, "mode": mode},
    )
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
    else:
        data = response.json
        assert "distance" in data
        assert "duration" in data
        assert "steps" in data
        assert isinstance(data["distance"]["value"], int)
        assert isinstance(data["duration"]["value"], int)
        assert isinstance(data["steps"], list)


def test_is_valid_coordinates_string():
    """Test the is_valid_coordinates_string function.

    This test checks the is_valid_coordinates_string function with different parameters.
    """

    assert is_valid_coordinates_string("52.370216,4.895168") == True
    assert is_valid_coordinates_string("52.370216") == False
    assert is_valid_coordinates_string("52.370216,wrong") == False
    assert is_valid_coordinates_string("91,181") == False
