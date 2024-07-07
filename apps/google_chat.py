"""Talon code for Google Chat support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.google_chat = """
app.name: Google Chat
"""

ctx.matches = r"""
app: google_chat
"""


@mod.action_class
class Actions:
  """Google Chat actions."""

  def google_chat_focus_search():
    """Focuses the search field in Google Chat."""
    actions.key("escape /")
    actions.sleep("100ms")


@ctx.action_class("user")
class ExtensionActions:
  """Action overrides."""

  def line_insert_down():
    actions.user.line_end()
    actions.key("shift-enter")

  def line_insert_up():
    # Going to line end first can help consistently preserve indentation in code.
    actions.user.line_end()
    actions.user.line_start()
    actions.key("shift-enter up")
