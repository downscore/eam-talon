"""Talon code for VS Code support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, clip
from ..core import mode_dictation
from ..core.lib import path_util

mod = Module()
ctx = Context()

# Matchers for VS Code app on MacOS.
mod.apps.vscode = """
os: mac
and app.bundle: com.microsoft.VSCode
os: mac
and app.bundle: com.microsoft.VSCodeInsiders
os: mac
and app.bundle: com.visualstudio.code.oss
"""

ctx.matches = r"""
app: vscode
"""


@mod.action_class
class Actions:
  """VS Code-specific actions."""

  def vscode_jump_to_file(path: str):
    """Jumps to the given file in VS Code."""
    actions.key("cmd-p")
    actions.user.insert_via_clipboard(path)
    actions.key("enter")

  def vscode_jump_to_test():
    """Jumps to the test file for the current file in VS Code."""
    current_path = actions.user.app_get_current_location()
    # Default to python test files.
    # TODO: Override for other languages.
    test_path = path_util.get_test_path(current_path, ".py")
    actions.user.vscode_jump_to_file(test_path)

  def vscode_jump_to_related_file_with_extension(extension: str):
    """Jumps to a related file with the given extension in VS Code."""
    current_path = actions.user.app_get_current_location()
    new_path = path_util.remove_test_suffix(current_path)
    new_path = path_util.replace_file_extension(new_path, extension)
    actions.user.vscode_jump_to_file(new_path)


@ctx.action_class("win")
class WinActions:
  """Action overwrites."""

  def filename():
    """Gets the open filename. Required for files opened over SSH."""
    title = actions.win.title()
    parts = title.split(" — ")
    if len(parts) == 0:
      return ""
    return parts[0]


@ctx.action_class("user")
class ExtensionActions:
  """Action overwrites."""

  def dictation_get_preceding_text() -> str:
    for _ in range(mode_dictation.NUM_PRECEDING_CHARS):
      actions.user.extend_left()

    # Bypass extension for getting selected text. This allows dictation to work in, for example, the Search and
    # Source Control panels.
    with clip.capture() as s:
      actions.user.copy()
    try:
      preceding_text = s.text()
    except clip.NoChange:
      preceding_text = ""

    # Deselect preceding text only if it was not empty.
    if preceding_text:
      actions.user.right()

    return preceding_text

  def tab_open():
    actions.user.vscode("workbench.action.files.newUntitledFile")

  def tab_close():
    actions.user.vscode("workbench.action.closeActiveEditor")

  def tab_next():
    actions.user.vscode("workbench.action.nextEditorInGroup")

  def tab_reopen():
    actions.user.vscode("workbench.action.reopenClosedEditor")

  def window_close():
    actions.user.vscode("workbench.action.closeWindow")

  def window_open():
    actions.user.vscode("workbench.action.newWindow")

  # Note: Prevents using delete line command outside of editor (e.g. in Search panel).
  # def delete_line():
  #   actions.user.vscode_and_wait("editor.action.deleteLines")

  def find_next():
    actions.user.vscode("search.action.focusNextSearchResult")

  def find_previous():
    actions.user.vscode("search.action.focusPreviousSearchResult")

  def indent_more():
    actions.user.vscode("editor.action.indentLines")

  def indent_less():
    actions.user.vscode("editor.action.outdentLines")

  def jump_line(n: int):
    actions.user.vscode("workbench.action.gotoLine")
    actions.insert(n)
    actions.key("down enter")

  def line_insert_down():
    # Using the action prevents triggering autocomplete instead of inserting new line.
    actions.user.vscode("editor.action.insertLineAfter")

  def line_insert_up():
    # Using the action prevents triggering autocomplete instead of inserting new line.
    actions.user.vscode("editor.action.insertLineBefore")

  def line_swap_down():
    actions.user.vscode("editor.action.moveLinesDownAction")

  def line_swap_up():
    actions.user.vscode("editor.action.moveLinesUpAction")

  def save_all():
    actions.user.vscode("workbench.action.files.saveAll")

  # Note: Prevents using select line command outside of editor (e.g. in Search panel).
  # def select_line():
  #   actions.user.vscode("expandLineSelection")

  def select_line_including_line_break():
    # Ensure leading white spaces included.
    actions.key("cmd-right cmd-left cmd-left cmd-shift-right shift-right")

  def zoom_reset():
    actions.key("cmd-keypad_0")

  def duplicate_line():
    actions.user.vscode("editor.action.copyLinesDownAction")

  def multi_cursor_skip():
    actions.key("cmd-k cmd-d")

  def multi_cursor_select_all():
    actions.key("cmd-shift-l")

  def multi_cursor_add_to_line_ends():
    # Alternative action: editor.action.insertCursorAtEndOfEachLineSelected
    actions.key("alt-shift-i")

  def navigation_back():
    actions.user.vscode("workbench.action.navigateBack")

  def navigation_forward():
    actions.user.vscode("workbench.action.navigateForward")

  def source_control_change_previous():
    actions.user.vscode("workbench.action.editor.previousChange")

  def source_control_change_next():
    actions.user.vscode("workbench.action.editor.nextChange")

  def split_open_up():
    actions.user.vscode("workbench.action.moveEditorToAboveGroup")

  def split_open_down():
    actions.user.vscode("workbench.action.moveEditorToBelowGroup")

  def split_open_left():
    actions.user.vscode("workbench.action.moveEditorToLeftGroup")

  def split_open_right():
    actions.user.vscode("workbench.action.moveEditorToRightGroup")

  def split_close():
    actions.user.vscode("workbench.action.joinTwoGroups")

  def split_maximize():
    actions.user.vscode("workbench.action.toggleMaximizeEditorGroup")

  def split_next():
    actions.user.vscode_and_wait("workbench.action.focusNextGroup")

  def split_last():
    actions.user.vscode_and_wait("workbench.action.focusPreviousGroup")

  def split_switch_up():
    actions.user.vscode_and_wait("workbench.action.focusAboveGroup")

  def split_switch_down():
    actions.user.vscode_and_wait("workbench.action.focusBelowGroup")

  def split_switch_left():
    actions.user.vscode_and_wait("workbench.action.focusLeftGroup")

  def split_switch_right():
    actions.user.vscode_and_wait("workbench.action.focusRightGroup")

  def split_move_file_up():
    actions.user.vscode_and_wait("workbench.action.moveEditorToAboveGroup")

  def split_move_file_down():
    actions.user.vscode_and_wait("workbench.action.moveEditorToBelowGroup")

  def split_move_file_left():
    actions.user.vscode_and_wait("workbench.action.moveEditorToLeftGroup")

  def split_move_file_right():
    actions.user.vscode_and_wait("workbench.action.moveEditorToRightGroup")

  def split_switch_by_index(index: int):
    if index > 9:
      return
    actions.key(f"cmd-{index}")

  def switcher_jump_to_bookmark(bookmark_num: int):
    # IDE is already focused so just jump to the bookmark.
    actions.key(f"ctrl-{bookmark_num}")

  def tab_nth_previous(n: int):
    # Make sure number of tab switches is reasonable.
    if n < 1 or n > 9:
      return
    if n == 1:
      actions.key("ctrl-tab")
    else:
      actions.key(f"cmd-p down:{n} enter")

  def tab_list(name: str):
    # Alternative: actions.user.vscode("workbench.action.quickOpen")
    actions.key("cmd-p")
    if name:
      actions.user.insert_via_clipboard(name or "")
      actions.sleep("50ms")

  def tab_switch_by_name(name: str):
    # Alternative: actions.user.vscode("workbench.action.quickOpen")
    actions.key("cmd-p")
    actions.user.insert_via_clipboard(name)
    actions.sleep("50ms")
    actions.key("enter")

  def textflow_get_selected_text_potato_mode() -> str:
    # By default, VS Code copies the entire line if nothing is selected, which breaks a bunch of TextFlow stuff.
    # Always pretend nothing is selected.
    return ""
