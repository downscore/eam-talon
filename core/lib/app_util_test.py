"""Tests for app utils."""

import unittest
from .app_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class FilenameToAppLaunchStringTestCase(unittest.TestCase):
  """Test for util function."""

  def test_parsing_filename(self):
    self.assertEqual(filename_to_app_launch_string("test.app", {}), "test")
    self.assertEqual(filename_to_app_launch_string("foo.app", {"Calculator": "calc"}), "foo")
    self.assertEqual(filename_to_app_launch_string("test", {}), "test")
    self.assertEqual(filename_to_app_launch_string("PascalCase.app", {}), "pascal case")
    # Apply override.
    self.assertEqual(filename_to_app_launch_string("Calculator.app", {"Calculator": "calc"}),
                     "calc")
    # Overrides are case sensitive.
    self.assertEqual(filename_to_app_launch_string("calculator.app", {"Calculator": "calc"}),
                     "calculator")
    self.assertEqual(filename_to_app_launch_string("test1", {}), "test")
    self.assertEqual(filename_to_app_launch_string("Test - Case", {}), "test case")
