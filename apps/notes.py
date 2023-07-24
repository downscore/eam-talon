"""Talon code for Notes support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.notes = """
os: mac
and app.bundle: com.apple.Notes
"""

ctx.matches = r"""
app: notes
"""


@ctx.action_class("edit")
class EditActions:
  """Action overwrites."""

  def line_swap_down():
    actions.key("cmd-ctrl-down")

  def line_swap_up():
    actions.key("cmd-ctrl-up")

  def paste_match_style():
    actions.key("cmd-shift-alt-v")


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def style_title():
    actions.key("cmd-shift-t")

  def style_subtitle():
    actions.key("cmd-shift-h")

  def style_heading(number: int):
    if number == 1:
      actions.key("cmd-shift-h")
    else:
      actions.key("cmd-shift-j")

  def style_body():
    actions.key("cmd-shift-b")

  def style_bold():
    actions.key("cmd-b")

  def style_italic():
    actions.key("cmd-i")

  def style_underline():
    actions.key("cmd-u")

  def style_strikethrough():
    pass

  def style_bullet_list():
    actions.key("cmd-shift-7")

  def style_numbered_list():
    actions.key("cmd-shift-9")

  def style_checklist():
    actions.key("cmd-shift-l")

  def style_toggle_check():
    actions.key("cmd-shift-u")
