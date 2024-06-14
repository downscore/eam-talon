"""Tests for applying modifiers."""

import unittest
from .textflow_modifiers import *  # pylint: disable=wildcard-import, unused-wildcard-import


class TestLineIncludingLineBreakModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_apply_line_modifier_single_line(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test string.")

  def test_apply_line_modifier_trailing_newline(self):
    text = "This is a test string.\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "")

  def test_apply_line_modifier_multi_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test string.\n")

  def test_apply_line_modifier_last_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Another line of text.")

  def test_apply_line_modifier_middle_line(self):
    text = "This is a test string.\nAnother line of text.\nThe last line."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Another line of text.\n")

  def test_apply_line_modifier_empty_line(self):
    text = "This is a test string.\n\nAnother line of text."
    input_match = TextMatch(TextRange(23, 23))  # empty line
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)

    self.assertEqual(result, TextMatch(TextRange(23, 24)))

  def test_apply_line_modifier_invalid_match(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.LINE_INCLUDING_LINE_BREAK, None)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier)


class TestLineExcludingLineBreakModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_apply_line_modifier_single_line(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test string.")

  def test_apply_line_modifier_trailing_newline(self):
    text = "This is a test string.\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "")

  def test_apply_line_modifier_multi_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a test string.")

  def test_apply_line_modifier_last_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Another line of text.")

  def test_apply_line_modifier_middle_line(self):
    text = "This is a test string.\nAnother line of text.\nThe last line."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Another line of text.")

  def test_apply_line_modifier_empty_line(self):
    text = "This is a test string.\n\nAnother line of text."
    input_match = TextMatch(TextRange(23, 23))  # empty line
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_apply_line_modifier_invalid_match(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.LINE_EXCLUDING_LINE_BREAK, None)
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

  def test_line_comment_between_code(self):
    text = "y -= 4\n# My comment.\nx += 5"
    input_match = TextMatch(TextRange(9, 11))  # "My"
    modifier = Modifier(ModifierType.COMMENT, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "# My comment.")

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
    self.assertEqual(result.text_range.extract(text), "test string")

  def test_apply_string_modifier_different_delimiter(self):
    text = "This is a 'test string'."
    input_match = TextMatch(TextRange(11, 15))  # "test"
    modifier = Modifier(ModifierType.STRING, None, "'")
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "test string")

  def test_apply_string_modifier_nested_string(self):
    text = "This is a \"nested \"test\" string\"."
    input_match = TextMatch(TextRange(19, 23))  # "test"
    modifier = Modifier(ModifierType.STRING, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "test")

  def test_apply_string_modifier_nested_string_outside(self):
    text = "This is a \"nested \"test\" string\"."
    input_match = TextMatch(TextRange(11, 17))  # "nested"
    modifier = Modifier(ModifierType.STRING, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "nested ")

  def test_apply_string_modifier_multiple_strings(self):
    text = "This is a \"test string\" and \"another string\"."
    input_match = TextMatch(TextRange(11, 15))  # "test"
    modifier = Modifier(ModifierType.STRING, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "test string")

  def test_apply_string_modifier_no_string(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.STRING, None)
    result = apply_modifier(text, input_match, modifier)
    # Modifier does not modify result.
    self.assertEqual(result.text_range.extract(text), "This is a test string.")

  def test_apply_string_modifier_invalid_match(self):
    text = "This is a \"test string\"."
    input_match = TextMatch(TextRange(100, 104))
    modifier = Modifier(ModifierType.STRING, None)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier)


class TestCharsModifier(unittest.TestCase):
  """Tests for applying character modifiers."""

  def test_single_char(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.CHARS, TextRange(1, 2))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "e")

  def test_first_char(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.CHARS, TextRange(0, 1))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "t")

  def test_multiple_chars(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.CHARS, TextRange(1, 3))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "es")

  def test_full_word(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.CHARS, TextRange(0, 4))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "test")

  def test_longer_than_word(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.CHARS, TextRange(0, 5))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "test")

  def test_beyond_word(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.CHARS, TextRange(50, 55))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "")

  def test_missing_range(self):
    with self.assertRaises(ValueError):
      modifier = Modifier(ModifierType.CHARS, None)
      apply_modifier("test", TextMatch(TextRange(1, 2)), modifier)


