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

  def obsidian_open_document(document_name: str = ""):
    """Focuses Obsidian and opens the given document. Remains on the currently-open document if no document name is
    provided."""
    actions.user.switcher_focus_app_by_name("Obsidian")
    actions.sleep("50ms")
    if document_name:
      actions.key("cmd-o")
      actions.user.insert_via_clipboard(document_name)
      actions.key("enter")
      actions.sleep("50ms")

  def obsidian_append_to_document(document_name: str = "", section_name: str = ""):
    """Focuses Obsidian and adds a new entry to the given section of the given document.
    Uses the currently-open document if no document name is provided.
    Appends to the bottom of the document if no section name is provided."""
    actions.user.obsidian_open_document(document_name)
    if section_name:
      actions.user.textflow_move_cursor_after_markdown_section(section_name)
    else:
      actions.user.file_end()
    actions.user.line_insert_down()
