"""Talon code for cross-browser actions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from dataclasses import dataclass
from typing import Callable
from talon import Context, Module, ui, actions
from .lib import browser_util

mod = Module()
ctx = Context()


@dataclass
class BrowserInterface:
  """Interface to a running browser."""
  app: ui.App
  get_all_tabs: Callable[[], list[browser_util.Tab]]
  focus_tab: Callable[[int], None]
  focus_tab_and_window: Callable[[int, int], None]
  is_focused: Callable[[], bool]
  get_current_address: Callable[[], str]


def _get_active_browser_interface() -> BrowserInterface:
  """Gets an interface to the currently-running browser."""
  chrome_app = actions.user.chrome_get_app()
  if chrome_app:
    return BrowserInterface(chrome_app, actions.user.chrome_get_all_tabs,
                            actions.user.chrome_focus_tab, actions.user.chrome_focus_tab_and_window,
                            actions.user.chrome_is_focused, actions.user.chrome_get_current_address)

  safari_app = actions.user.safari_get_app()
  if safari_app:
    return BrowserInterface(safari_app, actions.user.safari_get_all_tabs,
                            actions.user.safari_focus_tab, actions.user.safari_focus_tab_and_window,
                            actions.user.safari_is_focused, actions.user.safari_get_current_address)

  raise ValueError("Found no running browser.")


def _focus_tab_and_window_with_context(interface: BrowserInterface,
                                       context: browser_util.BrowserContext, window_index: int,
                                       tab_index: int):
  """Internal implementation for focusing a tab using a context."""
  # Try to find the window for the given window index.
  window_id = context.window_ids[window_index -
                                 1] if len(context.window_ids) >= window_index else None
  window = None
  if window_id:
    for w in interface.app.windows():
      if w.id == window_id:
        window = w
        break

  # Fall back to focus method that does not use a context if the window was not found. This method
  # can be unreliable if multiple windows or Chrome apps are open.
  if not window:
    print(f"Could not find window for changing browser tab. Window Index: {window_index}, "
          "Tab Index: {tab_index}")
    interface.focus_tab_and_window(window_index, tab_index)
    return

  # Focus the window, then focus the tab.
  actions.user.switcher_focus_window(window)
  interface.focus_tab(tab_index)


@mod.action_class
class Actions:
  """Cross-browser actions."""

  def cross_browser_get_current_address() -> str:
    """Gets the current address from the running browser."""
    return _get_active_browser_interface().get_current_address()

  def cross_browser_get_context() -> browser_util.BrowserContext:
    """Gets the context, including open tabs and windows, for the currently-running browser."""
    interface = _get_active_browser_interface()
    tabs = interface.get_all_tabs()
    return browser_util.match_windows(tabs, interface.app.windows())

  def cross_browser_focus_tab(tab_index: int):
    """Focuses the tab with the given index in the front window of the running browser. Index is
    1-based."""
    _get_active_browser_interface().focus_tab(tab_index)

  def cross_browser_focus_tab_and_window(window_index: int, tab_index: int):
    """Focuses the given window and tab in the running browser. Window and tab indices are 1-based.
    This may be unreliable if multiple windows or Chrome apps are open. Prefer to use the
    context-based actions when possible."""
    interface = _get_active_browser_interface()
    interface.focus_tab_and_window(window_index, tab_index)

  def cross_browser_focus_tab_and_window_with_context(context: browser_util.BrowserContext,
                                                      window_index: int, tab_index: int):
    """Focuses the tab specified by the given context."""
    interface = _get_active_browser_interface()
    _focus_tab_and_window_with_context(interface, context, window_index, tab_index)

  def cross_browser_focus_tab_by_hostname(hostname: str):
    """Focuses the first tab with a URL containing the given hostname."""
    interface = _get_active_browser_interface()
    all_tabs = interface.get_all_tabs()

    # Get all tabs with a matching hostname.
    matching_tabs = browser_util.get_tabs_matching_hostname(all_tabs, hostname)
    if len(matching_tabs) == 0:
      raise ValueError(f"No tabs found with hostname: {hostname}")

    # Note: Windows need to be matched to all tabs, as the process relies on matching the title of
    # the active tab in each window.
    context = browser_util.match_windows(all_tabs, interface.app.windows())

    # Focus the appropriate matching tab.
    actions.user.cross_browser_focus_matching_tab(context, matching_tabs)

  def cross_browser_focus_matching_tab(context: browser_util.BrowserContext,
                                       matching_tabs: list[browser_util.Tab]):
    """Focuses a tab from a list of tabs matching some query."""
    if len(matching_tabs) == 0:
      raise ValueError("No matching tabs found.")

    interface = _get_active_browser_interface()
    is_browser_focused = interface.is_focused()

    # Check if we are already focused on a matching tab.
    focused_tab_index = browser_util.get_focused_tab_list_index(matching_tabs)
    if not is_browser_focused and focused_tab_index is not None:
      # The browser is not focused, but it is already on a matching tab. Switch to it.
      _focus_tab_and_window_with_context(interface, context,
                                         matching_tabs[focused_tab_index].window_index,
                                         matching_tabs[focused_tab_index].index)
    elif is_browser_focused and focused_tab_index is not None and len(matching_tabs) > 1:
      # We are already focused on a matching tab with more available. Go to the next matching tab.
      next_index = (focused_tab_index + 1) % len(matching_tabs)
      _focus_tab_and_window_with_context(interface, context, matching_tabs[next_index].window_index,
                                         matching_tabs[next_index].index)
    else:
      # Go to the first matching tab.
      _focus_tab_and_window_with_context(interface, context, matching_tabs[0].window_index,
                                         matching_tabs[0].index)

  def cross_browser_is_browser_focused():
    """Returns whether the browser is currently focused."""
    return _get_active_browser_interface().is_focused()
