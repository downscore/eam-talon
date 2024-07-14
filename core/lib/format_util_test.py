"""Tests for formatting utils."""

import unittest
from .format_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class FormatOptionsTestCase(unittest.TestCase):
  """Tests for fetching and combining options for different formatters."""

  def test_identity(self):
    options = get_format_options([Formatters.IDENTITY])
    self.assertEqual(options.first_capitalization, WordCapitalization.NO_CHANGE)
    self.assertEqual(options.rest_capitalization, WordCapitalization.NO_CHANGE)
    self.assertEqual(options.separator, " ")
    self.assertEqual(options.surround, "")

  def test_enum(self):
    options = get_format_options([Formatters.ENUM])
    self.assertEqual(options.first_capitalization, WordCapitalization.UPPERCASE)
    self.assertEqual(options.rest_capitalization, WordCapitalization.UPPERCASE)
    self.assertEqual(options.separator, "_")
    self.assertEqual(options.surround, "")

  def test_pascal(self):
    options = get_format_options([Formatters.PASCAL])
    self.assertEqual(options.first_capitalization, WordCapitalization.CAPITALIZE_FIRST)
    self.assertEqual(options.rest_capitalization, WordCapitalization.CAPITALIZE_FIRST)
    self.assertEqual(options.separator, "")
    self.assertEqual(options.surround, "")

  def test_lowercase_no_spaces(self):
    options = get_format_options([Formatters.LOWERCASE, Formatters.NO_SPACES])
    self.assertEqual(options.first_capitalization, WordCapitalization.LOWERCASE)
    self.assertEqual(options.rest_capitalization, WordCapitalization.LOWERCASE)
    self.assertEqual(options.separator, "")
    self.assertEqual(options.surround, "")

  def test_uppercase_title(self):
    # Combine two case formatters. Last one should take precendence.
    options = get_format_options([Formatters.UPPERCASE, Formatters.TITLE_CASE])
    self.assertEqual(options.first_capitalization,
                     WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING)
    self.assertEqual(options.rest_capitalization, WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING)
    self.assertEqual(options.separator, " ")
    self.assertEqual(options.surround, "")

  def test_slash_packed(self):
    # Combine two separator formatters. Last one should take precendence.
    options = get_format_options([Formatters.SLASH_SEPARATED, Formatters.DOUBLE_COLON_SEPARATED])
    self.assertEqual(options.first_capitalization, WordCapitalization.NO_CHANGE)
    self.assertEqual(options.rest_capitalization, WordCapitalization.NO_CHANGE)
    self.assertEqual(options.separator, "::")
    self.assertEqual(options.surround, "")

  def test_title_all_snake(self):
    # Snake formatter sets case. If it comes last, it should override another case formatter.
    options = get_format_options([Formatters.TITLE_CASE_ALL, Formatters.SNAKE])
    self.assertEqual(options.first_capitalization, WordCapitalization.LOWERCASE)
    self.assertEqual(options.rest_capitalization, WordCapitalization.LOWERCASE)
    self.assertEqual(options.separator, "_")
    self.assertEqual(options.surround, "")

  def test_dotted_sentence_space_surrounded(self):
    options = get_format_options(
        [Formatters.DOT_SEPARATED, Formatters.SENTENCE, Formatters.SPACE_SURROUNDED])
    self.assertEqual(options.first_capitalization,
                     WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING)
    self.assertEqual(options.rest_capitalization, WordCapitalization.NO_CHANGE)
    self.assertEqual(options.separator, ".")
    self.assertEqual(options.surround, " ")

  def test_camel_kebab(self):
    options = get_format_options([Formatters.CAMEL, Formatters.KEBAB])
    self.assertEqual(options.first_capitalization, WordCapitalization.LOWERCASE)
    self.assertEqual(options.rest_capitalization, WordCapitalization.CAPITALIZE_FIRST)
    self.assertEqual(options.separator, "-")
    self.assertEqual(options.surround, "")


