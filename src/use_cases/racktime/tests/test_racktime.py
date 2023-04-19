"""The following tests run only with Docker containers running."""

import pytest
from racktime.app import (
    app,
    get_issues,
    play_music,
    get_route,
    get_calendar_events_tomorrow,
)


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


@pytest.mark.parametrize(
    "username, expected_result",
    [
        ("lawrimon", "Congrats! There are no open issues assigned to you. "),
        ("sadsaassddsa", "No open issues found for the provided user. "),
        (
            "maxkie1",
            "The following issue is a perfect start for your day tommorow: Test Issue 1 in the PDA_SWE repository. It is about This is a test issue. These are the labels: task. ",
        ),
    ],
)
def test_get_issues(username, expected_result):
    """Test the get_issues function.

    This test checks if the get_issues function returns the expected result for different usernames.
    """

    assert get_issues(username) == expected_result


@pytest.mark.parametrize(
    "artist, expected_result",
    [
        ("Ski Aggu", "Music of your favorite artist Ski Aggu is playing. Groove on! "),
        ("sadsaassddsa", "No music found for the provided artist. "),
    ],
)
def test_play_music(artist, expected_result):
    """Test the play_music function.

    To run this test, a local Spotify device must be running.
    This test checks if the play_music function returns the expected result for different artists.
    """

    assert play_music(artist) == expected_result


@pytest.mark.parametrize(
    "origin, destination, mode, expected_result",
    [
        (
            "52.370216,4.895168",
            "53.23445344722573,5.622244185533128",
            "Car",
            "The route from your home to your first appointment is 129km long and will take 1h 23min with your preferred means of transportation Car. ",
        ),
        (
            "0,0",
            "53.23445344722573,5.622244185533128",
            "Walking",
            "No route found for the provided origin and destination. ",
        ),
    ],
)
def test_get_route(origin, destination, mode, expected_result):
    """Test the get_route function.

    This test checks if the get_route function returns the expected result for different origins, destinations and modes.
    """

    assert get_route(origin, destination, mode) == expected_result


@pytest.mark.parametrize(
    "user, expected_result",
    [
        ("asdsadassaddsa", None),
        (
            "test_user",
            [
                {
                    "summary": "Test Summary",
                    "location": "Stuttgart",
                    "start": "2023-04-18T10:00:00+02:00",
                    "end": "2023-04-18T11:00:00+02:00",
                }
            ],
        ),
    ],
)
def test_get_calendar_events_tomorrow(user, expected_result):
    """Test the get_calendar_events_tomorrow function.

    This test checks if the get_calendar_events_tomorrow function returns the expected result.
    """

    assert get_calendar_events_tomorrow(user) == expected_result


@pytest.mark.parametrize(
    "user, expected_status_code, expected_error",
    [
        ("test_user", 200, None),
        (None, 400, "Missing parameters"),
    ],
)
def test_get_racktime(client, user, expected_status_code, expected_error):
    """Test the rack time endpoint.

    To run this test a user called "test_user" must be present in the database.

    This test checks if the rack time endpoint returns the expected status code and error message. If the status code is 200, it also checks if the response contains the expected result.
    """

    response = client.get("/racktime", query_string={"user": user})
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        data = response.json
        assert isinstance(data["_name"], str)
        assert isinstance(data["1introduction"], str)
        assert isinstance(data["tomorrows_events"], str)
        assert isinstance(data["route"], str)
        assert isinstance(data["music"], str)
        assert isinstance(data["issues"], str)
    else:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
