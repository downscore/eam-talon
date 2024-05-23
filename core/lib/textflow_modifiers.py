"""Code for applying modifiers to matched text ranges."""

import re
from .textflow_match import get_nth_regex_match
from .textflow_types import Modifier, ModifierType, SearchDirection, TextMatch, TextRange
from .format_util import get_fragment_ranges


def _make_match(start: int, end: int) -> TextMatch:
  """Match a text match using a single range."""
  return TextMatch(TextRange(start, end))


def _get_line_at_index(text: str, index: int, include_trailing_line_break: bool) -> TextRange:
  """Get the line containing the given index."""
  start_index = index
  while start_index > 0 and text[start_index - 1] != "\n":
    start_index -= 1
  end_index = index
  while end_index < len(text) and text[end_index] != "\n":
    end_index += 1
  if include_trailing_line_break and end_index < len(text) and text[end_index] == "\n":
    end_index += 1
  return TextRange(start_index, end_index)


def _apply_chars_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes characters from the matched token."""
  del text  # Unused.
  if modifier.modifier_range is None:
    raise ValueError("No modifier range provided")
  # Clamp the modifier range to the end of the input.
  start_index = min(input_match.text_range.end, input_match.text_range.start + modifier.modifier_range.start)
  end_index = min(input_match.text_range.end, input_match.text_range.start + modifier.modifier_range.end)
  return _make_match(start_index, end_index)


def _apply_fragments_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes fragments from the matched token."""
  if modifier.modifier_range is None:
    raise ValueError("No modifier range provided")

  # Divide matched text into fragments.
  fragment_ranges = get_fragment_ranges(text)

  # Clamp range to the number of fragments.
  start_fragment = min(len(fragment_ranges), modifier.modifier_range.start)
  end_fragment = min(len(fragment_ranges), modifier.modifier_range.end)
  assert end_fragment >= start_fragment

  # Return empty end of range if start fragment is beyond last fragment.
  if start_fragment >= len(fragment_ranges):
    return _make_match(input_match.text_range.end, input_match.text_range.end)

  return _make_match(fragment_ranges[start_fragment][0], fragment_ranges[end_fragment - 1][1])


def _apply_line_including_line_break_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the line containing the match."""
  del modifier  # Unused.
  line_range = _get_line_at_index(text, input_match.text_range.start, include_trailing_line_break=True)
  return TextMatch(line_range)


def _apply_line_excluding_line_break_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the line containing the match."""
  del modifier  # Unused.
  line_range = _get_line_at_index(text, input_match.text_range.start, include_trailing_line_break=False)
  return TextMatch(line_range)


def _apply_end_of_line_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes an empty match at the end of the line containing the input match."""
  del modifier  # Unused.
  line_range = _get_line_at_index(text, input_match.text_range.start, include_trailing_line_break=True)
  return _make_match(line_range.end, line_range.end)


def _apply_start_of_line_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes an empty match at the start of the line containing the match."""
  del modifier  # Unused.
  line_range = _get_line_at_index(text, input_match.text_range.start, include_trailing_line_break=True)
  return _make_match(line_range.start, line_range.start)


def _apply_line_head_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes from the start of the line containing the match to the end of the match."""
  del modifier  # Unused.
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index - 1] != "\n":
    start_index -= 1
  return _make_match(start_index, input_match.text_range.end)


def _apply_line_tail_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes from the start of the match to the end of the line containing the match."""
  del modifier  # Unused.
  end_index = input_match.text_range.start  # Start of match to ensure we always take a single line.
  while end_index < len(text) and text[end_index] != "\n":
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
  """Takes the comment containing the match."""
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
    while end_index < len(text) and text[end_index] != "\n":
      end_index += 1
  else:
    while end_index < len(text) - 1:
      if text[end_index:end_index + 2] == "*/":
        end_index += 2
        break
      end_index += 1

  return _make_match(start_index, end_index)


