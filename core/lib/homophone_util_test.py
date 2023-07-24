"""Tests for homophone utils."""

import unittest
from .homophone_util import get_next_homophone_dict, get_next_homophone_dict_for_single_set


class NextHomophoneDictSingleSetTestCase(unittest.TestCase):
  """Tests for getting a dict for a single set of homophones."""

  def test_two_phones(self):
    phones = ["here", "hear"]
    expected = {"here": "hear", "hear": "here"}
    actual = get_next_homophone_dict_for_single_set(phones)
    self.assertDictEqual(expected, actual)

  def test_two_phones_padded(self):
    phones = [" here ", " hear "]
    # Keys and values are stripped.
    expected = {"here": "hear", "hear": "here"}
    actual = get_next_homophone_dict_for_single_set(phones)
    self.assertDictEqual(expected, actual)

  def test_two_phones_capitalized(self):
    phones = ["Here", "Hear"]
    # Keys are lowercased.
    expected = {"here": "Hear", "hear": "Here"}
    actual = get_next_homophone_dict_for_single_set(phones)
    self.assertDictEqual(expected, actual)

  def test_two_phones_padded_capitalized(self):
    phones = [" Here ", " Hear "]
    # Keys are lowercased.
    expected = {"here": "Hear", "hear": "Here"}
    actual = get_next_homophone_dict_for_single_set(phones)
    self.assertDictEqual(expected, actual)

  def test_three_phones(self):
    phones = ["their", "there", "they're"]
    expected = {"their": "there", "there": "they're", "they're": "their"}
    actual = get_next_homophone_dict_for_single_set(phones)
    self.assertDictEqual(expected, actual)

  def test_empty_input(self):
    with self.assertRaises(ValueError):
      get_next_homophone_dict_for_single_set([])

  def test_one_phone(self):
    with self.assertRaises(ValueError):
      get_next_homophone_dict_for_single_set(["here"])

  def test_empty_string(self):
    with self.assertRaises(ValueError):
      get_next_homophone_dict_for_single_set(["here", ""])


class NextHomophoneDictTestCase(unittest.TestCase):
  """Tests for getting a dict for multiple sets of homophones."""

  def test_two_sets(self):
    phones = [["here", "hear"], ["thrown", "throne"]]
    expected = {"here": "hear", "hear": "here", "thrown": "throne", "throne": "thrown"}
    actual = get_next_homophone_dict(phones)
    self.assertDictEqual(expected, actual)

  def test_three_sets(self):
    phones = [["here", "hear"], ["thrown", "throne"], ["their", "there", "they're"]]
    expected = {
        "here": "hear",
        "hear": "here",
        "thrown": "throne",
        "throne": "thrown",
        "their": "there",
        "there": "they're",
        "they're": "their"
    }
    actual = get_next_homophone_dict(phones)
    self.assertDictEqual(expected, actual)

  def test_empty_input(self):
    self.assertEqual(get_next_homophone_dict([]), {})

  def test_duplicate_word(self):
    # For this implementation, each word needs to show up exactly once. Words with multiple pronunciations (e.g. "read"
    # and "tear") must have their homophones mashed together in one list (e.g. ["read", "red", "reed"]).
    phones = [["read", "red"], ["read", "reed"]]
    with self.assertRaises(ValueError):
      get_next_homophone_dict(phones)
