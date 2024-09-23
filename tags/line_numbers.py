"""Actions and tags for apps with line numbers."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, clip
from ..core.lib import number_util, scrambler_types as st
from ..core.scrambler_captures import ScramblerMatch

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
    """Selects a range of lines. 1-based. Selects trailing line break if present. If `to_index` is
    zero, selects the from line."""
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
    """Selects text from a range of lines in a way suitable for editing them. 1-based. Does not
    select the trailing line break or leading indentation if a single line is selected. Does select
    trailing line breaks and leading indentation if multiple lines are selected. If `to_index` is
    zero, selects the from line."""
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

  def line_numbers_bring_line_range(from_index: int, to_index: int = 0):
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

  def line_numbers_scrambler_run_command(line_number: int, command_type: st.CommandType,
                                         match: ScramblerMatch):
    """Runs the given command."""
    # Check if we need to save and restore the current cursor position.
    restore_position = command_type not in (st.CommandType.SELECT, st.CommandType.CLEAR_MOVE_CURSOR,
                                            st.CommandType.MOVE_CURSOR_BEFORE,
                                            st.CommandType.MOVE_CURSOR_AFTER)
    if restore_position:
      actions.user.position_mark()

    # Translate "bring" commands to copy commands so we can insert the text after restoring the
    # cursor position.
    is_bring = command_type == st.CommandType.BRING
    if is_bring:
      command_type = st.CommandType.COPY_TO_CLIPBOARD

    # Jump to the line and run the command.
    actions.user.jump_line(line_number)
    if is_bring:
      # Bring commands capture the copied text.
      with clip.capture() as s:
        actions.user.scrambler_run_command(command_type, match)
      try:
        bring_text = s.text()
      except clip.NoChange as exc:
        raise ValueError("No text copied by bring command") from exc
    else:
      actions.user.scrambler_run_command(command_type, match)

    if restore_position:
      actions.user.position_restore()
    if is_bring:
      actions.user.insert_via_clipboard(bring_text)
