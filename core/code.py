"""Default implementations for built-in Talon code actions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, actions

ctx = Context()


@ctx.action_class("code")
class Actions:
  """Default implementations for common code actions."""

  def complete():
    actions.key("ctrl-space")

  def rename(name: str):
    actions.key("f2")
    actions.sleep("50ms")
    actions.insert(name)

  def toggle_comment():
    actions.key("ctrl-/")
