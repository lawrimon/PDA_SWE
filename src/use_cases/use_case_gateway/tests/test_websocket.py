import json
import pytest

from flask.testing import FlaskClient
from flask_socketio import SocketIOTestClient

from app import app, on_message


@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope='module')
def socketio_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            socketio = SocketIOTestClient(app, client)
            yield socketio


def test_on_message():
    message = {'text': 'test message'}
    user_id = 'test_user_id'
    delivery_tag = 'test_delivery_tag'
    with app.app_context():
        on_message(user_id, json.dumps(message), delivery_tag)


def test_connect(socketio_client):
    received_events = []
    socketio_client.on('connect', lambda: received_events.append('connect'))
    socketio_client.connect()
    assert 'connect' in received_events


def test_start(socketio_client):
    received_events = []
    socketio_client.on('start', lambda data: received_events.append('start'))
    socketio_client.emit('start', {'user_id': 'test_user_id'})
    assert 'start' in received_events


def test_ack(socketio_client):
    received_events = []
    socketio_client.on('ack', lambda data: received_events.append('ack'))
    socketio_client.emit('ack', {'delivery_tag': 'test_delivery_tag'})
    assert 'ack' in received_events


def test_disconnect(socketio_client):
    received_events = []
    socketio_client.on('disconnect', lambda: received_events.append('disconnect'))
    socketio_client.disconnect()
    assert 'disconnect' in received_events