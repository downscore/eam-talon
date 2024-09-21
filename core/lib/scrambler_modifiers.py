"""Modifiers that can be applied to text ranges. Used to find regions of text for navigation and
modification."""

import re
from typing import Callable, Optional, Sequence
from .scrambler_types import Modifier, ModifierType, TextMatch, TextRange, UtilityFunctions

# Regex for matching a token.
_TOKEN_CHAR = r"[\w_]"  # Determines which characters are allowed in a token.
_NON_TOKEN_CHAR = r"[^\w_]"
_REGEX_TOKEN: re.Pattern = re.compile(_TOKEN_CHAR + r"+", re.IGNORECASE)


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


def _maybe_add_token_deletion_range(text: str, start: int, end: int) -> TextMatch:
  """Adds a deletion range to the given token match to include spaces and commas around the
  token."""
  assert end <= len(text)
  text_range = TextRange(start, end)

  # Check if there is ", " following the token.
  if end + 1 < len(text) and text[end] == "," and text[end + 1] == " ":
    return TextMatch(text_range=text_range, deletion_range=TextRange(start, end + 2))

  # Check for space or comma.
  if end < len(text) and text[end] in (" ", ","):
    return TextMatch(text_range=text_range, deletion_range=TextRange(start, end + 1))

  # If the sentence ends following the token, try to include a leading space in the deletion range.
  if (end == len(text) or text[end] in (".", "?", "!")) and start > 0 and text[start - 1] == " ":
    return TextMatch(text_range=text_range, deletion_range=TextRange(start - 1, end))

  # The deletion range would be the same as the text range, so do not include it.
  return TextMatch(text_range=text_range)


def _apply_token_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                               utilities: UtilityFunctions) -> TextMatch:
  """Gets the next token after the input match."""
  del modifier, utilities
  search_text = text[input_match.text_range.end:]
  match = _REGEX_TOKEN.search(search_text)
  if match is None:
    raise ValueError(f"No token found after input match: {input_match}")
  return _maybe_add_token_deletion_range(text, input_match.text_range.end + match.start(),
                                         input_match.text_range.end + match.end())


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
  return _maybe_add_token_deletion_range(text, input_match.text_range.start - match.end(),
                                         input_match.text_range.start - match.start())


def _get_word_start_token_match_after(search_text: str, search: str) -> Optional[TextRange]:
  """Tries to find a token starting with the given substring."""
  word_start_regex = re.compile(f"(^|{_NON_TOKEN_CHAR})({re.escape(search)}{_TOKEN_CHAR}*)",
                                re.IGNORECASE)
  match = word_start_regex.search(search_text)
  if match is None:
    return None
  start, end = match.span(2)
  return TextRange(start, end)


def _get_word_start_token_match_before(search_text: str, search: str) -> Optional[TextRange]:
  """Tries to find a token starting with the given substring, searching reversed text."""
  # Use a reversed search regex as the search text should also be reversed.
  word_start_regex = re.compile(f"({_TOKEN_CHAR}*{re.escape(search[::-1])})($|{_NON_TOKEN_CHAR})",
                                re.IGNORECASE)
  match = word_start_regex.search(search_text)
  if match is None:
    return None
  start, end = match.span(1)
  return TextRange(start, end)


def _get_substring_token_match(search_text: str, search: str) -> Optional[TextRange]:
  """Tries to find a token containing the given substring."""
  substring_regex = re.compile(f"{_TOKEN_CHAR}*{re.escape(search)}{_TOKEN_CHAR}*", re.IGNORECASE)
  match = substring_regex.search(search_text)
  return None if match is None else TextRange(match.start(), match.end())


