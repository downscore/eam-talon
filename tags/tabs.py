"""Actions and tags for apps with tabs."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

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
    actions.key("cmd-w")

  def tab_next():
    """Jumps to the next tab."""
    actions.key("cmd-shift-]")

  def tab_open():
    """Opens a new tab."""
    actions.key("cmd-t")

  def tab_previous():
    """Jumps to the previous tab."""
    actions.key("ctrl-tab")

  def tab_reopen():
    """Reopens the last closed tab."""
    actions.key("cmd-shift-t")

  def tab_left():
    """Jumps to the tab to the left."""
    actions.key("cmd-shift-[")

  def tab_right():
    """Jumps to the tab to the right."""
    actions.key("cmd-shift-]")

  def tab_switch_by_index(num: int):
    """Switches to a tab given its index."""
    actions.key(f"cmd-{num}")

  def tab_switch_by_name(name: str):
    """Switches to a tab by name."""

  def tab_list(name: str):
    """Lists open tabs and applies an optional search string."""

  def tab_nth_previous(n: int):
    """Switches to the nth previous tab."""
    # Make sure number of tab switches is reasonable.
    if n < 1 or n > 9:
      return
    # Default implementation can only switch to the previous tab.
    # Using key("ctrl:down tab:{n} ctrl:up") doesn't seem to work.
    actions.user.tab_previous()
