"""Util functions for homophones."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class HomophoneSet:
  """A set of homophones."""
  words_excluding_uncommon: list[str]
  uncommon_words: list[str]

  def get_next_word(self, word: str) -> str:
    """Get the next word for the given word."""
    for i, curr_word in enumerate(self.words_excluding_uncommon):
      if curr_word == word:
        next_index = (i + 1) % len(self.words_excluding_uncommon)
        return self.words_excluding_uncommon[next_index]

    if not word in self.uncommon_words:
      raise ValueError(f"Word not found in homophone set: {word}")

    # Word is uncommon, so just return the first word in the set.
    return self.words_excluding_uncommon[0]


def get_homophone_sets(homophones: list[list[str]]) -> list[HomophoneSet]:
  """Given a list of homophones, return a list of HomophoneSets."""
  result = []
  for homophones_set in homophones:
    if len(homophones_set) == 0:
      raise ValueError("Homophone set must contain at least one word")
    words_excluding_uncommon = []
    uncommon_words = []
    for word in homophones_set:
      # Uncommon words have an asterisk prepended.
      if word.startswith("*"):
        uncommon_words.append(word[1:])
      else:
        words_excluding_uncommon.append(word)
    result.append(HomophoneSet(words_excluding_uncommon, uncommon_words))
  return result


def get_homograph_homophone_sets(homophone_sets: list[list[str]]) -> dict[str, list[HomophoneSet]]:
  """Given a list of homophone sets, return HomophoneSets keyed by homograph."""
  result = {}
  for homophone_set in homophone_sets:
    if len(homophone_set) == 0:
      raise ValueError("Homophone set must contain at least one word")
    words_excluding_uncommon = []
    uncommon_words = []
    homograph = homophone_set[0]
    for word in homophone_set:
      # Uncommon words have an asterisk prepended.
      if word.startswith("*"):
        uncommon_words.append(word[1:])
      else:
        words_excluding_uncommon.append(word)
    if not homograph in result:
      result[homograph] = []
    result[homograph].append(HomophoneSet(words_excluding_uncommon, uncommon_words))
  return result


def get_word_to_homophone_set_dict(
    homophone_sets: list[HomophoneSet],
    homograph_homophone_sets: dict[str, list[HomophoneSet]]) -> Dict[str, HomophoneSet]:
  """Given a list of homophones, return a list of HomophoneSets."""
  result = {}
  for homophone_set in homophone_sets:
    for word in homophone_set.words_excluding_uncommon:
      result[word] = homophone_set
    for word in homophone_set.uncommon_words:
      result[word] = homophone_set

  for homograph, curr_sets in homograph_homophone_sets.items():
    if homograph in result:
      raise ValueError(f"Duplicate homograph found: {homograph}")

    # Make a new set for the homograph so we can combine sets.
    result[homograph] = HomophoneSet([], [])

    for homophone_set in curr_sets:
      # Merge all sets for the homograph.
      for word in homophone_set.words_excluding_uncommon:
        if word not in result[homograph].words_excluding_uncommon:
          result[homograph].words_excluding_uncommon.append(word)
      for word in homophone_set.uncommon_words:
        if word not in result[homograph].uncommon_words:
          result[homograph].uncommon_words.append(word)

      # Point non-homograph words to the set they appear in.
      for word in homophone_set.words_excluding_uncommon:
        if word != homograph:
          result[word] = homophone_set
      for word in homophone_set.uncommon_words:
        if word != homograph:
          result[word] = homophone_set

  return result
