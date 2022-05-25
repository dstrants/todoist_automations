from os import environ as env

TODOIST_CLIENT_ID = env.get("TODOIST_CLIENT_ID", None)
TODOIST_CLIENT_SECRET = env.get("TODOIST_CLIENT_SECRET", None)
TODOIST_STATE_STRING = env.get("STATE_STRING", None)

MONGO_CLIENT = env.get("MONGO_CLIENT", None)
PRIORITY_LABELS_INPUT = env.get("TODOIST_PRIORITY_LABELS", "high,big,medium,quick")
PRIORITY_LABELS = PRIORITY_LABELS_INPUT.split(",")

TIMEZONE = env.get("TIMEZONE", "Europe/Athens")