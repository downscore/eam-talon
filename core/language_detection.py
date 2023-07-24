"""Talon code for managing the currently-active programming language."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

_FILE_EXTENSIONS_BY_LANGUAGE = {
    "cpp": {"cpp", "hpp", "cc", "c", "h"},
    "csharp": {"cs"},
    "markdown": {"md"},
    "python": {"py"},
    "talon": {"talon"},
    "typescript": {"ts"},
    "protobuf": {"proto"},
}
_LANGUAGE_BY_EXTENSION = {
    "." + ext: language for language, extensions in _FILE_EXTENSIONS_BY_LANGUAGE.items() for ext in extensions
}

# Create a context for each defined language
for lang in _FILE_EXTENSIONS_BY_LANGUAGE:
  mod.tag(f"lang_{lang}")
  mod.tag(f"lang_forced_{lang}")
  c = Context()
  # Context is active if language is forced or auto language matches.
  c.matches = f"""
    tag: user.lang_forced_{lang}
    tag: user.lang_auto
    and code.language: {lang}
    """
  c.tags = [f"user.lang_{lang}"]

# Create a mode for the automated language detection. This is active when no lang is forced.
mod.tag("lang_auto")
ctx.tags = ["user.lang_auto"]


@ctx.action_class("code")
class CodeActions:

  def language():
    result = ""
    file_extension = actions.win.file_ext()
    if file_extension and file_extension in _LANGUAGE_BY_EXTENSION:
      result = _LANGUAGE_BY_EXTENSION[file_extension]
    return result


@mod.action_class
class Actions:

  def code_set_language_mode(language: str):
    """Sets the active language mode, and disables extension matching."""
    assert language in _FILE_EXTENSIONS_BY_LANGUAGE
    ctx.tags = [f"user.lang_forced_{language}"]

  def code_clear_language_mode():
    """Clears the active language mode, and re-enables code.language: extension matching."""
    ctx.tags = ["user.lang_auto"]