class CapitalizationTestCase(unittest.TestCase):
  """Tests for different ways of capitalizing a word."""

  def test_capitalization(self):
    self.assertEqual(format_word_capitalization("eXAmple", WordCapitalization.NO_CHANGE), "eXAmple")
    self.assertEqual(format_word_capitalization("eXAmple", WordCapitalization.LOWERCASE), "example")
    self.assertEqual(format_word_capitalization("eXAmple", WordCapitalization.UPPERCASE), "EXAMPLE")
    self.assertEqual(format_word_capitalization("eXAmple", WordCapitalization.CAPITALIZE_FIRST),
                     "Example")
    self.assertEqual(format_word_capitalization("aND", WordCapitalization.CAPITALIZE_FIRST), "And")
    self.assertEqual(format_word_capitalization("eXAmple", WordCapitalization.TITLE_CASE),
                     "Example")
    self.assertEqual(format_word_capitalization("aND", WordCapitalization.TITLE_CASE), "and")
    self.assertEqual(
        format_word_capitalization("eXAmple",
                                   WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING),
        "EXAmple")
    self.assertEqual(
        format_word_capitalization("aNd", WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING),
        "ANd")
    self.assertEqual(
        format_word_capitalization("eXAmple", WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING),
        "EXAmple")
    self.assertEqual(
        format_word_capitalization("aND", WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING), "and")

  def test_capitalization_empty(self):
    # Empty input should always return empty output.
    self.assertEqual(format_word_capitalization("", WordCapitalization.NO_CHANGE), "")
    self.assertEqual(format_word_capitalization("", WordCapitalization.LOWERCASE), "")
    self.assertEqual(format_word_capitalization("", WordCapitalization.UPPERCASE), "")
    self.assertEqual(format_word_capitalization("", WordCapitalization.CAPITALIZE_FIRST), "")
    self.assertEqual(format_word_capitalization("", WordCapitalization.TITLE_CASE), "")
    self.assertEqual(
        format_word_capitalization("", WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING), "")
    self.assertEqual(
        format_word_capitalization("", WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING), "")

  def test_capitalization_single_char(self):
    # Single character input should behave as expected.
    self.assertEqual(format_word_capitalization("a", WordCapitalization.NO_CHANGE), "a")
    self.assertEqual(format_word_capitalization("A", WordCapitalization.LOWERCASE), "a")
    self.assertEqual(format_word_capitalization("a", WordCapitalization.UPPERCASE), "A")
    self.assertEqual(format_word_capitalization("a", WordCapitalization.CAPITALIZE_FIRST), "A")
    self.assertEqual(format_word_capitalization("a", WordCapitalization.TITLE_CASE), "a")
    self.assertEqual(format_word_capitalization("b", WordCapitalization.TITLE_CASE), "B")
    self.assertEqual(
        format_word_capitalization("a", WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING),
        "A")
    self.assertEqual(
        format_word_capitalization("a", WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING), "a")
    self.assertEqual(
        format_word_capitalization("b", WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING), "B")

  def test_capitalization_invalid(self):
    # Two words should throw an exception.
    with self.assertRaises(ValueError):
      format_word_capitalization("two words", WordCapitalization.NO_CHANGE)


