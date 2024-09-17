# pylint: disable=missing-module-docstring, missing-class-docstring
import unittest
from .scrambler_types import *  # pylint: disable=wildcard-import, unused-wildcard-import


class TextRangeTestCase(unittest.TestCase):
  """Test for counting lines and words in a string."""

  def test_length(self):
    text_range = TextRange(0, 0)
    self.assertEqual(0, text_range.length())

    text_range = TextRange(0, 10)
    self.assertEqual(10, text_range.length())

    text_range = TextRange(5, 10)
    self.assertEqual(5, text_range.length())

  def test_extract(self):
    text_range = TextRange(0, 0)
    self.assertEqual("", text_range.extract("example"))

    text_range = TextRange(7, 7)
    self.assertEqual("", text_range.extract("example"))

    text_range = TextRange(1, 1)
    self.assertEqual("", text_range.extract("example"))

    text_range = TextRange(0, 1)
    self.assertEqual("e", text_range.extract("example"))

    text_range = TextRange(0, 2)
    self.assertEqual("ex", text_range.extract("example"))

    text_range = TextRange(1, 2)
    self.assertEqual("x", text_range.extract("example"))

    text_range = TextRange(1, 3)
    self.assertEqual("xa", text_range.extract("example"))

    # Extract past end of text.
    with self.assertRaises(ValueError):
      text_range = TextRange(1, 8)
      text_range.extract("example")

  def test_invalid_range(self):
    # End before start.
    with self.assertRaises(ValueError):
      TextRange(10, 5)

    # Negative start.
    with self.assertRaises(ValueError):
      TextRange(-10, 5)

    # Huge range.
    with self.assertRaises(ValueError):
      TextRange(0, 500000000)
