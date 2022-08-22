import string
import random

from fastapi.testclient import TestClient

from main import app
from config.base import config

client = TestClient(app)


def test_health_endpoint():
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello World"}


def test_root_endpoint():
    resp = client.get("/")
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'Not Found'}


def test_todoist_login_redirect():
    resp = client.get("/todoist/login", allow_redirects=False)
    assert resp.status_code == 307
    assert resp.is_redirect
    assert not resp.is_permanent_redirect


def test_todoist_login_callback_invalid_state():
    letters = string.ascii_lowercase
    code = (''.join(random.choice(letters) for _ in range(10)))
    state = (''.join(random.choice(letters) for _ in range(50)))
    resp = client.get(f"/todoist/callback?code={code}&state={state}")
    assert resp.status_code == 403
    assert resp.json() == {"message": "Access denied"}


def test_todoist_login_callback_valid_state():
    letters = string.ascii_lowercase
    code = (''.join(random.choice(letters) for _ in range(10)))
    resp = client.get(f"/todoist/callback?code={code}&state={config.todoist.state_string}")

    assert resp.status_code == 400
    assert resp.json() == {"message": "Invalid code"}
