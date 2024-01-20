"""Tests for top-level textflow functionality."""

import unittest
from .textflow import *  # pylint: disable=wildcard-import, unused-wildcard-import
from .textflow_sim import simulate_actions
from .textflow_test_util import UTILITY_FUNCTIONS
from .textflow_types import CommandType, CompoundTarget, SimpleTarget, TokenMatchMethod, TokenMatchOptions, UtilityFunctions


def _get_substring_target(s: str) -> CompoundTarget:
  """Convenience method for getting a compound target that matches a given substring."""
  return CompoundTarget(SimpleTarget(TokenMatchOptions(search=s)))


def _get_phrase_target(s: str) -> CompoundTarget:
  """Convenience method for getting a compound target that matches a given phrase with homophones."""
  return CompoundTarget(SimpleTarget(TokenMatchOptions(TokenMatchMethod.PHRASE, search=s)))


class TextFlowTestCase(unittest.TestCase):
  """Tests for textflow commands."""

  def test_unmatched_targets(self):
    with self.assertRaises(ValueError):
      command = Command(CommandType.MOVE_CURSOR_BEFORE, _get_substring_target("xyz"))
      run_command(command, "", TextRange(0, 0), UTILITY_FUNCTIONS)
    with self.assertRaises(ValueError):
      command = Command(CommandType.MOVE_CURSOR_BEFORE, _get_substring_target("ips"), _get_substring_target("xyz"))
      run_command(command, "Lorem ipsum", TextRange(0, 0), UTILITY_FUNCTIONS)

  def test_empty_string(self):
    command = Command(CommandType.MOVE_CURSOR_BEFORE, CompoundTarget())
    actions = run_command(command, "", TextRange(0, 0), UTILITY_FUNCTIONS)
    text, selection, clipboard = simulate_actions("", TextRange(0, 0), actions)
    self.assertEqual(text, "")
    self.assertEqual(selection, TextRange(0, 0))
    self.assertEqual(clipboard, "")

  def test_select_word(self):
    test_string = "Lorem ipsum dolor sit amet."
    command = Command(CommandType.SELECT, _get_substring_target("Lo"))
    actions = run_command(command, test_string, TextRange(0, 0), UTILITY_FUNCTIONS)
    text, selection, clipboard = simulate_actions(test_string, TextRange(0, 0), actions)
    self.assertEqual(text, test_string)
    self.assertEqual(selection.extract(test_string), "Lorem")
    self.assertEqual(clipboard, "")

  def test_select_punctuation(self):
    test_string = "Lorem ipsum dolor sit amet."
    command = Command(CommandType.SELECT, _get_substring_target("."))
    actions = run_command(command, test_string, TextRange(0, 0), UTILITY_FUNCTIONS)
    text, selection, clipboard = simulate_actions(test_string, TextRange(0, 0), actions)
    self.assertEqual(text, test_string)
    self.assertEqual(selection.extract(test_string), ".")
    self.assertEqual(clipboard, "")

  def test_swap_words(self):
    test_string = "Lorem ipsum dolor sit amet."
    command = Command(CommandType.SWAP, _get_substring_target("ip"), _get_substring_target("do"))
    actions = run_command(command, test_string, TextRange(0, 0), UTILITY_FUNCTIONS)
    text, selection, clipboard = simulate_actions(test_string, TextRange(0, 0), actions)
    self.assertEqual(text, "Lorem dolor ipsum sit amet.")
    self.assertEqual(selection, TextRange(11, 11))
    self.assertEqual(clipboard, "")

  def test_bring_phrase_homophones(self):
    test_string = "Lorem ipsum their dolor sit amet."
    command = Command(CommandType.BRING, _get_phrase_target("ipsum there"))
    actions = run_command(command, test_string, TextRange(28, 28), UTILITY_FUNCTIONS)
    text, selection, clipboard = simulate_actions(test_string, TextRange(28, 28), actions)
    self.assertEqual(text, "Lorem ipsum their dolor sit ipsum theiramet.")
    self.assertEqual(selection, TextRange(39, 39))
    self.assertEqual(clipboard, "")

  def test_select_word_not_fragment(self):
    test_string = "combo type to [m.textflow_target_combo_type]"
    command = Command(CommandType.SELECT, _get_substring_target("ty"))
    actions = run_command(command, test_string, TextRange(44, 44), UTILITY_FUNCTIONS)
    text, selection, clipboard = simulate_actions(test_string, TextRange(44, 44), actions)
    self.assertEqual(text, test_string)
    self.assertEqual(selection, TextRange(6, 10))
    self.assertEqual(clipboard, "")

  def test_replace_word_search_backwards(self):
    # Second "this" should be replaced. Cursor is at end of string.
    test_string = "this is this test."
    initial_selection = TextRange(18, 18)
    target_from = CompoundTarget(SimpleTarget(TokenMatchOptions(TokenMatchMethod.PHRASE, search="this")))
    command = Command(CommandType.REPLACE_WORD_MATCH_CASE, target_from, insert_text="that")
    actions = run_command(command, test_string, initial_selection, UTILITY_FUNCTIONS)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "this is that test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_delete_word(self):
    test_string = "Lorem ipsum dolor sit amet."
    command = Command(CommandType.CLEAR_NO_MOVE, _get_substring_target("ips"))
    actions = run_command(command, test_string, TextRange(0, 0), UTILITY_FUNCTIONS)
    text, selection, clipboard = simulate_actions(test_string, TextRange(0, 0), actions)
    # Space after word should also be removed.
    self.assertEqual(text, "Lorem dolor sit amet.")
    self.assertEqual(selection, TextRange(0, 0))
    self.assertEqual(clipboard, "")
