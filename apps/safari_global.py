"""Talon code for Safari actions that can be used from other applications."""
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
  """Safari global actions."""

  def safari_insert_address():
    """Insert the address of the active Safari tab."""
    script = """
      tell application "Safari"
          set theUrl to URL of front document
      end tell
      return theUrl
      """
    result = applescript.run(script)
    actions.user.insert_via_clipboard(result)
