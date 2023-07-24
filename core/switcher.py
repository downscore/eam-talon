"""Talon code for switching between apps."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import subprocess
import talon
from talon import Context, Module, app, imgui, ui, actions
import os
import time
from .lib import format_util
from .user_settings import load_dict_from_csv

mod = Module()
ctx = Context()

# Load app name overrides from file and monitor for updates.
_OVERRIDES = load_dict_from_csv("app_name_overrides.csv")

# Initialize empty lists. They will be populated on ready, and when apps are opened or closed.
mod.list("running_app_name", desc="All running applications")
ctx.lists["user.running_app_name"] = {}
mod.list("launch_app_name", desc="All launchable applications")
ctx.lists["user.launch_app_name"] = {}

_MAC_APPLICATION_DIRECTORIES = [
    "/Applications",
    "/Applications/Utilities",
    "/System/Applications",
    "/System/Applications/Utilities",
]


def _update_running_list():
  running = {}
  for curr_app in ui.apps(background=False):
    name = curr_app.name
    running[name.lower()] = name

  for spoken in _OVERRIDES:
    app_name = _OVERRIDES[spoken]
    key = app_name.lower()
    if key in running:
      del running[key]
      running[spoken] = app_name

  ctx.lists["self.running_app_name"] = running


def _update_launch_list():
  launch = {}
  for base in _MAC_APPLICATION_DIRECTORIES:
    if not os.path.isdir(base):
      raise ValueError(f"Invalid directory: {base}")
    for name in os.listdir(base):
      path = os.path.join(base, name)
      if name.startswith(".") or not name.endswith(".app"):
        continue
      # Remove everything after the last dot in the filename.
      name = name.rsplit(".", 1)[0]
      # Unformat the name (split on case changes, etc.).
      name = format_util.unformat_phrase(name)
      name = name.lower()
      # Remove all characters except the alphabet and spaces.
      filtered = ""
      for c in name:
        if not c.isalpha() and c != " ":
          continue
        filtered += c
      filtered = filtered.strip()
      # TODO: Replace numbers with spoken forms.
      # TODO: Apply overrides.
      # TODO: Gui list of launchable applications.
      # TODO: Util function for normalizing names.
      launch[filtered] = path
  ctx.lists["self.launch_app_name"] = launch


@imgui.open()
def running_gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  gui.text("Names of running applications")
  gui.line()
  for line in ctx.lists["self.running_app_name"]:
    gui.text(line)


@imgui.open()
def launch_gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  gui.text("Names of launchable applications")
  gui.line()
  for line in ctx.lists["self.launch_app_name"]:
    gui.text(line)


@mod.capture(rule="{self.running_app_name}")
def running_applications(m) -> str:
  """Returns a single application name."""
  return m.running_app_name


@mod.capture(rule="{self.launch_app_name}")
def launch_applications(m) -> str:
  """Returns a single application name."""
  return m.launch


@mod.action_class
class Actions:
  """Actions related to launching and switching between apps."""

  def get_running_app(name: str) -> ui.App:
    """Gets the first available running app with `name`."""
    for running_app in ui.apps():
      if running_app.name == name and not running_app.background:
        return running_app
    raise ValueError(f'App not running: "{name}"')

  def switcher_focus(name: str):
    """Focuses an application by name."""
    running_app = actions.user.get_running_app(name)
    running_app.focus()

    # Hacky solution to do this reliably on Mac.
    timeout_secs = 1
    sleep_secs = 0.1
    start_time_secs = time.monotonic()
    if talon.app.platform == "mac":
      while ui.active_app() != running_app and time.monotonic() - start_time_secs < timeout_secs:
        time.sleep(sleep_secs)

  def switcher_focus_google_meet():
    """Focus browser window with Google Meet open."""
    for window in ui.windows():
      if window.app.name not in ("Google Chrome", "Safari") or not window.title.startswith("Meet - "):
        continue
      window.focus()
      return
    # If we didn't find the window, bail out so we don't send subsequent commands to the wrong window.
    raise ValueError("Could not find Google Meet window")

  def switcher_launch(path: str):
    """Launches a new application by path."""
    ui.launch(path=path)

  def switcher_toggle_running():
    """Shows/hides all running applications."""
    if running_gui.showing:
      running_gui.hide()
    else:
      running_gui.show()

  def switcher_hide_running():
    """Hides list of running applications."""
    running_gui.hide()

  def switcher_toggle_launch():
    """Shows/hides all launch applications."""
    if launch_gui.showing:
      launch_gui.hide()
    else:
      launch_gui.show()

  def switcher_hide_launch():
    """Hides list of launch applications."""
    launch_gui.hide()

  def switcher_test():
    """Runs test script."""
    subprocess.Popen(["/opt/homebrew/bin/python3", "/Users/eamdoherty/Documents/Code/PythonTools/llm.py"], shell=False)


def _on_app_change(event: str):
  del event
  _update_running_list()


def _on_ready():
  _update_launch_list()
  _update_running_list()
  ui.register("app_launch", _on_app_change)
  ui.register("app_close", _on_app_change)


app.register("ready", _on_ready)
