"""Utilities for parsing and converting timestamps."""

import datetime
import time


def convert_unix_timestamp(ts: str) -> datetime.datetime:
  """Converts unix timestamp to a datetime."""
  timestamp = ts.strip()

  # If timestamp is integral, truncate to seconds.
  if not "." in timestamp and len(timestamp) > 10:
    timestamp = timestamp[:10]

  return datetime.datetime.fromtimestamp(float(timestamp))


def datetime_to_unix(dt: datetime.datetime) -> int:
  """Converts a datetime to a unix timestamp."""
  return int(time.mktime(dt.timetuple()))


# TODO: datetime_to_epoch - same as datetime_to_unix but floating point.
