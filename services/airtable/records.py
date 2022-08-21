from config.base import config


def create_record(record: dict, typecast: bool = False) -> dict:
    return config.airtable.base.create(record, typecast=typecast)
