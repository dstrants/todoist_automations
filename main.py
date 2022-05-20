from fastapi import BackgroundTasks, FastAPI, Response, status
from fastapi.responses import RedirectResponse


from config.constants import TODOIST_CLIENT_ID, TODOIST_CLIENT_SECRET, TODOIST_STATE_STRING
from models.todoist import TodoistWebhook
from tasks.todoist_auth import todoist_oauth_flow_step_2
from tasks.todoist_crud import create_task


app = FastAPI()


@app.post("/todoist/webhooks")
async def todoist_webhooks(item: TodoistWebhook, background_tasks: BackgroundTasks):
    background_tasks.add_task(create_task, webhook=item)
    return {"message": "Item has been created"}


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
