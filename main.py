from fastapi import BackgroundTasks, FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse

from config.base import config
from models.todoist import TodoistWebhook
from services.telegram import auth as telegram_auth
from services.todoist import auth as todoist_auth
from services.todoist import items as todoist_items
from services.todoist import users as todoist_users
from utils import start_up
from utils.security import todoist_validate_webhook_hmac

app = FastAPI()
app.on_event("startup")(start_up.startup_ensure_mongo_unique_id_indexes)
app.on_event("startup")(start_up.startup_ensure_telegram_webhook)


@app.post("/todoist/webhooks")
async def todoist_webhooks(request: Request, response: Response,
                           webhook: TodoistWebhook, background_tasks: BackgroundTasks):
    if not await todoist_validate_webhook_hmac(request=request):
        config.logger.info("Invalid webhook HMAC")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Request does not have the right format"}
    config.logger.info("Received webhook from todoist with event type: %s", webhook.event_name)
    match webhook.event_name:
        case "item:added" | "item:updated":
            background_tasks.add_task(todoist_items.create_or_update_task, webhook=webhook)
        case "item:deleted":
            background_tasks.add_task(todoist_items.delete_task, webhook=webhook)
        case "item:completed" | "item:uncompleted":
            background_tasks.add_task(todoist_items.complete_task, webhook=webhook)
    return {"message": "Webhook item received"}


@app.get("/health")
async def health():
    return {"message": "Hello World"}


# Todoist Auth Flow

@app.get("/todoist/login")
async def todoist_login_redirect():
    return RedirectResponse(f"https://todoist.com/oauth/authorize?client_id={config.todoist.client_id}&scope=data:read_write,data:delete&state={config.todoist.state_string}")


@app.get("/todoist/callback")
async def todoist_redirect_callback(response: Response, background_tasks: BackgroundTasks,
                                    code: str = "", state: str = ""):
    if state != config.todoist.state_string:
        config.logger.info("Invalid state string from todoist callback")
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Access denied"}

    user_info = await todoist_auth.todoist_oauth_flow_step_2(code, full_sync=True)
    background_tasks.add_task(todoist_users.create_user, user=user_info)
    telegram_link = telegram_auth.start_telegram_authentication_process(user_info["id"])

    return {"message": "Login successful", "telegram_link": telegram_link}


# Telegram Flow
@app.post("/telegram/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    text = data["message"]["text"]

    if text.startswith("/start"):
        config.logger.info("Received /start command from telegram")
        background_tasks.add_task(telegram_auth.complete_telegram_verification, webhook_body=data)

    return {"message": "Webhook received"}
