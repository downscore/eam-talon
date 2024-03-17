"""Talon code for handling homophones."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from typing import Optional
from talon import Context, Module, actions
from .lib import format_util, homophone_util, text_util
from .user_settings import load_lists_from_csv

mod = Module()
ctx = Context()

_NEXT_HOMOPHONE_DICT = homophone_util.get_next_homophone_dict(load_lists_from_csv("homophones.csv"))


@mod.action_class
class Actions:
  """Homophones actions."""

  def homophones_selected_word():
    """Replaces the selected word with the next homophone. Attempts to match case."""
    selected: str = actions.user.selected_text()
    if len(selected) == 0:
      actions.user.select_word()
      selected = actions.user.selected_text()
    selected_stripped = text_util.StrippedString(selected)

    if len(selected_stripped.stripped) == 0 or " " in selected_stripped.stripped:
      print(f"Invalid word for homophones: {selected_stripped}")
      return

    # Handle casing and replace non-ascii apostrophes with an ascii quote.
    guessed_capitalization = format_util.guess_capitalization(selected_stripped.stripped)
    word_key = selected_stripped.stripped.lower().replace("’", "'")

    if word_key not in _NEXT_HOMOPHONE_DICT:
      actions.app.notify(f"No homophones found: {word_key}")
      return

    # Get homophone, trying to match original case and whitespace padding.
    result = format_util.format_word_capitalization(_NEXT_HOMOPHONE_DICT[word_key], guessed_capitalization)
    result = selected_stripped.apply_padding(result)

    # Insert homophone.
    actions.insert(result)

  def get_all_homophones(word: str) -> list[str]:
    """Gets a list of all homophones for the given word, including the given word."""
    result = [word]
    curr_word = word
    while curr_word in _NEXT_HOMOPHONE_DICT:
      curr_word = _NEXT_HOMOPHONE_DICT[curr_word]
      if curr_word in result:
        break
      result.append(curr_word)
    return result

  def get_next_homophone(word: str) -> Optional[str]:
    """Gets the next homophone for the given word, or None if there are no homophones for it."""
    if word not in _NEXT_HOMOPHONE_DICT:
      return None
    return _NEXT_HOMOPHONE_DICT[word]
