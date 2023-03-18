import pytest
from weather_service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


@pytest.mark.parametrize(
    "lat, lon", [(37.7749, -122.4194), (40.7128, -74.0060), ("invalid", "invalid")]
)
def test_get_weather(client, lat, lon):
    """Test the Weather endpoint.
    This test checks if the Weather endpoint returns the correct status code and error message.
    """

    url = "/weather"
    params = {
        "lat": lat,
        "lon": lon,
    }
    response = client.get(url, query_string=params)

    if lat == "invalid" or lon == "invalid":
        assert response.json["cod"] == "400"
        assert response.json["message"] == "wrong latitude"
    else:
        assert response.status_code == 200
        assert response.json["cod"] == "200"
        assert "clouds" in response.json["list"][0]
