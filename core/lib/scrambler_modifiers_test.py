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

  def test_punctuation(self):
    text = "This is.a test"
    input_match = TextMatch(TextRange(0, 4))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_NEXT, 1, ".")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), ".")

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

  def test_punctuation(self):
    text = "This is.a test"
    input_match = TextMatch(TextRange(14, 14))
    modifier = Modifier(ModifierType.WORD_SUBSTRING_PREVIOUS, 1, ".")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), ".")

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

  def test_no_match(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.PHRASE_NEXT, 1, "none")
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class PhrasePreviousTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(14, 14))
    modifier = Modifier(ModifierType.PHRASE_PREVIOUS, 1, "this")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_first_two_tokens(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.PHRASE_PREVIOUS, 1, "is is")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This is")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This is ")

  def test_homophone_expansion(self):
    text = "Test they're here"
    input_match = TextMatch(TextRange(17, 17))
    modifier = Modifier(ModifierType.PHRASE_PREVIOUS, 1, "there here")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "they're here")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " they're here")

  def test_no_match(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.PHRASE_PREVIOUS, 1, "none")
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class PhraseClosestTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(14, 14))
    modifier = Modifier(ModifierType.PHRASE_CLOSEST, 1, "this")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_match_before(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(8, 8))
    modifier = Modifier(ModifierType.PHRASE_CLOSEST, 1, "test")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "Test ")

  def test_match_after(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(12, 12))
    modifier = Modifier(ModifierType.PHRASE_CLOSEST, 1, "test")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " test")

  def test_match_before_substring(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(8, 8))
    modifier = Modifier(ModifierType.PHRASE_CLOSEST, 1, "es")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "Test ")

  def test_match_after_substring(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(12, 12))
    modifier = Modifier(ModifierType.PHRASE_CLOSEST, 1, "es")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " test")

  def test_no_match(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.PHRASE_CLOSEST, 1, "none")
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class ExactWordNextTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.EXACT_WORD_NEXT, 1, "this")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_second_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.EXACT_WORD_NEXT, 1, "is")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 5)  # Make sure we didn't match inside "This".
    self.assertEqual(result.text_range.extract(text), "is")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is ")

  def test_match_apostrophe_separator(self):
    text = "Fake this'is'a'token test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.EXACT_WORD_NEXT, 1, "a")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 13)  # Make sure we didn't match inside "fake".
    self.assertEqual(result.text_range.extract(text), "a")
    self.assertIsNone(result.deletion_range)

  def test_no_match_inside_token(self):
    text = "Fake this_is_a_token test"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.EXACT_WORD_NEXT, 1, "a")
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class ExactWordPreviousTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(14, 14))
    modifier = Modifier(ModifierType.EXACT_WORD_PREVIOUS, 1, "this")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_second_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(14, 14))
    modifier = Modifier(ModifierType.EXACT_WORD_PREVIOUS, 1, "is")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 5)  # Make sure we didn't match inside "This".
    self.assertEqual(result.text_range.extract(text), "is")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "is ")

  def test_match_apostrophe_separator(self):
    text = "Fake this'is'a'token test"
    input_match = TextMatch(TextRange(21, 24))
    modifier = Modifier(ModifierType.EXACT_WORD_PREVIOUS, 1, "a")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 13)  # Make sure we didn't match inside "fake".
    self.assertEqual(result.text_range.extract(text), "a")
    self.assertIsNone(result.deletion_range)

  def test_no_match_inside_token(self):
    text = "Fake this_is_a_token test"
    input_match = TextMatch(TextRange(24, 24))
    modifier = Modifier(ModifierType.EXACT_WORD_PREVIOUS, 1, "a")
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class ExactWordClosestTestCase(unittest.TestCase):

  def test_first_token(self):
    text = "This is a test"
    input_match = TextMatch(TextRange(14, 14))
    modifier = Modifier(ModifierType.EXACT_WORD_CLOSEST, 1, "this")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This ")

  def test_match_before(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(8, 8))
    modifier = Modifier(ModifierType.EXACT_WORD_CLOSEST, 1, "test")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "Test ")

  def test_match_after(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(12, 12))
    modifier = Modifier(ModifierType.EXACT_WORD_CLOSEST, 1, "test")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " test")

  def test_no_match_for_substring(self):
    text = "Test and another test"
    input_match = TextMatch(TextRange(8, 8))
    modifier = Modifier(ModifierType.EXACT_WORD_CLOSEST, 1, "es")
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class TestCommentModifier(unittest.TestCase):

  def test_apply_comment_modifier_single_line(self):
    text = "This is a #test comment string."
    input_match = TextMatch(TextRange(11, 15))  # "test"
    modifier = Modifier(ModifierType.COMMENT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "#test comment string.")

  def test_line_comment_between_code(self):
    text = "y -= 4\n# My comment.\nx += 5"
    input_match = TextMatch(TextRange(9, 11))  # "My"
    modifier = Modifier(ModifierType.COMMENT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "# My comment.")

  def test_apply_comment_modifier_multi_line(self):
    text = "This is a /*test comment\nmultiline string.*/"
    input_match = TextMatch(TextRange(12, 16))  # "test"
    modifier = Modifier(ModifierType.COMMENT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "/*test comment\nmultiline string.*/")

  def test_apply_comment_modifier_multi_line_cursor_in_delimiter(self):
    text = "This is a /*test comment\nmultiline string.*/"
    input_match = TextMatch(TextRange(11, 11))
    modifier = Modifier(ModifierType.COMMENT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "/*test comment\nmultiline string.*/")

  def test_apply_comment_modifier_c_style_line_comment(self):
    text = "This is a //test comment string."
    input_match = TextMatch(TextRange(12, 16))  # "test"
    modifier = Modifier(ModifierType.COMMENT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "//test comment string.")

  def test_apply_comment_modifier_nested_comments(self):
    text = "This is a /*test comment\nnested multiline string.\nend of comment*/"
    input_match = TextMatch(TextRange(12, 16))  # "test"
    modifier = Modifier(ModifierType.COMMENT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text),
                     "/*test comment\nnested multiline string.\nend of comment*/")

  def test_apply_comment_modifier_no_comment(self):
    text = "This is a test string with no comment."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.COMMENT, 1)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, input_match)

  def test_apply_comment_modifier_invalid_match(self):
    text = "This is a #test comment string."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.COMMENT, 1)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class TestArgumentModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0), TextRange(0, 0))
    modifier = Modifier(ModifierType.ARGUMENT)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_simple_call(self):
    text = "my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(14, 15))
    modifier = Modifier(ModifierType.ARGUMENT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg2")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), ", arg2")

  def test_for_loop(self):
    text = "for (arg1; arg2; arg3);"
    input_match = TextMatch(TextRange(12, 13))
    modifier = Modifier(ModifierType.ARGUMENT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg2")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "; arg2")

  def test_for_loop_first_arg(self):
    text = "for (arg1; arg2; arg3);"
    input_match = TextMatch(TextRange(6, 7))
    modifier = Modifier(ModifierType.ARGUMENT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg1")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "arg1; ")

  def test_first_argument(self):
    text = "my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(9, 10))
    modifier = Modifier(ModifierType.ARGUMENT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg1")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "arg1, ")

  def test_last_argument(self):
    text = "my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(21, 22))
    modifier = Modifier(ModifierType.ARGUMENT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg3")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), ", arg3")

  def test_surrounding_whitespace(self):
    text = "my_func( arg );"
    input_match = TextMatch(TextRange(10, 11))
    modifier = Modifier(ModifierType.ARGUMENT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " arg ")

  def test_nested_call_before(self):
    text = "f1(arg1, f2(arg2), arg3);"
    input_match = TextMatch(TextRange(17, 17))
    modifier = Modifier(ModifierType.ARGUMENT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "f2(arg2)")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), ", f2(arg2)")

  def test_nested_call_after(self):
    text = "f1(arg1, f2(arg2), arg3);"
    input_match = TextMatch(TextRange(10, 11))
    modifier = Modifier(ModifierType.ARGUMENT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "f2(arg2)")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), ", f2(arg2)")


class TestArgumentFirstModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0), TextRange(0, 0))
    modifier = Modifier(ModifierType.ARGUMENT_FIRST)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_simple_call(self):
    text = "my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.ARGUMENT_FIRST)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg1")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "arg1, ")

  def test_skip_empty_call(self):
    text = "first_call().my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.ARGUMENT_FIRST)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg1")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "arg1, ")


class TestArgumentNextModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0), TextRange(0, 0))
    modifier = Modifier(ModifierType.ARGUMENT_NEXT)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_simple_call(self):
    text = "my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(9, 10))
    modifier = Modifier(ModifierType.ARGUMENT_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg2")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), ", arg2")


class TestArgumentPreviousModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0), TextRange(0, 0))
    modifier = Modifier(ModifierType.ARGUMENT_PREVIOUS)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_simple_call(self):
    text = "my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(15, 16))
    modifier = Modifier(ModifierType.ARGUMENT_PREVIOUS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "arg1")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "arg1, ")


class TestFunctionCallModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.FUNCTION_CALL)
    self.assertEqual(apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS), input_match)

  def test_single_call(self):
    text = "func(x, y);"
    input_match = TextMatch(TextRange(1, 2))
    modifier = Modifier(ModifierType.FUNCTION_CALL)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "func(x, y)")

  def test_single_call_cursor_at_func_name_start(self):
    text = "func(x, y);"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.FUNCTION_CALL)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "func(x, y)")

  def test_single_call_cursor_at_open_parenthesis(self):
    text = "func(x, y);"
    input_match = TextMatch(TextRange(4, 4))
    modifier = Modifier(ModifierType.FUNCTION_CALL)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "func(x, y)")

  def test_single_call_c_namespace(self):
    text = "namespace::func(x, y);"
    input_match = TextMatch(TextRange(12, 12))
    modifier = Modifier(ModifierType.FUNCTION_CALL)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "namespace::func(x, y)")

  def test_nested_call(self):
    text = "func(x, func2(y));"
    input_match = TextMatch(TextRange(1, 2))
    modifier = Modifier(ModifierType.FUNCTION_CALL)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "func(x, func2(y))")

  def test_complex_call(self):
    text = "(*obj)->get_thing().field[0].method(arg1, &arg2, arg3);"
    input_match = TextMatch(TextRange(20, 21))
    modifier = Modifier(ModifierType.FUNCTION_CALL)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text),
                     "(*obj)->get_thing().field[0].method(arg1, &arg2, arg3)")

  def test_parenthesis_before_call(self):
    text = "(func(x, func2(y));"
    input_match = TextMatch(TextRange(2, 3))
    modifier = Modifier(ModifierType.FUNCTION_CALL)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "func(x, func2(y))")


class TestFunctionCallNextModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.FUNCTION_CALL_NEXT)
    self.assertEqual(apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS), input_match)

  def test_single_call(self):
    text = "test func(x, y);"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.FUNCTION_CALL_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "func(x, y)")

  def test_extra_parens(self):
    text = "test (func(x, y));"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.FUNCTION_CALL_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "func(x, y)")


class TestFunctionCallPreviousModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.FUNCTION_CALL_PREVIOUS)
    self.assertEqual(apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS), input_match)

  def test_single_call(self):
    text = "test func1(x, y); func2(a, b);"
    input_match = TextMatch(TextRange(20, 20))
    modifier = Modifier(ModifierType.FUNCTION_CALL_PREVIOUS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "func1(x, y)")

  def test_extra_parens(self):
    text = "test (func1(x, y)); (func2(a, b));"
    input_match = TextMatch(TextRange(22, 22))
    modifier = Modifier(ModifierType.FUNCTION_CALL_PREVIOUS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "func1(x, y)")


class TestStringModifier(unittest.TestCase):

  def test_single_string(self):
    text = "This is a \"test string\"."
    input_match = TextMatch(TextRange(11, 15))  # "test"
    modifier = Modifier(ModifierType.STRING)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test string")

  def test_different_delimiter(self):
    text = "This is a 'test string'."
    input_match = TextMatch(TextRange(11, 15))  # "test"
    modifier = Modifier(ModifierType.STRING, delimiter="'")
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test string")

  def test_nested_string(self):
    text = "This is a \"nested \"test\" string\"."
    input_match = TextMatch(TextRange(19, 23))  # "test"
    modifier = Modifier(ModifierType.STRING)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")

  def test_nested_string_outside(self):
    text = "This is a \"nested \"test\" string\"."
    input_match = TextMatch(TextRange(11, 17))  # "nested"
    modifier = Modifier(ModifierType.STRING)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "nested ")

  def test_multiple_strings(self):
    text = "This is a \"test string\" and \"another string\"."
    input_match = TextMatch(TextRange(11, 15))  # "test"
    modifier = Modifier(ModifierType.STRING)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test string")

  def test_no_string(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.STRING)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    # Modifier does not modify result.
    self.assertEqual(result.text_range.extract(text), "This is a test string.")

  def test_invalid_match(self):
    text = "This is a \"test string\"."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.STRING)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class TestStringFirstModifier(unittest.TestCase):

  def test_single_string(self):
    text = "This is a \"test string\"."
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.STRING_FIRST)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test string")

  def test_docstring(self):
    text = "This is a \"\"\"test string\"\"\"."
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.STRING_FIRST)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test string")


