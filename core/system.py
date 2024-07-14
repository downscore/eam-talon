"""Talon code for managing and debugging the speech system."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, actions, app, imgui, registry, scope, ui

mod = Module()


def unsupported_command(message: str = ""):
  """When a command is not supported, this function notifies the user and raises an exception to
  interrupt chained commands. This prevents subsequent commands that may have relied on the current
  command completing successfully from having unintended effects."""
  message = message if message else "Unsupported command"
  actions.app.notify(message)
  raise ValueError(message)


@imgui.open(y=0)
def context_gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  """Creates a gui displaying active context."""
  for tag in registry.tags:
    gui.text(f"Tag: {str(tag)}")
  gui.spacer()

  for mode in scope.get("mode"):
    gui.text(f"Mode: {str(mode)}")
  gui.spacer()

  for application in scope.get("app.app"):
    gui.text(f"App: {str(application)}")
  gui.spacer()

  gui.text(f"app.name: {actions.app.name()}")
  gui.text(f"app.bundle: {actions.app.bundle()}")
  gui.text(f"app.platform: {app.platform}")
  # gui.text(f"browser.address: {actions.browser.address()}")
  gui.text(f"win.title: {actions.win.title()}")
  gui.text(f"win.file_ext: {actions.win.file_ext()}")
  gui.text(f"ui.active_window().id: {ui.active_window().id}")


@mod.action_class
class Actions:
  """Speech system management and debugging actions."""

  def system_context_ui_toggle():
    """Toggles showing the context UI."""
    if context_gui.showing:
      context_gui.hide()
    else:
      context_gui.show()

  def system_toggle_speech():
    """Toggles speech recognition and updates status file. Useful for making sure the status file is
    updated when toggling speech via a button (as opposed to a spoken command)."""
    actions.speech.toggle()
    actions.user.status_file_update()
