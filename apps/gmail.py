"""Talon code for Gmail support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from ..core import mode_dictation

mod = Module()
ctx = Context()

mod.apps.gmail = """
tag: browser
browser.host: /mail.google.com/
"""

ctx.matches = r"""
app: gmail
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def dictation_get_preceding_text() -> str:
    """Gets the preceding text to use for dictation."""
    for _ in range(mode_dictation.NUM_PRECEDING_CHARS):
      actions.user.extend_left()
    preceding_text = actions.user.selected_text()

    # Pressing "right" at the end of the text when writing a reply (note: not composing a new email) can jump to
    # another UI element and interpret subsequent keystrokes as commands. This happens even when the cursor is on the
    # left side of a selection that includes the end of the text.
    #
    # To avoid this, we just select to the right for the number of characters we actually selected.
    for _ in range(len(preceding_text)):
      actions.user.extend_right()

    return preceding_text
