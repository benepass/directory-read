from datetime import date, datetime, timezone


def rfc3339_formatted_datetime(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat(timespec="seconds")


def datetime_utc_now() -> datetime:
    return datetime.now(timezone.utc)


def date_utc_now() -> date:
    return datetime_utc_now().date()


def rfc3339_utc_now_formatted_datetime() -> str:
    return rfc3339_formatted_datetime(datetime_utc_now())
