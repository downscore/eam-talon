"""Talon code for managing macros."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, imgui, speech_system
from .user_settings import append_to_csv, load_macros_from_csv

mod = Module()
ctx = Context()

# Characters to display per line in the macro display GUI.
_GUI_CHARS_PER_LINE = 60

_MACROS_FILENAME: str = "macros.csv"
_MACROS_BY_LABEL: dict[str, list[str]] = load_macros_from_csv(_MACROS_FILENAME)

mod.list("macro_label", desc="Labels for macros")
ctx.lists["user.macro_label"] = _MACROS_BY_LABEL.keys()

_macro: list[str] = []
_recording: bool = False


def _on_pre_phrase(d):
  if not _recording:
    return
  if "parsed" not in d:
    return
  command = d["parsed"]._unmapped  # pylint: disable=protected-access

  # Skip empty commands and macro-related commands.
  if len(command) == 0 or command[0] == "macro":
    return

  _macro.append(" ".join(command))


@imgui.open(y=0)
def gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  """Creates a gui displaying macro contents."""
  gui.text("Macro Contents")
  gui.line()
  if _recording:
    gui.text("**RECORDING**")
    gui.line()
  for i, line in enumerate(_macro):
    display_line = f"{i}. {line[:_GUI_CHARS_PER_LINE]}"
    if len(line) > _GUI_CHARS_PER_LINE:
      display_line += "..."
    gui.text(display_line)


@mod.action_class
class Actions:
  """Actions for managing macros."""

  def macro_record():
    """Records a new macro."""
    global _macro
    global _recording

    if not _recording:
      speech_system.register("pre:phrase", _on_pre_phrase)
    _macro = []
    _recording = True

  def macro_stop():
    """Stops recording."""
    global _recording
    if _recording:
      speech_system.unregister("pre:phrase", _on_pre_phrase)
    _recording = False

  def macro_play():
    """Plays the recorded macro."""
    actions.user.macro_stop()
    for entry in _macro:
      actions.mimic(entry.split(" "))

  def macro_repeat(n: int):
    """Plays the recorded macro n times."""
    for _ in range(n):
      actions.user.macro_play()

  def macro_display_toggle():
    """Toggles viewing macro contents."""
    if gui.showing:
      gui.hide()
    else:
      gui.show()

  def macro_delete_entry(index: int):
    """Deletes an entry from the recorded macro."""
    if index < 0 or index >= len(_macro):
      return
    _macro.pop(index)

  def macro_save(label: str):
    """Saves the current macro to file."""
    rows = [label]
    rows.extend(_macro)
    append_to_csv(_MACROS_FILENAME, rows)

  def macro_load_label(label: str):
    """Loads the macro with the given label."""
    global _macro
    _macro = _MACROS_BY_LABEL[label]
