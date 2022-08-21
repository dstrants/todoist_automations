from github.Repository import Repository

from config.base import config
from services.gh.repos import get_repo
from services.airtable.records import create_record


# TODO: Cache repos to the mongo db


def form_repo_dict(repo: Repository) -> dict:
    return {
        "Name": repo.name,
        "Github": repo.html_url,
        "Tags": repo.get_topics(),
        "Notes": repo.description,
        "Webpage": repo.homepage,
        "Language": repo.language

    }


def create_record_from_repo(repo_name: str) -> None:
    repo = get_repo(repo_name)
    repo_dict = form_repo_dict(repo)

    create_record(repo_dict, typecast=True)
    config.logger.info("Repo %s has been created", repo_name)

    return None
