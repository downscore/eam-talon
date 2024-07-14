"""Utilities for working with URLs."""

import re
from urllib.parse import parse_qs, urlparse


def get_query_string_value(url: str, key: str) -> str:
  """Get the value of a parameter in the query string of the given URL. If the parameter occurs more
  than once, returns the last set value. Throws ValueError if the value was not found."""
  parsed_url = urlparse(url)
  parsed_query_string = parse_qs(parsed_url.query)
  if not key in parsed_query_string:
    raise ValueError(f"Query param not found: {key}")
  return parsed_query_string[key][-1]


def extract_url(text):
  # Regular expression to match markdown URLs (surrounded by parentheses).
  markdown_url_pattern = r'\((https?://[^\s]+)\)'

  # Search for markdown URL first
  markdown_url_match = re.search(markdown_url_pattern, text)
  if markdown_url_match:
    return markdown_url_match.group(1)

  # Regular expression to match URLs.
  url_pattern = r'(https?://[^\s]+)'

  # Search for plain URL
  url_match = re.search(url_pattern, text)
  if url_match:
    return url_match.group(1)

  # Regular expression to match short URLs like go/example or x/12345
  short_url_pattern = r'(\b[a-zA-Z]{1,2}/[^\s]+)'
  url_match = re.search(short_url_pattern, text)
  if url_match:
    short_url = url_match.group(1)
    # Remove trailing punctuation.
    short_url = re.sub(r'[.,!?]+$', '', short_url)
    return f"http://{short_url}"

  return None