class TestStringNextModifier(unittest.TestCase):

  def test_simple_strings(self):
    text = "This is \"string1\" and \"string2\"."
    input_match = TextMatch(TextRange(11, 12))
    modifier = Modifier(ModifierType.STRING_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "string2")

  def test_docstring(self):
    text = "This is \"\"\"string1\"\"\" and \"\"\"string2\"\"\"."
    input_match = TextMatch(TextRange(11, 12))
    modifier = Modifier(ModifierType.STRING_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "string2")


class TestStringPreviousModifier(unittest.TestCase):

  def test_simple_strings(self):
    text = "This is \"string1\" and \"string2\"."
    input_match = TextMatch(TextRange(27, 27))
    modifier = Modifier(ModifierType.STRING_PREVIOUS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "string1")

  def test_docstring(self):
    text = "This is \"\"\"string1\"\"\" and \"\"\"string2\"\"\"."
    input_match = TextMatch(TextRange(30, 30))
    modifier = Modifier(ModifierType.STRING_PREVIOUS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "string1")


class TestPythonScopeModifier(unittest.TestCase):

  def test_not_in_code(self):
    text = "\n\nprint('Hello, world!')"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_single_line(self):
    text = "print('Hello, world!')"
    input_match = TextMatch(TextRange(7, 12))
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "print('Hello, world!')")

  def test_single_line_cursor_at_file_start(self):
    text = "print('Hello, world!')"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "print('Hello, world!')")

  def test_single_line_trailing_newline(self):
    text = "print('Hello, world!')\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "print('Hello, world!')\n")

  def test_function(self):
    text = """
      def test_function():
          print('Hello, world!')
          x = 5
          y = x + 1
          return y

      def test_function2():
          print('Test!')
          a = 3
    """
    input_match = TextMatch(TextRange(38, 43))  # print
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 28)
    self.assertEqual(result.text_range.end, 116)

  def test_function_with_indentation(self):
    text = """
      def test_function():
          print('Hello, world!')
          if x > 6:
            x = x + 5
          return x

      def test_function2():
          print('Test!')
          a = 3
    """
    input_match = TextMatch(TextRange(38, 43))  # print
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 28)
    self.assertEqual(result.text_range.end, 122)

  def test_function_with_empty_linw(self):
    # "Empty" line has some space characters.
    text = """
      def test_function():
          print('Hello, world!')

          x = x + 5
          return x

      def test_function2():
          print('Test!')
          a = 3
    """
    input_match = TextMatch(TextRange(38, 43))  # print
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 28)
    self.assertEqual(result.text_range.end, 101)


class TestCScopeModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.C_SCOPE)
    self.assertEqual(apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS), input_match)

  def test_not_in_code(self):
    text = "\n\ncout << \"Hello, world!\";"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "\ncout << \"Hello, world!\";")

  def test_opening_brace_only(self):
    text = "{"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 1)
    self.assertEqual(result.text_range.end, 1)

  def test_single_line(self):
    text = "{ cout << \"Hello, world!\"; }"
    input_match = TextMatch(TextRange(11, 16))  # "Hello"
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), " cout << \"Hello, world!\";")

  def test_function(self):
    text = """
      void test_function() {
          cout << "Hello, world!";
          int x = 5;
          int y = x + 1;
      }

      void test_function2() {
          cout << "Test!";
          int a = 3;
      }
    """
    input_match = TextMatch(TextRange(49, 54))  # "Hello"
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 30)
    self.assertEqual(result.text_range.end, 111)

  def test_function_nested_before(self):
    text = """
      void test_function() {
          cout << "Hello, world!";
          int x = 5;
          if (x > 6) {
            x = x + 5;
          }
          int y = x + 1;
      }

      void test_function2() {
          cout << "Test!";
          int a = 3;
      }
    """
    input_match = TextMatch(TextRange(154, 157))  # "int"
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 30)
    self.assertEqual(result.text_range.end, 169)

  def test_function_nested_after(self):
    text = """
      void test_function() {
          cout << "Hello, world!";
          int x = 5;
          if (x > 6) {
            x = x + 5;
          }
          int y = x + 1;
      }

      void test_function2() {
          cout << "Test!";
          int a = 3;
      }
    """
    input_match = TextMatch(TextRange(49, 54))  # "Hello"
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.start, 30)
    self.assertEqual(result.text_range.end, 169)


class TestSentenceModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0), TextRange(0, 0))
    modifier = Modifier(ModifierType.SENTENCE)
    self.assertEqual(apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS), input_match)

  def test_single_sentence(self):
    text = "This is a sentence."
    input_match = TextMatch(TextRange(7, 9))
    modifier = Modifier(ModifierType.SENTENCE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This is a sentence.")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This is a sentence.")

  def test_first_sentence(self):
    text = "This is a sentence. Here is another sentence!"
    input_match = TextMatch(TextRange(7, 9))
    modifier = Modifier(ModifierType.SENTENCE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This is a sentence.")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This is a sentence. ")

  def test_last_sentence(self):
    text = "This is a sentence. Here is another sentence!"
    input_match = TextMatch(TextRange(25, 27))
    modifier = Modifier(ModifierType.SENTENCE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Here is another sentence!")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " Here is another sentence!")

  def test_newline_delimited(self):
    text = "## Markdown Header\n\nThis is my sentence."
    input_match = TextMatch(TextRange(25, 27))
    modifier = Modifier(ModifierType.SENTENCE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This is my sentence.")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This is my sentence.")


class TestSentenceNextModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0), TextRange(0, 0))
    modifier = Modifier(ModifierType.SENTENCE_NEXT)
    self.assertEqual(apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS), input_match)

  def test_simple_sentence(self):
    text = "Sentence one. Sentence two."
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.SENTENCE_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Sentence two.")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " Sentence two.")

  def test_end_of_sentence_selected(self):
    text = "Sentence one. Sentence two."
    input_match = TextMatch(TextRange(0, 13))
    modifier = Modifier(ModifierType.SENTENCE_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Sentence two.")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " Sentence two.")


class TestSentencePreviousModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0), TextRange(0, 0))
    modifier = Modifier(ModifierType.SENTENCE_PREVIOUS)
    self.assertEqual(apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS), input_match)

  def test_simple_sentence(self):
    text = "Sentence one. Sentence two."
    input_match = TextMatch(TextRange(20, 20))
    modifier = Modifier(ModifierType.SENTENCE_PREVIOUS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Sentence one.")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "Sentence one. ")


class TestSentenceClauseModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.SENTENCE_CLAUSE)
    self.assertEqual(apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS), input_match)

  def test_clause(self):
    text = "This is the first clause, this is the second."
    input_match = TextMatch(TextRange(29, 29))
    modifier = Modifier(ModifierType.SENTENCE_CLAUSE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "this is the second")

  def test_clause_colon(self):
    text = "This is the first clause: this is the second."
    input_match = TextMatch(TextRange(29, 29))
    modifier = Modifier(ModifierType.SENTENCE_CLAUSE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "this is the second")

  def test_clause_trailing_line_break(self):
    text = "This is the first clause: this is the second\n"
    input_match = TextMatch(TextRange(29, 29))
    modifier = Modifier(ModifierType.SENTENCE_CLAUSE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "this is the second")


class TestBracketModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.BRACKETS)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_simple_brackets(self):
    text = "[test]"
    input_match = TextMatch(TextRange(1, 2))
    modifier = Modifier(ModifierType.BRACKETS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")

  def test_no_opening_bracket(self):
    text = "test]"
    input_match = TextMatch(TextRange(1, 2))
    modifier = Modifier(ModifierType.BRACKETS)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_nested_brackets_outside(self):
    text = "([test])"
    input_match = TextMatch(TextRange(2, 3))
    modifier = Modifier(ModifierType.BRACKETS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")

  def test_nested_brackets_before(self):
    text = "[before[nest]after]"
    input_match = TextMatch(TextRange(14, 15))
    modifier = Modifier(ModifierType.BRACKETS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "before[nest]after")

  def test_nested_brackets_after(self):
    text = "[before[nest]after]"
    input_match = TextMatch(TextRange(3, 4))
    modifier = Modifier(ModifierType.BRACKETS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "before[nest]after")


class TestBracketFirstModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.BRACKETS_FIRST)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_simple_brackets(self):
    text = "outside [test]"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.BRACKETS_FIRST)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")

  def test_comparison(self):
    text = "less < more [test]"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.BRACKETS_FIRST)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test")


class TestBracketNextModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.BRACKETS_NEXT)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_simple_brackets(self):
    text = "(test1) [test2]"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.BRACKETS_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test2")

  def test_comparison(self):
    text = "(test1) less < more [test2]"
    input_match = TextMatch(TextRange(3, 3))
    modifier = Modifier(ModifierType.BRACKETS_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test2")

  def test_comparison_inside_bracket(self):
    text = "(test1 a > b) less < more [test2]"
    input_match = TextMatch(TextRange(3, 3))
    modifier = Modifier(ModifierType.BRACKETS_NEXT)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test2")


class TestBracketPreviousModifier(unittest.TestCase):

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.BRACKETS_PREVIOUS)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

  def test_simple_brackets(self):
    text = "(test1) [test2]"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.BRACKETS_PREVIOUS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test1")

  def test_comparison(self):
    text = "(test1) most > less < more [test2]"
    input_match = TextMatch(TextRange(30, 30))
    modifier = Modifier(ModifierType.BRACKETS_PREVIOUS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test1")

  def test_comparison_inside_brackets(self):
    text = "(test1) most > less < more [a < b test2]"
    input_match = TextMatch(TextRange(35, 35))
    modifier = Modifier(ModifierType.BRACKETS_PREVIOUS)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "test1")


class TestStartOfLineModifier(unittest.TestCase):

  def test_single_line(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.START_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(0, 0)))

  def test_trailing_newline(self):
    text = "This is a test string.\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.START_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_multi_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.START_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(0, 0)))

  def test_last_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.START_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_middle_line(self):
    text = "This is a test string.\nAnother line of text.\nThe last line."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.START_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))


class TestEndOfLineModifier(unittest.TestCase):

  def test_single_line(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.END_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(22, 22)))

  def test_trailing_newline(self):
    text = "This is a test string.\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.END_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_multi_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.END_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_last_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.END_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(44, 44)))

  def test_middle_line(self):
    text = "This is a test string.\nAnother line of text.\nThe last line."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.END_OF_LINE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(45, 45)))


class TestBetweenWhitespaceModifier(unittest.TestCase):

  def test_single_word(self):
    text = "test"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(0, 4), deletion_range=TextRange(0, 4)))

  def test_sentence(self):
    text = "This is a test."
    input_match = TextMatch(TextRange(5, 5))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(5, 7), deletion_range=TextRange(5, 8)))

  def test_end_of_sentence(self):
    text = "This is a test."
    input_match = TextMatch(TextRange(11, 12))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(10, 15), deletion_range=TextRange(9, 15)))

  def test_line_breaks(self):
    text = "This\nis\na test."
    input_match = TextMatch(TextRange(5, 5))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(5, 7), deletion_range=TextRange(5, 8)))

  def test_path_in_sentence(self):
    text = "Path ~/test/a_b/c-d/* is invalid."
    input_match = TextMatch(TextRange(6, 7))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(5, 21), deletion_range=TextRange(5, 22)))


