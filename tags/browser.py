"""Actions for browsers."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from ..core.lib import browser_util

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: browser
"""


def _get_tab_title() -> str:
  """Gets the title of the current tab for use with saving context links in markdown."""
  title = actions.win.title()
  partial_suffix = " - Google Chrome"
  if partial_suffix in title:
    title = title[:title.index(partial_suffix)]
  title = title.replace("[", "").replace("]", "").replace("(", "").replace(")", "")
  return title


def _add_new_context_line():
  """Focuses Obsidian and adds a new line to the context section of the current document."""
  actions.user.switcher_focus_app_by_name("Obsidian")
  actions.user.textflow_move_cursor_after_markdown_section("Context")
  actions.user.line_insert_down()


@mod.action_class
class BrowserActions:
  """Browser actions.
  Note that many of these actions are also built-in to Talon in the "browser" namespace. They are defined here in the
  "user" namespace to avoid conflicts with Talon internals.

  It looks like browser.address() is called several times by Talon on startup. It should not be implemented by
  performing any keyboard input, and should likely not have a default implementation unless its usage within Talon is
  understood."""

  def browser_go(url: str):
    """Navigates to the specified URL."""
    actions.user.browser_focus_address()
    actions.sleep("50ms")
    actions.insert(url)
    actions.key("enter")

  def browser_reload():
    """Reloads the current page."""
    actions.key("cmd-r")

  def browser_focus_address():
    """Focuses the browser address bar."""
    actions.key("cmd-l")

  def browser_open_private_tab():
    """Opens a new private tab."""
    actions.key("cmd-shift-n")

  def browser_bookmarks():
    """Opens the browser bookmarks."""
    actions.key("cmd-alt-b")

  def browser_add_bookmark():
    """Adds a bookmark for the current page."""
    actions.key("cmd-d")

  def browser_get_all_tabs() -> list[browser_util.Tab]:
    """Gets all open tabs in all open windows."""
    # Implementation most likely requires AppleScript, an extension, or similar.
    raise NotImplementedError()

  def browser_add_tab_to_context_and_close():
    """Adds the current tab to the context section of the current Obisidan doc and closes it."""
    url = actions.user.app_get_current_location()
    title = _get_tab_title()
    actions.user.tab_close()
    _add_new_context_line()
    actions.user.insert_via_clipboard(f"[{title}]({url})")

  def browser_add_tab_to_context_keep_open():
    """Adds the current tab to the context section of the current Obisidan doc but does not close it."""
    url = actions.user.app_get_current_location()
    title = _get_tab_title()
    _add_new_context_line()
    actions.user.insert_via_clipboard(f"[{title}]({url})")


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def app_get_current_location() -> str:
    return actions.browser.address()
