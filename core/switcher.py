"""Talon code for switching between apps."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from typing import Optional
import talon
from talon import Context, Module, app, imgui, ui, actions
import os
import time
from .lib import app_util
from .user_settings import load_dict_from_csv

mod = Module()
ctx = Context()

# Max lines per page for app lists.
_MAX_LINES_PER_PAGE = 45

# Load app name overrides from file and monitor for updates.
_OVERRIDES_SPOKEN_BY_APP_NAME = load_dict_from_csv("app_name_overrides.csv")

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

# Remembered window IDs keyed by name.
_window_id_by_name: dict[str, int] = {}

# Saved window ID for restoring focus.
_saved_window_id: Optional[int] = None

# Current page for app lists.
_running_page = 0
_launch_page = 0


def _update_running_list():
  running = {}
  for curr_app in ui.apps(background=False):
    name = curr_app.name
    running[name.lower()] = name

  for app_name in _OVERRIDES_SPOKEN_BY_APP_NAME:
    spoken = _OVERRIDES_SPOKEN_BY_APP_NAME[app_name]
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
      app_launch_string = app_util.filename_to_app_launch_string(name, _OVERRIDES_SPOKEN_BY_APP_NAME)
      launch[app_launch_string] = path
  ctx.lists["self.launch_app_name"] = launch


def _focus_window_by_id(window_id: int):
  window_found = False
  for window in ui.windows():
    if window.id != window_id:
      continue
    window_found = True
    window.focus()
    return
  if not window_found:
    raise ValueError(f"Could not find window. ID: {window_id}")

  # Hack to wait for window to be focused on Macos.
  timeout_secs = 1
  sleep_secs = 0.1
  start_time_secs = time.monotonic()
  if talon.app.platform == "mac":
    while ui.active_window().id != window_id and time.monotonic() - start_time_secs < timeout_secs:
      time.sleep(sleep_secs)


def _focus_window_by_type(type_name: str, app_names: list[str]):
  """Tries to focus a window given its type name and possible app names."""
  if type_name in _window_id_by_name:
    try:
      _focus_window_by_id(_window_id_by_name[type_name])
      return
    except ValueError:
      # Could not find window. Delete the saved ID and fall back to switching to apps.
      del _window_id_by_name[type_name]

  # No saved window, or saved window could not be found. Try to switch to known applications.
  for app_name in app_names:
    try:
      actions.user.switcher_focus(app_name)
      return
    except ValueError:
      pass
  raise ValueError(f"Could not find window. Type: {type_name}")


@imgui.open()
def running_gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  gui.text("Names of running applications")
  gui.line()
  for line in ctx.lists["self.running_app_name"]:
    gui.text(line)


@imgui.open()
def launch_gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  apps = list(ctx.lists["self.launch_app_name"])
  apps.sort()

  gui.text(f"Launchable Apps ({_launch_page + 1}/{len(apps) // _MAX_LINES_PER_PAGE + 1})")
  gui.line()

  page_content = apps[_launch_page * _MAX_LINES_PER_PAGE:(_launch_page + 1) * _MAX_LINES_PER_PAGE]
  for line in page_content:
    gui.text(line)


@mod.capture(rule="{self.running_app_name}")
def running_applications(m) -> str:
  """Returns a single application name."""
  return m.running_app_name


@mod.capture(rule="{self.launch_app_name}")
def launch_applications(m) -> str:
  """Returns a single application name."""
  return m.launch_app_name


@mod.action_class
class Actions:
  """Actions related to launching and switching between apps."""

  def switcher_get_running_app(name: str) -> ui.App:
    """Gets the first available running app with `name`."""
    for running_app in ui.apps():
      if running_app.name == name and not running_app.background:
        return running_app
    raise ValueError(f'App not running: "{name}"')

  def switcher_focus(name: str):
    """Focuses an application by name."""
    running_app = actions.user.switcher_get_running_app(name)
    running_app.focus()

    # Hacky solution to do this reliably on Mac.
    timeout_secs = 1
    sleep_secs = 0.1
    start_time_secs = time.monotonic()
    if talon.app.platform == "mac":
      while ui.active_app() != running_app and time.monotonic() - start_time_secs < timeout_secs:
        time.sleep(sleep_secs)

  def switcher_focus_google_meet():
    """Focuses browser window with Google Meet open."""
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
    global _running_page
    _running_page = 0
    if running_gui.showing:
      running_gui.hide()
    else:
      running_gui.show()

  def switcher_toggle_launch():
    """Shows/hides all launch applications."""
    global _launch_page
    _launch_page = 0
    if launch_gui.showing:
      launch_gui.hide()
    else:
      launch_gui.show()

  def switcher_launch_next_page():
    """Shows the next page of launchable applications."""
    global _launch_page
    _launch_page = (_launch_page + 1) % (len(ctx.lists["self.launch_app_name"]) // _MAX_LINES_PER_PAGE + 1)

  def switcher_launch_previous_page():
    """Shows the previous page of launchable applications."""
    global _launch_page
    _launch_page = (_launch_page - 1) % (len(ctx.lists["self.launch_app_name"]) // _MAX_LINES_PER_PAGE + 1)

  def switcher_new_terminal_tab(directory: str = ""):
    """Opens a new terminal tab in the given directory. If directory is empty, open in the default directory, usually
    the current user's home."""
    actions.user.switcher_focus_terminal()
    actions.user.tab_open()
    if directory:
      actions.user.insert_via_clipboard(f"cd \"{directory.strip()}\"")
      actions.key("enter")
      actions.insert("ls")
      actions.key("enter")

  def switcher_save_current_window_by_name(name: str):
    """Saves the current window as the window with the given name."""
    _window_id_by_name[name] = ui.active_window().id

  def switcher_save_window():
    """Saves the current window so it can be restored later."""
    global _saved_window_id
    _saved_window_id = ui.active_window().id

  def switcher_restore_window():
    """Restores the last saved window to focus."""
    if _saved_window_id is None:
      raise ValueError("No window saved")
    _focus_window_by_id(_saved_window_id)

  def switcher_focus_coder():
    """Switches to the saved IDE window or try to find an app."""
    _focus_window_by_type("coder", ["Code - Insiders", "Code"])

  def switcher_focus_browser():
    """Switches to the saved browser window or try to find an app."""
    _focus_window_by_type("browser", ["Google Chrome", "Safari"])

  def switcher_focus_terminal():
    """Switches to the saved terminal window or try to find an app."""
    _focus_window_by_type("terminal", ["iTerm2", "Terminal"])


def _on_app_change(event: str):
  del event
  _update_running_list()


def _on_ready():
  _update_launch_list()
  _update_running_list()
  ui.register("app_launch", _on_app_change)
  ui.register("app_close", _on_app_change)


app.register("ready", _on_ready)
