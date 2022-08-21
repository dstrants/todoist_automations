import pytest
from github import GithubException
from github.Repository import Repository as RepoModel

from services.gh.repos import get_repo

EXISTING_REPO = "tiangolo/fastapi"


def test_get_repo_existing_repo() -> None:
    repo = get_repo(EXISTING_REPO)

    assert isinstance(repo, RepoModel)
    assert repo.full_name == EXISTING_REPO


def test_get_repo_nonexisting_repo() -> None:
    with pytest.raises(GithubException):
        get_repo("tiangolo/fastapi-does-not-exist")


def test_get_repo_as_dict() -> None:
    repo = get_repo(EXISTING_REPO, dictionary=True)
    assert isinstance(repo, dict)
    assert repo["full_name"] == EXISTING_REPO


def test_repo_dict_should_be_repo_raw_data() -> None:
    repo_dict = get_repo(EXISTING_REPO, dictionary=True)
    repo_instance = get_repo(EXISTING_REPO)

    assert repo_dict == repo_instance.raw_data
    assert repo_dict["full_name"] == EXISTING_REPO == repo_instance.full_name
