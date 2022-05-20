from asyncio import gather
from pymongo.mongo_client import MongoClient



async def todoist_import_all(state: dict):
    imports = [ massive_import(state, kind) for kind in {'projects', 'labels'} ]
    gather(*imports)



async def massive_import(state, kind: str):
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client['todoist']
    collection = db[kind]
    collection.insert_many(state[kind])
