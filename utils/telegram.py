import random
import string

from config.base import config
from tasks import telegram_crud


def generate_telegram_authentication_string() -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(48))


def start_telegram_authentication_process(todoist_user_id: int) -> str:
    if not (telegram_authentication_code_dict := telegram_crud.get_authentication_code_from_user_id(todoist_user_id)):
        config.logger.info("No authentication code found for user %s creating a new one", todoist_user_id)
        telegram_authentication_code = generate_telegram_authentication_string()
        telegram_crud.create_authentication_code(telegram_authentication_code, todoist_user_id)
    else:
        config.logger.info("Found authentication code for user %s", todoist_user_id)
        telegram_authentication_code = telegram_authentication_code_dict["code"]
    return f"https://t.me/{config.telegram.bot_name}?start={telegram_authentication_code}"
