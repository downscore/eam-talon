"""Talon code for using numbers."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import re
from talon import Context, Module, actions
from .lib import number_util, ordinal_util

mod = Module()
ctx = Context()

# Captures for number words.
_ALT_DIGITS = "(" + ("|".join(number_util.DIGITS_BY_WORD.keys())) + ")"
_ALT_TEENS = "(" + ("|".join(number_util.TEENS_BY_WORD.keys())) + ")"
_ALT_TENS = "(" + ("|".join(number_util.TENS_BY_WORD.keys())) + ")"
_ALT_FIRST_NUMBER_WORDS = "(" + "|".join(number_util.FIRST_NUMBERS_BY_WORD.keys()) + ")"
_ALT_NUMBER_WORDS = "(" + "|".join(number_util.NUMBERS_BY_WORD.keys()) + ")"

# Get ordinals and delete "first" since it's typically not useful (e.g. for repeating commands).
_ORDINALS_DICT = ordinal_util.get_ints_by_ordinal_words(99)
del _ORDINALS_DICT["first"]
_ORDINALS_SMALL_DICT = ordinal_util.get_ints_by_ordinal_words(20)
del _ORDINALS_SMALL_DICT["first"]

mod.list("ordinals", desc="List of ordinals used for repeating commands.")
ctx.lists["self.ordinals"] = _ORDINALS_DICT.keys()

mod.list("ordinals_small", desc="Smaller list of ordinals used for repeating commands.")
ctx.lists["self.ordinals_small"] = _ORDINALS_SMALL_DICT.keys()


@mod.capture(rule=f"{_ALT_FIRST_NUMBER_WORDS} {_ALT_NUMBER_WORDS}* (and {_ALT_NUMBER_WORDS}+)*")
def number_list_of_words(m) -> list[str]:
  """Captures a number as a list of words. e.g. ["one", "thousand", "and", "twenty", "five"]."""
  return list(m)


@mod.capture(rule="<user.number_list_of_words>")
def number_string_of_digits(m) -> str:
  """Parses a number phrase, returning that number as a string of digits. e.g. "1025"."""
  return number_util.parse_number(m.number_list_of_words)


@mod.capture(rule="<user.number_string_of_digits>")
def number(m) -> int:
  """Parses a number phrase, returning it as an integer."""
  return int(m.number_string_of_digits)


@mod.capture(
    rule="(numb|num) <user.number_string_of_digits> [(punch|point) <user.number_string_of_digits>]")
def dictate_number(m) -> str:
  """A number prefixed with a dictation command. Includes an optional decimal point"""
  if len(m.number_string_of_digits_list) > 1:
    return m.number_string_of_digits_list[0] + "." + m.number_string_of_digits_list[1]
  return m.number_string_of_digits_list[0]


@mod.capture(rule=f"({_ALT_DIGITS} | {_ALT_TEENS} | {_ALT_TENS} [{_ALT_DIGITS}])")
def number_small(m) -> int:
  return int(number_util.parse_number(list(m)))


@mod.capture(rule="{self.ordinals}")
def ordinals(m) -> int:
  """Returns a single ordinal as a digit."""
  return int(_ORDINALS_DICT[m[0]])


@mod.capture(rule="{self.ordinals_small}")
def ordinals_small(m) -> int:
  """Returns a single ordinal as a digit. Captures a small subset of `ordinals`."""
  return int(_ORDINALS_DICT[m[0]])


@mod.capture(rule="{self.ordinals_small}")
def repeat_ordinal(m) -> int:
  """Subtracts one from a single ordinal and returns it as an integer. Captures a small subset of
  `ordinals`."""
  return int(_ORDINALS_DICT[m[0]]) - 1


@mod.action_class
class Actions:
  """Actions related to numbers."""

  def number_add(n: int):
    """Adds n to any selected numbers."""
    selected: str = actions.user.selected_text_or_word()

    # Match all numbers in selected text using a regex. Also matches negative numbers.
    regex = r"[-]?\d+"
    replace = re.sub(regex, lambda match: str(int(match.group(0)) + n), selected)

    actions.user.insert_replacing_selected(replace)

  def number_subtract(n: int):
    """Subtracts n from any selected numbers."""
    actions.user.number_add(n * -1)  # `-n` causes pylint warning.

  def number_multiply(n: int):
    """Multiplies n with any selected numbers."""
    selected: str = actions.user.selected_text_or_word()

    # Match all numbers in selected text using a regex. Also matches negative numbers.
    regex = r"[-]?\d+"
    replace = re.sub(regex, lambda match: str(int(match.group(0)) * n), selected)

    actions.user.insert_replacing_selected(replace)

  def number_divide(n: int):
    """Divides any selected numbers by n. Truncates results to integers."""
    selected: str = actions.user.selected_text_or_word()

    # Match all numbers in selected text using a regex. Also matches negative numbers.
    regex = r"[-]?\d+"
    replace = re.sub(regex, lambda match: str(int(match.group(0)) // n), selected)

    actions.user.insert_replacing_selected(replace)
