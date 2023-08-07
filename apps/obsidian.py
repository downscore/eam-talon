"""Talon code for Obsidian support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.obsidian = """
app.bundle: md.obsidian
"""

ctx.matches = r"""
app: obsidian
"""


@mod.action_class
class Actions:
  """Obsidian actions."""

  def obsidian(command: str):
    """Executes a command using the Obsidian command palette."""
    actions.key("cmd-p")
    actions.insert(command)
    actions.key("enter")


@ctx.action_class("edit")
class EditActions:
  """Edit action overwrites."""

  def select_line(n: int = None):
    # cmd-left stops before checkboxes in Obsidian.
    actions.key("cmd-left:2 cmd-shift-right shift-right")


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def navigation_back():
    actions.key("cmd-alt-left")

  def navigation_forward():
    actions.key("cmd-alt-right")

  def split_down():
    actions.user.obsidian("Split down")

  def split_right():
    actions.user.obsidian("Split right")

  def tab_nth_previous(n: int):
    # Make sure number of tab switches is reasonable.
    if n < 1 or n > 9:
      return
    if n == 1:
      actions.key("ctrl-tab")
    else:
      actions.key(f"cmd-o down:{n} enter")

  def tab_switch_by_name(name: str):
    actions.key("cmd-o")
    actions.insert(name)
    actions.key("enter")

  def textflow_get_selected_text_potato_mode() -> str:
    # Obsidian copies the entire line if nothing is selected, which breaks a bunch of TextFlow stuff.
    # Always pretend nothing is selected.
    return ""

  def textflow_force_potato_mode() -> bool:
    # Obsidian does not properly implement the accessibility API. It does not give accurate character counts for
    # the current selection, and appears to group multiple consecutive line breaks into a single line break.
    return True
