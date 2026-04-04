from datetime import UTC, datetime, timedelta
from numpy import datetime64, timedelta64

EPOCH = datetime64(0, 's')
SECOND = timedelta64(1, 's')

def dt64_to_dt(dt: datetime64):
    unixtime = (dt - EPOCH) / SECOND
    return datetime.fromtimestamp(unixtime, UTC)

def dt_to_dt64(dt: datetime):
    unixtime = dt.timestamp() // 1
    return EPOCH + SECOND * unixtime

def ceil_to_interval(dt: datetime, hours: int) -> datetime:
    # HACK: this function was written with AI
    assert hours > 0
    interval_s = hours * 3600
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = (dt - midnight).seconds + dt.microsecond / 1_000_000
    # if already exactly on an interval boundary (no fractional seconds)
    if seconds_since_midnight % interval_s == 0 and dt.microsecond == 0:
        return dt
    # next interval offset in seconds (integer)
    next_offset = ((int(seconds_since_midnight) + interval_s) // interval_s) * interval_s
    return midnight + timedelta(seconds=next_offset)

def marks_between(start: datetime, end: datetime, hours: int = 24):
    """
    Yield datetime at every `hours`-mark between start and end inclusive.

    Rounds, so eg if `hours = 12` then markers are at noon and midnight.
    """
    cur = ceil_to_interval(start, hours)
    step = timedelta(hours=hours)
    while cur <= end:
        yield cur
        cur += step
