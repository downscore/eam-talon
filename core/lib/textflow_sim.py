"""Utils for simulating textflow actions."""

from typing import Tuple
from .textflow_types import EditorAction, EditorActionType, TextRange


def simulate_actions(initial_text: str, initial_selection: TextRange,
                     actions: list[EditorAction]) -> Tuple[str, TextRange, str]:
  """Simulate a set of input commands given the starting text and selection range. Returns resulting (text, selection
  range, clipboard contents)."""
  text = initial_text
  selection = initial_selection
  clipboard = ""

  # Verify selection is inside text.
  if selection.end > len(text):
    raise ValueError("Selection range outside of text")

  # Apply actions to the given text and selection.
  for action in actions:
    if action.action_type == EditorActionType.SET_SELECTION_RANGE:
      if action.text_range is None:
        raise ValueError("Set selection range action has no text range")
      selection = action.text_range
    elif action.action_type == EditorActionType.CLEAR:
      text = text[0:selection.start] + text[selection.end:]
      selection = TextRange(selection.start, selection.start)
    elif action.action_type == EditorActionType.INSERT_TEXT:
      text = text[0:selection.start] + action.text + text[selection.end:]
      selection = TextRange(selection.start + len(action.text), selection.start + len(action.text))
    elif action.action_type in (EditorActionType.SET_CLIPBOARD_WITH_HISTORY, EditorActionType.SET_CLIPBOARD_NO_HISTORY):
      clipboard = action.text

    # Verify selection is still inside text after action.
    if selection.end > len(text):
      raise ValueError("Selection range outside of text")

  return (text, selection, clipboard)
