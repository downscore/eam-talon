"""Talon code for Safari support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import collections
import re
from talon import Context, Module, actions, ui
from talon.mac import applescript
from ..core.lib import browser_util
from ..core.lib.textflow_match import get_phrase_regex

mod = Module()
ctx = Context()

mod.apps.safari = """
os: mac
and app.bundle: com.apple.Safari
"""

ctx.matches = r"""
app: safari
"""


@ctx.action_class("browser")
class BrowserActions:
  """Browser action overrides."""

  def address():
    script = """
      tell application "Safari"
          set currentURL to URL of front document
          return currentURL
      end tell
    """
    return applescript.run(script)


@ctx.action_class("user")
class ExtensionActions:
  """Action overrides."""

  def browser_go(url: str):
    toolbar = ui.active_window().children.find_one(AXRole="AXToolbar", max_depth=1)
    address_field = toolbar.children.find_one(
        AXRole="AXTextField",
        AXIdentifier="WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD",
    )
    # Need to focus the address bar so that the updated text is recognized.
    address_field.AXFocused = True
    address_field.AXValue = url
    address_field.perform("AXConfirm")

  def find():
    actions.key("cmd-f")
    # Add a brief pause so we don't swallow subsequent keystrokes before the find dialog opens.
    actions.sleep("100ms")

  def line_insert_down():
    actions.user.line_end()
    actions.key("shift-enter")

  def line_insert_up():
    # Going to line end first can help consistently preserve indentation in code.
    actions.user.line_end()
    actions.user.line_start()
    actions.key("shift-enter up")

  def paste_match_style():
    actions.sleep("50ms")
    actions.key("cmd-shift-alt-v")
    actions.sleep("50ms")

  def tab_close():
    actions.key("cmd-w")

  def tab_next():
    actions.key("cmd-shift-]")

  def tab_open():
    actions.key("cmd-t")

  def tab_previous():
    actions.key("ctrl-tab")

  def tab_reopen():
    actions.key("cmd-shift-t")

  def tab_left():
    actions.key("cmd-shift-[")

  def tab_right():
    actions.key("cmd-shift-]")

  def tab_switch_by_index(num: int):
    actions.key(f"cmd-{num}")

  def tab_switch_by_name(name: str):
    # TODO: Implement in browser tag using browser_get_all_tabs and other actions.
    tab_delimiter = "|||"
    script = f"set my_delimiter to \"{tab_delimiter}\"\n\n"
    script += """
      on remove_delimiter_from_text(the_text, the_delimiter)
          set AppleScript's text item delimiters to the_delimiter
          set text_items to text items of the_text
          set AppleScript's text item delimiters to ""
          set the_text to text_items as text
          return the_text
      end remove_delimiter_from_text

      tell application "Safari"
          set currentWindow to front window
          set all_tabs to {}
          set tab_count to count of tabs in currentWindow
          repeat with j from 1 to tab_count
              set tab_url to url of tab j of currentWindow
              set tab_name to name of tab j of currentWindow
              set clean_url to my remove_delimiter_from_text(tab_url, my_delimiter)
              set clean_name to my remove_delimiter_from_text(tab_name, my_delimiter)
              set tab_info to {clean_url & my_delimiter & clean_name & my_delimiter}
              set end of all_tabs to tab_info
          end repeat
      end tell
      return all_tabs as text
      """
    tab_list_string = applescript.run(script)

    # Removed trailing delimiter from output, if present.
    if tab_list_string.endswith(tab_delimiter):
      tab_list_string = tab_list_string[:-len(tab_delimiter)]

    # Make a list of tabs.
    Tab = collections.namedtuple("Tab", ["name", "url"])
    tab_strings = tab_list_string.split(tab_delimiter)
    tabs: list[Tab] = []
    for i in range(0, len(tab_strings), 2):
      tabs.append(Tab(name=tab_strings[i + 1].strip(), url=tab_strings[i].strip()))

    # Prepare query regex.
    regex_str = get_phrase_regex(name.split(), actions.user.get_all_homophones)
    regex = re.compile(regex_str, re.IGNORECASE)

    # Find the tab with the given string as a substring of its name or URL.
    found_index = 0  # 1-based.
    for i, tab in enumerate(tabs):
      # Perform a case-insensitive search with homophones.
      if regex.search(tab.name) or regex.search(tab.url):
        found_index = i + 1
        break
    if found_index == 0:
      raise ValueError(f"Could not find tab. Name: {name}")

    # Switch to the tab.
    set_tab_script = f"""
      tell application "Safari"
          set currentWindow to front window
          set current tab of currentWindow to tab {found_index} of currentWindow
      end tell
      """
    applescript.run(set_tab_script)

  def tab_list(name: str):
    actions.key("cmd-shift-\\")
    actions.sleep("250ms")
    if name:
      actions.key("cmd-f")
      actions.insert(name)
      actions.sleep("50ms")

  def browser_get_all_tabs() -> list[browser_util.Tab]:
    return actions.user.safari_get_all_tabs()
