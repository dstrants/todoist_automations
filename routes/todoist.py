from fastapi import APIRouter, BackgroundTasks, Request, Response, status
from fastapi.responses import RedirectResponse
from requests.exceptions import HTTPError

from config.base import config
from models.todoist import TodoistWebhook
from services.telegram import auth as telegram_auth
from services.todoist import auth as todoist_auth
from services.todoist import items as todoist_items
from services.todoist import users as todoist_users
from utils.security import todoist_validate_webhook_hmac

router = APIRouter(
    prefix="/todoist",
    tags=["todoist"],
    responses={404: {"description": "Not found"}},
)


@router.post("/webhooks")
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


# Todoist Auth Flow

@router.get("/login")
async def todoist_login_redirect():
    return RedirectResponse(config.todoist.oauth_full_url)


@router.get("/callback")
async def todoist_redirect_callback(response: Response, background_tasks: BackgroundTasks,
                                    code: str = "", state: str = ""):
    if state != config.todoist.state_string:
        config.logger.info("Invalid state string from todoist callback")
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Access denied"}

    try:
        user_info = await todoist_auth.todoist_oauth_flow_step_2(code, full_sync=True)
    except HTTPError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid code"}

    background_tasks.add_task(todoist_users.create_user, user=user_info)
    telegram_link = telegram_auth.start_telegram_authentication_process(user_info["id"])

    return {"message": "Login successful", "telegram_link": telegram_link}
