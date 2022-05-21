from pymongo import ASCENDING

from utils.mongo import mongo_collection

async def startup_ensure_mongo_unique_id_indexes():
    for collection_name in {'items', 'projects', 'labels'}:
        collection = mongo_collection(collection_name)
        existing_indexes = collection.index_information().keys()
        if f"id_1" in existing_indexes:
            continue

        collection.create_index([("id", ASCENDING)], unique=True)