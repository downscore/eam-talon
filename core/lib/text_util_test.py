"""Tests for text utils."""

import unittest
from .text_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class TextUtilTestCase(unittest.TestCase):
  """Tests for text utilities."""

  def test_count_lines(self):
    self.assertEqual(count_lines(""), 0)
    self.assertEqual(count_lines("\n"), 1)
    self.assertEqual(count_lines("\r"), 1)
    self.assertEqual(count_lines("\r\n"), 1)
    self.assertEqual(count_lines("\n\n"), 2)
    self.assertEqual(count_lines("\r\r"), 2)
    self.assertEqual(count_lines("Hello\n"), 1)
    self.assertEqual(count_lines("Hello\nWorld"), 2)
    self.assertEqual(count_lines("Hello\nWorld\n"), 2)

  def test_count_words(self):
    self.assertEqual(count_words(""), 0)
    self.assertEqual(count_words("\n"), 0)
    self.assertEqual(count_words("\r"), 0)
    self.assertEqual(count_words("\r\n"), 0)
    self.assertEqual(count_words("Hello\n"), 1)
    self.assertEqual(count_words("Hello\nWorld"), 2)
    self.assertEqual(count_words("Hello\nWorld\n"), 2)
    self.assertEqual(count_words("Hello World"), 2)
    self.assertEqual(count_words("Hello  World"), 2)

  def test_sort_lines(self):
    self.assertEqual(sort_lines(""), "")
    self.assertEqual(sort_lines("\n"), "\n")
    self.assertEqual(sort_lines("\r"), "\r")
    self.assertEqual(sort_lines("b\nc\nd\na"), "a\nb\nc\nd")
    self.assertEqual(sort_lines("b\nC\nd\na"), "a\nb\nC\nd")
    self.assertEqual(sort_lines("\n \nb\nC\nd\na\n \n"), "\n \na\nb\nC\nd\n \n")
    self.assertEqual(sort_lines("\n \nb\nC\nd\na\n \n", reverse=True), "\n \nd\nC\nb\na\n \n")


class StrippedStringTestCase(unittest.TestCase):
  """Tests for stripped string class."""

  def test_empty_string(self):
    s = StrippedString("")
    self.assertEqual(s.stripped, "")
    self.assertEqual(s.left_padding, "")
    self.assertEqual(s.right_padding, "")
    self.assertEqual(s.apply_padding("x"), "x")

  def test_unpadded_string(self):
    s = StrippedString("a")
    self.assertEqual(s.stripped, "a")
    self.assertEqual(s.left_padding, "")
    self.assertEqual(s.right_padding, "")
    self.assertEqual(s.apply_padding("x"), "x")

  def test_left_padded_string(self):
    s = StrippedString(" a")
    self.assertEqual(s.stripped, "a")
    self.assertEqual(s.left_padding, " ")
    self.assertEqual(s.right_padding, "")
    self.assertEqual(s.apply_padding("x"), " x")

  def test_right_padded_string(self):
    s = StrippedString("a\n")
    self.assertEqual(s.stripped, "a")
    self.assertEqual(s.left_padding, "")
    self.assertEqual(s.right_padding, "\n")
    self.assertEqual(s.apply_padding("x"), "x\n")

  def test_padded_string(self):
    s = StrippedString("\n a \n ")
    self.assertEqual(s.stripped, "a")
    self.assertEqual(s.left_padding, "\n ")
    self.assertEqual(s.right_padding, " \n ")
    self.assertEqual(s.apply_padding("x"), "\n x \n ")

  def test_keep_first_number(self):
    s = StrippedString("abc12 def", StripMethod.KEEP_FIRST_NUMBER)
    self.assertEqual(s.stripped, "12")
    self.assertEqual(s.left_padding, "abc")
    self.assertEqual(s.right_padding, " def")
    self.assertEqual(s.apply_padding("x"), "abcx def")

  def test_keep_first_number_no_right_padding(self):
    s = StrippedString("abc12", StripMethod.KEEP_FIRST_NUMBER)
    self.assertEqual(s.stripped, "12")
    self.assertEqual(s.left_padding, "abc")
    self.assertEqual(s.right_padding, "")
    self.assertEqual(s.apply_padding("x"), "abcx")

  def test_keep_first_number_no_left_padding(self):
    s = StrippedString("12 def", StripMethod.KEEP_FIRST_NUMBER)
    self.assertEqual(s.stripped, "12")
    self.assertEqual(s.left_padding, "")
    self.assertEqual(s.right_padding, " def")
    self.assertEqual(s.apply_padding("x"), "x def")

  def test_keep_first_number_no_number(self):
    s = StrippedString("abc def", StripMethod.KEEP_FIRST_NUMBER)
    self.assertEqual(s.stripped, "")
    self.assertEqual(s.left_padding, "abc def")
    self.assertEqual(s.right_padding, "")
    self.assertEqual(s.apply_padding("x"), "abc defx")
