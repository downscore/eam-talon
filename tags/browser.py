"""Actions for browsers."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from ..core.lib import browser_util

mod = Module()
ctx = Context()


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


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def app_get_current_location() -> str:
    return actions.browser.address()
