import pytest
from events_service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


@pytest.mark.parametrize(
    "location, enddate, expected_status_code, expected_error",
    [
        ("Stuttgart", "2023-05-01T14:00:00Z", 200, None),
        (None, None, 400, "Missing route parameters"),
    ],
)
def test_get_events_location(
    client, location, enddate, expected_status_code, expected_error
):
    """Test the event location endpoint.

    This test checks if the event location endpoint returns the correct status code and error message.
    """

    response = client.get(
        "/events/location", query_string={"location": location, "enddate": enddate}
    )
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error


@pytest.mark.parametrize(
    "artists, enddate, expected_status_code, expected_error",
    [
        ('["Avril Lavigne"]', "2023-05-01T14:00:00Z", 200, None),
        (None, None, 400, "Missing route parameters"),
        ([], None, 400, "Missing route parameters"),
    ],
)
def test_get_events_artists(
    client, artists, enddate, expected_status_code, expected_error
):
    """Test the event artists endpoint.

    This test checks if the event artists endpoint returns the correct status code and error message.
    """

    response = client.get(
        "/events/artists", query_string={"artists": artists, "enddate": enddate}
    )
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error

@pytest.mark.parametrize(
    "artists, location, enddate, expected_status_code, expected_error",
    [
        ('["Avril Lavigne"]', "Stuttgart", "2023-05-01T14:00:00Z", 200, None),
        (None, None, None, 400, "Missing route parameters"),
        ([], None, None, 400, "Missing route parameters"),
    ],
)
def test_get_events(
    client, artists, location, enddate, expected_status_code, expected_error
    )  :
    """Test the event endpoint.

    This test checks if the event endpoint returns the correct status code and error message.
    """

    response = client.get(
        "/events/all",
        query_string={
            "artists": artists,
            "location": location,
            "enddate": enddate,
        },
    )
    assert response.status_code == expected_status_code
    if expected_error:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
