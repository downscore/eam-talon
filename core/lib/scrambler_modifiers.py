"""Modifiers that can be applied to text ranges. Used to find regions of text for navigation and
modification."""

import re
from typing import Callable, Optional, Sequence
from .scrambler_types import Modifier, ModifierType, TextMatch, TextRange, UtilityFunctions

# Regexes for matching a token. Note: \w includes underscores.
_TOKEN_CHAR = r"\w"  # Determines which characters are allowed in a token.
_NON_TOKEN_CHAR = r"[^\w]"
_REGEX_TOKEN: re.Pattern = re.compile(_TOKEN_CHAR + r"+", re.IGNORECASE)

_OPEN_BRACKETS = ["(", "[", "{", "<"]
_CLOSE_BRACKETS = [")", "]", "}", ">"]
_BRACKET_PAIRS = dict(zip(_OPEN_BRACKETS, _CLOSE_BRACKETS))
_SENTENCE_DELIMITERS = [".", "!", "?", "\n"]


def get_phrase_regex(words: Sequence[str], get_homophones: Callable[[str], list[str]]) -> str:
  """Get a regex for matching the given phrase. Expands with homophones using `get_homophones`:
  Given a word, the function should return a list containing the word and its homophones."""
  alts = []
  for word in words:
    # Get all homophones in lowercase and escaped for use in a regex.
    phones = list(map(lambda w: re.escape(w.lower()).replace("\n", "\\n"), get_homophones(word)))
    phones_alt = ""
    if len(phones) > 1:
      phones_alt = f"({'|'.join(phones)})"  # pylint: disable=inconsistent-quotes
    elif len(phones) == 1:
      phones_alt = phones[0]
    if len(phones_alt) > 0:
      alts.append(phones_alt)
  return r"[ .,\-\_\"]*".join(alts)


def _make_match(start: int, end: int) -> TextMatch:
  """Match a text match using a single range."""
  return TextMatch(TextRange(start, end))


def _get_line_at_index(text: str, index: int, include_trailing_line_break: bool) -> TextRange:
  """Get the line containing the given index."""
  start_index = index
  while start_index > 0 and text[start_index - 1] != "\n":
    start_index -= 1
  end_index = index
  while end_index < len(text) and text[end_index] != "\n":
    end_index += 1
  if include_trailing_line_break and end_index < len(text) and text[end_index] == "\n":
    end_index += 1
  return TextRange(start_index, end_index)


def _index_of_next_character(text: str, index: int, characters: list[str]):
  """Given an index in some text, get the index after the next instance of any of the given
  characters."""
  while index < len(text) and text[index] not in characters:
    index += 1
  return index


def _index_of_previous_character(text: str, index: int, characters: list[str]):
  """Given an index in some text, get the index before the last instance of any of the given
  characters."""
  while index > 0 and (index == len(text) or text[index] not in characters):
    index -= 1
  return index


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
  # If the query begins with a non-token character, do not expand to full tokens.
  if len(search) > 0 and re.match(_NON_TOKEN_CHAR, search[0]):
    word_start_regex_text = f"(^|{_NON_TOKEN_CHAR})({re.escape(search)})"
  else:
    word_start_regex_text = f"(^|{_NON_TOKEN_CHAR})({re.escape(search)}{_TOKEN_CHAR}*)"

  word_start_regex = re.compile(word_start_regex_text, re.IGNORECASE)
  match = word_start_regex.search(search_text)
  if match is None:
    return None
  start, end = match.span(2)
  return TextRange(start, end)


def _get_word_start_token_match_before(search_text: str, search: str) -> Optional[TextRange]:
  """Tries to find a token starting with the given substring, searching reversed text."""
  # Use a reversed search regex as the search text should also be reversed.
  # If the query begins with a non-token character, do not expand to full tokens.
  if len(search) > 0 and re.match(_NON_TOKEN_CHAR, search[0]):
    word_start_regex_text = f"({re.escape(search[::-1])})($|{_NON_TOKEN_CHAR})"
  else:
    word_start_regex_text = f"({_TOKEN_CHAR}*{re.escape(search[::-1])})($|{_NON_TOKEN_CHAR})"

  word_start_regex = re.compile(word_start_regex_text, re.IGNORECASE)
  match = word_start_regex.search(search_text)
  if match is None:
    return None
  start, end = match.span(1)
  return TextRange(start, end)


def _get_substring_token_match(search_text: str, search: str) -> Optional[TextRange]:
  """Tries to find a token containing the given substring."""
  # If the query begins with a non-token character, do not expand to full tokens.
  if len(search) > 0 and re.match(_NON_TOKEN_CHAR, search[0]):
    substring_regex_text = re.escape(search)
  else:
    substring_regex_text = f"{_TOKEN_CHAR}*{re.escape(search)}{_TOKEN_CHAR}*"

  substring_regex = re.compile(substring_regex_text, re.IGNORECASE)
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


