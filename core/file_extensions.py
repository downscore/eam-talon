"""Talon code for handling file extensions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, Context

mod = Module()
ctx = Context()

# File extensions that can be used when dictating prose.
_FILE_EXTENSIONS = {
    "python": ".py",
    "talon": ".talon",
    "tallon": ".talon",
    "markdown": ".md",
    "m d": ".md",
    "see see": ".cc",
    "cc": ".cc",
    "header": ".h",
    "comma separated": ".csv"
}
mod.list("file_extension", desc="Extensions for different file types.")
ctx.lists["self.file_extension"] = _FILE_EXTENSIONS


@mod.capture(rule="file {self.file_extension}")
def file_extension(m) -> str:
  """Multiple letter keys preceded by a dictation command."""
  return m.file_extension
