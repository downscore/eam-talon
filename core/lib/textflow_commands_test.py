"""Tests for performing commands."""

import unittest
from .textflow_commands import *  # pylint: disable=wildcard-import, unused-wildcard-import
from .textflow_sim import simulate_actions
from .textflow_test_util import UTILITY_FUNCTIONS


def _perform_command(command_type: CommandType,
                     text: str,
                     selection_range: TextRange,
                     match_from: TextMatch,
                     match_to: Optional[TextMatch] = None,
                     insert_text: str = "") -> list[EditorAction]:
  """Helper methods for performing a command."""
  return perform_command(command_type, text, selection_range, match_from, match_to, insert_text, UTILITY_FUNCTIONS)


class PerformCommandTestCase(unittest.TestCase):
  """Tests for implementing a command."""

  def test_invalid_command(self):
    with self.assertRaises(ValueError):
      _perform_command(CommandType.SELECT, "", TextRange(0, 1), TextMatch(TextRange(0, 0)), TextMatch(TextRange(0, 0)))
    with self.assertRaises(ValueError):
      _perform_command(CommandType.SELECT, "", TextRange(0, 0), TextMatch(TextRange(0, 1)), TextMatch(TextRange(0, 0)))
    with self.assertRaises(ValueError):
      _perform_command(CommandType.SELECT, "", TextRange(0, 0), TextMatch(TextRange(0, 0)), TextMatch(TextRange(0, 1)))

  def test_empty_string(self):
    actions = _perform_command(CommandType.MOVE_CURSOR_BEFORE, "", TextRange(0, 0), TextMatch(TextRange(0, 0)), None)
    text, selection, clipboard = simulate_actions("", TextRange(0, 0), actions)
    self.assertEqual(text, "")
    self.assertEqual(selection, TextRange(0, 0))
    self.assertEqual(clipboard, "")

  def test_select(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.SELECT, test_string, initial_selection, TextMatch(TextRange(8, 9)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, test_string)
    self.assertEqual(selection.extract(text), "a")
    self.assertEqual(clipboard, "")

  def test_select_beginning(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.SELECT, test_string, initial_selection, TextMatch(TextRange(0, 4)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, test_string)
    self.assertEqual(selection.extract(text), "This")
    self.assertEqual(clipboard, "")

  def test_select_end(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.SELECT, test_string, initial_selection, TextMatch(TextRange(10, 15)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, test_string)
    self.assertEqual(selection.extract(text), "test.")
    self.assertEqual(clipboard, "")

  def test_clear_move_cursor(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_MOVE_CURSOR, test_string, initial_selection,
                               TextMatch(TextRange(8, 9)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is  test.")
    self.assertEqual(selection, TextRange(8, 8))
    self.assertEqual(clipboard, "")

  def test_clear_move_cursor_beginning(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_MOVE_CURSOR, test_string, initial_selection,
                               TextMatch(TextRange(0, 4)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, " is a test.")
    self.assertEqual(selection, TextRange(0, 0))
    self.assertEqual(clipboard, "")

  def test_clear_move_cursor_end(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_MOVE_CURSOR, test_string, initial_selection,
                               TextMatch(TextRange(10, 15)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is a ")
    self.assertEqual(selection, TextRange(10, 10))
    self.assertEqual(clipboard, "")

  def test_clear_no_move(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection, TextMatch(TextRange(8, 9)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is  test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_clear_no_move_beginning(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection, TextMatch(TextRange(0, 4)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, " is a test.")
    self.assertEqual(selection, TextRange(1, 3))
    self.assertEqual(clipboard, "")

  def test_clear_no_move_end(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection, TextMatch(TextRange(10, 15)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is a ")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_clear_no_move_intersection(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection, TextMatch(TextRange(4, 7)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This a test.")
    self.assertEqual(selection, TextRange(4, 4))
    self.assertEqual(clipboard, "")

  def test_clear_no_move_intersection_beginning(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection, TextMatch(TextRange(0, 7)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, " a test.")
    self.assertEqual(selection, TextRange(0, 0))
    self.assertEqual(clipboard, "")

  def test_clear_no_move_intersection_end(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.CLEAR_NO_MOVE, test_string, initial_selection, TextMatch(TextRange(7, 15)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is")
    self.assertEqual(selection, TextRange(7, 7))
    self.assertEqual(clipboard, "")

  def test_move_cursor_before(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.MOVE_CURSOR_BEFORE, test_string, initial_selection,
                               TextMatch(TextRange(7, 15)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, test_string)
    self.assertEqual(selection, TextRange(7, 7))
    self.assertEqual(clipboard, "")

  def test_move_cursor_after(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.MOVE_CURSOR_AFTER, test_string, initial_selection,
                               TextMatch(TextRange(7, 15)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, test_string)
    self.assertEqual(selection, TextRange(15, 15))
    self.assertEqual(clipboard, "")

  def test_cut_to_clipboard(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.CUT_TO_CLIPBOARD, test_string, initial_selection,
                               TextMatch(TextRange(10, 15)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is a ")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "test.")

  def test_copy_to_clipboard(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 9)
    actions = _perform_command(CommandType.COPY_TO_CLIPBOARD, test_string, initial_selection,
                               TextMatch(TextRange(10, 15)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is a test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "test.")

  def test_bring(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.BRING, test_string, initial_selection, TextMatch(TextRange(0, 4)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This This a test.")
    self.assertEqual(selection, TextRange(9, 9))
    self.assertEqual(clipboard, "")

  def test_bring_match_to(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.BRING, test_string, initial_selection, TextMatch(TextRange(0, 4)),
                               TextMatch(TextRange(8, 9)))
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is This test.")
    self.assertEqual(selection, TextRange(12, 12))
    self.assertEqual(clipboard, "")

  def test_move(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.MOVE, test_string, initial_selection, TextMatch(TextRange(0, 4)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, " This a test.")
    self.assertEqual(selection, TextRange(5, 5))
    self.assertEqual(clipboard, "")

  def test_move_match_to(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.MOVE, test_string, initial_selection, TextMatch(TextRange(0, 4)),
                               TextMatch(TextRange(8, 9)))
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, " is This test.")
    self.assertEqual(selection, TextRange(8, 8))
    self.assertEqual(clipboard, "")

  def test_swap(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.SWAP, test_string, initial_selection, TextMatch(TextRange(0, 4)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "is This a test.")
    self.assertEqual(selection, TextRange(2, 2))
    self.assertEqual(clipboard, "")

  def test_swap_match_to(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.SWAP, test_string, initial_selection, TextMatch(TextRange(0, 4)),
                               TextMatch(TextRange(8, 9)))
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "a is This test.")
    self.assertEqual(selection, TextRange(1, 1))
    self.assertEqual(clipboard, "")

  def test_swap_matches_reversed(self):
    test_string = "This is a test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.SWAP, test_string, initial_selection, TextMatch(TextRange(8, 9)),
                               TextMatch(TextRange(0, 4)))
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "a is This test.")
    self.assertEqual(selection, TextRange(1, 1))
    self.assertEqual(clipboard, "")

  def test_next_homophone(self):
    test_string = "This is there test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection, TextMatch(TextRange(8, 13)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is their test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_match_title_case(self):
    test_string = "This is There test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection, TextMatch(TextRange(8, 13)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is Their test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_match_all_caps(self):
    test_string = "This is THERE test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection, TextMatch(TextRange(8, 13)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is THEIR test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_before_selection(self):
    test_string = "This is there test."
    initial_selection = TextRange(14, 18)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection, TextMatch(TextRange(8, 13)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is their test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_intersection(self):
    test_string = "This is there test."
    initial_selection = TextRange(9, 15)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection, TextMatch(TextRange(8, 13)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is their test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_next_homophone_different_length(self):
    test_string = "This is they're test."
    initial_selection = TextRange(16, 20)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection, TextMatch(TextRange(8, 15)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is there test.")
    self.assertEqual(selection, TextRange(14, 18))
    self.assertEqual(selection.extract(text), "test")
    self.assertEqual(clipboard, "")

  def test_next_homophone_no_homophone(self):
    test_string = "This is our test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.NEXT_HOMOPHONE, test_string, initial_selection, TextMatch(TextRange(8, 11)),
                               None)
    self.assertEqual(len(actions), 0)

  def test_replace(self):
    test_string = "This is there test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.REPLACE, test_string, initial_selection, TextMatch(TextRange(8, 13)), None,
                               "their")
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is their test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_before_selection(self):
    test_string = "This is there test."
    initial_selection = TextRange(14, 18)
    actions = _perform_command(CommandType.REPLACE, test_string, initial_selection, TextMatch(TextRange(8, 13)), None,
                               "their")
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is their test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_intersection(self):
    test_string = "This is there test."
    initial_selection = TextRange(9, 15)
    actions = _perform_command(CommandType.REPLACE, test_string, initial_selection, TextMatch(TextRange(8, 13)), None,
                               "our")
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is our test.")
    self.assertEqual(selection, TextRange(11, 11))
    self.assertEqual(clipboard, "")

  def test_replace_different_length(self):
    test_string = "This is they're test."
    initial_selection = TextRange(16, 20)
    actions = _perform_command(CommandType.REPLACE, test_string, initial_selection, TextMatch(TextRange(8, 15)), None,
                               "their")
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is their test.")
    self.assertEqual(selection, TextRange(14, 18))
    self.assertEqual(selection.extract(text), "test")
    self.assertEqual(clipboard, "")

  def test_title_case(self):
    # Ensure first word "a" is capitalized.
    test_string = "a test and a string."
    initial_selection = TextRange(11, 12)
    actions = _perform_command(CommandType.TITLE_CASE, test_string, initial_selection, TextMatch(TextRange(0, 10)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "A Test and a string.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_title_case_full_string(self):
    # Ensure first word "a" is capitalized.
    test_string = "a test and a string."
    initial_selection = TextRange(11, 12)
    actions = _perform_command(CommandType.TITLE_CASE, test_string, initial_selection, TextMatch(TextRange(0, 20)),
                               None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "A Test and a String.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_lowercase(self):
    test_string = "A Test And a String."
    initial_selection = TextRange(11, 12)
    actions = _perform_command(CommandType.LOWERCASE, test_string, initial_selection, TextMatch(TextRange(0, 10)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "a test and a String.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_uppercase(self):
    test_string = "A Test And a String."
    initial_selection = TextRange(11, 12)
    actions = _perform_command(CommandType.UPPERCASE, test_string, initial_selection, TextMatch(TextRange(0, 10)), None)
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "A TEST AND a String.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_word_match_case(self):
    test_string = "This is there test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.REPLACE_WORD_MATCH_CASE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)), None, "Their")
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is their test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_word_match_case_title(self):
    test_string = "This is There test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.REPLACE_WORD_MATCH_CASE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)), None, "their")
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is Their test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")

  def test_replace_word_match_case_all_caps(self):
    test_string = "This is THERE test."
    initial_selection = TextRange(5, 7)
    actions = _perform_command(CommandType.REPLACE_WORD_MATCH_CASE, test_string, initial_selection,
                               TextMatch(TextRange(8, 13)), None, "their")
    text, selection, clipboard = simulate_actions(test_string, initial_selection, actions)
    self.assertEqual(text, "This is THEIR test.")
    self.assertEqual(selection, initial_selection)
    self.assertEqual(clipboard, "")
