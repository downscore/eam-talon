"""Tests for simulating textflow actions."""

import unittest
from .textflow_sim import *  # pylint: disable=wildcard-import, unused-wildcard-import


class SimulateActionsTestCase(unittest.TestCase):
  """Test for simulating editor actions."""

  def test_invalid_input(self):
    # Index OOB
    with self.assertRaises(ValueError):
      simulate_actions("This is a test", TextRange(100, 200), [])

    # Set selection range with no range.
    with self.assertRaises(ValueError):
      simulate_actions("This is a test", TextRange(0, 0),
                       [EditorAction(EditorActionType.SET_SELECTION_RANGE)])

    # Set selection range outside of text.
    with self.assertRaises(ValueError):
      simulate_actions("This is a test", TextRange(0, 0),
                       [EditorAction(EditorActionType.SET_SELECTION_RANGE, TextRange(0, 100))])
