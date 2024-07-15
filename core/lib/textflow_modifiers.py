"""Code for applying modifiers to matched text ranges."""

import re
from .textflow_match import get_nth_regex_match
from .textflow_types import Modifier, ModifierType, SearchDirection, TextMatch, TextRange
from .format_util import get_fragment_ranges

_OPEN_BRACKETS = ["(", "[", "{", "<"]
_CLOSE_BRACKETS = [")", "]", "}", ">"]
_BRACKET_PAIRS = dict(zip(_OPEN_BRACKETS, _CLOSE_BRACKETS))
_SENTENCE_DELIMITERS = [".", "!", "?", "\n"]


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


def _index_of_next_character(text: str, index: int, characters: list[str]):
  """Given an index in some text, get the index after the next instance of any of the given
  characters."""
  while index < len(text) and text[index] not in characters:
    index += 1
  return index


def _index_of_previous_character(text: str, index: int, characters: list[str]):
  """Given an index in some text, get the index before the last instance of any of the given
  characters."""
  while index > 0 and (index == len(text) or text[index] not in characters):
    index -= 1
  return index


def _apply_chars_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes characters from the matched token."""
  del text  # Unused.
  if modifier.modifier_range is None:
    raise ValueError("No modifier range provided")
  # Clamp the modifier range to the end of the input.
  start_index = min(input_match.text_range.end,
                    input_match.text_range.start + modifier.modifier_range.start)
  end_index = min(input_match.text_range.end,
                  input_match.text_range.start + modifier.modifier_range.end)
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


def _apply_line_including_line_break_modifier(text: str, input_match: TextMatch,
                                              modifier: Modifier) -> TextMatch:
  """Takes the line containing the match."""
  del modifier  # Unused.
  line_range = _get_line_at_index(text,
                                  input_match.text_range.start,
                                  include_trailing_line_break=True)
  return TextMatch(line_range)


def _apply_line_excluding_line_break_modifier(text: str, input_match: TextMatch,
                                              modifier: Modifier) -> TextMatch:
  """Takes the line containing the match."""
  del modifier  # Unused.
  line_range = _get_line_at_index(text,
                                  input_match.text_range.start,
                                  include_trailing_line_break=False)
  return TextMatch(line_range)


def _apply_end_of_line_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes an empty match at the end of the line containing the input match."""
  del modifier  # Unused.
  line_range = _get_line_at_index(text,
                                  input_match.text_range.start,
                                  include_trailing_line_break=True)
  return _make_match(line_range.end, line_range.end)


def _apply_start_of_line_modifier(text: str, input_match: TextMatch,
                                  modifier: Modifier) -> TextMatch:
  """Takes an empty match at the start of the line containing the match."""
  del modifier  # Unused.
  line_range = _get_line_at_index(text,
                                  input_match.text_range.start,
                                  include_trailing_line_break=True)
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

  # Blocks are separated by two or more line breaks (or document beginning) with optional whitespace
  # in between.
  first_separator_regex = re.compile(r"\n([ \t\r]*\n)+", re.IGNORECASE)
  second_separator_regex = re.compile(r"($|(\n[ \t\r]*)+\n)", re.IGNORECASE)

  # Get first block separator before the match.
  first_match = get_nth_regex_match(text[:input_match.text_range.start], first_separator_regex, 1,
                                    SearchDirection.BACKWARD)
  block_start_index = 0
  if first_match is not None:
    block_start_index = first_match.end()

  # Get block separator after the first.
  second_match = get_nth_regex_match(text[block_start_index:], second_separator_regex, 1,
                                     SearchDirection.FORWARD)
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

  # Check if there are any unbalanced opening braces. If there are any, start the block after the
  # last one.
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
  """Takes the content between symmetric delimiters containing the match. Defaults to C-style
  strings."""
  delimiter = "\"" if not modifier.delimiter else modifier.delimiter
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index - 1] != delimiter:
    start_index -= 1
  end_index = input_match.text_range.end
  while end_index < len(text) and text[end_index] != delimiter:
    end_index += 1

  return _make_match(start_index, end_index)


