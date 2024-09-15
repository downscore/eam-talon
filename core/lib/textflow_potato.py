"""Support for TextFlow's potato mode, where only simple input commands are available for accessing
and modifying text. Potato mode is used in editors where accessibility APIs do not work."""

from dataclasses import dataclass
from enum import Enum, unique
from .textflow_types import EditorAction, EditorActionType, TextRange
from .textflow_sim import simulate_actions


@unique
class PotatoEditorActionType(Enum):
  """Simple text input action types for an editor in potato mode."""
  # Clears the selected text. No-op if no text is selected.
  CLEAR = 2
  # Inserts text at the current cursor position. Overwrites selected text, if any.
  INSERT_TEXT = 3
  # Sets the clipboard contents to the given text and adds it to clipboard history.
  SET_CLIPBOARD_WITH_HISTORY = 4
  # Sets the clipboard contents to the given text, but does not add to the clipboard history.
  SET_CLIPBOARD_NO_HISTORY = 5
  # Navigation.
  GO_UP = 6
  GO_DOWN = 7
  GO_LEFT = 8
  GO_RIGHT = 9
  GO_WORD_LEFT = 10
  GO_WORD_RIGHT = 11
  GO_LINE_START = 12
  GO_LINE_END = 13
  # Selection.
  EXTEND_UP = 14
  EXTEND_DOWN = 15
  EXTEND_LEFT = 16
  EXTEND_RIGHT = 17
  EXTEND_WORD_LEFT = 18
  EXTEND_WORD_RIGHT = 19
  EXTEND_LINE_START = 20
  EXTEND_LINE_END = 21


@dataclass
class PotatoEditorAction:
  """A simple text editing action for an editor in potato mode. Used as output from TextFlow."""
  action_type: PotatoEditorActionType
  # Text to insert, copy to the clipboard, etc.
  text: str = ""
  # Number of times to repeat the action.
  repeat: int = 1


def _move_before_text(text: str) -> list[PotatoEditorAction]:
  """Generate actions to move before the given text."""
  # TODO: Smarter navigation (by word, by line if word wrap disabled, etc.). Navigation by word is
  # difficult because it works differently in different editors (e.g. handling of line ends and
  # punctuation characters).
  return [PotatoEditorAction(PotatoEditorActionType.GO_LEFT, repeat=len(text))]


def _move_after_text(text: str) -> list[PotatoEditorAction]:
  """Generate actions to move before the given text."""
  # TODO: Smarter navigation (by word, by line if word wrap disabled, etc.). Navigation by word is
  # difficult because it works differently in different editors (e.g. handling of line ends and
  # punctuation characters).
  return [PotatoEditorAction(PotatoEditorActionType.GO_RIGHT, repeat=len(text))]


def _select_text(text: str) -> list[PotatoEditorAction]:
  """Generate actions to select the given text."""
  # TODO: Smarter navigation (by word, by line if word wrap disabled, etc.). Navigation by word is
  # difficult because it works differently in different editors (e.g. handling of line ends and
  # punctuation characters).
  return [PotatoEditorAction(PotatoEditorActionType.EXTEND_RIGHT, repeat=len(text))]


def _convert_set_selection_range(set_selection: TextRange, curr_text: str,
                                 curr_selection: TextRange) -> list[PotatoEditorAction]:
  """Converts selection range command to potato mode."""
  result: list[PotatoEditorAction] = []

  # No action necessary if we have already selected the desired range. Note: We must match the exact
  # selection. We can't extend an existing selection because we don't know whether the cursor is at
  # the beginning or end of the selection.
  if set_selection == curr_selection:
    return result

  # Collapse selection if necessary.
  cursor_pos = curr_selection.start
  if curr_selection.start != curr_selection.end:
    if set_selection.start >= curr_selection.end:
      result.append(PotatoEditorAction(PotatoEditorActionType.GO_RIGHT))
      cursor_pos = curr_selection.end
    else:
      result.append(PotatoEditorAction(PotatoEditorActionType.GO_LEFT))

  # Move to start of selection.
  if set_selection.start < cursor_pos:
    result.extend(_move_before_text(curr_text[set_selection.start:cursor_pos]))
  elif set_selection.start > cursor_pos:
    result.extend(_move_after_text(curr_text[cursor_pos:set_selection.start]))

  # Select until end.
  if set_selection.end > set_selection.start:
    result.extend(_select_text(curr_text[set_selection.start:set_selection.end]))

  return result


def _convert_delete_range(delete_range: TextRange, curr_text: str,
                          curr_selection: TextRange) -> list[PotatoEditorAction]:
  """Converts delete range command to potato mode."""
  result: list[PotatoEditorAction] = []

  # Collapse selection if necessary.
  cursor_pos = curr_selection.start
  if curr_selection.start != curr_selection.end:
    if delete_range.start >= curr_selection.end:
      result.append(PotatoEditorAction(PotatoEditorActionType.GO_RIGHT))
      cursor_pos = curr_selection.end
    else:
      result.append(PotatoEditorAction(PotatoEditorActionType.GO_LEFT))

  # Move to end of range.
  if delete_range.end < cursor_pos:
    result.extend(_move_before_text(curr_text[delete_range.end:cursor_pos]))
  elif delete_range.end > cursor_pos:
    result.extend(_move_after_text(curr_text[cursor_pos:delete_range.end]))

  # Select until end.
  if delete_range.end > delete_range.start:
    # TODO: Smarter deletion (by word, by line if word wrap disabled, etc.). Deletion by word is
    # difficult because it works differently in different editors (e.g. handling of line ends and
    # punctuation characters).
    result.append(PotatoEditorAction(PotatoEditorActionType.CLEAR, repeat=delete_range.length()))

  return result


def convert_actions_to_potato_mode(actions: list[EditorAction], text: str,
                                   selection_range: TextRange) -> list[PotatoEditorAction]:
  """Converts editor actions to the equivalent potato mode actions."""
  curr_text = text
  curr_selection = selection_range
  result: list[PotatoEditorAction] = []
  for action in actions:
    if action.action_type == EditorActionType.CLEAR:
      result.append(PotatoEditorAction(PotatoEditorActionType.CLEAR))
    elif action.action_type == EditorActionType.INSERT_TEXT:
      result.append(PotatoEditorAction(PotatoEditorActionType.INSERT_TEXT, action.text))
    elif action.action_type == EditorActionType.SET_CLIPBOARD_NO_HISTORY:
      result.append(PotatoEditorAction(PotatoEditorActionType.SET_CLIPBOARD_NO_HISTORY,
                                       action.text))
    elif action.action_type == EditorActionType.SET_CLIPBOARD_WITH_HISTORY:
      result.append(
          PotatoEditorAction(PotatoEditorActionType.SET_CLIPBOARD_WITH_HISTORY, action.text))
    elif action.action_type == EditorActionType.SET_SELECTION_RANGE:
      if action.text_range is None:
        raise ValueError("Set selection range action has no range")
      result.extend(_convert_set_selection_range(action.text_range, curr_text, curr_selection))
    elif action.action_type == EditorActionType.DELETE_RANGE:
      if action.text_range is None:
        raise ValueError("Delete range action has no range")
      result.extend(_convert_delete_range(action.text_range, curr_text, curr_selection))
    else:
      raise ValueError(f"Unrecognized editor action type: {action.action_type}")

    # Update current state to simulate the action.
    curr_text, curr_selection, _ = simulate_actions(curr_text, curr_selection, [action])
  return result
