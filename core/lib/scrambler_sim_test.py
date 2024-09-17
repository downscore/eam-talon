# pylint: disable=missing-module-docstring, missing-class-docstring
import unittest
from .scrambler_sim import *  # pylint: disable=wildcard-import, unused-wildcard-import


class SimulateActionsTestCase(unittest.TestCase):

  def test_set_selection_range(self):
    context = Context("This is a test", TextRange(0, 0), editor_mode="i")
    clipboard = simulate_actions(
        context, [EditorAction(EditorActionType.SET_SELECTION_RANGE, TextRange(0, 4))])
    self.assertEqual(context.selection_range, TextRange(0, 4))
    self.assertEqual(context.text, "This is a test")
    self.assertEqual(context.editor_mode, "v")
    self.assertEqual(clipboard, "")

  def test_set_selection_range_empty(self):
    context = Context("This is a test", TextRange(0, 0), editor_mode="n")
    clipboard = simulate_actions(
        context, [EditorAction(EditorActionType.SET_SELECTION_RANGE, TextRange(5, 5))])
    self.assertEqual(context.selection_range, TextRange(5, 5))
    self.assertEqual(context.text, "This is a test")
    self.assertEqual(context.editor_mode, "i")
    self.assertEqual(clipboard, "")

  def test_insert_text(self):
    context = Context("This is a test", TextRange(5, 5), editor_mode="v")
    clipboard = simulate_actions(context,
                                 [EditorAction(EditorActionType.INSERT_TEXT, text="also ")])
    self.assertEqual(context.selection_range, TextRange(10, 10))
    self.assertEqual(context.text, "This also is a test")
    self.assertEqual(context.editor_mode, "i")
    self.assertEqual(clipboard, "")

  def test_set_clipboard(self):
    context = Context("This is a test", TextRange(5, 5), editor_mode="v")
    clipboard = simulate_actions(
        context, [EditorAction(EditorActionType.SET_CLIPBOARD_NO_HISTORY, text="Copied")])
    self.assertEqual(context.selection_range, TextRange(5, 5))
    self.assertEqual(context.text, "This is a test")
    self.assertEqual(context.editor_mode, "v")
    self.assertEqual(clipboard, "Copied")

  def test_delete_range(self):
    context = Context("This is a test", TextRange(5, 5), editor_mode="v")
    clipboard = simulate_actions(context,
                                 [EditorAction(EditorActionType.DELETE_RANGE, TextRange(5, 10))])
    self.assertEqual(context.selection_range, TextRange(5, 5))
    self.assertEqual(context.text, "This test")
    self.assertEqual(context.editor_mode, "i")
    self.assertEqual(clipboard, "")

  def test_invalid_input(self):
    # Index OOB
    with self.assertRaises(ValueError):
      context = Context("This is a test", TextRange(100, 200), editor_mode="i")
      simulate_actions(context, [])

    # Set selection range with no range.
    with self.assertRaises(ValueError):
      context = Context("This is a test", TextRange(0, 0), editor_mode="i")
      simulate_actions(context, [EditorAction(EditorActionType.SET_SELECTION_RANGE)])

    # Set selection range outside of text.
    with self.assertRaises(ValueError):
      context = Context("This is a test", TextRange(0, 0), editor_mode="i")
      simulate_actions(context,
                       [EditorAction(EditorActionType.SET_SELECTION_RANGE, TextRange(0, 100))])

    # Set deletion range with no range.
    with self.assertRaises(ValueError):
      context = Context("This is a test", TextRange(0, 0), editor_mode="i")
      simulate_actions(context, [EditorAction(EditorActionType.DELETE_RANGE)])
