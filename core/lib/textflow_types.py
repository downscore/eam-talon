"""TextFlow API types."""

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Callable, Optional


@unique
class SearchDirection(Enum):
  """Directions for searching through text."""
  FORWARD = 1
  BACKWARD = 2


@dataclass(frozen=True)
class TextRange:
  """A range of characters in some text. May have zero length (start == end), in which case it
  represents a cursor position (empty selection). This class is intended to be immutable."""
  start: int = 0
  end: int = 0

  def __init__(self, start: int, end: int):
    if start < 0 or end < start:
      raise ValueError(f"Invalid range: {start}-{end}")
    if end > 100000000:
      raise ValueError(f"End value too large: {end}")
    object.__setattr__(self, "start", start)
    object.__setattr__(self, "end", end)

  def length(self):
    """Returns the length of this range. Non negative, zero if start and end positions are the
    same."""
    return self.end - self.start

  def extract(self, text: str) -> str:
    """Extracts this range from the given text and returns it."""
    if len(text) < self.end:
      raise ValueError("Tried to extract range beyond end of text")
    return text[self.start:self.end]


@dataclass
class TextMatch:
  """A text range matched by a target or modifier. Includes extra metadata to help with text
  manipulation."""
  # The range that was matched.
  text_range: TextRange
  # Optional text range to use when deleting the match. May include comma and space separators, etc.
  deletion_range: Optional[TextRange] = None


@unique
class TokenMatchMethod(Enum):
  """Methods of matching a token."""
  # Match only the start of a word.
  WORD_START = 1
  # Match a word substring. No preference given to the start of a word.
  WORD_SUBSTRING = 2
  # Try to match the start of a word. If that fails, match a substring.
  WORD_START_THEN_SUBSTRING = 3
  # Match the start of a line (like `WORD_START` for the first word in each line). Ignores
  # indentation.
  LINE_START = 4
  # Match by counting tokens (e.g. 3rd last token before the cursor).
  TOKEN_COUNT = 5
  # Match by a text phrase with homophone expansion.
  PHRASE = 6
  # Match by an exact word (case insensitive).
  EXACT_WORD = 7
  # Matches LINE_START, then falls back to WORD_START_THEN_SUBSTRING.
  LINE_START_THEN_WORD_START_THEN_SUBSTRING = 8


@dataclass
class TokenMatchOptions:
  """Options for matching a token from some text."""
  # How to match the token.
  match_method: TokenMatchMethod = TokenMatchMethod.WORD_START_THEN_SUBSTRING
  # Which match to return (e.g. 2 to return the second matching token).
  nth_match: int = 1
  # Search string to use to match the token.
  search: str = ""


