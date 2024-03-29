from asyncio import gather

from config.base import config


def todoist_instances_to_dict(entries: list) -> list[dict]:
    """Converts a list of todoist instances to a list of dictionaries."""
    transformed_entries = []
    for entry in entries:
        tmp_dict = entry.__dict__
        data = tmp_dict["data"]

        del tmp_dict["api"]
        del tmp_dict["data"]

        transformed_entries.append(tmp_dict | data)

    return transformed_entries


async def todoist_import_all(state: dict):
    """Performs a full import of the todoist state."""
    imports = [massive_import(state, kind) for kind in {'projects', 'labels'}]
    gather(*imports)


async def massive_import(state, kind: str):
    """Imports all items of a given kind"""
    data = todoist_instances_to_dict(state[kind])
    collection = config.mongo.todoist_collection(kind)
    for entry in data:
        collection.update_one({"id": entry["id"]}, {"$set": entry}, upsert=True)
    config.logger.info("Imported %s %s", len(data), kind)
