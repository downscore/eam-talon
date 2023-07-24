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
