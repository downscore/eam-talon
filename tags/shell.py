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

  def shell_search_files():
    """Searches through files."""
    actions.key("ctrl-t")

  def shell_tmux_prefix():
    """Sends the tmux prefix key."""
    actions.key("ctrl-a")

  def shell_tmux_command(command: str):
    """Runs a command at the : prompt in the tmux session. `command` should not include the : character."""
    actions.user.shell_tmux_prefix()
    actions.insert(":")
    actions.sleep("50ms")
    actions.insert(command)
    actions.key("enter")
    actions.sleep("50ms")

  def shell_tmux_new_window(title: str = ""):
    """Creates a new tmux window. Optionally sets the window title."""
    actions.user.tab_open()
    if title:
      actions.user.shell_tmux_prefix()
      actions.key(",")
      actions.user.delete_line()
      actions.insert(title)
      actions.key("enter")
      actions.sleep("50ms")


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def file_manager_open_parent():
    actions.insert("cd ..")

  def file_manager_open_directory(path: str):
    actions.insert(f"cd {path}")

  def file_manager_make_directory(name: str = ""):
    actions.insert(f"mkdir {name}")

  def delete_line():
    actions.key("ctrl-u")

  def delete_all():
    actions.key("ctrl-u")

  def delete_word():
    actions.key("ctrl-w")

  def delete_to_line_end():
    actions.key("ctrl-p")

  def delete_to_line_start():
    actions.key("ctrl-o")

  def delete_word_left(n: int = 1):
    for _ in range(n):
      actions.key("ctrl-w")

  def delete_word_right(n: int = 1):
    for _ in range(n):
      actions.user.word_right()
    actions.user.delete_word_left(n)

  def line_start():
    actions.key("home")

  def line_end():
    actions.key("end")

  def tab_close():
    actions.user.shell_tmux_command("kill-window")

  def tab_next():
    actions.user.shell_tmux_command("next-window")

  def tab_open():
    actions.user.shell_tmux_command("new-window")

  def tab_previous():
    actions.user.shell_tmux_command("last-window")

  def tab_left():
    actions.user.shell_tmux_command("select-window -t :-")

  def tab_right():
    actions.user.shell_tmux_command("select-window -t :+")

  def tab_switch_by_index(num: int):
    actions.user.shell_tmux_command(f"select-window -t {num}")

  def tab_list(name: str):
    actions.user.shell_tmux_command("list-windows")
    if name:
      actions.key("/")
      actions.sleep("50ms")
      actions.insert(name)
      actions.key("enter")
