"""Talon code for Obsidian actions that can be used from other applications."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
  """Obsidian global actions."""

  def obsidian_add_context():
    """Focus Obsidian and add a new entry to the context section of the current document."""
    actions.user.switcher_focus_app_by_name("Obsidian")
    actions.user.textflow_move_cursor_after_markdown_section("Context")
    actions.user.line_insert_down()

  def obsidian_add_task():
    """Focus Obsidian and add a new entry to the tasks section of the current document."""
    actions.user.switcher_focus_app_by_name("Obsidian")
    actions.user.textflow_move_cursor_after_markdown_section("Tasks")
    actions.user.line_insert_down()
