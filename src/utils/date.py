from datetime import datetime


def get_datetime_from_iso(date_str: str) -> datetime:
    """
    Return the datetime object from a string in format 2024-02-10T16:20:30.000Z
    """
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
