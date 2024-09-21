# pylint: disable=missing-module-docstring, missing-class-docstring
import unittest
from .scrambler_run import *  # pylint: disable=wildcard-import, unused-wildcard-import
from .scrambler_sim import simulate_actions
from .scrambler_test_util import UTILITY_FUNCTIONS
from .scrambler_types import CommandType, Context, MatchCombinationType, Modifier, ModifierType, UtilityFunctions


def _get_substring_modifiers(s: str) -> list[Modifier]:
  """Convenience method for getting a modifier list that matches a given substring."""
  return [Modifier(ModifierType.WORD_SUBSTRING_CLOSEST, search=s)]


def _get_phrase_modifiers(s: str) -> list[Modifier]:
  """Convenience method for getting a modifier list that matches a given phrase with homophones."""
  return [Modifier(ModifierType.PHRASE_CLOSEST, search=s)]


class RunCommandTestCase(unittest.TestCase):
  """Tests for running commands."""

  def test_unmatched_targets(self):
    with self.assertRaises(ValueError):
      command = Command(CommandType.MOVE_CURSOR_BEFORE, _get_substring_modifiers("xyz"))
      run_command(command, "", TextRange(0, 0), UTILITY_FUNCTIONS)
    with self.assertRaises(ValueError):
      command = Command(CommandType.MOVE_CURSOR_BEFORE, _get_substring_modifiers("ips"),
                        _get_substring_modifiers("xyz"))
      run_command(command, "Lorem ipsum", TextRange(0, 0), UTILITY_FUNCTIONS)

  def test_empty_string(self):
    command = Command(CommandType.MOVE_CURSOR_BEFORE, [])
    actions = run_command(command, "", TextRange(0, 0), UTILITY_FUNCTIONS)
    context = Context("", TextRange(0, 0))
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "")
    self.assertEqual(context.selection_range, TextRange(0, 0))
    self.assertEqual(clipboard, "")

  def test_select_word(self):
    test_string = "Lorem ipsum dolor sit amet."
    command = Command(CommandType.SELECT, _get_substring_modifiers("Lo"))
    actions = run_command(command, test_string, TextRange(0, 0), UTILITY_FUNCTIONS)
    context = Context(test_string, TextRange(0, 0))
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, test_string)
    self.assertEqual(context.selection_range.extract(test_string), "Lorem")
    self.assertEqual(clipboard, "")

  def test_select_punctuation(self):
    test_string = "Lorem ipsum dolor sit amet."
    command = Command(CommandType.SELECT, _get_substring_modifiers("."))
    actions = run_command(command, test_string, TextRange(0, 0), UTILITY_FUNCTIONS)
    context = Context(test_string, TextRange(0, 0))
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, test_string)
    self.assertEqual(context.selection_range.extract(test_string), ".")
    self.assertEqual(clipboard, "")

  def test_bring_phrase_homophones(self):
    test_string = "Lorem ipsum their dolor sit amet."
    command = Command(CommandType.BRING, _get_phrase_modifiers("ipsum there"))
    actions = run_command(command, test_string, TextRange(28, 28), UTILITY_FUNCTIONS)
    context = Context(test_string, TextRange(28, 28))
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "Lorem ipsum their dolor sit ipsum theiramet.")
    self.assertEqual(context.selection_range, TextRange(39, 39))
    self.assertEqual(clipboard, "")

  def test_select_word_not_fragment(self):
    test_string = "combo type to [m.textflow_target_combo_type]"
    command = Command(CommandType.SELECT, _get_substring_modifiers("ty"))
    actions = run_command(command, test_string, TextRange(44, 44), UTILITY_FUNCTIONS)
    context = Context(test_string, TextRange(44, 44))
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, test_string)
    self.assertEqual(context.selection_range, TextRange(6, 10))
    self.assertEqual(clipboard, "")

  def test_replace_word_search_backwards(self):
    # Second "this" should be replaced. Cursor is at end of string.
    test_string = "this is this test."
    initial_selection = TextRange(18, 18)
    command = Command(CommandType.REPLACE_WORD_MATCH_CASE,
                      _get_phrase_modifiers("this"),
                      insert_text="that")
    actions = run_command(command, test_string, initial_selection, UTILITY_FUNCTIONS)
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "this is that test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_delete_word(self):
    test_string = "Lorem ipsum dolor sit amet."
    command = Command(CommandType.CLEAR_NO_MOVE, _get_substring_modifiers("ips"))
    actions = run_command(command, test_string, TextRange(0, 0), UTILITY_FUNCTIONS)
    context = Context(test_string, TextRange(0, 0))
    clipboard = simulate_actions(context, actions)
    # Space after word should also be removed.
    self.assertEqual(context.text, "Lorem dolor sit amet.")
    self.assertEqual(context.selection_range, TextRange(0, 0))
    self.assertEqual(clipboard, "")
