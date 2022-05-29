from typing import Tuple
from todoist_api_python.api import TodoistAPI

from config.base import config
from models.todoist import TodoistItem
from utils.mongo import mongo_collection

def helper_load_priority_labels() -> dict[str, int]:
    labels_collection = mongo_collection("labels")
    labels = {}

    for priority_label_name in config.todoist.priority_labels_set:
        label = labels_collection.find_one({"name": priority_label_name})
        if not label:
            # TODO: Add logic to create the label
            continue
        labels[priority_label_name] = label["id"]

    return labels

def helper_load_user_todoist_token(user_id: int) -> str:
    users_collection = mongo_collection("users")
    user = users_collection.find_one({"id": user_id})

    if not user:
        # TODO: Use a more specific exception
        raise ValueError("User does not exist in the database")

    return user["token"]


def check_if_size_label_missing(item: TodoistItem) -> Tuple[set[int], dict[str, int]]:
    size_labels = helper_load_priority_labels()
    size_labels_ids = set(size_labels.values())
    item_labels_ids = set(item.labels)

    return size_labels_ids.intersection(item_labels_ids), size_labels

def automations_priority_labelling(item: TodoistItem) -> None:
    common_labels, size_labels = check_if_size_label_missing(item)
    if common_labels:
        print(f"Task {item.id} already has time label")
        return None

    print(f"Task {item.id} does not have time label. Will add quick")
    # TODO: Make default size label configurable
    item.labels.append(size_labels["quick"])

    todoist_token = helper_load_user_todoist_token(item.user_id)
    api = TodoistAPI(todoist_token)
    api.update_task(item.id, label_ids=item.labels)






