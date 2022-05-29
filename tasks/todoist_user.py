from utils.mongo import mongo_collection


def create_user(user: dict):
    users_collection = mongo_collection("users")
    users_collection.insert_one(user)


def update_user(user: dict):
    users_collection = mongo_collection("users")
    users_collection.update_one({"email": user["email"]}, {"$set": user})


def find_user_by_email(todoist_user_email: str) -> dict | None:
    users_collection = mongo_collection("users")
    return users_collection.find_one({"email": todoist_user_email})


def find_user_by_query(query: dict) -> dict | None:
    users_collection = mongo_collection("users")
    return users_collection.find_one(query)