"""Talon code for Neovim support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.apps.neovim = """
app.bundle: org.alacritty
title: / - neovim$/
"""

ctx.matches = r"""
app: neovim
"""


@ctx.action_class("win")
class WinActions:
  """Action overrides."""

  def filename():
    """Gets the open filename."""
    title = actions.win.title()
    parts = title.split(" - ")
    if len(parts) == 0:
      return ""
    return parts[0]
