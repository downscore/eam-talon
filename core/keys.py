"""Talon code for simulating keyboard input."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, Context

mod = Module()
ctx = Context()

_LETTERS = {
    "air": "a",
    "bill": "b",
    "cap": "c",
    "drum": "d",
    "each": "e",
    "fine": "f",
    "gust": "g",
    "harp": "h",
    "sit": "i",
    "jury": "j",
    "crunch": "k",
    "look": "l",
    "made": "m",
    "near": "n",
    "odd": "o",
    "prime": "p",
    "quench": "q",
    "red": "r",
    "sun": "s",
    "trap": "t",
    "urge": "u",
    "vest": "v",
    "whale": "w",
    "plex": "x",
    "yank": "y",
    "zip": "z",
}
mod.list("letter", desc="The spoken phonetic alphabet")
ctx.lists["self.letter"] = _LETTERS

# Spoken letter words.
mod.list("letter_spoken", desc="Words used in spoken phonetic alphabet. No mapping to letters.")
ctx.lists["self.letter_spoken"] = _LETTERS.keys()

# Create a list including all letters and capital letters with spoken forms preceded by "ship".
# TODO: Clean this up. We should be able to allow dictating capital letters without including them in a new list.
_LETTER_WITH_CAPITALS = _LETTERS.copy()
for spoken, written in _LETTERS.items():
  _LETTER_WITH_CAPITALS[f"ship {spoken}"] = written.upper()
mod.list("letter_with_capitals", desc="The spoken phonetic alphabet including capital letters")
ctx.lists["self.letter_with_capitals"] = _LETTER_WITH_CAPITALS

_DIGITS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
mod.list("number_key", desc="All number keys")
ctx.lists["self.number_key"] = _DIGITS

_FUNCTION_KEYS = {
    "function key one": "f1",
    "function key two": "f2",
    "function key three": "f3",
    "function key four": "f4",
    "function key five": "f5",
    "function key six": "f6",
    "function key seven": "f7",
    "function key eight": "f8",
    "function key nine": "f9",
    "function key ten": "f10",
    "function key eleven": "f11",
    "function key twelve": "f12",
    "function key thirteen": "f13",
    "function key fourteen": "f14",
    "function key fifteen": "f15",
    "function key sixteen": "f16",
    "function key seventeen": "f17",
    "function key eighteen": "f18",
    "function key nineteen": "f19",
    "function key twenty": "f20",
}
mod.list("function_key", desc="All function keys")
ctx.lists["self.function_key"] = _FUNCTION_KEYS

_MODIFIER_KEYS = {
    # "alt": "alt",  # Use option instead.
    "troll": "ctrl",
    "ship": "shift",
    # "super": "super",  # Use cmd instead.
    "many": "cmd",
    "option": "alt",
}
mod.list("modifier_key", desc="All modifier keys")
ctx.lists["self.modifier_key"] = _MODIFIER_KEYS

# Punctuation words are usable in prose formatters ("say", "title", etc.).
# Using "gram" to trigger symbols.
# The values are key names but need to be the actual symbols for use in prose.
_PUNCTUATION_WORDS = {
    # Commonly-used punctuation that can be used in prose.
    "punch": ".",
    "drip": ",",
    "trip": ",",  # Common misrecognition for "drip".
    "bang": "!",
    "bank": "!",  # Common misrecognition for "bang".
    "quest": "?",
    "dash": "-",
    "stack": ":",
    # Prefixed punctuation.
    "gram semi": ";",
    "gram pound": "#",
    "gram score": "_",
    "gram paren": "(",
    "gram round": "(",  # Alternative that works better in prose.
    "gram close paren": ")",
    "gram square": "[",
    "gram close square": "]",
    "gram brace": "{",
    "gram close brace": "}",
    "gram percent": "%",
    "gram amper": "&",
    "gram pipe": "|",
    "gram single": "'",
    "gram double": "\"",
    "gram stroke": "/",
    "gram backstroke": "\\",
    "gram at": "@",
    "gram dollar": "$",
    "gram caret": "^",
    "gram star": "*",
    "gram plus": "+",
    "gram equal": "=",
    "gram tilde": "~",
    "gram grave": "`",
    "gram less": "<",
    "gram more": ">",
    "gram sterling": "£",
    "gram euro": "€",
}
mod.list("punctuation", desc="Words for inserting punctuation into text")
ctx.lists["self.punctuation"] = _PUNCTUATION_WORDS

# Symbol keys are a superset of punctuation words, and are usable as commands, but not necessarily in prose.
_SYMBOL_KEYS = _PUNCTUATION_WORDS | {
    "semi": ";",
    "pound": "#",
    "score": "_",
    "paren": "(",
    "close paren": ")",
    "square": "[",
    "close square": "]",
    "brace": "{",
    "close brace": "}",
    "percent": "%",
    "amper": "&",
    "single": "'",
    "double": '"',
    "stroke": "/",
    "backstroke": "\\",
    "star": "*",
    "equal": "=",
}
mod.list("symbol_key", desc="All symbols from the keyboard")
ctx.lists["self.symbol_key"] = _SYMBOL_KEYS

_ARROW_KEYS = {
    "down": "down",
    "left": "left",
    "right": "right",
    "up": "up",
}
mod.list("arrow_key", desc="All arrow keys")
ctx.lists["self.arrow_key"] = _ARROW_KEYS

_SPECIAL_KEYS = {
    "enter": "enter",
    "scrape": "escape",
    "void": "space",
    "page up": "pageup",
    "page down": "pagedown",
    "tabber": "tab",
    "wiper": "backspace",
    "deli": "delete",
    "press insert": "insert",
    "press end": "end",
    "press home": "home",
}
mod.list("special_key", desc="All special keys")
ctx.lists["self.special_key"] = _SPECIAL_KEYS


@mod.capture(rule="{self.modifier_key}+")
def modifiers(m) -> str:
  "A single or more modifier keys."
  return "-".join(m.modifier_key_list)


@mod.capture(rule="{self.arrow_key}")
def arrow_key(m) -> str:
  "A single directional arrow key."
  return m.arrow_key


@mod.capture(rule="<self.arrow_key>+")
def arrow_keys(m) -> str:
  "One or more arrow keys separated by a space."
  return str(m)


@mod.capture(rule="{self.number_key}")
def number_key(m) -> str:
  "A single number key."
  return m.number_key


@mod.capture(rule="{self.letter}")
def letter(m) -> str:
  "A single letter key."
  return m.letter


@mod.capture(rule="{self.special_key}")
def special_key(m) -> str:
  "A single special key."
  return m.special_key


@mod.capture(rule="{self.symbol_key}")
def symbol_key(m) -> str:
  "A single symbol key."
  return m.symbol_key


@mod.capture(rule="{self.function_key}")
def function_key(m) -> str:
  "A single function key."
  return m.function_key


@mod.capture(rule="( <self.letter> | <self.number_key> | <self.symbol_key> "
             "| <self.arrow_key> | <self.function_key> | <self.special_key> )")
def unmodified_key(m) -> str:
  "A single key with no modifiers."
  return str(m)


@mod.capture(rule="{self.letter}+")
def letters(m) -> str:
  "Multiple letter keys."
  return "".join(m.letter_list)


@mod.capture(rule="spell {self.letter_with_capitals}+")
def dictate_letters(m) -> str:
  """Multiple letter keys preceded by a dictation command. Includes capital letters."""
  return "".join(m.letter_with_capitals_list)
