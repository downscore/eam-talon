"""Talon code for Chrome support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from talon.mac import applescript
from ..core.lib import browser_util

mod = Module()
ctx = Context()

mod.apps.chrome = "app.name: Google Chrome"
mod.apps.chrome = """
os: mac
and app.bundle: com.google.Chrome
"""
mod.apps.chrome = """
os: mac
and app.bundle: org.chromium.Chromium
"""

ctx.matches = r"""
app: chrome
"""


@ctx.action_class("browser")
class BrowserActions:
  """Browser action overrides."""

  def address():
    return applescript.run("""
                tell application id "com.google.Chrome"
                    if not (exists (window 1)) then return ""
                    return window 1's active tab's URL
                end tell
            """)


@ctx.action_class("user")
class ExtensionActions:
  """Action overrides."""

  def browser_go(url: str):
    applescript.run("""
                tell application id "com.google.Chrome"
                    if not (exists (window 1)) then return
                    set window 1's active tab's URL to "[URL]"
                end tell
            """.replace("[URL]", url))

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

  def tab_close():
    actions.key("cmd-w")

  def tab_next():
    actions.key("cmd-shift-]")

  def tab_open():
    actions.key("cmd-t")

  def tab_previous():
    actions.key("cmd-shift-a")
    actions.sleep("250ms")
    actions.key("enter")

  def tab_reopen():
    actions.key("cmd-shift-t")

  def tab_left():
    actions.key("cmd-shift-[")

  def tab_right():
    actions.key("cmd-shift-]")

  def tab_switch_by_index(num: int):
    actions.key(f"cmd-{num}")

  def tab_list(name: str):
    actions.key("cmd-shift-a")
    actions.sleep("250ms")
    if name:
      actions.insert(name)
      actions.sleep("50ms")

  def browser_get_all_tabs() -> list[browser_util.Tab]:
    return actions.user.chrome_get_all_tabs()