def _apply_string_first_modifier(text: str, input_match: TextMatch,
                                 modifier: Modifier) -> TextMatch:
  """From outside a string, takes the next string."""
  delimiter = "\"" if not modifier.delimiter else modifier.delimiter

  # Find the start of the next string.
  start_index = _index_of_next_character(text, input_match.text_range.end, [delimiter])
  # Check if the delimiter is tripled, like a docstring or markdown block.
  is_docstring = start_index < len(text) - 2 and text[start_index:start_index + 3] == delimiter * 3
  if is_docstring:
    start_index += 2

  # Start from within the string.
  start_index = min(start_index + 1, len(text))

  return _apply_string_modifier(text, _make_match(start_index, start_index), modifier)


def _apply_string_next_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """From inside a string, takes the next string."""
  delimiter = "\"" if not modifier.delimiter else modifier.delimiter

  # Find the end of the current string.
  start_index = _index_of_next_character(text, input_match.text_range.end, [delimiter])
  # Check if the delimiter is tripled, like a docstring or markdown block.
  is_docstring = start_index < len(text) - 2 and text[start_index:start_index + 3] == delimiter * 3
  if is_docstring:
    start_index += 2

  # Start from outside the string.
  start_index = min(start_index + 1, len(text))

  # Find the next string after leaving the current one.
  return _apply_string_first_modifier(text, _make_match(start_index, start_index), modifier)


def _apply_string_previous_modifier(text: str, input_match: TextMatch,
                                    modifier: Modifier) -> TextMatch:
  """From inside a string, takes the previous string."""
  delimiter = "\"" if not modifier.delimiter else modifier.delimiter

  # Find the start of the current string.
  index = _index_of_previous_character(text, input_match.text_range.start, [delimiter])
  # Check if the delimiter is tripled, like a docstring or markdown block.
  is_docstring = index > 2 and text[index - 2:index + 1] == delimiter * 3
  if is_docstring:
    index -= 2

  # Move outside the current string.
  index = max(index - 1, 0)

  # Find the end of the previous string.
  index = _index_of_previous_character(text, index, [delimiter])
  # Check if the delimiter is tripled, like a docstring or markdown block.
  is_docstring = index > 2 and text[index - 2:index + 1] == delimiter * 3
  if is_docstring:
    index -= 2

  # Move into the previous string.
  index = max(index - 1, 0)

  # Find the previous string before entering the current one.
  return _apply_string_modifier(text, _make_match(index, index), modifier)


def _apply_string_nth_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """From outside a string, takes the nth string."""
  if modifier.n is None or modifier.n < 1:
    raise ValueError("n must be positive.")
  result = _apply_string_first_modifier(text, input_match, modifier)
  for _ in range(modifier.n - 1):
    result = _apply_string_next_modifier(text, result, modifier)
  return result


def _apply_python_scope_modifier(text: str, input_match: TextMatch,
                                 modifier: Modifier) -> TextMatch:
  """Takes the current scope in Python code."""
  del modifier  # Unused.

  # Find the indentation level of the current or last non-empty line.
  indentation_search_index = input_match.text_range.start
  min_indentation_level = None
  while indentation_search_index >= 0 and min_indentation_level is None:
    line_range = _get_line_at_index(text,
                                    indentation_search_index,
                                    include_trailing_line_break=True)
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
  start_line_range = _get_line_at_index(text,
                                        input_match.text_range.start,
                                        include_trailing_line_break=True)
  first_non_whitespace_line_range = start_line_range
  while start_line_range.start > 0:
    previous_line_range = _get_line_at_index(text,
                                             start_line_range.start - 1,
                                             include_trailing_line_break=True)
    previous_line_text = previous_line_range.extract(text)
    is_whitespace = previous_line_text.strip() == ""
    # Stop if we find a non-whitespace line with less indentation.
    if not is_whitespace and len(previous_line_text) - len(
        previous_line_text.lstrip()) < min_indentation_level:
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
    if not is_whitespace and len(next_line_text) - len(
        next_line_text.lstrip()) < min_indentation_level:
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

  # Find the first argument delimiter before the match. Track close parentheses to handle nested
  # calls.
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

  # Try to include leading comma in deletion range. There are cases where we may not want to delete
  # a leading semicolon, so we ignore semicolons for now.
  found_leading_delimiter = False
  if deletion_start_index > 0 and text[deletion_start_index - 1] in (",", ";"):
    deletion_start_index -= 1
    found_leading_delimiter = True

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

  # If we did not include a leading delimiter in the deletion range, try to find a trailing
  # delimiter.
  if not found_leading_delimiter and deletion_end_index < len(
      text) and text[deletion_end_index] in (",", ";"):
    deletion_end_index += 1
    # Include a whitespace character after the delimiter, if present.
    if deletion_end_index < len(text) and text[deletion_end_index] in [" ", "\t"]:
      deletion_end_index += 1

  return TextMatch(TextRange(start_index, end_index),
                   TextRange(deletion_start_index, deletion_end_index))


