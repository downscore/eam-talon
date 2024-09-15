"""Talon code for Neovim support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from dataclasses import dataclass
from talon import Context, Module, actions, clip
from ..core.lib import textflow_types as tf

mod = Module()
ctx = Context()

mod.apps.neovim = """
app.bundle: org.alacritty
title: / - neovim$/
"""

ctx.matches = r"""
app: neovim
"""


@dataclass
class NeovimContext:
  """Context, including mode, text, and selection range, from neovim."""
  # A character representing the current mode. n - normal, i - insert, v - visual.
  mode: str
  # Text around the cursor.
  text: str
  # 0-based character indexes of the selection range.
  selection_range: tf.TextRange
  # 1-based line numbers of the selection range.
  selection_range_line_numbers: tf.TextRange


@mod.action_class
class Actions:
  """Neovim-specific actions."""

  def neovim_get_context() -> NeovimContext:
    """Gets the current editor context, including the current mode."""
    with clip.capture() as s:
      actions.key("ctrl-s")
    try:
      context = s.text()
    except clip.NoChange as exc:
      raise ValueError("Failed to capture Neovim context.") from exc

    # The first few lines contain information about the mode and selection.
    lines = context.split("\n")
    if len(lines) < 6:
      raise ValueError(f"Invalid Neovim context: {context}")
    mode = lines[0].strip()
    if len(mode) != 1:
      raise ValueError(f"Invalid Neovim mode: {context}")
    selection_from = int(lines[1])
    selection_to = int(lines[2])
    if (selection_from < 0 or selection_to < 0 or selection_from > selection_to):
      raise ValueError(f"Invalid Neovim selection range: {context}")
    selection_line_from = int(lines[3])
    selection_line_to = int(lines[4])
    if (selection_line_from < 0 or selection_line_to < 0 or
        selection_line_from > selection_line_to):
      raise ValueError(f"Invalid Neovim selection line range: {context}")

    # The rest of the lines contain the text around the cursor.
    text = "\n".join(lines[5:])

    return NeovimContext(mode, text, tf.TextRange(selection_from, selection_to),
                         tf.TextRange(selection_line_from, selection_line_to))


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
