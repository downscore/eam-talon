"""Util functions for text processing."""

from dataclasses import dataclass
from enum import Enum, unique
import re


@unique
class StripMethod(Enum):
  """Method of stripping a string."""
  # Strip surrounding whitespace.
  WHITESPACE = 1
  # Strip everything except the first number in the string.
  KEEP_FIRST_NUMBER = 2


@dataclass
class StrippedString:
  """A stripped string along with the padding that was stripped from it."""
  stripped: str
  left_padding: str
  right_padding: str

  def __init__(self, s: str, method: StripMethod = StripMethod.WHITESPACE):
    # Strip to keep first number if necessary.
    if method == StripMethod.KEEP_FIRST_NUMBER:
      self.stripped = ""
      self.left_padding = ""
      self.right_padding = ""
      found_number = False
      for i, c in enumerate(s):
        if c.isdigit():
          self.stripped += c
          found_number = True
        elif found_number:
          self.right_padding = s[i:]
          return
        else:
          self.left_padding += c
      return

    left_stripped = s.lstrip()
    self.left_padding = s[0:len(s) - len(left_stripped)]
    self.stripped = left_stripped.rstrip()
    self.right_padding = left_stripped[len(self.stripped):]

  def apply_padding(self, s: str):
    """Applies the padding in this object to the given string."""
    return self.left_padding + s + self.right_padding


def count_lines(s: str):
  """Returns the number of lines in the passed string. Excludes trailing empty lines."""
  # TODO: Might be faster to count line breaks and check if last character(s) is/are a line break. Avoids creating the
  # collection of split lines in memory.
  return len(s.splitlines())


def count_words(s: str):
  """Returns the number of words in the passed string."""
  return len(re.findall(r"\w+", s))


def sort_lines(s: str, reverse: bool = False) -> str:
  """Returns a new string consisting of the input string with all lines sorted. Preserves padding around input.
  Case insensitive."""
  stripped_input = StrippedString(s)
  lines = stripped_input.stripped.splitlines()
  return stripped_input.apply_padding("\n".join(sorted(lines, key=str.casefold, reverse=reverse)))
