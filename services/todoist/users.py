from config.base import config


def create_user(user: dict):
    """Creates a todoist user in the database."""
    users_collection = config.mongo.todoist_collection("users")
    users_collection.insert_one(user)
    config.logger.info("Created user %s", user["id"])


def update_user(user: dict):
    """Updates a todoist user in the database."""
    users_collection = config.mongo.todoist_collection("users")
    users_collection.update_one({"email": user["email"]}, {"$set": user})
    config.logger.info("Updated user %s", user["id"])


def find_user_by_email(todoist_user_email: str) -> dict | None:
    """Finds a user by their todoist email."""
    users_collection = config.mongo.todoist_collection("users")
    return users_collection.find_one({"email": todoist_user_email})


def find_user_by_query(query: dict) -> dict | None:
    """Finds a user by a query."""
    users_collection = config.mongo.todoist_collection("users")
    return users_collection.find_one(query)
