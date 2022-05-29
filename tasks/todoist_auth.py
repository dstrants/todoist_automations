import requests
from todoist import TodoistAPI as SyncTodoistAPI

from config.base import config
from tasks.todoist_initial_sync import todoist_import_all


async def todoist_oauth_flow_step_2(code: str, full_sync=False) :
    token = retrieve_user_token(code)

    user_info = await retrieve_user_info(token, full_sync=full_sync)

    return user_info


def retrieve_user_token(code: str) -> str:
    resp = requests.post("https://todoist.com/oauth/access_token", {
        'client_id': config.todoist.client_id,
        'client_secret': config.todoist.client_secret,
        'code': code,
    })
    resp.raise_for_status()
    data = resp.json()

    return data['access_token']


async def retrieve_user_info(token: str, full_sync=False) -> dict:
    api  = SyncTodoistAPI(token)
    api.sync()

    if full_sync:
        await todoist_import_all(api.state)

    return api.state["user"] | {"token": token}