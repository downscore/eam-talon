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

    # Remove leading asterisk (indicating uncommon word) if present.
    if word.startswith("*"):
      word = word[1:]

    next_index = (i + 1) % len(homophones_set)
    next_word = homophones_set[next_index].strip()

    # Remove leading asterisk (indicating uncommon word) from next word if present.
    if next_word.startswith("*"):
      next_word = next_word[1:]

    result[word.strip().lower()] = next_word
  return result


def get_next_homophone_dict(homophones_sets: list[list[str]]) -> Dict[str, str]:
  """Given lists of homophones, get a dictionay mapping each word to its next homophone in the list (wrapping around at
  the end). Keys are all lowercase. Values have case preserved from input list. Both are stripped."""
  result = {}
  for homophones_set in homophones_sets:
    # Check for dupes.
    for word in homophones_set:
      # Remove leading asterisk (indicating uncommon word) if present.
      # TODO: Do not have entries pointing to uncommon words, but don't break getting full homophone sets.
      if word.startswith("*"):
        word = word[1:]

      if word.lower() in result:
        raise ValueError(f"Duplicate entry: {word}")
    result.update(get_next_homophone_dict_for_single_set(homophones_set))
  return result
