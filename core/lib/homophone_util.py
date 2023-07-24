"""Util functions for homophones."""

from typing import Dict


def get_next_homophone_dict_for_single_set(homophones_set: list[str]) -> Dict[str, str]:
  """Given a list of a single set of homophones, get a dictionary mapping each word to the next homophone in the list.
  Keys are all lowercase. Values have case preserved from input list. Both are stripped."""
  if (len(homophones_set)) < 2:
    raise ValueError("Homophones list must have at least 2 elements.")
  result: Dict[str, str] = {}
  for i, word in enumerate(homophones_set):
    if len(word) == 0:
      raise ValueError("Empty string in homophones list.")
    next_index = (i + 1) % len(homophones_set)
    result[word.strip().lower()] = homophones_set[next_index].strip()
  return result


def get_next_homophone_dict(homophones_sets: list[list[str]]) -> Dict[str, str]:
  """Given lists of homophones, get a dictionay mapping each word to its next homophone in the list (wrapping around at
  the end). Keys are all lowercase. Values have case preserved from input list. Both are stripped."""
  result = {}
  for homophones_set in homophones_sets:
    # Check for dupes.
    for word in homophones_set:
      if word.lower() in result:
        raise ValueError(f"Duplicate entry: {word}")
    result.update(get_next_homophone_dict_for_single_set(homophones_set))
  return result
