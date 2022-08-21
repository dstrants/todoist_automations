import sentry_sdk
from fastapi import BackgroundTasks, FastAPI, Request
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from config.base import config
from routes import todoist as todoist_routes
from services.telegram import auth as telegram_auth
from utils import start_up


if config.sentry.dsn:
    sentry_sdk.init(
        dsn=config.sentry.dsn,
        environment=config.env,
        traces_sample_rate=config.sentry.traces_sample_rate,
    )

app = FastAPI()
app.include_router(todoist_routes.router)
app.on_event("startup")(start_up.startup_ensure_mongo_unique_id_indexes)
app.on_event("startup")(start_up.startup_ensure_telegram_webhook)

try:
    app.add_middleware(SentryAsgiMiddleware)
except Exception as e:  # skipcq: PYL-W0703 - Every import error should be handled
    config.logger.warning(f"Failed to add SentryAsgiMiddleware: {e}")


app.include_router

@app.get("/health")
async def health():
    return {"message": "Hello World"}


# Telegram Flow
@app.post("/telegram/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    text = data["message"]["text"]

    if text.startswith("/start"):
        config.logger.info("Received /start command from telegram")
        background_tasks.add_task(telegram_auth.complete_telegram_verification, webhook_body=data)

    return {"message": "Webhook received"}
