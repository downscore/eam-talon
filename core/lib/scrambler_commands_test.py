# pylint: disable=missing-module-docstring, missing-class-docstring
import unittest
from .scrambler_commands import *  # pylint: disable=wildcard-import, unused-wildcard-import
from .scrambler_sim import simulate_actions
from .scrambler_test_util import UTILITY_FUNCTIONS
from .scrambler_types import Context


def _perform_command(
    command_type: CommandType,
    text: str,
    selection_range: TextRange,
    match_from: TextMatch,
    insert_text: str = "",
    lambda_func: Optional[Callable[[str], str]] = None,
) -> list[EditorAction]:
  """Helper methods for performing a command."""
  return perform_command(command_type, text, selection_range, match_from, insert_text, lambda_func,
                         UTILITY_FUNCTIONS)


class PerformCommandTestCase(unittest.TestCase):
  """Tests for implementing a command."""

  def test_invalid_command(self):
    with self.assertRaises(ValueError):
      _perform_command(CommandType.SELECT, "", TextRange(0, 1), TextMatch(TextRange(0, 0)))
    with self.assertRaises(ValueError):
      _perform_command(CommandType.SELECT, "", TextRange(0, 0), TextMatch(TextRange(0, 1)))

  def test_empty_string(self):
    actions = _perform_command(CommandType.MOVE_CURSOR_BEFORE, "", TextRange(0, 0),
                               TextMatch(TextRange(0, 0)))
    context = Context("", TextRange(0, 0))
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "")
    self.assertEqual(context.selection_range, TextRange(0, 0))
    self.assertEqual(clipboard, "")

  def test_select(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.SELECT, test_string, initial_selection,
                               TextMatch(TextRange(8, 9)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, test_string)
    self.assertEqual(context.selection_range.extract(context.text), "a")
    self.assertEqual(clipboard, "")

  def test_select_beginning(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.SELECT, test_string, initial_selection,
                               TextMatch(TextRange(0, 4)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, test_string)
    self.assertEqual(context.selection_range.extract(context.text), "This")
    self.assertEqual(clipboard, "")

  def test_select_end(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.SELECT, test_string, initial_selection,
                               TextMatch(TextRange(10, 15)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, test_string)
    self.assertEqual(context.selection_range.extract(context.text), "test.")
    self.assertEqual(clipboard, "")

  def test_clear_move_cursor(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_MOVE_CURSOR, test_string, initial_selection,
                               TextMatch(TextRange(8, 9)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is  test.")
    self.assertEqual(context.selection_range, TextRange(8, 8))
    self.assertEqual(clipboard, "")

  def test_clear_move_cursor_beginning(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_MOVE_CURSOR, test_string, initial_selection,
                               TextMatch(TextRange(0, 4)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, " is a test.")
    self.assertEqual(context.selection_range, TextRange(0, 0))
    self.assertEqual(clipboard, "")

  def test_clear_move_cursor_end(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_MOVE_CURSOR, test_string, initial_selection,
                               TextMatch(TextRange(10, 15)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is a ")
    self.assertEqual(context.selection_range, TextRange(10, 10))
    self.assertEqual(clipboard, "")

  def test_clear_no_move(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection,
                               TextMatch(TextRange(8, 9)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is  test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_clear_no_move_beginning(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection,
                               TextMatch(TextRange(0, 4)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, " is a test.")
    self.assertEqual(context.selection_range, TextRange(1, 3))
    self.assertEqual(clipboard, "")

  def test_clear_no_move_end(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection,
                               TextMatch(TextRange(10, 15)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is a ")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_clear_no_move_intersection(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection,
                               TextMatch(TextRange(4, 7)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This a test.")
    self.assertEqual(context.selection_range, TextRange(4, 4))
    self.assertEqual(clipboard, "")

  def test_clear_no_move_intersection_beginning(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection,
                               TextMatch(TextRange(0, 7)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, " a test.")
    self.assertEqual(context.selection_range, TextRange(0, 0))
    self.assertEqual(clipboard, "")

  def test_clear_no_move_intersection_end(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection,
                               TextMatch(TextRange(7, 15)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is")
    self.assertEqual(context.selection_range, TextRange(7, 7))
    self.assertEqual(clipboard, "")

  def test_move_cursor_before(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.MOVE_CURSOR_BEFORE, test_string, initial_selection,
                               TextMatch(TextRange(7, 15)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, test_string)
    self.assertEqual(context.selection_range, TextRange(7, 7))
    self.assertEqual(clipboard, "")

  def test_move_cursor_after(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.MOVE_CURSOR_AFTER, test_string, initial_selection,
                               TextMatch(TextRange(7, 15)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, test_string)
    self.assertEqual(context.selection_range, TextRange(15, 15))
    self.assertEqual(clipboard, "")

  def test_cut_to_clipboard(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.CUT_TO_CLIPBOARD, test_string, initial_selection,
                               TextMatch(TextRange(10, 15)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is a ")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "test.")

  def test_copy_to_clipboard(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.COPY_TO_CLIPBOARD, test_string, initial_selection,
                               TextMatch(TextRange(10, 15)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is a test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "test.")

  def test_bring(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.BRING, test_string, initial_selection,
                               TextMatch(TextRange(0, 4)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This This a test.")
    self.assertEqual(context.selection_range, TextRange(9, 9))
    self.assertEqual(clipboard, "")

  def test_next_homophone(self):
    test_string = "This is there test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is their test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_match_title_case(self):
    test_string = "This is There test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is Their test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_match_all_caps(self):
    test_string = "This is THERE test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is THEIR test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_before_selection(self):
    test_string = "This is there test."
    initial_selection = TextRange(14, 18)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is their test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_intersection(self):
    test_string = "This is there test."
    initial_selection = TextRange(9, 15)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is their test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_different_length(self):
    test_string = "This is they're test."
    initial_selection = TextRange(16, 20)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection,
                               TextMatch(TextRange(8, 15)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is there test.")
    self.assertEqual(context.selection_range, TextRange(14, 18))
    self.assertEqual(context.selection_range.extract(context.text), "test")
    self.assertEqual(clipboard, "")

  def test_next_homophone_no_homophone(self):
    test_string = "This is our test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection,
                               TextMatch(TextRange(8, 11)))
    self.assertEqual(len(actions), 0)

  def test_replace(self):
    test_string = "This is there test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.REPLACE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)), "their")
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is their test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_before_selection(self):
    test_string = "This is there test."
    initial_selection = TextRange(14, 18)
    actions = _perform_command(CommandType.REPLACE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)), "their")
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is their test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_intersection(self):
    test_string = "This is there test."
    initial_selection = TextRange(9, 15)
    actions = _perform_command(CommandType.REPLACE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)), "our")
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is our test.")
    self.assertEqual(context.selection_range, TextRange(11, 11))
    self.assertEqual(clipboard, "")

  def test_replace_different_length(self):
    test_string = "This is they're test."
    initial_selection = TextRange(16, 20)
    actions = _perform_command(CommandType.REPLACE, test_string, initial_selection,
                               TextMatch(TextRange(8, 15)), "their")
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is their test.")
    self.assertEqual(context.selection_range, TextRange(14, 18))
    self.assertEqual(context.selection_range.extract(context.text), "test")
    self.assertEqual(clipboard, "")

  def test_title_case(self):
    # Ensure first word "a" is capitalized.
    test_string = "a test and a string."
    initial_selection = TextRange(11, 12)
    actions = _perform_command(CommandType.TITLE_CASE, test_string, initial_selection,
                               TextMatch(TextRange(0, 10)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "A Test and a string.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_title_case_full_string(self):
    # Ensure first word "a" is capitalized.
    test_string = "a test and a string."
    initial_selection = TextRange(11, 12)
    actions = _perform_command(CommandType.TITLE_CASE, test_string, initial_selection,
                               TextMatch(TextRange(0, 20)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "A Test and a String.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_lowercase(self):
    test_string = "A Test And a String."
    initial_selection = TextRange(11, 12)
    actions = _perform_command(CommandType.LOWERCASE, test_string, initial_selection,
                               TextMatch(TextRange(0, 10)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "a test and a String.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_uppercase(self):
    test_string = "A Test And a String."
    initial_selection = TextRange(11, 12)
    actions = _perform_command(CommandType.UPPERCASE, test_string, initial_selection,
                               TextMatch(TextRange(0, 10)))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "A TEST AND a String.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_word_match_case(self):
    test_string = "This is there test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.REPLACE_WORD_MATCH_CASE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)), "Their")
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is their test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_word_match_case_title(self):
    test_string = "This is There test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.REPLACE_WORD_MATCH_CASE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)), "their")
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is Their test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_word_match_case_all_caps(self):
    test_string = "This is THERE test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.REPLACE_WORD_MATCH_CASE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)), "their")
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "This is THEIR test.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_with_lambda(self):
    test_string = "Let's play base ball now."
    initial_selection = TextRange(5, 5)
    actions = _perform_command(CommandType.REPLACE_WITH_LAMBDA, test_string, initial_selection,
                               TextMatch(TextRange(11, 20)), "", lambda s: s.replace(" ", ""))
    context = Context(test_string, initial_selection)
    clipboard = simulate_actions(context, actions)
    self.assertEqual(context.text, "Let's play baseball now.")
    self.assertEqual(context.selection_range, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_no_lambda_provided(self):
    test_string = "Let's play base ball now."
    initial_selection = TextRange(5, 5)
    with self.assertRaises(ValueError):
      _perform_command(CommandType.REPLACE_WITH_LAMBDA, test_string, initial_selection,
                       TextMatch(TextRange(11, 20)), "", None)
