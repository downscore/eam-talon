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


class ExtractUrlTestCase(unittest.TestCase):
  """Test for utility function."""

  def test_plain_url(self):
    text = "Here is a link to Google: https://www.google.com"
    expected = "https://www.google.com"
    self.assertEqual(extract_url(text), expected)

  def test_markdown_url(self):
    text = "Check this [link](https://www.example.com) for more information."
    expected = "https://www.example.com"
    self.assertEqual(extract_url(text), expected)

  def test_no_url(self):
    text = "This is a sentence without a URL."
    expected = None
    self.assertEqual(extract_url(text), expected)

  def test_multiple_urls(self):
    text = "Here is a link: https://www.google.com and another [link](https://www.example.com)."
    expected = "https://www.example.com"  # Markdown URL should be preferred
    self.assertEqual(extract_url(text), expected)

  def test_text_with_spaces_around_url(self):
    text = "Visit this link:  https://www.google.com for more info."
    expected = "https://www.google.com"
    self.assertEqual(extract_url(text), expected)

  def test_markdown_with_spaces(self):
    text = "See the [example]( https://www.example.com ) for details."
    expected = "https://www.example.com"
    self.assertEqual(extract_url(text), expected)
