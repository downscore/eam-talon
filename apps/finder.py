"""Talon code for Finder support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from talon.mac import applescript

mod = Module()
ctx = Context()

mod.apps.finder = """
os: mac
and app.bundle: com.apple.finder
"""

ctx.matches = r"""
app: finder
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def file_manager_open_parent():
    actions.key("cmd-up")

  def file_manager_open_directory(path: str):
    actions.key("cmd-shift-g")
    actions.sleep("50ms")
    actions.insert(path)
    actions.key("enter")

  def file_manager_make_directory(name: str = ""):
    actions.key("cmd-shift-n")
    actions.sleep("50ms")
    if name:
      actions.insert(name)

  def tab_list(name: str):
    actions.key("cmd-shift-\\")
    actions.sleep("250ms")
    if name:
      actions.key("cmd-f")
      actions.insert(name)
      actions.sleep("50ms")

  def switcher_get_current_directory() -> str:
    return applescript.run(r"""
      tell application "Finder"
          set currentPath to POSIX path of (target of front window as alias)
      end tell
      return currentPath""")
