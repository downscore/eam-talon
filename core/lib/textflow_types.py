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
  """A range of characters in some text. May have zero length (start == end), in which case it represents a cursor
  position (empty selection). This class is intended to be immutable."""
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
    """Returns the length of this range. Non negative, zero if start and end positions are the same."""
    return self.end - self.start

  def extract(self, text: str) -> str:
    """Extracts this range from the given text and returns it."""
    if len(text) < self.end:
      raise ValueError("Tried to extract range beyond end of text")
    return text[self.start:self.end]


@dataclass
class TextMatch:
  """A text range matched by a target or modifier. Includes extra metadata to help with text manipulation."""
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
  # Match the start of a line (like `WORD_START` for the first word in each line). Ignores indentation.
  LINE_START = 4
  # Match by counting tokens (e.g. 3rd last token before the cursor).
  TOKEN_COUNT = 5
  # Match by a text phrase with homophone expansion.
  PHRASE = 6


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
  # Take the line containing the token.
  LINE = 4
  # Take the token and the rest of the line before it.
  LINE_HEAD = 5
  # Take the token and the rest of the line after it.
  LINE_TAIL = 6
  # Take the block/paragraph containing the token.
  BLOCK = 7
  # Take the function call argument or C-style for loop segment (; separated) containing the token.
  ARG = 8
  # Take the function call containing the token.
  CALL = 9
  # Take the comment containing the token.
  COMMENT = 10
  # Take the string containing the token.
  STRING = 11


@dataclass
class Modifier:
  """Options for modifying the matched range of a token."""
  modifier_type: ModifierType = ModifierType.NONE
  # Range for taking fragments or chars from the token.
  modifier_range: Optional[TextRange] = None


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
  """A compound target that may have a modifier applied. Represents a single range in the text. If a 'from' target is
  not supplied, the current selection range is used. If both a 'from' and 'to' target are supplied, the unmodified
  range for this target is:
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


@dataclass
class Command:
  """A high-level command for manipulating text."""
  command_type: CommandType
  target_from: CompoundTarget
  target_to: Optional[CompoundTarget] = None

  # Text for replacement/insertion commands.
  insert_text: str = ""


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
