"""Talon code for Steam support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.steam = """
os: mac
and app.bundle: com.valvesoftware.steam.helper
"""

ctx.matches = r"""
app: steam
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def app_get_current_directory() -> str:
    # Use the Anki user data directory as current.
    return "/Users/${USER}/Library/Application Support/Steam/steamapps/common/"

  def app_get_current_location() -> str:
    return actions.user.app_get_current_directory()
