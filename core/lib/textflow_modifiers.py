"""Code for applying modifiers to matched text ranges."""

import functools
import re
from .textflow_match import get_nth_regex_match
from .textflow_types import Modifier, ModifierType, SearchDirection, TextMatch, TextRange


def _make_match(start: int, end: int) -> TextMatch:
  """Match a text match using a single range."""
  return TextMatch(TextRange(start, end))


def _apply_chars_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes characters from the matched token."""
  del text  # Unused.
  if modifier.modifier_range is None:
    raise ValueError("No modifier range provided")
  if (modifier.modifier_range.start < 0 or modifier.modifier_range.end < modifier.modifier_range.start):
    raise ValueError(f"Invalid modifier range: {modifier.modifier_range}")
  # Clamp end of the modifier range.
  end_index = min(input_match.text_range.end, input_match.text_range.start + modifier.modifier_range.end)
  return _make_match(input_match.text_range.start + modifier.modifier_range.start, end_index)


def _apply_words_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes words from the matched token."""
  if modifier.modifier_range is None:
    raise ValueError("No modifier range provided")
  if (modifier.modifier_range.start < 0 or modifier.modifier_range.end < modifier.modifier_range.start):
    raise ValueError(f"Invalid modifier range: {modifier.modifier_range}")

  # Split matched token into words.
  # TODO: Split camel/pascal/snake/kebab case words and track word positions.
  token = text[input_match.text_range.start:input_match.text_range.end]
  words = re.split(r" |\_|\-", token)

  # Return empty start of range if there are no words.
  if len(words) == 0:
    return _make_match(input_match.text_range.start, input_match.text_range.start)

  # Clamp word range to last word.
  start_word = min(len(words) - 1, modifier.modifier_range.start)
  end_word = min(len(words), modifier.modifier_range.end)
  assert end_word >= start_word

  # Sum word lengths, then add number of spaces/separators between words.
  start_index = functools.reduce(lambda index, word: index + len(word), words[0:start_word], 0)
  start_index += start_word
  end_index = functools.reduce(lambda index, word: index + len(word), words[start_word:end_word], start_index)
  end_index += end_word - start_word

  return _make_match(start_index, end_index)


def _apply_line_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the line containing the token."""
  del modifier  # Unused.
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index - 1] != "\n":
    start_index -= 1
  end_index = input_match.text_range.start  # Start of token to ensure we always take a single line.
  while end_index < len(text) - 1 and text[end_index] != "\n":
    end_index += 1
  return _make_match(start_index, end_index + 1)


def _apply_line_head_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the start of the line containing the token."""
  del modifier  # Unused.
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index - 1] != "\n":
    start_index -= 1
  return _make_match(start_index, input_match.text_range.end)


def _apply_line_tail_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the end of the line containing the token."""
  del modifier  # Unused.
  end_index = input_match.text_range.start  # Start of token to ensure we always take a single line.
  while end_index < len(text) - 1 and text[end_index + 1] != "\n":
    end_index += 1
  return _make_match(input_match.text_range.start, end_index)


def _apply_block_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the block containing the match. The input match may be at the end of the block."""
  del modifier  # Unused.

  # Blocks are separated by two or more line breaks (or document beginning) with optional whitespace in between.
  first_separator_regex = re.compile(r"\n([ \t\r]*\n)+", re.IGNORECASE)
  second_separator_regex = re.compile(r"($|(\n[ \t\r]*)+\n)", re.IGNORECASE)

  # Get first block separator before the match.
  first_match = get_nth_regex_match(text[:input_match.text_range.start], first_separator_regex, 1,
                                    SearchDirection.BACKWARD)
  block_start_index = 0
  if first_match is not None:
    block_start_index = first_match.end()

  # Get block separator after the first.
  second_match = get_nth_regex_match(text[block_start_index:], second_separator_regex, 1, SearchDirection.FORWARD)
  if second_match is None:
    raise ValueError("Could not match end of block")
  block_end_index = block_start_index + second_match.start()

  # Look for unbalanced braces from the beginning and end of the block.
  block_text = text[block_start_index:block_end_index]
  brace_stack = []
  for i, char in enumerate(block_text):
    if char == "{":
      brace_stack.append(i)
    elif char == "}":
      if len(brace_stack) == 0:
        # There is an unbalanced closing brace. Make that the end of the block.
        block_end_index = block_start_index + i
        break
      brace_stack.pop()

  # Check if there are any unbalanced opening braces. If there are any, start the block after the last one.
  if len(brace_stack) > 0:
    block_start_index = block_start_index + brace_stack[-1] + 1
    # If the brace is followed by a line break, do not include it in the block.
    if block_start_index < block_end_index and text[block_start_index] == "\n":
      block_start_index += 1
    block_end_index = max(block_end_index, block_start_index)

  return _make_match(block_start_index, block_end_index)


def _apply_comment_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the comment containing the token."""
  del modifier  # Unused.
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
    while end_index < len(text) and (end_index == len(text) - 1 or text[end_index + 1] != "\n"):
      end_index += 1
  else:
    while end_index < len(text) - 1:
      if text[end_index:end_index + 2] == "*/":
        end_index += 2
        break
      end_index += 1

  return _make_match(start_index, end_index)


def _apply_string_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the C-style string containing the token."""
  del modifier  # Unused.
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index] != "\"":
    start_index -= 1
  end_index = input_match.text_range.end
  while end_index < len(text) and text[end_index - 1] != "\"":
    end_index += 1

  # Make sure a string was matched.
  if text[start_index] != "\"" or text[end_index - 1] != "\"":
    return input_match

  return _make_match(start_index, end_index)


_MODIFIER_FUNCTIONS = {
    ModifierType.CHARS: _apply_chars_modifier,
    ModifierType.FRAGMENTS: _apply_words_modifier,
    ModifierType.LINE: _apply_line_modifier,
    ModifierType.LINE_HEAD: _apply_line_head_modifier,
    ModifierType.LINE_TAIL: _apply_line_tail_modifier,
    ModifierType.BLOCK: _apply_block_modifier,
    ModifierType.COMMENT: _apply_comment_modifier,
    ModifierType.STRING: _apply_string_modifier,
}


def apply_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Applies a modifier to the given range and returns the new range."""
  if input_match.text_range.end > len(text):
    raise ValueError(f"Match beyond end of text: {input_match}")
  if modifier.modifier_type == ModifierType.NONE:
    return input_match
  return _MODIFIER_FUNCTIONS[modifier.modifier_type](text, input_match, modifier)
