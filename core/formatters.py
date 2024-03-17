"""Talon code for formatting text."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, Context, actions
from .lib import format_util, text_util

mod = Module()
ctx = Context()

# Formatters keyed by word.
# Note: Sentence and Title formatters are separate as they do not need to be combined with other formatters.
_FORMATTERS_BY_WORD = {
    # Case formatters. They do not modify separators or surround strings.
    "allcaps": format_util.Formatters.UPPERCASE,
    "alldown": format_util.Formatters.LOWERCASE,

    # Join formatters. May also change case.
    "camel": format_util.Formatters.CAMEL,
    "dotted": format_util.Formatters.DOT_SEPARATED,
    "numerate": format_util.Formatters.ENUM,
    "hammer": format_util.Formatters.PASCAL,
    "kebab": format_util.Formatters.KEBAB,
    "packed": format_util.Formatters.DOUBLE_COLON_SEPARATED,
    "smash": format_util.Formatters.NO_SPACES,
    "snake": format_util.Formatters.SNAKE,
    # Haven't found a use yet for slash separation formatter.
    # "slasher": format_util.Formatters.SLASH_SEPARATED,
}
mod.list("formatter", desc="List of all formatter words")
ctx.lists["self.formatter"] = _FORMATTERS_BY_WORD.keys()

# Last strings output from each formatter. Keyed by a single formatter enum value.
# Strings sent to multiple formatters are stored under each individual formatter.
# Not updated when a selection is reformatted.
_LAST_OUTPUT_BY_FORMATTER = {}

# Last strings output in other formats.
_LAST_TITLE = ""
_LAST_SENTENCE = ""


def _reformat_string(s: str, options: format_util.FormatOptions) -> str:
  """Reformat the given string with the given options, preserving padding."""
  stripped = text_util.StrippedString(s)
  if not stripped.stripped:
    return ""
  unformatted = format_util.unformat_phrase(stripped.stripped)
  formatted = format_util.format_phrase(unformatted, options)
  return stripped.apply_padding(formatted)


def _title_reformat_string(s: str) -> str:
  """Reformat the given string with the given options, preserving padding."""
  stripped = text_util.StrippedString(s)
  if not stripped.stripped:
    return ""
  unformatted = format_util.unformat_phrase(stripped.stripped)
  formatted = format_util.title_format_phrase(unformatted)
  return stripped.apply_padding(formatted)


@mod.action_class
class Actions:
  """Formatter actions."""

  def format_single(phrase: str, formatter_word: str) -> str:
    """Formats a phrase using the given formatter."""
    formatter_enums = [_FORMATTERS_BY_WORD[formatter_word]]
    options = format_util.get_format_options(formatter_enums)
    result = format_util.format_phrase(phrase, options)
    _LAST_OUTPUT_BY_FORMATTER[formatter_enums[0]] = result
    return result

  def format_multiple(phrase: str, formatter_words: list[str]) -> str:
    """Formats a phrase using the given formatters."""
    formatter_enums = list(map(lambda f: _FORMATTERS_BY_WORD[f], formatter_words))
    options = format_util.get_format_options(formatter_enums)
    result = format_util.format_phrase(phrase, options)
    for formatter_enum in formatter_enums:
      _LAST_OUTPUT_BY_FORMATTER[formatter_enum] = result
    return result

  def format_selection(formatter_words: list[str]):
    """Formats the current selection in place using the given formatters."""
    formatter_enums = list(map(lambda f: _FORMATTERS_BY_WORD[f], formatter_words))
    options = format_util.get_format_options(formatter_enums)
    selected = actions.user.selected_text()
    reformatted = _reformat_string(selected, options)
    if not reformatted:
      return
    actions.user.insert_via_clipboard(reformatted)

  def format_title(phrase: str) -> str:
    """Formats a phrase using title casing."""
    return format_util.title_format_phrase(phrase)

  def format_title_with_history(phrase: str) -> str:
    """Formats a phrase using title casing."""
    global _LAST_TITLE
    result = format_util.title_format_phrase(phrase)
    _LAST_TITLE = result
    return result

  def format_selection_title():
    """Reformats the current selection as a title."""
    selected = actions.user.selected_text()
    reformatted = _title_reformat_string(selected)
    if not reformatted:
      return
    actions.user.insert_via_clipboard(reformatted)

  def format_sentence(phrase: str) -> str:
    """Formats a phrase using sentence casing."""
    global _LAST_SENTENCE
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
    result = format_util.format_phrase(phrase, options)
    _LAST_SENTENCE = result
    return result

  def format_selection_sentence():
    """Reformats the current selection as a sentence."""
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
    selected = actions.user.selected_text()
    reformatted = _reformat_string(selected, options)
    if not reformatted:
      return
    actions.user.insert_via_clipboard(reformatted)

  def format_selection_phrase():
    """Reformats the current selection as a phrase."""
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.LOWERCASE
    selected = actions.user.selected_text()
    reformatted = _reformat_string(selected, options)
    if not reformatted:
      return
    actions.user.insert_via_clipboard(reformatted)

  def format_uppercase(phrase: str) -> str:
    """Formats a phrase using all caps."""
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.UPPERCASE
    return format_util.format_phrase(phrase, options)

  def format_replay(formatter_word: str) -> str:
    """Returns the last string output by the given formatter."""
    formatter_enums = [_FORMATTERS_BY_WORD[formatter_word]]
    if formatter_enums[0] not in _LAST_OUTPUT_BY_FORMATTER:
      actions.app.notify(f"No output found. Formatter: {formatter_word}")
      return ""
    return _LAST_OUTPUT_BY_FORMATTER[formatter_enums[0]]

  def format_replay_title() -> str:
    """Returns the last string output by the title formatter."""
    if not _LAST_TITLE:
      actions.app.notify("No title output found.")
      return ""
    return _LAST_TITLE

  def format_replay_sentence() -> str:
    """Returns the last string output by the sentence formatter."""
    if not _LAST_SENTENCE:
      actions.app.notify("No sentence output found.")
      return ""
    return _LAST_SENTENCE
