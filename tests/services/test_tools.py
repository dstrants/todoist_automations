from services.gh.repos import get_repo
from services.toolslib.tools import form_repo_dict


EXISTING_REPO = "tiangolo/fastapi"


def test_form_repo_dict() -> None:
    repo = get_repo(EXISTING_REPO)
    repo_dict = form_repo_dict(repo)

    assert isinstance(repo_dict, dict)
    assert repo_dict["Name"] == repo.name

    assert {
        "Name": repo.name,
        "Github": repo.html_url,
        "Tags": repo.get_topics(),
        "Notes": repo.description,
        "Webpage": repo.homepage,
        "Language": repo.language

    } == repo_dict
