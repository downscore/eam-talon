"""Talon code for Safari actions that can be used from other applications."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, ui
from talon.mac import applescript
from ..core.lib import browser_util

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
  """Safari global actions."""

  def safari_is_focused() -> bool:
    """Returns whether Safari is focused."""
    return ui.active_app().name == "Safari"

  def safari_get_app() -> ui.App:
    """Gets the running Safari app. Returns None if Safari is not running."""
    for running_app in ui.apps():
      if running_app.name == "Safari" and not running_app.background:
        return running_app
    return None

  def safari_get_current_address():
    """Insert the address of the active Safari tab."""
    script = """
      tell application "Safari"
          set theUrl to URL of front document
      end tell
      return theUrl
      """
    return applescript.run(script)

  def safari_get_all_tabs() -> list[browser_util.Tab]:
    """Gets all open tabs in all open windows. This is a version of `browser_get_all_tabs` that can be used when
    Safari doesn't have focus."""
    script = f'set my_window_delimiter to "{browser_util.WINDOW_DELIMITER}"\n\n'
    script += f'set my_tab_delimiter to "{browser_util.TAB_DELIMITER}"\n\n'
    script += """
      on remove_delimiters_from_text(input_text, my_tab_delimiter, my_window_delimiter)
        set AppleScript's text item delimiters to my_tab_delimiter
        set temp_list to text items of input_text
        set AppleScript's text item delimiters to "^^^"
        set temp_list to text items of temp_list as text
        set AppleScript's text item delimiters to "" -- Reset delimiters to default
        return temp_list as text
      end remove_delimiters_from_text

      tell application "Safari"
        set output to {}
        set window_list to every window
        repeat with w from 1 to count window_list
          set current_window to item w of window_list
          set active_tab to current tab of current_window
          set end of output to {my_window_delimiter & w & "," & (index of active_tab) & my_window_delimiter}
          set tab_list to every tab of current_window
          repeat with t from 1 to count tab_list
            set tab_url to url of tab t of current_window
            set tab_name to name of tab t of current_window
            set clean_url to my remove_delimiters_from_text(tab_url, my_tab_delimiter, my_window_delimiter)
            set clean_name to my remove_delimiters_from_text(tab_name, my_tab_delimiter, my_window_delimiter)
            set tab_info to {clean_url & my_tab_delimiter & clean_name & my_tab_delimiter}
            set end of output to tab_info
          end repeat
        end repeat
      end tell
      return output as text
      """
    tab_list_string = applescript.run(script)
    return browser_util.parse_tab_list_string(tab_list_string)

  def safari_focus_tab_and_window(window_index: int, tab_index: int):
    """Focuses the specified tab and window. Window and tab indices are 1-based. This can be used when Safari doesn't
    have focus."""
    set_tab_script = f"""
      tell application "Safari"
        set current_window to window {window_index}
        tell current_window to set current tab to tab {tab_index}
        set index of current_window to 1 -- Brings the window to the front
        activate
      end tell
      """
    applescript.run(set_tab_script)

  def safari_focus_tab(tab_index: int):
    """Focuses the specified tab in the front window. Tab indices are 1-based. This can be used when Safari doesn't
    have focus."""
    set_tab_script = f"""
      tell application "Safari"
        set current_window to front window
        tell current_window to set current tab to tab {tab_index}
        activate
      end tell
      """
    applescript.run(set_tab_script)