@unique
class ModifierType(Enum):
  """Methods of modifying the matched range of a token."""
  # No modification - keep the token itself.
  NONE = 1
  # Take a range of characters in the token itself.
  CHARS = 2
  # Take a range of fragments in the token itself.
  FRAGMENTS = 3
  # Take the line containing the token. Include the trailing line break if present.
  LINE_INCLUDING_LINE_BREAK = 4
  # Take the line containing the token. Do not include trailing line breaks.
  LINE_EXCLUDING_LINE_BREAK = 5
  # Take the token and the rest of the line before it.
  LINE_HEAD = 6
  # Take the token and the rest of the line after it.
  LINE_TAIL = 7
  # Take the block/paragraph containing the token.
  BLOCK = 8
  # Take the function call argument or C-style for loop segment (; separated) containing the token.
  ARGUMENT = 9
  # Take the function call containing the token.
  CALL = 10
  # Take the comment containing the token.
  COMMENT = 11
  # Take the contents of a string containing the token with configurable delimiters (defaults to
  # double quotes).
  STRING = 12
  # The current scope in python code. Includes all contiguous lines at the current or greater
  # indentation level.
  PYTHON_SCOPE = 13
  # The current scope in C-like code. Includes all content between the previous opening brace and
  # its closing brace.
  C_SCOPE = 14
  # Take a sentence in English prose.
  SENTENCE = 15
  # Take the contents of a pair of brackets containing the target.
  BRACKETS = 16
  # Take the start of the line (empty selection after previous line break or at start of file).
  START_OF_LINE = 17
  # Take the end of the line (empty selection after line break or at end of file).
  END_OF_LINE = 18
  # Take all text between whitespace characters.
  BETWEEN_WHITESPACE = 19
  # Take a link in markdown syntax.
  MARKDOWN_LINK = 20
  # Empty selection before the line break on the last non-whitespace line in a markdown section.
  # "Markdown sections" are delimited by any headings or EOF.
  # Moving the cursor before the last line break can be useful for maintaining indentation or list
  # types when adding a new line below.
  MARKDOWN_SECTION_END = 21
  # Find the next function call and take the first argument from it. Assumes the initial match is
  # outside the function call.
  # It's the _first_ argument after the cursor, we need to call this then _next_ if we want the
  # second.
  ARGUMENT_FIRST = 22
  # From a match inside an argument, take the next argument.
  ARGUMENT_NEXT = 23
  # From a match inside an argument, take the previous argument.
  ARGUMENT_PREVIOUS = 24
  # Find the next function call and take the nth argument from it. Assumes the initial match is
  # outside the function call.
  # This uses the first/next modifiers and is provided as an optimization to reduce the number of
  # required textflow commands.
  ARGUMENT_NTH = 25
  # From outside a string, take the next string. Handles doc strings and markdown blocks when the
  # delimiter is a double quote or grave.
  # It's the _first_ string after the cursor, we need to call this then _next_ if we want the
  # second.
  STRING_FIRST = 26
  # From inside a string, take the next string.
  STRING_NEXT = 27
  # From inside a string, take the previous string.
  STRING_PREVIOUS = 28
  # From outside a string, take the nth string.
  # This uses the first/next modifiers and is provided as an optimization to reduce the number of
  # required textflow commands.
  STRING_NTH = 29
  # From outside brackets, take the contents of the next set of brackets.
  # It's the _first_ set of brackets after the cursor, we need to call this then _next_ if we want
  # the second.
  BRACKETS_FIRST = 30
  # From inside a pair of brackets, take the contents of the next pair of brackets.
  BRACKETS_NEXT = 31
  # From inside a pair of brackets, take the contents of the previous pair of brackets.
  BRACKETS_PREVIOUS = 32
  # From outside brackets, take the contents of the nth pair of brackets.
  # This uses the first/next modifiers and is provided as an optimization to reduce the number of
  # required textflow commands.
  BRACKETS_NTH = 33
  # From outside the parentheses of a function call, take the next function call.
  CALL_NEXT = 34
  # From outside the parentheses of a function call, take the previous function call.
  CALL_PREVIOUS = 35
  # Take the next sentence in English prose.
  SENTENCE_NEXT = 36
  # Take the previous sentence in English prose.
  SENTENCE_PREVIOUS = 37
  # A clause in a sentence in English prose. Delimited by commas, some other punctuation, or line
  # breaks.
  SENTENCE_CLAUSE = 38


@dataclass
class Modifier:
  """Options for modifying the matched range of a token."""
  modifier_type: ModifierType = ModifierType.NONE
  # Range for taking fragments or chars from the token.
  modifier_range: Optional[TextRange] = None
  # Delimiter for modifiers where applicable. Empty string to use default.
  delimiter: str = ""
  # Count for modifiers that can repeat actions.
  n: Optional[int] = None


@unique
class TargetCombinationType(Enum):
  """Methods of combining simple targets."""
  # Match until the end of the 'to' target.
  PAST_TO = 1
  # Match until the start of the 'to' target.
  UNTIL_TO = 2


