import pendulum

from config.base import config
from models.todoist import TodoistWebhook
from services.todoist import automations_items


def create_or_update_task(webhook: TodoistWebhook) -> None:
    """Creates or updates a task in the database."""
    items_collection = config.mongo.todoist_collection()
    items_collection.update_one(
        {"id": webhook.event_data.id},
        {"$set": webhook.event_data.dict()},
        upsert=True
    )
    config.logger.info("Created or updated task %s", webhook.event_data.id)
    automations_items.automations_priority_labelling(webhook.event_data)


def delete_task(webhook: TodoistWebhook) -> None:
    """Deletes a task from the database."""
    items_collection = config.mongo.todoist_collection()
    items_collection.delete_one({"id": webhook.event_data.id})
    config.logger.info("Deleted task %s", webhook.event_data.id)


def complete_task(webhook: TodoistWebhook) -> None:
    """
        Mark a task as completed in the database.

        It also creates a audit logging entry for the completion.
    """

    create_or_update_task(webhook=webhook)

    log_collection = config.mongo.todoist_collection("completion_logs")
    log_collection.insert_one({
        'task_id': webhook.event_data.id,
        'checked': webhook.event_data.checked,
        'uid': webhook.event_data.user_id,
        'timestamp': pendulum.now(tz=config.timezone)
    })
    config.logger.info(
        "%s task %s",
        ("Completed" if webhook.event_data.checked else "Uncompleted"),
        webhook.event_data.id
    )
