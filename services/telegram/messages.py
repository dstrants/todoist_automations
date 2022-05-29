from telegram import Bot, Message

from config.base import config


def send_telegram_message(message: str, chat_id: int) -> Message:
    bot = Bot(token=config.telegram.bot_token)
    config.logger.info("Sending message to chat %s", chat_id)
    return bot.send_message(chat_id=chat_id, text=message)