class TestFragmentsModifier(unittest.TestCase):
  """Tests for applying fragment modifiers."""

  def test_single_word(self):
    text = "This_is_the_test_string."
    input_match = TextMatch(TextRange(0, len(text)))
    modifier = Modifier(ModifierType.FRAGMENTS, TextRange(1, 2))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "is")

  def test_single_word_pascal(self):
    text = "ThisIsTheTestString."
    input_match = TextMatch(TextRange(0, len(text)))
    modifier = Modifier(ModifierType.FRAGMENTS, TextRange(1, 2))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Is")

  def test_multiple_words(self):
    text = "This_is_the_test_string."
    input_match = TextMatch(TextRange(0, len(text)))
    modifier = Modifier(ModifierType.FRAGMENTS, TextRange(1, 4))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "is_the_test")

  def test_multiple_words_pascal(self):
    text = "ThisIsTheTestString."
    input_match = TextMatch(TextRange(0, len(text)))
    modifier = Modifier(ModifierType.FRAGMENTS, TextRange(1, 4))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "IsTheTest")

  def test_beyond_token(self):
    text = "This_is_the_test_string."
    input_match = TextMatch(TextRange(0, len(text)))
    modifier = Modifier(ModifierType.FRAGMENTS, TextRange(10, 12))
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range, TextRange(len(text), len(text)))

  def test_missing_range(self):
    with self.assertRaises(ValueError):
      modifier = Modifier(ModifierType.FRAGMENTS, None)
      apply_modifier("test", TextMatch(TextRange(1, 2)), modifier)


class TestLineHeadModifier(unittest.TestCase):
  """Tests for applying line head modifiers."""

  def test_first_line(self):
    # Second line starts at char 17.
    # Third line starts at char 34.
    text = "Test first line.\nThe second line.\nFinal text."
    input_match = TextMatch(TextRange(5, 10))
    modifier = Modifier(ModifierType.LINE_HEAD)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Test first")

  def test_middle_line(self):
    text = "Test first line.\nThe second line.\nFinal text."
    input_match = TextMatch(TextRange(22, 27))
    modifier = Modifier(ModifierType.LINE_HEAD)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "The second")


class TestLineTailModifier(unittest.TestCase):
  """Tests for applying line tail modifiers."""

  def test_first_line(self):
    # Second line starts at char 17.
    # Third line starts at char 34.
    text = "Test first line.\nThe second line.\nFinal text."
    input_match = TextMatch(TextRange(5, 10))
    modifier = Modifier(ModifierType.LINE_TAIL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "first line.")

  def test_middle_line(self):
    text = "Test first line.\nThe second line.\nFinal text."
    input_match = TextMatch(TextRange(21, 27))
    modifier = Modifier(ModifierType.LINE_TAIL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "second line.")

  def test_last_line(self):
    text = "Test first line.\nThe second line.\nFinal text."
    input_match = TextMatch(TextRange(37, 38))
    modifier = Modifier(ModifierType.LINE_TAIL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "al text.")


class TestPythonScopeModifier(unittest.TestCase):
  """Tests for applying Python scope modifiers."""

  def test_not_in_code(self):
    text = "\n\nprint('Hello, world!')"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier)

  def test_single_line(self):
    text = "print('Hello, world!')"
    input_match = TextMatch(TextRange(7, 12))
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "print('Hello, world!')")

  def test_single_line_cursor_at_file_start(self):
    text = "print('Hello, world!')"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "print('Hello, world!')")

  def test_single_line_trailing_newline(self):
    text = "print('Hello, world!')\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "print('Hello, world!')\n")

  def test_function(self):
    text = """
      def test_function():
          print('Hello, world!')
          x = 5
          y = x + 1
          return y

      def test_function2():
          print('Test!')
          a = 3
    """
    input_match = TextMatch(TextRange(38, 43))  # print
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.start, 28)
    self.assertEqual(result.text_range.end, 116)

  def test_function_with_indentation(self):
    text = """
      def test_function():
          print('Hello, world!')
          if x > 6:
            x = x + 5
          return x

      def test_function2():
          print('Test!')
          a = 3
    """
    input_match = TextMatch(TextRange(38, 43))  # print
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.start, 28)
    self.assertEqual(result.text_range.end, 122)

  def test_function_with_empty_linw(self):
    # "Empty" line has some space characters.
    text = """
      def test_function():
          print('Hello, world!')

          x = x + 5
          return x

      def test_function2():
          print('Test!')
          a = 3
    """
    input_match = TextMatch(TextRange(38, 43))  # print
    modifier = Modifier(ModifierType.PYTHON_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.start, 28)
    self.assertEqual(result.text_range.end, 101)