def _apply_string_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the content between symmetric delimiters containing the match. Defaults to C-style strings."""
  delimiter = "\"" if modifier.delimiter == "" else modifier.delimiter
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index - 1] != delimiter:
    start_index -= 1
  end_index = input_match.text_range.end
  while end_index < len(text) and text[end_index] != delimiter:
    end_index += 1

  return _make_match(start_index, end_index)


def _apply_python_scope_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the current scope in Python code."""
  del modifier  # Unused.

  # Find the indentation level of the current or last non-empty line.
  indentation_search_index = input_match.text_range.start
  min_indentation_level = None
  while indentation_search_index >= 0 and min_indentation_level is None:
    line_range = _get_line_at_index(text, indentation_search_index, include_trailing_line_break=True)
    line_text = line_range.extract(text)
    # Make sure the line isn't just whitespace.
    if line_text.strip() != "":
      # We found a non-whitespace line. Use its indentation level.
      min_indentation_level = len(line_text) - len(line_text.lstrip())
      break
    # Move to the previous line.
    indentation_search_index = line_range.start - 1

  # Make sure we found an indentation level.
  if min_indentation_level is None:
    raise ValueError("Could not find indentation level for Python scope")

  # Find the start of the current scope.
  start_line_range = _get_line_at_index(text, input_match.text_range.start, include_trailing_line_break=True)
  first_non_whitespace_line_range = start_line_range
  while start_line_range.start > 0:
    previous_line_range = _get_line_at_index(text, start_line_range.start - 1, include_trailing_line_break=True)
    previous_line_text = previous_line_range.extract(text)
    is_whitespace = previous_line_text.strip() == ""
    # Stop if we find a non-whitespace line with less indentation.
    if not is_whitespace and len(previous_line_text) - len(previous_line_text.lstrip()) < min_indentation_level:
      break
    start_line_range = previous_line_range
    if not is_whitespace:
      first_non_whitespace_line_range = start_line_range

  # Find the end of the current scope.
  end_line_range = start_line_range
  last_non_whitespace_line_range = end_line_range
  while end_line_range.end < len(text):
    next_line_range = _get_line_at_index(text, end_line_range.end, include_trailing_line_break=True)
    next_line_text = next_line_range.extract(text)
    is_whitespace = next_line_text.strip() == ""
    # Stop if we find a line with less indentation.
    if not is_whitespace and len(next_line_text) - len(next_line_text.lstrip()) < min_indentation_level:
      break
    end_line_range = next_line_range
    if not is_whitespace:
      last_non_whitespace_line_range = end_line_range

  # Return the scope, excluding surrounding lines that are just whitespace.
  return _make_match(first_non_whitespace_line_range.start, last_non_whitespace_line_range.end)


def _apply_c_scope_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the current scope in C-style code."""
  del modifier  # Unused.

  # Find the first opening brace before the match. Keep track of the number of close braces.
  close_braces = 0
  start_index = input_match.text_range.start
  while start_index > 0:
    if text[start_index - 1] == "}":
      close_braces += 1
    elif text[start_index - 1] == "{":
      if close_braces <= 0:
        break
      close_braces -= 1
    start_index -= 1

  # Don't include the newline after the opening brace if present.
  if (start_index < len(text) and text[start_index] == "\n"):
    start_index += 1

  # Find the corresponding closing brace. Keep track of the number of open nested braces.
  open_braces = 0
  end_index = start_index
  while end_index < len(text):
    if text[end_index] == "{":
      open_braces += 1
    elif text[end_index] == "}":
      if open_braces <= 0:
        break
      open_braces -= 1
    end_index += 1

  # Remove indentation before the closing brace.
  while end_index > start_index and text[end_index - 1] in [" ", "\t"]:
    end_index -= 1

  return _make_match(start_index, end_index)


def _apply_argument_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the current argument."""
  del modifier  # Unused.

  # Find the first argument delimiter before the match. Track close parentheses to handle nested calls.
  start_index = input_match.text_range.start
  close_parentheses = 0
  while start_index > 0:
    if text[start_index - 1] == ")":
      close_parentheses += 1
    elif text[start_index - 1] == "(":
      if close_parentheses == 0:
        break
      close_parentheses -= 1
    elif text[start_index - 1] in (",", ";") and close_parentheses == 0:
      break
    start_index -= 1

  # Deletion range start includes leading whitespace, but remove it from the selection range.
  deletion_start_index = start_index
  while start_index < len(text) and text[start_index] in [" ", "\t", "\n"]:
    start_index += 1

  # Try to include leading comma in deletion range. There are cases where we may not want to delete a leading semicolon,
  # so we ignore semicolons for now.
  found_leading_comma = False
  if deletion_start_index > 0 and text[deletion_start_index - 1] == ",":
    deletion_start_index -= 1
    found_leading_comma = True

  # Find the next argument delimiter after the match. Track open parentheses to handle nested calls.
  end_index = input_match.text_range.end
  open_parentheses = 0
  while end_index < len(text):
    if text[end_index] == "(":
      open_parentheses += 1
    elif text[end_index] == ")":
      if open_parentheses == 0:
        break
      open_parentheses -= 1
    elif text[end_index] in (",", ";") and open_parentheses == 0:
      break
    end_index += 1

  # Deletion range end includes trailing whitespace, but remove it from the selection range.
  deletion_end_index = end_index
  while end_index > start_index and text[end_index - 1] in [" ", "\t", "\n"]:
    end_index -= 1

  # If we did not include a leading comma in the deletion range, try to find a trailing comma.
  if not found_leading_comma and deletion_end_index < len(text) and text[deletion_end_index] == ",":
    deletion_end_index += 1
    # Include a whitespace character after the comma, if present.
    if deletion_end_index < len(text) and text[deletion_end_index] in [" ", "\t"]:
      deletion_end_index += 1

  return TextMatch(TextRange(start_index, end_index), TextRange(deletion_start_index, deletion_end_index))


