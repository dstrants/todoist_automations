from config.base import config


def create_record(record: dict) -> dict:
    return config.airtable.base.create(record)
