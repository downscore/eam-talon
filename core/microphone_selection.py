"""Talon code for managing the active microphone."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, actions, app, imgui
from talon.lib import cubeb

mod = Module()
cubeb_ctx = cubeb.Context()

_microphone_device_list = []

# By convention, None and System Default are listed first to match the Talon context menu.
def _update_microphone_list():
  global _microphone_device_list
  _microphone_device_list = ["None", "System Default"]

  # On Windows, it's necessary to check the state, or we will get every microphone that was ever connected.
  devices = [dev.name for dev in cubeb_ctx.inputs() if dev.state == cubeb.DeviceState.ENABLED]

  devices.sort()
  _microphone_device_list += devices


@imgui.open()
def gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  gui.text("Select a Microphone")
  gui.line()
  for index, item in enumerate(_microphone_device_list, 1):
    if gui.button(f"{index}. {item}"):
      actions.user.microphone_select(index)


@mod.action_class
class Actions:
  """Microphone selection actions."""

  def microphone_selection_toggle():
    """Toggles showing microphone selection gui."""
    if gui.showing:
      gui.hide()
    else:
      _update_microphone_list()
      gui.show()

  def microphone_select(index: int):
    """Selects a microphone by index."""
    if 1 <= index <= len(_microphone_device_list):
      actions.speech.set_microphone(_microphone_device_list[index - 1])
      app.notify(f"Activating microphone: {_microphone_device_list[index - 1]}")
      gui.hide()


def _on_devices_changed(device_type):
  del device_type
  _update_microphone_list()


def _on_ready():
  cubeb_ctx.register("devices_changed", _on_devices_changed)
  _update_microphone_list()


app.register("ready", _on_ready)
