"""Utilities for working with URLs."""

from urllib.parse import parse_qs, urlparse


def get_query_string_value(url: str, key: str) -> str:
  """Get the value of a parameter in the query string of the given URL. If the parameter occurs more than once, returns
  the last set value. Throws ValueError if the value was not found."""
  parsed_url = urlparse(url)
  parsed_query_string = parse_qs(parsed_url.query)
  if not key in parsed_query_string:
    raise ValueError(f"Query param not found: {key}")
  return parsed_query_string[key][-1]
