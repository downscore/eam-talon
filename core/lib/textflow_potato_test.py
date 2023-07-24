"""Tests for textflow potato mode."""

import unittest
from .textflow_potato import *  # pylint: disable=wildcard-import, unused-wildcard-import


class ConvertActionsTestCase(unittest.TestCase):
  """Test for converting editor actions to potato mode."""

  def test_invalid_input(self):
    # Selection action has no range.
    with self.assertRaises(ValueError):
      convert_actions_to_potato_mode([EditorAction(EditorActionType.SET_SELECTION_RANGE)], "", TextRange(0, 0))

  def test_passthrough_actions(self):
    actions = [
        EditorAction(EditorActionType.CLEAR),
        EditorAction(EditorActionType.INSERT_TEXT, text="abc"),
        EditorAction(EditorActionType.SET_CLIPBOARD_NO_HISTORY, text="bcd"),
        EditorAction(EditorActionType.SET_CLIPBOARD_WITH_HISTORY, text="cde"),
    ]
    result = convert_actions_to_potato_mode(actions, "test", TextRange(0, 0))
    self.assertListEqual(result, [
        PotatoEditorAction(PotatoEditorActionType.CLEAR),
        PotatoEditorAction(PotatoEditorActionType.INSERT_TEXT, text="abc"),
        PotatoEditorAction(PotatoEditorActionType.SET_CLIPBOARD_NO_HISTORY, text="bcd"),
        PotatoEditorAction(PotatoEditorActionType.SET_CLIPBOARD_WITH_HISTORY, text="cde"),
    ])

  def test_idempotent_selection(self):
    # Convert a command to select the range that is already selected.
    actions = [
        EditorAction(EditorActionType.SET_SELECTION_RANGE, TextRange(1, 3)),
    ]
    result = convert_actions_to_potato_mode(actions, "test", TextRange(1, 3))
    self.assertListEqual(result, [])

  def test_selection_left(self):
    actions = [
        EditorAction(EditorActionType.SET_SELECTION_RANGE, TextRange(5, 7)),
    ]
    result = convert_actions_to_potato_mode(actions, "This is a test.", TextRange(8, 9))
    self.assertListEqual(
        result,
        [
            # Collapse selection.
            PotatoEditorAction(PotatoEditorActionType.GO_LEFT, repeat=1),
            # Move to start.
            PotatoEditorAction(PotatoEditorActionType.GO_LEFT, repeat=3),
            # Expand selection.
            PotatoEditorAction(PotatoEditorActionType.EXTEND_RIGHT, repeat=2),
        ])

  def test_selection_left_multiple_words(self):
    actions = [
        EditorAction(EditorActionType.SET_SELECTION_RANGE, TextRange(0, 4)),
    ]
    result = convert_actions_to_potato_mode(actions, "This is a test.", TextRange(12, 12))
    self.assertListEqual(
        result,
        [
            # Move to start.
            PotatoEditorAction(PotatoEditorActionType.GO_LEFT, repeat=12),
            # Expand selection.
            PotatoEditorAction(PotatoEditorActionType.EXTEND_RIGHT, repeat=4),
        ])

  def test_selection_right(self):
    actions = [
        EditorAction(EditorActionType.SET_SELECTION_RANGE, TextRange(10, 14)),
    ]
    result = convert_actions_to_potato_mode(actions, "This is a test.", TextRange(8, 9))
    self.assertListEqual(
        result,
        [
            # Collapse selection.
            PotatoEditorAction(PotatoEditorActionType.GO_RIGHT, repeat=1),
            # Move to start.
            PotatoEditorAction(PotatoEditorActionType.GO_RIGHT, repeat=1),
            # Expand selection.
            PotatoEditorAction(PotatoEditorActionType.EXTEND_RIGHT, repeat=4),
        ])

  def test_selection_right_multiple_words(self):
    actions = [
        EditorAction(EditorActionType.SET_SELECTION_RANGE, TextRange(10, 14)),
    ]
    result = convert_actions_to_potato_mode(actions, "This is a test.", TextRange(2, 2))
    self.assertListEqual(
        result,
        [
            # Move to start.
            PotatoEditorAction(PotatoEditorActionType.GO_RIGHT, repeat=8),
            # Expand selection.
            PotatoEditorAction(PotatoEditorActionType.EXTEND_RIGHT, repeat=4),
        ])
