"""Talon code for dictating text. Common to both command and dicatation modes."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, grammar
from .lib import format_util
from .user_settings import load_dict_from_csv

mod = Module()
ctx = Context()

mod.list("vocabulary", desc="additional vocabulary words")

# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words Talon recognized. Entries in word_map
# don't change the priority with which Talon recognizes some words over others.
ctx.settings["dictate.word_map"] = load_dict_from_csv("words_to_replace.csv")

# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't recognize. Words in user.vocabulary (or
# other lists and captures) are "command-like" and their recognition is prioritized over ordinary words.
ctx.lists["user.vocabulary"] = load_dict_from_csv("additional_words.csv")


def _capture_to_words(m):
  words = []
  for item in m:
    if isinstance(item, grammar.vm.Phrase):
      words.extend(actions.dictate.replace_words(actions.dictate.parse_words(item)))
    else:
      words.extend(item.split(" "))
  return words


def _format_captured_text(m):
  words = _capture_to_words(m)
  result = ""
  for i, curr_word in enumerate(words):
    if i > 0 and format_util.needs_space_between(words[i - 1], curr_word):
      result += " "
    result += curr_word
  return result


@mod.capture(rule="({user.vocabulary} | <word>)")
def word(m) -> str:
  """A single word, including user-defined vocabulary."""
  try:
    return m.vocabulary
  except AttributeError:
    return " ".join(actions.dictate.replace_words(actions.dictate.parse_words(m.word)))


@mod.capture(rule="({user.vocabulary} | <phrase>)+")
def text(m) -> str:
  """A sequence of words, including user-defined vocabulary."""
  return _format_captured_text(m)


@mod.capture(rule="({user.punctuation} | <user.dictate_letters> | <user.dictate_number> | " +
             "<user.file_extension> | {user.vocabulary} | <phrase>)+")
def prose(m) -> str:
  """Mixed words and punctuation, auto-spaced and capitalized."""
  capitalized = format_util.auto_capitalize(_format_captured_text(m))
  return capitalized
