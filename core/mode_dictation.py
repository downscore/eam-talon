"""Talon code for dictation mode."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, actions
from .lib import format_util

mod = Module()

_NUM_PRECEDING_CHARS = 2


def _get_preceding_text() -> str:
  """Gets the preceding text to use for dictation."""
  for _ in range(_NUM_PRECEDING_CHARS):
    actions.edit.extend_left()
  preceding_text = actions.edit.selected_text()
  actions.edit.right()
  return preceding_text


def _backspace_required(preceding_text: str, next_text: str) -> bool:
  """Determine if we must press backspace before inserting the next text."""
  # Backspace if we are inserting a period after a space.
  if len(preceding_text) < 2:
    return False
  return preceding_text[-1] == " " and preceding_text[-2] != " " and next_text[0] in (".", ",", ";", ")", "]", "}", ">",
                                                                                      ":", "?", "!")


def _space_required(preceding_text: str, next_text: str) -> bool:
  """Determines if a space is required between the preceding and next text."""
  # Assume there is no preceding text if the text is too long (the editor may copy the entire line if no selection).
  if len(preceding_text) == 0 or len(preceding_text) > _NUM_PRECEDING_CHARS:
    return False
  if len(next_text) == 0:
    return False
  preceding_char = preceding_text[-1]
  next_char = next_text[0]
  if next_char in (".", ",", ";", ")", "]", "}", ">", ":", "?", "!", "%", "'", "\""):
    return False
  if preceding_char in (" ", "$", "#", "@", "\n", "(", "[", "{", "<", "-", "_", "/", "'", "\""):
    return False
  return True


def _capitalization_required(preceding_text: str) -> bool:
  """Determines if capitalization is required for the next word."""
  # Assume there is no preceding text if the text is too long (the editor may copy the entire line if no selection).
  if len(preceding_text) == 0 or len(preceding_text) > _NUM_PRECEDING_CHARS:
    return True
  last_char = preceding_text[-1] if preceding_text[-1] != " " else preceding_text[-2]
  if last_char.isalnum() or last_char in ("%", ";", ":", ",", "(", ")", "[", "]", "{", "}", "<", ">", "-", "_", "/",
                                          "'", "\""):
    return False
  return True


@mod.action_class
class Actions:
  """Dictation mode actions."""

  def dictation_insert_prose(prose: str):
    """Inserts prose using maintained state (e.g. for spacing and capitalization) from dictation mode. Updates
    maintained state based on what is inserted."""
    preceding_text = _get_preceding_text()
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
