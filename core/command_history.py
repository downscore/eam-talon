"""Talon code for managing command history."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import imgui, Module, speech_system

mod = Module()

# Characters to display per line in the history GUI.
_GUI_CHARS_PER_LINE = 80

# We keep command_history_size lines of history, but by default display only command_history_display of them.
_COMMAND_HISTORY_SIZE = 50
_COMMAND_HISTORY_DISPLAY = 10

_show_more_history = False
_command_history = []


def _parse_phrase(word_list):
  return " ".join(word.split("\\")[0] for word in word_list)


def _on_phrase(j):
  """Event handler called for every phrase."""
  global _command_history

  try:
    val = _parse_phrase(getattr(j["parsed"], "_unmapped", j["phrase"]))
  except KeyError:
    val = _parse_phrase(j["phrase"])

  if val == "":
    return

  # Add the new command to history and delete oldest commands if necessary.
  _command_history.append(val)
  _command_history = _command_history[-_COMMAND_HISTORY_SIZE:]


@imgui.open(y=0)
def gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  """Creates a gui displaying command history."""
  gui.text("Command History")
  gui.line()
  text = (_command_history[:] if _show_more_history else _command_history[-_COMMAND_HISTORY_DISPLAY:])
  for line in text:
    display_line = line[:_GUI_CHARS_PER_LINE]
    if len(line) > _GUI_CHARS_PER_LINE:
      display_line += "..."
    gui.text(display_line)


speech_system.register("phrase", _on_phrase)


@mod.action_class
class Actions:
  """Command history actions."""

  def history_toggle():
    """Toggles viewing the history"""
    if gui.showing:
      gui.hide()
    else:
      gui.show()

  def history_clear():
    """Clear the history"""
    global _command_history
    _command_history = []

  def history_more():
    """Show more history"""
    global _show_more_history
    _show_more_history = True

  def history_less():
    """Show less history"""
    global _show_more_history
    _show_more_history = False
