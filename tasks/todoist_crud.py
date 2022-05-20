from pymongo.mongo_client import MongoClient

from models.todoist import TodoistWebhook


def create_task(webhook: TodoistWebhook) -> None:
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client['todoist']
    items_collection = db['items']

    items_collection.insert_one(webhook.event_data.dict())
