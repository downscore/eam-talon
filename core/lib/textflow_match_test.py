"""Tests for text matching."""

import unittest
from .textflow_match import *  # pylint: disable=wildcard-import, unused-wildcard-import

_SAMPLE_TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat."""

_TEXT_BEFORE = """Match.span([group])
For a match m, return the 2-tuple (m.start(group), m.end(group)). Note that if group did not contribute to the match,
this is (-1, -1). group defaults to zero, the entire match."""

_TEXT_AFTER = """Pattern.findall(string[, pos[, endpos]])
Similar to the findall() function, using the compiled pattern, but also accepts optional pos and endpos parameters that
limit the search region like for search()."""

_FORMATTED_TOKENS = "camelCaseOne snake_var_name camelCaseTwo kebab-str-ing dot.sep.name ! _ PascalEndOfSentence. Tim's"

_SIMILAR_LINES = """  Indented Line 1 - Line content
  Indented Line 2 - Line content unknown
Unindented Line 3 - Line content"""

_REGEX_WORD: re.Pattern = re.compile(r"\w+")


def _get_homophones_mock(word: str) -> list[str]:
  """Mock function for getting homophones."""
  sample_phones = ["there", "their", "they're"]
  if word in sample_phones:
    return sample_phones
  return [word]


class GetNthRegexMatchTestCase(unittest.TestCase):
  """Tests for getting the nth match of a regex."""

  def test_first_word_forward(self):
    match = get_nth_regex_match(_SAMPLE_TEXT, _REGEX_WORD, 1, SearchDirection.FORWARD)
    assert match is not None
    self.assertEqual(match.span(), (0, 5))
    self.assertEqual(match.group(), "Lorem")

  def test_second_word_forward(self):
    match = get_nth_regex_match(_SAMPLE_TEXT, _REGEX_WORD, 2, SearchDirection.FORWARD)
    assert match is not None
    self.assertEqual(match.span(), (6, 11))
    self.assertEqual(match.group(), "ipsum")

  def test_first_word_backward(self):
    match = get_nth_regex_match(_SAMPLE_TEXT, _REGEX_WORD, 1, SearchDirection.BACKWARD)
    assert match is not None
    self.assertEqual(match.span(), (221, 230))
    self.assertEqual(match.group(), "consequat")

  def test_second_word_backward(self):
    match = get_nth_regex_match(_SAMPLE_TEXT, _REGEX_WORD, 2, SearchDirection.BACKWARD)
    assert match is not None
    self.assertEqual(match.span(), (213, 220))
    self.assertEqual(match.group(), "commodo")

  def test_word_includes_numbers(self):
    match = get_nth_regex_match("First 22 third", _REGEX_WORD, 2, SearchDirection.FORWARD)
    assert match is not None
    self.assertEqual(match.span(), (6, 8))
    self.assertEqual(match.group(), "22")

  def test_single_letter(self):
    match = get_nth_regex_match("a", _REGEX_WORD, 1, SearchDirection.FORWARD)
    assert match is not None
    self.assertEqual(match.span(), (0, 1))
    self.assertEqual(match.group(), "a")

  def test_empty_string(self):
    match = get_nth_regex_match("", _REGEX_WORD, 1, SearchDirection.FORWARD)
    self.assertTrue(match is None)

  def test_search_past_end(self):
    match = get_nth_regex_match(_SAMPLE_TEXT, _REGEX_WORD, 1000, SearchDirection.FORWARD)
    self.assertTrue(match is None)

  def test_invalid_n(self):
    with self.assertRaises(ValueError):
      get_nth_regex_match(_SAMPLE_TEXT, _REGEX_WORD, 0, SearchDirection.FORWARD)
    with self.assertRaises(ValueError):
      get_nth_regex_match(_SAMPLE_TEXT, _REGEX_WORD, -1, SearchDirection.FORWARD)


class GetNthSubstringMatchTestCase(unittest.TestCase):
  """Tests for getting the nth match of a substring."""

  def test_first_comma_forward(self):
    match = get_nth_substring_match(_SAMPLE_TEXT, ",", 1, SearchDirection.FORWARD)
    assert match is not None
    self.assertEqual(match.span(), (26, 27))
    self.assertEqual(match.group(), ",")

  def test_second_comma_forward(self):
    match = get_nth_substring_match(_SAMPLE_TEXT, ",", 2, SearchDirection.FORWARD)
    assert match is not None
    self.assertEqual(match.span(), (55, 56))
    self.assertEqual(match.group(), ",")

  def test_first_comma_backward(self):
    match = get_nth_substring_match(_SAMPLE_TEXT, ",", 1, SearchDirection.BACKWARD)
    assert match is not None
    self.assertEqual(match.span(), (147, 148))
    self.assertEqual(match.group(), ",")

  def test_second_comma_backward(self):
    match = get_nth_substring_match(_SAMPLE_TEXT, ",", 2, SearchDirection.BACKWARD)
    assert match is not None
    self.assertEqual(match.span(), (55, 56))
    self.assertEqual(match.group(), ",")

  def test_case_insensitive(self):
    match = get_nth_substring_match(_SAMPLE_TEXT, "lorem", 1, SearchDirection.BACKWARD)
    assert match is not None
    self.assertEqual(match.span(), (0, 5))
    self.assertEqual(match.group(), "Lorem")

  def test_empty_string(self):
    match = get_nth_substring_match("", ",", 1, SearchDirection.FORWARD)
    self.assertTrue(match is None)

  def test_search_past_end(self):
    match = get_nth_substring_match(_SAMPLE_TEXT, ",", 1000, SearchDirection.FORWARD)
    self.assertTrue(match is None)

  def test_invalid_n(self):
    with self.assertRaises(ValueError):
      get_nth_substring_match(_SAMPLE_TEXT, ",", 0, SearchDirection.FORWARD)
    with self.assertRaises(ValueError):
      get_nth_substring_match(_SAMPLE_TEXT, ",", -1, SearchDirection.FORWARD)


class GetPhraseRegexTestCase(unittest.TestCase):
  """Tests for getting a regex to match a phrase."""

  def test_get_phrase_regex(self):
    sep = r"[ .,\-\_\"]*"
    self.assertEqual(get_phrase_regex([], _get_homophones_mock), "")
    # Note: No parens in regex when a word has no homophones.
    self.assertEqual(get_phrase_regex(["a"], _get_homophones_mock), "a")
    self.assertEqual(get_phrase_regex("a b".split(" "), _get_homophones_mock), f"a{sep}b")  # type: ignore
    self.assertEqual(
        get_phrase_regex("we are there".split(" "), _get_homophones_mock),  # type: ignore
        f"we{sep}are{sep}(there|their|they're)")


class MatchNthWordStartSubstringTestCase(unittest.TestCase):
  """Tests for matching a substring to the beginning of a word."""

  def test_empty_string(self):
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "", 1, SearchDirection.FORWARD), None)
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "", 1, SearchDirection.BACKWARD), None)
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "", 2, SearchDirection.FORWARD), None)
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "", 2, SearchDirection.BACKWARD), None)

  def test_first_word_forward(self):
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "p", 1, SearchDirection.FORWARD), make_text_match(0, 1))
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "pat", 1, SearchDirection.FORWARD), make_text_match(0, 3))

  def test_second_match_forward(self):
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "p", 2, SearchDirection.FORWARD), make_text_match(25, 26))
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "pat", 2, SearchDirection.FORWARD), make_text_match(95, 98))

  def test_second_word_forward(self):
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "f", 1, SearchDirection.FORWARD), make_text_match(8, 9))
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "find", 1, SearchDirection.FORWARD), make_text_match(8, 12))

  def test_first_word_backward(self):
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "m", 1, SearchDirection.BACKWARD),
                     make_text_match(191, 192))
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "mat", 1, SearchDirection.BACKWARD),
                     make_text_match(191, 194))

  def test_second_match_backward(self):
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "m", 2, SearchDirection.BACKWARD),
                     make_text_match(131, 132))
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "mat", 2, SearchDirection.BACKWARD),
                     make_text_match(131, 134))

  def test_second_word_backward(self):
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "e", 1, SearchDirection.BACKWARD),
                     make_text_match(184, 185))
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "ent", 1, SearchDirection.BACKWARD),
                     make_text_match(184, 187))

  def test_no_match_not_word_start(self):
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "attern", 1, SearchDirection.FORWARD), None)
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "earch", 1, SearchDirection.BACKWARD), None)
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, "attern", 2, SearchDirection.FORWARD), None)
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "earch", 2, SearchDirection.BACKWARD), None)

  def test_non_starting_then_starting_substring(self):
    # Match non-starting substring of an earlier word that starts a later word (searching backwards).
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "re", 1, SearchDirection.BACKWARD), make_text_match(35, 37))

  def test_starting_with_symbol(self):
    self.assertEqual(get_nth_word_start_match(_TEXT_AFTER, ", end", 1, SearchDirection.FORWARD),
                     make_text_match(29, 34))
    self.assertEqual(get_nth_word_start_match(_TEXT_BEFORE, "[group", 1, SearchDirection.BACKWARD),
                     make_text_match(11, 17))

  def test_fragments_are_not_words(self):
    text = "combo type to [m.textflow_target_combo_type]"
    self.assertEqual(get_nth_word_start_match(text, "ty", 1, SearchDirection.BACKWARD), make_text_match(6, 8))

  def test_symbol_search_ignores_word_starts(self):
    # First ] should be matched, not the second one.
    text = "combo]]"
    self.assertEqual(get_nth_word_start_match(text, "]", 1, SearchDirection.FORWARD), make_text_match(5, 6))

  def test_space_search_ignores_word_starts(self):
    # First space should be matched, not the doubled space.
    text = "This is a  test."
    self.assertEqual(get_nth_word_start_match(text, " ", 1, SearchDirection.FORWARD), make_text_match(4, 5))

  def test_underscore_search_respects_word_starts(self):
    # First ] should be matched, not the second one.
    text = "first_second _something"
    self.assertEqual(get_nth_word_start_match(text, "_s", 1, SearchDirection.FORWARD), make_text_match(13, 15))


class MatchNthLineStartSubstringTestCase(unittest.TestCase):
  """Tests for matching a substring to the beginning of a line."""

  def test_empty_string(self):
    self.assertEqual(get_nth_line_start_match(_TEXT_AFTER, "", 1, SearchDirection.FORWARD), None)
    self.assertEqual(get_nth_line_start_match(_TEXT_BEFORE, "", 1, SearchDirection.BACKWARD), None)
    self.assertEqual(get_nth_line_start_match(_TEXT_AFTER, "", 2, SearchDirection.FORWARD), None)
    self.assertEqual(get_nth_line_start_match(_TEXT_BEFORE, "", 2, SearchDirection.BACKWARD), None)

  def test_first_line_forward(self):
    self.assertEqual(get_nth_line_start_match(_TEXT_AFTER, "p", 1, SearchDirection.FORWARD), make_text_match(0, 1))
    self.assertEqual(get_nth_line_start_match(_TEXT_AFTER, "pat", 1, SearchDirection.FORWARD), make_text_match(0, 3))

  def test_second_line_forward(self):
    self.assertEqual(get_nth_line_start_match(_TEXT_AFTER, "s", 1, SearchDirection.FORWARD), make_text_match(41, 42))
    self.assertEqual(get_nth_line_start_match(_TEXT_AFTER, "sim", 1, SearchDirection.FORWARD), make_text_match(41, 44))

  def test_first_line_backward(self):
    self.assertEqual(get_nth_line_start_match(_TEXT_BEFORE, "t", 1, SearchDirection.BACKWARD),
                     make_text_match(138, 139))
    self.assertEqual(get_nth_line_start_match(_TEXT_BEFORE, "this", 1, SearchDirection.BACKWARD),
                     make_text_match(138, 142))

  def test_second_line_backward(self):
    self.assertEqual(get_nth_line_start_match(_TEXT_BEFORE, "f", 1, SearchDirection.BACKWARD), make_text_match(20, 21))
    self.assertEqual(get_nth_line_start_match(_TEXT_BEFORE, "for", 1, SearchDirection.BACKWARD),
                     make_text_match(20, 23))

  def test_no_match_not_line_start(self):
    self.assertEqual(get_nth_line_start_match(_TEXT_AFTER, "a", 1, SearchDirection.FORWARD), None)
    self.assertEqual(get_nth_line_start_match(_TEXT_AFTER, "attern", 1, SearchDirection.FORWARD), None)
    self.assertEqual(get_nth_line_start_match(_TEXT_BEFORE, "h", 1, SearchDirection.BACKWARD), None)
    self.assertEqual(get_nth_line_start_match(_TEXT_BEFORE, "his", 1, SearchDirection.BACKWARD), None)
    self.assertEqual(get_nth_line_start_match(_TEXT_AFTER, "attern", 2, SearchDirection.FORWARD), None)
    self.assertEqual(get_nth_line_start_match(_TEXT_BEFORE, "his", 2, SearchDirection.BACKWARD), None)

  def test_indented_lines(self):
    self.assertEqual(get_nth_line_start_match(_SIMILAR_LINES, "in", 1, SearchDirection.FORWARD), make_text_match(2, 4))
    self.assertEqual(get_nth_line_start_match(_SIMILAR_LINES, "in", 2, SearchDirection.FORWARD),
                     make_text_match(35, 37))


class ExpandMatchToTokenTestCase(unittest.TestCase):
  """Tests for expanding a partial match to a full token."""

  def test_first_token(self):
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(0, 0)), make_text_match(0, 12))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(0, 1)), make_text_match(0, 12))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(0, 12)), make_text_match(0, 12))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(1, 11)), make_text_match(0, 12))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(9, 10)), make_text_match(0, 12))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(12, 12)), make_text_match(0, 12))

  def test_snake_case(self):
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(13, 13)), make_text_match(13, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(13, 14)), make_text_match(13, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(14, 14)), make_text_match(13, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(14, 26)), make_text_match(13, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(14, 27)), make_text_match(13, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(27, 27)), make_text_match(13, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(19, 22)), make_text_match(13, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(18, 21)), make_text_match(13, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(18, 19)), make_text_match(13, 27))

  def test_camel_case(self):
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(28, 28)), make_text_match(28, 40))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(28, 29)), make_text_match(28, 40))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(29, 29)), make_text_match(28, 40))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(29, 39)), make_text_match(28, 40))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(29, 40)), make_text_match(28, 40))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(40, 40)), make_text_match(28, 40))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(33, 37)), make_text_match(28, 40))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(32, 36)), make_text_match(28, 40))

  def test_kebab_case(self):
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(41, 41)), make_text_match(41, 54))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(41, 42)), make_text_match(41, 54))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(42, 42)), make_text_match(41, 54))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(42, 53)), make_text_match(41, 54))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(42, 54)), make_text_match(41, 54))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(41, 54)), make_text_match(41, 54))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(47, 50)), make_text_match(41, 54))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(46, 49)), make_text_match(41, 54))

  def test_dot_separated(self):
    # Note: Dots are not treated as separator characters. Each dot-separated component is its own token.
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(55, 58)), make_text_match(55, 58))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(55, 55)), make_text_match(55, 58))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(55, 56)), make_text_match(55, 58))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(56, 56)), make_text_match(55, 58))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(58, 58)), make_text_match(55, 58))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(59, 62)), make_text_match(59, 62))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(59, 59)), make_text_match(59, 62))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(62, 62)), make_text_match(59, 62))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(63, 67)), make_text_match(63, 67))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(63, 63)), make_text_match(63, 67))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(63, 64)), make_text_match(63, 67))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(67, 67)), make_text_match(63, 67))

  def test_pascal_case(self):
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(72, 91)), make_text_match(72, 91))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(72, 72)), make_text_match(72, 91))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(72, 73)), make_text_match(72, 91))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(91, 91)), make_text_match(72, 91))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(78, 81)), make_text_match(72, 91))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(81, 83)), make_text_match(72, 91))

  def test_spanning_multiple_tokens(self):
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(1, 20)), make_text_match(0, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(0, 27)), make_text_match(0, 27))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(1, 92)), make_text_match(0, 92))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(0, 92)), make_text_match(0, 92))

  def test_non_separator_symbol(self):
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(68, 68)), make_text_match(68, 68))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(68, 69)), make_text_match(68, 69))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(67, 69)), make_text_match(67, 69))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(67, 70)), make_text_match(67, 70))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(68, 70)), make_text_match(68, 70))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(69, 70)), make_text_match(69, 70))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(91, 92)), make_text_match(91, 92))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(92, 92)), make_text_match(92, 92))
    # Matching a non-separator symbol (space, dot) between tokens. Should not expand to adjacent tokens.
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(12, 13)), make_text_match(12, 13))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(58, 59)), make_text_match(58, 59))

  def test_separator_symbol(self):
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(70, 70)), make_text_match(70, 71))
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(70, 71)), make_text_match(70, 71))

  def test_apostrophe(self):
    self.assertEqual(expand_match_to_token(_FORMATTED_TOKENS, make_text_match(93, 95)), make_text_match(93, 98))

  def test_invalid_range(self):
    with self.assertRaises(ValueError):
      expand_match_to_token(_FORMATTED_TOKENS, make_text_match(10, 5))
    with self.assertRaises(ValueError):
      expand_match_to_token(_FORMATTED_TOKENS, make_text_match(0, -1))
    with self.assertRaises(ValueError):
      expand_match_to_token(_FORMATTED_TOKENS, make_text_match(-5, -1))
    with self.assertRaises(ValueError):
      expand_match_to_token(_FORMATTED_TOKENS, make_text_match(1, 200))
    with self.assertRaises(ValueError):
      expand_match_to_token("", make_text_match(0, 1))


class MaybeAddDeletionRangeTestCase(unittest.TestCase):
  """Tests for adding a deletion range to a match."""

  def test_first_word(self):
    text = "apples, oranges, bananas"
    match = make_text_match(0, 6)
    match = maybe_add_deletion_range(text, match)
    assert (match.deletion_range is not None)
    self.assertEqual(match.deletion_range.start, 0)
    self.assertEqual(match.deletion_range.end, 8)

  def test_middle_word(self):
    text = "apples, oranges bananas"
    match = make_text_match(8, 15)
    match = maybe_add_deletion_range(text, match)
    assert (match.deletion_range is not None)
    self.assertEqual(match.deletion_range.start, 8)
    self.assertEqual(match.deletion_range.end, 16)

  def test_end(self):
    text = "apples, oranges bananas"
    match = make_text_match(16, 23)
    match = maybe_add_deletion_range(text, match)
    self.assertIsNone(match.deletion_range)

  def test_no_deletion_range(self):
    text = "apples-oranges bananas"
    match = make_text_match(0, 6)
    match = maybe_add_deletion_range(text, match)
    self.assertIsNone(match.deletion_range)


class MatchTokenTestCase(unittest.TestCase):
  """Tests for matching a token."""

  def _token(self, text: str, options: TokenMatchOptions, direction: SearchDirection) -> Optional[str]:
    """Helper method for getting the text of a matched token. Returns None for no match."""
    match = match_token(text, options, direction, _get_homophones_mock)
    if match is None:
      return None
    return match.text_range.extract(text)

  def test_empty_string(self):
    # Empty string matches first position (cursor position).
    self.assertEqual(match_token(_TEXT_BEFORE, TokenMatchOptions(), SearchDirection.BACKWARD, _get_homophones_mock),
                     make_text_match(len(_TEXT_BEFORE), len(_TEXT_BEFORE)))
    self.assertEqual(match_token(_TEXT_AFTER, TokenMatchOptions(), SearchDirection.FORWARD, _get_homophones_mock),
                     make_text_match(0, 7))

  def test_first_token_forward(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.TOKEN_COUNT, nth_match=1)
    self.assertEqual(match_token(_TEXT_AFTER, options, SearchDirection.FORWARD, _get_homophones_mock),
                     make_text_match(0, 7))
    self.assertEqual(self._token(_TEXT_AFTER, options, SearchDirection.FORWARD), "Pattern")

  def test_second_token_forward(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.TOKEN_COUNT, nth_match=2)
    self.assertEqual(match_token(_TEXT_AFTER, options, SearchDirection.FORWARD, _get_homophones_mock),
                     make_text_match(8, 15))
    self.assertEqual(self._token(_TEXT_AFTER, options, SearchDirection.FORWARD), "findall")

  def test_first_token_backward(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.TOKEN_COUNT, nth_match=1)
    self.assertEqual(match_token(_TEXT_BEFORE, options, SearchDirection.BACKWARD, _get_homophones_mock),
                     make_text_match(191, 196))
    self.assertEqual(self._token(_TEXT_BEFORE, options, SearchDirection.BACKWARD), "match")

  def test_second_token_backward(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.TOKEN_COUNT, nth_match=2)
    result = match_token(_TEXT_BEFORE, options, SearchDirection.BACKWARD, _get_homophones_mock)
    assert (result is not None)
    self.assertEqual(result.text_range, make_text_match(184, 190).text_range)
    self.assertEqual(self._token(_TEXT_BEFORE, options, SearchDirection.BACKWARD), "entire")

  def test_token_count_no_match(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.TOKEN_COUNT, nth_match=2000)
    self.assertEqual(self._token(_TEXT_AFTER, options, SearchDirection.FORWARD), None)
    self.assertEqual(self._token(_TEXT_BEFORE, options, SearchDirection.BACKWARD), None)

  def test_word_start(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_START, search="do", nth_match=1)
    self.assertEqual(self._token(_SAMPLE_TEXT, options, SearchDirection.FORWARD), "dolor")
    options.nth_match = 2
    self.assertEqual(self._token(_SAMPLE_TEXT, options, SearchDirection.FORWARD), "do")
    options.nth_match = 3
    self.assertEqual(self._token(_SAMPLE_TEXT, options, SearchDirection.FORWARD), "dolore")

  def test_word_start_no_match(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_START, search="xyz")
    self.assertEqual(self._token(_TEXT_AFTER, options, SearchDirection.FORWARD), None)
    self.assertEqual(self._token(_TEXT_BEFORE, options, SearchDirection.BACKWARD), None)

  def test_word_start_then_substring_no_match(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_START_THEN_SUBSTRING, search="xyz")
    self.assertEqual(self._token(_TEXT_AFTER, options, SearchDirection.FORWARD), None)
    self.assertEqual(self._token(_TEXT_BEFORE, options, SearchDirection.BACKWARD), None)

  def test_word_substring(self):
    text = "redo_snake done-kebab"
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_SUBSTRING, search="do", nth_match=1)
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), "redo_snake")
    options.nth_match = 2
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), "done-kebab")

  def test_word_substring_no_match(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_SUBSTRING, search="xyz")
    self.assertEqual(self._token(_TEXT_AFTER, options, SearchDirection.FORWARD), None)
    self.assertEqual(self._token(_TEXT_BEFORE, options, SearchDirection.BACKWARD), None)

  def test_exact_word(self):
    text = "aa a aaa"
    options = TokenMatchOptions(match_method=TokenMatchMethod.EXACT_WORD, search="a", nth_match=1)
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), "a")
    options.search = "aa"
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), "aa")

  def test_exact_word_no_match(self):
    text = "aa aaa"
    options = TokenMatchOptions(match_method=TokenMatchMethod.EXACT_WORD, search="a", nth_match=1)
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), None)

  def test_line_start(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.LINE_START, search="in", nth_match=1)
    self.assertEqual(self._token(_SIMILAR_LINES, options, SearchDirection.FORWARD), "Indented")
    options.nth_match = 2
    self.assertEqual(self._token(_SIMILAR_LINES, options, SearchDirection.FORWARD), "Indented")
    options.nth_match = 1
    options.search = "un"
    self.assertEqual(self._token(_SIMILAR_LINES, options, SearchDirection.FORWARD), "Unindented")

  def test_line_start_no_match(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.LINE_START, search="xyz")
    self.assertEqual(self._token(_TEXT_AFTER, options, SearchDirection.FORWARD), None)
    self.assertEqual(self._token(_TEXT_BEFORE, options, SearchDirection.BACKWARD), None)

  def test_phrase(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.PHRASE, search="var name", nth_match=1)
    self.assertEqual(self._token(_FORMATTED_TOKENS, options, SearchDirection.FORWARD), "snake_var_name")

  def test_phrase_case_mismatch(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.PHRASE, search="VAR NAME", nth_match=1)
    self.assertEqual(self._token(_FORMATTED_TOKENS, options, SearchDirection.FORWARD), "snake_var_name")

  def test_phrase_matches_partial_words(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.PHRASE, search="ar nam", nth_match=1)
    self.assertEqual(self._token(_FORMATTED_TOKENS, options, SearchDirection.FORWARD), "snake_var_name")

  def test_phrase_homophones(self):
    text = "find their dog"
    options = TokenMatchOptions(match_method=TokenMatchMethod.PHRASE, search="there dog", nth_match=1)
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), "their dog")

  def test_phrase_homophones_beginning(self):
    text = "find their dog"
    options = TokenMatchOptions(match_method=TokenMatchMethod.PHRASE, search="find there", nth_match=1)
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), "find their")

  def test_phrase_no_match(self):
    options = TokenMatchOptions(match_method=TokenMatchMethod.PHRASE, search="xyz")
    self.assertEqual(self._token(_TEXT_AFTER, options, SearchDirection.FORWARD), None)
    self.assertEqual(self._token(_TEXT_BEFORE, options, SearchDirection.BACKWARD), None)

  def test_word_start_takes_precedence(self):
    # "return" occurs after "entire" while searching backwards.
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_START_THEN_SUBSTRING, search="re")
    self.assertEqual(self._token(_TEXT_BEFORE, options, SearchDirection.BACKWARD), "return")

  def test_word_start_does_not_match_inside_snake(self):
    # Word start should match a component of a snake-case token.
    text = "ninth two_three_four five"
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_START, search="th")
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), None)

  def test_word_start_does_not_match_inside_camel(self):
    # We may want to change this behavior: Word start does not currently match inside of camel/pascal case tokens.
    text = "ninth twoThreeFour five"
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_START, search="th")
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), None)

  def test_substring_after_word_start(self):
    # "commodo" occurs after three words starting with "do" while searching forward.
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_START_THEN_SUBSTRING, search="do", nth_match=4)
    self.assertEqual(self._token(_SAMPLE_TEXT, options, SearchDirection.FORWARD), "commodo")

  def test_substring_interspersed_with_word_start(self):
    # Note: This may be confusing behavior. Word start match is performed first. If words with substring matches are
    # interspersed, they are skipped over in the first match attempt.
    text = "door redo done donut"
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_START_THEN_SUBSTRING, search="do", nth_match=2)
    self.assertEqual(self._token(text, options, SearchDirection.FORWARD), "done")

  def test_word_start_takes_precedence_over_fragment_start(self):
    # "type" occurs after "textflow_target_combo_type" while searching backwards.
    text = "combo type to [m.textflow_target_combo_type]"
    options = TokenMatchOptions(match_method=TokenMatchMethod.WORD_START_THEN_SUBSTRING, search="ty")
    self.assertEqual(self._token(text, options, SearchDirection.BACKWARD), "type")
