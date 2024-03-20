"""Actions and overrides for functionality provided by the VS Code extension."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

ctx = Context()
mod = Module()

ctx.matches = r"""
app: vscode
"""


@mod.action_class
class Actions:
  """Actions available only when the VS Code extension is installed."""


@ctx.action_class("user")
class UserActions:
  """Action overrides available only when the VS Code extension is installed."""

  def jump_line(n: int):
    actions.user.vscode("eam-talon.jumpToLine", n)

  def select_line_range(from_index: int, to_index: int = 0):
    actions.user.vscode("eam-talon.selectLineRange", from_index, to_index if to_index > 0 else None)