def _apply_argument_first_modifier(text: str, input_match: TextMatch,
                                   modifier: Modifier) -> TextMatch:
  """Finds the next function call and takes the first argument from it. Assumes the initial match is
  outside the function call."""
  # Find the start of the next function call. Start looking from the end of the current match.
  paren_index = _index_of_next_character(text, input_match.text_range.end, ["("])
  # Skip over empty function calls: func()
  while paren_index < len(text) - 1 and text[paren_index + 1] == ")":
    paren_index = _index_of_next_character(text, paren_index + 1, ["("])
  paren_index = min(paren_index + 1, len(text))

  # Match the argument after the opening parenthesis.
  return _apply_argument_modifier(text, _make_match(paren_index, paren_index), modifier)


def _apply_argument_next_modifier(text: str, input_match: TextMatch,
                                  modifier: Modifier) -> TextMatch:
  """From a match inside an argument, takes the next argument."""
  divider_index = _index_of_next_character(text, input_match.text_range.end, [",", ";"])
  divider_index = min(divider_index + 1, len(text))
  return _apply_argument_modifier(text, _make_match(divider_index + 1, divider_index + 1), modifier)


def _apply_argument_previous_modifier(text: str, input_match: TextMatch,
                                      modifier: Modifier) -> TextMatch:
  """From a match inside an argument, takes the previous argument."""
  divider_index = _index_of_previous_character(text, input_match.text_range.start, [",", ";"])
  divider_index = max(divider_index - 1, 0)
  return _apply_argument_modifier(text, _make_match(divider_index, divider_index), modifier)


def _apply_argument_nth_modifier(text: str, input_match: TextMatch,
                                 modifier: Modifier) -> TextMatch:
  """Finds the next function call and takes the nth argument from it. Assumes the initial match is
  outside the function call."""
  if modifier.n is None or modifier.n < 1:
    raise ValueError("n must be positive.")
  result = _apply_argument_first_modifier(text, input_match, modifier)
  for _ in range(modifier.n - 1):
    result = _apply_argument_next_modifier(text, result, modifier)
  return result