class TestMarkdownLinkModifier(unittest.TestCase):

  def test_link_only(self):
    text = "[link](url)"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.MARKDOWN_LINK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(0, 11)))

  def test_from_link_text(self):
    text = "This is a [link](url) to a site"
    input_match = TextMatch(TextRange(12, 13))
    modifier = Modifier(ModifierType.MARKDOWN_LINK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(10, 21)))

  def test_from_url(self):
    text = "This is a [link](url) to a site"
    input_match = TextMatch(TextRange(18, 19))
    modifier = Modifier(ModifierType.MARKDOWN_LINK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(10, 21)))

  def test_from_link_text_bracket(self):
    text = "This is a [link](url) to a site"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.MARKDOWN_LINK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(10, 21)))

  def test_from_url_bracket(self):
    text = "This is a [link](url) to a site"
    input_match = TextMatch(TextRange(21, 21))
    modifier = Modifier(ModifierType.MARKDOWN_LINK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(10, 21)))


class TestMarkdownSectionEndModifier(unittest.TestCase):

  def test_no_headings(self):
    text = "[link](url)"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.MARKDOWN_SECTION_END)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(11, 11)))

  def test_from_start_of_heading(self):
    text = "## Heading\nTest line one\nTest line two\n\n## Next Heading"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.MARKDOWN_SECTION_END)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))

  def test_from_end_of_heading(self):
    text = "## Heading\nTest line one\nTest line two\n\n## Next Heading"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.MARKDOWN_SECTION_END)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))

  def test_from_after_heading(self):
    text = "## Heading\nTest line one\nTest line two\n\n## Next Heading"
    input_match = TextMatch(TextRange(11, 11))
    modifier = Modifier(ModifierType.MARKDOWN_SECTION_END)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))

  def test_from_whitespace_before_next_heading(self):
    text = "## Heading\nTest line one\nTest line two\n\n## Next Heading"
    input_match = TextMatch(TextRange(39, 39))
    modifier = Modifier(ModifierType.MARKDOWN_SECTION_END)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))

  def test_search_until_eof(self):
    text = "## Heading\nTest line one\nTest line two\n\n"
    input_match = TextMatch(TextRange(13, 13))
    modifier = Modifier(ModifierType.MARKDOWN_SECTION_END)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))


class TestLineIncludingLineBreakModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_apply_line_modifier_single_line(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This is a test string.")

  def test_apply_line_modifier_trailing_newline(self):
    text = "This is a test string.\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "")

  def test_apply_line_modifier_multi_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This is a test string.\n")

  def test_apply_line_modifier_last_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Another line of text.")

  def test_apply_line_modifier_middle_line(self):
    text = "This is a test string.\nAnother line of text.\nThe last line."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Another line of text.\n")

  def test_apply_line_modifier_empty_line(self):
    text = "This is a test string.\n\nAnother line of text."
    input_match = TextMatch(TextRange(23, 23))  # empty line
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)

    self.assertEqual(result, TextMatch(TextRange(23, 24)))

  def test_apply_line_modifier_invalid_match(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)


class TestLineExcludingLineBreakModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_apply_line_modifier_single_line(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This is a test string.")

  def test_apply_line_modifier_trailing_newline(self):
    text = "This is a test string.\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "")

  def test_apply_line_modifier_multi_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "This is a test string.")

  def test_apply_line_modifier_last_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Another line of text.")

  def test_apply_line_modifier_middle_line(self):
    text = "This is a test string.\nAnother line of text.\nThe last line."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result.text_range.extract(text), "Another line of text.")

  def test_apply_line_modifier_empty_line(self):
    text = "This is a test string.\n\nAnother line of text."
    input_match = TextMatch(TextRange(23, 23))  # empty line
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK)
    result = apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_apply_line_modifier_invalid_match(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier, UTILITY_FUNCTIONS)
