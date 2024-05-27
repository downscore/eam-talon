"""Talon code for YouTube actions that can be used from other applications."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
  """YouTube global actions."""

  def youtube_focus():
    """Focuses a YouTube tab if one is found open."""
    actions.user.cross_browser_focus_tab_by_hostname("youtube.com")

  def youtube_increase_playback_speed():
    """Increases the playback speed of a YouTube video even if it is not focused."""
    actions.user.switcher_save_focus()
    actions.user.youtube_focus()
    actions.key("shift-.")
    actions.user.switcher_restore_focus()

  def youtube_decrease_playback_speed():
    """Decreases the playback speed of a YouTube video even if it is not focused."""
    actions.user.switcher_save_focus()
    actions.user.youtube_focus()
    actions.key("shift-,")
    actions.user.switcher_restore_focus()

  def youtube_seek_forward():
    """Jumps ahead in a YouTube video even if it is not focused."""
    actions.user.switcher_save_focus()
    actions.user.youtube_focus()
    actions.key("l")
    actions.user.switcher_restore_focus()

  def youtube_seek_backward():
    """Jumps back in a YouTube video even if it is not focused."""
    actions.user.switcher_save_focus()
    actions.user.youtube_focus()
    actions.key("j")
    actions.user.switcher_restore_focus()
