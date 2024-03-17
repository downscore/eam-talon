"""Talon code for Slack support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.slack = """
os: mac
and app.bundle: com.tinyspeck.slackmacgap
"""

ctx.matches = r"""
app: slack
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def line_insert_down():
    actions.user.line_end()
    actions.key("shift-enter")

  def line_insert_up():
    # Going to line end first can help consistently preserve indentation in code.
    actions.user.line_end()
    actions.user.line_start()
    actions.key("shift-enter up")

  def insert_link():
    actions.key("cmd-shift-u")

  def style_bold():
    actions.key("cmd-b")

  def style_italic():
    actions.key("cmd-i")

  def style_strikethrough():
    actions.key("cmd-shift-x")

  def style_bullet_list():
    actions.key("cmd-shift-8")

  def style_numbered_list():
    actions.key("cmd-shift-7")
