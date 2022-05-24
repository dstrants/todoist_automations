from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection

from config.constants import MONGO_CLIENT

def mongo_collection(collection_name: str = "items") -> Collection:
    client = MongoClient(MONGO_CLIENT)
    # TODO: Make the database name dynamic
    db = client['todoist']
    return db[collection_name]