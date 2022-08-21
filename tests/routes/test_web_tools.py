from fastapi.testclient import TestClient

from main import app
from config.base import config

client = TestClient(app)


def test_missing_auth_header() -> None:
    resp = client.post("/tools/new", {"full_name": "fastapi/fastapi"})
    assert resp.status_code == 403
    assert resp.json() == {"detail": "Not authenticated"}


def test_wrong_auth_header() -> None:
    resp = client.post(
        "/tools/new",
        {"full_name": "fastapi/fastapi"},
        headers={"X-DOISTER-API-KEY": "Bearer wrong"}
    )
    assert resp.status_code == 403
    assert resp.json() == {"detail": "Could not authenticate user"}


def test_correct_auth_header_non_existent_repo():
    resp = client.post(
        "/tools/new",
        json={"full_name": "fastapi/fastapi"},
        headers={"X-DOISTER-API-KEY": config.api_key}
    )
    assert resp.status_code == 200
    assert resp.json() == {"message": "Repo has been created"}