def _apply_word_substring_closest_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                           utilities: UtilityFunctions) -> TextMatch:
  """Gets the closest token matching a given substring."""
  del utilities
  search_text_forward = text[input_match.text_range.end:]
  search_text_backward = text[:input_match.text_range.start][::-1]

  # First try to match the start of a word.
  match_forward = _get_word_start_token_match_after(search_text_forward, modifier.search)
  match_backward = _get_word_start_token_match_before(search_text_backward, modifier.search)

  # Match a substring if no word start is found.
  if match_forward is None and match_backward is None:
    match_forward = _get_substring_token_match(search_text_forward, modifier.search)
    match_backward = _get_substring_token_match(search_text_backward, modifier.search[::-1])

  if match_forward is None and match_backward is None:
    raise ValueError(f"No match for substring: {modifier.search}")

  forward_result = match_backward is None or (match_forward is not None and
                                              match_forward.start < match_backward.start)
  if forward_result:
    assert match_forward is not None
    return _maybe_add_token_deletion_range(text, input_match.text_range.end + match_forward.start,
                                           input_match.text_range.end + match_forward.end)
  assert match_backward is not None
  return _maybe_add_token_deletion_range(text, input_match.text_range.start - match_backward.end,
                                         input_match.text_range.start - match_backward.start)


def _apply_word_substring_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                        utilities: UtilityFunctions) -> TextMatch:
  """Gets the next token matching a given substring after the input match. Tries to match the start
  of a word first."""
  del utilities
  search_text = text[input_match.text_range.end:]
  match = _get_word_start_token_match_after(search_text, modifier.search)
  if match is None:
    match = _get_substring_token_match(search_text, modifier.search)
  if match is None:
    raise ValueError(
        f"No match for substring after input match: {input_match}. Substring: {modifier.search}")
  return _maybe_add_token_deletion_range(text, input_match.text_range.end + match.start,
                                         input_match.text_range.end + match.end)


def _apply_word_substring_previous_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                            utilities: UtilityFunctions) -> TextMatch:
  """Gets the previous token matching a given substring before the input match. Tries to match the
  start of a word first."""
  del utilities
  search_text = text[:input_match.text_range.start][::-1]
  match = _get_word_start_token_match_before(search_text, modifier.search)
  if match is None:
    match = _get_substring_token_match(search_text, modifier.search[::-1])
  if match is None:
    raise ValueError(
        f"No match for substring before input match: {input_match}. Substring: {modifier.search}")
  return _maybe_add_token_deletion_range(text, input_match.text_range.start - match.end,
                                         input_match.text_range.start - match.start)


def _get_phrase_regex_with_expanded_tokens(search: str, get_homophones: Callable[[str],
                                                                                 list[str]]) -> str:
  phrase_regex = get_phrase_regex(search.split(" "), get_homophones)
  return f"{_TOKEN_CHAR}*{phrase_regex}{_TOKEN_CHAR}*"


def _apply_phrase_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                utilities: UtilityFunctions) -> TextMatch:
  """Gets the next matching phrase after the input match."""
  search_text = text[input_match.text_range.end:]
  phrase_regex = _get_phrase_regex_with_expanded_tokens(modifier.search, utilities.get_homophones)
  match = re.search(phrase_regex, search_text, re.IGNORECASE)
  if match is None:
    raise ValueError(f"No phrase found after input match: {input_match}")
  return _maybe_add_token_deletion_range(text, input_match.text_range.end + match.start(),
                                         input_match.text_range.end + match.end())


_MODIFIER_FUNCTIONS = {
    ModifierType.TOKEN_NEXT: _apply_token_next_modifier,
    ModifierType.TOKEN_PREVIOUS: _apply_token_previous_modifier,
    ModifierType.WORD_SUBSTRING_CLOSEST: _apply_word_substring_closest_modifier,
    ModifierType.WORD_SUBSTRING_NEXT: _apply_word_substring_next_modifier,
    ModifierType.WORD_SUBSTRING_PREVIOUS: _apply_word_substring_previous_modifier,
    ModifierType.PHRASE_NEXT: _apply_phrase_next_modifier,
}


def apply_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                   utilities: UtilityFunctions) -> TextMatch:
  """Applies a modifier to the given range and returns the new range."""
  if input_match.text_range.end > len(text):
    raise ValueError(f"Input match beyond end of text: {input_match}")
  if input_match.deletion_range is not None and input_match.deletion_range.end > len(text):
    raise ValueError(f"Input match deletion range beyond end of text: {input_match}")

  # Apply the modifier the requested number of times.
  result = input_match
  for _ in range(0, modifier.repeat):
    result = _MODIFIER_FUNCTIONS[modifier.modifier_type](text, result, modifier, utilities)
    # No modifier is allowed to match outside the text.
    assert result.text_range.end <= len(text)
    assert result.deletion_range is None or result.deletion_range.end <= len(text)
  return result
