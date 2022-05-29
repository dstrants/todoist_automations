import random
import string

from config.base import config
from services.telegram import messages
from services.todoist import users


def generate_telegram_authentication_string() -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(48))

def create_authentication_code(code: str, todoist_user_id: int):
    telegram_authentication_code = config.mongo.telegram_collection("authentication_codes")
    telegram_authentication_code.insert_one({"code": code, "todoist_user_id": todoist_user_id})
    config.logger.info("Created telegram authentication code for user %s", todoist_user_id)


def get_authentication_code_from_code(code: str) -> dict:
    telegram_authentication_code = config.mongo.telegram_collection("authentication_codes")
    return telegram_authentication_code.find_one({"code": code})


def get_authentication_code_from_user_id(todoist_user_id: int) -> dict:
    telegram_authentication_code = config.mongo.telegram_collection("authentication_codes")
    return telegram_authentication_code.find_one({"todoist_user_id": todoist_user_id})


def delete_authentication_code_from_code(code: str) -> None:
    telegram_authentication_code = config.mongo.telegram_collection("authentication_codes")
    telegram_authentication_code.delete_one({"code": code})
    config.logger.info("Deleted telegram authentication code %s", code)


def complete_telegram_verification(webhook_body: dict):
    if webhook_body["message"]["text"].startswith("/start"):
        code = webhook_body["message"]["text"].split(" ")[1]
        if result := get_authentication_code_from_code(code=code):
            user = users.find_user_by_query({"id": result["todoist_user_id"]})

            if not user:
                config.logger.warning("User %s not found", result["todoist_user_id"])
                return None

            updated_user = user | {"telegram_chat_id": webhook_body["message"]["chat"]["id"]}
            users.update_user(user=updated_user)
            delete_authentication_code_from_code(code=code)
            messages.send_telegram_message(message="Your account has been successfully verified", chat_id=webhook_body["message"]["chat"]["id"])
            config.logger.info("User's %s telegram profile has been verified", user["id"])
            return None
        config.logger.warning("Authentication code %s not found", code)
        return None
    config.logger.warning("Message is not a start command")


def start_telegram_authentication_process(todoist_user_id: int) -> str:
    if not (telegram_authentication_code_dict := get_authentication_code_from_user_id(todoist_user_id)):
        config.logger.info("No authentication code found for user %s creating a new one", todoist_user_id)
        telegram_authentication_code = generate_telegram_authentication_string()
        create_authentication_code(telegram_authentication_code, todoist_user_id)
    else:
        config.logger.info("Found authentication code for user %s", todoist_user_id)
        telegram_authentication_code = telegram_authentication_code_dict["code"]
    return f"https://t.me/{config.telegram.bot_name}?start={telegram_authentication_code}"