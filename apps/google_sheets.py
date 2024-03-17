"""Talon code for Google Sheets support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.google_sheets = """
title: /Google Sheets/
"""

ctx.matches = """
app: google_sheets
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
