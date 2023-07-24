"""Default implementations for built-in Talon app actions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, actions

ctx = Context()


@ctx.action_class("app")
class Actions:
  """Default implementations for common app actions."""

  def preferences():
    actions.key("cmd-,")
