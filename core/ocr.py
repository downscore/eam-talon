"""Talon code for optical character recognition commands."""

# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from typing import Any, Optional, Tuple
from talon import Context, Module, actions, screen, ui
from talon.experimental import ocr
from .lib import ocr_util, scrambler_run, scrambler_types as st
from ..core.scrambler import ScramblerMatch

mod = Module()
ctx = Context()


def _mouse_select_text(start: Tuple[float, float], end: Tuple[float, float], button: int = 0):
  """Selects text between the given screen coordinates."""
  actions.mouse_move(start[0], start[1])
  actions.mouse_drag(button)
  actions.sleep("50ms")
  actions.mouse_move(end[0], end[1])
  actions.sleep("50ms")
  actions.mouse_release(button)


def _ocr_active_screen() -> list[Any]:
  """Runs OCR over the active screen or main screen."""
  active_window = ui.active_window()
  if active_window.id == -1:
    rect = ui.main_screen().rect
  else:
    rect = active_window.screen.rect
  screencap = screen.capture(rect.x, rect.y, rect.width, rect.height, retina=False)
  return ocr.ocr(screencap)


def _run_command(command: st.Command, expand_to_ocr_results: bool = False):
  """Runs the given command and returns the selection range."""
  # Run OCR and turn the result into a context we can use.
  ocr_results = _ocr_active_screen()
  context = ocr_util.create_ocr_scrambler_context(ocr_results, actions.mouse_x(), actions.mouse_y())
  utility_functions = st.UtilityFunctions(actions.user.get_all_homophones,
                                          actions.user.get_next_homophone)

  # Uncomment the following line to disable trying to infer a cursor position from the current mouse
  # coords.
  # context.mouse_index = 0

  # Run the command.
  editor_actions = scrambler_run.run_command(
      command,
      context.text,
      st.TextRange(context.mouse_index, context.mouse_index),
      utility_functions,
  )

  # Only execute selection range actions.
  for action in editor_actions:
    if action.action_type != st.EditorActionType.SET_SELECTION_RANGE:
      continue
    if action.text_range is None:
      raise ValueError("Set selection range action with missing range.")

    from_index = action.text_range.start
    to_index = action.text_range.end
    if expand_to_ocr_results:
      from_index, to_index = context.expand_range_to_ocr_results(from_index, to_index)

    from_coords = context.index_to_screen_coordinates(from_index)
    to_coords = context.index_to_screen_coordinates(to_index)
    _mouse_select_text(from_coords, to_coords)

    # Sleep to let the UI catch up.
    actions.sleep("50ms")


def _modifier_type_from_string(modifier_type: str) -> Optional[st.ModifierType]:
  """Converts a string to a modifier type. "SCOPE" is a special modifier that gets the appropriate
  modifier for the current context."""
  if modifier_type == "":
    return None
  if modifier_type == "SCOPE":
    return actions.user.scrambler_get_scope_modifier()
  else:
    return st.ModifierType[modifier_type]


@mod.action_class
class Actions:
  """OCR actions."""

  def ocr_select_by_word(match: ScramblerMatch, modifier_string: str = "", delimiter: str = ""):
    """Selects a modified range on screen with the given word."""
    modifier_type = _modifier_type_from_string(modifier_string)
    if modifier_type is not None:
      match.modifiers.append(st.Modifier(modifier_type, delimiter=delimiter))
    command = st.Command(st.CommandType.SELECT, match.modifiers, match.extend_modifiers,
                         match.combination_type)
    _run_command(command)

  def ocr_select_full_result_by_word(match: ScramblerMatch):
    """Selects an OCRed line on screen with the given word."""
    command = st.Command(st.CommandType.SELECT, match.modifiers, match.extend_modifiers,
                         match.combination_type)
    _run_command(command, expand_to_ocr_results=True)
