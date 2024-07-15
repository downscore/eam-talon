"""Talon code for dictation mode."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from typing import Optional
from talon import Module, actions
from .lib import format_util

mod = Module()

NUM_PRECEDING_CHARS = 2


def _backspace_required(preceding_text: str, next_text: str) -> bool:
  """Determine if we must press backspace before inserting the next text."""
  # Backspace if we are inserting a period after a space.
  if len(preceding_text) < 2:
    return False
  return preceding_text[-1] == " " and preceding_text[-2] != " " and next_text[0] in (
      ".", ",", ";", ")", "]", "}", ">", ":", "?", "!")


def _space_required(preceding_text: str, next_text: str) -> bool:
  """Determines if a space is required between the preceding and next text."""
  if len(preceding_text) == 0:
    return False
  if len(next_text) == 0:
    return False
  preceding_char = preceding_text[-1]
  next_char = next_text[0]

  # Special case: No space after quotes if there is nothing before it.
  if len(preceding_text) == 1 and preceding_char in ("'", "\""):
    return False

  # Special case: No space after quotes if there is whitespace before it.
  if len(preceding_text) >= 2 and preceding_text[-2] in (" ", "\n",
                                                         "\t") and preceding_char in ("'", "\""):
    return False

  if next_char in (".", ",", ";", ")", "]", "}", ">", ":", "?", "!", "%", "'", "\"", "/"):
    return False
  if preceding_char in (" ", "#", "@", "\n", "(", "[", "{", "<", "-", "_", "/", "'"):
    return False
  return True


def _capitalization_required(preceding_text: str) -> bool:
  """Determines if capitalization is required for the next word."""
  if len(preceding_text) < 2:
    return True

  # Special case: Capitalize after "/ " to support dictating code comments.
  if preceding_text[-2:] == "/ ":
    return True

  last_char = preceding_text[-1] if preceding_text[-1] != " " else preceding_text[-2]
  if last_char.isalnum() or last_char in ("%", ";", ",", "(", ")", "[", "]", "{", "}", "<", "_",
                                          "/", "'", "\"", "`", "$", "=", "@"):
    return False
  return True


@mod.action_class
class Actions:
  """Dictation mode actions."""

  def dictation_insert_prose(prose: Optional[str]):
    """Inserts prose using the surrounding context to determine appropriate spacing and
    capitalization."""
    if prose is None or prose == "":
      return
    preceding_text = actions.user.dictation_get_preceding_text()
    if _backspace_required(preceding_text, prose):
      actions.key("backspace")
    if _space_required(preceding_text, prose):
      actions.insert(" ")
    if _capitalization_required(preceding_text):
      options = format_util.FormatOptions()
      options.first_capitalization = format_util.WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
      actions.insert(format_util.format_phrase(prose, options))
    else:
      actions.insert(prose)

  def dictation_repeat_line_insert_down(n: int):
    """Inserts a new line below `n` times"""
    for _ in range(n):
      actions.user.line_insert_down()

  def dictation_get_preceding_text() -> str:
    """Gets the preceding text to use for dictation."""
    for _ in range(NUM_PRECEDING_CHARS):
      actions.user.extend_left()
    preceding_text = actions.user.selected_text()

    # Deselect preceding text only if it was not empty.
    if preceding_text:
      actions.user.right()

    return preceding_text
