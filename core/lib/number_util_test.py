"""Tests for number utils."""

import unittest
from .number_util import parse_number, copy_leading_decimal_digits


class ParseNumberTestCase(unittest.TestCase):
  """Tests for util function."""

  def test_parse_number(self):
    self.assertEqual(parse_number(["one"]), "1")
    self.assertEqual(parse_number(["ten"]), "10")
    self.assertEqual(parse_number(["eleven"]), "11")
    self.assertEqual(parse_number(["fifteen"]), "15")
    self.assertEqual(parse_number(["twenty"]), "20")
    self.assertEqual(parse_number(["fifty", "three"]), "53")
    self.assertEqual(parse_number(["one", "hundred", "twenty", "three"]), "123")
    self.assertEqual(parse_number(["one", "oh", "one"]), "101")
    self.assertEqual(parse_number(["one", "hundred", "thousand"]), "100000")
    self.assertEqual(parse_number(["one", "hundred", "thousand", "three", "hundred", "twenty", "one"]), "100321")
    self.assertEqual(
        parse_number(["one", "hundred", "twenty", "three", "thousand", "three", "hundred", "twenty", "one"]), "123321")
    self.assertEqual(parse_number(["one", "million"]), "1000000")
    self.assertEqual(parse_number(["thirty", "hundred"]), "3000")
    self.assertEqual(parse_number(["thirty", "five", "hundred"]), "3500")
    self.assertEqual(parse_number(["eighty", "two", "thousand"]), "82000")
    self.assertEqual(parse_number(["one", "million", "five", "hundred", "one", "thousand"]), "1501000")
    self.assertEqual(parse_number(["one", "thousand", "one"]), "1001")
    self.assertEqual(parse_number(["one", "thousand", "ten"]), "1010")
    self.assertEqual(parse_number(["one", "twenty", "three", "thousand", "four", "fifty", "six"]), "123456")

  def test_including_and(self):
    self.assertEqual(parse_number(["one", "hundred", "and", "twenty", "three"]), "123")
    self.assertEqual(parse_number(["one", "hundred", "thousand", "three", "hundred", "and", "twenty", "one"]), "100321")
    self.assertEqual(
        parse_number(
            ["one", "hundred", "and", "twenty", "three", "thousand", "three", "hundred", "and", "twenty", "one"]),
        "123321")
    self.assertEqual(parse_number(["one", "hundred", "and", "five", "thousand"]), "105000")
    self.assertEqual(
        parse_number(["one", "million", "five", "hundred", "and", "one", "thousand", "one", "hundred", "and", "six"]),
        "1501106")
    self.assertEqual(
        parse_number(
            ["one", "hundred", "and", "twenty", "three", "thousand", "and", "four", "hundred", "and", "fifty", "six"]),
        "123456")

  def test_concatenating_numbers(self):
    self.assertEqual(parse_number(["one", "two"]), "12")
    self.assertEqual(parse_number(["one", "two", "three"]), "123")
    self.assertEqual(parse_number(["twelve", "three"]), "123")
    self.assertEqual(parse_number(["one", "twenty", "three"]), "123")
    self.assertEqual(parse_number(["twenty", "one", "five", "seven"]), "2157")
    self.assertEqual(parse_number(["one", "hundred", "twenty", "seven", "five"]), "1275")
    self.assertEqual(parse_number(["ten", "four"]), "104")
    self.assertEqual(parse_number(["ten", "sixty", "six"]), "1066")
    self.assertEqual(parse_number(["nineteen", "oh", "six"]), "1906")
    self.assertEqual(parse_number(["twenty", "twenty"]), "2020")
    self.assertEqual(parse_number(["twenty", "oh", "one"]), "2001")

  def test_unmatchable_first_word(self):
    """We are still able to parse strings with an unmatchable first word.
    Included for completeness, as we don't currently rely on this functionality and may remove it in the future."""
    self.assertEqual(parse_number(["hundred"]), "100")
    self.assertEqual(parse_number(["hundred", "one"]), "101")
    self.assertEqual(parse_number(["hundred", "and", "one"]), "101")
    self.assertEqual(parse_number(["million"]), "1000000")

  def test_unnatural_phrasing(self):
    """We are still able to parse strings with unnatural phrasing. Some of these may not be matched by voice commands.
    Included for completeness, as we don't currently rely on this functionality and may remove it in the future."""
    self.assertEqual(parse_number(["fifty", "and", "one"]), "51")
    self.assertEqual(parse_number(["one", "hundred", "and", "and", "one"]), "101")
    self.assertEqual(parse_number(["and", "one", "hundred", "and", "one"]), "101")
    self.assertEqual(parse_number(["and", "and", "thousand", "one"]), "1001")
    self.assertEqual(parse_number(["one", "thousand", "thousand"]), "1000000")
    self.assertEqual(parse_number(["two", "million", "oh", "five"]), "2000005")

  def test_corner_cases(self):
    """Test cases that may potentially be treated as errors in the future. Some or all of these may not be matched by
    voice commands."""
    self.assertEqual(parse_number([]), "")
    self.assertEqual(parse_number(["and"]), "")
    self.assertEqual(parse_number(["and", "and"]), "")


class CopyLeadingDecimalDigitsTestCase(unittest.TestCase):
  """Tests for util function."""

  def test_zeros(self):
    self.assertEqual(copy_leading_decimal_digits(0, 0), 0)

  def test_same_length(self):
    self.assertEqual(copy_leading_decimal_digits(12, 34), 34)

  def test_first_longer(self):
    self.assertEqual(copy_leading_decimal_digits(123, 34), 134)

  def test_second_longer(self):
    self.assertEqual(copy_leading_decimal_digits(12, 534), 534)

  def test_two_digits_longer(self):
    self.assertEqual(copy_leading_decimal_digits(1234, 56), 1256)

  def test_with_zeros(self):
    self.assertEqual(copy_leading_decimal_digits(103, 6), 106)