class TestCScopeModifier(unittest.TestCase):
  """Tests for applying C scope modifiers."""

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.C_SCOPE)
    self.assertEqual(apply_modifier(text, input_match, modifier), input_match)

  def test_not_in_code(self):
    text = "\n\ncout << \"Hello, world!\";"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "\ncout << \"Hello, world!\";")

  def test_opening_brace_only(self):
    text = "{"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.start, 1)
    self.assertEqual(result.text_range.end, 1)

  def test_single_line(self):
    text = "{ cout << \"Hello, world!\"; }"
    input_match = TextMatch(TextRange(11, 16))  # "Hello"
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), " cout << \"Hello, world!\";")

  def test_function(self):
    text = """
      void test_function() {
          cout << "Hello, world!";
          int x = 5;
          int y = x + 1;
      }

      void test_function2() {
          cout << "Test!";
          int a = 3;
      }
    """
    input_match = TextMatch(TextRange(49, 54))  # "Hello"
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.start, 30)
    self.assertEqual(result.text_range.end, 111)

  def test_function_nested_before(self):
    text = """
      void test_function() {
          cout << "Hello, world!";
          int x = 5;
          if (x > 6) {
            x = x + 5;
          }
          int y = x + 1;
      }

      void test_function2() {
          cout << "Test!";
          int a = 3;
      }
    """
    input_match = TextMatch(TextRange(154, 157))  # "int"
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.start, 30)
    self.assertEqual(result.text_range.end, 169)

  def test_function_nested_after(self):
    text = """
      void test_function() {
          cout << "Hello, world!";
          int x = 5;
          if (x > 6) {
            x = x + 5;
          }
          int y = x + 1;
      }

      void test_function2() {
          cout << "Test!";
          int a = 3;
      }
    """
    input_match = TextMatch(TextRange(49, 54))  # "Hello"
    modifier = Modifier(ModifierType.C_SCOPE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.start, 30)
    self.assertEqual(result.text_range.end, 169)


class TestArgumentModifier(unittest.TestCase):
  """Tests for applying argument modifiers."""

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.ARG)
    self.assertEqual(apply_modifier(text, input_match, modifier), input_match)

  def test_simple_call(self):
    text = "my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(14, 15))
    modifier = Modifier(ModifierType.ARG)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "arg2")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), ", arg2")

  def test_for_loop(self):
    text = "for (arg1; arg2; arg3);"
    input_match = TextMatch(TextRange(12, 13))
    modifier = Modifier(ModifierType.ARG)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "arg2")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "; arg2")

  def test_for_loop_first_arg(self):
    text = "for (arg1; arg2; arg3);"
    input_match = TextMatch(TextRange(6, 7))
    modifier = Modifier(ModifierType.ARG)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "arg1")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "arg1; ")

  def test_first_argument(self):
    text = "my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(9, 10))
    modifier = Modifier(ModifierType.ARG)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "arg1")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "arg1, ")

  def test_last_argument(self):
    text = "my_func(arg1, arg2, arg3);"
    input_match = TextMatch(TextRange(21, 22))
    modifier = Modifier(ModifierType.ARG)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "arg3")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), ", arg3")

  def test_surrounding_whitespace(self):
    text = "my_func( arg );"
    input_match = TextMatch(TextRange(10, 11))
    modifier = Modifier(ModifierType.ARG)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "arg")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " arg ")

  def test_nested_call_before(self):
    text = "f1(arg1, f2(arg2), arg3);"
    input_match = TextMatch(TextRange(17, 17))
    modifier = Modifier(ModifierType.ARG)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "f2(arg2)")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), ", f2(arg2)")

  def test_nested_call_after(self):
    text = "f1(arg1, f2(arg2), arg3);"
    input_match = TextMatch(TextRange(10, 11))
    modifier = Modifier(ModifierType.ARG)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "f2(arg2)")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), ", f2(arg2)")


