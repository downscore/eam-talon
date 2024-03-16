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


@ctx.action_class("edit")
class EditActions:
  """Action overwrites."""

  def delete_line():
    actions.key("ctrl-u")

  def line_end():
    actions.key("ctrl-e")

  def line_start():
    actions.key("ctrl-a")


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def delete_to_line_end():
    actions.key("ctrl-k")

  def delete_word_left(n: int = 1):
    # Deletes to the end of the line. Makes this command useful for the last word on the line.
    actions.edit.word_left()
    actions.user.delete_to_line_end()

  def split_up():
    app.notify("Only splitting down or right is supported")

  def split_down():
    # Split horizontally.
    actions.key("cmd-shift-d")

  def split_left():
    app.notify("Only splitting down or right is supported")

  def split_right():
    # Split vertically.
    actions.key("cmd-d")

  def split_close():
    actions.key("cmd-w")


@ctx.action_class("app")
class AppActions:
  """Action overwrites."""

  def tab_close():
    # Close all panes in the tab.
    actions.key("cmd-alt-w")
