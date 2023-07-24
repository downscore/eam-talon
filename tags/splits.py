"""Actions and tags for apps with split windows."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module

mod = Module()
ctx = Context()

mod.tag("splits", "Application with split windows")

ctx.matches = r"""
tag: user.splits
"""


@mod.action_class
class Actions:
  """Split-related actions."""

  def split_up():
    """Splits the current window and moves active window to upper split."""

  def split_down():
    """Splits the current window and moves active window to lower split."""

  def split_left():
    """Splits the current window and moves active window to left split."""

  def split_right():
    """Splits the current window and moves active window to right split."""

  def split_close():
    """Closes the current split."""

  def split_maximize():
    """Maximizes the current split."""

  def split_next():
    """Focuses the next split."""

  def split_last():
    """Focuses the last split."""

  def split_switch_by_index(index: int):
    """Focuses the split with the given index."""
