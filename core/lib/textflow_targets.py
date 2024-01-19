"""Code for matching TextFlow targets inside text."""

import copy
from typing import Optional, Tuple
from .textflow_types import CompoundTarget, SearchDirection, SimpleTarget, TargetCombinationType, TextMatch, TextRange, TokenMatchMethod, UtilityFunctions
from .textflow_match import match_token


def _add_to_match(match: TextMatch, num_chars: int) -> TextMatch:
  """Returns a new text match with the given number of characters added to the given match's ranges."""
  result = TextMatch(TextRange(match.text_range.start + num_chars, match.text_range.end + num_chars))
  if match.deletion_range is not None:
    result.deletion_range = TextRange(match.deletion_range.start + num_chars, match.deletion_range.end + num_chars)
  return result


def _combine_ranges(range_from: TextRange, unmapped_range_to: TextRange,
                    combo_type: TargetCombinationType) -> TextRange:
  """Returns a new range that is a combination of two given ones."""
  unmapped_end = unmapped_range_to.start if combo_type == TargetCombinationType.UNTIL_TO else unmapped_range_to.end
  return TextRange(range_from.start, range_from.end + unmapped_end)


def _combine_matches(match_from: TextMatch, unmapped_match_to: TextMatch,
                     combo_type: TargetCombinationType) -> TextMatch:
  """Return a new match that is a combination of two given ones."""
  result = TextMatch(_combine_ranges(match_from.text_range, unmapped_match_to.text_range, combo_type))
  # TODO: Handle deletion ranges if necessary.
  return result


def _get_best_token_match(target: SimpleTarget, text_before: str, text_after,
                          utility_functions: UtilityFunctions) -> Optional[Tuple[SearchDirection, TextMatch]]:
  """Finds the best matching token. Does not implement priority of word starts over substrings across directions."""
  match_before = None
  if target.direction is None or target.direction == SearchDirection.BACKWARD:
    match_before = match_token(text_before, target.match_options, SearchDirection.BACKWARD,
                               utility_functions.get_homophones)
  match_after = None
  if target.direction is None or target.direction == SearchDirection.FORWARD:
    match_after = match_token(text_after, target.match_options, SearchDirection.FORWARD,
                              utility_functions.get_homophones)
  if match_before is not None and match_after is not None:
    # We have matches before and after the cursor. Select the closer match. Break ties by choosing the match after the
    # cursor.
    dist_before = len(text_before) - match_before.text_range.end
    dist_after = match_after.text_range.start
    if dist_after <= dist_before:
      return (SearchDirection.FORWARD, match_after)
    return (SearchDirection.BACKWARD, match_before)
  if match_before is not None:
    return (SearchDirection.BACKWARD, match_before)
  if match_after is not None:
    return (SearchDirection.FORWARD, match_after)
  return None


def _match_simple_target(target: SimpleTarget, text_before: str, text_after,
                         utility_functions: UtilityFunctions) -> Optional[Tuple[SearchDirection, TextMatch]]:
  """Match a simple target in the given text. Returns None if no match was found. Returned direction is `BACKWARD` if
  the match is in `text_before` and `FORWARD` if the match is in `text_after`."""
  # If we are giving priority to word starts, search only word starts first.
  if target.match_options.match_method == TokenMatchMethod.WORD_START_THEN_SUBSTRING:
    target_copy = copy.deepcopy(target)
    target_copy.match_options.match_method = TokenMatchMethod.WORD_START
    result = _get_best_token_match(target_copy, text_before, text_after, utility_functions)
    if result is not None:
      return result
  return _get_best_token_match(target, text_before, text_after, utility_functions)


def match_compound_target(target: CompoundTarget, text: str, selection_range: TextRange,
                          utility_functions: UtilityFunctions) -> Optional[TextMatch]:
  """Match a compound target in the given text. Does not apply modifiers. Returns None if no match was found."""
  # Get text to search before and after the selection.
  text_before = text[0:selection_range.start]
  text_after = text[selection_range.end:]

  # Match 'from' simple target. If no 'from' target supplied, use the beginning of the current selection.
  match_tuple_from: Optional[Tuple[SearchDirection, TextMatch]] = (SearchDirection.BACKWARD, TextMatch(selection_range))
  if target.target_from is not None:
    match_tuple_from = _match_simple_target(target.target_from, text_before, text_after, utility_functions)
  if match_tuple_from is None:
    return None

  # Map the 'from' match to the original text input.
  match_from = match_tuple_from[1]  # Note: No need to modify the range if it was matched in `text_before`.
  if match_tuple_from[0] == SearchDirection.FORWARD:
    match_from = _add_to_match(match_tuple_from[1], selection_range.end)

  # If there is no 'to' target, return the 'from' target.
  if target.target_to is None:
    return match_from

  # Note: We allow searching through the selected text for the 'to' target. For this search, there is no 'text_before'
  # since we need to match after the 'from' target.
  match_tuple_to = _match_simple_target(target.target_to, "", text[match_from.text_range.end:], utility_functions)
  if match_tuple_to is None:
    return None
  assert match_tuple_to[0] == SearchDirection.FORWARD

  # Combine target matches.
  return _combine_matches(match_from, match_tuple_to[1], target.target_combo)
