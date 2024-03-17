"""Talon module and context for window-snapping actions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import ui, Module, Context, actions

mod = Module()
ctx = Context()

# TODO: Map keyboard shortcuts for snapping windows.


class RelativeScreenPos(object):
  """Represents a window position as a fraction of the screen."""

  def __init__(self, left, top, right, bottom):
    self.left = left
    self.top = top
    self.bottom = bottom
    self.right = right


_SNAP_POSITIONS = {
    # Halves
    # .---.---.     .-------.
    # |   |   |  &  |-------|
    # '---'---'     '-------'
    "left": RelativeScreenPos(0, 0, 0.5, 1),
    "right": RelativeScreenPos(0.5, 0, 1, 1),
    "top": RelativeScreenPos(0, 0, 1, 0.5),
    "bottom": RelativeScreenPos(0, 0.5, 1, 1),
    # Thirds
    # .--.--.--.
    # |  |  |  |
    # '--'--'--'
    "center third": RelativeScreenPos(1 / 3, 0, 2 / 3, 1),
    "left third": RelativeScreenPos(0, 0, 1 / 3, 1),
    "right third": RelativeScreenPos(2 / 3, 0, 1, 1),
    "left two thirds": RelativeScreenPos(0, 0, 2 / 3, 1),
    "right two thirds": RelativeScreenPos(
        1 / 3,
        0,
        1,
        1,
    ),
    # Quarters
    # .---.---.
    # |---|---|
    # '---'---'
    "top left": RelativeScreenPos(0, 0, 0.5, 0.5),
    "top right": RelativeScreenPos(0.5, 0, 1, 0.5),
    "bottom left": RelativeScreenPos(0, 0.5, 0.5, 1),
    "bottom right": RelativeScreenPos(0.5, 0.5, 1, 1),
    # Sixths
    # .--.--.--.
    # |--|--|--|
    # '--'--'--'
    "top left third": RelativeScreenPos(0, 0, 1 / 3, 0.5),
    "top right third": RelativeScreenPos(2 / 3, 0, 1, 0.5),
    "top left two thirds": RelativeScreenPos(0, 0, 2 / 3, 0.5),
    "top right two thirds": RelativeScreenPos(1 / 3, 0, 1, 0.5),
    "top center third": RelativeScreenPos(1 / 3, 0, 2 / 3, 0.5),
    "bottom left third": RelativeScreenPos(0, 0.5, 1 / 3, 1),
    "bottom right third": RelativeScreenPos(2 / 3, 0.5, 1, 1),
    "bottom left two thirds": RelativeScreenPos(0, 0.5, 2 / 3, 1),
    "bottom right two thirds": RelativeScreenPos(1 / 3, 0.5, 1, 1),
    "bottom center third": RelativeScreenPos(1 / 3, 0.5, 2 / 3, 1),
    # Special
    "center": RelativeScreenPos(1 / 8, 1 / 6, 7 / 8, 5 / 6),
    "full": RelativeScreenPos(0, 0, 1, 1),
    "fullscreen": RelativeScreenPos(0, 0, 1, 1),
}
mod.list("window_snap_positions", "Predefined window positions for the current window.")
ctx.lists["user.window_snap_positions"] = _SNAP_POSITIONS.keys()


def _set_window_pos(window: ui.Window, x: float, y: float, width: float, height: float):
  """Helper to set the window position."""
  window.rect = ui.Rect(round(x), round(y), round(width), round(height))


def _bring_forward(window: ui.Window):
  current_window = ui.active_window()
  # TODO: Figure out when this might throw an exception.
  window.focus()
  current_window.focus()


def _get_app_window(app_name: str) -> ui.Window:
  return actions.self.get_running_app(app_name).active_window


def _move_window_to_screen(window: ui.Window, screen: ui.Screen):
  """Move the given window to the given screen."""
  source_screen = window.screen
  if source_screen == screen:
    return

  # Retain the same proportions on the new screen.
  source_rect = source_screen.visible_rect
  dest_rect = screen.visible_rect

  proportional_width: float = dest_rect.width / source_rect.width
  proportional_height: float = dest_rect.height / source_rect.height
  _set_window_pos(
      window,
      x=dest_rect.left + (window.rect.left - source_rect.left) * proportional_width,
      y=dest_rect.top + (window.rect.top - source_rect.top) * proportional_height,
      width=window.rect.width * proportional_width,
      height=window.rect.height * proportional_height,
  )


def _move_window_to_next_screen(window: ui.Window):
  """Move window to the next screen from its current screen."""
  _move_window_to_screen(window, actions.user.screens_get_next(window.screen))


def _move_window_to_previous_screen(window: ui.Window):
  """Move window to the previous screen from its current screen."""
  _move_window_to_screen(window, actions.user.screens_get_previous(window.screen))


def _move_window_to_screen_number(window: ui.Window, screen_number: int):
  """Move window to the screen with the given number."""
  _move_window_to_screen(window, actions.user.screens_get_by_number(screen_number))


def _snap_window_helper(window: ui.Window, pos: RelativeScreenPos):
  screen = window.screen.visible_rect

  _set_window_pos(
      window,
      x=screen.x + (screen.width * pos.left),
      y=screen.y + (screen.height * pos.top),
      width=screen.width * (pos.right - pos.left),
      height=screen.height * (pos.bottom - pos.top),
  )


@mod.capture(rule="{user.window_snap_positions}")
def window_snap_position(m) -> RelativeScreenPos:
  return _SNAP_POSITIONS[m.window_snap_positions]


@mod.action_class
class Actions:
  """Actions for window management windows."""

  def window_close():
    """Close the active window."""
    actions.key("cmd-w")

  def window_next():
    """Focus the next window."""
    actions.key("cmd-`")

  def window_open():
    """Open a new window."""
    actions.key("cmd-n")

  def window_previous():
    """Focus the previous window."""
    actions.key("cmd-shift-`")

  def snap_window(pos: RelativeScreenPos) -> None:
    """Move the active window to a specific position on-screen."""
    _snap_window_helper(ui.active_window(), pos)

  def move_window_next_screen() -> None:
    """Move the active window to the next screen."""
    _move_window_to_next_screen(ui.active_window())

  def move_window_previous_screen() -> None:
    """Move the active window to the previous screen."""
    _move_window_to_previous_screen(ui.active_window())

  def move_window_to_screen(screen_number: int) -> None:
    """Move the active window to the screen with the given number."""
    _move_window_to_screen_number(ui.active_window(), screen_number)

  def snap_app(app_name: str, pos: RelativeScreenPos):
    """Snap a specific application to another screen."""
    window = _get_app_window(app_name)
    _bring_forward(window)
    _snap_window_helper(window, pos)

  def move_app_to_screen(app_name: str, screen_number: int):
    """Move a specific application to another screen."""
    window = _get_app_window(app_name)
    _bring_forward(window)
    _move_window_to_screen_number(window, screen_number)
