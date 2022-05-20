from pymongo.mongo_client import MongoClient


def create_user(user: dict):
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client['todoist']
    users_collection = db['users']

    users_collection.insert_one(user)