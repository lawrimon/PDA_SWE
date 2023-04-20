import pytest
from calendar_service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.parametrize(
    "endpoint, status_code",
    [
        ("/calendar/appointments/all", 200),
        ("/calendar/appointments/tomorrow", 200),
        ("/calendar/appointments/invalid_date", 400),
    ],
)
def test_get_calendar_appointments(client, endpoint, status_code):
    """Test the get_calendar_appointments endpoint.

    This test checks if the get_calendar_appointments endpoint returns the correct status code and content type.
    """
    response = client.get(endpoint)
    assert response.status_code == status_code
    assert response.content_type == "application/json"


def test_get_calendar_appointments_empty(client):
    """Test the get_calendar_appointments endpoint with an empty calendar.

    This test checks if the get_calendar_appointments endpoint returns an empty list when the calendar is empty.
    """
    app.calendar = {}
    response = client.get("/calendar/appointments/all")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.data == b"[]"


@pytest.mark.parametrize(
    "data, expected_status, expected_response",
    [
        (
            {
                "title": "Meeting",
                "description": "Discuss project",
                "start_time": "2023-04-20T09:00:00",
                "end_time": "2023-04-20T10:00:00",
            },
            201,
            b"Meeting",
        ),
        (
            {
                "title": "Meeting",
                "description": "Discuss project",
                "start_time": "2023-04-20T09:00:00",
                "end_time": "2023-04-20T10:00:00",
            },
            409,
            b"Conflict",
        ),
    ],
)
def test_add_calendar_appointment(client, data, expected_status, expected_response):
    """Test the add_calendar_appointment endpoint.

    This test checks if the add_calendar_appointment endpoint adds an appointment to the calendar and returns the
    expected status code and response.
    """
    app.calendar = {
        "2023-04-20": [
            {
                "title": "Busy",
                "description": "",
                "start_time": "2023-04-20T08:00:00",
                "end_time": "2023-04-20T09:30:00",
            }
        ]
    }
    response = client.post("/calendar/appointments", json=data)
    assert response.status_code == expected_status
    assert response.content_type == "application/json"
    assert expected_response in response.data
