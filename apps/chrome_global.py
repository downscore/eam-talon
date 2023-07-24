"""Talon code for Chrome actions that can be used from other applications."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from talon.mac import applescript

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
  """Chrome global actions."""

  def chrome_insert_address():
    """Insert the address of the active Chrome tab."""
    script = """
      tell application "Google Chrome"
          set theUrl to URL of active tab of window 1
      end tell
      return theUrl
      """
    result = applescript.run(script)
    actions.user.insert_via_clipboard(result)