def _apply_exact_word_closest_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                       utilities: UtilityFunctions) -> TextMatch:
  """Gets the closest exact matching word."""
  del utilities
  search_text_forward = text[input_match.text_range.end:]
  search_text_backward = text[:input_match.text_range.start][::-1]
  regex_forward = re.compile(f"\\b{re.escape(modifier.search)}\\b", re.IGNORECASE)
  regex_backward = re.compile(f"\\b{re.escape(modifier.search[::-1])}\\b", re.IGNORECASE)
  match_forward = regex_forward.search(search_text_forward)
  match_backward = regex_backward.search(search_text_backward)
  if match_forward is None and match_backward is None:
    raise ValueError(f"No exact match found: {modifier.search}")

  forward_result = match_backward is None or (match_forward is not None and
                                              match_forward.start() < match_backward.start())
  if forward_result:
    assert match_forward is not None
    return _maybe_add_token_deletion_range(text, input_match.text_range.end + match_forward.start(),
                                           input_match.text_range.end + match_forward.end())
  assert match_backward is not None
  return _maybe_add_token_deletion_range(text, input_match.text_range.start - match_backward.end(),
                                         input_match.text_range.start - match_backward.start())


def _apply_exact_word_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                    utilities: UtilityFunctions) -> TextMatch:
  """Gets the next exact matching word after the input match."""
  del utilities
  search_text = text[input_match.text_range.end:]
  regex = re.compile(f"\\b{re.escape(modifier.search)}\\b", re.IGNORECASE)
  match = regex.search(search_text)
  if match is None:
    raise ValueError(f"No exact match found after input match: {input_match}")
  return _maybe_add_token_deletion_range(text, input_match.text_range.end + match.start(),
                                         input_match.text_range.end + match.end())


def _apply_exact_word_previous_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                        utilities: UtilityFunctions) -> TextMatch:
  """Gets the previous exact matching word before the input match."""
  del utilities
  search_text = text[:input_match.text_range.start][::-1]
  regex = re.compile(f"\\b{re.escape(modifier.search[::-1])}\\b", re.IGNORECASE)
  match = regex.search(search_text)
  if match is None:
    raise ValueError(f"No exact match found before input match: {input_match}")
  return _maybe_add_token_deletion_range(text, input_match.text_range.start - match.end(),
                                         input_match.text_range.start - match.start())


def _get_phrase_regex_with_expanded_tokens_reversed(
    search: str, get_homophones: Callable[[str], list[str]]) -> str:
  """Gets a phrase regex with all words reversed."""
  words = search.split(" ")
  alt_sets: list[list[str]] = []
  for word in words:
    # Get all homophones in lowercase and escaped for use in a regex.
    phones = list(map(lambda w: re.escape(w.lower()), get_homophones(word)))
    # Reverse the words.
    for i in range(len(phones)):
      phones[i] = phones[i][::-1].replace("\n", "\\n")
    alt_sets.append(phones)

  # Iterate through alt sets in reverse order.
  reversed_alts = []
  for alt_set in alt_sets[::-1]:
    reversed_alts.append(f"({'|'.join(alt_set[::-1])})")  # pylint: disable=inconsistent-quotes

  phrase_regex = r"[ .,\-\_\"]*".join(reversed_alts)
  return f"{_TOKEN_CHAR}*{phrase_regex}{_TOKEN_CHAR}*"


def _apply_phrase_closest_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                   utilities: UtilityFunctions) -> TextMatch:
  """Gets the closest phrase matching the given words."""
  search_text_forward = text[input_match.text_range.end:]
  search_text_backward = text[:input_match.text_range.start][::-1]
  regex_forward = _get_phrase_regex_with_expanded_tokens(modifier.search, utilities.get_homophones)
  regex_backward = _get_phrase_regex_with_expanded_tokens_reversed(modifier.search,
                                                                   utilities.get_homophones)
  match_forward = re.search(regex_forward, search_text_forward, re.IGNORECASE)
  match_backward = re.search(regex_backward, search_text_backward, re.IGNORECASE)
  if match_forward is None and match_backward is None:
    raise ValueError(f"No match for phrase: {modifier.search}")

  forward_result = match_backward is None or (match_forward is not None and
                                              match_forward.start() < match_backward.start())
  if forward_result:
    assert match_forward is not None
    return _maybe_add_token_deletion_range(text, input_match.text_range.end + match_forward.start(),
                                           input_match.text_range.end + match_forward.end())
  assert match_backward is not None
  return _maybe_add_token_deletion_range(text, input_match.text_range.start - match_backward.end(),
                                         input_match.text_range.start - match_backward.start())


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


def _apply_phrase_previous_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                    utilities: UtilityFunctions) -> TextMatch:
  """Gets the previous matching phrase before the input match."""
  search_text = text[:input_match.text_range.start][::-1]
  phrase_regex = _get_phrase_regex_with_expanded_tokens_reversed(modifier.search,
                                                                 utilities.get_homophones)
  match = re.search(phrase_regex, search_text, re.IGNORECASE)
  if match is None:
    raise ValueError(f"No phrase found before input match: {input_match}")
  return _maybe_add_token_deletion_range(text, input_match.text_range.start - match.end(),
                                         input_match.text_range.start - match.start())


