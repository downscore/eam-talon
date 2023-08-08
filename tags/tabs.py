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


@ctx.action_class("app")
class AppActions:
  """Default implementations for common app actions."""

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


@mod.action_class
class Actions:
  """Tab-related actions not covered in the 'app' set."""

  def tab_jump(number: int):
    """Jumps to the specified tab."""

  def tab_final():
    """Jumps to the final tab."""

  def tab_duplicate():
    """Duplicates the current tab."""

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

  def tab_nth_previous(n: int):
    """Switches to the nth previous tab."""
    # Make sure number of tab switches is reasonable.
    if n < 1 or n > 9:
      return
    # Default implementation can only switch to the previous tab.
    # Using key("ctrl:down tab:{n} ctrl:up") doesn't seem to work.
    actions.app.tab_previous()
