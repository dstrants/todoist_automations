import random
import string

from tasks.telergam_crud import create_authentication_code


def generate_telegram_authentication_string() -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(48))


def start_telegram_authentication_process(todoist_user_id: int) -> str:
    telegram_authentication_code = generate_telegram_authentication_string()
    create_authentication_code(telegram_authentication_code, todoist_user_id)
    return f"https://t.me/doister_stg?start={telegram_authentication_code}"