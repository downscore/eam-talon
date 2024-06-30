"""Talon code for C# language support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module
from ..core.lib import textflow_types as tf

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.lang_csharp
"""


@ctx.action_class("user")
class ExtensionActions:
  """Action overrides."""

  def textflow_get_scope_modifier() -> tf.ModifierType:
    return tf.ModifierType.C_SCOPE
