"""Talon code for Terminal support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.terminal = """
os: mac
and app.bundle: com.apple.Terminal
"""

ctx.matches = r"""
app: terminal
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
    # Only split down action is available.
    actions.key("cmd-d")

  def split_open_down():
    actions.key("cmd-d")

  def split_close():
    actions.key("cmd-shift-d")

  def tab_left():
    actions.key("ctrl-shift-tab")

  def tab_right():
    actions.key("ctrl-tab")
