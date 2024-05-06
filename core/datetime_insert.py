"""Talon code for managing datetimes."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import datetime
from talon import Module, actions
from .lib import datetime_util

mod = Module()


@mod.action_class
class Actions:
  """Datetime actions."""

  def time_format(fmt: str = "") -> str:
    """Return the current time, formatted.
        fmt: strftime()-style format string, defaults to ISO format."""
    now = datetime.datetime.now()
    if fmt == "":
      return now.isoformat()
    return now.strftime(fmt)

  def time_format_utc(fmt: str = "") -> str:
    """Return the current UTC time, formatted.
        fmt: strftime()-style format string, defaults to ISO format."""
    now = datetime.datetime.utcnow()
    if fmt == "":
      return now.isoformat()
    return now.strftime(fmt)

  def date_utc(year: str, month: int, day: int) -> str:
    """Gets the given date in UTC format."""
    dt = datetime.datetime(int(year), month, day)
    return dt.strftime("%Y-%m-%d")

  def notify_selected_unix_to_datetime():
    """Convert the selected unix timestamp to a datetime and display it in a notification."""
    dt = datetime_util.convert_unix_timestamp(actions.user.selected_text())
    actions.app.notify(str(dt))

  def clipboard_selected_unix_to_datetime():
    """Convert the selected unix timestamp to a datetime and copy it to the clipboard."""
    dt = datetime_util.convert_unix_timestamp(actions.user.selected_text())
    actions.user.clipboard_history_set_text(str(dt))
