"""Talon code for switching between apps."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from dataclasses import dataclass
from typing import Optional
from talon import Context, Module, app, imgui, ui, actions
import os
from .lib import app_util, browser_util
from .user_settings import load_dict_from_csv

mod = Module()
ctx = Context()


@dataclass
class FocusedWindowAndTab:
  """Struct used to remember the focused window, and potentially tab in that window."""
  window_id: int
  tab_index: Optional[int] = None  # Tab index is 1-based.


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

# Remembered focused window.
_saved_focused_window: Optional[FocusedWindowAndTab] = None

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

  def switcher_focus_app_by_name(name: str):
    """Focuses an application by name."""
    running_app = actions.user.switcher_get_running_app(name)
    running_app.focus()
    # Pause to give the app time to focus.
    # Note: More time may be required if the window is in a different workspace. Chrome in particular can take a while
    # to be ready for subsequent commands.
    actions.sleep("100ms")

  def switcher_focus_window(window: ui.Window):
    """Focuses the given window. Does nothing if the window is already focused."""
    if ui.active_window().id == window.id:
      return
    # Focus the window twice. In some cases (e.g. multiple fullscreen Chrome windows), this seems to be necessary.
    window.focus()
    window.focus()
    # Pause to give the app time to focus.
    # Note: More time may be required if the window is in a different workspace. Chrome in particular can take a while
    # to be ready for subsequent commands.
    actions.sleep("100ms")

  def switcher_focus_window_by_id(window_id: int):
    """Focuses the window with the given ID. Does nothing if the window is already focused."""
    for window in ui.windows():
      if window.id != window_id:
        continue
      actions.user.switcher_focus_window(window)
      return
    raise ValueError(f"Could not find window. ID: {window_id}")

  def switcher_focus_window_by_type(type_name: str, app_name1: str = "", app_name2: str = "", app_name3: str = ""):
    """Tries to focus a window given its type name and possible app names."""
    # Talon doesn't support list arguments, so use optional arguments instead.
    app_names: list[str] = []
    if app_name1:
      app_names.append(app_name1)
    if app_name2:
      app_names.append(app_name2)
    if app_name3:
      app_names.append(app_name3)

    if type_name in _window_id_by_name:
      try:
        actions.user.switcher_focus_window_by_id(_window_id_by_name[type_name])
        return
      except ValueError:
        # Could not find window. Delete the saved ID and fall back to switching to apps.
        del _window_id_by_name[type_name]

    # No saved window, or saved window could not be found. Try to switch to known applications.
    for app_name in app_names:
      try:
        actions.user.switcher_focus_app_by_name(app_name)
        return
      except ValueError:
        pass
    raise ValueError(f"Could not find window. Type: {type_name}")

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

  def switcher_focus_terminal():
    """Focuses the terminal application."""
    actions.user.switcher_focus_window_by_type("terminal", "Alacritty", "iTerm2", "Terminal")

  def switcher_focus_coder():
    """Focuses the IDE application."""
    actions.user.switcher_focus_window_by_type("coder", "Code", "Code - Insiders")

  def switcher_focus_browser():
    """Focuses the browser window."""
    actions.user.switcher_focus_window_by_type("browser", "Google Chrome", "Safari")

  def switcher_new_tmux_window(directory: str = ""):
    """Opens a new tmux window in the given directory. If directory is empty, open in the default directory, usually
    the current user's home."""
    actions.user.switcher_focus_terminal()
    actions.user.shell_tmux_new_window()
    if directory:
      actions.user.insert_via_clipboard(f"cd \"{directory.strip()}\"")
      actions.key("enter")
      actions.insert("ls")
      actions.key("enter")

  def switcher_save_current_window_by_name(name: str):
    """Saves the current window as the window with the given name."""
    _window_id_by_name[name] = ui.active_window().id

  def switcher_save_focus():
    """Saves the current window, and possibly tab in that window, to be restored to focus later."""
    global _saved_focused_window
    result = FocusedWindowAndTab(ui.active_window().id)
    # Check if a browser is currently focused.
    if actions.user.cross_browser_is_browser_focused():
      context: browser_util.BrowserContext = actions.user.cross_browser_get_context()

      # Print an error if window IDs don't match.
      if not context.window_ids:
        print("Saving focus: Browser context does not have window IDs.")
      if context.window_ids[0] != result.window_id:
        print(f"Saving focus: Window IDs do not match. Context: {context.window_ids[0]}, "
              "Active Window: {result.window_id}")

      # Get first active tab from the context.
      active_tab: Optional[browser_util.Tab] = next(
          filter(lambda tab: tab.active and tab.window_index == 1, context.tabs), None)
      if active_tab:
        result.tab_index = active_tab.index
    _saved_focused_window = result

  def switcher_restore_focus():
    """Restores saved window and possibly tab to focus."""
    if not _saved_focused_window:
      raise ValueError("No saved focus to restore.")
    print(f"Restoring focus: {_saved_focused_window}")
    actions.user.switcher_focus_window_by_id(_saved_focused_window.window_id)
    if _saved_focused_window.tab_index:
      actions.user.cross_browser_focus_tab(_saved_focused_window.tab_index)

  def switcher_jump_to_bookmark(bookmark_num: int):
    """Jumps to the bookmark with the given number."""
    actions.user.switcher_focus_coder()
    actions.key(f"ctrl-{bookmark_num}")


def _on_app_change(event: str):
  del event
  _update_running_list()


def _on_ready():
  _update_launch_list()
  _update_running_list()
  ui.register("app_launch", _on_app_change)
  ui.register("app_close", _on_app_change)


app.register("ready", _on_ready)
