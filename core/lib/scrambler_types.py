"""Types used by the Scrambler API for navigating and editing text."""

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any, Callable, Optional


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
class ModifierType(Enum):
  """Types of modifiers that can be applied to a text match to generate a new match."""
  # Get the token before or after the current match.
  TOKEN_NEXT = 1
  TOKEN_PREVIOUS = 2
  # Given a substring, find a word that matches. Will try to match the start of words first, then
  # substrings inside words if that fails.
  WORD_SUBSTRING_CLOSEST = 3
  WORD_SUBSTRING_NEXT = 4
  WORD_SUBSTRING_PREVIOUS = 5
  # Match an exact word.
  EXACT_WORD_CLOSEST = 6
  EXACT_WORD_NEXT = 7
  EXACT_WORD_PREVIOUS = 8
  # Match a phrase with homophone expansion.
  PHRASE_CLOSEST = 9
  PHRASE_NEXT = 10
  PHRASE_PREVIOUS = 11
  # Expand the match to the comment containing it.
  COMMENT = 12
  # Match function call arguments or C-style for loop segment (; separated).
  ARGUMENT = 13  # Expand the current match to the argument containing it.
  ARGUMENT_FIRST = 14  # Find the next function call and match the first argument.
  ARGUMENT_NEXT = 15  # Move between arguments.
  ARGUMENT_PREVIOUS = 16
  # Match full function calls.
  FUNCTION_CALL = 17  # Expand the current match to the function call containing it.
  FUNCTION_CALL_NEXT = 18  # From outside of a function call, take the next function call.
  FUNCTION_CALL_PREVIOUS = 19  # From outside of a function call, take the previous function call.
  # Match strings with configurable symmetric delimiters.
  STRING = 20  # Expand the current match to the string containing it.
  STRING_FIRST = 21  # From outside a string, match the contents of the next string.
  STRING_NEXT = 22  # Move between strings.
  STRING_PREVIOUS = 23
  # The current scope in python code. Includes all contiguous lines at the current or greater
  # indentation level.
  PYTHON_SCOPE = 24
  # The current scope in C-like code. Includes all content between the previous opening brace and
  # its closing brace.
  C_SCOPE = 25
  # Match sentences in English prose.
  SENTENCE = 26  # Expand the match to the sentence containing it.
  SENTENCE_NEXT = 27  # Move between sentences.
  SENTENCE_PREVIOUS = 28
  SENTENCE_CLAUSE = 29  # Expand the match to the clause containing it.
  # Match the contents of pairs of brackets.
  BRACKETS = 30  # Expand the current match to the contents of the brackets containing it.
  BRACKETS_FIRST = 31  # From outside of brackets, match the contents of the next pair.
  BRACKETS_NEXT = 32  # Move between pairs of brackets.
  BRACKETS_PREVIOUS = 33
  # Take the start of the line (empty selection after previous line break or at start of file).
  START_OF_LINE = 34
  # Take the end of the line (empty selection after line break or at end of file).
  END_OF_LINE = 35
  # Expand the match to text delimited by whitespace.
  BETWEEN_WHITESPACE = 36
  # Take a link in markdown syntax.
  MARKDOWN_LINK = 37
  # Empty selection before the line break on the last non-whitespace line in a markdown section.
  # "Markdown sections" are delimited by any headings or EOF.
  # Moving the cursor before the last line break can be useful for maintaining indentation or list
  # types when adding a new line below.
  MARKDOWN_SECTION_END = 38


@dataclass
class Modifier:
  """Options for modifying the matched range of a token."""
  modifier_type: ModifierType = ModifierType.TOKEN_NEXT
  # How many times to apply the modifier.
  repeat: int = 1
  # Text for the modifier to match where applicable.
  search: str = ""
  # Delimiter for modifiers where applicable. Empty string to use default.
  delimiter: str = ""


