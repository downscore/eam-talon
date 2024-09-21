# pylint: disable=missing-module-docstring, missing-class-docstring
import unittest

from .scrambler_modifiers import *  # pylint: disable=wildcard-import, unused-wildcard-import
from .scrambler_test_util import UTILITY_FUNCTIONS


class ApplyModifierTestCase(unittest.TestCase):

  def test_match_beyond_text(self):
    with self.assertRaises(ValueError):
      apply_modifier("This is a test", TextMatch(TextRange(0, 100)),
                     Modifier(ModifierType.TOKEN_NEXT, 1), UTILITY_FUNCTIONS)

  def test_deletion_range_beyond_text(self):
    with self.assertRaises(ValueError):
      apply_modifier("This is a test", TextMatch(TextRange(0, 0), TextRange(0, 100)),
                     Modifier(ModifierType.TOKEN_NEXT, 1), UTILITY_FUNCTIONS)


class GetPhraseRegexTestCase(unittest.TestCase):
  """Tests for getting a regex to match a phrase."""

  def test_get_phrase_regex(self):
    sep = r"[ .,\-\_\"]*"
    self.assertEqual(get_phrase_regex([], UTILITY_FUNCTIONS.get_homophones), "")
    # Note: No parens in regex when a word has no homophones.
    self.assertEqual(get_phrase_regex(["a"], UTILITY_FUNCTIONS.get_homophones), "a")
    self.assertEqual(get_phrase_regex("a b".split(" "), UTILITY_FUNCTIONS.get_homophones),
                     f"a{sep}b")  # type: ignore
    self.assertEqual(
        get_phrase_regex("we are there".split(" "),
                         UTILITY_FUNCTIONS.get_homophones),  # type: ignore
        f"we{sep}are{sep}(there|their|they're|dolor)")


class TokenNextTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_second_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 4))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is ")

  def test_last_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " test")

  def test_partial_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "his")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "his ")

  def test_comma_after_token(self):
    text = "Hello world, goodbye"
    input_match = TextMatch(TextRange(5, 5))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "world")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "world, ")

  def test_multiple_sentences(self):
    text = "First sentence. Second here."
    input_match = TextMatch(TextRange(5, 5))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "sentence")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " sentence")

  def test_single_token(self):
    text = "test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    self.assertIsNone(result.deletion_range)

  def test_underscore_in_token(self):
    text = "This is_a test"
    input_match = TextMatch(TextRange(0, 4))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is_a")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is_a ")

  def test_dot_between_tokens(self):
    text = "This is.a test"
    input_match = TextMatch(TextRange(0, 4))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " is")

  def test_no_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(14, 14))
    modifier = Modifier(ModifierType.TOKEN_NEXT, 1)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class TokenPreviousTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(5, 5))
    modifier = Modifier(ModifierType.TOKEN_PREVIOUS, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_second_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(7, 9))
    modifier = Modifier(ModifierType.TOKEN_PREVIOUS, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is ")

  def test_last_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(14, 14))
    modifier = Modifier(ModifierType.TOKEN_PREVIOUS, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " test")

  def test_partial_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(2, 4))
    modifier = Modifier(ModifierType.TOKEN_PREVIOUS, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Th")
    self.assertIsNone(result.deletion_range)

  def test_single_token(self):
    text = "test"
    input_match = TextMatch(TextRange(4, 4))
    modifier = Modifier(ModifierType.TOKEN_PREVIOUS, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    self.assertIsNone(result.deletion_range)

  def test_comma_after_token(self):
    text = "Hello world, goodbye"
    input_match = TextMatch(TextRange(13, 13))
    modifier = Modifier(ModifierType.TOKEN_PREVIOUS, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "world")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "world, ")

  def test_underscore_in_token(self):
    text = "This is_a test"
    input_match = TextMatch(TextRange(10, 14))
    modifier = Modifier(ModifierType.TOKEN_PREVIOUS, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is_a")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is_a ")

  def test_dot_between_tokens(self):
    text = "This is.a test"
    input_match = TextMatch(TextRange(8, 9))
    modifier = Modifier(ModifierType.TOKEN_PREVIOUS, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " is")

  def test_no_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.TOKEN_PREVIOUS, 1)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class WordSubstringNextTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_NEXT, 1, "this")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_second_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_NEXT, 1, "is")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is")
    self.assertEqual(result.text_range.start, 5)  # Make sure we didn't match inside "This".
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is ")

  def test_last_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(4, 6))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_NEXT, 1, "es")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " test")

  def test_underscore_in_token(self):
    text = "This is_a test"
    input_match = TextMatch(TextRange(0, 4))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_NEXT, 1, "_a")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is_a")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is_a ")

  def test_no_match(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_NEXT, 1, "none")
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class WordSubstringPreviousTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(8, 8))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_PREVIOUS, 1, "this")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_second_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_PREVIOUS, 1, "is")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is")
    self.assertEqual(result.text_range.start, 5)  # Make sure we didn't match inside "This".
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is ")

  def test_last_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(14, 14))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_PREVIOUS, 1, "es")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " test")

  def test_underscore_in_token(self):
    text = "This is_a test"
    input_match = TextMatch(TextRange(10, 14))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_PREVIOUS, 1, "is")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "is_a")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is_a ")

  def test_no_match(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_PREVIOUS, 1, "none")
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class WordSubstringClosestTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_CLOSEST, 1, "this")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_match_before(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(8, 8))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_CLOSEST, 1, "test")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "Test ")

  def test_match_after(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(12, 12))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_CLOSEST, 1, "test")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " test")

  def test_match_before_substring(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(8, 8))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_CLOSEST, 1, "es")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "Test ")

  def test_match_after_substring(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(12, 12))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_CLOSEST, 1, "es")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " test")

  def test_no_match(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_CLOSEST, 1, "none")
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class PhraseNextTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.PHRASE_NEXT, 1, "this")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_first_two_tokens(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.PHRASE_NEXT, 1, "is is")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This is")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This is ")

  def test_homophone_expansion(self):
    text = "Test they're here"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.PHRASE_NEXT, 1, "there here")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "they're here")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " they're here")
