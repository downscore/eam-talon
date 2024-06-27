"""Talon code for MacOS support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import subprocess
from talon import Context, Module, actions
from talon.mac import applescript

mod = Module()
ctx = Context()

ctx.matches = r"""
os: mac
"""


@mod.action_class
class Actions:
  """MacOS system actions."""

  def notifications_close():
    """Action that can be overridden to close app-specific notifications in addition to system ones."""
    actions.user.macos_close_all_notifications()

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

  def macos_beep():
    """Plays a system beep sound."""
    subprocess.Popen(["afplay", "/System/Library/Sounds/Ping.aiff"])

  def macos_spotlight(query: str = ""):
    """Opens Spotlight and optionally opens the first result for the given query."""
    actions.key("cmd-space")
    actions.sleep("100ms")
    if query:
      actions.insert(query)
      actions.sleep("100ms")
      actions.key("enter")
      actions.sleep("100ms")

  def macos_change_sound_output_device(device_name: str):
    """Change the selected audio output device to the given device name."""
    if not device_name:
      raise ValueError("Device name must be provided.")
    actions.user.macos_spotlight("Sound output")

    # Wait for the sound output window to open and populate. This can take a while, especially if there are airplay
    # devices.
    actions.sleep("1500ms")

    # Click on the given device name.
    actions.user.mouse_ocr_click(device_name, button=0, use_active_window=True, interactive_disambiguation=False)