def _apply_comment_modifier(text: str, input_match: TextMatch, modifier,
                            utilities: UtilityFunctions) -> TextMatch:
  """Takes the comment containing the match."""
  del modifier, utilities
  block_comment = False
  start_index = input_match.text_range.start

  # Search for the beginning of the comment.
  while start_index > 0:
    if text[start_index] == "#":
      break
    elif len(text) > start_index + 1 and text[start_index:start_index + 2] == "//":
      break
    elif len(text) > start_index + 1 and text[start_index:start_index + 2] == "/*":
      block_comment = True
      break
    start_index -= 1

  # If no comment start found, return the input match.
  if start_index == 0 and not (text[start_index] == "#" or text[:2] in ["//", "/*"]):
    return input_match

  # Use start of input match to ensure we always take a single line if not a block comment.
  end_index = input_match.text_range.start
  if not block_comment:
    while end_index < len(text) and text[end_index] != "\n":
      end_index += 1
  else:
    while end_index < len(text) - 1:
      if text[end_index:end_index + 2] == "*/":
        end_index += 2
        break
      end_index += 1

  return _make_match(start_index, end_index)


def _apply_argument_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                             utilities: UtilityFunctions) -> TextMatch:
  """Takes the current argument."""
  del modifier, utilities

  if text == "":
    raise ValueError("No text to match.")

  # Find the first argument delimiter before the match. Track close parentheses to handle nested
  # calls.
  start_index = input_match.text_range.start
  close_parentheses = 0
  while start_index > 0:
    if text[start_index - 1] == ")":
      close_parentheses += 1
    elif text[start_index - 1] == "(":
      if close_parentheses == 0:
        break
      close_parentheses -= 1
    elif text[start_index - 1] in (",", ";") and close_parentheses == 0:
      break
    start_index -= 1

  # Deletion range start includes leading whitespace, but remove it from the selection range.
  deletion_start_index = start_index
  while start_index < len(text) and text[start_index] in [" ", "\t", "\n"]:
    start_index += 1

  # Try to include leading comma in deletion range. There are cases where we may not want to delete
  # a leading semicolon, so we ignore semicolons for now.
  found_leading_delimiter = False
  if deletion_start_index > 0 and text[deletion_start_index - 1] in (",", ";"):
    deletion_start_index -= 1
    found_leading_delimiter = True

  # Find the next argument delimiter after the match. Track open parentheses to handle nested calls.
  end_index = input_match.text_range.end
  open_parentheses = 0
  while end_index < len(text):
    if text[end_index] == "(":
      open_parentheses += 1
    elif text[end_index] == ")":
      if open_parentheses == 0:
        break
      open_parentheses -= 1
    elif text[end_index] in (",", ";") and open_parentheses == 0:
      break
    end_index += 1

  # Deletion range end includes trailing whitespace, but remove it from the selection range.
  deletion_end_index = end_index
  while end_index > start_index and text[end_index - 1] in [" ", "\t", "\n"]:
    end_index -= 1

  # If we did not include a leading delimiter in the deletion range, try to find a trailing
  # delimiter.
  if not found_leading_delimiter and deletion_end_index < len(
      text) and text[deletion_end_index] in (",", ";"):
    deletion_end_index += 1
    # Include a whitespace character after the delimiter, if present.
    if deletion_end_index < len(text) and text[deletion_end_index] in [" ", "\t"]:
      deletion_end_index += 1

  return TextMatch(TextRange(start_index, end_index),
                   TextRange(deletion_start_index, deletion_end_index))


def _apply_argument_first_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                   utilities: UtilityFunctions) -> TextMatch:
  """Finds the next function call and takes the first argument from it. Assumes the initial match is
  outside the function call."""
  # Find the start of the next function call. Start looking from the end of the current match.
  paren_index = _index_of_next_character(text, input_match.text_range.end, ["("])
  # Skip over empty function calls: func()
  while paren_index < len(text) - 1 and text[paren_index + 1] == ")":
    paren_index = _index_of_next_character(text, paren_index + 1, ["("])
  paren_index = min(paren_index + 1, len(text))

  # Match the argument after the opening parenthesis.
  return _apply_argument_modifier(text, _make_match(paren_index, paren_index), modifier, utilities)


def _apply_argument_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                  utilities: UtilityFunctions) -> TextMatch:
  """From a match inside an argument, takes the next argument."""
  divider_index = _index_of_next_character(text, input_match.text_range.end, [",", ";"])
  divider_index = min(divider_index + 1, len(text))
  return _apply_argument_modifier(text, _make_match(divider_index + 1, divider_index + 1), modifier,
                                  utilities)


def _apply_argument_previous_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                      utilities: UtilityFunctions) -> TextMatch:
  """From a match inside an argument, takes the previous argument."""
  divider_index = _index_of_previous_character(text, input_match.text_range.start, [",", ";"])
  divider_index = max(divider_index - 1, 0)
  return _apply_argument_modifier(text, _make_match(divider_index, divider_index), modifier,
                                  utilities)


