"""Actions and tags for apps with line numbers."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.tag("line_numbers", "Apps with line numbers")

ctx.matches = r"""
tag: user.line_numbers
"""


@ctx.action_class("edit")
class EditActions:
  """Overrides for built-in edit actions."""

  def jump_line(n: int):
    actions.key("ctrl-g")
    actions.insert(str(n))
    actions.key("enter")


@mod.action_class
class Actions:
  """Line number actions."""

  def select_line_range(from_index: int, to_index: int = 0):
    """Selects a range of lines. 1-based. If `to_index` is zero, selects the from line."""
    actions.edit.jump_line(from_index)
    if to_index <= from_index:
      actions.edit.select_line()
    else:
      for _ in range(to_index - from_index + 1):
        actions.edit.extend_down()
