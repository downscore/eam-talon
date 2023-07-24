"""Tests for applying modifiers."""

import unittest
from .textflow_modifiers import *  # pylint: disable=wildcard-import, unused-wildcard-import


class TestLineModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_apply_line_modifier_single_line(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test string.")

  def test_apply_line_modifier_multi_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test string.\n")

  def test_apply_line_modifier_last_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Another line of text.")

  def test_apply_line_modifier_middle_line(self):
    text = "This is a test string.\nAnother line of text.\nThe last line."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Another line of text.\n")

  def test_apply_line_modifier_empty_line(self):
    text = "This is a test string.\n\nAnother line of text."
    input_match = TextMatch(TextRange(23, 23))  # empty line
    modifier = Modifier(ModifierType.LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(23, 24)))

  def test_apply_line_modifier_invalid_match(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.LINE, None)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier)


class TestCommentModifier(unittest.TestCase):
  """Tests for applying comment modifiers."""

  def test_apply_comment_modifier_single_line(self):
    text = "This is a #test comment string."
    input_match = TextMatch(TextRange(11, 15))  # "test"
    modifier = Modifier(ModifierType.COMMENT, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "#test comment string.")

  def test_apply_comment_modifier_multi_line(self):
    text = "This is a /*test comment\nmultiline string.*/"
    input_match = TextMatch(TextRange(12, 16))  # "test"
    modifier = Modifier(ModifierType.COMMENT, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "/*test comment\nmultiline string.*/")

  def test_apply_comment_modifier_multi_line_cursor_in_delimiter(self):
    text = "This is a /*test comment\nmultiline string.*/"
    input_match = TextMatch(TextRange(11, 11))
    modifier = Modifier(ModifierType.COMMENT, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "/*test comment\nmultiline string.*/")

  def test_apply_comment_modifier_c_style_line_comment(self):
    text = "This is a //test comment string."
    input_match = TextMatch(TextRange(12, 16))  # "test"
    modifier = Modifier(ModifierType.COMMENT, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "//test comment string.")

  def test_apply_comment_modifier_nested_comments(self):
    text = "This is a /*test comment\nnested multiline string.\nend of comment*/"
    input_match = TextMatch(TextRange(12, 16))  # "test"
    modifier = Modifier(ModifierType.COMMENT, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "/*test comment\nnested multiline string.\nend of comment*/")

  def test_apply_comment_modifier_no_comment(self):
    text = "This is a test string with no comment."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.COMMENT, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, input_match)

  def test_apply_comment_modifier_invalid_match(self):
    text = "This is a #test comment string."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.COMMENT, None)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier)


class TestBlockModifier(unittest.TestCase):
  """Tests for applying block modifiers."""

  def test_apply_block_modifier_single_block(self):
    text = "This is a test block."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test block.")

  def test_apply_block_modifier_multi_block(self):
    text = "This is a test block.\n\nAnother block of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test block.")

  def test_apply_block_modifier_multi_line_block(self):
    text = "This is a test block\nwith multiple lines.\n\nAnother block of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test block\nwith multiple lines.")

  def test_apply_block_modifier_last_block(self):
    text = "This is a test block.\n\nAnother block of text."
    input_match = TextMatch(TextRange(24, 30))  # "Another"
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Another block of text.")

  def test_apply_block_modifier_middle_block(self):
    text = "This is a test block.\n\nAnother block of text.\n\nThe last block."
    input_match = TextMatch(TextRange(24, 30))  # "Another"
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Another block of text.")

  def test_apply_block_modifier_invalid_match(self):
    text = "This is a test block."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.BLOCK, None)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier)

  def test_apply_block_modifier_last_block_zero_length_match(self):
    text = "This is a test block.\n\nAnother block of text."
    input_match = TextMatch(TextRange(28, 28))
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Another block of text.")

  def test_apply_block_modifier_balanced_braces(self):
    text = "if (something) {\nThis is a test block.\n}\n\nAnother block of text.}"
    input_match = TextMatch(TextRange(27, 31))  # "test"
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "if (something) {\nThis is a test block.\n}")

  def test_apply_block_modifier_unbalanced_open_brace(self):
    text = "if (something) {\nThis is a test block.\n\nAnother block of text."
    input_match = TextMatch(TextRange(27, 31))  # "test"
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test block.")

  def test_apply_block_modifier_unbalanced_open_braces(self):
    text = "if (something) {\nif(something else) {\nThis is a test block.\n\nAnother block of text."
    input_match = TextMatch(TextRange(48, 52))  # "test"
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test block.")

  def test_apply_block_modifier_unbalanced_closing_brace(self):
    text = "This is a test block.\n}\n\nAnother block of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.BLOCK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test block.\n")


class TestStringModifier(unittest.TestCase):
  """Tests for applying string modifiers."""

  def test_apply_string_modifier_single_string(self):
    text = "This is a \"test string\"."
    input_match = TextMatch(TextRange(11, 15))  # "test"
    modifier = Modifier(ModifierType.STRING, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "\"test string\"")

  def test_apply_string_modifier_nested_string(self):
    text = "This is a \"nested \"test\" string\"."
    input_match = TextMatch(TextRange(19, 23))  # "test"
    modifier = Modifier(ModifierType.STRING, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "\"test\"")

  def test_apply_string_modifier_nested_string_outside(self):
    text = "This is a \"nested \"test\" string\"."
    input_match = TextMatch(TextRange(11, 17))  # "nested"
    modifier = Modifier(ModifierType.STRING, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "\"nested \"")

  def test_apply_string_modifier_multiple_strings(self):
    text = "This is a \"test string\" and \"another string\"."
    input_match = TextMatch(TextRange(11, 15))  # "test"
    modifier = Modifier(ModifierType.STRING, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "\"test string\"")

  def test_apply_string_modifier_no_string(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.STRING, None)
    result = apply_modifier(text, input_match, modifier)
    # Modifier does not modify result.
    self.assertEqual(result.text_range.extract(text), "test")

  def test_apply_string_modifier_invalid_match(self):
    text = "This is a \"test string\"."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.STRING, None)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier)
