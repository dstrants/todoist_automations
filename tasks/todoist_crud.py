
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection

from models.todoist import TodoistWebhook


def mongo_items_collection() -> Collection:
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client['todoist']
    return db['items']


def create_task(webhook: TodoistWebhook) -> None:
    items_collection = mongo_items_collection()
    items_collection.insert_one(webhook.event_data.dict())


def update_task(webhook: TodoistWebhook) -> None:
    items_collection = mongo_items_collection()
    items_collection.update_one({"id": webhook.event_data.id}, {"$set": webhook.event_data.dict()})


def delete_task(webhook: TodoistWebhook) -> None:
    items_collection = mongo_items_collection()
    items_collection.delete_one({"id": webhook.event_data.id})