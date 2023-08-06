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

  def bring_line_by_number(n: int):
    """Copies a given line to the cursor location."""
    # Insert some unique placeholder text so we can find the insertion position later.
    # Note: In VS Code, the workbench.action.navigateBack action is unreliable for finding the insertion position.
    placeholder = f"!!!BringLine{n}!!!"
    actions.user.insert_via_clipboard(placeholder)

    # In VS Code, jumps to beginning of line, before indentation.
    actions.edit.jump_line(n)
    actions.sleep("100ms")

    # Get line without trailing newline.
    actions.edit.extend_line_end()
    line = actions.edit.selected_text()

    # Go back to original position and insert the line.
    actions.edit.find()
    actions.user.insert_via_clipboard(placeholder)
    actions.key("escape")
    actions.user.insert_via_clipboard(line)
