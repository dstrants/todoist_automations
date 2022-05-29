from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection

from config.base import config

def mongo_collection(collection_name: str = "items") -> Collection:
    return config.mongo.todoist_collection(collection_name)