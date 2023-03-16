import pytest
from wisdom_service.app import app

@pytest.fixture
def client():
    """Create a test client for the app."""

    return app.test_client()

def test_get_random_facts(client):
    """Test the random facts endpoint.

    This test checks if the random facts endpoint returns a status code 200 and the correct data.
    """

    response = client.get("/wisdom/random_facts")
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) == 5
    assert "fact" in data[0]
    assert isinstance(data[0]["fact"], str)


def test_get_quotes(client):
    """Test the quotes endpoint.

    This test checks if the quotes endpoint returns a status code 200 and the correct data.
    """

    response = client.get("/wisdom/quotes")
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) == 5
    assert "category" in data[0]
    assert "quote" in data[0]
    assert "author" in data[0]
    assert isinstance(data[0]["category"], str)
    assert isinstance(data[0]["quote"], str)
    assert isinstance(data[0]["author"], str)

def test_get_apod(client):
    """Test the astronomy picture of the day endpoint.

    This test checks if the astronomy picture of the day endpoint returns a status code 200 and the correct data.
    """

    response = client.get("/wisdom/apod")
    assert response.status_code == 200
    data = response.json
    assert "title" in data
    assert "explanation" in data
    assert "url" in data
    assert isinstance(data["title"], str)
    assert isinstance(data["explanation"], str)
    assert isinstance(data["url"], str)    
    