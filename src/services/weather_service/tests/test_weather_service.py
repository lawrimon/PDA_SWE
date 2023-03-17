import pytest
from weather_service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()


@pytest.mark.parametrize("lat, lon", [(37.7749, -122.4194), (40.7128, -74.0060), ("invalid", "invalid")])
def test_get_weather(lat, lon):
    """Test the Weather endpoint.
    This test checks if the Weather endpoint returns the correct status code and error message.
    """

    url = 'http://localhost:5000/weather'
    params = {
        'lat': lat,
        'lon': lon,
    }
    response = requests.get(url, params=params)

    if lat == "invalid" or lon == "invalid":
        assert response.status_code == 400
    else:
        assert response.status_code == 200
        assert response.json()['cod'] == '200'
        assert 'daily' in response.json()['list'][0]
