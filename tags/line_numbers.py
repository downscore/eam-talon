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


def _insert_placeholder() -> str:
  """Inserts a unique placeholder at the cursor position and returns it."""
  # Insert some unique placeholder text so we can find the current position again later.
  # Note: In VS Code, the workbench.action.navigateBack action is unreliable for finding the insertion position.
  # Reusing the same placeholder can result in the cursor not jumping to it, so we always create a unique one.
  placeholder_uuid = uuid.uuid4()
  placeholder = f"!!!LineNumbers{str(placeholder_uuid)[:5]}!!!"
  actions.user.insert_via_clipboard(placeholder)
  return placeholder


def _restore_position_from_placeholder(placeholder: str):
  """Finds the given placeholder text, moves the cursor to it, and deletes it."""
  actions.user.find()
  actions.user.insert_via_clipboard(placeholder)
  actions.key("escape")
  actions.key("backspace")


@mod.action_class
class Actions:
  """Line-number related actions."""

  def jump_line(n: int):
    """Jumps to the specified line number."""
    actions.key("ctrl-g")
    actions.insert(str(n))
    actions.key("enter")

  def select_line_range_including_line_break(from_index: int, to_index: int = 0):
    """Selects a range of lines. 1-based. Selects trailing line break if present. If `to_index` is zero, selects the
    from line."""
    actions.user.jump_line(from_index)
    if to_index <= from_index:
      actions.user.select_line_including_line_break()
    else:
      for _ in range(to_index - from_index + 1):
        actions.user.extend_down()

  def bring_line_range(from_index: int, to_index: int = 0):
    """Copies a given line to the cursor location."""
    placeholder = _insert_placeholder()

    # Jump to the beginning of the first line, before indentation.
    actions.user.jump_line(from_index)
    actions.user.line_end()
    actions.user.line_start()
    actions.user.line_start()
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
    _restore_position_from_placeholder(placeholder)
    actions.user.insert_via_clipboard(lines)

  def line_numbers_insert_line_above_no_move(n: int):
    """Inserts a line above the given line number without moving the cursor."""
    placeholder = _insert_placeholder()

    # Jump to the beginning of the line, before indentation.
    actions.user.jump_line(n)
    actions.user.line_end()
    actions.user.line_start()
    actions.user.line_start()

    actions.insert("\n")
    _restore_position_from_placeholder(placeholder)

  def line_numbers_insert_line_below_no_move(n: int):
    """Inserts a line below the given line number without moving the cursor."""
    placeholder = _insert_placeholder()

    # Jump to the end of the line.
    actions.user.jump_line(n)
    actions.user.line_end()

    actions.insert("\n")
    _restore_position_from_placeholder(placeholder)
