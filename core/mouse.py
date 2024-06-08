"""Talon code for handling the mouse."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from dataclasses import dataclass
import re
from typing import Any, Optional, Tuple, Union
from talon import Context, Module, actions, canvas, screen, ui
from talon.experimental import ocr
from talon.types import Rect
from talon.skia.typeface import Typeface
from .lib.textflow_match import get_phrase_regex
from .user_settings import append_to_csv, load_coords_from_csv

mod = Module()
ctx = Context()


@dataclass()
class MouseCoordinateDelta:
  x: int = 0
  y: int = 0


_COORDINATE_DELTAS_BY_SPOKEN: dict[str, MouseCoordinateDelta] = {
    "north": MouseCoordinateDelta(y=-100),
    "south": MouseCoordinateDelta(y=100),
    "west": MouseCoordinateDelta(x=-100),
    "east": MouseCoordinateDelta(x=100),
    "up": MouseCoordinateDelta(y=-300),
    "down": MouseCoordinateDelta(y=300),
    "left": MouseCoordinateDelta(x=-300),
    "right": MouseCoordinateDelta(x=300),
}
mod.list("mouse_direction", desc="Mouse movement directions")
ctx.lists["self.mouse_direction"] = _COORDINATE_DELTAS_BY_SPOKEN.keys()

# Available labels for matches.
_LABELS = "abcdefghijklmnopqrstuvwxyz0123456789"

_COORDS_FILENAME: str = "mouse_coords.csv"
_COORDS_BY_LABEL: dict[str, Tuple[float, float]] = load_coords_from_csv(_COORDS_FILENAME)

mod.list("mouse_label", desc="Labels for mouse coordinates")
ctx.lists["user.mouse_label"] = _COORDS_BY_LABEL.keys()

# Tag set when the mouse OCR UI is open.
mod.tag("mouse_ocr_ui_open", desc="The mouse OCR selection UI is open")

# Query regex, matches, and target rects from the last OCR search.
_regex_from_last_search: Optional[re.Pattern] = None
_target_rects_from_last_search = []
# Button we want to click when we find a search result. None if we just want to move the mouse.
_button_from_last_search: Optional[int] = None


@mod.capture(rule="{self.mouse_direction}+")
def mouse_directions(m) -> MouseCoordinateDelta:
  """Maps a set of spoken mouse directions to the sum of coordinate deltas."""
  result = MouseCoordinateDelta()
  for direction in m.mouse_direction_list:
    delta = _COORDINATE_DELTAS_BY_SPOKEN[direction]
    result.x += delta.x
    result.y += delta.y
  return result


class OcrUi:
  """An interface for selecting OCR matches."""

  def __init__(self, screen_index: Optional[int] = None):
    # If no screen index is supplied, try to use the active screen.
    if screen_index is None:
      active_window = ui.active_window()
      if active_window.id == -1:
        rect = ui.main_screen().rect
      else:
        rect = active_window.screen.rect
      self._canvas = canvas.Canvas.from_rect(rect)
    else:
      self._canvas = canvas.Canvas.from_screen(ui.screens()[screen_index])

    self._canvas.register("draw", self._draw)
    self._canvas.hide()

  def show(self):
    self._canvas.show()
    # Freeze stops draw being called at 60Hz and just uses the initial paint.
    self._canvas.freeze()

  def hide(self):
    self._canvas.hide()

  def destroy(self):
    self._canvas.close()

  def _draw(self, canvas_instance):
    self._draw_markers(canvas_instance)

  @staticmethod
  def _draw_markers(canvas_instance):
    """Draws OCR matches on the given canvas."""
    paint = canvas_instance.paint
    paint.textsize = 16
    paint.typeface = Typeface.from_name("monospace")
    min_width = 12
    min_height = 12

    # Zip matches to available labels.
    for rect, label in zip(_target_rects_from_last_search, _LABELS):
      # trect.x and .y are the offsets the text is printed at.
      _, trect = paint.measure_text(label)

      # Draw the box.
      height = max(trect.height, min_height) + 4
      width = max(trect.width, min_width) + 4
      ypos = rect.y + (rect.height - height) // 2
      bg_rect = Rect(rect.x + (rect.width - width) // 2, ypos, width, height)
      paint.style = paint.Style.FILL
      paint.color = "aaffffff"
      canvas_instance.draw_rect(bg_rect)

      # Draw the label.
      paint.color = "black"
      paint.style = paint.Style.FILL
      canvas_instance.draw_text(label, bg_rect.x - trect.x + (bg_rect.width - trect.width) / 2,
                                bg_rect.y - trect.y + (bg_rect.height - trect.height) / 2)


# UI instance for selecting OCR matches. Populated when the UI is visible.
_ocr_ui: Optional[OcrUi] = None


def _ocr_active_context() -> list[Any]:
  """Runs OCR over the active screen or main screen."""
  active_window = ui.active_window()
  if active_window.id == -1:
    rect = ui.main_screen().rect
  else:
    rect = active_window.screen.rect
  screencap = screen.capture(rect.x, rect.y, rect.width, rect.height, retina=False)
  return ocr.ocr(screencap)


def _ocr_search(s: str):
  """Perform an OCR search for the given string."""
  global _regex_from_last_search
  global _target_rects_from_last_search

  regex_str = get_phrase_regex(s.split(), actions.user.get_all_homophones)
  _regex_from_last_search = re.compile(regex_str, re.IGNORECASE)

  results = _ocr_active_context()
  _target_rects_from_last_search = []
  for result in results:
    regex_match = _regex_from_last_search.search(result.text)
    if regex_match is None:
      continue

    # Try to get a rectangle centered on the matched text (assume one line monospace font and no padding).
    fraction_start = regex_match.start() / len(result.text)
    fraction_end = regex_match.end() / len(result.text)
    width = result.rect.width * (fraction_end - fraction_start)
    rect = Rect(result.rect.x + result.rect.width * fraction_start, result.rect.y, max(width, 10), result.rect.height)

    _target_rects_from_last_search.append(rect)


def _ocr_move_mouse_to_rect(rect: Rect):
  """Moves the mouse to the center of the given rectangle."""
  actions.mouse_move(rect.x + rect.width / 2, rect.y + rect.height / 2)


@mod.action_class
class Actions:
  """Mouse actions."""

  def mouse_move_delta(delta: MouseCoordinateDelta):
    """Moves the mouse by the given delta."""
    x: float = actions.mouse_x() + delta.x
    y: float = actions.mouse_y() + delta.y
    actions.mouse_move(x, y)

  def mouse_click_label(label: str, button: int = 0):
    """Clicks the given label with the given mouse button and restores the mouse position."""
    x: float = actions.mouse_x()
    y: float = actions.mouse_y()
    actions.user.mouse_move_to_label(label)
    actions.mouse_click(button)
    actions.mouse_move(x, y)

  def mouse_drag_to_label(label: str, button: int = 0):
    """Drags the mouse from the current location to the given label."""
    actions.mouse_drag(button)
    actions.sleep("50ms")
    actions.user.mouse_move_to_label(label)
    actions.sleep("50ms")
    actions.mouse_release(button)

  def mouse_move_to_label(label: str):
    """Moves the mouse to the coordinates with the given label."""
    x, y = _COORDS_BY_LABEL[label]
    actions.mouse_move(x, y)

  def mouse_ocr_click(s: str, button: int = 0):
    """Searches for the given string. If there is one match, clicks it, otherwise displays matches."""
    global _button_from_last_search

    _ocr_search(s)
    _button_from_last_search = button

    if len(_target_rects_from_last_search) == 0:
      return
    if len(_target_rects_from_last_search) == 1:
      _ocr_move_mouse_to_rect(_target_rects_from_last_search[0])
      actions.mouse_click(button)
      return

    # Display matches for clicking.
    actions.user.mouse_ocr_ui_show()

  def mouse_ocr_move(s: str):
    """Searches for the given string. If there is one match, moves the mouse to it, otherwise displays matches."""
    global _button_from_last_search

    _ocr_search(s)
    _button_from_last_search = None

    if len(_target_rects_from_last_search) == 0:
      return
    if len(_target_rects_from_last_search) == 1:
      _ocr_move_mouse_to_rect(_target_rects_from_last_search[0])
      return

    # Display matches for moving.
    actions.user.mouse_ocr_ui_show()

  def mouse_ocr_ui_activate_label(label: Union[str, int]):
    """Activates (moves the mouse to or clicks on) the given label."""
    label = str(label)  # pylint: disable=self-cls-assignment

    # Zip labels to matches and create a dictionary.
    rects_by_label = dict(zip(_LABELS, _target_rects_from_last_search))

    # Make sure the label exists.
    if label not in rects_by_label:
      return

    # Hide the UI.
    actions.user.mouse_ocr_ui_hide()

    # Move the mouse to the match and click if required.
    _ocr_move_mouse_to_rect(rects_by_label[label])
    if _button_from_last_search is not None:
      actions.mouse_click(_button_from_last_search)

  def mouse_ocr_ui_hide():
    """Hides the OCR UI."""
    global _ocr_ui
    if _ocr_ui is not None:
      _ocr_ui.destroy()
    _ocr_ui = None
    ctx.tags = []

  def mouse_ocr_ui_show():
    """Displays the OCR UI."""
    global _ocr_ui
    if _ocr_ui is None:
      _ocr_ui = OcrUi()
    _ocr_ui.show()
    ctx.tags = ["user.mouse_ocr_ui_open"]

  def mouse_ocr_copy_nearby_line():
    """Copies the line of text nearest to the mouse."""
    ocr_results = _ocr_active_context()
    x: float = actions.mouse_x()
    y: float = actions.mouse_y()

    # Find the closest OCR result to the mouse coordinates.
    closest_result = None
    closest_distance_squared = None
    for result in ocr_results:
      distance_squared = (result.rect.x + result.rect.width / 2 - x)**2 + (result.rect.y + result.rect.height / 2 -
                                                                           y)**2
      if closest_distance_squared is None or distance_squared < closest_distance_squared:
        closest_result = result
        closest_distance_squared = distance_squared
    if closest_result is None:
      actions.app.notify("No nearby text found")
      return

    # Copy the line of text.
    actions.user.clipboard_history_set_text(closest_result.text)
    actions.app.notify(f"Copied: {closest_result.text}")

  def mouse_save_coords(label: str):
    """Saves the current mouse coordinates to file."""
    x: float = actions.mouse_x()
    y: float = actions.mouse_y()
    append_to_csv(_COORDS_FILENAME, [label, str(x), str(y)])