def _apply_function_call_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                  utilities: UtilityFunctions) -> TextMatch:
  """Takes the current function call. Assumes the input match is in the function name, not inside
  the parentheses."""
  del modifier, utilities

  # Find the start of the function call.
  # Try to be permissive and include balanced parentheses to allow complex C++ calls such as:
  # (*obj)->get_thing().field[0].method(arg1, &arg2, arg3);
  start_index = input_match.text_range.start
  nested_parentheses = 0
  while start_index > 0 and (text[start_index - 1].isalnum() or text[start_index - 1]
                             in ("_", ".", "-", ">", "*", "(", ")", "[", "]", ":")):
    if text[start_index - 1] == "(":
      if nested_parentheses == 0:
        break
      nested_parentheses -= 1
    elif text[start_index - 1] == ")":
      nested_parentheses += 1
    start_index -= 1

  # Find the end of the function call. Look for an opening parenthesis after the input match, then
  # its balanced close. Use the input match so we can get the entire call if the input match is in
  # `method` in the  example above.
  end_index = input_match.text_range.end
  nested_parentheses = -1  # Start with -1 to so we stop after closing the first open parenthesis.
  while end_index < len(text):
    if text[end_index] == "(":
      nested_parentheses += 1
    elif text[end_index] == ")":
      if nested_parentheses == 0:
        # Include closing parenthesis.
        end_index += 1
        break
      nested_parentheses -= 1
    end_index += 1

  return _make_match(start_index, end_index)


def _apply_function_call_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                       utilities: UtilityFunctions) -> TextMatch:
  """From inside a function call, takes the next function call."""
  # Find the start of the next function call.
  start_index = _index_of_next_character(text, input_match.text_range.end, ["("])
  # Skip over parens without a function name before them.
  while start_index > 0 and not text[start_index - 1].isalnum():
    start_index = _index_of_next_character(text, start_index + 1, ["("])
  start_index = max(start_index - 1, 0)

  # Match the function call before the opening parenthesis.
  return _apply_function_call_modifier(text, _make_match(start_index, start_index), modifier,
                                       utilities)


def _apply_function_call_previous_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                           utilities: UtilityFunctions) -> TextMatch:
  """From inside a function call, takes the previous function call."""
  # Find the start of the previous function call.
  start_index = _index_of_previous_character(text, input_match.text_range.start, ["("])
  # Skip over parens without a function name before them.
  while start_index > 0 and not text[start_index - 1].isalnum():
    start_index = _index_of_previous_character(text, start_index - 1, ["("])
  start_index = max(start_index - 1, 0)

  # Match the function call before the opening parenthesis.
  return _apply_function_call_modifier(text, _make_match(start_index, start_index), modifier,
                                       utilities)


def _apply_string_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                           utilities: UtilityFunctions) -> TextMatch:
  """Takes the content between symmetric delimiters containing the match. Defaults to C-style
  strings."""
  del utilities
  delimiter = "\"" if not modifier.delimiter else modifier.delimiter
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index - 1] != delimiter:
    start_index -= 1
  end_index = input_match.text_range.end
  while end_index < len(text) and text[end_index] != delimiter:
    end_index += 1

  return _make_match(start_index, end_index)


def _apply_string_first_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                 utilities: UtilityFunctions) -> TextMatch:
  """From outside a string, takes the next string."""
  delimiter = "\"" if not modifier.delimiter else modifier.delimiter

  # Find the start of the next string.
  start_index = _index_of_next_character(text, input_match.text_range.end, [delimiter])
  # Check if the delimiter is tripled, like a docstring or markdown block.
  is_docstring = start_index < len(text) - 2 and text[start_index:start_index + 3] == delimiter * 3
  if is_docstring:
    start_index += 2

  # Start from within the string.
  start_index = min(start_index + 1, len(text))

  return _apply_string_modifier(text, _make_match(start_index, start_index), modifier, utilities)


def _apply_string_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                utilities: UtilityFunctions) -> TextMatch:
  """From inside a string, takes the next string."""
  delimiter = "\"" if not modifier.delimiter else modifier.delimiter

  # Find the end of the current string.
  start_index = _index_of_next_character(text, input_match.text_range.end, [delimiter])
  # Check if the delimiter is tripled, like a docstring or markdown block.
  is_docstring = start_index < len(text) - 2 and text[start_index:start_index + 3] == delimiter * 3
  if is_docstring:
    start_index += 2

  # Start from outside the string.
  start_index = min(start_index + 1, len(text))

  # Find the next string after leaving the current one.
  return _apply_string_first_modifier(text, _make_match(start_index, start_index), modifier,
                                      utilities)


