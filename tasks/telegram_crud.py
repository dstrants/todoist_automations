from config.base import config


def create_authentication_code(code: str, todoist_user_id: int):
    telegram_authentication_code = config.mongo.telegram_collection("authentication_codes")
    telegram_authentication_code.insert_one({"code": code, "todoist_user_id": todoist_user_id})


def get_authentication_code_from_code(code: str) -> dict:
    telegram_authentication_code = config.mongo.telegram_collection("authentication_codes")
    return telegram_authentication_code.find_one({"code": code})

def get_authentication_code_from_user_id(todoist_user_id: int) -> dict:
    telegram_authentication_code = config.mongo.telegram_collection("authentication_codes")
    return telegram_authentication_code.find_one({"todoist_user_id": todoist_user_id})


def delete_authentication_code_from_code(code: str) -> None:
    telegram_authentication_code = config.mongo.telegram_collection("authentication_codes")
    telegram_authentication_code.delete_one({"code": code})