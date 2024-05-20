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


def get_word_to_homophone_set_dict(homophone_sets: list[HomophoneSet]) -> Dict[str, HomophoneSet]:
  """Given a list of homophones, return a list of HomophoneSets."""
  result = {}
  for homophone_set in homophone_sets:
    for word in homophone_set.words_excluding_uncommon:
      result[word] = homophone_set
    for word in homophone_set.uncommon_words:
      result[word] = homophone_set
  return result
