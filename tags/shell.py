"""Actions and tags for terminal apps. Called "shell" to disambiguate from MacOS Terminal app."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.tag("shell", "Application with a terminal")

ctx.matches = r"""
tag: user.shell
"""


@mod.action_class
class Actions:
  """Common terminal actions."""

  def shell_search_commands():
    """Searches through commands."""
    actions.key("ctrl-r")


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def file_manager_open_parent():
    actions.insert("cd ..")

  def file_manager_open_directory(path: str):
    actions.insert(f"cd {path}")
