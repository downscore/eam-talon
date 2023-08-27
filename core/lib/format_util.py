"""Utils to support formatting text by changing word segmentation, capitalization, etc."""

from dataclasses import dataclass
from enum import Enum, unique
import re
from typing import Tuple

# Words that remain lowercase in title case.
_WORDS_TO_KEEP_LOWERCASE = [
    "a", "an", "the", "at", "by", "for", "in", "is", "of", "on", "to", "up", "and", "as", "but", "or", "nor"
]

# Regexes for deciding if two strings require a space between them.
_NO_SPACE_AFTER_REGEX = re.compile(
    r"""
  (?:
    [\s\-_/#@([{‘“]     # Characters that never need space after them.
  | (?<!\w)[$£€¥₩₽₹]    # Currency symbols not preceded by a word character.
  # Quotes preceded by beginning of string, space, opening braces, dash, or other quotes.
  | (?: ^ | [\s([{\-'"] ) ['"]
  )$""", re.VERBOSE)
_NO_SPACE_BEFORE_REGEX = re.compile(
    r"""
  ^(?:
    [\s\-_.,!?;:/%)\]}’”]   # Characters that never need space before them.
  | [$£€¥₩₽₹](?!\w)         # Currency symbols not followed by a word character.
  # Quotes followed by end of string, space, closing braces, dash, other quotes, or some punctuation.
  | ['"] (?: $ | [\s)\]}\-'".,!?;:/] )
  )""", re.VERBOSE)


@unique
class WordCapitalization(Enum):
  """Methods of capitalizing a word."""
  NO_CHANGE = 1
  LOWERCASE = 2
  UPPERCASE = 3
  CAPITALIZE_FIRST = 4  # Always capitalize the first letter.
  TITLE_CASE = 5  # Capitalize first letter unless it is a word to keep lowercase.
  CAPITALIZE_FIRST_PRESERVE_FOLLOWING = 6  # Always capitalize the first letter, preserve case of following letters.
  TITLE_CASE_PRESERVE_FOLLOWING = 7  # Title case, but only potentially modifies the first letter of a word.


@unique
class Formatters(Enum):
  """Types of available formatters."""
  IDENTITY = 1
  LOWERCASE = 2
  UPPERCASE = 3
  SENTENCE = 4
  TITLE_CASE = 5
  TITLE_CASE_ALL = 6  # All words (including "a", "in", etc.) will have their first letter capitalized.
  NO_SPACES = 7
  DOT_SEPARATED = 8
  SLASH_SEPARATED = 9
  DOUBLE_COLON_SEPARATED = 10
  KEBAB = 11
  SNAKE = 12
  PASCAL = 13
  CAMEL = 14
  ENUM = 15
  SPACE_SURROUNDED = 16


@unique
class CharacterType(Enum):
  """Character classes."""
  OTHER = 1  # Includes whitespace and symbols.
  LOWERCASE = 2
  UPPERCASE = 3
  DIGIT = 4


@dataclass
class FormatOptions:
  """Options for formatting a phrase. Defaults to no change."""
  # How to capitalize the first word.
  first_capitalization: WordCapitalization = WordCapitalization.NO_CHANGE
  # How to capitalize all words after the first.
  rest_capitalization: WordCapitalization = WordCapitalization.NO_CHANGE
  # Separator between words.
  separator: str = " "
  # String to surround the result with.
  surround: str = ""