@dataclass
class SimpleTarget:
  """A single target for finding a token in some text."""
  match_options: TokenMatchOptions = field(default_factory=TokenMatchOptions)
  # Direction to search for the target. None to get the closest match before or after the cursor.
  direction: Optional[SearchDirection] = None


@dataclass
class CompoundTarget:
  """A compound target that may have a modifier applied. Represents a single range in the text. If a
  'from' target is not supplied, the current selection range is used. If both a 'from' and 'to'
  target are supplied, the unmodified range for this target is:
  PAST_TO: [from_range.start, to_range.end]
  UNTIL_TO: [from_range.start, to_range.start]"""
  target_from: Optional[SimpleTarget] = None
  target_to: Optional[SimpleTarget] = None
  target_combo: TargetCombinationType = TargetCombinationType.PAST_TO
  # Modifier defaults to no-op.
  modifier: Modifier = field(default_factory=Modifier)


@unique
class CommandType(Enum):
  """A high-level command type for manipulating text."""
  # Selects a target.
  SELECT = 1
  # Clears a target and move the cursor to its location.
  CLEAR_MOVE_CURSOR = 2
  # Clears a target but do not move the cursor to its location.
  CLEAR_NO_MOVE = 3
  # Moves cursor before a target.
  MOVE_CURSOR_BEFORE = 4
  # Moves cursor after a target.
  MOVE_CURSOR_AFTER = 5
  # Copies the target to the clipboard then clear it without moving the cursor to its location.
  CUT_TO_CLIPBOARD = 6
  # Copies the target to the clipboard without moving the cursor to its location.
  COPY_TO_CLIPBOARD = 7
  # Copies the first target to the second.
  BRING = 8
  # Replaces the second target with the first.
  MOVE = 9
  # Swaps the first and second targets.
  SWAP = 12
  # Replace the matched target with a given string without moving the cursor.
  REPLACE = 13
  # Replace a word with its next homophone without moving the cursor.
  NEXT_HOMOPHONE = 14
  # Title case the matched target.
  TITLE_CASE = 15
  # Lowercase the matched target.
  LOWERCASE = 16
  # Replace a single word, matching case, without moving the cursor.
  REPLACE_WORD_MATCH_CASE = 17
  # Make the matched target all uppercase.
  UPPERCASE = 18
  # Replace a matched string with the output of a given lambda.
  REPLACE_WITH_LAMBDA = 19


@dataclass
class Command:
  """A high-level command for manipulating text."""
  command_type: CommandType
  target_from: CompoundTarget
  target_to: Optional[CompoundTarget] = None

  # Text for replacement/insertion commands.
  insert_text: str = ""

  # Lambda for REPLACE_WITH_LAMBDA commands.
  lambda_func: Optional[Callable[[str], str]] = None


@unique
class EditorActionType(Enum):
  """Text input action types."""
  # Sets the currently selected text range. Zero-length range to move the cursor.
  SET_SELECTION_RANGE = 1
  # Clears the selected text. No-op if no text is selected.
  CLEAR = 2
  # Inserts text at the current cursor position. Overwrites selected text, if any.
  INSERT_TEXT = 3
  # Sets the clipboard contents to the given text and adds it to clipboard history.
  SET_CLIPBOARD_WITH_HISTORY = 4
  # Sets the clipboard contents to the given text, but does not add to the clipboard history.
  SET_CLIPBOARD_NO_HISTORY = 5


@dataclass
class EditorAction:
  """A text editing action. Used as output from TextFlow."""
  action_type: EditorActionType
  # Text range for selection.
  text_range: Optional[TextRange] = None
  # Text to insert, copy to the clipboard, etc.
  text: str = ""


@dataclass
class UtilityFunctions:
  """Utility functions for running TextFlow commands."""
  # Get all homophones for a given word. Result includes the given word.
  get_homophones: Callable[[str], list[str]]
  # Get the next homophone for a given word. Returns none if no homophones available.
  get_next_homophone: Callable[[str], Optional[str]]
