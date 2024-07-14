"""Tests for matching targets."""

import unittest
from .textflow_targets import *  # pylint: disable=wildcard-import, unused-wildcard-import
from .textflow_test_util import UTILITY_FUNCTIONS
from .textflow_types import TokenMatchOptions

# Line indices including line breaks for first and second lines:
# [0, 99]
# [100, 212]
# [213, 231]
_SAMPLE_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat."""


class MatchCompoundTargetTestCase(unittest.TestCase):
  """Tests for matching a compound target."""

  def test_empty_string(self):
    target = CompoundTarget()
    match = match_compound_target(target, "", TextRange(0, 0), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range, TextRange(0, 0))

  def test_match_selection(self):
    target = CompoundTarget()
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(10, 20), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range, TextRange(10, 20))

  def test_match_word_before_selection(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ips")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum")

  def test_match_word_after_selection(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ull")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ullamco")

  def test_match_word_before_and_after_selection_before_wins(self):
    # Use a substring that matches a word before and after the selection. Tie should be broken by
    # distance to selection.
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "di")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "adipiscing")

  def test_match_word_before_and_after_selection_after_wins(self):
    # Use a substring that matches a word before and after the selection. Tie should be broken by
    # distance to selection.
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "do")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "do")

  def test_match_word_substring(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "psum")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum")

  def test_match_multiple_words_before_selection(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ip")))
    target.target_to = SimpleTarget(
        TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "am"))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum dolor sit amet")

  def test_match_multiple_words_after_selection(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "en")))
    target.target_to = SimpleTarget(
        TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ve"))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "enim ad minim veniam")

  def test_match_multiple_words_across_selection(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "adi")))
    target.target_to = SimpleTarget(
        TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "eiu"))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "adipiscing elit, sed do eiusmod")

  def test_match_nonexistent_from_target(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "xyz")))
    target.target_to = SimpleTarget(
        TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "am"))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    self.assertIsNone(match)

  def test_match_nonexistent_to_target(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ip")))
    target.target_to = SimpleTarget(
        TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "xyz"))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    self.assertIsNone(match)

  def test_match_phrase_single_word(self):
    target = CompoundTarget(SimpleTarget(TokenMatchOptions(TokenMatchMethod.PHRASE, 1, "ipsum")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum")

  def test_match_phrase_missing_letter(self):
    target = CompoundTarget(SimpleTarget(TokenMatchOptions(TokenMatchMethod.PHRASE, 1, "ipsu")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum")

  def test_match_phrase(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.PHRASE, 1, "ipsum dolor sit")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum dolor sit")

  def test_match_phrase_backwards(self):
    # Second "this" should be matched.
    text = "this is this test."
    target = CompoundTarget(SimpleTarget(TokenMatchOptions(TokenMatchMethod.PHRASE, 1, "this")))
    match = match_compound_target(target, text, TextRange(18, 18), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range, TextRange(8, 12))

  def test_match_phrase_homophone(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.PHRASE, 1, "ipsum there sit")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum dolor sit")

  def test_selection_at_start(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ips")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(0, 4), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum")

  def test_selection_at_end(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ips")))
    match = match_compound_target(target, _SAMPLE_TEXT,
                                  TextRange(len(_SAMPLE_TEXT), len(_SAMPLE_TEXT)),
                                  UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum")

  def test_selection_in_token(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ips")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(9, 10), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ips")

  def test_empty_selection(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ips")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(200, 200), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "ipsum")

  def test_match_first_word(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "lor")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "Lorem")

  def test_match_last_word(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "conseq")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "consequat")

  def test_match_last_dot(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, ".")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(210, 220), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range, TextRange(230, 231))
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), ".")

  def test_match_closest_token_no_direction(self):
    # Default to before selection.
    target = CompoundTarget(SimpleTarget(TokenMatchOptions(TokenMatchMethod.TOKEN_COUNT, 1)))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "adipiscing")

  def test_match_current_line_first(self):
    text = "line 1 test\nline 2 end test"
    target = CompoundTarget(SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START, 1, "test")))
    match = match_compound_target(target, text, TextRange(13, 14), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.start, 23)
    self.assertEqual(match.text_range.end, 27)

  def test_match_last_token(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.TOKEN_COUNT, 1), SearchDirection.BACKWARD))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "adipiscing")

  def test_match_next_token(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.TOKEN_COUNT, 1), SearchDirection.FORWARD))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "do")

  def test_match_second_last_token(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.TOKEN_COUNT, 2), SearchDirection.BACKWARD))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "consectetur")

  def test_match_second_next_token(self):
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.TOKEN_COUNT, 2), SearchDirection.FORWARD))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "eiusmod")

  def test_match_line_start(self):
    target = CompoundTarget(SimpleTarget(TokenMatchOptions(TokenMatchMethod.LINE_START, 1, "e")))
    match = match_compound_target(target, _SAMPLE_TEXT, TextRange(50, 60), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range.extract(_SAMPLE_TEXT), "et")

  def test_word_start_takes_precedence_over_fragment_start(self):
    # "type" occurs after "textflow_target_combo_type" while searching backwards.
    text = "combo type to [m.textflow_target_combo_type]"
    target = CompoundTarget(
        SimpleTarget(TokenMatchOptions(TokenMatchMethod.WORD_START_THEN_SUBSTRING, 1, "ty")))
    match = match_compound_target(target, text, TextRange(44, 44), UTILITY_FUNCTIONS)
    assert match is not None
    self.assertEqual(match.text_range, TextRange(6, 10))
