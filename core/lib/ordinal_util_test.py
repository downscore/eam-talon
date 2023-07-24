"""Tests for ordinal utils."""

import unittest
from .ordinal_util import get_ints_by_ordinal_words


class GetOrdinalsDictTestCase(unittest.TestCase):
  """Test for getting a dict of ints keyed by ordinal strings."""

  def test_single_element(self):
    expected = {"first": 1}
    actual = get_ints_by_ordinal_words(1)
    self.assertDictEqual(expected, actual)

  def test_two_elements(self):
    expected = {"first": 1, "second": 2}
    actual = get_ints_by_ordinal_words(2)
    self.assertDictEqual(expected, actual)

  def test_many_elements(self):
    expected_subset = {
        "first": 1,
        "second": 2,
        "tenth": 10,
        "eleventh": 11,
        "thirtieth": 30,
        "forty fifth": 45,
        "ninety ninth": 99
    }
    actual = get_ints_by_ordinal_words(99)
    self.assertEqual(99, len(actual))
    self.assertEqual(actual, actual | expected_subset)

  def test_bad_input(self):
    with self.assertRaises(ValueError):
      # Max value too high.
      get_ints_by_ordinal_words(100)
    with self.assertRaises(ValueError):
      # Max value must be positive.
      get_ints_by_ordinal_words(0)
    with self.assertRaises(ValueError):
      # Max value must be positive.
      get_ints_by_ordinal_words(-1)