class FormatPhraseTestCase(unittest.TestCase):
  """Tests for formatting full phrases of space-separated words."""

  def test_format_phrase_identity(self):
    options = FormatOptions(first_capitalization=WordCapitalization.NO_CHANGE,
                            rest_capitalization=WordCapitalization.NO_CHANGE,
                            separator=" ",
                            surround="")
    self.assertEqual(format_phrase("", options), "")
    self.assertEqual(format_phrase(" ", options), "")
    self.assertEqual(format_phrase("  ", options), "")
    self.assertEqual(format_phrase("a", options), "a")
    self.assertEqual(format_phrase("ab", options), "ab")
    self.assertEqual(format_phrase("5", options), "5")
    self.assertEqual(format_phrase("this is a test", options), "this is a test")
    self.assertEqual(format_phrase("this is a test.", options), "this is a test.")
    self.assertEqual(format_phrase("thIS is a teSt", options), "thIS is a teSt")
    self.assertEqual(format_phrase("this is a3 test", options), "this is a3 test")
    self.assertEqual(format_phrase("this is a 3 test", options), "this is a 3 test")

  def test_format_phrase_sentence(self):
    options = FormatOptions(
        first_capitalization=WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING,
        rest_capitalization=WordCapitalization.NO_CHANGE,
        separator=" ",
        surround="")
    self.assertEqual(format_phrase("", options), "")
    self.assertEqual(format_phrase(" ", options), "")
    self.assertEqual(format_phrase("  ", options), "")
    self.assertEqual(format_phrase("\t", options), "")
    self.assertEqual(format_phrase(" \t ", options), "")
    self.assertEqual(format_phrase("a", options), "A")
    self.assertEqual(format_phrase("ab", options), "Ab")
    self.assertEqual(format_phrase("5", options), "5")
    self.assertEqual(format_phrase("this is a test", options), "This is a test")
    self.assertEqual(format_phrase("this is a test.", options), "This is a test.")
    self.assertEqual(format_phrase("thIS is a teSt", options), "ThIS is a teSt")
    self.assertEqual(format_phrase("this is a3 test", options), "This is a3 test")
    self.assertEqual(format_phrase("this is a 3 test", options), "This is a 3 test")

  def test_format_phrase_title(self):
    options = FormatOptions(
        first_capitalization=WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING,
        rest_capitalization=WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING,
        separator=" ",
        surround="")
    self.assertEqual(format_phrase("", options), "")
    self.assertEqual(format_phrase(" ", options), "")
    self.assertEqual(format_phrase("  ", options), "")
    self.assertEqual(format_phrase("\t", options), "")
    self.assertEqual(format_phrase(" \t ", options), "")
    self.assertEqual(format_phrase("a", options), "A")
    self.assertEqual(format_phrase("ab", options), "Ab")
    self.assertEqual(format_phrase("5", options), "5")
    self.assertEqual(format_phrase("this is a test", options), "This is a Test")
    self.assertEqual(format_phrase("this is a test.", options), "This is a Test.")
    self.assertEqual(format_phrase("thIS is a teSt", options), "ThIS is a TeSt")
    self.assertEqual(format_phrase("this is a3 test", options), "This is A3 Test")
    self.assertEqual(format_phrase("this is a 3 test", options), "This is a 3 Test")

  def test_format_phrase_pascal(self):
    options = FormatOptions(first_capitalization=WordCapitalization.CAPITALIZE_FIRST,
                            rest_capitalization=WordCapitalization.CAPITALIZE_FIRST,
                            separator="",
                            surround="")
    self.assertEqual(format_phrase("", options), "")
    self.assertEqual(format_phrase(" ", options), "")
    self.assertEqual(format_phrase("  ", options), "")
    self.assertEqual(format_phrase("\t", options), "")
    self.assertEqual(format_phrase(" \t ", options), "")
    self.assertEqual(format_phrase("a", options), "A")
    self.assertEqual(format_phrase("ab", options), "Ab")
    self.assertEqual(format_phrase("5", options), "5")
    self.assertEqual(format_phrase("this is a test", options), "ThisIsATest")
    self.assertEqual(format_phrase("this is a test.", options), "ThisIsATest.")
    self.assertEqual(format_phrase("thIS is a teSt", options), "ThisIsATest")
    self.assertEqual(format_phrase("this is a3 test", options), "ThisIsA3Test")
    self.assertEqual(format_phrase("this is a 3 test", options), "ThisIsA3Test")

  def test_format_phrase_camel(self):
    options = FormatOptions(first_capitalization=WordCapitalization.LOWERCASE,
                            rest_capitalization=WordCapitalization.CAPITALIZE_FIRST,
                            separator="",
                            surround="")
    self.assertEqual(format_phrase("", options), "")
    self.assertEqual(format_phrase(" ", options), "")
    self.assertEqual(format_phrase("  ", options), "")
    self.assertEqual(format_phrase("\t", options), "")
    self.assertEqual(format_phrase(" \t ", options), "")
    self.assertEqual(format_phrase("a", options), "a")
    self.assertEqual(format_phrase("ab", options), "ab")
    self.assertEqual(format_phrase("5", options), "5")
    self.assertEqual(format_phrase("this is a test", options), "thisIsATest")
    self.assertEqual(format_phrase("this is a test.", options), "thisIsATest.")
    self.assertEqual(format_phrase("thIS is a teSt", options), "thisIsATest")
    self.assertEqual(format_phrase("this is a3 test", options), "thisIsA3Test")
    self.assertEqual(format_phrase("this is a 3 test", options), "thisIsA3Test")

  def test_format_phrase_snake(self):
    options = FormatOptions(first_capitalization=WordCapitalization.LOWERCASE,
                            rest_capitalization=WordCapitalization.LOWERCASE,
                            separator="_",
                            surround="")
    self.assertEqual(format_phrase("", options), "")
    self.assertEqual(format_phrase(" ", options), "")
    self.assertEqual(format_phrase("  ", options), "")
    self.assertEqual(format_phrase("\t", options), "")
    self.assertEqual(format_phrase(" \t ", options), "")
    self.assertEqual(format_phrase("a", options), "a")
    self.assertEqual(format_phrase("ab", options), "ab")
    self.assertEqual(format_phrase("5", options), "5")
    self.assertEqual(format_phrase("this is a test", options), "this_is_a_test")
    self.assertEqual(format_phrase("this is a test.", options), "this_is_a_test.")
    self.assertEqual(format_phrase("thIS is a teSt", options), "this_is_a_test")
    self.assertEqual(format_phrase("this is a3 test", options), "this_is_a3_test")
    self.assertEqual(format_phrase("this is a 3 test", options), "this_is_a_3_test")

  def test_format_phrase_kebab(self):
    options = FormatOptions(first_capitalization=WordCapitalization.LOWERCASE,
                            rest_capitalization=WordCapitalization.LOWERCASE,
                            separator="-",
                            surround="")
    self.assertEqual(format_phrase("", options), "")
    self.assertEqual(format_phrase(" ", options), "")
    self.assertEqual(format_phrase("  ", options), "")
    self.assertEqual(format_phrase("\t", options), "")
    self.assertEqual(format_phrase(" \t ", options), "")
    self.assertEqual(format_phrase("a", options), "a")
    self.assertEqual(format_phrase("ab", options), "ab")
    self.assertEqual(format_phrase("5", options), "5")
    self.assertEqual(format_phrase("this is a test", options), "this-is-a-test")
    self.assertEqual(format_phrase("this is a test.", options), "this-is-a-test.")
    self.assertEqual(format_phrase("thIS is a teSt", options), "this-is-a-test")
    self.assertEqual(format_phrase("this is a3 test", options), "this-is-a3-test")
    self.assertEqual(format_phrase("this is a 3 test", options), "this-is-a-3-test")

  def test_format_phrase_quoted_snake(self):
    options = FormatOptions(first_capitalization=WordCapitalization.LOWERCASE,
                            rest_capitalization=WordCapitalization.LOWERCASE,
                            separator="_",
                            surround="'")
    self.assertEqual(format_phrase("", options), "''")
    self.assertEqual(format_phrase(" ", options), "''")
    self.assertEqual(format_phrase("  ", options), "''")
    self.assertEqual(format_phrase("\t", options), "''")
    self.assertEqual(format_phrase(" \t ", options), "''")
    self.assertEqual(format_phrase("a", options), "'a'")
    self.assertEqual(format_phrase("ab", options), "'ab'")
    self.assertEqual(format_phrase("5", options), "'5'")
    self.assertEqual(format_phrase("this is a test", options), "'this_is_a_test'")
    self.assertEqual(format_phrase("this is a test.", options), "'this_is_a_test.'")
    self.assertEqual(format_phrase("thIS is a teSt", options), "'this_is_a_test'")
    self.assertEqual(format_phrase("this is a3 test", options), "'this_is_a3_test'")
    self.assertEqual(format_phrase("this is a 3 test", options), "'this_is_a_3_test'")

  def test_format_phrase_double_underscore(self):
    options = FormatOptions(first_capitalization=WordCapitalization.NO_CHANGE,
                            rest_capitalization=WordCapitalization.NO_CHANGE,
                            separator=" ",
                            surround="__")
    self.assertEqual(format_phrase("", options), "____")
    self.assertEqual(format_phrase(" ", options), "____")
    self.assertEqual(format_phrase("  ", options), "____")
    self.assertEqual(format_phrase("\t", options), "____")
    self.assertEqual(format_phrase(" \t ", options), "____")
    self.assertEqual(format_phrase("a", options), "__a__")
    self.assertEqual(format_phrase("ab", options), "__ab__")
    self.assertEqual(format_phrase("5", options), "__5__")
    self.assertEqual(format_phrase("this is a test", options), "__this is a test__")
    self.assertEqual(format_phrase("this is a test.", options), "__this is a test.__")
    self.assertEqual(format_phrase("thIS is a teSt", options), "__thIS is a teSt__")
    self.assertEqual(format_phrase("this is a3 test", options), "__this is a3 test__")
    self.assertEqual(format_phrase("this is a 3 test", options), "__this is a 3 test__")


