"""Actions and tags for file management apps."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module

mod = Module()
ctx = Context()

mod.tag("file_manager", "File management apps")

ctx.matches = r"""
tag: user.file_manager
"""

@mod.action_class
class Actions:
  """File management actions."""

  def file_manager_open_parent():
    """Open parent folder."""

  def file_manager_open_directory(path: str):
    """Open the given directory."""