def _apply_sentence_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the current sentence. Suitable for English prose."""
  del modifier  # Unused.

  sentence_delimiters = [".", "!", "?", "\n"]

  # Find the end of the previous sentence.
  start_index = input_match.text_range.start
  while start_index > 0:
    if text[start_index - 1] in sentence_delimiters:
      break
    start_index -= 1

  # Remove leading whitespace from the range.
  while start_index < len(text) and text[start_index] in [" ", "\t", "\n"]:
    start_index += 1

  # Find the end of the current sentence.
  end_index = input_match.text_range.end
  while end_index < len(text):
    if text[end_index] in sentence_delimiters:
      end_index += 1  # Include the delimiter.
      break
    end_index += 1

  # Prefer to include trailing spaces in the deletion range, as leading spaces may be indentation or other formatting.
  included_trailing_spaces = False
  deletion_end_index = end_index
  # Limit to 2 trailing spaces.
  while deletion_end_index < len(text) and text[deletion_end_index] == " " and deletion_end_index - end_index < 2:
    deletion_end_index += 1
    included_trailing_spaces = True

  # Include leading spaces in the deletion range if necessary.
  deletion_start_index = start_index
  if not included_trailing_spaces:
    # Limit to 2 leading spaces.
    while deletion_start_index > 0 and text[deletion_start_index - 1] == " " and start_index - deletion_start_index < 2:
      deletion_start_index -= 1

  return TextMatch(TextRange(start_index, end_index), TextRange(deletion_start_index, deletion_end_index))


def _apply_call_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the current function call. Assumes the input match is in the function name, not inside the parentheses."""
  del modifier  # Unused.

  # Find the start of the function call.
  # Try to be permissive and include balanced parentheses to allow complex C++ calls such as:
  # (*obj)->get_thing().field[0].method(arg1, &arg2, arg3);
  start_index = input_match.text_range.start
  nested_parentheses = 0
  while start_index > 0 and (text[start_index - 1].isalnum() or
                             text[start_index - 1] in ("_", ".", "-", ">", "*", "(", ")", "[", "]")):
    if text[start_index - 1] == "(":
      if nested_parentheses == 0:
        break
      nested_parentheses -= 1
    elif text[start_index - 1] == ")":
      nested_parentheses += 1
    start_index -= 1

  # Find the end of the function call. Look for an opening parenthesis after the input match, then its balanced close.
  # Use the input match so we can get the entire call if the input match is in `method` in the example above.
  end_index = input_match.text_range.end
  nested_parentheses = -1  # Start with -1 to so we stop after closing the first open parenthesis.
  while end_index < len(text):
    if text[end_index] == "(":
      nested_parentheses += 1
    elif text[end_index] == ")":
      if nested_parentheses == 0:
        # Include closing parenthesis.
        end_index += 1
        break
      nested_parentheses -= 1
    end_index += 1

  return _make_match(start_index, end_index)


