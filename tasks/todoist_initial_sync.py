from asyncio import gather

from config.base import config


def todoist_instances_to_dict(entries: list) -> list[dict]:
    transformed_entries = []
    for entry in entries:
        tmp_dict = entry.__dict__
        data = tmp_dict["data"]

        del tmp_dict["api"]
        del tmp_dict["data"]

        transformed_entries.append(tmp_dict | data)

    return transformed_entries


async def todoist_import_all(state: dict):
    imports = [ massive_import(state, kind) for kind in {'projects', 'labels'} ]
    gather(*imports)


async def massive_import(state, kind: str):
    data = todoist_instances_to_dict(state[kind])
    collection = config.mongo.todoist_collection(kind)
    collection.insert_many(data)

