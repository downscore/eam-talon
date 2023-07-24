"""Talon code for Warp Terminal support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.warp = """
os: mac
and app.bundle: dev.warp.Warp-Stable
"""

ctx.matches = r"""
app: warp
"""


@ctx.action_class("edit")
class EditActions:
  """Action overwrites."""

  def line_insert_down():
    actions.edit.line_end()
    actions.key("shift-enter")

  def line_insert_up():
    # Going to line end first can help consistently preserve indentation in code.
    actions.edit.line_end()
    actions.edit.line_start()
    actions.key("shift-enter up")


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def multi_cursor_select_more():
    actions.key("ctrl-g")

  def multi_cursor_add_above():
    actions.key("ctrl-shift-up")

  def multi_cursor_add_below():
    actions.key("ctrl-shift-down")

  def split_up():
    # Only split down action is available.
    actions.key("cmd-shift-d")

  def split_down():
    actions.key("cmd-shift-d")

  def split_left():
    # Only split right action is available.
    actions.key("cmd-d")

  def split_right():
    actions.key("cmd-d")

  def split_close():
    actions.key("ctrl-d")

  def split_maximize():
    actions.key("cmd-shift-enter")

  def split_next():
    actions.key("cmd-]")

  def split_last():
    actions.key("cmd-[")

  def tab_left():
    actions.key("ctrl-shift-tab")

  def tab_right():
    actions.key("ctrl-tab")
