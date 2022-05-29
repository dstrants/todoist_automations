import pendulum

from config.base import config
from models.todoist import TodoistWebhook
from tasks.automations_items import automations_priority_labelling
from utils.mongo import mongo_collection

def create_task(webhook: TodoistWebhook) -> None:
    items_collection = mongo_collection()
    items_collection.insert_one(webhook.event_data.dict())
    automations_priority_labelling(webhook.event_data)


def update_task(webhook: TodoistWebhook) -> None:
    items_collection = mongo_collection()
    result = items_collection.update_one({"id": webhook.event_data.id}, {"$set": webhook.event_data.dict()})
    if not result.matched_count:
        # TODO: Replace with actual logging
        print("Task with id {webhook.event_data.id} has not been found. Will be created!")
        create_task(webhook=webhook)
        return None
    automations_priority_labelling(webhook.event_data)


def delete_task(webhook: TodoistWebhook) -> None:
    items_collection = mongo_collection()
    items_collection.delete_one({"id": webhook.event_data.id})


def complete_task(webhook: TodoistWebhook) -> None:
    update_task(webhook=webhook)

    log_collection = mongo_collection("completion_logs")
    log_collection.insert_one({
        'task_id': webhook.event_data.id,
        'checked': webhook.event_data.checked,
        'uid': webhook.event_data.user_id,
        'timestamp': pendulum.now(tz=config.timezone)
         })