class TitlePhraseTestCase(unittest.TestCase):
  """Tests for title case formatting."""

  def test_format_phrase_title(self):
    self.assertEqual(title_format_phrase(""), "")
    self.assertEqual(title_format_phrase(" "), "")
    self.assertEqual(title_format_phrase("  "), "")
    self.assertEqual(title_format_phrase("\t"), "")
    self.assertEqual(title_format_phrase(" \t "), "")
    self.assertEqual(title_format_phrase("a"), "A")
    self.assertEqual(title_format_phrase("ab"), "Ab")
    self.assertEqual(title_format_phrase("5"), "5")
    self.assertEqual(title_format_phrase("this is a test"), "This is a Test")
    self.assertEqual(title_format_phrase("this is a test."), "This is a Test.")
    self.assertEqual(title_format_phrase("thIS is a teSt"), "ThIS is a TeSt")
    self.assertEqual(title_format_phrase("this is a3 test"), "This is A3 Test")
    self.assertEqual(title_format_phrase("this is a 3 test"), "This is a 3 Test")
    self.assertEqual(title_format_phrase("hyphenated-title"), "Hyphenated-Title")


class UnformatPhraseTestCase(unittest.TestCase):
  """Tests for unformatting potentially already-formatted text."""

  def test_unformat(self):
    self.assertEqual(unformat_phrase(""), "")
    self.assertEqual(unformat_phrase(" "), " ")
    self.assertEqual(unformat_phrase("  "), " ")
    self.assertEqual(unformat_phrase("\t"), " ")
    self.assertEqual(unformat_phrase(" \t"), " ")
    self.assertEqual(unformat_phrase("a"), "a")
    self.assertEqual(unformat_phrase("A"), "a")
    self.assertEqual(unformat_phrase("ab"), "ab")
    self.assertEqual(unformat_phrase("5"), "5")
    self.assertEqual(unformat_phrase("this is a test"), "this is a test")
    self.assertEqual(unformat_phrase("this is a test."), "this is a test ")
    self.assertEqual(unformat_phrase("thIS is a teSt"), "th is is a te st")
    self.assertEqual(unformat_phrase("this is a 3 test"), "this is a 3 test")
    self.assertEqual(unformat_phrase("ThisIsPascalCase"), "this is pascal case")
    self.assertEqual(unformat_phrase("thisIsCamelCase"), "this is camel case")
    self.assertEqual(unformat_phrase("this-is-kebab"),
                     "this-is-kebab")  # Kebab case can't be unformatted.
    self.assertEqual(unformat_phrase("this_is_snake"), "this is snake")
    self.assertEqual(unformat_phrase("this_is-mixed"),
                     "this is-mixed")  # Kebab case can't be unformatted.
    self.assertEqual(unformat_phrase("This::Is::Packed"), "this is packed")

    # Note: Unformatting introduces a space where letters and numbers are concatenated.
    self.assertEqual(unformat_phrase("this is a3 test"), "this is a 3 test")


