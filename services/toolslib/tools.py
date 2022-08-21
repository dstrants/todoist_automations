from services.gh.repos import get_repo
from services.airtable.records import create_record


def create_record_from_repo(repo_name: str) -> None:
    repo = get_repo(repo_name, dictionary=True)
    create_record(repo)

    return None