"""Actions and overrides for functionality provided by the VS Code extension."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from ..core.lib import textflow_types as tf
from ..core import textflow as tft

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

  def bring_line_range(from_index: int, to_index: int = 0):
    actions.user.vscode("eam-talon.copyLinesToCursor", from_index, to_index if to_index > 0 else None)

  def textflow_get_context() -> tft.TextFlowContext:
    context = actions.user.vscode_return_value("eam-talon.getTextFlowContext")
    # Disable potato mode because we implement the set selection action.
    text_offset = context["textStartOffset"]
    result = tft.TextFlowContext(text=context["text"],
                                 selection_range=tf.TextRange(context["selectionStartOffset"] - text_offset,
                                                              context["selectionEndOffset"] - text_offset),
                                 text_offset=text_offset,
                                 potato_mode=False)
    return result

  def textflow_set_selection_action(editor_action: tf.EditorAction, context: tft.TextFlowContext):
    """Sets the selection in an editor, given a textflow context. Can be overwritten in apps with accessibility
    extensions."""
    if editor_action.text_range is None:
      raise ValueError("Set selection range action with missing range.")
    actions.user.vscode_and_wait("eam-talon.setSelection", editor_action.text_range.start + context.text_offset,
                                 editor_action.text_range.end + context.text_offset)
