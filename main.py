from fastapi import BackgroundTasks, FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse


from config.constants import TODOIST_CLIENT_ID, TODOIST_CLIENT_SECRET, TODOIST_STATE_STRING
from models.todoist import TodoistWebhook
from models.telegram import TelegramLogin
from tasks.todoist_auth import todoist_oauth_flow_step_2
from tasks.todoist_crud import create_task, update_task, delete_task, complete_task
from tasks.telegram import telegram_send_authorization_code_to_user
from utils.start_up import startup_ensure_mongo_unique_id_indexes
from utils.security import todoist_validate_webhook_hmac


app = FastAPI()

app.on_event("startup")(startup_ensure_mongo_unique_id_indexes)

@app.post("/todoist/webhooks")
async def todoist_webhooks(request: Request, response: Response, webhook: TodoistWebhook, background_tasks: BackgroundTasks):
    if not await todoist_validate_webhook_hmac(request=request):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Request does not have the right format"}
    match webhook.event_name:
        case "item:added":
            background_tasks.add_task(create_task, webhook=webhook)
        case "item:updated":
            background_tasks.add_task(update_task, webhook=webhook)
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
async def todoist_login_redirect(response: Response):
    if not (TODOIST_CLIENT_ID and TODOIST_CLIENT_SECRET and TODOIST_STATE_STRING):
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return {"message": "No configuration available"}
    return RedirectResponse(f"https://todoist.com/oauth/authorize?client_id={TODOIST_CLIENT_ID}&scope=data:read_write,data:delete&state={TODOIST_STATE_STRING}")


@app.get("/todoist/callback")
async def todoist_redirect_callback(response: Response, background_tasks: BackgroundTasks, code: str = "", state: str = ""):
    if state != TODOIST_STATE_STRING:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Access denied"}
    background_tasks.add_task(todoist_oauth_flow_step_2, code=code, full_sync=True)
    return {"message": "Login successful"}


# Telegram Bot Authentication
@app.post("/telegram/login")
async def telegram_login_redirect(response: Response, background_tasks: BackgroundTasks, body: TelegramLogin):
    background_tasks.add_task(telegram_send_authorization_code_to_user, phone=body.phone)
    return {"message": "Authorization code sent"}