def _apply_brackets_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the contents of surrounding brackets."""
  del modifier  # Unused.

  bracket_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}

  # Find the first opening bracket before the match without a matching closing bracket.
  start_index = input_match.text_range.start
  nesting_level_by_bracket = {}
  # Initialize nesting level at zero for all bracket types.
  for bracket in bracket_pairs:
    nesting_level_by_bracket[bracket] = 0
  opening_bracket = None
  while start_index > 0:
    c = text[start_index - 1]
    if c in bracket_pairs:
      nesting_level_by_bracket[c] -= 1
      if nesting_level_by_bracket[c] < 0:
        opening_bracket = c
        break
    elif c in bracket_pairs.values():
      # Get key for value c
      for bracket, close_bracket in bracket_pairs.items():
        if close_bracket == c:
          nesting_level_by_bracket[bracket] += 1
          break
    start_index -= 1

  # Make sure we found an opening bracket.
  if opening_bracket is None:
    raise ValueError("Could not find opening bracket")

  # Find the corresponding closing bracket.
  end_index = start_index
  nesting_level = 0
  while end_index < len(text):
    c = text[end_index]
    if c == opening_bracket:
      nesting_level += 1
    elif c == bracket_pairs[opening_bracket]:
      if nesting_level == 0:
        break
      nesting_level -= 1
    end_index += 1

  return _make_match(start_index, end_index)


def _apply_between_whitespace_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the contents of surrounding whitespace (including line breaks)."""
  del modifier  # Unused.

  delimiters = [" ", "\t", "\n"]

  # Find whitespace before the input match.
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index - 1] not in delimiters:
    start_index -= 1

  # Find whitespace after the input match.
  end_index = input_match.text_range.end
  while end_index < len(text) and text[end_index] not in delimiters:
    end_index += 1

  # Try to include trailing whitespace in the deletion range.
  deletion_end_index = end_index
  included_trailing_whitespace = False
  if deletion_end_index < len(text) and text[deletion_end_index] in delimiters:
    deletion_end_index += 1
    included_trailing_whitespace = True

  # If we couldn't include trailing whitespace, try to include leading whitespace.
  deletion_start_index = start_index
  if not included_trailing_whitespace and deletion_start_index > 0 and text[deletion_start_index - 1] in delimiters:
    deletion_start_index -= 1

  return TextMatch(TextRange(start_index, end_index), TextRange(deletion_start_index, deletion_end_index))


_MODIFIER_FUNCTIONS = {
    ModifierType.CHARS: _apply_chars_modifier,
    ModifierType.FRAGMENTS: _apply_fragments_modifier,
    ModifierType.LINE_INCLUDING_LINE_BREAK: _apply_line_including_line_break_modifier,
    ModifierType.LINE_EXCLUDING_LINE_BREAK: _apply_line_excluding_line_break_modifier,
    ModifierType.LINE_HEAD: _apply_line_head_modifier,
    ModifierType.LINE_TAIL: _apply_line_tail_modifier,
    ModifierType.BLOCK: _apply_block_modifier,
    ModifierType.ARG: _apply_argument_modifier,
    ModifierType.CALL: _apply_call_modifier,
    ModifierType.COMMENT: _apply_comment_modifier,
    ModifierType.STRING: _apply_string_modifier,
    ModifierType.PYTHON_SCOPE: _apply_python_scope_modifier,
    ModifierType.C_SCOPE: _apply_c_scope_modifier,
    ModifierType.SENTENCE: _apply_sentence_modifier,
    ModifierType.BRACKETS: _apply_brackets_modifier,
    ModifierType.END_OF_LINE: _apply_end_of_line_modifier,
    ModifierType.START_OF_LINE: _apply_start_of_line_modifier,
    ModifierType.BETWEEN_WHITESPACE: _apply_between_whitespace_modifier,
}


def apply_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Applies a modifier to the given range and returns the new range."""
  # Just return the input match unmodified if the text is empty.
  if len(text) == 0:
    return input_match

  if input_match.text_range.end > len(text):
    raise ValueError(f"Match beyond end of text: {input_match}")
  if modifier.modifier_type == ModifierType.NONE:
    return input_match
  return _MODIFIER_FUNCTIONS[modifier.modifier_type](text, input_match, modifier)
