import pytest
from app import app, get_response, get_scuttlebutt, get_lookout, get_shoreleave, get_racktime, get_all_user, notify_event
from unittest import mock
from app import notify_event


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_pika():
    with mock.patch('app.pika') as mock_pika:
        yield mock_pika


def test_get_response(client):
    response = get_response("http://httpbin.org/get")
    assert response is not None
    assert response['args'] == {}


def test_get_scuttlebutt(client):
    response = get_scuttlebutt("user1")
    assert response is not None


def test_get_lookout(client):
    response = get_lookout("user1")
    assert response is not None


def test_get_shoreleave(client):
    response = get_shoreleave("user1")
    assert response is not None


def test_get_racktime(client):
    response = get_racktime("user1")
    assert response is not None


def test_get_all_user(client):
    response = get_all_user()
    assert response is not None


def test_notify_event(mock_pika):
    mock_users = [{'id': 'user1'}, {'id': 'user2'}, {'id': 'user3'}]
    mock_response = [{'response': 'some response'}]
    mock_get_all_user = mock.MagicMock(return_value=mock_users)
    mock_get_scuttlebutt = mock.MagicMock(return_value=mock_response)
    mock_get_lookout = mock.MagicMock(return_value=mock_response)
    mock_get_shoreleave = mock.MagicMock(return_value=mock_response)
    mock_get_racktime = mock.MagicMock(return_value=mock_response)

    with mock.patch('app.get_all_user', mock_get_all_user):
        with mock.patch('app.get_scuttlebutt', mock_get_scuttlebutt):
            with mock.patch('app.get_lookout', mock_get_lookout):
                with mock.patch('app.get_shoreleave', mock_get_shoreleave):
                    with mock.patch('app.get_racktime', mock_get_racktime):
                        notify_event('scuttlebutt')
                        notify_event('lookout')
                        notify_event('shoreleave')
                        notify_event('racktime')

    assert mock_get_all_user.call_count == 4
    assert mock_get_scuttlebutt.call_count == 3
    assert mock_get_lookout.call_count == 3
    assert mock_get_shoreleave.call_count == 3
    assert mock_get_racktime.call_count == 3
    assert mock_pika.BlockingConnection.call_count == 4
    assert mock_pika.ConnectionParameters.call_count == 4
    assert mock_pika.BlockingConnection.return_value.channel.call_count == 4
    assert mock_pika.BlockingConnection.return_value.channel.return_value.exchange_declare.call_count == 4
    assert mock_pika.BlockingConnection.return_value.channel.return_value.queue_declare.call_count == 12
    assert mock_pika.BlockingConnection.return_value.channel.return_value.queue_bind.call_count == 12
    assert mock_pika.BlockingConnection.return_value.channel.return_value.basic_publish.call_count == 3
    assert mock_pika.BlockingConnection.return_value.channel.close.call_count == 4
    assert mock_pika.BlockingConnection.return_value.close.call_count == 4