def _apply_string_previous_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                    utilities: UtilityFunctions) -> TextMatch:
  """From inside a string, takes the previous string."""
  delimiter = "\"" if not modifier.delimiter else modifier.delimiter

  # Find the start of the current string.
  index = _index_of_previous_character(text, input_match.text_range.start, [delimiter])
  # Check if the delimiter is tripled, like a docstring or markdown block.
  is_docstring = index > 2 and text[index - 2:index + 1] == delimiter * 3
  if is_docstring:
    index -= 2

  # Move outside the current string.
  index = max(index - 1, 0)

  # Find the end of the previous string.
  index = _index_of_previous_character(text, index, [delimiter])
  # Check if the delimiter is tripled, like a docstring or markdown block.
  is_docstring = index > 2 and text[index - 2:index + 1] == delimiter * 3
  if is_docstring:
    index -= 2

  # Move into the previous string.
  index = max(index - 1, 0)

  # Find the previous string before entering the current one.
  return _apply_string_modifier(text, _make_match(index, index), modifier, utilities)


def _apply_python_scope_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                 utilities: UtilityFunctions) -> TextMatch:
  """Takes the current scope in Python code."""
  del modifier, utilities

  # Find the indentation level of the current or last non-empty line.
  indentation_search_index = input_match.text_range.start
  min_indentation_level = None
  while indentation_search_index >= 0 and min_indentation_level is None:
    line_range = _get_line_at_index(text,
                                    indentation_search_index,
                                    include_trailing_line_break=True)
    line_text = line_range.extract(text)
    # Make sure the line isn't just whitespace.
    if line_text.strip() != "":
      # We found a non-whitespace line. Use its indentation level.
      min_indentation_level = len(line_text) - len(line_text.lstrip())
      break
    # Move to the previous line.
    indentation_search_index = line_range.start - 1

  # Make sure we found an indentation level.
  if min_indentation_level is None:
    raise ValueError("Could not find indentation level for Python scope")

  # Find the start of the current scope.
  start_line_range = _get_line_at_index(text,
                                        input_match.text_range.start,
                                        include_trailing_line_break=True)
  first_non_whitespace_line_range = start_line_range
  while start_line_range.start > 0:
    previous_line_range = _get_line_at_index(text,
                                             start_line_range.start - 1,
                                             include_trailing_line_break=True)
    previous_line_text = previous_line_range.extract(text)
    is_whitespace = previous_line_text.strip() == ""
    # Stop if we find a non-whitespace line with less indentation.
    if not is_whitespace and len(previous_line_text) - len(
        previous_line_text.lstrip()) < min_indentation_level:
      break
    start_line_range = previous_line_range
    if not is_whitespace:
      first_non_whitespace_line_range = start_line_range

  # Find the end of the current scope.
  end_line_range = start_line_range
  last_non_whitespace_line_range = end_line_range
  while end_line_range.end < len(text):
    next_line_range = _get_line_at_index(text, end_line_range.end, include_trailing_line_break=True)
    next_line_text = next_line_range.extract(text)
    is_whitespace = next_line_text.strip() == ""
    # Stop if we find a line with less indentation.
    if not is_whitespace and len(next_line_text) - len(
        next_line_text.lstrip()) < min_indentation_level:
      break
    end_line_range = next_line_range
    if not is_whitespace:
      last_non_whitespace_line_range = end_line_range

  # Return the scope, excluding surrounding lines that are just whitespace.
  return _make_match(first_non_whitespace_line_range.start, last_non_whitespace_line_range.end)


def _apply_c_scope_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                            utilities: UtilityFunctions) -> TextMatch:
  """Takes the current scope in C-style code."""
  del modifier, utilities

  # Find the first opening brace before the match. Keep track of the number of close braces.
  close_braces = 0
  start_index = input_match.text_range.start
  while start_index > 0:
    if text[start_index - 1] == "}":
      close_braces += 1
    elif text[start_index - 1] == "{":
      if close_braces <= 0:
        break
      close_braces -= 1
    start_index -= 1

  # Don't include the newline after the opening brace if present.
  if (start_index < len(text) and text[start_index] == "\n"):
    start_index += 1

  # Find the corresponding closing brace. Keep track of the number of open nested braces.
  open_braces = 0
  end_index = start_index
  while end_index < len(text):
    if text[end_index] == "{":
      open_braces += 1
    elif text[end_index] == "}":
      if open_braces <= 0:
        break
      open_braces -= 1
    end_index += 1

  # Remove indentation before the closing brace.
  while end_index > start_index and text[end_index - 1] in [" ", "\t"]:
    end_index -= 1

  return _make_match(start_index, end_index)