class NeedsSpaceBetweenTestCase(unittest.TestCase):
  """Tests for checking if two strings need a space between them."""

  def test_needs_space_between(self):
    self.assertTrue(needs_space_between("a", "break"))
    self.assertTrue(needs_space_between("break", "a"))
    self.assertTrue(needs_space_between(".", "a"))
    self.assertTrue(needs_space_between("said", "'hello"))
    self.assertTrue(needs_space_between("hello'", "said"))
    self.assertTrue(needs_space_between("hello.", "'John"))
    self.assertTrue(needs_space_between("John.'", "They"))
    self.assertTrue(needs_space_between("paid", "$50"))
    self.assertTrue(needs_space_between("50$", "payment"))
    self.assertFalse(needs_space_between("", ""))
    self.assertFalse(needs_space_between("a", ""))
    self.assertFalse(needs_space_between("a", " "))
    self.assertFalse(needs_space_between("", "a"))
    self.assertFalse(needs_space_between(" ", "a"))
    self.assertFalse(needs_space_between("a", ","))
    self.assertFalse(needs_space_between("'", "a"))
    self.assertFalse(needs_space_between("a", "'"))
    self.assertFalse(needs_space_between("and-", "or"))
    self.assertFalse(needs_space_between("mary", "-kate"))
    self.assertFalse(needs_space_between("$", "50"))
    self.assertFalse(needs_space_between("US", "$"))
    self.assertFalse(needs_space_between("(", ")"))
    self.assertFalse(needs_space_between("(", "e.g."))
    self.assertFalse(needs_space_between("example", ")"))
    self.assertFalse(needs_space_between("example", '".'))
    self.assertFalse(needs_space_between("example", '."'))
    self.assertFalse(needs_space_between("hello'", "."))
    self.assertFalse(needs_space_between("hello.", "'"))

  def test_needs_space_between_ordinals(self):
    self.assertFalse(needs_space_between("1", "st"))
    self.assertFalse(needs_space_between("2", "nd"))
    self.assertFalse(needs_space_between("3", "rd"))
    self.assertFalse(needs_space_between("4", "th"))
    self.assertFalse(needs_space_between("25", "th"))
    self.assertFalse(needs_space_between("121", "st"))
    # Ordinals don't get spaces even if "before" starts with letters.
    self.assertFalse(needs_space_between("a25", "th"))
    self.assertFalse(needs_space_between("number1", "st"))
    # Incorrect ordinals get spaces.
    self.assertTrue(needs_space_between("1", "th"))
    self.assertTrue(needs_space_between("2", "st"))
    self.assertTrue(needs_space_between("8", "rd"))
    self.assertTrue(needs_space_between("21", "th"))


