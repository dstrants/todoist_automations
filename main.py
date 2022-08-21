import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from config.base import config
from routes import todoist as todoist_routes
from routes import telegram as telegram_routes
from utils import start_up


if config.sentry.dsn:
    sentry_sdk.init(
        dsn=config.sentry.dsn,
        environment=config.env,
        traces_sample_rate=config.sentry.traces_sample_rate,
    )

app = FastAPI()
app.include_router(todoist_routes.router)
app.include_router(telegram_routes.router)
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
