"""Actions and tags for apps with split windows."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module
from ..core.system import unsupported_command

mod = Module()
ctx = Context()

mod.tag("splits", "Application with split windows")

ctx.matches = r"""
tag: user.splits
"""


@mod.action_class
class Actions:
  """Split-related actions."""

  def split_open_up():
    """Splits the current window and moves active window to upper split."""
    unsupported_command("Opening split above not supported.")

  def split_open_down():
    """Splits the current window and moves active window to lower split."""
    unsupported_command("Opening split below not supported.")

  def split_open_left():
    """Splits the current window and moves active window to left split."""
    unsupported_command("Opening split to the left not supported.")

  def split_open_right():
    """Splits the current window and moves active window to right split."""
    unsupported_command("Opening split to the right not supported.")

  def split_close():
    """Closes the current split."""
    unsupported_command("Closing splits not supported.")

  def split_maximize():
    """Maximizes the current split."""
    unsupported_command("Maximizing splits not supported.")

  def split_next():
    """Focuses the next split."""
    unsupported_command("Switching to next split not supported.")

  def split_last():
    """Focuses the last split."""
    unsupported_command("Switching to last split not supported.")

  def split_switch_up():
    """Focuses the split above the current one."""
    unsupported_command("Switching to split above not supported.")

  def split_switch_down():
    """Focuses the split below the current one."""
    unsupported_command("Switching to split below not supported.")

  def split_switch_left():
    """Focuses the split to the left of the current one."""
    unsupported_command("Switching to split to the left not supported.")

  def split_switch_right():
    """Focuses the split to the right of the current one."""
    unsupported_command("Switching to split to the right not supported.")

  def split_switch_by_index(index: int):
    """Focuses the split with the given index."""
    unsupported_command("Switching to split by index not supported.")

  def split_move_file_up():
    """Moves the current file to the split above."""
    unsupported_command("Moving file to split above not supported.")

  def split_move_file_down():
    """Moves the current file to the split below."""
    unsupported_command("Moving file to split below not supported.")

  def split_move_file_left():
    """Moves the current file to the split to the left."""
    unsupported_command("Moving file to split to the left not supported.")

  def split_move_file_right():
    """Moves the current file to the split to the right."""
    unsupported_command("Moving file to split to the right not supported.")
