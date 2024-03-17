"""Actions and tags for apps with line numbers."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import uuid
from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.tag("line_numbers", "Apps with line numbers")

ctx.matches = r"""
tag: user.line_numbers
"""


@mod.action_class
class Actions:
  """Line-number related actions."""

  def jump_line(n: int):
    """Jumps to the specified line number."""
    actions.key("ctrl-g")
    actions.insert(str(n))
    actions.key("enter")

  def select_line_range(from_index: int, to_index: int = 0):
    """Selects a range of lines. 1-based. If `to_index` is zero, selects the from line."""
    actions.user.jump_line(from_index)
    if to_index <= from_index:
      actions.user.select_line()
    else:
      for _ in range(to_index - from_index + 1):
        actions.user.extend_down()

  def bring_line_range(from_index: int, to_index: int = 0):
    """Copies a given line to the cursor location."""
    # Insert some unique placeholder text so we can find the insertion position later.
    # Note: In VS Code, the workbench.action.navigateBack action is unreliable for finding the insertion position.
    # Reusing the same placeholder can result in the cursor not jumping to it, so we always create a unique one.
    placeholder_uuid = uuid.uuid4()
    placeholder = f"!!!BringLine{str(placeholder_uuid)[:5]}!!!"
    actions.user.insert_via_clipboard(placeholder)

    # In VS Code, jumps to beginning of line, before indentation.
    actions.user.jump_line(from_index)
    if to_index <= from_index:
      # Get single line without trailing newline.
      actions.user.extend_line_end()
    else:
      for _ in range(to_index - from_index + 1):
        actions.user.extend_down()
      # Deselect the last line's newline.
      actions.user.extend_left()
    actions.sleep("100ms")

    lines = actions.user.selected_text()

    # Go back to original position and insert the line.
    actions.user.find()
    actions.user.insert_via_clipboard(placeholder)
    actions.key("escape")
    actions.user.insert_via_clipboard(lines)
