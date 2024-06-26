"""Actions and tags for apps that interact with source control."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.tag("source_control", "Application that interacts with source control")

ctx.matches = r"""
tag: user.source_control
"""


@mod.action_class
class Actions:
  """Source control-related actions."""

  def source_control_file_previous():
    """Jump to the previous changed file."""
    actions.user.tab_previous()

  def source_control_file_next():
    """Jump to the next changed file."""
    actions.user.tab_next()

  def source_control_change_previous():
    """Jump to the previous change in the current file."""

  def source_control_change_next():
    """Jump to the next change in the current file."""
