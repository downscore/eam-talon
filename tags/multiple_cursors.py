"""Actions and tags for apps that support multiple cursors."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.tag("multiple_cursors", "Application supporting multiple cursors")

ctx.matches = r"""
tag: user.multiple_cursors
"""


@mod.action_class
class Actions:
  """Actions for multiple cursors."""

  def multi_cursor_add_above():
    """Adds cursor to line above."""
    actions.key("cmd-alt-up")

  def multi_cursor_add_below():
    """Adds cursor to line below."""
    actions.key("cmd-alt-down")

  def multi_cursor_select_fewer():
    """Removes selection and cursor at last occurrence."""
    # TODO: Default keystroke for VS Code?
    #actions.key("cmd-u")

  def multi_cursor_select_more():
    """Adds cursor at next occurrence of selection."""
    actions.key("cmd-d")

  def multi_cursor_skip():
    """Skips adding a cursor at next occurrence of selection."""
    actions.key("cmd-k cmd-d")

  def multi_cursor_select_all():
    """Adds cursor at every occurrence of selection."""
    actions.key("cmd-shift-l")

  def multi_cursor_add_to_line_ends():
    """Adds cursor at end of every selected line."""
    actions.key("alt-shift-i")
