"""Talon code for Neovim support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, clip
from ..core.lib import number_util, scrambler_types as st
from ..core import mode_dictation

mod = Module()
ctx = Context()

mod.apps.neovim = """
app.bundle: org.alacritty
title: / - neovim$/
"""

ctx.matches = r"""
app: neovim
"""

_MARK = "q"  # Mark to use for temporary navigation.


def _insert_mode(context: st.Context):
  """Change the editor to insert mode. No-op if it is already in insert mode."""
  if context.editor_mode == "i":
    return
  if context.editor_mode != "n":
    actions.key("escape")
  actions.key("i")


def _normal_mode(context: st.Context):
  """Change the editor to normal mode. No-op if it is already in normal mode."""
  if context.editor_mode == "n":
    return
  actions.key("escape")


def _move_cursor_to_start_of_range(text_range: st.TextRange, context: st.Context):
  """Moves the cursor to the start of the given range. Ends in normal mode."""
  # Make sure all the indices are in bounds. They should be relative to the first character in the
  # context text.
  if context.selection_range.start > len(context.text) or context.selection_range.end > len(
      context.text):
    raise ValueError(f"Selection index outside of context text. Context: {context}")
  if context.selection_range.length() != 0 and context.editor_mode != "v":
    raise ValueError("Non-empty selection in non-visual mode. Context: {context}")
  if text_range.start > len(context.text) or text_range.end > len(context.text):
    raise ValueError("Editor action start index outside of context text. "
                     f"Range: {text_range}, Context: {context}")

  # If there is a non-empty selection, jump to the beginning of the selection.
  _normal_mode(context)
  if context.selection_range.start != context.selection_range.end:
    actions.insert("`<")  # Jump to the beginning of the selection.

  if text_range.start < context.selection_range.start:
    move_up = True
    move_text = context.text[text_range.start:context.selection_range.start]
  else:
    move_up = False
    move_text = context.text[context.selection_range.start:text_range.start]

  move_lines = move_text.count("\n")
  if move_lines > 0:
    if move_up:
      actions.insert(f"{move_lines}k$")
      move_chars = move_text.find("\n") - 1
      if move_chars > 0:
        actions.insert(f"{move_chars}h")
    else:
      actions.insert(f"{move_lines}j0")
      move_chars = len(move_text) - move_text.rfind("\n") - 1
      if move_chars > 0:
        actions.insert(f"{move_chars}l")
  else:
    if move_up:
      actions.insert(f"{len(move_text)}h")
    else:
      actions.insert(f"{len(move_text)}l")


@mod.action_class
class Actions:
  """Neovim-specific actions."""

  def neovim_get_mode() -> str:
    """Returns a character indicating the current mode in Neovim."""
    # TODO: More efficient implementation if we need the mode often.
    return actions.user.scrambler_get_context().editor_mode

  def neovim_run(command: str):
    """Runs the command string from normal mode in Neovim."""
    actions.key("escape")
    actions.insert(command)


@ctx.action_class("win")
class WinActions:
  """Action overrides."""

  def filename():
    title = actions.win.title()
    parts = title.split(" - ")
    if len(parts) == 0:
      return ""
    return parts[0]


@ctx.action_class("user")
class ExtensionActions:
  """Action overrides."""

  def dictation_get_preceding_text() -> str:
    context = actions.user.scrambler_get_context()
    from_index = max(0, context.selection_range.start - mode_dictation.NUM_PRECEDING_CHARS)
    to_index = context.selection_range.start

    # Change to insert mode before proceeding to allow inserting dictated text directly.
    _insert_mode(context)

    return context.text[from_index:to_index]

  def selected_text() -> str:
    context: st.Context = actions.user.scrambler_get_context()
    return context.selection_range.extract(context.text)

  def insert_via_clipboard(text: str):
    actions.user.neovim_run("i")  # Insert mode.
    if not text:
      return
    with clip.revert():
      clip.set_text(text)
      actions.user.paste()
      # Sleep here so that clip.revert doesn't revert the clipboard too soon.
      actions.sleep("50ms")

  def copy():
    context: st.Context = actions.user.scrambler_get_context()
    clip.set_text(context.selection_range.extract(context.text))

  def jump_line(n: int):
    # Insert mode at the first non-whitespace character of the line.
    actions.user.neovim_run(f"{n}G^i")

  def position_mark():
    actions.user.neovim_run(f"m{_MARK}")

  def position_restore():
    actions.user.neovim_run(f"`{_MARK}:delmarks {_MARK}\n")  # Jump to the mark and delete it.

  def scrambler_get_context() -> st.Context:
    with clip.capture() as s:
      actions.key("ctrl-s")
    try:
      context = s.text()
    except clip.NoChange as exc:
      raise ValueError("Failed to capture Neovim context.") from exc

    # The first few lines contain information about the mode and selection.
    lines = context.split("\n")
    if len(lines) < 4:
      raise ValueError(f"Invalid Neovim context: {context}")
    mode = lines[0].strip()
    if len(mode) != 1:
      raise ValueError(f"Invalid Neovim mode: {context}")
    selection_from = int(lines[1])
    selection_to = int(lines[2])
    if (selection_from < 0 or selection_to < 0 or selection_from > selection_to):
      raise ValueError(f"Invalid Neovim selection range: {context}")

    # The rest of the lines contain the text around the cursor.
    text = "\n".join(lines[3:])

    # Disable potato mode because we have custom implementations for all actions for neovim.
    return st.Context(text=text,
                      selection_range=st.TextRange(selection_from, selection_to),
                      potato_mode=False,
                      editor_mode=mode)

  def scrambler_set_selection_action(editor_action: st.EditorAction, context: st.Context):
    if editor_action.text_range is None:
      raise ValueError("Set selection range action with missing range in neovim.")
    _move_cursor_to_start_of_range(editor_action.text_range, context)
    # Use visual mode for non-empty selection.
    if editor_action.text_range.length() > 0:
      actions.insert(f"v{editor_action.text_range.length() - 1}l")
    else:
      _insert_mode(context)

    # Update context with new selection range to allow subsequent actions to work correctly.
    context.selection_range = editor_action.text_range

  def scrambler_delete_range_action(editor_action: st.EditorAction, context: st.Context):
    if editor_action.text_range is None:
      raise ValueError("Delete range action with missing range.")
    _move_cursor_to_start_of_range(editor_action.text_range, context)
    if editor_action.text_range.length() > 0:
      actions.insert(f"{editor_action.text_range.length()}x")
    _insert_mode(context)

  def scrambler_clear_action(editor_action: st.EditorAction, context: st.Context):
    # We can delete from normal mode or visual mode.
    if context.editor_mode == "i":
      actions.key("escape")
    actions.insert("x")
    _insert_mode(context)

  def scrambler_insert_text_action(editor_action: st.EditorAction, context: st.Context):
    _insert_mode(context)
    actions.user.insert_via_clipboard(editor_action.text)

  def select_line_range_including_line_break(from_index: int, to_index: int = 0):
    if to_index > 0:
      to_index = number_util.copy_leading_decimal_digits(from_index, to_index)
    actions.user.neovim_run(f"{from_index}G0v")  # End in visual mode.
    lines_down = 0 if to_index < from_index else to_index - from_index
    if lines_down > 0:
      actions.insert(f"{lines_down}j")
    actions.insert("$h")

  def select_line_range_for_editing(from_index: int, to_index: int = 0):
    if to_index > 0:
      to_index = number_util.copy_leading_decimal_digits(from_index, to_index)
    actions.user.neovim_run(f"{from_index}G0v")  # End in visual mode.
    lines_down = 0 if to_index <= from_index else to_index - from_index
    if lines_down > 0:
      actions.insert(f"{lines_down}j$")
    else:
      actions.insert("$h")

  def line_numbers_bring_line_range(from_index: int, to_index: int = 0):
    if to_index > 0:
      to_index = number_util.copy_leading_decimal_digits(from_index, to_index)
    actions.user.position_mark()

    # Select the text to bring in visual mode.
    actions.user.neovim_run(f"{from_index}G0v")  # End in visual mode.
    lines_down = 0 if to_index <= from_index else to_index - from_index
    if lines_down > 0:
      actions.insert(f"{lines_down}j")
    actions.insert("$h")

    # Get the text.
    lines = actions.user.selected_text()

    # Go back to original position and insert the line.
    actions.user.position_restore()
    actions.user.insert_via_clipboard(lines)

  def line_numbers_insert_line_above_no_move(n: int):
    actions.user.position_mark()
    actions.user.neovim_run("O")
    actions.user.position_restore()

  def line_numbers_insert_line_below_no_move(n: int):
    actions.user.position_mark()
    actions.user.neovim_run("o")
    actions.user.position_restore()

  def split_open_down():
    actions.key("ctrl--")

  def split_open_right():
    actions.key("ctrl-\\")

  def split_close():
    actions.key("ctrl-x")

  def split_maximize():
    actions.key("ctrl-z")

  def split_last():
    actions.key("ctrl-p")

  def split_switch_up():
    actions.key("ctrl-k")

  def split_switch_down():
    actions.key("ctrl-j")

  def split_switch_left():
    actions.key("ctrl-h")

  def split_switch_right():
    actions.key("ctrl-l")

  def splits_line_numbers_bring_line_range(from_index: int, to_index: int = 0):
    if to_index > 0:
      to_index = number_util.copy_leading_decimal_digits(from_index, to_index)
    actions.user.position_mark()
    actions.user.split_last()

    # Select the text to bring in visual mode.
    actions.user.neovim_run(f"{from_index}G0v")  # End in visual mode.
    lines_down = 0 if to_index <= from_index else to_index - from_index
    if lines_down > 0:
      actions.insert(f"{lines_down}j")
    actions.insert("$h")

    # Get the text.
    lines = actions.user.selected_text()
    actions.key("escape")  # Exit visual mode.

    # Go back to original position and insert the line.
    actions.user.split_last()
    actions.user.position_restore()
    actions.user.insert_via_clipboard(lines)
