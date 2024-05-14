"""Library for helping with browser-related tasks."""

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

# Delimiters for dumping tab information via AppleScript.
TAB_DELIMITER = "|||"
WINDOW_DELIMITER = "^^^"


@dataclass
class Tab:
  """An open browser tab."""
  # Index of the window containing the tab.
  window_index: int = 0  # 1-based index.

  # Index of the tab within the window.
  index: int = 0  # 1-based index.

  # Whether the tab is active within its window. True for one tab per window.
  # Note: If the browser has focus, then the focused tab is the active tab of window index 1
  active: bool = False

  # The title of the tab.
  title: str = ""

  # The Url of the tab.
  url: str = ""


def parse_tab_list_string(tab_list_string: str) -> list[Tab]:
  """Parses the output of a tab list AppleScript call."""
  if not tab_list_string:
    raise ValueError("Empty tab list string.")

  result: list[Tab] = []
  input_string: str = tab_list_string

  # Remove leading window delimiter if present.
  if input_string.startswith(WINDOW_DELIMITER):
    input_string = input_string[len(WINDOW_DELIMITER):]

  # Split the string into window sections.
  window_parts = input_string.split(WINDOW_DELIMITER)
  if len(window_parts) % 2 != 0:
    raise ValueError("Unexpected number of window strings.")

  # Parse each window's tabs.
  for i in range(0, len(window_parts), 2):
    window_index_parts = window_parts[i].split(",")
    if len(window_index_parts) != 2:
      raise ValueError("Unexpected number of window index parts.")
    window_index = int(window_index_parts[0])
    active_tab_index = int(window_index_parts[1])

    # Move to next window if there are no tabs.
    if not window_parts[i + 1]:
      continue

    # Remove trailing tab delimiter if present.
    tabs_string = window_parts[i + 1]
    if tabs_string.endswith(TAB_DELIMITER):
      tabs_string = tabs_string[:-len(TAB_DELIMITER)]

    # Split tab strings for the window.
    tab_parts = tabs_string.split(TAB_DELIMITER)
    if len(tab_parts) % 2 != 0:
      raise ValueError("Unexpected number of tab strings.")

    # Parse each tab.
    for j in range(0, len(tab_parts), 2):
      tab_index = (j // 2) + 1
      result.append(
          Tab(window_index=window_index,
              index=tab_index,
              active=active_tab_index == tab_index,
              title=tab_parts[j + 1],
              url=tab_parts[j]))

  return result


def get_tabs_matching_hostname(tabs: list[Tab], hostname: str) -> list[Tab]:
  """Returns a list of tabs with URLs matching the given hostname."""
  result: list[Tab] = []
  for tab in tabs:
    url = urlparse(tab.url)

    # Check if the tab's URL matches the hostname (case insensitive).
    if url.hostname and url.hostname.lower() == hostname.lower():
      result.append(tab)
  return result


def get_focused_tab_list_index(tabs: list[Tab]) -> Optional[int]:
  """Returns the index in the list of the  active tab for window index 1. None if such a tab is not present."""
  for i, tab in enumerate(tabs):
    if tab.active and tab.window_index == 1:
      return i
  return None
