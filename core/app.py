"""Default implementations for built-in Talon app actions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
  """App actions."""

  def preferences():
    """Opens app preferences."""
    actions.key("cmd-,")
