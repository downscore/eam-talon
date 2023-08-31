"""Talon code for using numbers."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from .lib import number_util, ordinal_util, text_util

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


def _get_selected_number() -> text_util.StrippedString:
  """Get the currently-selected number, or the number where the cursor is located."""
  selected: str = actions.edit.selected_text()
  if len(selected) == 0:
    actions.edit.select_word()
    selected = actions.edit.selected_text()
  selected_stripped = text_util.StrippedString(selected, text_util.StripMethod.KEEP_FIRST_NUMBER)
  return selected_stripped


@mod.capture(rule=f"{_ALT_FIRST_NUMBER_WORDS} {_ALT_NUMBER_WORDS}* (and {_ALT_NUMBER_WORDS}+)*")
def number_string(m) -> str:
  """Parses a number phrase, returning that number as a string."""
  return number_util.parse_number(list(m))


@mod.capture(rule="<user.number_string>")
def number(m) -> int:
  """Parses a number phrase, returning it as an integer."""
  return int(m.number_string)


@mod.capture(rule="(numb|num) <user.number_string> [(punch|point) <user.number_string>]")
def dictate_number(m) -> int:
  """A number prefixed with a dictation command. Includes an optional decimal point"""
  if len(m.number_string_list) > 1:
    return m.number_string_list[0] + "." + m.number_string_list[1]
  return m.number_string_list[0]


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
  """Subtracts one from a single ordinal and returns it as an integer. Captures a small subset of `ordinals`."""
  return int(_ORDINALS_DICT[m[0]]) - 1


@mod.action_class
class Actions:
  """Actions related to numbers."""

  def number_increment():
    """Increments the selected number."""
    selected_stripped = _get_selected_number()

    if len(selected_stripped.stripped) == 0:
      print(f"Invalid number: {selected_stripped}")
      return

    incremented = int(selected_stripped.stripped) + 1
    text = selected_stripped.apply_padding(str(incremented))
    actions.user.insert_via_clipboard(text)

  def number_decrement():
    """Decrements the selected number."""
    selected_stripped = _get_selected_number()

    if len(selected_stripped.stripped) == 0:
      print(f"Invalid number: {selected_stripped}")
      return

    decremented = int(selected_stripped.stripped) - 1
    text = selected_stripped.apply_padding(str(decremented))
    actions.user.insert_via_clipboard(text)

  def number_add(n: int):
    """Adds n to the selected number."""
    selected_stripped = _get_selected_number()

    if len(selected_stripped.stripped) == 0:
      print(f"Invalid number: {selected_stripped}")
      return

    result = int(selected_stripped.stripped) + n
    text = selected_stripped.apply_padding(str(result))
    actions.user.insert_via_clipboard(text)

  def number_subtract(n: int):
    """Subtracts n from the selected number."""
    selected_stripped = _get_selected_number()

    if len(selected_stripped.stripped) == 0:
      print(f"Invalid number: {selected_stripped}")
      return

    result = int(selected_stripped.stripped) - n
    text = selected_stripped.apply_padding(str(result))
    actions.user.insert_via_clipboard(text)

  def number_multiply(n: int):
    """Multiplies n with the selected number."""
    selected_stripped = _get_selected_number()

    if len(selected_stripped.stripped) == 0:
      print(f"Invalid number: {selected_stripped}")
      return

    result = int(selected_stripped.stripped) * n
    text = selected_stripped.apply_padding(str(result))
    actions.user.insert_via_clipboard(text)

  def number_divide(n: int):
    """Divides the selected number by n. Truncates result to integer."""
    selected_stripped = _get_selected_number()

    if len(selected_stripped.stripped) == 0:
      print(f"Invalid number: {selected_stripped}")
      return

    result = int(int(selected_stripped.stripped) / n)
    text = selected_stripped.apply_padding(str(result))
    actions.user.insert_via_clipboard(text)
