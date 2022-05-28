from telethon.sync import TelegramClient

from config.constants import TELEGRAM_BOT_ID, TELEGRAM_BOT_TOKEN


def get_telegram_client():
    """
    Returns a TelegramClient instance.
    """
    if not (TELEGRAM_BOT_ID and TELEGRAM_BOT_TOKEN):
        raise ValueError("TELEGRAM_BOT_ID and TELEGRAM_BOT_TOKEN env variables must be set.")


    return TelegramClient(
        "userbot",
        api_id=int(TELEGRAM_BOT_ID),
        api_hash=TELEGRAM_BOT_TOKEN,
    )