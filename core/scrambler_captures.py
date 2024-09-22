"""Definition of scambler actions and default implementations."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Optional, Tuple
from talon import Context, Module, actions, grammar
from .lib import scrambler_types as st

mod = Module()
ctx = Context()

_COMMAND_TYPES_BY_SPOKEN = {
    "pick": st.CommandType.SELECT,
    "before": st.CommandType.MOVE_CURSOR_BEFORE,
    "after": st.CommandType.MOVE_CURSOR_AFTER,
    "bring": st.CommandType.BRING,
    "chuck": st.CommandType.CLEAR_NO_MOVE,
    "change": st.CommandType.CLEAR_MOVE_CURSOR,
    "phony": st.CommandType.NEXT_HOMOPHONE,
    "bigger": st.CommandType.TITLE_CASE,
    "biggest": st.CommandType.UPPERCASE,
    "smaller": st.CommandType.LOWERCASE,
}
mod.list("scrambler_command_type", desc="All scrambler command types")
ctx.lists["self.scrambler_command_type"] = _COMMAND_TYPES_BY_SPOKEN.keys()

# Commands that act on a single word.
_SINGLE_WORD_COMMAND_TYPES_BY_SPOKEN = {
    "grab": st.CommandType.SELECT,
    "prepend": st.CommandType.MOVE_CURSOR_BEFORE,
    "append": st.CommandType.MOVE_CURSOR_AFTER,
    "bring word": st.CommandType.BRING,
    "junker": st.CommandType.CLEAR_NO_MOVE,
    "change": st.CommandType.CLEAR_MOVE_CURSOR,
    "phony": st.CommandType.NEXT_HOMOPHONE,
    "bigger": st.CommandType.TITLE_CASE,
    "biggest": st.CommandType.UPPERCASE,
    "smaller": st.CommandType.LOWERCASE,
}
mod.list("scrambler_single_word_command_type",
         desc="Text navigation command types that act on a single word")
ctx.lists["self.scrambler_single_word_command_type"] = _SINGLE_WORD_COMMAND_TYPES_BY_SPOKEN.keys()

# Tuples of object expansion type and optional delimiter keyed by spoken form.
_OBJECT_EXPANSION_TYPES_BY_SPOKEN = {
    "sentence": (st.ModifierType.SENTENCE, None),
    "chunk": (st.ModifierType.SENTENCE_CLAUSE, None),
    "scope": (st.ModifierType.C_SCOPE, None),  # Can be replaced with another type based on context.
    "argument": (st.ModifierType.ARGUMENT, None),
    "dubstring": (st.ModifierType.STRING, "\""),
    "string": (st.ModifierType.STRING, "'"),
    "graves": (st.ModifierType.STRING, "`"),
    "whitespace": (st.ModifierType.BETWEEN_WHITESPACE, None),
    "link": (st.ModifierType.MARKDOWN_LINK, None),
    "comment": (st.ModifierType.COMMENT, None),
    "brackets": (st.ModifierType.BRACKETS, None),
    "invoke": (st.ModifierType.FUNCTION_CALL, None),
}
mod.list("scrambler_object_expansion_type", desc="Object expansion match types")
ctx.lists["self.scrambler_object_expansion_type"] = _OBJECT_EXPANSION_TYPES_BY_SPOKEN.keys()

# Tuples of countable object type and optional delimiter keyed by spoken form.
_OBJECT_COUNT_TYPES_BY_SPOKEN = {
    "argument": (st.ModifierType.ARGUMENT, None),
    "dubstring": (st.ModifierType.STRING, "\""),
    "string": (st.ModifierType.STRING, "'"),
    "graves": (st.ModifierType.STRING, "`"),
    "brackets": (st.ModifierType.BRACKETS, None),
    "invoke": (st.ModifierType.FUNCTION_CALL, None),
    "token": (st.ModifierType.TOKEN_NEXT, None),
}
mod.list("scrambler_object_count_type", desc="Countable object match types")
ctx.lists["self.scrambler_object_count_type"] = _OBJECT_COUNT_TYPES_BY_SPOKEN.keys()

# Tuples of object movement type and optional delimiter keyed by spoken form.
_OBJECT_MOVEMENT_TYPES_BY_SPOKEN = {
    "sentence": (st.ModifierType.SENTENCE, None),
    "argument": (st.ModifierType.ARGUMENT, None),
    "dubstring": (st.ModifierType.STRING, "\""),
    "string": (st.ModifierType.STRING, "'"),
    "graves": (st.ModifierType.STRING, "`"),
    "brackets": (st.ModifierType.BRACKETS, None),
    "invoke": (st.ModifierType.FUNCTION_CALL, None),
    "token": (st.ModifierType.TOKEN_NEXT, None),
}
mod.list("scrambler_object_movement_type", desc="Countable object match types")
ctx.lists["self.scrambler_object_movement_type"] = _OBJECT_MOVEMENT_TYPES_BY_SPOKEN.keys()


@unique
class SearchDirection(Enum):
  """Directions for searching through text."""
  FORWARD = 1
  BACKWARD = 2


_SEARCH_DIRECTION_BY_SPOKEN = {
    "next": SearchDirection.FORWARD,
    "last": SearchDirection.BACKWARD,
    # Common misrecognition of "last".
    "lust": SearchDirection.BACKWARD,
}
mod.list("scrambler_search_direction", desc="Search directions for scrambler commands")
ctx.lists["self.scrambler_search_direction"] = _SEARCH_DIRECTION_BY_SPOKEN.keys()

_MATCH_COMBO_TYPE_BY_SPOKEN = {
    "past": st.MatchCombinationType.UP_TO_AND_INCLUDING,
    "until": st.MatchCombinationType.UP_TO_BUT_EXCLUDING,
}
mod.list("scrambler_target_combo_type", desc="Target combination types for scrambler commands")
ctx.lists["self.scrambler_target_combo_type"] = _MATCH_COMBO_TYPE_BY_SPOKEN.keys()


@unique
class Article(Enum):
  """Grammatical articles."""
  A = 1
  THE = 2


_ARTICLE_BY_SPOKEN = {
    "definite": Article.THE,
    "indefinite": Article.A,
}
mod.list("scrambler_article", desc="Articles for scrambler commands")
ctx.lists["self.scrambler_article"] = _ARTICLE_BY_SPOKEN.keys()


@dataclass
class ScramblerMatch:
  """Sets of modifiers and combination type representing a scrambler match."""
  modifiers: list[st.Modifier]
  combination_type: st.MatchCombinationType = st.MatchCombinationType.UP_TO_AND_INCLUDING
  extend_modifiers: list[st.Modifier] = field(default_factory=list)


def _capture_to_words(m) -> list[str]:
  """Convert a capture to a list of words."""
  words = []
  for item in m:
    if isinstance(item, grammar.vm.Phrase):
      words.extend(actions.dictate.replace_words(actions.dictate.parse_words(item)))
    else:
      words.extend(item.split(" "))
  return words


def _get_ordinal_and_search_direction(m):
  """Get the repeat ordinal and search direction from a capture."""
  try:
    repeat = m.ordinals_small
  except AttributeError:
    repeat = 1

  try:
    direction = m.scrambler_search_direction
  except AttributeError:
    direction = None

  # Default to searching forward if an ordinal was specified.
  if repeat > 1 and direction is None:
    direction = SearchDirection.FORWARD

  return repeat, direction


@mod.capture(rule="{self.scrambler_command_type}")
def scrambler_command_type(m) -> st.CommandType:
  """Maps a spoken command to the command type."""
  return _COMMAND_TYPES_BY_SPOKEN[m.scrambler_command_type]


@mod.capture(rule="{self.scrambler_single_word_command_type}")
def scrambler_single_word_command_type(m) -> st.CommandType:
  """Maps a spoken command for a single to the command type."""
  return _SINGLE_WORD_COMMAND_TYPES_BY_SPOKEN[m.scrambler_single_word_command_type]


@mod.capture(rule="{self.scrambler_object_expansion_type}")
def scrambler_object_expansion_type(m) -> Tuple[st.ModifierType, Optional[str]]:
  """Maps a spoken object expansion type to the type info."""
  return _OBJECT_EXPANSION_TYPES_BY_SPOKEN[m.scrambler_object_expansion_type]


@mod.capture(rule="{self.scrambler_object_count_type}")
def scrambler_object_count_type(m) -> Tuple[st.ModifierType, Optional[str]]:
  """Maps a spoken countable object type to the type info."""
  return _OBJECT_COUNT_TYPES_BY_SPOKEN[m.scrambler_object_count_type]


@mod.capture(rule="{self.scrambler_object_movement_type}")
def scrambler_object_movement_type(m) -> Tuple[st.ModifierType, Optional[str]]:
  """Maps a spoken object movement type to the type info."""
  return _OBJECT_MOVEMENT_TYPES_BY_SPOKEN[m.scrambler_object_movement_type]


@mod.capture(rule="{self.scrambler_search_direction}")
def scrambler_search_direction(m) -> SearchDirection:
  """Maps a spoken search direction to the direction enum."""
  return _SEARCH_DIRECTION_BY_SPOKEN[m.scrambler_search_direction]


@mod.capture(rule="{self.scrambler_target_combo_type}")
def scrambler_target_combo_type(m) -> st.MatchCombinationType:
  """Maps a spoken target combo type to the enum."""
  return _MATCH_COMBO_TYPE_BY_SPOKEN[m.scrambler_target_combo_type]


@mod.capture(rule="(<user.symbol_key> | <user.letters> | <user.dictate_number>)+")
def scrambler_characters(m) -> str:
  """A scrambler capture for a word substring."""
  return "".join(_capture_to_words(m))


@mod.capture(rule="phrase <phrase>")
def scrambler_phrase(m) -> str:
  """A scrambler capture for a phrase."""
  return " ".join(_capture_to_words(m.phrase))


@mod.capture(rule="[<user.ordinals_small>] [<user.scrambler_search_direction>] " +
             "({self.scrambler_article} | <user.word>)")
def scrambler_word(m) -> ScramblerMatch:
  """A scrambler capture for a single word match."""
  repeat, direction = _get_ordinal_and_search_direction(m)
  try:
    article = _ARTICLE_BY_SPOKEN[m.scrambler_article]
    if article == Article.A:
      word = "a"
    word = "the"
  except AttributeError:
    word = m.word

  # If direction is none, repeat must also be 1.
  if direction is None:
    return ScramblerMatch([st.Modifier(st.ModifierType.EXACT_WORD_CLOSEST, repeat, word)])
  if direction == SearchDirection.FORWARD:
    return ScramblerMatch([st.Modifier(st.ModifierType.EXACT_WORD_NEXT, repeat, word)])
  return ScramblerMatch([st.Modifier(st.ModifierType.EXACT_WORD_PREVIOUS, repeat, word)])


@mod.capture(rule="[<user.ordinals_small>] [<user.scrambler_search_direction>] " +
             "(<user.scrambler_characters> | <user.scrambler_phrase>)")
def scrambler_substring(m) -> ScramblerMatch:
  """A scrambler capture for a substring match."""
  repeat, direction = _get_ordinal_and_search_direction(m)

  # Check if a substring was specified.
  try:
    substring = m.scrambler_characters
    if direction is None:
      modifier_type = st.ModifierType.WORD_SUBSTRING_CLOSEST
    elif direction == SearchDirection.FORWARD:
      modifier_type = st.ModifierType.WORD_SUBSTRING_NEXT
    else:
      modifier_type = st.ModifierType.WORD_SUBSTRING_PREVIOUS
    return ScramblerMatch([st.Modifier(modifier_type, repeat, substring)])
  except AttributeError:
    pass

  # Default to a phrase.
  phrase = m.scrambler_phrase
  if direction is None:
    modifier_type = st.ModifierType.PHRASE_CLOSEST
  elif direction == SearchDirection.FORWARD:
    modifier_type = st.ModifierType.PHRASE_NEXT
  else:
    modifier_type = st.ModifierType.PHRASE_PREVIOUS
  return ScramblerMatch([st.Modifier(modifier_type, repeat, phrase)])


@mod.capture(rule="<user.scrambler_substring> " +
             "[<user.scrambler_target_combo_type> <user.scrambler_substring>]")
def scrambler_substring_range(m) -> ScramblerMatch:
  """A scrambler capture substring range match."""
  modifiers = m.scrambler_substring_list[0]
  if len(m.scrambler_substring_list) > 1:
    extend_type = m.scrambler_target_combo_type
    extend_modifiers = m.scrambler_substring_list[1]
  else:
    extend_type = st.MatchCombinationType.UP_TO_AND_INCLUDING
    extend_modifiers = []
  return ScramblerMatch(modifiers, extend_type, extend_modifiers)


@mod.capture(rule="<user.scrambler_object_expansion_type>")
def scrambler_object_expansion(m) -> ScramblerMatch:
  """A scrambler capture for an object expansion match."""
  modifier_type, delimiter = m.scrambler_object_expansion_type
  if modifier_type == st.ModifierType.C_SCOPE:
    modifier_type = actions.user.scrambler_get_scope_modifier()
  return ScramblerMatch([st.Modifier(modifier_type, delimiter=delimiter)])


@mod.capture(rule="<user.scrambler_object_count_type> <user.number_small> " +
             "[<user.scrambler_target_combo_type> <user.number_small>]")
def scrambler_object_count(m) -> ScramblerMatch:
  """A scrambler capture for an object count match."""
  modifier_type, delimiter = m.scrambler_object_count_type
  from_count = m.number_small_list[0]

  # Get modifiers for initial match.
  modifiers = []
  if modifier_type == st.ModifierType.ARGUMENT:
    modifiers.append(st.Modifier(st.ModifierType.ARGUMENT_FIRST, delimiter=delimiter))
    if from_count > 1:
      modifiers.append(
          st.Modifier(st.ModifierType.ARGUMENT_NEXT, from_count - 1, delimiter=delimiter))
  elif modifier_type == st.ModifierType.STRING:
    modifiers.append(st.Modifier(st.ModifierType.STRING_FIRST, delimiter=delimiter))
    if from_count > 1:
      modifiers.append(st.Modifier(st.ModifierType.STRING_NEXT, from_count - 1,
                                   delimiter=delimiter))
  elif modifier_type == st.ModifierType.BRACKETS:
    modifiers.append(st.Modifier(st.ModifierType.BRACKETS_FIRST, delimiter=delimiter))
    if from_count > 1:
      modifiers.append(
          st.Modifier(st.ModifierType.BRACKETS_NEXT, from_count - 1, delimiter=delimiter))
  elif modifier_type == st.ModifierType.FUNCTION_CALL:
    modifiers.append(
        st.Modifier(st.ModifierType.FUNCTION_CALL_NEXT, from_count, delimiter=delimiter))
  elif modifier_type == st.ModifierType.TOKEN_NEXT:
    modifiers.append(st.Modifier(st.ModifierType.TOKEN_NEXT, from_count, delimiter=delimiter))

  # Get modifiers for extend matches if present.
  extend_type = st.MatchCombinationType.UP_TO_AND_INCLUDING
  extend_modifiers = []
  if len(m.number_small_list) > 1:
    to_count = m.number_small_list[1]
    count_diff = to_count - from_count
    if count_diff < 0:
      raise ValueError("Object `from` count must be less than or equal to `to` count")
    if count_diff > 0:
      if modifier_type == st.ModifierType.ARGUMENT:
        extend_modifiers.append(
            st.Modifier(st.ModifierType.ARGUMENT_NEXT, count_diff, delimiter=delimiter))
      elif modifier_type == st.ModifierType.STRING:
        extend_modifiers.append(
            st.Modifier(st.ModifierType.STRING_NEXT, count_diff, delimiter=delimiter))
      elif modifier_type == st.ModifierType.BRACKETS:
        extend_modifiers.append(
            st.Modifier(st.ModifierType.BRACKETS_NEXT, count_diff, delimiter=delimiter))
      elif modifier_type == st.ModifierType.FUNCTION_CALL:
        extend_modifiers.append(
            st.Modifier(st.ModifierType.FUNCTION_CALL_NEXT, count_diff, delimiter=delimiter))
      elif modifier_type == st.ModifierType.TOKEN_NEXT:
        extend_modifiers.append(
            st.Modifier(st.ModifierType.TOKEN_NEXT, count_diff, delimiter=delimiter))

  return ScramblerMatch(modifiers, extend_type, extend_modifiers)


@mod.capture(rule="<user.scrambler_object_movement_type> [<user.ordinals_small>] " +
             "<user.scrambler_search_direction>")
def scrambler_object_movement(m) -> ScramblerMatch:
  """A scrambler capture for an object count match."""
  repeat, direction = _get_ordinal_and_search_direction(m)
  modifier_type, delimiter = m.scrambler_object_movement_type

  if modifier_type == st.ModifierType.SENTENCE:
    if direction == SearchDirection.FORWARD:
      return ScramblerMatch(
          [st.Modifier(st.ModifierType.SENTENCE_NEXT, repeat, delimiter=delimiter)])
    return ScramblerMatch(
        [st.Modifier(st.ModifierType.SENTENCE_PREVIOUS, repeat, delimiter=delimiter)])
  elif modifier_type == st.ModifierType.ARGUMENT:
    if direction == SearchDirection.FORWARD:
      return ScramblerMatch(
          [st.Modifier(st.ModifierType.ARGUMENT_NEXT, repeat, delimiter=delimiter)])
    return ScramblerMatch(
        [st.Modifier(st.ModifierType.ARGUMENT_PREVIOUS, repeat, delimiter=delimiter)])
  elif modifier_type == st.ModifierType.STRING:
    if direction == SearchDirection.FORWARD:
      return ScramblerMatch([st.Modifier(st.ModifierType.STRING_NEXT, repeat, delimiter=delimiter)])
    return ScramblerMatch(
        [st.Modifier(st.ModifierType.STRING_PREVIOUS, repeat, delimiter=delimiter)])
  elif modifier_type == st.ModifierType.BRACKETS:
    if direction == SearchDirection.FORWARD:
      return ScramblerMatch(
          [st.Modifier(st.ModifierType.BRACKETS_NEXT, repeat, delimiter=delimiter)])
    return ScramblerMatch(
        [st.Modifier(st.ModifierType.BRACKETS_PREVIOUS, repeat, delimiter=delimiter)])
  elif modifier_type == st.ModifierType.FUNCTION_CALL:
    if direction == SearchDirection.FORWARD:
      return ScramblerMatch(
          [st.Modifier(st.ModifierType.FUNCTION_CALL_NEXT, repeat, delimiter=delimiter)])
    return ScramblerMatch(
        [st.Modifier(st.ModifierType.FUNCTION_CALL_PREVIOUS, repeat, delimiter=delimiter)])
  elif modifier_type == st.ModifierType.TOKEN_NEXT:
    if direction == SearchDirection.FORWARD:
      return ScramblerMatch([st.Modifier(st.ModifierType.TOKEN_NEXT, repeat, delimiter=delimiter)])
    return ScramblerMatch(
        [st.Modifier(st.ModifierType.TOKEN_PREVIOUS, repeat, delimiter=delimiter)])

  raise ValueError(f"Unsupported object movement type: {modifier_type}")