class AutoCapitalizeTestCase(unittest.TestCase):
  """Tests for auto-capitalizing text."""

  def test_auto_capitalize(self):
    self.assertEqual(auto_capitalize(""), "")
    self.assertEqual(auto_capitalize(" "), " ")
    self.assertEqual(auto_capitalize("?"), "?")
    self.assertEqual(auto_capitalize("."), ".")
    self.assertEqual(auto_capitalize(".a"), ".a")  # Looks like a file extension.
    self.assertEqual(auto_capitalize(". a"), ". A")
    self.assertEqual(auto_capitalize("\n"), "\n")
    self.assertEqual(auto_capitalize("\n\n"), "\n\n")
    self.assertEqual(auto_capitalize("\na"), "\na")
    self.assertEqual(auto_capitalize("\n a"), "\n a")
    self.assertEqual(auto_capitalize("\n\na"), "\n\nA")
    self.assertEqual(auto_capitalize("\n\n a"), "\n\n A")
    self.assertEqual(auto_capitalize("This is a test"), "This is a test")
    self.assertEqual(auto_capitalize("This is. a test"), "This is. A test")
    self.assertEqual(auto_capitalize("This is a! test"), "This is a! Test")
    self.assertEqual(auto_capitalize("This is a? test"), "This is a? Test")
    self.assertEqual(auto_capitalize("This is a\ntest"), "This is a\ntest")
    self.assertEqual(auto_capitalize("This is a\n\ntest"), "This is a\n\nTest")
    self.assertEqual(auto_capitalize("This is. A test"), "This is. A test")
    self.assertEqual(auto_capitalize("This is., a test"), "This is., a test")
    self.assertEqual(auto_capitalize("This is.:a test"), "This is.:a test")
    self.assertEqual(auto_capitalize("This is test.py"), "This is test.py")


