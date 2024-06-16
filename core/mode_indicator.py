"""Mode indicator rendering for Talon."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from enum import Enum
from talon import Context, Module, app, registry, scope, ui
from talon.canvas import Canvas
from talon.screen import Screen
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia.imagefilter import ImageFilter

mod = Module()
ctx = Context()


# Enumeration of possible modes.
class SpeechMode(Enum):
  UNKNOWN = 0
  SLEEP = 1
  DICTATION = 2
  MIXED = 3
  COMMAND = 4


# Colors by mode.
_COLOR_BY_MODE = {
    SpeechMode.SLEEP: "404040",
    SpeechMode.DICTATION: "ff00ff",
    SpeechMode.MIXED: "4454ff",
    SpeechMode.COMMAND: "00c303",
    SpeechMode.UNKNOWN: "ff0000",
}

_SCREEN_X_MIDPOINT_OFFSET_PIXELS = -100
_SCREEN_Y_OFFSET_PIXELS = 12
_RADIUS_PIXELS = 6
_ALPHA_FRACTION = 0.75

_current_mode: SpeechMode = SpeechMode.UNKNOWN
_canvas: Canvas = None


def _get_color():
  mode_color = _COLOR_BY_MODE[_current_mode]
  alpha = f"{int(_ALPHA_FRACTION * 255):02x}"
  return f"{mode_color}{alpha}"


def _on_draw(canvas: SkiaCanvas):
  rect = canvas.rect
  x = rect.left + 0.5 * rect.width + _SCREEN_X_MIDPOINT_OFFSET_PIXELS - _RADIUS_PIXELS
  y = rect.top + _SCREEN_Y_OFFSET_PIXELS + _RADIUS_PIXELS
  mode_color = _get_color()
  canvas.paint.imagefilter = ImageFilter.drop_shadow(1, 1, 1, 1, "000000")
  canvas.paint.style = canvas.paint.Style.FILL
  canvas.paint.color = mode_color
  canvas.draw_circle(x, y, _RADIUS_PIXELS)


def _disable_indicator():
  global _canvas
  if _canvas:
    _canvas.unregister("draw", _on_draw)
    _canvas.close()
    _canvas = None


def _enable_indicator():
  global _canvas
  # Create canvas over full screen if it doesnt exist.
  if not _canvas:
    screen: Screen = ui.main_screen()
    _canvas = Canvas.from_rect(screen.rect)
    _canvas.register("draw", _on_draw)


def _update_indicator():
  # Update the canvas.
  if _canvas:
    _canvas.freeze()


def _on_mode_change(_):
  global _current_mode
  modes = scope.get("mode")
  if "sleep" in modes:
    new_mode = SpeechMode.SLEEP
  elif "dictation" in modes:
    if "command" in modes:
      new_mode = SpeechMode.MIXED
    else:
      new_mode = SpeechMode.DICTATION
  elif "command" in modes:
    new_mode = SpeechMode.COMMAND
  else:
    # Default to sleep mode.
    new_mode = SpeechMode.SLEEP

  if _current_mode != new_mode:
    _current_mode = new_mode
    _update_indicator()


def _on_screen_change(_):
  # Reload canvas if it is enabled.
  if _canvas:
    _disable_indicator()
    _enable_indicator()
    _update_indicator()


def _on_ready():
  registry._modes.register("mode_change", _on_mode_change)  # pylint: disable=protected-access
  ui.register("screen_change", _on_screen_change)
  _on_mode_change({})


@mod.action_class
class Actions:
  """Mode indicator actions."""

  def mode_indicator_toggle():
    """Toggles the mode indicator."""
    if _canvas:
      _disable_indicator()
    else:
      _enable_indicator()


app.register("ready", _on_ready)