@unique
class MatchCombinationType(Enum):
  """Methods of combining matches."""
  UP_TO_AND_INCLUDING = 1
  UP_TO_BUT_EXCLUDING = 2


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
  # Replace the matched target with a given string without moving the cursor.
  REPLACE = 9
  # Replace a word with its next homophone without moving the cursor.
  NEXT_HOMOPHONE = 10
  # Change the case of the matched target.
  TITLE_CASE = 11
  LOWERCASE = 12
  UPPERCASE = 13
  # Replace a single word, matching case, without moving the cursor.
  REPLACE_WORD_MATCH_CASE = 14
  # Replace a matched string with the output of a given lambda.
  REPLACE_WITH_LAMBDA = 15


@dataclass
class Command:
  """A high-level command for manipulating text."""
  command_type: CommandType

  # Modifiers applied to the cursor/current selection to get the initial matched range. If this list
  # is empty, the command will apply to the current selection or cursor position.
  modifiers: list[Modifier] = field(default_factory=list)

  # Modifiers applied to extend the initial matched range, and the method of extending the range.
  # - If this list is empty, the command will apply to the initial range only.
  # - Otherwise, this will apply modifiers to the original range, 'a' to produce a new range, 'b'.
  #   - UP_TO_AND_INCLUDING: Final range is [a.start:b.end].
  #   - UP_TO_BUT_EXCLUDING: Final range is [a.start:b.start].
  extend_modifiers: list[Modifier] = field(default_factory=list)
  extend_type: MatchCombinationType = MatchCombinationType.UP_TO_AND_INCLUDING

  # Text for replacement/insertion commands.
  insert_text: str = ""

  # Lambda for REPLACE_WITH_LAMBDA commands.
  lambda_func: Optional[Callable[[str], str]] = None


@unique
class EditorActionType(Enum):
  """Text input action types."""
  # Sets the currently selected text range. Zero-length range to move the cursor.
  # If the range has zero length, vim-style editors should end in insert mode.
  # If the range has non-zero length, vim-style editors should end in visual mode.
  SET_SELECTION_RANGE = 1
  # Inserts text at the current cursor position. Overwrites selected text, if any.
  # Vim-style editors should end in insert mode.
  INSERT_TEXT = 2
  # Sets the clipboard contents to the given text and adds it to clipboard history.
  # Does not affect the editor mode in vim-style editors.
  SET_CLIPBOARD_WITH_HISTORY = 3
  # Sets the clipboard contents to the given text, but does not add to the clipboard history.
  # Does not affect the editor mode in vim-style editors.
  SET_CLIPBOARD_NO_HISTORY = 4
  # Deletes the given text range. Leaves the cursor at the start of the deleted range.
  # Vim-style editors should end in insert mode.
  DELETE_RANGE = 5


@dataclass
class EditorAction:
  """A text editing action. Used as output from scrambler."""
  action_type: EditorActionType
  # Text range for selection, deletion, etc.
  text_range: Optional[TextRange] = None
  # Text to insert, copy to the clipboard, etc.
  text: str = ""


@dataclass
class UtilityFunctions:
  """Utility functions for running commands."""
  # Get all homophones for a given word. Result includes the given word.
  get_homophones: Callable[[str], list[str]]
  # Get the next homophone for a given word. Returns none if no homophones available.
  get_next_homophone: Callable[[str], Optional[str]]


@dataclass
class Context:
  """Context, including text and selection range, that commands will act in."""
  # Text around the cursor. First and last lines should be full lines from the source text.
  text: str
  # The range of the current selection. If the range has zero length, it represents the position of
  # the cursor (an empty selection).
  selection_range: TextRange
  # Whether we are in potato mode. Defaults to true to make overriding `scrambler_get_context` safe
  # by default. If `scrambler_get_context` is overridden but `scrambler_set_selection_action` is not,
  # the non-potato default implementation is likely to fail (e.g. the overridden context action may
  # not populate `editor_element`).
  potato_mode: bool = True
  # The starting offset of `text` in the active editor. Used when we are not operating on the entire
  # contents of the editor. Not used in potato mode.
  text_offset: int = 0
  # The element that contains the text we are editing. Not used outside of AX accessibility mode.
  editor_element: Any = None
  # The current editor mode. Empty string if not applicable.
  # In vim-style editing, this is a character representing the current mode:
  #   n = normal, i = insert, v = visual.
  editor_mode: str = ""