class TestSentenceModifier(unittest.TestCase):
  """Tests for applying sentence modifiers."""

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.SENTENCE)
    self.assertEqual(apply_modifier(text, input_match, modifier), input_match)

  def test_single_sentence(self):
    text = "This is a sentence."
    input_match = TextMatch(TextRange(7, 9))
    modifier = Modifier(ModifierType.SENTENCE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a sentence.")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This is a sentence.")

  def test_first_sentence(self):
    text = "This is a sentence. Here is another sentence!"
    input_match = TextMatch(TextRange(7, 9))
    modifier = Modifier(ModifierType.SENTENCE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is a sentence.")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This is a sentence. ")

  def test_last_sentence(self):
    text = "This is a sentence. Here is another sentence!"
    input_match = TextMatch(TextRange(25, 27))
    modifier = Modifier(ModifierType.SENTENCE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "Here is another sentence!")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), " Here is another sentence!")

  def test_newline_delimited(self):
    text = "## Markdown Header\n\nThis is my sentence."
    input_match = TextMatch(TextRange(25, 27))
    modifier = Modifier(ModifierType.SENTENCE)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "This is my sentence.")
    assert result.deletion_range is not None
    self.assertEqual(result.deletion_range.extract(text), "This is my sentence.")


class TestCallModifier(unittest.TestCase):
  """Tests for applying function call modifiers."""

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.CALL)
    self.assertEqual(apply_modifier(text, input_match, modifier), input_match)

  def test_single_call(self):
    text = "func(x, y);"
    input_match = TextMatch(TextRange(1, 2))
    modifier = Modifier(ModifierType.CALL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "func(x, y)")

  def test_single_call_cursor_at_func_name_start(self):
    text = "func(x, y);"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.CALL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "func(x, y)")

  def test_single_call_cursor_at_open_parenthesis(self):
    text = "func(x, y);"
    input_match = TextMatch(TextRange(4, 4))
    modifier = Modifier(ModifierType.CALL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "func(x, y)")

  def test_single_call_c_namespace(self):
    text = "namespace::func(x, y);"
    input_match = TextMatch(TextRange(12, 12))
    modifier = Modifier(ModifierType.CALL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "namespace::func(x, y)")

  def test_nested_call(self):
    text = "func(x, func2(y));"
    input_match = TextMatch(TextRange(1, 2))
    modifier = Modifier(ModifierType.CALL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "func(x, func2(y))")

  def test_complex_call(self):
    text = "(*obj)->get_thing().field[0].method(arg1, &arg2, arg3);"
    input_match = TextMatch(TextRange(20, 21))
    modifier = Modifier(ModifierType.CALL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "(*obj)->get_thing().field[0].method(arg1, &arg2, arg3)")

  def test_parenthesis_before_call(self):
    text = "(func(x, func2(y));"
    input_match = TextMatch(TextRange(2, 3))
    modifier = Modifier(ModifierType.CALL)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "func(x, func2(y))")


class TestBracketModifier(unittest.TestCase):
  """Tests for applying bracket modifiers."""

  def test_empty_string(self):
    text = ""
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.BRACKETS)
    self.assertEqual(apply_modifier(text, input_match, modifier), input_match)

  def test_simple_brackets(self):
    text = "[test]"
    input_match = TextMatch(TextRange(1, 2))
    modifier = Modifier(ModifierType.BRACKETS)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "test")

  def test_no_opening_bracket(self):
    text = "test]"
    input_match = TextMatch(TextRange(1, 2))
    modifier = Modifier(ModifierType.BRACKETS)
    with self.assertRaises(ValueError):
      apply_modifier(text, input_match, modifier)

  def test_nested_brackets_outside(self):
    text = "([test])"
    input_match = TextMatch(TextRange(2, 3))
    modifier = Modifier(ModifierType.BRACKETS)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "test")

  def test_nested_brackets_before(self):
    text = "[before[nest]after]"
    input_match = TextMatch(TextRange(14, 15))
    modifier = Modifier(ModifierType.BRACKETS)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "before[nest]after")

  def test_nested_brackets_after(self):
    text = "[before[nest]after]"
    input_match = TextMatch(TextRange(3, 4))
    modifier = Modifier(ModifierType.BRACKETS)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result.text_range.extract(text), "before[nest]after")


class TestStartOfLineModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_single_line(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.START_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(0, 0)))

  def test_trailing_newline(self):
    text = "This is a test string.\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.START_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_multi_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.START_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(0, 0)))

  def test_last_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.START_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_middle_line(self):
    text = "This is a test string.\nAnother line of text.\nThe last line."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.START_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))


class TestEndOfLineModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_single_line(self):
    text = "This is a test string."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.END_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(22, 22)))

  def test_trailing_newline(self):
    text = "This is a test string.\n"
    input_match = TextMatch(TextRange(len(text), len(text)))
    modifier = Modifier(ModifierType.END_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_multi_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(10, 14))  # "test"
    modifier = Modifier(ModifierType.END_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(23, 23)))

  def test_last_line(self):
    text = "This is a test string.\nAnother line of text."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.END_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(44, 44)))

  def test_middle_line(self):
    text = "This is a test string.\nAnother line of text.\nThe last line."
    input_match = TextMatch(TextRange(23, 29))  # "Another"
    modifier = Modifier(ModifierType.END_OF_LINE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(45, 45)))


class TestBetweenWhitespaceModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_single_word(self):
    text = "test"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(0, 4), deletion_range=TextRange(0, 4)))

  def test_sentence(self):
    text = "This is a test."
    input_match = TextMatch(TextRange(5, 5))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(5, 7), deletion_range=TextRange(5, 8)))

  def test_end_of_sentence(self):
    text = "This is a test."
    input_match = TextMatch(TextRange(11, 12))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(10, 15), deletion_range=TextRange(9, 15)))

  def test_line_breaks(self):
    text = "This\nis\na test."
    input_match = TextMatch(TextRange(5, 5))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(5, 7), deletion_range=TextRange(5, 8)))

  def test_path_in_sentence(self):
    text = "Path ~/test/a_b/c-d/* is invalid."
    input_match = TextMatch(TextRange(6, 7))
    modifier = Modifier(ModifierType.BETWEEN_WHITESPACE, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(5, 21), deletion_range=TextRange(5, 22)))


class TestMarkdownLinkModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_link_only(self):
    text = "[link](url)"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.MARKDOWN_LINK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(0, 11)))

  def test_from_link_text(self):
    text = "This is a [link](url) to a site"
    input_match = TextMatch(TextRange(12, 13))
    modifier = Modifier(ModifierType.MARKDOWN_LINK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(10, 21)))

  def test_from_url(self):
    text = "This is a [link](url) to a site"
    input_match = TextMatch(TextRange(18, 19))
    modifier = Modifier(ModifierType.MARKDOWN_LINK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(10, 21)))

  def test_from_link_text_bracket(self):
    text = "This is a [link](url) to a site"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.MARKDOWN_LINK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(10, 21)))

  def test_from_url_bracket(self):
    text = "This is a [link](url) to a site"
    input_match = TextMatch(TextRange(21, 21))
    modifier = Modifier(ModifierType.MARKDOWN_LINK, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(10, 21)))


class TestEndOfMarkdownSectionModifier(unittest.TestCase):
  """Tests for applying modifiers."""

  def test_no_headings(self):
    text = "[link](url)"
    input_match = TextMatch(TextRange(1, 1))
    modifier = Modifier(ModifierType.END_OF_MARKDOWN_SECTION, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(11, 11)))

  def test_from_start_of_heading(self):
    text = "## Heading\nTest line one\nTest line two\n\n## Next Heading"
    input_match = TextMatch(TextRange(0, 0))
    modifier = Modifier(ModifierType.END_OF_MARKDOWN_SECTION, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))

  def test_from_end_of_heading(self):
    text = "## Heading\nTest line one\nTest line two\n\n## Next Heading"
    input_match = TextMatch(TextRange(10, 10))
    modifier = Modifier(ModifierType.END_OF_MARKDOWN_SECTION, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))

  def test_from_after_heading(self):
    text = "## Heading\nTest line one\nTest line two\n\n## Next Heading"
    input_match = TextMatch(TextRange(11, 11))
    modifier = Modifier(ModifierType.END_OF_MARKDOWN_SECTION, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))

  def test_from_whitespace_before_next_heading(self):
    text = "## Heading\nTest line one\nTest line two\n\n## Next Heading"
    input_match = TextMatch(TextRange(39, 39))
    modifier = Modifier(ModifierType.END_OF_MARKDOWN_SECTION, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))

  def test_search_until_eof(self):
    text = "## Heading\nTest line one\nTest line two\n\n"
    input_match = TextMatch(TextRange(13, 13))
    modifier = Modifier(ModifierType.END_OF_MARKDOWN_SECTION, None)
    result = apply_modifier(text, input_match, modifier)
    self.assertEqual(result, TextMatch(TextRange(38, 38)))
