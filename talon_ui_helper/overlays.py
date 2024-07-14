"""UI Helper overlays."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import abc
import numpy as np
import threading
from typing import Optional

from talon import Module, ui, canvas, screen, cron

from talon.skia import image, rrect, paint
from talon.types import Rect as TalonRect
from talon.experimental import locate

from .ui_widgets import layout_text, render_text
from .marker_ui import MarkerUi
from .blob_detector import calculate_blob_rects

mod = Module()


def find_active_window_rect() -> TalonRect:
  return ui.active_window().rect


def screencap_to_image(rect: TalonRect) -> image.Image:
  """Captures the given rectangle off the screen."""

  return screen.capture(rect.x, rect.y, rect.width, rect.height, retina=False)


class ScreenshotOverlay(abc.ABC):
  """Abstract base class for overlay windows operating on a static screenshot."""

  def __init__(self, result_handler, text=None, screen_idx=None):
    self.result_handler = result_handler

    if screen_idx is not None:
      rect = ui.screens()[screen_idx].rect
    else:
      active_window = ui.active_window()
      if active_window.id == -1:
        rect = ui.main_screen().rect
      else:
        rect = active_window.screen.rect
    self.can = canvas.Canvas.from_rect(rect)
    # Redundantly include these offset so threads can access them (self.can gets locked during draw
    # handler).
    self.offsetx = int(self.can.rect.x)
    self.offsety = int(self.can.rect.y)
    self.image = screencap_to_image(rect)
    self.text = text
    self.text_position = "bottom"
    self.text_rect = None
    self.flash_text = None

    self.can.register("draw", self._draw)
    self.can.blocks_mouse = True
    self.can.register("mouse", self._mouse_event)
    self.can.register("key", self._key_event)
    self.can.register("focus", self._focus_event)
    self.can.focused = True
    self.can.freeze()

  def destroy(self):
    self.can.close()

  def _get_keyboard_commands(self):
    return [
        ("escape", "Close overlay"),
        ("enter", "Confirm selection and close overlay"),
    ]

  def _calculate_result(self):
    raise NotImplementedError

  def _draw(self, canvas_instance):
    canvas_instance.draw_image(self.image, canvas_instance.rect.x, canvas_instance.rect.y)
    canvas_instance.paint = paint.Paint()
    canvas_instance.paint.color = "000000aa"
    canvas_instance.draw_rect(canvas_instance.rect)

    self._draw_widgets(canvas_instance)

    self._draw_text(canvas_instance)

    self._draw_flash(canvas_instance)

  def _draw_widgets(self, canvas_instance):
    pass

  def _draw_text(self, canvas_instance):
    all_text = self.text or ""
    all_text += "\n\nKeyboard shortcuts (or use equivalent voice command):\n"
    all_text += "\n".join(
        [f" - {key}: {description}" for key, description in self._get_keyboard_commands()])

    canvas_instance.paint = paint.Paint()
    canvas_instance.paint.antialias = True
    canvas_instance.paint.color = "ffffffff"
    ((width, height), formatted_text) = layout_text(all_text, canvas_instance.paint, 600)

    xpos = canvas_instance.rect.x + (canvas_instance.width - width - 20) / 2
    ypos = 10 + canvas_instance.rect.y
    if self.text_position == "bottom":
      ypos = canvas_instance.rect.y + canvas_instance.height - height - 20 - 10
    self.text_rect = TalonRect(xpos, ypos, width + 20, height + 20)

    canvas_instance.paint.color = "000000ff"
    canvas_instance.paint.style = canvas_instance.paint.Style.FILL
    thing = rrect.RoundRect.from_rect(self.text_rect, x=10, y=10, radii=(10, 10))
    canvas_instance.draw_rrect(thing)

    render_text(canvas_instance, formatted_text, xpos + 10, ypos + 20)

  def _draw_flash(self, canvas_instance):
    if self.flash_text is None:
      return

    canvas_instance.paint = paint.Paint()
    canvas_instance.paint.antialias = True
    canvas_instance.paint.color = "ffffffff"
    ((width, height), formatted_text) = layout_text(self.flash_text, canvas_instance.paint, 300)

    xpos = canvas_instance.rect.x + (canvas_instance.width - width - 20) / 2
    ypos = canvas_instance.rect.y + (canvas_instance.height - height - 20) / 2
    text_rect = TalonRect(xpos, ypos, width + 20, height + 20)

    canvas_instance.paint.color = "660000ff"
    canvas_instance.paint.style = canvas_instance.paint.Style.FILL
    thing = rrect.RoundRect.from_rect(text_rect, x=10, y=10, radii=(10, 10))
    canvas_instance.draw_rrect(thing)

    render_text(canvas_instance, formatted_text, xpos + 10, ypos + 20)

  def _show_flash(self, text):
    self.flash_text = text

    def clear_flash():
      self.flash_text = None
      self.can.freeze()

    cron.after("2s", clear_flash)

  def _focus_event(self, focussed):
    if not focussed:
      self.destroy()
      self.result_handler(None)

  def _key_event(self, evt):
    if evt.down:
      return

    # Lowercase events are for public, upper for Rust beta
    if evt.key in ("Escape", "esc"):
      self.destroy()
      self.result_handler(None)

    if evt.key in ("Return", "return"):
      self.destroy()
      self.result_handler(self._calculate_result())

  def _mouse_event(self, evt):
    if self.text_rect:
      if self.text_rect.contains(evt.gpos.x, evt.gpos.y):
        self.text_position = "top" if self.text_position == "bottom" else "bottom"
        self.can.freeze()


class BoxSelectorOverlay(ScreenshotOverlay):
  """Show an overlay allowing the user to select a region of the screen."""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.hl_region = None
    self.is_selecting = False
    self.settled_countdown_timer = None

  def _calculate_result(self):
    return self.hl_region

  def _get_keyboard_commands(self):
    commands = super()._get_keyboard_commands()
    commands += [
        ("up/down/left/right", "Nudge selection in indicated direction"),
        ("shift + up/down/left/right", "Nudge selection a larger amount"),
        ("ctrl + up/down/left/right", "Shrink/grow selection"),
        ("shift + ctrl + up/down/left/right", "Shrink/grow selection a larger amount"),
    ]
    return commands

  def _selection_settled(self, finished_selection):
    """Called when we can assume that the user has finished selecting a region, or when they've just
    started drawing a new one. If you want to draw any other markers after the user has finished
    selecting this is the place to set and unset a flag for _draw_widgets."""

  def _get_region(self):
    """Gets the selected region, normalising any negative widths."""

    if self.hl_region is None:
      return None

    if self.hl_region.width < 0:
      x = self.hl_region.x + self.hl_region.width
      width = self.hl_region.width * -1
    else:
      x = self.hl_region.x
      width = self.hl_region.width

    if self.hl_region.height < 0:
      y = self.hl_region.y + self.hl_region.height
      height = self.hl_region.height * -1
    else:
      y = self.hl_region.y
      height = self.hl_region.height

    return TalonRect(int(x), int(y), int(width), int(height))

  def _draw_widgets(self, canvas_instance):
    super()._draw_widgets(canvas_instance)

    if not self.hl_region:
      return
    canvas_instance.save()
    canvas_instance.clip_rect(self.hl_region, canvas_instance.ClipOp.INTERSECT)
    canvas_instance.draw_image(self.image, self.offsetx, self.offsety)
    canvas_instance.restore()
    canvas_instance.paint = paint.Paint()
    canvas_instance.paint.style = canvas_instance.paint.Style.STROKE
    canvas_instance.paint.color = "ffffffff"
    if self.hl_region.width == 0 or self.hl_region.height == 0:
      # Deal with the zero thickness cases that happen when using voice commands
      canvas_instance.draw_line(self.hl_region.x, self.hl_region.y,
                                self.hl_region.x + self.hl_region.width,
                                self.hl_region.y + self.hl_region.height)
    else:
      canvas_instance.draw_rect(self.hl_region)

  def _get_region_centre(self):
    if self.hl_region:
      return (self.hl_region.x + self.hl_region.width / 2,
              self.hl_region.y + self.hl_region.height / 2)
    else:
      return None

  def _get_cropped_image(self) -> Optional[image.Image]:
    if self.hl_region is None:
      return None

    # I think make_subset does this more cleanly, but I don't know what the Talon API is
    region = self._get_region()
    if region is None:
      raise ValueError("No valid region")
    xpos = region.x - self.offsetx
    ypos = region.y - self.offsety
    arr = np.array(self.image)[
        ypos:(ypos + region.height),
        xpos:(xpos + region.width),
    ]
    if len(arr) == 0:
      return None

    return image.Image.from_array(arr)

  def _mouse_event(self, evt):
    super()._mouse_event(evt)

    if evt.event == "mousedown" and evt.button == 0:
      self.hl_region = TalonRect(evt.gpos.x, evt.gpos.y, 0, 0)
      self.is_selecting = True
      self._selection_settled(False)
      self.can.freeze()
    elif evt.event == "mousemove" and self.is_selecting and self.hl_region:
      self.hl_region = TalonRect(self.hl_region.x, self.hl_region.y, evt.gpos.x - self.hl_region.x,
                                 evt.gpos.y - self.hl_region.y)
      self.can.freeze()
    elif evt.event == "mouseup" and evt.button == 0:
      self.is_selecting = False
      self._selection_settled(True)
      self.can.freeze()

  def _key_event(self, evt):
    super()._key_event(evt)

    if evt.down or self.hl_region is None:
      return

    keymap = [
        # Rust beta
        ("Left", ["x", "width", "-"]),
        ("Right", ["x", "width", "+"]),
        ("Up", ["y", "height", "-"]),
        ("Down", ["y", "height", "+"]),

        # Public Talon
        ("left", ["x", "width", "-"]),
        ("right", ["x", "width", "+"]),
        ("up", ["y", "height", "-"]),
        ("down", ["y", "height", "+"]),
    ]

    for key, args in keymap:
      if key != evt.key:
        continue

      position, scale, direction = args
      magnitude = 25 if "shift" in evt.mods else 1
      magnitude = -1 * magnitude if direction == "-" else magnitude

      if "ctrl" in evt.mods:
        curr = getattr(self.hl_region, scale)
        new_val = curr + magnitude
        new_val = new_val if new_val >= 0 else 1
        setattr(self.hl_region, scale, new_val)
      else:
        curr = getattr(self.hl_region, position)
        new_val = curr + magnitude
        new_val = new_val if new_val >= 0 else 0
        setattr(self.hl_region, position, new_val)

      # Ensure the region is still within the bounds of the canvas
      for (position, scale) in (("x", "width"), ("y", "height")):
        min_pos = getattr(self.can.rect, position)
        max_pos = min_pos + getattr(self.can.rect, scale)
        curr_extent = getattr(self.hl_region, position) + getattr(self.hl_region, scale)

        if getattr(self.hl_region, position) < min_pos:
          setattr(self.hl_region, position, min_pos)
        if getattr(self.hl_region, position) > max_pos:
          setattr(self.hl_region, position, max_pos - 1)

        if curr_extent > max_pos:
          setattr(self.hl_region, scale, max_pos - getattr(self.hl_region, position))

      # Start the selection settled countdown timer
      self._selection_settled(False)
      self._reset_settled_countdown("2s")

      self.can.freeze()

  def _reset_settled_countdown(self, countdown):

    def _inner():
      self._selection_settled(True)
      self.settled_countdown_timer = None

    if self.settled_countdown_timer:
      cron.cancel(self.settled_countdown_timer)
    self.settled_countdown_timer = cron.after(countdown, _inner)


class ImageSelectorOverlay(BoxSelectorOverlay):
  """Allows the user to select a region on the screen to use as an image for the locator API."""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.offset_coord = None
    self.result_rects = []

  def _calculate_result(self):
    if self.hl_region:
      if self.offset_coord is not None:
        cx, cy = self._get_region_centre()
        offset = (self.offset_coord.x - cx, self.offset_coord.y - cy)
      else:
        offset = None

      index = 0
      for i, rect in enumerate(self.result_rects):
        if rect == self._get_region():
          index = i

      return {"image": self._get_cropped_image(), "offset": offset, "index": index}
    else:
      return None

  def _selection_settled(self, finished_selection):
    if not finished_selection:
      self.result_rects = []
      return

    th = threading.Thread(target=self._find_matches, daemon=True)
    th.start()
    th.join(timeout=1)
    timed_out = th.is_alive()

    if timed_out or len(self.result_rects) > 20:
      self._show_flash("Too many matches, not showing any of them")
      self.result_rects = []

    self.can.freeze()

  def _draw_widgets(self, canvas_instance):
    super()._draw_widgets(canvas_instance)
    if not self.hl_region:
      return

    # Draw other matching regions
    if len(self.result_rects) > 0:
      self._draw_matches(canvas_instance)

    # Draw the offset marker
    canvas_instance.paint = paint.Paint()
    canvas_instance.paint.style = canvas_instance.paint.Style.FILL
    canvas_instance.paint.color = "ff00ffff"
    canvas_instance.paint.stroke_width = 1
    if self.offset_coord is None:
      args = [
          self.hl_region.x + self.hl_region.width / 2, self.hl_region.y + self.hl_region.height / 2
      ]
    else:
      args = [self.offset_coord.x, self.offset_coord.y]
      canvas_instance.paint.antialias = True
      canvas_instance.draw_line(*self._get_region_centre(), *args)

    canvas_instance.draw_circle(*args, 2)

  def _find_matches(self):
    cropped_img = self._get_cropped_image()
    if cropped_img is None:
      self.result_rects = []
      return

    self.result_rects = locate.locate_in_image(self.image, cropped_img, threshold=0.999)
    self.result_rects = [
        TalonRect(rect.x + self.offsetx, rect.y + self.offsety, rect.width, rect.height)
        for rect in self.result_rects
    ]

  def _draw_matches(self, canvas_instance):
    canvas_instance.paint = paint.Paint()
    canvas_instance.paint.color = "ff0000aa"
    canvas_instance.paint.style = canvas_instance.paint.Style.STROKE
    canvas_instance.paint.stroke_width = 1
    for rect in self.result_rects:
      if rect == self._get_region():
        continue
      canvas_instance.save()
      canvas_instance.clip_rect(rect, canvas_instance.ClipOp.INTERSECT)
      canvas_instance.draw_image(self.image, self.offsetx, self.offsety)
      canvas_instance.restore()
      canvas_instance.draw_rect(rect)

  def _mouse_event(self, evt):
    super()._mouse_event(evt)

    if evt.event == "mousedown" and evt.button == 0:
      # Reset the coord when a new box is started
      self.offset_coord = None

    if evt.event == "mouseup" and evt.button == 1:
      self.offset_coord = evt.gpos
      self.can.freeze()


class BlobBoxOverlay(BoxSelectorOverlay):
  """And overlay that helps the user build a blob box by displaying the matched blobs live as they
  define boxes."""

  def _selection_settled(self, finished_selection):
    if not finished_selection:
      self.markers = []
      return

    maybe_image = self._get_cropped_image()
    if maybe_image is None:
      return

    img = np.array(maybe_image)
    region = self._get_region()
    rects = calculate_blob_rects(img, region)

    self.markers = [
        MarkerUi.Marker(rect, label)
        for rect, label in zip(rects, "abcdefghijklmnopqrstuvwxyz0123456789" * 3)
    ]
    self.can.freeze()

  def _draw_widgets(self, canvas_instance):
    super()._draw_widgets(canvas_instance)

    if not self.hl_region:
      return

    if self.markers:
      MarkerUi.draw_markers(canvas_instance, self.markers)
