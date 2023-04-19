"""The following tests run only with Docker containers running."""

import pytest
from lookoutduty.app import app, get_club_ids, get_events, get_sports


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


@pytest.mark.parametrize(
    "clubs, expected_result",
    [
        (["Bayern München", "Borussia Dortmund"], ["157", "165"]),
        (
            ["Bayern München", "Borussia Dortmund", "VfB Stuttgart"],
            ["157", "165", "172"],
        ),
        (
            ["Unknown Club", "Borussia Dortmund", "VfB Stuttgart", "Real Madrid"],
            ["Club ID not found", "165", "172", "541"],
        ),
    ],
)
def test_get_club_ids(clubs, expected_result):
    """Test the get_club_ids function.

    This test checks if the get_club_ids function returns the correct club IDs for a given list of club names.
    """

    assert get_club_ids(clubs) == expected_result


@pytest.mark.parametrize(
    "location, keyword_list, enddate, expected_result",
    [
        (
            "Stuttgart",
            ["Avril Lavigne"],
            "2023-05-01T14:00:00Z",
            "On the 2023-04-20T20:00:00Z in Stuttgart you can see Avril Lavigne. The price is 53.75 and the genre of the event is Music.",
        ),
        (
            "Stuttgart",
            ["123sads"],
            "2023-04-01T14:00:00Z",
            "No events found for the provided search criteria.",
        ),
        (
            "Stuttgart",
            ["Beyoncé"],
            "2023-05-01T14:00:00Z",
            "No events found in your area based on your favorite artists.",
        ),
    ],
)
def test_get_events(location, keyword_list, enddate, expected_result):
    """Test the get_events function.

    This test checks if the get_events function returns the correct events for a given location, keyword list and end date.
    """

    assert get_events(location, keyword_list, enddate) == expected_result


@pytest.mark.parametrize(
    "club_ids, clubs, expected_result",
    [
        (
            ["165"],
            ["Borussia Dortmund"],
            "Your favorite team Borussia Dortmund will play against Eintracht Frankfurt on the 2023-04-22 at 18:30. The will be played in Dortmund at the Signal Iduna Park.",
        ),
        (["123321312321"], ["Fake Club"], "No sports fixture found for Fake Club."),
    ],
)
def test_get_sports(club_ids, clubs, expected_result):
    """Test the get_sports function.

    This test checks if the get_sports function returns the correct sports fixture for a given club ID and club name.
    """

    assert get_sports(club_ids, clubs) == expected_result


@pytest.mark.parametrize(
    "user, expected_status_code, expected_error",
    [
        ("test_user", 200, None),
        (None, 400, "Missing parameters"),
    ],
)
def test_get_lookoutduty(client, user, expected_status_code, expected_error):
    """Test the lookout duty endpoint.

    To run this test a user called "test_user" must be present in the database.

    This test checks if the lookout duty endpoint returns the correct status code and error message for a given user. If status code is 200, it also checks if the response contains the correct data.
    """

    response = client.get("/lookout", query_string={"user": user})
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        data = response.json
        assert isinstance(data["sports"], str)
        assert isinstance(data["events"], str)
        assert isinstance(data["_name"], str)
    else:
        data = response.json
        assert "error" in data
        assert data["error"] == expected_error
