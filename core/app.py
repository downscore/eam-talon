"""Default implementations for built-in Talon app actions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
  """App actions."""

  def app_preferences():
    """Opens app preferences."""
    actions.key("cmd-,")

  def app_get_current_directory() -> str:
    """Returns the current directory of the active window. Empty string if unknown or not applicable."""
    return ""

  def app_get_current_location() -> str:
    """Returns the current file path or URL from the active window. Empty string if unknown or not applicable."""
    return ""

  def app_copy_current_location():
    """Copies the current file path or URL from the active window to the clipboard."""
    location = actions.user.app_get_current_location()
    if not location:
      actions.app.notify("No location found")
      return
    actions.user.clipboard_history_set_text(location)

  def app_copy_current_directory():
    """Copies the current directory from the active window to the clipboard."""
    directory = actions.user.app_get_current_directory()
    if not directory:
      actions.app.notify("No directory found")
      return
    actions.user.clipboard_history_set_text(directory)
