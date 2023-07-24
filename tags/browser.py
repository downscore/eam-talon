"""Actions for browsers."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()


@ctx.action_class("browser")
class Actions:
  """Default implementations for common browser actions."""

  # def address() -> str:
  #   # Note: It looks like browser.address() is called several times by Talon on startup. It should not be implemented
  #   # by performing any keyboard input, and should likely not be implemented at all unless its usage within Talon is
  #   # understood.
  #   pass

  def bookmark():
    actions.key("cmd-d")

  def bookmark_tabs():
    actions.key("cmd-shift-d")

  def bookmarks():
    actions.key("cmd-alt-b")

  def bookmarks_bar():
    actions.key("cmd-shift-b")

  def focus_address():
    actions.key("cmd-l")

  def focus_search():
    actions.browser.focus_address()

  def go(url: str):
    actions.browser.focus_address()
    actions.sleep("50ms")
    actions.insert(url)
    actions.key("enter")

  def go_back():
    actions.key("cmd-[")

  def go_blank():
    actions.key("cmd-n")

  def go_forward():
    actions.key("cmd-]")

  def go_home():
    actions.key("cmd-shift-h")

  def open_private_window():
    actions.key("cmd-shift-n")

  def reload():
    actions.key("cmd-r")

  def reload_hard():
    actions.key("cmd-shift-r")

  def show_history():
    actions.key("cmd-y")

  def submit_form():
    actions.key("enter")

  def toggle_dev_tools():
    actions.key("cmd-alt-i")


@mod.action_class
class ExtensionActions:
  """Browser actions that are not built in to Talon."""

  def browser_copy_address():
    """Copy the current browser address to the clipboard."""
    actions.user.clipboard_history_set_text(actions.browser.address())

  def browser_open_private_tab():
    """Open a new private tab."""
    actions.key("cmd-shift-n")
