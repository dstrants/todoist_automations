import requests
from asyncio import run
from todoist import TodoistAPI as SyncTodoistAPI


from config.constants import TODOIST_CLIENT_ID, TODOIST_CLIENT_SECRET
from tasks.todoist_user import create_user
from tasks.todoist_initial_sync import todoist_import_all


def todoist_oauth_flow_step_2(code: str, full_sync=False):
    token = retrieve_user_token(code)

    user_info = retrieve_user_info(token, full_sync=full_sync)

    create_user(user_info)


def retrieve_user_token(code: str) -> str:
    if not (TODOIST_CLIENT_ID and TODOIST_CLIENT_SECRET):
        raise ValueError("Todoist application credentials have not been configured")

    resp = requests.post("https://todoist.com/oauth/access_token", {
        'client_id': TODOIST_CLIENT_ID,
        'client_secret': TODOIST_CLIENT_SECRET,
        'code': code,
    })
    resp.raise_for_status()
    data = resp.json()

    return data['access_token']


def retrieve_user_info(token: str, full_sync=False) -> dict:
    api  = SyncTodoistAPI(token)
    api.sync()

    if full_sync:
        run(todoist_import_all(api.state))

    return api.state["user"] | {"token": token}