"""Talon code for iTerm actions that can be used from other applications."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
  """iTerm global actions."""

  def iterm_focus_new_tab():
    """Changes focus to iterm and opens a new tab."""
    actions.user.switcher_focus("iTerm2")
    actions.user.tab_open()
