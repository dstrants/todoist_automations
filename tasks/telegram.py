from telegram import Bot, Message

from config.base import config

from tasks import todoist_user as users
from tasks import telegram_crud

def complete_telegram_verification(webhook_body: dict):
    if webhook_body["message"]["text"].startswith("/start"):
        code = webhook_body["message"]["text"].split(" ")[1]
        if result := telegram_crud.get_authentication_code_from_code(code=code):
            user = users.find_user_by_query({"id": result["todoist_user_id"]})

            if not user:
                config.logger.warning("User %s not found", result["todoist_user_id"])
                return None

            updated_user = user | {"telegram_chat_id": webhook_body["message"]["chat"]["id"]}
            users.update_user(user=updated_user)
            telegram_crud.delete_authentication_code_from_code(code=code)
            send_telegram_message(message="Your account has been successfully verified", chat_id=webhook_body["message"]["chat"]["id"])
            config.logger.info("User's %s telegram profile has been verified", user["id"])
            return None
        config.logger.warning("Authentication code %s not found", code)
        return None
    config.logger.warning("Message is not a start command")



def send_telegram_message(message: str, chat_id: int) -> Message:
    bot = Bot(token=config.telegram.bot_token)
    config.logger.info("Sending message to chat %s", chat_id)
    return bot.send_message(chat_id=chat_id, text=message)