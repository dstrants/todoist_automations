from fastapi import BackgroundTasks, FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse


from config.base import config
from models.todoist import TodoistWebhook
from tasks.todoist_auth import todoist_oauth_flow_step_2
from tasks.todoist_crud import create_or_update_task, delete_task, complete_task

from tasks import telegram
from utils.start_up import startup_ensure_mongo_unique_id_indexes, startup_ensure_telegram_webhook
from utils.security import todoist_validate_webhook_hmac
from utils.telegram import start_telegram_authentication_process
from tasks.todoist_user import create_user


app = FastAPI()

app.on_event("startup")(startup_ensure_mongo_unique_id_indexes)
app.on_event("startup")(startup_ensure_telegram_webhook)

@app.post("/todoist/webhooks")
async def todoist_webhooks(request: Request, response: Response, webhook: TodoistWebhook, background_tasks: BackgroundTasks):
    if not await todoist_validate_webhook_hmac(request=request):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Request does not have the right format"}
    match webhook.event_name:
        case "item:added" | "item:updated":
            background_tasks.add_task(create_or_update_task, webhook=webhook)
        case "item:deleted":
            background_tasks.add_task(delete_task, webhook=webhook)
        case "item:completed" | "item:uncompleted":
            background_tasks.add_task(complete_task, webhook=webhook)
    return {"message": "Webhook item received"}


@app.get("/health")
async def health():
    return {"message": "Hello World"}


# Todoist Auth Flow

@app.get("/todoist/login")
async def todoist_login_redirect():
    return RedirectResponse(f"https://todoist.com/oauth/authorize?client_id={config.todoist.client_id}&scope=data:read_write,data:delete&state={config.todoist.state_string}")


@app.get("/todoist/callback")
async def todoist_redirect_callback(response: Response, background_tasks: BackgroundTasks, code: str = "", state: str = ""):
    if state != config.todoist.state_string:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Access denied"}

    user_info = await todoist_oauth_flow_step_2(code, full_sync=True)
    print(user_info)
    background_tasks.add_task(create_user, user=user_info)
    telegram_link = start_telegram_authentication_process(user_info["id"])


    return {"message": "Login successful", "telegram_link": telegram_link}


# Telegram Flow
@app.post("/telegram/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    text = data["message"]["text"]

    if text.startswith("/start"):
        background_tasks.add_task(telegram.complete_telegram_verification, webhook_body=data)

    return {"message": "Webhook received"}