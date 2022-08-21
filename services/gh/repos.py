from github import Github, Repository


def get_repo(repo_name: str, dictionary: bool = False) -> Repository.Repository | dict:
    g = Github()

    repo = g.get_repo(repo_name)

    if dictionary:
        return repo.raw_data

    return g.get_repo(repo_name)
