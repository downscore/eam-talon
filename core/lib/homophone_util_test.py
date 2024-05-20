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
    actual = get_word_to_homophone_set_dict(homophone_sets)
    self.assertEqual(expected, actual)

  def test_uncommon_word(self):
    homophone_sets = [HomophoneSet(["here", "hear"], []), HomophoneSet(["frees", "freeze"], ["frieze"])]
    expected = {
        "here": homophone_sets[0],
        "hear": homophone_sets[0],
        "frees": homophone_sets[1],
        "freeze": homophone_sets[1],
        "frieze": homophone_sets[1]
    }
    actual = get_word_to_homophone_set_dict(homophone_sets)
    self.assertEqual(expected, actual)


class HomophoneSetGetNextWordTestCase(unittest.TestCase):
  """Tests for homophone util."""

  def test_uncommon_word(self):
    homophone_set = HomophoneSet(["frees", "freeze"], ["frieze"])
    self.assertEqual(homophone_set.get_next_word("frees"), "freeze")
    self.assertEqual(homophone_set.get_next_word("freeze"), "frees")
    self.assertEqual(homophone_set.get_next_word("frieze"), "frees")
    with self.assertRaises(ValueError):
      homophone_set.get_next_word("unknown")
