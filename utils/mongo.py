from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection

from config.base import config

def mongo_collection(collection_name: str = "items") -> Collection:
    client = MongoClient(config.mongo.server)
    # TODO: Make the database name dynamic
    db = client['todoist']
    return db[collection_name]