from datetime import datetime, timedelta, date


def from_seconds_to_date(value, as_date=False):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date() if as_date else value
    if isinstance(value, date):
        return value
    if isinstance(value, (int, float)):
        dt = datetime(1970, 1, 1) + timedelta(seconds=value)
        return dt.date() if as_date else dt
