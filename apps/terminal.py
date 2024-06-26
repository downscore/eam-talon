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
