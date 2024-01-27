import arrow

from app import settings


def get_utc_as_string() -> str:
    return arrow.utcnow().datetime.strftime(settings.DATETIME_FORMAT)
