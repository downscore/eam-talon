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
from .lib import browser_util, format_util
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

# Remembered window IDs keyed by name.
_window_id_by_name: dict[str, int] = {}

# Saved window ID for restoring focus.
_saved_window_id: Optional[int] = None


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


def _is_chrome_running() -> bool:
  """Returns whether Chrome is running with open windows."""
  for running_app in ui.apps():
    if running_app.name == "Google Chrome" and not running_app.background:
      return True
  return False


def _is_chrome_focused() -> bool:
  """Returns whether Chrome is focused."""
  return ui.active_app().name == "Google Chrome"


def _is_safari_running() -> bool:
  """Returns whether Safari is running with open windows."""
  for running_app in ui.apps():
    if running_app.name == "Safari" and not running_app.background:
      return True
  return False


def _is_safari_focused() -> bool:
  """Returns whether Safari is focused."""
  return ui.active_app().name == "Safari"


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
    if "coder" in _window_id_by_name:
      try:
        _focus_window_by_id(_window_id_by_name["coder"])
        return
      except ValueError:
        # Could not find window. Delete the saved ID and fall back to switching apps.
        del _window_id_by_name["coder"]

    # No saved window, or saved window could not be found. Try to switch to known IDEs.
    try:
      actions.user.switcher_focus("Code - Insiders")
      return
    except ValueError:
      pass
    try:
      actions.user.switcher_focus("Code")
      return
    except ValueError:
      pass
    raise ValueError("Could not find IDE window")

  def switcher_focus_browser():
    """Switches to the saved browser window or try to find an app."""
    if "browser" in _window_id_by_name:
      try:
        _focus_window_by_id(_window_id_by_name["browser"])
        return
      except ValueError:
        # Could not find window. Delete the saved ID and fall back to switching apps.
        del _window_id_by_name["browser"]

    # No saved window, or saved window could not be found. Try to switch to known browsers.
    try:
      actions.user.switcher_focus("Chrome")
      return
    except ValueError:
      pass
    try:
      actions.user.switcher_focus("Safari")
      return
    except ValueError:
      pass
    raise ValueError("Could not find browser window")

  def switcher_focus_terminal():
    """Switches to the saved terminal window or try to find an app."""
    if "terminal" in _window_id_by_name:
      try:
        _focus_window_by_id(_window_id_by_name["terminal"])
        return
      except ValueError:
        # Could not find window. Delete the saved ID and fall back to switching apps.
        del _window_id_by_name["terminal"]

    # No saved window, or saved window could not be found. Try to switch to known terminals.
    try:
      actions.user.switcher_focus("iTerm2")
      return
    except ValueError:
      pass
    try:
      actions.user.switcher_focus("Terminal")
      return
    except ValueError:
      pass
    raise ValueError("Could not find terminal window")

  def switcher_focus_browser_tab_by_hostname(hostname: str):
    """Switches to the browser tab with the given hostname in the URL. If a tab is already focused and multiple tabs
    match, focuses the next one."""
    if _is_chrome_running():
      get_all_tabs_action = actions.user.chrome_get_all_tabs
      focus_tab_action = actions.user.chrome_focus_tab
      is_browser_focused = _is_chrome_focused()
    elif _is_safari_running():
      get_all_tabs_action = actions.user.safari_get_all_tabs
      focus_tab_action = actions.user.safari_focus_tab
      is_browser_focused = _is_safari_focused()
    else:
      raise ValueError("Did not find running browser.")

    # Get all tabs matching the given hostname.
    tabs: list[browser_util.Tab] = get_all_tabs_action()
    matches = browser_util.get_tabs_matching_hostname(tabs, hostname)
    if len(matches) == 0:
      raise ValueError(f"No tabs found with hostname: {hostname}")

    # Check if we are already focused on a matching tab.
    focused_tab_index = browser_util.get_focused_tab_list_index(matches)
    if not is_browser_focused and focused_tab_index is not None:
      # The browser is not focused, but it is already on a matching tab. Switch to it.
      focus_tab_action(matches[focused_tab_index].window_index, matches[focused_tab_index].index)
    elif is_browser_focused and focused_tab_index is not None and len(matches) > 1:
      # We are already focused on a matching tab with more available. Go to the next matching tab.
      next_index = (focused_tab_index + 1) % len(matches)
      focus_tab_action(matches[next_index].window_index, matches[next_index].index)
    else:
      # Go to the first matching tab.
      focus_tab_action(matches[0].window_index, matches[0].index)


def _on_app_change(event: str):
  del event
  _update_running_list()


def _on_ready():
  _update_launch_list()
  _update_running_list()
  ui.register("app_launch", _on_app_change)
  ui.register("app_close", _on_app_change)


app.register("ready", _on_ready)
