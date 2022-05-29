from pymongo import ASCENDING

from utils.mongo import mongo_collection

from telegram import Bot

from config.constants import TELEGRAM_BOT_TOKEN as token, APPLICATION_HOST as host

async def startup_ensure_mongo_unique_id_indexes():
    for collection_name in {'items', 'projects', 'labels'}:
        collection = mongo_collection(collection_name)
        existing_indexes = collection.index_information().keys()
        if f"id_1" in existing_indexes:
            continue

        collection.create_index([("id", ASCENDING)], unique=True)

async def startup_ensure_telegram_webhook():
    if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    bot = Bot(token=token)
    webhook_info = bot.get_webhook_info()
    if webhook_info.url != f"{host}/telegram/webhook":
        bot.set_webhook(f"{host}/telegram/webhook")
