import pytz
from src.config import TIMEZONE_STR

def get_target_timezone():
    try:
        return pytz.timezone(TIMEZONE_STR)
    except pytz.UnknownTimeZoneError:
        return pytz.UTC
