from config.base import config


def create_record(record: dict, typecast: bool = False) -> dict:
    """
        Creates a record on the tools database on airtable
    """
    return config.airtable.base.create(record, typecast=typecast)