def _apply_sentence_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the current sentence. Suitable for English prose."""
  del modifier  # Unused.

  # Find the end of the previous sentence.
  start_index = input_match.text_range.start
  while start_index > 0:
    if text[start_index - 1] in _SENTENCE_DELIMITERS:
      break
    start_index -= 1

  # Remove leading whitespace from the range.
  while start_index < len(text) and text[start_index] in [" ", "\t", "\n"]:
    start_index += 1

  # Find the end of the current sentence.
  end_index = input_match.text_range.end
  while end_index < len(text):
    if text[end_index] in _SENTENCE_DELIMITERS:
      end_index += 1  # Include the delimiter.
      break
    end_index += 1

  # Prefer to include trailing spaces in the deletion range, as leading spaces may be indentation or
  # other formatting.
  included_trailing_spaces = False
  deletion_end_index = end_index
  # Limit to 2 trailing spaces.
  while deletion_end_index < len(
      text) and text[deletion_end_index] == " " and deletion_end_index - end_index < 2:
    deletion_end_index += 1
    included_trailing_spaces = True

  # Include leading spaces in the deletion range if necessary.
  deletion_start_index = start_index
  if not included_trailing_spaces:
    # Limit to 2 leading spaces.
    while deletion_start_index > 0 and text[deletion_start_index -
                                            1] == " " and start_index - deletion_start_index < 2:
      deletion_start_index -= 1

  return TextMatch(TextRange(start_index, end_index),
                   TextRange(deletion_start_index, deletion_end_index))


def _apply_sentence_next_modifier(text: str, input_match: TextMatch,
                                  modifier: Modifier) -> TextMatch:
  """Takes the next sentence."""
  end_index = input_match.text_range.end
  # Special case: End of the current sentence is selected.
  if input_match.text_range.length() > 0 and end_index > 0 and text[end_index -
                                                                    1] in _SENTENCE_DELIMITERS:
    return _apply_sentence_modifier(text, _make_match(end_index, end_index), modifier)
  # Find the end of the sentence.
  end_index = _index_of_next_character(text, input_match.text_range.end, _SENTENCE_DELIMITERS)
  end_index = min(end_index + 1, len(text))
  return _apply_sentence_modifier(text, _make_match(end_index, end_index), modifier)


def _apply_sentence_previous_modifier(text: str, input_match: TextMatch,
                                      modifier: Modifier) -> TextMatch:
  """Takes the previous sentence."""
  # Find the start of the previous sentence.
  start_index = _index_of_previous_character(text, input_match.text_range.start,
                                             _SENTENCE_DELIMITERS)
  start_index = max(start_index - 1, 0)
  return _apply_sentence_modifier(text, _make_match(start_index, start_index), modifier)


def _apply_sentence_clause_modifier(text: str, input_match: TextMatch,
                                    modifier: Modifier) -> TextMatch:
  """Expands the match to cover a clause in English prose. Doesn't include leading or trailing
  whitespace in the deletion range"""
  del modifier  # Unused.
  clause_delimiters = [",", ".", "!", "?", "\n", "(", ")", ":", ";"]

  # Find the end of the previous clause.
  start_index = input_match.text_range.start
  while start_index > 0:
    if text[start_index - 1] in clause_delimiters:
      break
    start_index -= 1

  # Remove leading whitespace from the range.
  while start_index < len(text) and text[start_index] in [" ", "\t", "\n"]:
    start_index += 1

  # Find the end of the current sentence.
  end_index = input_match.text_range.end
  while end_index < len(text):
    if text[end_index] in clause_delimiters:
      break
    end_index += 1

  return TextMatch(TextRange(start_index, end_index))


def _apply_call_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the current function call. Assumes the input match is in the function name, not inside
  the parentheses."""
  del modifier  # Unused.

  # Find the start of the function call.
  # Try to be permissive and include balanced parentheses to allow complex C++ calls such as:
  # (*obj)->get_thing().field[0].method(arg1, &arg2, arg3);
  start_index = input_match.text_range.start
  nested_parentheses = 0
  while start_index > 0 and (text[start_index - 1].isalnum() or text[start_index - 1]
                             in ("_", ".", "-", ">", "*", "(", ")", "[", "]", ":")):
    if text[start_index - 1] == "(":
      if nested_parentheses == 0:
        break
      nested_parentheses -= 1
    elif text[start_index - 1] == ")":
      nested_parentheses += 1
    start_index -= 1

  # Find the end of the function call. Look for an opening parenthesis after the input match, then
  # its balanced close. Use the input match so we can get the entire call if the input match is in
  # `method` in the  example above.
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


def _apply_call_next_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """From inside a function call, takes the next function call."""
  # Find the start of the next function call.
  start_index = _index_of_next_character(text, input_match.text_range.end, ["("])
  # Skip over parens without a function name before them.
  while start_index > 0 and not text[start_index - 1].isalnum():
    start_index = _index_of_next_character(text, start_index + 1, ["("])
  start_index = max(start_index - 1, 0)

  # Match the function call before the opening parenthesis.
  return _apply_call_modifier(text, _make_match(start_index, start_index), modifier)


def _apply_call_previous_modifier(text: str, input_match: TextMatch,
                                  modifier: Modifier) -> TextMatch:
  """From inside a function call, takes the previous function call."""
  # Find the start of the previous function call.
  start_index = _index_of_previous_character(text, input_match.text_range.start, ["("])
  # Skip over parens without a function name before them.
  while start_index > 0 and not text[start_index - 1].isalnum():
    start_index = _index_of_previous_character(text, start_index - 1, ["("])
  start_index = max(start_index - 1, 0)

  # Match the function call before the opening parenthesis.
  return _apply_call_modifier(text, _make_match(start_index, start_index), modifier)


