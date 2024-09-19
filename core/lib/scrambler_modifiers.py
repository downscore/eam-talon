"""Modifiers that can be applied to text ranges. Used to find regions of text for navigation and
modification."""

import re
from typing import Callable, Sequence
from .scrambler_types import Modifier, ModifierType, TextMatch, TextRange, UtilityFunctions

# Regex for matching a token.
_REGEX_TOKEN: re.Pattern = re.compile(r"[\w_]+")


def get_phrase_regex(words: Sequence[str], get_homophones: Callable[[str], list[str]]) -> str:
  """Get a regex for matching the given phrase. Expands with homophones using `get_homophones`:
  Given a word, the function should return a list containing the word and its homophones."""
  alts = []
  for word in words:
    # Get all homophones in lowercase and escaped for use in a regex.
    phones = list(map(lambda w: re.escape(w.lower()), get_homophones(word)))
    phones_alt = ""
    if len(phones) > 1:
      phones_alt = f"({'|'.join(phones)})"  # pylint: disable=inconsistent-quotes
    elif len(phones) == 1:
      phones_alt = phones[0]
    if len(phones_alt) > 0:
      alts.append(phones_alt)
  return r"[ .,\-\_\"]*".join(alts)


def _maybe_add_token_deletion_range(text: str, match: TextMatch) -> TextMatch:
  """Adds a deletion range to the given token match to include spaces and commas around the
  token."""
  assert match.text_range.end <= len(text)

  # Check if there is ", " following the token.
  if match.text_range.end + 1 < len(text) and text[match.text_range.end] == "," and text[
      match.text_range.end + 1] == " ":
    return TextMatch(text_range=match.text_range,
                     deletion_range=TextRange(match.text_range.start, match.text_range.end + 2))

  # Check for space or comma.
  if match.text_range.end < len(text) and text[match.text_range.end] in (" ", ","):
    return TextMatch(text_range=match.text_range,
                     deletion_range=TextRange(match.text_range.start, match.text_range.end + 1))

  # If the sentence ends following the token, try to include a leading space in the deletion range.
  if (match.text_range.end == len(text) or text[match.text_range.end] in
      (".", "?", "!")) and match.text_range.start > 0 and text[match.text_range.start - 1] == " ":
    return TextMatch(text_range=match.text_range,
                     deletion_range=TextRange(match.text_range.start - 1, match.text_range.end))

  # The deletion range would be the same as the text range, so do not include it.
  return TextMatch(text_range=match.text_range)


def _apply_token_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                               utilities: UtilityFunctions) -> TextMatch:
  """Gets the next token after the input match."""
  del modifier, utilities
  search_text = text[input_match.text_range.end:]
  match = _REGEX_TOKEN.search(search_text)
  if match is None:
    raise ValueError(f"No token found after input match: {input_match}")
  return _maybe_add_token_deletion_range(
      text,
      TextMatch(
          TextRange(input_match.text_range.end + match.start(),
                    input_match.text_range.end + match.end())))


def _apply_token_previous_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                   utilities: UtilityFunctions) -> TextMatch:
  """Gets the previous token before the input match."""
  del modifier, utilities
  # Reverse the string for searching. The order of characters in a token is not important, so
  # reversing them does not affect the match.
  search_text = text[:input_match.text_range.start][::-1]
  match = _REGEX_TOKEN.search(search_text)
  if match is None:
    raise ValueError(f"No token found before input match: {input_match}")
  return _maybe_add_token_deletion_range(
      text,
      TextMatch(
          TextRange(input_match.text_range.start - match.end(),
                    input_match.text_range.start - match.start())))


_MODIFIER_FUNCTIONS = {
    ModifierType.TOKEN_NEXT: _apply_token_next_modifier,
    ModifierType.TOKEN_PREVIOUS: _apply_token_previous_modifier,
}


def apply_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                   utilities: UtilityFunctions) -> TextMatch:
  """Applies a modifier to the given range and returns the new range."""
  if input_match.text_range.end > len(text):
    raise ValueError(f"Match beyond end of text: {input_match}")

  # Apply the modifier the requested number of times.
  result = input_match
  for _ in range(0, modifier.repeat):
    result = _MODIFIER_FUNCTIONS[modifier.modifier_type](text, result, modifier, utilities)
  return result
