"""Actions and tags for apps with line numbers and splits."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, clip
from ..core.lib import number_util, scrambler_types as st
from ..core.scrambler_captures import ScramblerMatch

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

  def splits_line_numbers_scrambler_run_command(line_number: int, command_type: st.CommandType,
                                                match: ScramblerMatch, cross_splits: bool):
    """Runs the given scrambler command on the given line. Optionally runs the command in the
    previously used split."""
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

    # Cross splits, jump to the line, and run the command.
    if cross_splits:
      actions.user.split_last()
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
      if cross_splits:
        actions.user.split_last()
      actions.user.position_restore()
    if is_bring:
      actions.user.insert_via_clipboard(bring_text)
