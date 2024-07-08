"""Actions and tags for apps with line numbers."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from ..core.lib import number_util

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

  def select_line_range_including_line_break(from_index: int, to_index: int = 0):
    """Selects a range of lines. 1-based. Selects trailing line break if present. If `to_index` is zero, selects the
    from line."""
    if to_index > 0:
      to_index = number_util.copy_leading_decimal_digits(from_index, to_index)
    actions.user.jump_line(from_index)
    if to_index <= from_index:
      actions.user.select_line_including_line_break()
    else:
      for _ in range(to_index - from_index):
        actions.user.extend_down()
      actions.user.extend_line_end()
      actions.user.extend_right()

  def select_line_range_for_editing(from_index: int, to_index: int = 0):
    """Selects text from a range of lines in a way suitable for editing them. 1-based. Does not select the trailing line
    break or leading indentation if a single line is selected. Does select trailing line breaks and leading indentation
    if multiple lines are selected. If `to_index` is zero, selects the from line."""
    if to_index > 0:
      to_index = number_util.copy_leading_decimal_digits(from_index, to_index)
    actions.user.jump_line(from_index)
    actions.user.line_start()
    if to_index <= from_index:
      actions.user.select_line_excluding_line_break()
    else:
      for _ in range(to_index - from_index):
        actions.user.extend_down()
      actions.user.extend_line_end()
      actions.user.extend_right()

  def bring_line_range(from_index: int, to_index: int = 0):
    """Copies a given line to the cursor location."""
    if to_index > 0:
      to_index = number_util.copy_leading_decimal_digits(from_index, to_index)
    actions.user.position_mark()

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
    actions.user.position_restore()
    actions.user.insert_via_clipboard(lines)

  def line_numbers_insert_line_above_no_move(n: int):
    """Inserts a line above the given line number without moving the cursor."""
    actions.user.position_mark()

    # Jump to the beginning of the line, before indentation.
    actions.user.jump_line(n)
    actions.user.line_end()
    actions.user.line_start()
    actions.user.line_start()

    actions.insert("\n")
    actions.user.position_restore()

  def line_numbers_insert_line_below_no_move(n: int):
    """Inserts a line below the given line number without moving the cursor."""
    actions.user.position_mark()

    # Jump to the end of the line.
    actions.user.jump_line(n)
    actions.user.line_end()

    actions.insert("\n")
    actions.user.position_restore()

  def line_numbers_bring_line_modifier(line_number: int, modifier_index: int, modifier_name: str, delimiter: str = ""):
    """Brings the given modifier at the given index from the given line number to the cursor position."""
    actions.user.position_mark()

    # Jump to the line, then select the target.
    actions.user.jump_line(line_number)
    actions.user.textflow_select_nth_modifier(modifier_index, modifier_name, delimiter)
    insert_text = actions.user.selected_text()

    # Go back to original position and insert the text.
    actions.user.position_restore()
    actions.user.insert_via_clipboard(insert_text)

  def line_numbers_bring_line_token(line_number: int, from_index: int, to_index: int = 0):
    """Brings the token at the given index, or tokens from the given range, from the given line number to the cursor
    position."""
    actions.user.position_mark()

    # Jump to the line, then select the target.
    actions.user.jump_line(line_number)
    actions.user.textflow_select_nth_token(from_index, to_index)
    insert_text = actions.user.selected_text()

    # Go back to original position and insert the text.
    actions.user.position_restore()
    actions.user.insert_via_clipboard(insert_text)

  def line_numbers_bring_line_call(line_number: int, call_index: int):
    """Brings the given function call at the given index from the given line number to the cursor position."""
    actions.user.position_mark()

    # Jump to the line, then select the target.
    actions.user.jump_line(line_number)
    for _ in range(call_index):
      actions.user.textflow_select_nth_modifier(1, "CALL_NEXT")
    insert_text = actions.user.selected_text()

    # Go back to original position and insert the text.
    actions.user.position_restore()
    actions.user.insert_via_clipboard(insert_text)

  def line_numbers_bring_line_scope(line_number: int):
    """Brings the scope from the given line number to the cursor position."""
    # Go to the beginning of the line to try to preserve indentation (especially important in python).
    actions.user.line_start()

    actions.user.position_mark()

    # Jump to the line, then select the target.
    actions.user.jump_line(line_number)
    actions.user.textflow_select_nth_modifier(1, "SCOPE")
    insert_text = actions.user.selected_text()

    # Go back to original position and insert the text.
    actions.user.position_restore()
    actions.user.insert_via_clipboard(insert_text)
