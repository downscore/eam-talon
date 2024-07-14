"""Talon code for optical character recognition commands."""

# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from typing import Any, Tuple
from talon import Context, Module, actions, screen, ui
from talon.experimental import ocr
from .lib import ocr_util, textflow, textflow_types as tf

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


def _run_command(command: tf.Command, expand_to_ocr_results: bool = False):
  """Runs the given command and returns the selection range."""
  # Run OCR and turn the result into a context we can use.
  ocr_results = _ocr_active_screen()
  context = ocr_util.create_ocr_textflow_context(ocr_results, actions.mouse_x(), actions.mouse_y())
  utility_functions = tf.UtilityFunctions(actions.user.get_all_homophones,
                                          actions.user.get_next_homophone)

  # Uncomment the following line to disable trying to infer a cursor position from the current mouse
  # coords.
  # context.mouse_index = 0

  # Run the command.
  editor_actions = textflow.run_command(
      command,
      context.text,
      tf.TextRange(context.mouse_index, context.mouse_index),
      utility_functions,
  )

  # Only execute selection range actions.
  for action in editor_actions:
    if action.action_type != tf.EditorActionType.SET_SELECTION_RANGE:
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


@mod.action_class
class Actions:
  """OCR actions."""

  def ocr_select_by_word(target_from: tf.CompoundTarget,
                         modifier_string: str = "",
                         delimiter: str = ""):
    """Selects a modified range on screen with the given word."""
    modifier_type = actions.user.textflow_modifier_type_from_string(modifier_string)
    if modifier_type != tf.ModifierType.NONE:
      target_from.modifier = tf.Modifier(modifier_type, delimiter=delimiter)
    command = tf.Command(tf.CommandType.SELECT, target_from)
    _run_command(command)

  def ocr_select_by_word_range(
      target_from: tf.CompoundTarget,
      target_to: tf.CompoundTarget,
      combo_type: tf.TargetCombinationType,
      modifier_string: str = "",
      delimiter: str = "",
  ):
    """Selects a modified range on screen with the given words."""
    # Combine the two "compound" targets into an actual compound target. Requires taking
    # `target_to.target_from`, as the second word was passed as a compound target.
    compound_target = tf.CompoundTarget(target_from.target_from, target_to.target_from, combo_type)
    modifier_type = actions.user.textflow_modifier_type_from_string(modifier_string)
    if modifier_type != tf.ModifierType.NONE:
      compound_target.modifier = tf.Modifier(modifier_type, delimiter=delimiter)
    command = tf.Command(tf.CommandType.SELECT, compound_target)
    _run_command(command)

  def ocr_select_full_result_by_word(target_from: tf.CompoundTarget):
    """Selects an OCRed line on screen with the given word."""
    command = tf.Command(tf.CommandType.SELECT, target_from)
    _run_command(command, expand_to_ocr_results=True)

  def ocr_select_full_result_by_word_range(
      target_from: tf.CompoundTarget,
      target_to: tf.CompoundTarget,
      combo_type: tf.TargetCombinationType,
  ):
    """Selects OCRed lines on screen with the given words."""
    # Combine the two "compound" targets into an actual compound target. Requires taking
    # `target_to.target_from`, as the second word was passed as a compound target.
    compound_target = tf.CompoundTarget(target_from.target_from, target_to.target_from, combo_type)
    command = tf.Command(tf.CommandType.SELECT, compound_target)
    _run_command(command, expand_to_ocr_results=True)
