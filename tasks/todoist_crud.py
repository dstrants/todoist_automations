import pendulum

from config.base import config
from models.todoist import TodoistWebhook
from tasks.automations_items import automations_priority_labelling


def create_or_update_task(webhook: TodoistWebhook) -> None:
    items_collection = config.mongo.todoist_collection()
    items_collection.update_one({"id": webhook.event_data.id}, {"$set": webhook.event_data.dict()}, upsert=True)
    automations_priority_labelling(webhook.event_data)


def delete_task(webhook: TodoistWebhook) -> None:
    items_collection = config.mongo.todoist_collection()
    items_collection.delete_one({"id": webhook.event_data.id})


def complete_task(webhook: TodoistWebhook) -> None:
    create_or_update_task(webhook=webhook)

    log_collection = config.mongo.todoist_collection("completion_logs")
    log_collection.insert_one({
        'task_id': webhook.event_data.id,
        'checked': webhook.event_data.checked,
        'uid': webhook.event_data.user_id,
        'timestamp': pendulum.now(tz=config.timezone)
    })
