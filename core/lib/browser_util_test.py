"""Tests for browser utils."""

import unittest
from .browser_util import *  # pylint: disable=wildcard-import, unused-wildcard-import

# Short aliases for delimiters.
TD = TAB_DELIMITER
WD = WINDOW_DELIMITER


# Fake window type.
@dataclass
class Window:
  id: int
  title: str


class ParseTabListTestCase(unittest.TestCase):
  """Test for parsing tab list."""

  def test_empty_string(self):
    with self.assertRaises(ValueError):
      parse_tab_list_string("")

  def test_one_window_no_tabs(self):
    result = parse_tab_list_string(f"{WD}1,0{WD}")
    self.assertEqual(len(result), 0)

  def test_one_window_one_tab(self):
    result = parse_tab_list_string(f"{WD}1,1{WD}url{TD}title{TD}")
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0].window_index, 1)
    self.assertEqual(result[0].index, 1)
    self.assertTrue(result[0].active)
    self.assertEqual(result[0].title, "title")
    self.assertEqual(result[0].url, "url")

  def test_one_window_multiple_tabs(self):
    result = parse_tab_list_string(f"{WD}1,2{WD}url1{TD}title1{TD}url2{TD}title2{TD}")
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0].window_index, 1)
    self.assertEqual(result[0].index, 1)
    self.assertFalse(result[0].active)
    self.assertEqual(result[0].title, "title1")
    self.assertEqual(result[0].url, "url1")
    self.assertEqual(result[1].window_index, 1)
    self.assertEqual(result[1].index, 2)
    self.assertTrue(result[1].active)
    self.assertEqual(result[1].title, "title2")
    self.assertEqual(result[1].url, "url2")

  def test_multiple_windows_multiple_tabs(self):
    result = parse_tab_list_string(
        f"{WD}1,2{WD}url1{TD}title1{TD}url2{TD}title2{TD}{WD}2,1{WD}url3{TD}title3{TD}url4{TD}title4{TD}")
    self.assertEqual(len(result), 4)
    self.assertEqual(result[0].window_index, 1)
    self.assertEqual(result[0].index, 1)
    self.assertFalse(result[0].active)
    self.assertEqual(result[0].title, "title1")
    self.assertEqual(result[0].url, "url1")

    self.assertEqual(result[1].window_index, 1)
    self.assertEqual(result[1].index, 2)
    self.assertTrue(result[1].active)
    self.assertEqual(result[1].title, "title2")
    self.assertEqual(result[1].url, "url2")

    self.assertEqual(result[2].window_index, 2)
    self.assertEqual(result[2].index, 1)
    self.assertTrue(result[2].active)
    self.assertEqual(result[2].title, "title3")
    self.assertEqual(result[2].url, "url3")

    self.assertEqual(result[3].window_index, 2)
    self.assertEqual(result[3].index, 2)
    self.assertFalse(result[3].active)
    self.assertEqual(result[3].title, "title4")
    self.assertEqual(result[3].url, "url4")

  def test_invalid_window(self):
    with self.assertRaises(ValueError):
      parse_tab_list_string(f"{WD}1,1url{TD}title{TD}")

  def test_missing_active_tab(self):
    with self.assertRaises(ValueError):
      parse_tab_list_string(f"{WD}1{WD}url{TD}title{TD}")

  def test_invalid_tab(self):
    with self.assertRaises(ValueError):
      parse_tab_list_string(f"{WD}1,1{WD}urltitle{TD}")