def _apply_sentence_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                             utilities: UtilityFunctions) -> TextMatch:
  """Takes the current sentence. Suitable for English prose."""
  del modifier, utilities

  # Find the end of the previous sentence.
  start_index = input_match.text_range.start
  while start_index > 0:
    if text[start_index - 1] in _SENTENCE_DELIMITERS:
      break
    start_index -= 1

  # Remove leading whitespace from the range.
  while start_index < len(text) and text[start_index] in [" ", "\t", "\n"]:
    start_index += 1

  # Find the end of the current sentence.
  end_index = input_match.text_range.end
  while end_index < len(text):
    if text[end_index] in _SENTENCE_DELIMITERS:
      end_index += 1  # Include the delimiter.
      break
    end_index += 1

  # Prefer to include trailing spaces in the deletion range, as leading spaces may be indentation or
  # other formatting.
  included_trailing_spaces = False
  deletion_end_index = end_index
  # Limit to 2 trailing spaces.
  while deletion_end_index < len(
      text) and text[deletion_end_index] == " " and deletion_end_index - end_index < 2:
    deletion_end_index += 1
    included_trailing_spaces = True

  # Include leading spaces in the deletion range if necessary.
  deletion_start_index = start_index
  if not included_trailing_spaces:
    # Limit to 2 leading spaces.
    while deletion_start_index > 0 and text[deletion_start_index -
                                            1] == " " and start_index - deletion_start_index < 2:
      deletion_start_index -= 1

  return TextMatch(TextRange(start_index, end_index),
                   TextRange(deletion_start_index, deletion_end_index))


def _apply_sentence_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                  utilities: UtilityFunctions) -> TextMatch:
  """Takes the next sentence."""
  end_index = input_match.text_range.end
  # Special case: End of the current sentence is selected.
  if input_match.text_range.length() > 0 and end_index > 0 and text[end_index -
                                                                    1] in _SENTENCE_DELIMITERS:
    return _apply_sentence_modifier(text, _make_match(end_index, end_index), modifier, utilities)
  # Find the end of the sentence.
  end_index = _index_of_next_character(text, input_match.text_range.end, _SENTENCE_DELIMITERS)
  end_index = min(end_index + 1, len(text))
  return _apply_sentence_modifier(text, _make_match(end_index, end_index), modifier, utilities)


def _apply_sentence_previous_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                      utilities: UtilityFunctions) -> TextMatch:
  """Takes the previous sentence."""
  # Find the start of the previous sentence.
  start_index = _index_of_previous_character(text, input_match.text_range.start,
                                             _SENTENCE_DELIMITERS)
  start_index = max(start_index - 1, 0)
  return _apply_sentence_modifier(text, _make_match(start_index, start_index), modifier, utilities)


def _apply_sentence_clause_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                    utilities: UtilityFunctions) -> TextMatch:
  """Expands the match to cover a clause in English prose. Doesn't include leading or trailing
  whitespace in the deletion range"""
  del modifier, utilities
  clause_delimiters = [",", ".", "!", "?", "\n", "(", ")", ":", ";"]

  # Find the end of the previous clause.
  start_index = input_match.text_range.start
  while start_index > 0:
    if text[start_index - 1] in clause_delimiters:
      break
    start_index -= 1

  # Remove leading whitespace from the range.
  while start_index < len(text) and text[start_index] in [" ", "\t", "\n"]:
    start_index += 1

  # Find the end of the current sentence.
  end_index = input_match.text_range.end
  while end_index < len(text):
    if text[end_index] in clause_delimiters:
      break
    end_index += 1

  return TextMatch(TextRange(start_index, end_index))


def _apply_brackets_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                             utilities: UtilityFunctions) -> TextMatch:
  """Takes the contents of surrounding brackets."""
  del modifier, utilities

  # Find the first opening bracket before the match without a matching closing bracket.
  start_index = input_match.text_range.start
  nesting_level_by_bracket = {}
  # Initialize nesting level at zero for all bracket types.
  for bracket in _BRACKET_PAIRS:
    nesting_level_by_bracket[bracket] = 0
  opening_bracket = None
  while start_index > 0:
    c = text[start_index - 1]
    if c in _BRACKET_PAIRS:
      nesting_level_by_bracket[c] -= 1
      if nesting_level_by_bracket[c] < 0:
        opening_bracket = c
        break
    elif c in _BRACKET_PAIRS.values():
      # Get key for value c
      for bracket, close_bracket in _BRACKET_PAIRS.items():
        if close_bracket == c:
          nesting_level_by_bracket[bracket] += 1
          break
    start_index -= 1

  # Make sure we found an opening bracket.
  if opening_bracket is None:
    raise ValueError("Could not find opening bracket")

  # Find the corresponding closing bracket.
  end_index = start_index
  nesting_level = 0
  while end_index < len(text):
    c = text[end_index]
    if c == opening_bracket:
      nesting_level += 1
    elif c == _BRACKET_PAIRS[opening_bracket]:
      if nesting_level == 0:
        break
      nesting_level -= 1
    end_index += 1

  return _make_match(start_index, end_index)


def _apply_brackets_first_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                   utilities: UtilityFunctions) -> TextMatch:
  """From outside a bracket, takes the next bracketed content."""
  # Find the start of the next bracketed content.
  start_index = _index_of_next_character(text, input_match.text_range.end, _OPEN_BRACKETS)
  # Ignore < with a trailing space. It's most likely to be a comparison, not a bracket.
  while 0 < start_index < len(text) - 1 and text[start_index:start_index + 2] == "< ":
    start_index = _index_of_next_character(text, start_index + 1, _OPEN_BRACKETS)
  # Start from within the bracket.
  start_index = min(start_index + 1, len(text))

  return _apply_brackets_modifier(text, _make_match(start_index, start_index), modifier, utilities)


