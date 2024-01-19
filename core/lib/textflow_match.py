"""Code for matching tokens inside text."""

import re
from typing import Callable, Optional, Tuple
from .textflow_types import SearchDirection, TextMatch, TextRange, TokenMatchMethod, TokenMatchOptions

# Regex for matching a token.
_REGEX_TOKEN: re.Pattern = re.compile(r"[\w\-_]+")

# Single character regex for matching alphanumeric characters and separators.
_REGEX_TOKEN_CHAR: re.Pattern = re.compile(r"[\w\-_']", re.IGNORECASE)


def tuple_to_text_match(range_tuple: Tuple[int, int]) -> TextMatch:
  return TextMatch(text_range=TextRange(range_tuple[0], range_tuple[1]))


def make_text_match(start: int, end: int) -> TextMatch:
  return TextMatch(text_range=TextRange(start, end))


def get_word_regex(word: str) -> str:
  """Get a regex for matching the given word exactly."""
  return r"\b" + re.escape(word) + r"\b"


def get_phrase_regex(words: list[str], get_homophones: Callable[[str], list[str]]) -> str:
  """Get a regex for matching the given phrase. Expands with homophones using `get_homophones`: Given a word, the
  function should return a list containing the word and its homophones."""
  alts = []
  for word in words:
    # Get all homophones in lowercase and escaped for use in a regex.
    phones = list(map(lambda w: re.escape(w.lower()), get_homophones(word)))
    phones_alt = ""
    if len(phones) > 1:
      phones_alt = f"({'|'.join(phones)})".format()
    elif len(phones) == 1:
      phones_alt = phones[0]
    if len(phones_alt) > 0:
      alts.append(phones_alt)
  return r"[ .,\-\_\"]*".join(alts)


def get_nth_regex_match(text: str, regex: re.Pattern, n: int, direction: SearchDirection) -> Optional[re.Match]:
  """Get the nth (1-based) match of a regex in the given text. Returns None if there is no nth match."""
  if n < 1:
    raise ValueError("n must be at least 1")

  matches = list(regex.finditer(text))
  if len(matches) < n:
    return None

  if direction == SearchDirection.BACKWARD:
    return matches[-n]
  return matches[n - 1]


def get_nth_substring_match(text: str, search: str, n: int, direction: SearchDirection) -> Optional[re.Match]:
  """Get the nth (1-based) match of a substring in the given text. Returns None if there is no nth match."""
  return get_nth_regex_match(text, re.compile(re.escape(search), re.IGNORECASE), n, direction)


def get_nth_word_start_match(text: str, search: str, n: int, direction: SearchDirection) -> Optional[TextMatch]:
  """Matches the given substring to the start of a word in the given text. Returns None if no match was found."""
  # No match for empty string.
  if len(search) == 0:
    return None

  # If the search string starts with a symbol (besides underscore), don't look for the start of a word.
  # Underscore is exempt because it is often used to start symbol names in code.
  if not search[0].isalnum() and search[0] != "_":
    result = get_nth_substring_match(text, search, n, direction)
    if result is None:
      return None
    return tuple_to_text_match(result.span())

  # Create a regex from the substring that only matches that start of words. Match is case insensitive.
  # Note: First capture group will match a single character if it is not at the start of the line.
  # Note: Underscores do not separate words.
  regex = re.compile(r"(^|[^a-z0-9_])" + re.escape(search), re.IGNORECASE)
  match = get_nth_regex_match(text, regex, n, direction)
  if match is None:
    return None
  return make_text_match(match.start() + len(match.group(1)), match.end())


def get_nth_line_start_match(text: str, search: str, n: int, direction: SearchDirection) -> Optional[TextMatch]:
  """Matches the given substring to the start of a line in the given text. Returns None if no match was found."""
  # No match for empty string.
  if len(search) == 0:
    return None
  # Create a regex from the substring that only matches that start of words. Match is case insensitive.
  # Note: First capture group will match a single character if it is not at the start of the line.
  regex = re.compile(r"^([ \t]*)" + re.escape(search), re.IGNORECASE | re.MULTILINE)
  match = get_nth_regex_match(text, regex, n, direction)
  if match is None:
    return None
  return make_text_match(match.start() + len(match.group(1)), match.end())