def get_format_options(formatters: list[Formatters]) -> FormatOptions:
  """Get combined options for a list of formatters. Order is important for formatters that set the same options."""
  result = FormatOptions()
  for formatter in formatters:
    # Replace this with "match" when Python 3.10+ supported by Talon.
    if formatter == Formatters.LOWERCASE:
      result.first_capitalization = WordCapitalization.LOWERCASE
      result.rest_capitalization = WordCapitalization.LOWERCASE
    elif formatter == Formatters.UPPERCASE:
      result.first_capitalization = WordCapitalization.UPPERCASE
      result.rest_capitalization = WordCapitalization.UPPERCASE
    elif formatter == Formatters.SENTENCE:
      result.first_capitalization = WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
      result.rest_capitalization = WordCapitalization.NO_CHANGE
    elif formatter == Formatters.TITLE_CASE:
      result.first_capitalization = WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
      result.rest_capitalization = WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING
    elif formatter == Formatters.TITLE_CASE_ALL:
      result.first_capitalization = WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
      result.rest_capitalization = WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
    elif formatter == Formatters.NO_SPACES:
      result.separator = ""
    elif formatter == Formatters.DOT_SEPARATED:
      result.separator = "."
    elif formatter == Formatters.SLASH_SEPARATED:
      result.separator = "/"
    elif formatter == Formatters.DOUBLE_COLON_SEPARATED:
      result.separator = "::"
    elif formatter == Formatters.KEBAB:
      result.separator = "-"
    elif formatter == Formatters.SNAKE:
      result.first_capitalization = WordCapitalization.LOWERCASE
      result.rest_capitalization = WordCapitalization.LOWERCASE
      result.separator = "_"
    elif formatter == Formatters.PASCAL:
      result.first_capitalization = WordCapitalization.CAPITALIZE_FIRST
      result.rest_capitalization = WordCapitalization.CAPITALIZE_FIRST
      result.separator = ""
    elif formatter == Formatters.CAMEL:
      result.first_capitalization = WordCapitalization.LOWERCASE
      result.rest_capitalization = WordCapitalization.CAPITALIZE_FIRST
      result.separator = ""
    elif formatter == Formatters.ENUM:
      result.first_capitalization = WordCapitalization.UPPERCASE
      result.rest_capitalization = WordCapitalization.UPPERCASE
      result.separator = "_"
    elif formatter == Formatters.SPACE_SURROUNDED:
      result.surround = " "

  return result


def format_word_capitalization(word: str, capitalization: WordCapitalization) -> str:
  """Outputs the given word with the given capitalization style."""
  if " " in word:
    raise ValueError("Word cannot contain spaces")

  # Replace this with "match" when Python 3.10+ supported by Talon.
  if capitalization == WordCapitalization.LOWERCASE:
    return word.lower()
  if capitalization == WordCapitalization.UPPERCASE:
    return word.upper()
  if capitalization == WordCapitalization.CAPITALIZE_FIRST:
    return word.capitalize()
  if capitalization == WordCapitalization.TITLE_CASE:
    word_lower = word.lower()
    return word.capitalize() if word_lower not in _WORDS_TO_KEEP_LOWERCASE else word_lower
  if capitalization == WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING:
    return word if len(word) == 0 else word[0].upper() + word[1:]
  if capitalization == WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING:
    if len(word) == 0:
      return word
    word_lower = word.lower()
    return word[0].upper() + word[1:] if word_lower not in _WORDS_TO_KEEP_LOWERCASE else word_lower
  # Default for NO_CHANGE.
  return word


def format_phrase(phrase: str, options: FormatOptions) -> str:
  """Returns the given phrase formatted with the given options."""
  result_words: list[str] = []
  words = phrase.strip().split(" ")
  for i, word in enumerate(words):
    if i == 0:
      result_words.append(format_word_capitalization(word, options.first_capitalization))
    else:
      result_words.append(format_word_capitalization(word, options.rest_capitalization))
  return options.surround + options.separator.join(result_words) + options.surround


def title_format_phrase(phrase: str) -> str:
  """Returns the given phrase formatted as a title."""
  # Find hyphens and remember their locations, then replace them with spaces.
  hyphen_indexes = []
  for i, c in enumerate(phrase):
    if c == "-":
      hyphen_indexes.append(i)
  phrase_processed = phrase.replace("-", " ")

  # Format as title case.
  options = FormatOptions()
  options.first_capitalization = WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
  options.rest_capitalization = WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING
  formatted = format_phrase(phrase_processed, options)

  # Restore hyphens.
  for index in hyphen_indexes:
    formatted = formatted[:index] + "-" + formatted[index + 1:]

  return formatted


