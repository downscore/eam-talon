"""Talon code for Neovim support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, clip
from ..core.lib import textflow_types as tf
from ..core import mode_dictation
from ..core.textflow import TextFlowContext

mod = Module()
ctx = Context()

mod.apps.neovim = """
app.bundle: org.alacritty
title: / - neovim$/
"""

ctx.matches = r"""
app: neovim
"""


def _insert_mode(context: TextFlowContext):
  """Change the editor to insert mode. No-op if it is already in insert mode."""
  if context.editor_mode == "i":
    return
  if context.editor_mode != "n":
    actions.key("escape")
  actions.key("i")
  context.editor_mode = "i"


def _normal_mode(context: TextFlowContext):
  """Change the editor to normal mode. No-op if it is already in normal mode."""
  if context.editor_mode == "n":
    return
  actions.key("escape")
  context.editor_mode = "n"


def _move_cursor_to_start_of_range(text_range: tf.TextRange, context: TextFlowContext):
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
    return actions.user.textflow_get_context().editor_mode


@ctx.action_class("win")
class WinActions:
  """Action overrides."""

  def filename():
    """Gets the open filename."""
    title = actions.win.title()
    parts = title.split(" - ")
    if len(parts) == 0:
      return ""
    return parts[0]


@ctx.action_class("user")
class ExtensionActions:
  """Action overrides."""

  def dictation_get_preceding_text() -> str:
    context = actions.user.textflow_get_context()
    from_index = max(0, context.selection_range.start - mode_dictation.NUM_PRECEDING_CHARS)
    to_index = context.selection_range.start

    # Change to insert mode before proceeding to allow inserting dictated text directly.
    _insert_mode(context)

    return context.text[from_index:to_index]

  def textflow_get_context() -> TextFlowContext:
    """Gets the textflow context for the current editor, including the current mode."""
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
    return TextFlowContext(text=text,
                           selection_range=tf.TextRange(selection_from, selection_to),
                           potato_mode=False,
                           editor_mode=mode)

  def textflow_set_selection_action(editor_action: tf.EditorAction, context: TextFlowContext):
    """Sets the selection in an editor, given a textflow context."""
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

  def textflow_delete_range_action(editor_action: tf.EditorAction, context: TextFlowContext):
    """Deletes a text range in an editor, given a textflow context."""
    if editor_action.text_range is None:
      raise ValueError("Delete range action with missing range.")

    _move_cursor_to_start_of_range(editor_action.text_range, context)

    if editor_action.text_range.length() > 0:
      actions.insert(f"{editor_action.text_range.length()}x")
      # Update context to allow subsequent actions to work correctly.
      context.text = context.text[:editor_action.text_range.start] + context.text[editor_action.
                                                                                  text_range.end:]
      context.selection_range = tf.TextRange(editor_action.text_range.start,
                                             editor_action.text_range.start)
    _insert_mode(context)

  def textflow_clear_action(editor_action: tf.EditorAction, context: TextFlowContext):
    """Deletes the selected text or the character to the left of the cursor if there is no
    selection."""
    # We can delete from normal mode or visual mode.
    if context.editor_mode == "i":
      actions.key("escape")
    actions.insert("x")
    _insert_mode(context)
    # TODO: Update context to reflect the deletion. Currently, the clear action never has other
    # editor actions following it, so this isn't a problem in practice.

  def textflow_insert_text_action(editor_action: tf.EditorAction, context: TextFlowContext):
    """Inserts the given text in an editor."""
    _insert_mode(context)
    actions.user.insert_via_clipboard(editor_action.text)

  def selected_text() -> str:
    context: TextFlowContext = actions.user.textflow_get_context()
    return context.selection_range.extract(context.text)

  def jump_line(n: int):
    actions.key("escape")  # Normal mode.
    actions.insert(f"{n}G^i")  # Insert mode at the first non-whitespace character of the line.
