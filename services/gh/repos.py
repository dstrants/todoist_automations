from github import Repository

from config.base import config


def get_repo(repo_name: str, dictionary: bool = False) -> Repository.Repository | dict:
    """Retrieves the repository information from github."""

    repo = config.github.client.get_repo(repo_name)

    if dictionary:
        return repo.raw_data

    return repo
