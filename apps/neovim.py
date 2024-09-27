"""Talon code for Neovim support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, clip
from ..core.lib import number_util, scrambler_types as st
from ..core import mode_dictation
from ..core.edit import get_selected_text_fragments

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
_REGISTER = "0"  # Register to use for temporary storage.


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


def _extend_selection(commands: str):
  """Extend the current selection using the given commands."""
  # Enter visual mode if not already in it.
  context: st.Context = actions.user.scrambler_get_context()
  if context.editor_mode != "v":
    actions.insert("v")
  actions.insert(commands)


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
    actions.sleep("100ms")
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

  def insert_replacing_selected(text: str):
    context: st.Context = actions.user.scrambler_get_context()
    if context.editor_mode == "v":
      actions.insert("xi")
    elif context.editor_mode == "n":
      actions.insert("i")
    actions.insert(text)

  def copy():
    context: st.Context = actions.user.scrambler_get_context()
    text = context.selection_range.extract(context.text)
    if text:
      clip.set_text(text)

  def cut():
    context: st.Context = actions.user.scrambler_get_context()
    text = context.selection_range.extract(context.text)
    if text:
      clip.set_text(text)
      # Text was selected, so we should be in visual mode.
      actions.insert("xi")

  def delete():
    context: st.Context = actions.user.scrambler_get_context()
    if context.editor_mode == "i":
      actions.key("escape")
    actions.insert("xi")

  def delete_all():
    """Deletes all text in the active editor."""
    actions.user.select_all()
    actions.user.delete()

  def delete_line():
    actions.user.select_line_including_line_break()
    actions.user.delete()

  def delete_word():
    actions.user.select_word()
    actions.user.delete()

  def delete_to_line_end():
    actions.user.extend_line_end()
    actions.user.delete()

  def delete_to_line_start():
    actions.user.extend_line_start()
    actions.user.delete()

  def delete_to_file_start():
    actions.user.extend_file_start()
    actions.user.delete()

  def delete_to_file_end():
    actions.user.extend_file_end()
    actions.user.delete()

  def delete_word_left(n: int = 1):
    for _ in range(n):
      actions.user.extend_word_left()
      actions.user.delete()

  def delete_word_right(n: int = 1):
    for _ in range(n):
      actions.user.extend_word_right()
      actions.user.delete()

  def line_start():
    actions.user.neovim_run("0i")

  def line_end():
    actions.user.neovim_run("$i")

  def file_end():
    actions.user.neovim_run("Gi")

  def file_start():
    actions.user.neovim_run("ggi")

  def extend_up():
    _extend_selection("k")

  def extend_down():
    _extend_selection("j")

  def extend_left():
    _extend_selection("h")

  def extend_right():
    _extend_selection("l")

  def extend_file_end():
    _extend_selection("G")

  def extend_file_start():
    _extend_selection("gg")

  def extend_line_end():
    _extend_selection("$")

  def extend_line_start():
    _extend_selection("0")

  def extend_page_down():
    _extend_selection("")
    actions.key("ctrl-d")

  def extend_page_up():
    _extend_selection("")
    actions.key("ctrl-u")

  def extend_word_left():
    _extend_selection("b")

  def extend_word_right():
    _extend_selection("w")

  def select_all():
    actions.user.neovim_run("gg0vG$")

  def select_line_excluding_line_break():
    actions.user.neovim_run("^v$h")

  def select_line_including_line_break():
    actions.user.neovim_run("0v$")

  def select_multiple_lines_including_line_break(n: int):
    if n <= 1:
      actions.user.neovim_run("0v$")
    else:
      actions.user.neovim_run(f"0v{n - 1}j$")

  def select_word():
    actions.user.neovim_run("viw")

  def find():
    actions.user.neovim_run("/")

  def find_next():
    actions.user.neovim_run("ni")

  def find_previous():
    actions.user.neovim_run("Ni")

  def indent_less():
    actions.user.neovim_run("<<i")

  def indent_more():
    actions.user.neovim_run(">>i")

  def line_insert_up():
    actions.user.neovim_run("O")

  def line_insert_down():
    actions.user.neovim_run("o")

  def line_swap_up():
    actions.user.neovim_run(f"\"{_REGISTER}yyddk\"{_REGISTER}P")

  def line_swap_down():
    actions.user.neovim_run(f"\"{_REGISTER}yydd\"{_REGISTER}p")

  def undo():
    actions.user.neovim_run("ui")

  def redo():
    actions.user.neovim_run("")
    actions.key("ctrl-r")
    actions.insert("i")

  def save():
    actions.user.neovim_run(":w<CR>i")

  def save_all():
    actions.user.neovim_run(":wa<CR>i")

  def duplicate_line():
    actions.user.neovim_run(f"\"{_REGISTER}yy\"{_REGISTER}pi")

  def join_lines():
    actions.user.neovim_run("J")

  def expand_selection_to_adjacent_characters():
    context: st.Context = actions.user.scrambler_get_context()
    if context.editor_mode != "v":
      actions.user.neovim_run("hvll")
    else:
      # TODO: This will shrink the selection if the cursor is at the beinning of the selection.
      actions.insert("ohol")

  def shrink_selection_by_first_and_last_characters():
    context: st.Context = actions.user.scrambler_get_context()
    if context.editor_mode != "v":
      raise ValueError("No text selected")

    # TODO: This will expand the selection if the cursor is at the beinning of the selection.
    actions.insert("oloh")

  def delete_first_and_last_characters_maintain_selection():
    """Deletes the first and last characters of the selected text. Maintains the selection."""
    selected_text = actions.user.selected_text()
    if not selected_text:
      return

    # Just delete the selection if it is small.
    if len(selected_text) <= 2:
      actions.insert("xi")
      return

    replace_text = selected_text[1:-1]
    actions.user.insert_replacing_selected(replace_text)

    # Reselect the text.
    # TODO: This won't work with multi-line selections.
    actions.user.neovim_run(f"{len(replace_text)}hv{len(replace_text)}l")

  def find_everywhere():
    # TODO: Ripgrep-style search.
    actions.user.neovim_run(" sf")

  def fragment_cursor_after(n: int):
    _, fragments = get_selected_text_fragments()
    if n <= 0 or n > len(fragments):
      raise ValueError(f"Invalid fragment index: {n}")
    fragment = fragments[n - 1]
    # TODO: This will not work if the cursor is at the start of the selection.
    actions.insert("o")
    actions.key("escape")
    if fragment[1] > 0:
      actions.insert(f"{fragment[1]}l")
    actions.insert("i")

  def fragment_cursor_before(n: int):
    _, fragments = get_selected_text_fragments()
    if n <= 0 or n > len(fragments):
      raise ValueError(f"Invalid fragment index: {n}")
    fragment = fragments[n - 1]
    # TODO: This will not work if the cursor is at the start of the selection.
    actions.insert("o")
    actions.key("escape")
    if fragment[0] > 0:
      actions.insert(f"{fragment[0]}l")
    actions.insert("i")

  def fragment_delete(from_index: int, to_index: int = 0):
    if from_index == 0:
      raise ValueError(f"Invalid fragment index: {from_index}")
    _, fragments = get_selected_text_fragments()
    if from_index > len(fragments):
      raise ValueError(f"Invalid fragment index: {from_index}")

    # Negative index deletes the last fragment.
    if from_index < 0:
      from_index = len(fragments)  # pylint: disable=self-cls-assignment

    from_fragment = fragments[from_index - 1]
    if 0 < to_index <= len(fragments):
      to_fragment = fragments[to_index - 1]
    else:
      to_fragment = from_fragment

    # Check if we need to delete a separator character before or after the fragment.
    delete_before = from_index > 1 and fragments[from_index - 2][1] < from_fragment[0]
    # Using int(n) below to suppress pylint error.
    delete_after = not delete_before and from_index < len(fragments) and to_fragment[1] < fragments[
        int(from_index)][0]

    start_index = from_fragment[0] - (1 if delete_before else 0)
    length = to_fragment[1] - from_fragment[0] + (1 if delete_before or delete_after else 0)

    # TODO: This will not work if the cursor is at the start of the selection.
    actions.insert("o")
    actions.key("escape")
    if start_index > 0:
      actions.insert(f"{start_index}l")
    if length > 0:
      actions.insert(f"{length}x")
    actions.insert("i")

  def fragment_select(from_index: int, to_index: int = 0):
    _, fragments = get_selected_text_fragments()
    from_index_effective = int(from_index)
    if from_index_effective < 0:
      from_index_effective = len(fragments)
    if from_index_effective <= 0 or from_index_effective > len(fragments):
      raise ValueError(f"Invalid fragment index: {from_index}")
    from_fragment = fragments[from_index_effective - 1]
    if to_index > 0 and to_index <= len(fragments):
      to_fragment = fragments[to_index - 1]
    else:
      to_fragment = from_fragment

    # TODO: This will not work if the cursor is at the start of the selection.
    actions.insert("o")
    actions.key("escape")
    if from_fragment[0] > 0:
      actions.insert(f"{from_fragment[0]}l")
    length = to_fragment[1] - from_fragment[0] - 1
    if length > 0:
      actions.insert(f"v{length}l")

  def fragment_select_head(n: int):
    _, fragments = get_selected_text_fragments()
    if n <= 0 or n > len(fragments):
      raise ValueError(f"Invalid fragment index: {n}")
    fragment = fragments[n - 1]
    # TODO: This will not work if the cursor is at the start of the selection.
    actions.insert("o")
    actions.key("escape")
    if fragment[1] > 1:
      actions.insert(f"v{fragment[1] - 1}l")

  def fragment_select_tail(n: int):
    text, fragments = get_selected_text_fragments()
    if n <= 0 or n > len(fragments):
      raise ValueError(f"Invalid fragment index: {n}")
    fragment = fragments[n - 1]

    actions.insert("o")
    actions.key("escape")
    if fragment[0] > 0:
      actions.insert(f"{fragment[0]}l")
    length = len(text) - fragment[0] - 1
    if length > 0:
      actions.insert(f"v{length}l")

  def fragment_select_next():
    # TODO: This will not work if the cursor is at the start of the selection.
    if actions.user.selected_text():
      actions.user.neovim_run("l")
    actions.user.extend_word_right()
    actions.user.fragment_select(1)

  def fragment_select_previous():
    # TODO: This will not work if the cursor is at the start of the selection.
    selected = actions.user.selected_text()
    if selected:
      actions.user.neovim_run(f"{len(selected)}h")
    actions.user.extend_word_left()
    actions.insert("o")  # Move cursor to the end of the selection.
    actions.user.fragment_select(-1)

  def jump_line(n: int):
    # Insert mode at the first non-whitespace character of the line.
    actions.user.neovim_run(f"{n}G^i")

  def position_mark():
    actions.user.neovim_run(f"m{_MARK}i")  # End in insert mode.

  def position_restore():
    # Jump to the mark and delete it, then end in insert mode.
    actions.user.neovim_run(f"`{_MARK}:delmarks {_MARK}\ni")

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
    actions.user.neovim_run(f"{n}GO")
    actions.user.position_restore()

  def line_numbers_insert_line_below_no_move(n: int):
    actions.user.position_mark()
    actions.user.neovim_run(f"{n}Go")
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
