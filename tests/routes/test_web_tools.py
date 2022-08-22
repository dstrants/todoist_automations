import pytest
from fastapi.testclient import TestClient
from github import GithubException

from main import app
from config.base import config

client = TestClient(app)

NONEXISTENT_REPO = "fastapi/fastapi-does-not-exist"


def test_missing_auth_header() -> None:
    resp = client.post("/tools/new", {"full_name": NONEXISTENT_REPO})
    assert resp.status_code == 403
    assert resp.json() == {"detail": "Not authenticated"}


def test_wrong_auth_header() -> None:
    resp = client.post(
        "/tools/new",
        {"full_name": NONEXISTENT_REPO},
        headers={"X-DOISTER-API-KEY": "Bearer wrong"}
    )
    assert resp.status_code == 403
    assert resp.json() == {"detail": "Could not authenticate user"}


def test_correct_auth_header_non_existent_repo():
    with pytest.raises(GithubException):
        resp = client.post(
            "/tools/new",
            json={"full_name": NONEXISTENT_REPO},
            headers={"X-DOISTER-API-KEY": config.api_key}
        )
        assert resp.status_code == 200
        assert resp.json() == {"message": "Repo has been created"}