def unformat_phrase(phrase: str) -> str:
  """Takes a formatted phrase and tries to return an unformatted version.
  Splits on case or character class changes. Output is always lowercase."""
  # Replace symbols with spaces. Don't include hyphens - this will not work for kebab-case.
  unformatted = re.sub(r"[^a-zA-Z0-9\-]+", " ", phrase)
  # Split on camel/pascal casing. Include numbers.
  unformatted = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-zA-Z])(?=[0-9])|(?<=[0-9])(?=[a-zA-Z])",
                       " ", unformatted)
  unformatted = unformatted.lower()
  return unformatted


def needs_space_between(before: str, after: str) -> bool:
  # Special case: ordinals.
  if before.endswith("1") and after == "st":
    return False
  if before.endswith("2") and after == "nd":
    return False
  if before.endswith("3") and after == "rd":
    return False
  if len(before) > 0 and before[-1] in ["4", "5", "6", "7", "8", "9", "0"] and after == "th":
    return False

  return (before != "" and after != "" and _NO_SPACE_AFTER_REGEX.search(before) is None and
          _NO_SPACE_BEFORE_REGEX.search(after) is None)


def auto_capitalize(text: str) -> str:
  """Auto-capitalize some text based on punctuation and line breaks."""
  result = ""
  capitalize_next = False
  last_was_newline = False
  for i, c in enumerate(text):
    # Sentence endings and double newlines cause the next alphanumeric character to be capitalized.
    if c in ".!?" or (last_was_newline and c == "\n"):
      if i < len(text) - 1 and c == "." and text[i + 1:].isalpha():  # Check if this looks like a file extension.
        capitalize_next = False  # Don't capitalize file extensions.
      else:
        capitalize_next = True
    # Alphanumeric characters and commas/colons absorb capitalize_next and try to capitalize. For numbers and
    # punctuation this does nothing, which is what we want.
    elif capitalize_next and (c.isalnum() or c in ",:"):
      capitalize_next = False
      c = c.capitalize()

    result += c
    last_was_newline = c == "\n"
  return result


def guess_capitalization(word: str) -> WordCapitalization:
  """Guess the capitalization of a given word."""
  stripped = word.strip()
  if len(stripped) == 0:
    raise ValueError("Word cannot be empty.")
  if " " in stripped:
    raise ValueError("Input must be a single word.")
  # If the first character is lowercase or non-alphabetic, we guess the word is lowercase.
  if stripped[0].islower() or not stripped[0].isalpha():
    return WordCapitalization.LOWERCASE
  # The first letter is uppercase. Check if there are any others.
  multiple_uppercase = False
  for c in stripped[1:]:
    if c.isupper():
      multiple_uppercase = True
      break
  # If the word has only one capitalized letter (includes case where word is a single uppercase letter), guess title
  # case.
  if not multiple_uppercase:
    return WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
  if all(c.isupper() or not c.isalpha() for c in stripped):
    # There are at least two uppercase letters and no lowercase letters. There may be numbers and symbols.
    return WordCapitalization.UPPERCASE
  return WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING


def get_fragment_ranges(token: str) -> list[Tuple[int, int]]:
  """Get a list of ranges of individual fragments in a camel/pascal/snake-cased token."""
  result = []
  start_index = 0
  last_character_type = CharacterType.OTHER
  for index, c in enumerate(token):
    # Get current character type.
    current_character_type = CharacterType.OTHER
    if c.isnumeric():
      current_character_type = CharacterType.DIGIT
    elif c.isalpha() and c.isupper():
      current_character_type = CharacterType.UPPERCASE
    elif c.isalpha():
      current_character_type = CharacterType.LOWERCASE

    type_changed = last_character_type != current_character_type
    if last_character_type == CharacterType.OTHER and current_character_type != CharacterType.OTHER:
      start_index = index
    elif type_changed and not (last_character_type == CharacterType.UPPERCASE and
                               current_character_type == CharacterType.LOWERCASE):
      result.append((start_index, index))
      start_index = index

    last_character_type = current_character_type

  # Handle case where token ends on a fragment.
  if last_character_type != CharacterType.OTHER:
    result.append((start_index, len(token)))

  return result
