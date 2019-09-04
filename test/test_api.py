from unittest.mock import patch
import pytest
from flask import Flask
import json
from mock import MagicMock
from api.controller import routes
from api.controller import tasks
from api.factory import create_app


app = Flask(__name__)
app.register_blueprint(routes.bp)


@pytest.fixture
def client():
    client = app.test_client()
    return client


def test_health(client):
    response = client.get('/')
    assert response.status_code == 200


def test_get_status(client):
    # Initialize dummy_task here
    dummy_task = dict(status='Working', info='Done')
    tasks.check_status = MagicMock(return_value=dummy_task)

    response = client.get('/status', data=json.dumps(dict(token='1234')), content_type='application/json')

    assert response.status_code == 200


# Do same thing for test_resize
