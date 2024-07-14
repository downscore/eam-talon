"""Tests for homophone utils."""

import unittest
from .homophone_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class GetHomophoneSetsTestCase(unittest.TestCase):
  """Tests for homophone util."""

  def test_two_sets(self):
    phones = [["here", "hear"], ["thrown", "throne"]]
    expected = [HomophoneSet(["here", "hear"], []), HomophoneSet(["thrown", "throne"], [])]
    actual = get_homophone_sets(phones)
    self.assertEqual(expected, actual)

  def test_uncommon_word(self):
    phones = [["here", "hear"], ["frees", "freeze", "*frieze"]]
    expected = [HomophoneSet(["here", "hear"], []), HomophoneSet(["frees", "freeze"], ["frieze"])]
    actual = get_homophone_sets(phones)
    self.assertEqual(expected, actual)

  def test_empty_set(self):
    phones = [["read", "reed"], []]
    with self.assertRaises(ValueError):
      get_homophone_sets(phones)


class GetHomographHomophoneSetsTestCase(unittest.TestCase):
  """Tests for homophone util."""

  def test_two_sets(self):
    phones = [["read", "reed"], ["read", "red"]]
    expected = {"read": [HomophoneSet(["read", "reed"], []), HomophoneSet(["read", "red"], [])]}
    actual = get_homograph_homophone_sets(phones)
    self.assertEqual(expected, actual)

  def test_uncommon_word(self):
    phones = [["read", "*reed"], ["read", "red"]]
    expected = {"read": [HomophoneSet(["read"], ["reed"]), HomophoneSet(["read", "red"], [])]}
    actual = get_homograph_homophone_sets(phones)
    self.assertEqual(expected, actual)

  def test_empty_set(self):
    phones = [["read", "reed"], []]
    with self.assertRaises(ValueError):
      get_homograph_homophone_sets(phones)


class GetWordToHomophoneSetDictTestCase(unittest.TestCase):
  """Tests for homophone util."""

  def test_two_sets(self):
    homophone_sets = [HomophoneSet(["here", "hear"], []), HomophoneSet(["thrown", "throne"], [])]
    expected = {
        "here": homophone_sets[0],
        "hear": homophone_sets[0],
        "thrown": homophone_sets[1],
        "throne": homophone_sets[1]
    }
    actual = get_word_to_homophone_set_dict(homophone_sets, {})
    self.assertEqual(expected, actual)

  def test_uncommon_word(self):
    homophone_sets = [
        HomophoneSet(["here", "hear"], []),
        HomophoneSet(["frees", "freeze"], ["frieze"])
    ]
    expected = {
        "here": homophone_sets[0],
        "hear": homophone_sets[0],
        "frees": homophone_sets[1],
        "freeze": homophone_sets[1],
        "frieze": homophone_sets[1]
    }
    actual = get_word_to_homophone_set_dict(homophone_sets, {})
    self.assertEqual(expected, actual)

  def test_homographs(self):
    homophone_sets = [HomophoneSet(["here", "hear"], []), HomophoneSet(["thrown", "throne"], [])]
    homophone_homograph_sets = {
        "read": [HomophoneSet(["read", "reed"], []),
                 HomophoneSet(["read", "red"], [])]
    }
    expected = {
        "here": homophone_sets[0],
        "hear": homophone_sets[0],
        "thrown": homophone_sets[1],
        "throne": homophone_sets[1],
        # New homophone set for combined homograph sets.
        "read": HomophoneSet(["read", "reed", "red"], []),
        "reed": homophone_homograph_sets["read"][0],
        "red": homophone_homograph_sets["read"][1]
    }
    actual = get_word_to_homophone_set_dict(homophone_sets, homophone_homograph_sets)
    self.assertEqual(expected, actual)

  def test_homographs_uncommon(self):
    homophone_sets = [HomophoneSet(["here", "hear"], []), HomophoneSet(["thrown", "throne"], [])]
    homophone_homograph_sets = {
        "read": [HomophoneSet(["read"], ["reed"]),
                 HomophoneSet(["read", "red"], [])]
    }
    expected = {
        "here": homophone_sets[0],
        "hear": homophone_sets[0],
        "thrown": homophone_sets[1],
        "throne": homophone_sets[1],
        # New homophone set for combined homograph sets.
        "read": HomophoneSet(["read", "red"], ["reed"]),
        "reed": homophone_homograph_sets["read"][0],
        "red": homophone_homograph_sets["read"][1]
    }
    actual = get_word_to_homophone_set_dict(homophone_sets, homophone_homograph_sets)
    self.assertEqual(expected, actual)

  def test_homographs_duplicate_word(self):
    homophone_sets = [HomophoneSet(["read", "red"], []), HomophoneSet(["thrown", "throne"], [])]
    homophone_homograph_sets = {
        "read": [HomophoneSet(["read"], ["reed"]),
                 HomophoneSet(["read", "red"], [])]
    }
    with self.assertRaises(ValueError):
      get_word_to_homophone_set_dict(homophone_sets, homophone_homograph_sets)


class HomophoneSetGetNextWordTestCase(unittest.TestCase):
  """Tests for homophone util."""

  def test_uncommon_word(self):
    homophone_set = HomophoneSet(["frees", "freeze"], ["frieze"])
    self.assertEqual(homophone_set.get_next_word("frees"), "freeze")
    self.assertEqual(homophone_set.get_next_word("freeze"), "frees")
    self.assertEqual(homophone_set.get_next_word("frieze"), "frees")
    with self.assertRaises(ValueError):
      homophone_set.get_next_word("unknown")
