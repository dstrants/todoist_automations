from utils.mongo import mongo_collection


def create_user(user: dict):
    users_collection = mongo_collection("users")
    users_collection.insert_one(user)