"""Utils for simulating text editor actions."""

from .scrambler_types import Context, EditorAction, EditorActionType, TextRange


def simulate_actions(context: Context, actions: list[EditorAction]) -> str:
  """Simulates a set of input commands on an editor context. Updates the given context to reflect
  the result of the actions and returns the clipboard contents."""
  clipboard = ""

  # Verify selection is inside text.
  if context.selection_range.end > len(context.text):
    raise ValueError("Selection range outside of text")

  # Apply actions to the given context.
  for action in actions:
    if action.action_type == EditorActionType.SET_SELECTION_RANGE:
      if action.text_range is None:
        raise ValueError("Set selection range action has no text range")
      context.selection_range = action.text_range
      if action.text_range.length() > 0:
        context.editor_mode = "v"
      else:
        context.editor_mode = "i"
    elif action.action_type == EditorActionType.INSERT_TEXT:
      context.text = context.text[0:context.selection_range.
                                  start] + action.text + context.text[context.selection_range.end:]
      context.selection_range = TextRange(context.selection_range.start + len(action.text),
                                          context.selection_range.start + len(action.text))
      context.editor_mode = "i"
    elif action.action_type in (EditorActionType.SET_CLIPBOARD_WITH_HISTORY,
                                EditorActionType.SET_CLIPBOARD_NO_HISTORY):
      clipboard = action.text
    elif action.action_type == EditorActionType.DELETE_RANGE:
      if action.text_range is None:
        raise ValueError("Delete range action has no text range")
      context.text = context.text[0:action.text_range.start] + context.text[action.text_range.end:]
      context.selection_range = TextRange(action.text_range.start, action.text_range.start)
      context.editor_mode = "i"

    # Verify selection is still inside text after action.
    if context.selection_range.end > len(context.text):
      raise ValueError("Selection range outside of text")

  return clipboard
