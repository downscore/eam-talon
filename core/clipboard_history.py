"""Talon code for managing clipboard history."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import imgui, Module, actions, clip

mod = Module()

# Characters to display per line in the history GUI.
_GUI_CHARS_PER_LINE = 60

# We keep clipboard_history_size lines of history, but by default display only clipboard_history_display of them.
_CLIPBOARD_HISTORY_SIZE = 50
_CLIPBOARD_HISTORY_DISPLAY = 10

_show_more_history = False
_clipboard_history = []


def _add_to_history(text: str):
  """Add some text to clipboard history."""
  global _clipboard_history
  if not text:
    return
  # De-dupe with last text only.
  if len(_clipboard_history) > 0 and text == _clipboard_history[-1]:
    return
  _clipboard_history.append(text)
  _clipboard_history = _clipboard_history[-_CLIPBOARD_HISTORY_SIZE:]


@imgui.open(y=0)
def gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  """Creates a gui displaying clipboard history."""
  gui.text("Clipboard History")
  gui.line()
  text = (_clipboard_history[:] if _show_more_history else _clipboard_history[-_CLIPBOARD_HISTORY_DISPLAY:])
  for i, line in enumerate(text):
    # History entries are indexed by added time descending. Indexes are 1-based.
    entry_index = len(text) - i
    display_line = f"{entry_index}. {line[:_GUI_CHARS_PER_LINE]}"
    if len(line) > _GUI_CHARS_PER_LINE:
      display_line += "..."
    gui.text(display_line)


@mod.action_class
class Actions:
  """Clipboard history actions."""

  def clipboard_history_toggle():
    """Toggles viewing clipboard history."""
    if gui.showing:
      gui.hide()
    else:
      gui.show()

  def clipboard_history_clear():
    """Clear the clipboard history."""
    global _clipboard_history
    _clipboard_history = []

  def clipboard_history_more():
    """Show more clipboard history."""
    global _show_more_history
    _show_more_history = True

  def clipboard_history_less():
    """Show less clipboard history."""
    global _show_more_history
    _show_more_history = False

  def clipboard_history_cut():
    """Cut and record text to history."""
    actions.user.cut()
    actions.sleep("50ms")
    _add_to_history(clip.text())

  def clipboard_history_copy():
    """Copy and record text to history."""
    actions.user.copy()
    actions.sleep("50ms")
    _add_to_history(clip.text())

  def clipboard_history_paste(index: int):
    """Copy and record text to history."""
    # Index should be 1-based starting from most recently added item.
    if index < 1 or index > len(_clipboard_history):
      return
    list_index = len(_clipboard_history) - index
    actions.user.insert_via_clipboard(_clipboard_history[list_index])

  def clipboard_history_set_text(text: str):
    """Set clipboard text and record history."""
    _add_to_history(text)
    actions.clip.set_text(text)
