"""Actions and tags for apps with tabs."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from ..core.system import unsupported_command

mod = Module()
ctx = Context()

mod.tag("tabs", "Application with tabs")

ctx.matches = r"""
tag: user.tabs
"""


@mod.action_class
class Actions:
  """Tab-related actions."""

  def tab_close():
    """Closes the current tab."""
    unsupported_command("Closing tabs not supported.")

  def tab_next():
    """Jumps to the next tab."""
    unsupported_command("Going to next tab not supported.")

  def tab_open():
    """Opens a new tab."""
    unsupported_command("Opening tabs not supported.")

  def tab_previous():
    """Jumps to the previous tab."""
    unsupported_command("Going to previous tab not supported.")

  def tab_reopen():
    """Reopens the last closed tab."""
    unsupported_command("Reopening tabs not supported.")

  def tab_left():
    """Jumps to the tab to the left."""
    unsupported_command("Going to tab to the left not supported.")

  def tab_right():
    """Jumps to the tab to the right."""
    unsupported_command("Going to tab to the right not supported.")

  def tab_switch_by_index(num: int):
    """Switches to a tab given its index."""
    unsupported_command("Switching tabs by index not supported.")

  def tab_switch_by_name(name: str):
    """Switches to a tab by name."""
    unsupported_command("Switching tabs by name not supported.")

  def tab_list(name: str):
    """Lists open tabs and applies an optional search string."""
    unsupported_command("Listing tabs not supported.")

  def tab_nth_previous(n: int):
    """Switches to the nth previous tab."""
    # Make sure number of tab switches is reasonable.
    if n < 1 or n > 9:
      return
    # Default implementation can only switch to the previous tab.
    # Using key("ctrl:down tab:{n} ctrl:up") doesn't seem to work.
    actions.user.tab_previous()