def _apply_brackets_modifier(text: str, input_match: TextMatch, modifier: Modifier) -> TextMatch:
  """Takes the contents of surrounding brackets."""
  del modifier  # Unused.

  # Find the first opening bracket before the match without a matching closing bracket.
  start_index = input_match.text_range.start
  nesting_level_by_bracket = {}
  # Initialize nesting level at zero for all bracket types.
  for bracket in _BRACKET_PAIRS:
    nesting_level_by_bracket[bracket] = 0
  opening_bracket = None
  while start_index > 0:
    c = text[start_index - 1]
    if c in _BRACKET_PAIRS:
      nesting_level_by_bracket[c] -= 1
      if nesting_level_by_bracket[c] < 0:
        opening_bracket = c
        break
    elif c in _BRACKET_PAIRS.values():
      # Get key for value c
      for bracket, close_bracket in _BRACKET_PAIRS.items():
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
    elif c == _BRACKET_PAIRS[opening_bracket]:
      if nesting_level == 0:
        break
      nesting_level -= 1
    end_index += 1

  return _make_match(start_index, end_index)


def _apply_brackets_first_modifier(text: str, input_match: TextMatch,
                                   modifier: Modifier) -> TextMatch:
  """From outside a bracket, takes the next bracketed content."""
  # Find the start of the next bracketed content.
  start_index = _index_of_next_character(text, input_match.text_range.end, _OPEN_BRACKETS)
  # Ignore < with a trailing space. It's most likely to be a comparison, not a bracket.
  while 0 < start_index < len(text) - 1 and text[start_index:start_index + 2] == "< ":
    start_index = _index_of_next_character(text, start_index + 1, _OPEN_BRACKETS)
  # Start from within the bracket.
  start_index = min(start_index + 1, len(text))

  return _apply_brackets_modifier(text, _make_match(start_index, start_index), modifier)


def _apply_brackets_next_modifier(text: str, input_match: TextMatch,
                                  modifier: Modifier) -> TextMatch:
  """From inside a bracket, takes the next bracketed content."""
  # Find the end of the current bracketed content.
  start_index = _index_of_next_character(text, input_match.text_range.end, _CLOSE_BRACKETS)
  # Ignore > with a leading space. It's most likely to be a comparison, not a bracket.
  while 0 < start_index < len(text) and text[start_index - 1:start_index + 1] == " >":
    start_index = _index_of_next_character(text, start_index + 1, _CLOSE_BRACKETS)
  # Start from outside the bracket.
  start_index = min(start_index + 1, len(text))

  # Find the next bracketed content after leaving the current one.
  return _apply_brackets_first_modifier(text, _make_match(start_index, start_index), modifier)


def _apply_brackets_previous_modifier(text: str, input_match: TextMatch,
                                      modifier: Modifier) -> TextMatch:
  """From inside a bracket, takes the previous bracketed content."""
  # Find the start of the current bracketed content.
  index = _index_of_previous_character(text, input_match.text_range.start, _OPEN_BRACKETS)
  # Ignore < with a trailing space. It's most likely to be a comparison, not a bracket.
  while 0 < index < len(text) - 1 and text[index:index + 2] == "< ":
    index = _index_of_previous_character(text, index - 1, _OPEN_BRACKETS)
  # Move outside the current bracket.
  index = max(index - 1, 0)

  # Find the end of the previous bracketed content.
  index = _index_of_previous_character(text, index, _CLOSE_BRACKETS)
  # Ignore > with a leading space. It's most likely to be a comparison, not a bracket.
  while 0 < index < len(text) and text[index - 1:index + 1] == " >":
    index = _index_of_previous_character(text, index - 1, _CLOSE_BRACKETS)
  # Move into the previous bracket.
  index = max(index - 1, 0)

  # Find the previous bracketed content before entering the current one.
  return _apply_brackets_modifier(text, _make_match(index, index), modifier)


def _apply_brackets_nth_modifier(text: str, input_match: TextMatch,
                                 modifier: Modifier) -> TextMatch:
  """From outside a bracket, takes the nth bracketed content."""
  if modifier.n is None or modifier.n < 1:
    raise ValueError("n must be positive.")
  result = _apply_brackets_first_modifier(text, input_match, modifier)
  for _ in range(modifier.n - 1):
    result = _apply_brackets_next_modifier(text, result, modifier)
  return result


def _apply_between_whitespace_modifier(text: str, input_match: TextMatch,
                                       modifier: Modifier) -> TextMatch:
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
  if not included_trailing_whitespace and deletion_start_index > 0 and text[deletion_start_index -
                                                                            1] in delimiters:
    deletion_start_index -= 1

  return TextMatch(TextRange(start_index, end_index),
                   TextRange(deletion_start_index, deletion_end_index))


