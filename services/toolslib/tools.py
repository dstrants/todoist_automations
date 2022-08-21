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


def save_to_mongo(repo: dict) -> None:
    tools = config.mongo.tools_collection()
    tools.insert_one(repo)


def create_record_from_repo(repo_name: str) -> None:
    repo = get_repo(repo_name)
    repo_dict = form_repo_dict(repo)

    create_record(repo_dict, typecast=True)
    config.logger.info("Repo %s has been created in airtable", repo_name)

    if config.airtable.cache:
        save_to_mongo(repo.raw_data)
        config.logger.info("Repo %s has been cached to mongo", repo_name)

    return None
