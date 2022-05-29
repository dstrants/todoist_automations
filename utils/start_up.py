from pymongo import ASCENDING
from telegram import Bot

from config.base import config


async def startup_ensure_mongo_unique_id_indexes():
    for collection_name in {'items', 'projects', 'labels'}:
        collection = config.mongo.todoist_collection(collection_name)
        existing_indexes = collection.index_information().keys()
        if f"id_1" in existing_indexes:
            continue

        collection.create_index([("id", ASCENDING)], unique=True)

async def startup_ensure_telegram_webhook():
    bot = Bot(token=config.telegram.bot_token)
    webhook_info = bot.get_webhook_info()
    if webhook_info.url != f"{config.host}/telegram/webhook":
        config.logger.info("Setting up telegram webhook to %s/telegram/webhook", config.host)
        bot.set_webhook(f"{config.host}/telegram/webhook")
