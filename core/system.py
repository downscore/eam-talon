"""Talon code for managing and debugging the speech system."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import os
from talon import Module, actions, app, imgui, registry, scope

mod = Module()


@imgui.open(y=0)
def context_gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  """Creates a gui displaying active context."""
  gui.text("Tags")
  gui.line()
  for tag in registry.tags:
    gui.text(str(tag))
  gui.spacer()
  gui.spacer()

  gui.text("Modes")
  gui.line()
  for mode in scope.get("mode"):
    gui.text(str(mode))
  gui.spacer()
  gui.spacer()

  gui.text("Apps")
  gui.line()
  for application in scope.get("app.app"):
    gui.text(str(application))
  gui.spacer()
  gui.spacer()

  gui.text(f"app.name: {actions.app.name()}")
  gui.text(f"app.bundle: {actions.app.bundle()}")
  gui.text(f"app.platform: {app.platform}")
  # gui.text(f"browser.address: {actions.browser.address()}")
  gui.text(f"win.title: {actions.win.title()}")
  gui.text(f"win.file_ext: {actions.win.file_ext()}")


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
    """Toggles speech recognition and updates status file. Useful for making sure the status file is updated when
    toggling speech via a button (as opposed to a spoken command)."""
    actions.speech.toggle()
    actions.user.status_file_update()

  def system_notify_say(text: str):
    """Says the given text."""
    os.system(f"say \"{text}\"")
