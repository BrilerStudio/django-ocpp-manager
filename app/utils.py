from datetime import datetime


def get_utc_as_string() -> str:
    return datetime.utcnow().isoformat()
