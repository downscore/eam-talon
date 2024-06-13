"""Talon code for iTerm2 support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, app

mod = Module()
ctx = Context()

mod.apps.iterm = """
app.bundle: com.googlecode.iterm2
"""

ctx.matches = r"""
app: iterm
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def delete_line():
    actions.key("ctrl-u")

  def line_end():
    actions.key("ctrl-e")

  def line_start():
    actions.key("ctrl-a")

  def delete_to_line_end():
    actions.key("ctrl-k")

  def delete_word_left(n: int = 1):
    # Deletes to the end of the line. Makes this command useful for the last word on the line.
    actions.user.word_left()
    actions.user.delete_to_line_end()

  def split_open_up():
    app.notify("Only splitting down or right is supported")

  def split_open_down():
    # Split horizontally.
    actions.key("cmd-shift-d")

  def split_open_left():
    app.notify("Only splitting down or right is supported")

  def split_open_right():
    # Split vertically.
    actions.key("cmd-d")

  def split_close():
    actions.key("cmd-w")

  def split_next():
    actions.key("cmd-]")

  def split_last():
    actions.key("cmd-[")

  def split_switch_up():
    actions.key("cmd-alt-up")

  def split_switch_down():
    actions.key("cmd-alt-down")

  def split_switch_left():
    actions.key("cmd-alt-left")

  def split_switch_right():
    actions.key("cmd-alt-right")

  def tab_close():
    # Close all panes in the tab.
    actions.key("cmd-alt-w")

  def tab_list(name: str):
    # Use "open quickly" command.
    actions.key("cmd-shift-o")
    actions.sleep("250ms")
    if name:
      actions.insert(name)
      actions.sleep("50ms")