def _apply_markdown_link_modifier(text: str, input_match: TextMatch,
                                  modifier: Modifier) -> TextMatch:
  """Takes a full link in markdown syntax, including brackets. Example:
  [link text](http://example.com)"""
  del modifier  # Unused.

  # Find the start of the link: "["
  start_index = input_match.text_range.start
  while start_index > 0 and text[start_index] != "[":
    start_index -= 1

  # Find the end of the link: ")"
  end_index = start_index
  while end_index < len(text) and text[end_index] != ")":
    end_index += 1

  return _make_match(start_index, end_index + 1)


def _apply_end_of_markdown_section_modifier(text: str, input_match: TextMatch,
                                            modifier: Modifier) -> TextMatch:
  """Takes an empty selection before the line break on the last non-whitespace line in a markdown
  section."""
  del modifier  # Unused.

  # Regex that matches pound symbols followed by a space.
  heading_regex = re.compile(r"^#+ ", re.IGNORECASE)

  # Search backwards so we can start on a non-whitespace line.
  curr_index = input_match.text_range.end
  while curr_index > 0:
    line_range = _get_line_at_index(text, curr_index, include_trailing_line_break=True)
    line_text = line_range.extract(text)

    if line_text.strip() != "":
      break

    # Move to the previous line.
    curr_index = line_range.start - 1

  # Move through the text line by line.
  is_first_line = True
  result_index = curr_index
  while curr_index < len(text):
    line_range = _get_line_at_index(text, curr_index, include_trailing_line_break=True)
    line_text = line_range.extract(text)

    # Ignore headings on the first line, otherwise terminate the search when we see a heading.
    if not is_first_line and heading_regex.match(line_text):
      break

    # If this line is not just whitespace, update the result index.
    if line_text.strip() != "":
      result_index = max(line_range.start,
                         line_range.end - 1 if line_text.endswith("\n") else line_range.end)

    # Move to the next line.
    curr_index = line_range.end
    is_first_line = False

  return _make_match(result_index, result_index)


_MODIFIER_FUNCTIONS = {
    ModifierType.CHARS: _apply_chars_modifier,
    ModifierType.FRAGMENTS: _apply_fragments_modifier,
    ModifierType.LINE_INCLUDING_LINE_BREAK: _apply_line_including_line_break_modifier,
    ModifierType.LINE_EXCLUDING_LINE_BREAK: _apply_line_excluding_line_break_modifier,
    ModifierType.LINE_HEAD: _apply_line_head_modifier,
    ModifierType.LINE_TAIL: _apply_line_tail_modifier,
    ModifierType.BLOCK: _apply_block_modifier,
    ModifierType.ARGUMENT: _apply_argument_modifier,
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
    ModifierType.MARKDOWN_LINK: _apply_markdown_link_modifier,
    ModifierType.MARKDOWN_SECTION_END: _apply_end_of_markdown_section_modifier,
    ModifierType.ARGUMENT_FIRST: _apply_argument_first_modifier,
    ModifierType.ARGUMENT_NEXT: _apply_argument_next_modifier,
    ModifierType.ARGUMENT_PREVIOUS: _apply_argument_previous_modifier,
    ModifierType.ARGUMENT_NTH: _apply_argument_nth_modifier,
    ModifierType.STRING_FIRST: _apply_string_first_modifier,
    ModifierType.STRING_NEXT: _apply_string_next_modifier,
    ModifierType.STRING_PREVIOUS: _apply_string_previous_modifier,
    ModifierType.STRING_NTH: _apply_string_nth_modifier,
    ModifierType.BRACKETS_FIRST: _apply_brackets_first_modifier,
    ModifierType.BRACKETS_NEXT: _apply_brackets_next_modifier,
    ModifierType.BRACKETS_PREVIOUS: _apply_brackets_previous_modifier,
    ModifierType.BRACKETS_NTH: _apply_brackets_nth_modifier,
    ModifierType.CALL_NEXT: _apply_call_next_modifier,
    ModifierType.CALL_PREVIOUS: _apply_call_previous_modifier,
    ModifierType.SENTENCE_NEXT: _apply_sentence_next_modifier,
    ModifierType.SENTENCE_PREVIOUS: _apply_sentence_previous_modifier,
    ModifierType.SENTENCE_CLAUSE: _apply_sentence_clause_modifier,
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
