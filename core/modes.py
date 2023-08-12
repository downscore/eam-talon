"""Talon code for changing modes."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, actions

mod = Module()


@mod.action_class
class ExtensionActions:
  """Actions for changing modes."""

  def mode_command():
    """Switches to command mode."""
    actions.mode.disable("sleep")
    actions.mode.disable("dictation")
    actions.mode.enable("command")

  def mode_dictation():
    """Switches to dictation mode."""
    actions.mode.disable("sleep")
    actions.mode.disable("command")
    actions.mode.enable("dictation")

  def mode_enable_speech():
    """Enables speech recognition."""
    actions.speech.enable()
    actions.user.mode_command()

  def mode_disable_speech():
    """Disables speech recognition."""
    actions.speech.disable()

  def mode_mixed():
    """Switches to mixed (dictation + command) mode."""
    actions.mode.disable("sleep")
    actions.mode.enable("command")
    actions.mode.enable("dictation")
