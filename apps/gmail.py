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


# Pressing "right" at the end of the text when writing a reply (note: not composing a new email) can
# jump to another UI element and interpret subsequent keystrokes as commands. This happens even when
# the cursor is on the left side of a selection that includes the end of the text.
@ctx.action_class("user")
class ExtensionActions:
  """Action overrides."""

  def line_end():
    # Move to the start of the line first to work around unusual UI behavior in Gmail.
    # See above for more information.
    actions.key("cmd-left cmd-right")

  def dictation_get_preceding_text() -> str:
    """Gets the preceding text to use for dictation."""
    for _ in range(mode_dictation.NUM_PRECEDING_CHARS):
      actions.user.extend_left()
    preceding_text = actions.user.selected_text()

    # Select to the right for the number of characters we actually selected. This works around
    # unusual UI behavior. See above for more information.
    for _ in range(len(preceding_text)):
      actions.user.extend_right()

    return preceding_text

  def scrambler_potato_get_text_before_cursor():
    # We only allow scrambler to act on one line in Gmail due to unusual UI behavior. See above for
    # more information.
    actions.key("ctrl-shift-a")
    result = actions.user.selected_text()

    # Select to the right for the number of characters we actually selected. This works around
    # unusual UI behavior.
    for _ in range(len(result)):
      actions.user.extend_right()

    return result

  def scrambler_potato_get_text_after_cursor():
    # We only allow scrambler to act on one line in Gmail due to unusual UI behavior. See above for
    # more information.
    actions.key("ctrl-shift-e")
    result = actions.user.selected_text()
    if len(result) > 0:
      actions.user.left()
    return result
