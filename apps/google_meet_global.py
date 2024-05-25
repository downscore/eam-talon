"""Talon code for Google Meet actions that can be used from other applications."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
  """Meet global actions."""

  def google_meet_focus():
    """Focuses a Google Meet tab if one is found open."""
    actions.user.cross_browser_focus_tab_by_hostname("meet.google.com")

  def google_meet_toggle_microphone():
    """Toggles microphone in Google Meet."""
    actions.user.switcher_save_focus()
    actions.user.google_meet_focus()
    actions.key("cmd-d")
    actions.user.switcher_restore_focus()

  def google_meet_toggle_camera():
    """Toggles camera in Google Meet."""
    actions.user.switcher_save_focus()
    actions.user.google_meet_focus()
    actions.key("cmd-e")
    actions.user.switcher_restore_focus()

  def google_meet_toggle_raise_hand():
    """Toggles raising hand in Google Meet."""
    actions.user.switcher_save_focus()
    actions.user.google_meet_focus()
    actions.key("ctrl-cmd-h")
    actions.user.switcher_restore_focus()

  def google_meet_toggle_chat():
    """Toggles showing chat window in Google Meet."""
    actions.user.switcher_save_focus()
    actions.user.google_meet_focus()
    actions.key("ctrl-cmd-c")
    actions.user.switcher_restore_focus()

  def google_meet_toggle_participants():
    """Toggles showing participants in Google Meet."""
    actions.user.switcher_save_focus()
    actions.user.google_meet_focus()
    actions.key("ctrl-cmd-p")
    actions.user.switcher_restore_focus()

  def google_meet_leave_meeting():
    """Leaves the current meeting in Google Meet."""
    actions.user.switcher_save_focus()
    actions.user.google_meet_focus()
    actions.key("cmd-w")
    # Note: If the focus was in the same window, this could switch to the wrong tab after the Meet tab is closed.
    actions.user.switcher_restore_focus()
