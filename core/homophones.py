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

_HOMOPHONE_SETS = homophone_util.get_homophone_sets(load_lists_from_csv("homophones.csv"))
_HOMOGRAPH_HOMOPHONE_SETS = homophone_util.get_homograph_homophone_sets(
    load_lists_from_csv("homophones_homographs.csv"))
_WORD_TO_HOMOPHONE_SET = homophone_util.get_word_to_homophone_set_dict(
    _HOMOPHONE_SETS, _HOMOGRAPH_HOMOPHONE_SETS)


@mod.action_class
class Actions:
  """Homophones actions."""

  def homophones_selected_word():
    """Replaces the selected word with the next homophone. Attempts to match case."""
    selected: str = actions.user.selected_text_or_word()
    selected_stripped = text_util.StrippedString(selected)

    if len(selected_stripped.stripped) == 0 or " " in selected_stripped.stripped:
      print(f"Invalid word for homophones: {selected_stripped}")
      return

    # Handle casing and replace non-ascii apostrophes with an ascii quote.
    guessed_capitalization = format_util.guess_capitalization(selected_stripped.stripped)
    word_key = selected_stripped.stripped.lower().replace("’", "'")

    if word_key not in _WORD_TO_HOMOPHONE_SET:
      actions.app.notify(f"No homophones found: {word_key}")
      return

    # Get homophone, trying to match original case and whitespace padding.
    homophone_set = _WORD_TO_HOMOPHONE_SET[word_key]
    result = format_util.format_word_capitalization(homophone_set.get_next_word(word_key),
                                                    guessed_capitalization)
    result = selected_stripped.apply_padding(result)

    # Insert homophone.
    actions.insert(result)

  def get_all_homophones(word: str) -> list[str]:
    """Gets a list of all homophones for the given word, including the given word."""
    if word not in _WORD_TO_HOMOPHONE_SET:
      return [word]

    homophone_set = _WORD_TO_HOMOPHONE_SET[word]

    # Return concatenation of common and uncommon word lists
    return homophone_set.words_excluding_uncommon + homophone_set.uncommon_words

  def get_next_homophone(word: str) -> Optional[str]:
    """Gets the next homophone for the given word, or None if there are no homophones for it."""
    if word not in _WORD_TO_HOMOPHONE_SET:
      return None
    return _WORD_TO_HOMOPHONE_SET[word].get_next_word(word)
