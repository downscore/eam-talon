"""Actions and tags for apps with line numbers and splits."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from ..core.lib import number_util

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.splits
and tag: user.line_numbers
"""


@mod.action_class
class Actions:
  """Actions using both line numbers and splits."""

  def splits_line_numbers_bring_line_range(from_index: int, to_index: int = 0):
    """Copies a given line from the previously active split to the cursor location."""
    # TODO: Refactor and reduce duplicated code with line numbers actions.
    if to_index > 0:
      to_index = number_util.copy_leading_decimal_digits(from_index, to_index)
    actions.user.position_mark()
    actions.user.split_last()

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
    actions.user.split_last()
    actions.user.position_restore()
    actions.user.insert_via_clipboard(lines)

  def splits_line_numbers_bring_line_modifier(line_number: int,
                                              modifier_index: int,
                                              modifier_name: str,
                                              delimiter: str = ""):
    """Brings the given modifier at the given index from the given line number in the previously
    active split to the cursor position."""
    # TODO: Refactor and reduce duplicated code with line numbers actions.
    actions.user.position_mark()
    actions.user.split_last()

    # Jump to the line, then select the target.
    actions.user.jump_line(line_number)
    actions.user.textflow_select_nth_modifier(modifier_index, modifier_name, delimiter)
    insert_text = actions.user.selected_text()

    # Go back to original position and insert the text.
    actions.user.split_last()
    actions.user.position_restore()
    actions.user.insert_via_clipboard(insert_text)

  def splits_line_numbers_bring_line_token(line_number: int, from_index: int, to_index: int = 0):
    """Brings the token at the given index, or tokens from the given range, from the given line
    number in the previously active split to the cursor position."""
    # TODO: Refactor and reduce duplicated code with line numbers actions.
    actions.user.position_mark()
    actions.user.split_last()

    # Jump to the line, then select the target.
    actions.user.jump_line(line_number)
    actions.user.textflow_select_nth_token(from_index, to_index)
    insert_text = actions.user.selected_text()

    # Go back to original position and insert the text.
    actions.user.split_last()
    actions.user.position_restore()
    actions.user.insert_via_clipboard(insert_text)

  def splits_line_numbers_bring_line_token_backwards(line_number: int,
                                                     from_index: int,
                                                     to_index: int = 0):
    """Brings the token at the given index, or tokens from the given range, from the given line
    number in the previously active split to the cursor position."""
    # TODO: Refactor and reduce duplicated code with line numbers actions.
    actions.user.position_mark()
    actions.user.split_last()

    # Jump to the line, then select the target.
    actions.user.jump_line(line_number)
    actions.user.line_end()
    actions.user.textflow_select_nth_token_backwards(from_index, to_index)
    insert_text = actions.user.selected_text()

    # Go back to original position and insert the text.
    actions.user.split_last()
    actions.user.position_restore()
    actions.user.insert_via_clipboard(insert_text)

  def splits_line_numbers_bring_line_call(line_number: int, call_index: int):
    """Brings the given function call at the given index from the given line number  in the
    previously active split to the cursor position."""
    # TODO: Refactor and reduce duplicated code with line numbers actions.
    actions.user.position_mark()
    actions.user.split_last()

    # Jump to the line, then select the target.
    actions.user.jump_line(line_number)
    for _ in range(call_index):
      actions.user.textflow_select_nth_modifier(1, "CALL_NEXT")
    insert_text = actions.user.selected_text()

    # Go back to original position and insert the text.
    actions.user.split_last()
    actions.user.position_restore()
    actions.user.insert_via_clipboard(insert_text)

  def splits_line_numbers_bring_line_scope(line_number: int):
    """Brings the scope from the given line number in the previously active split to the cursor
    position."""
    # TODO: Refactor and reduce duplicated code with line numbers actions.
    # Go to the beginning of the line to try to preserve indentation (especially important in
    # python).
    actions.user.line_start()

    actions.user.position_mark()
    actions.user.split_last()

    # Jump to the line, then select the target.
    actions.user.jump_line(line_number)
    actions.user.textflow_select_nth_modifier(1, "SCOPE")
    insert_text = actions.user.selected_text()

    # Go back to original position and insert the text.
    actions.user.split_last()
    actions.user.position_restore()
    actions.user.insert_via_clipboard(insert_text)