def _apply_brackets_next_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                  utilities: UtilityFunctions) -> TextMatch:
  """From inside a bracket, takes the next bracketed content."""
  # Find the end of the current bracketed content.
  start_index = _index_of_next_character(text, input_match.text_range.end, _CLOSE_BRACKETS)
  # Ignore > with a leading space. It's most likely to be a comparison, not a bracket.
  while 0 < start_index < len(text) and text[start_index - 1:start_index + 1] == " >":
    start_index = _index_of_next_character(text, start_index + 1, _CLOSE_BRACKETS)
  # Start from outside the bracket.
  start_index = min(start_index + 1, len(text))

  # Find the next bracketed content after leaving the current one.
  return _apply_brackets_first_modifier(text, _make_match(start_index, start_index), modifier,
                                        utilities)


def _apply_brackets_previous_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                      utilities: UtilityFunctions) -> TextMatch:
  """From inside a bracket, takes the previous bracketed content."""
  # Find the start of the current bracketed content.
  index = _index_of_previous_character(text, input_match.text_range.start, _OPEN_BRACKETS)
  # Ignore < with a trailing space. It's most likely to be a comparison, not a bracket.
  while 0 < index < len(text) - 1 and text[index:index + 2] == "< ":
    index = _index_of_previous_character(text, index - 1, _OPEN_BRACKETS)
  # Move outside the current bracket.
  index = max(index - 1, 0)

  # Find the end of the previous bracketed content.
  index = _index_of_previous_character(text, index, _CLOSE_BRACKETS)
  # Ignore > with a leading space. It's most likely to be a comparison, not a bracket.
  while 0 < index < len(text) and text[index - 1:index + 1] == " >":
    index = _index_of_previous_character(text, index - 1, _CLOSE_BRACKETS)
  # Move into the previous bracket.
  index = max(index - 1, 0)

  # Find the previous bracketed content before entering the current one.
  return _apply_brackets_modifier(text, _make_match(index, index), modifier, utilities)


def _apply_start_of_line_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                  utilities: UtilityFunctions) -> TextMatch:
  """Takes an empty match at the start of the line containing the match."""
  del modifier, utilities
  line_range = _get_line_at_index(text,
                                  input_match.text_range.start,
                                  include_trailing_line_break=True)
  return _make_match(line_range.start, line_range.start)


def _apply_end_of_line_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                utilities: UtilityFunctions) -> TextMatch:
  """Takes an empty match at the end of the line containing the input match."""
  del modifier, utilities
  line_range = _get_line_at_index(text,
                                  input_match.text_range.start,
                                  include_trailing_line_break=True)
  return _make_match(line_range.end, line_range.end)


def _apply_between_whitespace_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                       utilities: UtilityFunctions) -> TextMatch:
  """Takes the contents of surrounding whitespace (including line breaks)."""
  del modifier, utilities

  delimiters = [" ", "\t", "\n"]

  # Find whitespace before the input match.
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index - 1] not in delimiters:
    start_index -= 1

  # Find whitespace after the input match.
  end_index = input_match.text_range.end
  while end_index < len(text) and text[end_index] not in delimiters:
    end_index += 1

  # Try to include trailing whitespace in the deletion range.
  deletion_end_index = end_index
  included_trailing_whitespace = False
  if deletion_end_index < len(text) and text[deletion_end_index] in delimiters:
    deletion_end_index += 1
    included_trailing_whitespace = True

  # If we couldn't include trailing whitespace, try to include leading whitespace.
  deletion_start_index = start_index
  if not included_trailing_whitespace and deletion_start_index > 0 and text[deletion_start_index -
                                                                            1] in delimiters:
    deletion_start_index -= 1

  return TextMatch(TextRange(start_index, end_index),
                   TextRange(deletion_start_index, deletion_end_index))


def _apply_markdown_link_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                  utilities: UtilityFunctions) -> TextMatch:
  """Takes a full link in markdown syntax, including brackets. Example:
  [link text](http://example.com)"""
  del modifier, utilities

  # Find the start of the link: "["
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index] != "[":
    start_index -= 1

  # Find the end of the link: ")"
  end_index = start_index
  while end_index < len(text) and text[end_index] != ")":
    end_index += 1

  return _make_match(start_index, end_index + 1)


