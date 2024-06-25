"""Talon code for Alacritty support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.alacritty = """
app.bundle: org.alacritty
"""

ctx.matches = r"""
app: alacritty
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def delete_line():
    actions.key("ctrl-u")

  def line_end():
    actions.key("ctrl-e")
