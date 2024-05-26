"""Talon code for ChatGPT support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.chatgpt = """
app.bundle: com.openai.chat
"""

ctx.matches = r"""
app: chatgpt
"""


@mod.action_class
class Actions:
  """ChatGPT app actions."""

  def chatgpt_new_chat():
    """Start a new chat in ChatGPT."""
    actions.key("cmd-n")
    actions.sleep("500ms")

  def chatgpt_new_temporary_chat():
    """Start a new temporary chat in ChatGPT."""
    actions.key("cmd-shift-n")
    actions.sleep("500ms")
