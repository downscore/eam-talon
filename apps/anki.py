"""Talon code for Anki support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module

mod = Module()
ctx = Context()

mod.apps.anki = """
app.name: Anki
"""

ctx.matches = r"""
app: anki
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def app_get_current_directory() -> str:
    # Use the Anki user data directory as current.
    return "/Users/${USER}/Library/Application Support/Anki2"