def _apply_markdown_section_end_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                         utilities: UtilityFunctions) -> TextMatch:
  """Takes an empty selection before the line break on the last non-whitespace line in a markdown
  section."""
  del modifier, utilities

  # Regex that matches pound symbols followed by a space.
  heading_regex = re.compile(r"^#+ ", re.IGNORECASE)

  # Search backwards so we can start on a non-whitespace line.
  curr_index = input_match.text_range.end
  while curr_index > 0:
    line_range = _get_line_at_index(text, curr_index, include_trailing_line_break=True)
    line_text = line_range.extract(text)

    if line_text.strip() != "":
      break

    # Move to the previous line.
    curr_index = line_range.start - 1

  # Move through the text line by line.
  is_first_line = True
  result_index = curr_index
  while curr_index < len(text):
    line_range = _get_line_at_index(text, curr_index, include_trailing_line_break=True)
    line_text = line_range.extract(text)

    # Ignore headings on the first line, otherwise terminate the search when we see a heading.
    if not is_first_line and heading_regex.match(line_text):
      break

    # If this line is not just whitespace, update the result index.
    if line_text.strip() != "":
      result_index = max(line_range.start,
                         line_range.end - 1 if line_text.endswith("\n") else line_range.end)

    # Move to the next line.
    curr_index = line_range.end
    is_first_line = False

  return _make_match(result_index, result_index)


def _apply_line_including_line_break_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                              utilities: UtilityFunctions) -> TextMatch:
  """Takes the line containing the match."""
  del modifier, utilities
  line_range = _get_line_at_index(text,
                                  input_match.text_range.start,
                                  include_trailing_line_break=True)
  return TextMatch(line_range)


def _apply_line_excluding_line_break_modifier(text: str, input_match: TextMatch, modifier: Modifier,
                                              utilities: UtilityFunctions) -> TextMatch:
  """Takes the line containing the match."""
  del modifier, utilities
  line_range = _get_line_at_index(text,
                                  input_match.text_range.start,
                                  include_trailing_line_break=False)
  return TextMatch(line_range)


_MODIFIER_FUNCTIONS = {
    ModifierType.TOKEN_NEXT: _apply_token_next_modifier,
    ModifierType.TOKEN_PREVIOUS: _apply_token_previous_modifier,
    ModifierType.WORD_SUBSTRING_CLOSEST: _apply_word_substring_closest_modifier,
    ModifierType.WORD_SUBSTRING_NEXT: _apply_word_substring_next_modifier,
    ModifierType.WORD_SUBSTRING_PREVIOUS: _apply_word_substring_previous_modifier,
    ModifierType.EXACT_WORD_CLOSEST: _apply_exact_word_closest_modifier,
    ModifierType.EXACT_WORD_NEXT: _apply_exact_word_next_modifier,
    ModifierType.EXACT_WORD_PREVIOUS: _apply_exact_word_previous_modifier,
    ModifierType.PHRASE_CLOSEST: _apply_phrase_closest_modifier,
    ModifierType.PHRASE_NEXT: _apply_phrase_next_modifier,
    ModifierType.PHRASE_PREVIOUS: _apply_phrase_previous_modifier,
    ModifierType.COMMENT: _apply_comment_modifier,
    ModifierType.ARGUMENT: _apply_argument_modifier,
    ModifierType.ARGUMENT_FIRST: _apply_argument_first_modifier,
    ModifierType.ARGUMENT_NEXT: _apply_argument_next_modifier,
    ModifierType.ARGUMENT_PREVIOUS: _apply_argument_previous_modifier,
    ModifierType.FUNCTION_CALL: _apply_function_call_modifier,
    ModifierType.FUNCTION_CALL_NEXT: _apply_function_call_next_modifier,
    ModifierType.FUNCTION_CALL_PREVIOUS: _apply_function_call_previous_modifier,
    ModifierType.STRING: _apply_string_modifier,
    ModifierType.STRING_FIRST: _apply_string_first_modifier,
    ModifierType.STRING_NEXT: _apply_string_next_modifier,
    ModifierType.STRING_PREVIOUS: _apply_string_previous_modifier,
    ModifierType.PYTHON_SCOPE: _apply_python_scope_modifier,
    ModifierType.C_SCOPE: _apply_c_scope_modifier,
    ModifierType.SENTENCE: _apply_sentence_modifier,
    ModifierType.SENTENCE_NEXT: _apply_sentence_next_modifier,
    ModifierType.SENTENCE_PREVIOUS: _apply_sentence_previous_modifier,
    ModifierType.SENTENCE_CLAUSE: _apply_sentence_clause_modifier,
    ModifierType.BRACKETS: _apply_brackets_modifier,
    ModifierType.BRACKETS_FIRST: _apply_brackets_first_modifier,
    ModifierType.BRACKETS_NEXT: _apply_brackets_next_modifier,
    ModifierType.BRACKETS_PREVIOUS: _apply_brackets_previous_modifier,
    ModifierType.START_OF_LINE: _apply_start_of_line_modifier,
    ModifierType.END_OF_LINE: _apply_end_of_line_modifier,
    ModifierType.BETWEEN_WHITESPACE: _apply_between_whitespace_modifier,
    ModifierType.MARKDOWN_LINK: _apply_markdown_link_modifier,
    ModifierType.MARKDOWN_SECTION_END: _apply_markdown_section_end_modifier,
    ModifierType.LINE_INCLUDING_LINE_BREAK: _apply_line_including_line_break_modifier,
    ModifierType.LINE_EXCLUDING_LINE_BREAK: _apply_line_excluding_line_break_modifier,
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
