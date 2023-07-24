"""Actions and tags for apps with navigation."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.tag("navigation", "Apps with navigation")

ctx.matches = r"""
tag: user.navigation
"""


@mod.action_class
class Actions:
  """Navigation actions."""

  def navigation_back():
    """Go back."""
    actions.key("cmd-[")

  def navigation_forward():
    """Go forward."""
    actions.key("cmd-]")
