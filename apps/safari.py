"""Talon code for Safari support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, ui
from talon.mac import applescript
from ..core.lib import browser_util

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

  def tab_list(name: str):
    actions.key("cmd-shift-\\")
    actions.sleep("250ms")
    if name:
      actions.key("cmd-f")
      actions.insert(name)
      actions.sleep("50ms")

  def browser_get_all_tabs() -> list[browser_util.Tab]:
    return actions.user.safari_get_all_tabs()
