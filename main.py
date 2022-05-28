from fastapi import BackgroundTasks, FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse


from config.constants import TODOIST_CLIENT_ID, TODOIST_CLIENT_SECRET, TODOIST_STATE_STRING
from models.todoist import TodoistWebhook
from tasks.todoist_auth import todoist_oauth_flow_step_2
from tasks.todoist_crud import create_task, update_task, delete_task, complete_task
from utils.start_up import startup_ensure_mongo_unique_id_indexes
from utils.security import todoist_validate_webhook_hmac
from utils.telegram import start_telegram_authentication_process
from tasks.todoist_user import create_user


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

    user_info = await todoist_oauth_flow_step_2(code, full_sync=True)
    print(user_info)
    background_tasks.add_task(create_user, user=user_info)
    telegram_link = start_telegram_authentication_process(user_info["id"])


    return {"message": "Login successful", "telegram_link": telegram_link}


# Telegram Flow
# NOTE: WIP unsecure implementation at the moment
@app.post("/telegram/webhooks")
async def telegram_webhook(request: Request, response: Response, background_tasks: BackgroundTasks):
    data = await request.json()

    if data["message"]["text"].startswith("/start"):
        pass
        #background_tasks.add_task(create_task, data= )

    return {"message": "Webhook received"}