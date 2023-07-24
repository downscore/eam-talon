"""Talon code for Obsidian support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module

mod = Module()
ctx = Context()

mod.apps.obsidian = """
app.bundle: md.obsidian
"""

ctx.matches = r"""
app: obsidian
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def textflow_get_selected_text_potato_mode() -> str:
    # Obsidian copies the entire line if nothing is selected, which breaks a bunch of TextFlow stuff.
    # Always pretend nothing is selected.
    return ""

  def textflow_force_potato_mode() -> bool:
    # Obsidian does not properly implement the accessibility API. It does not give accurate character counts for
    # the current selection, and appears to group multiple consecutive line breaks into a single line break.
    return True
