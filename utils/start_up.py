from pymongo import ASCENDING
from pymongo.mongo_client import MongoClient

from config.constants import MONGO_CLIENT

async def startup_ensure_mongo_unique_id_indexes():
    client = MongoClient(MONGO_CLIENT)
    db = client['todoist']
    for collection_name in {'items', 'projects', 'labels'}:
        collection = db[collection_name]
        existing_indexes = collection.index_information().keys()
        if f"id_1" in existing_indexes:
            continue

        collection.create_index([("id", ASCENDING)], unique=True)