class GuessCapitalizationTestCase(unittest.TestCase):
  """Test for guessing capitalization of a word."""

  def test_guess_capitalization(self):
    self.assertEqual(guess_capitalization("test"), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("Test"),
                     WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING)
    self.assertEqual(guess_capitalization("TEST"), WordCapitalization.UPPERCASE)
    self.assertEqual(guess_capitalization(" test "), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("\tTest\t"),
                     WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING)
    self.assertEqual(guess_capitalization(" TEST "), WordCapitalization.UPPERCASE)
    self.assertEqual(guess_capitalization("a"), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("A"),
                     WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING)
    self.assertEqual(guess_capitalization("an"), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("An"),
                     WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING)
    self.assertEqual(guess_capitalization("AN"), WordCapitalization.UPPERCASE)
    # Mixed capitalization with first letter uppercase looks like "capitalize first".
    self.assertEqual(guess_capitalization("TeST"),
                     WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING)
    # Mixed capitalization with first letter lowercase looks like "lowercase".
    self.assertEqual(guess_capitalization("teST"), WordCapitalization.LOWERCASE)

  def test_guess_capitalization_numbers(self):
    self.assertEqual(guess_capitalization("1"), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("1test"), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("a1"), WordCapitalization.LOWERCASE)
    # Numbers and symbols in the first position always result in "lowercase". We may want to change
    # this in the future.
    self.assertEqual(guess_capitalization("1TEST"), WordCapitalization.LOWERCASE)
    # Numbers or symbols look like lowercase letters.
    self.assertEqual(guess_capitalization("A1"),
                     WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING)

  def test_guess_capitalization_symbols(self):
    # Symbols are treated the same as numbers.
    self.assertEqual(guess_capitalization("!"), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("@test"), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("a#"), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("$TEST"), WordCapitalization.LOWERCASE)
    self.assertEqual(guess_capitalization("A%"),
                     WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING)

  def test_guess_capitalization_empty_string(self):
    with self.assertRaises(ValueError):
      guess_capitalization("")

  def test_guess_capitalization_whitespace(self):
    with self.assertRaises(ValueError):
      guess_capitalization(" ")

  def test_guess_capitalization_multiple_words(self):
    with self.assertRaises(ValueError):
      guess_capitalization("test test")


class GetFragmentRangesTestCase(unittest.TestCase):
  """Tests for getting fragment ranges."""

  def test_get_fragment_ranges(self):
    self.assertEqual(get_fragment_ranges(""), [])
    self.assertEqual(get_fragment_ranges("a"), [(0, 1)])
    self.assertEqual(get_fragment_ranges("test"), [(0, 4)])
    self.assertEqual(get_fragment_ranges(" test "), [(1, 5)])
    self.assertEqual(get_fragment_ranges("camelCase"), [(0, 5), (5, 9)])
    self.assertEqual(get_fragment_ranges(" camelCase "), [(1, 6), (6, 10)])
    self.assertEqual(get_fragment_ranges("snake_case"), [(0, 5), (6, 10)])
    self.assertEqual(get_fragment_ranges("kebab-case"), [(0, 5), (6, 10)])
    self.assertEqual(get_fragment_ranges("number9"), [(0, 6), (6, 7)])
    self.assertEqual(get_fragment_ranges("number99"), [(0, 6), (6, 8)])
    self.assertEqual(get_fragment_ranges("number9middle"), [(0, 6), (6, 7), (7, 13)])
    self.assertEqual(get_fragment_ranges("number99middle"), [(0, 6), (6, 8), (8, 14)])
    self.assertEqual(get_fragment_ranges("PascalCase"), [(0, 6), (6, 10)])
    self.assertEqual(get_fragment_ranges("-test-a-"), [(1, 5), (6, 7)])
    self.assertEqual(get_fragment_ranges("9"), [(0, 1)])
    self.assertEqual(get_fragment_ranges("99"), [(0, 2)])
    self.assertEqual(get_fragment_ranges("-"), [])
    self.assertEqual(get_fragment_ranges("!-"), [])
