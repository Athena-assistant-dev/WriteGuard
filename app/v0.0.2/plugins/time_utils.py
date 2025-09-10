import os
import pytz
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

WINDOWS_TO_IANA = {
    "Central America Standard Time": "America/Costa_Rica",
    "Pacific Standard Time": "America/Los_Angeles",
    "Eastern Standard Time": "America/New_York",
    # Add more as needed
}

def get_local_timestamp(as_datetime=False):
    """
    Returns a local timestamp string in the format YYYY-MM-DD_HH-MM-SS
    using TIMEZONE env var or UTC fallback. Includes short hash for uniqueness.
    If as_datetime is True, returns a datetime object instead.
    """
    timezone_str = os.getenv("TIMEZONE", "UTC")
    try:
        tz = pytz.timezone(timezone_str)
    except Exception:
        tz = pytz.timezone(WINDOWS_TO_IANA.get(timezone_str, "UTC"))

    local_time = datetime.now(tz)
    if as_datetime:
        return local_time

    ts = local_time.strftime("%Y-%m-%d_%H-%M-%S")
    ts_hash = hashlib.md5(ts.encode("utf-8")).hexdigest()[:6]
    logger.info(f"[TimeUtils] Using timezone: {timezone_str}, local time: {ts}")
    return f"{ts}_{ts_hash}"

