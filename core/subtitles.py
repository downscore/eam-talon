"""Custom subtitles for Talon."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from typing import Optional
from talon import Module, actions, cron, speech_system, ui
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.types import Rect

mod = Module()

# Subtitle configuration.
_MAX_TEXT_LENGTH = 60
_TIMEOUT_MS = 1500
_TEXT_SIZE_PIXELS = 20
_TEXT_TYPEFACE = "MesloLGS NF"
_TEXT_COLOR = "ffffff"
_TEXT_STROKE_COLOR = "000033"
_TEXT_STROKE_WIDTH_PIXELS = 10
_SCREEN_X_OFFSET_PIXELS = -30
_SCREEN_Y_OFFSET_PIXELS = 15

# Subtitles need to be shown for wake commands even if speech is disabled.
# TODO: Get this from the actual commands, do not duplicate them here.
_WAKE_COMMANDS = ["papaya", "speech wake"]

# Canvas used to display the subtitle.
_subtitle_canvas: Optional[SkiaCanvas] = None


def _display_subtitle(input_text: str):
  """Shows the given text as a subtitle on the screen."""
  global _subtitle_canvas

  # Truncate text if necessary.
  text = input_text
  if len(text) > _MAX_TEXT_LENGTH:
    text = text[:_MAX_TEXT_LENGTH] + "…"

  # Clear existing subtitle if necessary.
  if _subtitle_canvas:
    _subtitle_canvas.close()
    _subtitle_canvas = None

  # Create new canvas using the main screen.
  screen = ui.main_screen()
  _subtitle_canvas = Canvas.from_screen(screen)
  assert _subtitle_canvas

  # Draw text on canvas.
  _subtitle_canvas.register("draw", lambda canvas: _on_canvas_draw(canvas, text))
  _subtitle_canvas.freeze()

  # Register a callback to close the canvas after a timeout.
  cron.after(f"{_TIMEOUT_MS}ms", _subtitle_canvas.close)


def _on_canvas_draw(canvas: SkiaCanvas, text: str):
  # Set font and get a rect representing the size of the rendered text.
  canvas.paint.typeface = _TEXT_TYPEFACE
  canvas.paint.textsize = _TEXT_SIZE_PIXELS
  text_rect: Rect = canvas.paint.measure_text(text)[1]

  # Place the text in the top right corner of the main screen.
  x = canvas.rect.x + canvas.rect.width - text_rect.width + _SCREEN_X_OFFSET_PIXELS
  y = canvas.rect.y + canvas.paint.textsize / 2 + _SCREEN_Y_OFFSET_PIXELS

  # Draw outline of the text.
  canvas.paint.style = canvas.paint.Style.STROKE
  canvas.paint.color = _TEXT_STROKE_COLOR
  canvas.paint.stroke_width = _TEXT_STROKE_WIDTH_PIXELS

  # Draw the text over the outline.
  canvas.draw_text(text, x, y)
  canvas.paint.style = canvas.paint.Style.FILL
  canvas.paint.color = _TEXT_COLOR
  canvas.draw_text(text, x, y)


def _on_pre_phrase(phrase):
  words = phrase.get("phrase")
  if not words:
    return
  text = " ".join(words)

  # Show subtitle if speech is enabled or the command is a wake command (speech is about to be enabled).
  if words and (actions.speech.enabled() or text in _WAKE_COMMANDS):
    text = " ".join(words)
    _display_subtitle(text)


speech_system.register("pre:phrase", _on_pre_phrase)