class GetTabsMatchingHostnameTestCase(unittest.TestCase):
  """Test for getting all tabs that match a given hostname."""

  def setUp(self):
    self.tabs = [
        Tab(1, 1, True, "title1", "http://host.example.com"),
        Tab(1, 2, False, "title2", "http://url2"),
        Tab(2, 1, False, "title3", "http://url3"),
        Tab(2, 2, True, "title4", "http://host.example.com/url4"),
        Tab(2, 3, False, "title5", "http://host.url.example.net/url5")
    ]

  def test_empty_string(self):
    self.assertEqual(get_tabs_matching_hostname(self.tabs, ""), [])

  def test_hostname(self):
    result = get_tabs_matching_hostname(self.tabs, "host.example.com")
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0].index, 1)
    self.assertEqual(result[0].title, "title1")
    self.assertEqual(result[0].url, "http://host.example.com")
    self.assertEqual(result[1].index, 2)
    self.assertEqual(result[1].title, "title4")
    self.assertEqual(result[1].url, "http://host.example.com/url4")

  def test_single_word(self):
    # Not a valid hostname.
    self.assertEqual(get_tabs_matching_hostname(self.tabs, "http://url3"), [])

  def test_partial_match(self):
    result = get_tabs_matching_hostname(self.tabs, "example.com")
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0].index, 1)
    self.assertEqual(result[0].title, "title1")
    self.assertEqual(result[0].url, "http://host.example.com")
    self.assertEqual(result[1].index, 2)
    self.assertEqual(result[1].title, "title4")
    self.assertEqual(result[1].url, "http://host.example.com/url4")

  def test_prefix_first(self):
    result = get_tabs_matching_hostname(self.tabs, "url")
    # Results use prefix first and don't match http://host.url.example.net/url5
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0].index, 2)
    self.assertEqual(result[0].title, "title2")
    self.assertEqual(result[0].url, "http://url2")
    self.assertEqual(result[1].index, 1)
    self.assertEqual(result[1].title, "title3")
    self.assertEqual(result[1].url, "http://url3")

    result = get_tabs_matching_hostname(self.tabs, "url.example")
    # Results use substring and match http://host.url.example.net/url5
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0].index, 3)
    self.assertEqual(result[0].title, "title5")
    self.assertEqual(result[0].url, "http://host.url.example.net/url5")


class GetFocusedTabListIndexTestCase(unittest.TestCase):
  """Test for getting the list index of the focused tab."""

  def setUp(self):
    self.tabs = [
        Tab(1, 1, False, "title1", "http://host.example.com"),
        Tab(1, 2, False, "title2", "url2"),
        Tab(1, 3, True, "title3", "url3"),  # Focused (active in window 1).
        Tab(2, 1, False, "title4", "url4"),
        Tab(2, 2, True, "title5", "http://host.example.com/url5")
    ]

  def test_empty_list(self):
    self.assertEqual(get_focused_tab_list_index([]), None)

  def test_get_index(self):
    self.assertEqual(get_focused_tab_list_index(self.tabs), 2)


class MatchWindowsTestCase(unittest.TestCase):
  """Test for browser utility."""

  def setUp(self):
    self.tabs = [
        Tab(1, 1, False, "title1", "http://host.example.com"),
        Tab(1, 2, False, "title2", "url2"),
        Tab(1, 3, True, "title3", "url3"),  # Focused (active in window 1).
        Tab(2, 1, False, "title4", "url4"),
        Tab(2, 2, True, "title5", "http://host.example.com/url5"),
        Tab(3, 1, False, "title4", "url4"),
        Tab(3, 2, True, "title5", "http://host.example.com/url5"),
        Tab(4, 1, True, "", "no_url"),
    ]
    self.windows = [
        Window(1, ""),
        Window(2, "title3 - Browser (Work)"),
        Window(3, ""),
        Window(4, "title^^^5 - Browser (Personal)"),  # Include a delimiter in the title.
        Window(5, "title5 - Browser (Work)"),
        Window(6, ""),
    ]

  def test_empty_list(self):
    self.assertEqual(match_windows([], []), BrowserContext([], []))

  def test_no_windows(self):
    self.assertEqual(match_windows(self.tabs, []), BrowserContext(self.tabs, [None] * 4))

  def test_match_windows(self):
    expected = BrowserContext(self.tabs, [2, 4, 5, None])
    self.assertEqual(match_windows(self.tabs, self.windows), expected)
