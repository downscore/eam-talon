"""Actions and tags for terminal apps. Called "shell" to disambiguate from MacOS Terminal app."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, clip

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
    # Give some time for the finder interface to appear. It can take a while in tmux.
    actions.sleep("200ms")

  def shell_search_files():
    """Searches through files."""
    actions.key("ctrl-t")
    # Give some time for the finder interface to appear. It can take a while in tmux.
    actions.sleep("200ms")

  def shell_tmux_prefix():
    """Sends the tmux prefix key."""
    actions.key("ctrl-b")

  def shell_tmux_command(command: str):
    """Runs a command at the : prompt in the tmux session. `command` should not include the :
    character."""
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
  """Action overrides."""

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

  def split_open_up():
    actions.user.shell_tmux_command("split-window -v -b")

  def split_open_down():
    actions.user.shell_tmux_command("split-window -v")

  def split_open_left():
    actions.user.shell_tmux_command("split-window -h -b")

  def split_open_right():
    actions.user.shell_tmux_command("split-window -h")

  def split_close():
    actions.user.shell_tmux_command("kill-pane")

  def split_maximize():
    actions.user.shell_tmux_command("resize-pane -Z")

  def split_next():
    actions.user.shell_tmux_command("next-window")

  def split_last():
    actions.user.shell_tmux_command("last-window")

  def split_switch_up():
    actions.user.shell_tmux_command("select-pane -U")

  def split_switch_down():
    actions.user.shell_tmux_command("select-pane -D")

  def split_switch_left():
    actions.user.shell_tmux_command("select-pane -L")

  def split_switch_right():
    actions.user.shell_tmux_command("select-pane -R")

  def split_switch_by_index(index: int):
    actions.user.shell_tmux_command(f"select-pane -t {index}")

  def split_move_file_up():
    actions.user.shell_tmux_command("rotate-window")

  def split_move_file_down():
    actions.user.shell_tmux_command("rotate-window -U")

  def split_move_file_left():
    actions.user.shell_tmux_command("rotate-window")

  def split_move_file_right():
    actions.user.shell_tmux_command("rotate-window -U")

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

  def website_open_clipboard():
    # Wait for a while so we can send keystrokes properly.
    actions.sleep("1500ms")
    # When opening a URL from the clipboard, we may need to copy the tmux internal buffer to the
    # system clipboard first. Enter keyboard shortcut to copy tmux buffer to system clipboard. This
    # should be a no-op in local tmux sessions.
    actions.key("ctrl-v")
    # Wait for the remote system to send the clipboard contents.
    actions.sleep("500ms")
    actions.user.website_open_clipboard_impl()
