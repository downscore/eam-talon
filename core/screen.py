"""Talon code for managing multiple screens."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, ui, cron
from talon.canvas import Canvas  # type: ignore

mod = Module()


def _get_sorted_screens():
  """Return screens sorted by their topmost then leftmost edges. Screens will be sorted
  left-to-right, with ties broken by top-to-bottom ordering."""
  return sorted(
      sorted(ui.screens(), key=lambda screen: screen.visible_rect.top),
      key=lambda screen: screen.visible_rect.left,
  )


def _get_screen_by_offset(screen: ui.Screen, offset: int) -> ui.Screen:
  screens = _get_sorted_screens()
  index = (screens.index(screen) + offset) % len(screens)
  return screens[index]


def _show_screen_number(screen: ui.Screen, number: int):
  """Draw numbers on each screen using a canvas."""

  def on_draw(c):
    c.paint.typeface = "arial"
    # Take min of width and height so this works on both landscape and portrait screens.
    c.paint.textsize = round(min(c.width, c.height) / 2)
    text = f"{number}"
    rect = c.paint.measure_text(text)[1]
    x = c.x + c.width / 2 - rect.x - rect.width / 2
    y = c.y + c.height / 2 + rect.height / 2

    c.paint.style = c.paint.Style.FILL
    c.paint.color = "eeeeee"
    c.draw_text(text, x, y)

    c.paint.style = c.paint.Style.STROKE
    c.paint.color = "000000"
    c.draw_text(text, x, y)

    cron.after("3s", canvas.close)

  canvas = Canvas.from_rect(screen.rect)
  canvas.register("draw", on_draw)
  canvas.freeze()


@mod.action_class
class Actions:
  """Actions related to screen management."""

  def screens_show_numbering():
    """Show the screen number on each screen."""
    screens = _get_sorted_screens()
    number = 1
    for screen in screens:
      _show_screen_number(screen, number)
      number += 1

  def screens_get_by_number(screen_number: int) -> ui.Screen:
    """Get a screen by number."""
    screens = _get_sorted_screens()
    length = len(screens)
    if screen_number < 1 or screen_number > length:
      raise ValueError(f"Non-existent screen: {screen_number} in range [1, {length}]")
    return screens[screen_number - 1]

  def screens_get_previous(screen: ui.Screen) -> ui.Screen:
    """Get the screen before the given one."""
    return _get_screen_by_offset(screen, -1)

  def screens_get_next(screen: ui.Screen) -> ui.Screen:
    """Get the screen after the given one."""
    return _get_screen_by_offset(screen, 1)
