"""Code for writing the current speech system status to a temp file."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from pathlib import Path
from tempfile import gettempdir
from talon import Module, app, clip, imgui, registry, scope, speech_system, ui

mod = Module()

# Contents of the last written status file.
_last_status: str = ""


def _get_status_file_path() -> Path:
  """Returns the path to the status file."""
  return Path(gettempdir()) / "talon-status"


def _get_current_status() -> str:
  """Get a string containing the current speech system status."""
  result = []
  for mode in scope.get("mode"):
    result.append(f"mode {mode}")
  for application in scope.get("app.app"):
    result.append(f"app {application}")
  for tag in registry.tags:
    result.append(f"tag {tag}")
  result.append("end")
  return "\n".join(result)


def _maybe_update_status_file():
  """Writes the status file if anything has changed since the last write."""
  global _last_status
  current_status = _get_current_status()
  if current_status == _last_status:
    return

  # Open file for writing text, replacing existing file if present.
  file_path = _get_status_file_path()
  with file_path.open("w") as out_file:
    out_file.write(current_status)

  _last_status = current_status


@imgui.open(y=0)
def status_gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  """Creates a gui displaying current status."""
  gui.text(str(_get_status_file_path()))
  gui.line()
  lines = _get_current_status().splitlines()
  for line in lines:
    gui.text(line)


@mod.action_class
class Actions:
  """Speech system status actions."""

  def status_file_ui_toggle():
    """Toggles showing the status file UI."""
    if status_gui.showing:
      status_gui.hide()
    else:
      status_gui.show()

  def status_file_copy_path():
    """Copy the path of the status file to the clipboard."""
    clip.set_text(str(_get_status_file_path()))

  def status_file_update():
    """Check the system status and update the new status file if necessary."""
    _maybe_update_status_file()


app.register("ready", _maybe_update_status_file)
speech_system.register("post:phrase", lambda _: _maybe_update_status_file())
ui.register("app_launch", lambda _: _maybe_update_status_file())
ui.register("app_close", lambda _: _maybe_update_status_file())
# Note: win_focus appears to not fire when closing an app.
ui.register("win_focus", lambda _: _maybe_update_status_file())
ui.register("win_title", lambda _: _maybe_update_status_file())
