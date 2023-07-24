"""Talon code for Finder support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module
from talon.mac import applescript

mod = Module()
ctx = Context()

ctx.matches = r"""
os: mac
"""


@mod.action_class
class Actions:
  """MacOS system actions."""

  def macos_close_all_notifications():
    """Closes all open notifications."""
    applescript.run(r"""
      # Ventura
      tell application "System Events"
        try
          set _groups to groups of UI element 1 of scroll area 1 of group 1 of window "Notification Center" of application process "NotificationCenter"
          repeat with _group in _groups
            set _actions to actions of _group
            repeat with _action in _actions
              if description of _action is in {"Close", "Clear All"} then
                perform _action
                exit repeat
              end if
            end repeat
          end repeat
        end try
      end tell""")
