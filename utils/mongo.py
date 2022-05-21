from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection

def mongo_collection(collection_name: str = "items") -> Collection:
    client = MongoClient("mongodb://root:example@localhost:27017/")
    # TODO: Make the database name dynamic
    db = client['todoist']
    return db[collection_name]