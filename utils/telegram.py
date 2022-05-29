import random
import string

from config.constants import TELEGRAM_BOT_NAME as bot_name
from tasks import telegram_crud


def generate_telegram_authentication_string() -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(48))


def start_telegram_authentication_process(todoist_user_id: int) -> str:
    if not (telegram_authentication_code_dict := telegram_crud.get_authentication_code_from_user_id(todoist_user_id)):
        telegram_authentication_code = generate_telegram_authentication_string()
        telegram_crud.create_authentication_code(telegram_authentication_code, todoist_user_id)
    else:
        telegram_authentication_code = telegram_authentication_code_dict["code"]
    return f"https://t.me/{bot_name}?start={telegram_authentication_code}"
