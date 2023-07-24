"""Tests for url utils."""

import unittest
from .url_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class UrlTestCase(unittest.TestCase):
  """Test for url utilities."""

  def test_get_query_string_value(self):
    self.assertEqual(get_query_string_value("http://www.example.com/?abc=xyz", "abc"), "xyz")

    # Test nonexistent param name.
    with self.assertRaises(ValueError):
      get_query_string_value("http://www.example.com/?abc=xyz", "def")
