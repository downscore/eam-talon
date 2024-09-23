"""Talon code for C++ language support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module
from ..core.lib import scrambler_types as st

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.lang_cpp
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overrides."""

  def scrambler_get_scope_modifier() -> st.ModifierType:
    return st.ModifierType.C_SCOPE
