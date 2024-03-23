"""Actions and overrides for functionality provided by the Obsidian plugin."""
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
app: obsidian
"""


@mod.action_class
class Actions:
  """Actions available only when the Obsidian extension is installed."""


@ctx.action_class("user")
class UserActions:
  """Action overrides available only when the Obsidian extension is installed."""

  def jump_line(n: int):
    actions.user.obsidian_command("jumpToLine", n)

  def select_line_range(from_index: int, to_index: int = 0):
    actions.user.obsidian_command("selectLineRange", from_index, to_index if to_index > 0 else None)

  def bring_line_range(from_index: int, to_index: int = 0):
    actions.user.obsidian_command("copyLinesToCursor", from_index, to_index if to_index > 0 else None)

  def textflow_get_context() -> tft.TextFlowContext:
    context = actions.user.obsidian_command_return_value("getTextFlowContext")
    # Disable potato mode because we implement the set selection action.
    text_offset = context["textStartOffset"]
    result = tft.TextFlowContext(text=context["text"],
                                 selection_range=tf.TextRange(context["selectionFromOffset"] - text_offset,
                                                              context["selectionToOffset"] - text_offset),
                                 text_offset=text_offset,
                                 potato_mode=False)
    return result

  def textflow_set_selection_action(editor_action: tf.EditorAction, context: tft.TextFlowContext):
    """Sets the selection in an editor, given a textflow context. Can be overwritten in apps with accessibility
    extensions."""
    if editor_action.text_range is None:
      raise ValueError("Set selection range action with missing range.")
    actions.user.obsidian_command_and_wait("setSelection", editor_action.text_range.start + context.text_offset,
                                           editor_action.text_range.end + context.text_offset)