"""Actions for remembering and restoring cursor positions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import uuid
from talon import Context, Module, actions

mod = Module()
ctx = Context()

# The placeholder text last used to mark the cursor position.
_last_placeholder = ""


@mod.action_class
class ExtensionActions:
  """Cursor position actions."""

  def position_mark():
    """Sets a mark at or remembers the current cursor position so it can be restored later."""
    # Insert some unique placeholder text so we can find the current position again later.
    # Note: In VS Code, the workbench.action.navigateBack action is unreliable for finding the insertion position.
    # Reusing the same placeholder can result in the cursor not jumping to it, so we always create a unique one.
    global _last_placeholder
    placeholder_uuid = uuid.uuid4()
    placeholder = f"!!!Marker{str(placeholder_uuid)[:5]}!!!"
    actions.user.insert_via_clipboard(placeholder)
    _last_placeholder = placeholder

  def position_restore():
    """Restores the cursor to the last marked position."""
    # Find the placeholder text, move the cursor to it, and delete it.
    global _last_placeholder
    if not _last_placeholder:
      actions.app.notify("No cursor position has been marked.")
      # Raise exception to stop chained commands from executing.
      raise ValueError("No cursor position has been marked.")
    actions.user.find()
    actions.user.insert_via_clipboard(_last_placeholder)
    actions.key("escape")
    actions.key("backspace")
    _last_placeholder = ""
