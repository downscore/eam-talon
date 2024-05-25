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
