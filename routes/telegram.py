from fastapi import APIRouter, BackgroundTasks, Request

from config.base import config
from services.telegram import auth as telegram_auth

router = APIRouter(
    prefix="/telegram",
    tags=["telegram"],
    responses={404: {"description": "Not found"}},
)


@router.post("/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    """Telegram webhook endpoint. Receives updates from the telegram bot."""
    data = await request.json()
    text = data["message"]["text"]

    if text.startswith("/start"):
        config.logger.info("Received /start command from telegram")
        background_tasks.add_task(telegram_auth.complete_telegram_verification, webhook_body=data)

    return {"message": "Webhook received"}
