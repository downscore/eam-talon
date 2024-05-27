"""Tests for path utils."""

import unittest
from .path_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class ReplaceFileExtensionTestCase(unittest.TestCase):
  """Test for util function."""

  def test_empty_string(self):
    with self.assertRaises(ValueError):
      replace_file_extension("", ".py")

  def test_no_extension(self):
    self.assertEqual(replace_file_extension("file", ".py"), "file.py")

  def test_filename(self):
    self.assertEqual(replace_file_extension("file.txt", ".py"), "file.py")

  def test_remove_extension(self):
    self.assertEqual(replace_file_extension("file.txt", ""), "file")

  def test_path(self):
    self.assertEqual(replace_file_extension("/test1/.test2/file.txt", ".py"), "/test1/.test2/file.py")


class RemoveTestSuffixTestCase(unittest.TestCase):
  """Test for util function."""

  def test_empty_string(self):
    with self.assertRaises(ValueError):
      remove_test_suffix("")

  def test_no_extension(self):
    self.assertEqual(remove_test_suffix("file_test"), "file")

  def test_filename(self):
    self.assertEqual(remove_test_suffix("file.txt"), "file.txt")

  def test_remove_suffix(self):
    self.assertEqual(remove_test_suffix("file_test.py"), "file.py")

  def test_path(self):
    self.assertEqual(remove_test_suffix("/test1/.test2/file_test.py"), "/test1/.test2/file.py")


class GetTestPathTestCase(unittest.TestCase):
  """Test for util function."""

  def test_empty_string(self):
    with self.assertRaises(ValueError):
      get_test_path("", ".py")

  def test_no_extension(self):
    self.assertEqual(get_test_path("file", ".py"), "file_test.py")
    self.assertEqual(get_test_path("file_test", ".py"), "file_test.py")

  def test_filename(self):
    self.assertEqual(get_test_path("file.txt", ".py"), "file_test.py")

  def test_maintain_suffix(self):
    self.assertEqual(get_test_path("file_test.py", ".py"), "file_test.py")

  def test_path(self):
    self.assertEqual(get_test_path("/test1/.test2/file_test.py", ".py"), "/test1/.test2/file_test.py")
    self.assertEqual(get_test_path("/test1/.test2/file.talon", ".py"), "/test1/.test2/file_test.py")
