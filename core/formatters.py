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
    "period": format_util.Formatters.DOT_SEPARATED,
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


def _reformat_string(s: str, options: format_util.FormatOptions) -> str:
  """Reformat the given string with the given options, preserving padding."""
  stripped = text_util.StrippedString(s)
  if not stripped.stripped:
    return ""
  unformatted = format_util.unformat_phrase(stripped.stripped)
  formatted = format_util.format_phrase(unformatted, options)
  return stripped.apply_padding(formatted)


@mod.action_class
class Actions:
  """Formatter actions."""

  def format_multiple(phrase: str, formatter_words: list[str]) -> str:
    """Formats a phrase using the given formatters."""
    formatter_enums = list(map(lambda f: _FORMATTERS_BY_WORD[f], formatter_words))
    options = format_util.get_format_options(formatter_enums)
    return format_util.format_phrase(phrase, options)

  def format_selection(formatter_words: list[str]):
    """Formats the current selection in place using the given formatters."""
    formatter_enums = list(map(lambda f: _FORMATTERS_BY_WORD[f], formatter_words))
    options = format_util.get_format_options(formatter_enums)
    selected = actions.edit.selected_text()
    reformatted = _reformat_string(selected, options)
    if not reformatted:
      return
    actions.user.insert_via_clipboard(reformatted)

  def format_title(phrase: str) -> str:
    """Formats a phrase using title casing."""
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
    options.rest_capitalization = format_util.WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING
    return format_util.format_phrase(phrase, options)

  def format_selection_title():
    """Reformats the current selection as a title."""
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
    options.rest_capitalization = format_util.WordCapitalization.TITLE_CASE_PRESERVE_FOLLOWING
    selected = actions.edit.selected_text()
    reformatted = _reformat_string(selected, options)
    if not reformatted:
      return
    actions.user.insert_via_clipboard(reformatted)

  def format_sentence(phrase: str) -> str:
    """Formats a phrase using sentence casing."""
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
    return format_util.format_phrase(phrase, options)

  def format_selection_sentence():
    """Reformats the current selection as a sentence."""
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.CAPITALIZE_FIRST_PRESERVE_FOLLOWING
    selected = actions.edit.selected_text()
    reformatted = _reformat_string(selected, options)
    if not reformatted:
      return
    actions.user.insert_via_clipboard(reformatted)

  def format_selection_phrase():
    """Reformats the current selection as a phrase."""
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.LOWERCASE
    selected = actions.edit.selected_text()
    reformatted = _reformat_string(selected, options)
    if not reformatted:
      return
    actions.user.insert_via_clipboard(reformatted)

  def format_uppercase(phrase: str) -> str:
    """Formats a phrase using all caps."""
    options = format_util.FormatOptions()
    options.first_capitalization = format_util.WordCapitalization.UPPERCASE
    return format_util.format_phrase(phrase, options)