def expand_match_to_token(text: str, match: TextMatch) -> TextMatch:
  """Expands the given match to cover a whole token. Extends to either side until a non-alphanumeric, non-separator
  char or string end is encountered. Note: Does not treat dots as a separator. Each "word" in "word.word.word" is a
  token."""
  if match.text_range.end > len(text):
    raise ValueError("Match out of bounds of given text.")
  start = match.text_range.start
  end = match.text_range.end
  empty_match = start == end
  # Do not expand to the left if we have a match starting on a non-token character.
  if empty_match or _REGEX_TOKEN_CHAR.match(text[start]) is not None:
    while start > 0:
      if _REGEX_TOKEN_CHAR.match(text[start - 1]) is None:
        break
      start -= 1
  # Do not expand to the right if we have a match ending on a non-token character.
  if empty_match or _REGEX_TOKEN_CHAR.match(text[end - 1]) is not None:
    while end < len(text):
      if _REGEX_TOKEN_CHAR.match(text[end]) is None:
        break
      end += 1
  return make_text_match(start, end)


def maybe_add_deletion_range(text: str, match: TextMatch) -> TextMatch:
  """Adds a deletion range to the given match if there is a comma, space, or similar following the token."""
  if match.text_range.end >= len(text):
    return match

  # Check if there is ", " following the token.
  if match.text_range.end + 1 < len(text) and text[match.text_range.end] == "," and text[match.text_range.end + 1] == " ":
    return TextMatch(text_range=match.text_range, deletion_range=TextRange(match.text_range.start, match.text_range.end + 2))

  # Check for space or comma.
  if text[match.text_range.end] in (" ", ","):
    return TextMatch(text_range=match.text_range, deletion_range=TextRange(match.text_range.start, match.text_range.end + 1))

  # The deletion range would be the same as the text range, so do not include it.
  return TextMatch(text_range=match.text_range)


def _match_token_partial(text: str, options: TokenMatchOptions, direction: SearchDirection,
                         get_homophones: Callable[[str], list[str]]) -> Optional[TextMatch]:
  """Finds a partial (may be full) match for a token in the given text using the given options. Returns the range or
  None if a matching token could not be found."""
  # Handle matching by token count or current cursor.
  if options.match_method == TokenMatchMethod.TOKEN_COUNT:
    count_match = get_nth_regex_match(text, _REGEX_TOKEN, options.nth_match, direction)
    if count_match is not None:
      return tuple_to_text_match(count_match.span())
    return None

  # Handle matching by phrase.
  if options.match_method == TokenMatchMethod.PHRASE:
    regex = get_phrase_regex(options.search.split(" "), get_homophones)
    phrase_match = get_nth_regex_match(text, re.compile(regex, re.IGNORECASE), options.nth_match, direction)
    if phrase_match is not None:
      return tuple_to_text_match(phrase_match.span())
    return None

  # Handle matching by line start.
  if options.match_method == TokenMatchMethod.LINE_START:
    return get_nth_line_start_match(text, options.search, options.nth_match, direction)

  # Handle matching by exact word.
  if options.match_method == TokenMatchMethod.EXACT_WORD:
    regex = get_word_regex(options.search)
    word_match = get_nth_regex_match(text, re.compile(regex, re.IGNORECASE), options.nth_match, direction)
    if word_match is not None:
      return tuple_to_text_match(word_match.span())
    return None

  # Handle matching by word start.
  if options.match_method in (TokenMatchMethod.WORD_START, TokenMatchMethod.WORD_START_THEN_SUBSTRING):
    start_match = get_nth_word_start_match(text, options.search, options.nth_match, direction)
    if start_match is not None or options.match_method == TokenMatchMethod.WORD_START:
      return start_match

  # Handle matching by word substring.
  substr_match = get_nth_substring_match(text, options.search, options.nth_match, direction)
  if substr_match is not None:
    return tuple_to_text_match(substr_match.span())
  return None


def match_token(text: str, options: TokenMatchOptions, direction: SearchDirection,
                get_homophones: Callable[[str], list[str]]) -> Optional[TextMatch]:
  """Matches a token in the given text using the given options. Returns the match range or None if a matching token
  could not be found.
  `get_homophones`: Used for homophone expansion when matching by phrase. Given a word, the function should return a
  list containing the word and its homophones."""
  partial_match = _match_token_partial(text, options, direction, get_homophones)
  if partial_match is None:
    return None
  expanded_match = expand_match_to_token(text, partial_match)
  return maybe_add_deletion_range(text, expanded_match)
