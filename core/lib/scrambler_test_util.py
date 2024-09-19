"""Utility functions for Scrambler tests."""

from typing import Optional
from .scrambler_types import UtilityFunctions


def _get_homophones_mock(word: str) -> list[str]:
  """Mock function for getting homophones."""
  sample_phones = ["there", "their", "they're", "dolor"]
  if word in sample_phones:
    return sample_phones
  return [word]


def _get_next_homophone_mock(word: str) -> Optional[str]:
  """Mock function for getting homophones."""
  words = _get_homophones_mock(word)
  for phone in words:
    if phone == word:
      continue
    return phone
  return None


UTILITY_FUNCTIONS = UtilityFunctions(_get_homophones_mock, _get_next_homophone_mock)
