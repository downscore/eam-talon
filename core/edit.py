"""Talon code for common edit actions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import re
from talon import Context, Module, actions, app, clip
from .lib import format_util, text_util

mod = Module()
ctx = Context()


def _get_selected_text_fragments():
  """Gets the selected text and its fragment ranges. If no text is selected, selects the current word."""
  text = actions.user.selected_text_or_word()

  # Special case: Ignore list item markers (e.g. in Apple Notes).
  if text.startswith("- "):
    text = text[2:]

  fragments = format_util.get_fragment_ranges(text)
  return text, fragments


@mod.action_class
class ExtensionActions:
  """User-defined edit actions.
  Note that many of these actions are also built-in to Talon in the "edit" namespace. After a Talon update that
  (probably unintentionally) overrode these implementations, and following some unexpected internal Talon usages of
  built-in actions, they were moved to user-defined actions to avoid the potential for problems in the future."""

  def copy():
    """Copies the currently-selected text to the clipboard."""
    actions.key("cmd-c")

  def cut():
    """Cuts the currently-selected text to the clipboard."""
    actions.key("cmd-x")

  def paste():
    """Pastes the clipboard contents."""
    # Short sleeps to allow UI to catch up for chained commands.
    actions.sleep("50ms")
    actions.key("cmd-v")
    actions.sleep("50ms")

  def paste_match_style():
    """Pastes the clipboard contents with the style of the surrounding text."""
    actions.key("cmd-shift-v")

  def delete():
    """Deletes the currently-selected text or the previous character."""
    actions.key("backspace")

  def delete_line():
    """Deletes the entire line."""
    actions.user.select_line_including_line_break()
    actions.user.delete()

  def delete_word():
    """Deletes the current word."""
    actions.user.select_word()
    actions.user.delete()

  def up():
    """Moves the cursor up."""
    actions.key("up")

  def down():
    """Moves the cursor down."""
    actions.key("down")

  def left():
    """Moves the cursor left."""
    actions.key("left")

  def right():
    """Moves the cursor right."""
    actions.key("right")

  def word_left():
    """Moves the cursor left by one word."""
    actions.key("alt-left")

  def word_right():
    """Moves the cursor right by one word."""
    actions.key("alt-right")

  def line_start():
    """Moves the cursor to the start of the line."""
    actions.key("cmd-left")

  def line_end():
    """Moves the cursor to the end of the line."""
    actions.key("cmd-right")

  def file_end():
    """Moves the cursor to the end of the file."""
    actions.key("cmd-down")

  def file_start():
    """Moves the cursor to the start of the file."""
    actions.key("cmd-up")

  def extend_up():
    """Extends the selection up."""
    actions.key("shift-up")

  def extend_down():
    """Extends the selection down."""
    actions.key("shift-down")

  def extend_left():
    """Extends the selection to the left."""
    actions.key("shift-left")

  def extend_right():
    """Extends the selection to the right."""
    actions.key("shift-right")

  def extend_file_end():
    """Extends the selection to the end of the file."""
    actions.key("cmd-shift-down")

  def extend_file_start():
    """Extends the selection to the start of the file."""
    actions.key("cmd-shift-up")

  def extend_line_end():
    """Extends the selection to the end of the line."""
    actions.key("cmd-shift-right")

  def extend_line_start():
    """Extends the selection to the start of the line."""
    actions.key("cmd-shift-left")

  def extend_page_down():
    """Extends the selection down by one page."""
    actions.key("cmd-shift-pagedown")

  def extend_page_up():
    """Extends the selection up by one page."""
    actions.key("cmd-shift-pageup")

  def extend_word_left():
    """Extends the selection to the left by one word."""
    actions.key("shift-alt-left")

  def extend_word_right():
    """Extends the selection to the right by one word."""
    actions.key("shift-alt-right")

  def select_all():
    """Selects all text in the active editor."""
    actions.key("cmd-a")

  def select_line_excluding_line_break():
    """Selects the current line, not including the trailing line break if present."""
    actions.key("cmd-left cmd-shift-right")

  def select_line_including_line_break():
    """Selects the current line, including the trailing line break if present."""
    actions.key("cmd-left cmd-shift-right shift-right")

  def select_word():
    """Selects the current word."""
    actions.user.left()
    actions.user.word_right()
    actions.user.word_left()
    actions.user.extend_word_right()

  def find():
    """Finds text in the active editor."""
    actions.key("cmd-f")

  def find_next():
    """Finds the next occurrence of the text."""
    actions.key("cmd-g")

  def find_previous():
    """Finds the previous occurrence of the text."""
    actions.key("cmd-shift-g")

  def indent_less():
    """Decreases the indentation level."""
    actions.key("cmd-[")

  def indent_more():
    """Increases the indentation level."""
    actions.key("cmd-]")

  def line_insert_up():
    """Inserts a new line above the current line."""
    # Going to line end first can help consistently preserve indentation in code.
    actions.user.line_end()
    actions.user.line_start()
    actions.key("enter up")

  def line_insert_down():
    """Inserts a new line below the current line."""
    actions.user.line_end()
    actions.key("enter")

  def line_swap_up():
    """Swaps the current line with the line above it."""
    actions.user.select_line_including_line_break()
    actions.user.cut()
    actions.sleep("50ms")
    actions.key("up")
    actions.user.paste()
    actions.key("left")

  def line_swap_down():
    """Swaps the current line with the line below it."""
    actions.user.select_line_including_line_break()
    actions.user.cut()
    actions.key("down")
    actions.user.paste()
    actions.key("left")

  def undo():
    """Undoes the last action."""
    actions.key("cmd-z")

  def redo():
    """Redoes the last action."""
    actions.key("cmd-shift-z")

  def save():
    """Saves the current file."""
    actions.key("cmd-s")

  def save_all():
    """Saves all open files."""
    actions.key("cmd-shift-s")

  def zoom_in():
    """Zooms in."""
    actions.key("cmd-=")

  def zoom_out():
    """Zooms out."""
    actions.key("cmd--")

  def zoom_reset():
    """Resets the zoom level."""
    actions.key("cmd-0")

  def selected_text() -> str:
    """Returns the currently-selected text. If no text is selected, returns an empty string."""
    with clip.capture() as s:
      actions.user.copy()
    try:
      return s.text()
    except clip.NoChange:
      return ""

  def selected_text_or_word() -> str:
    """Returns the currently-selected text. If no text is selected, tries to select the current word and return that."""
    selected = actions.user.selected_text()
    if selected:
      return selected
    actions.user.select_word()
    return actions.user.selected_text()

  def count_lines():
    """Pops up a notification with the number of lines in the currently selected text."""
    lines = text_util.count_lines(actions.user.selected_text())
    app.notify(f"Lines: {lines}")

  def count_words():
    """Pops up a notification with the number of words in the currently selected text."""
    words = text_util.count_words(actions.user.selected_text())
    app.notify(f"Words: {words}")

  def count_characters():
    """Pops up a notification with the number of characters in the currently selected text."""
    characters = len(actions.user.selected_text())
    app.notify(f"Characters: {characters}")

  def delete_to_line_end():
    """Delete from the cursor to the end of the line."""
    actions.user.extend_line_end()
    actions.user.delete()

  def delete_to_line_start():
    """Delete from the cursor to the start of the line."""
    actions.user.extend_line_start()
    actions.user.delete()

  def delete_word_left(n: int = 1):
    """Delete one or more words to the left of the cursor."""
    for _ in range(n):
      actions.user.extend_word_left()
      actions.user.delete()

  def delete_word_right(n: int = 1):
    """Delete one or more words to the right of the cursor."""
    for _ in range(n):
      actions.user.extend_word_right()
      actions.user.delete()

  def duplicate_line():
    """Duplicate the current line."""
    actions.user.select_line_including_line_break()
    line_text = actions.user.selected_text()
    actions.user.right()
    actions.user.insert_via_clipboard(line_text)
    actions.user.left()

  def expand_selection_to_adjacent_characters():
    """Expands the current selection to include adjacent characters on the left and right."""
    selection_length = len(actions.user.selected_text())
    # Disallow for long strings, as they can take a long time to select.
    if selection_length > 500:
      return
    actions.key(f"left:2 shift-right:{selection_length + 2}")

  def find_everywhere():
    """Finds text across project."""
    actions.key("cmd-shift-f")

  def fragment_cursor_after(n: int):
    """Moves the cursor after the nth fragment of the selected text. Index is 1-based."""
    _, fragments = _get_selected_text_fragments()
    if n <= 0 or n > len(fragments):
      return
    fragment = fragments[n - 1]
    actions.key(f"left right:{fragment[1]}")

  def fragment_cursor_before(n: int):
    """Moves the cursor before the nth fragment of the selected text. Index is 1-based."""
    _, fragments = _get_selected_text_fragments()
    if n <= 0 or n > len(fragments):
      return
    fragment = fragments[n - 1]
    actions.key(f"left right:{fragment[0]}")

  def fragment_delete(from_index: int, to_index: int = 0):
    """Deletes the given fragment or range of fragments of the selected text. Deletes the last fragment if `from_index`
    is negative. Index is 1-based."""
    if from_index == 0:
      return
    _, fragments = _get_selected_text_fragments()
    if from_index > len(fragments):
      return

    # Negative index deletes the last fragment.
    if from_index < 0:
      from_index = len(fragments)  # pylint: disable=self-cls-assignment

    from_fragment = fragments[from_index - 1]
    if to_index > 0 and to_index <= len(fragments):
      to_fragment = fragments[to_index - 1]
    else:
      to_fragment = from_fragment

    # Check if we need to delete a separator character before or after the fragment.
    delete_before = from_index > 1 and fragments[from_index - 2][1] < from_fragment[0]
    # Using int(n) below to suppress pylint error.
    delete_after = not delete_before and from_index < len(fragments) and to_fragment[1] < fragments[int(from_index)][0]

    start_index = from_fragment[0] - (1 if delete_before else 0)
    length = to_fragment[1] - from_fragment[0] + (1 if delete_before or delete_after else 0)

    actions.key(f"left right:{start_index}")
    actions.key(f"shift-right:{length}")
    actions.key("backspace")

  def fragment_select(from_index: int, to_index: int = 0):
    """Selects a fragment or range of fragments of the selected text. Index is 1-based."""
    _, fragments = _get_selected_text_fragments()
    if from_index <= 0 or from_index > len(fragments):
      return
    from_fragment = fragments[from_index - 1]
    if to_index > 0 and to_index <= len(fragments):
      to_fragment = fragments[to_index - 1]
    else:
      to_fragment = from_fragment
    actions.key(f"left right:{from_fragment[0]}")
    actions.key(f"shift-right:{to_fragment[1] - from_fragment[0]}")

  def fragment_select_head(n: int):
    """Selects from the nth fragment of the selected text to the start. Index is 1-based."""
    _, fragments = _get_selected_text_fragments()
    if n <= 0 or n > len(fragments):
      return
    fragment = fragments[n - 1]
    actions.key(f"left right:{fragment[1]}")
    actions.key(f"shift-left:{fragment[1]}")

  def fragment_select_tail(n: int):
    """Selects from the nth fragment of the selected text to the end. Index is 1-based."""
    text, fragments = _get_selected_text_fragments()
    if n <= 0 or n > len(fragments):
      return
    fragment = fragments[n - 1]
    actions.key(f"left right:{fragment[0]}")
    actions.key(f"shift-right:{len(text) - fragment[0]}")

  def insert_link():
    """Insert a link or make the selected text into a link."""
    actions.user.surround_selected_text("[", "]()")
    actions.key("left:1")

  def insert_link_from_clipboard():
    """Insert a link or make the selected text into a link using the URL in the clipboard."""
    # Prepend "http://" to special links that don't have a protocol.
    regex = r"^[a-zA-Z]{1,2}/"
    clipboard_text = clip.text()
    if clipboard_text and re.match(regex, clipboard_text):
      clipboard_text = f"http://{clipboard_text}"

    actions.user.surround_selected_text("[", f"]({clipboard_text})")

  def insert_link_from_browser_address():
    """Insert a link or make the selected text into a link using the URL in the last viewed browser tab."""
    address = actions.user.cross_browser_get_current_address()
    actions.user.surround_selected_text("[", f"]({address})")

  def insert_self_link():
    """Make the selected text into a link to itself."""
    selected = actions.user.selected_text()
    actions.user.surround_selected_text("[", f"](http://{selected})")

  def insert_via_clipboard(text: str):
    """Inserts a unicode string using the clipboard. The default insert(str) action cannot insert most non-ASCII
    character."""
    with clip.revert():
      clip.set_text(text)
      actions.user.paste()
      # Sleep here so that clip.revert doesn't revert the clipboard too soon.
      actions.sleep("50ms")

  def jump_to_last_occurrence(text: str):
    """Jumps to the last occurrence of the specified text."""
    actions.key("cmd-f")
    actions.insert(text)
    actions.key("shift-enter")
    actions.key("escape")

  def jump_to_next_occurrence(text: str):
    """Jumps to the next occurrence of the specified text."""
    actions.key("cmd-f")
    actions.insert(text)
    actions.key("escape")

  def push_word_left():
    """Pushes the word or symbol to the left of the cursor left by one word."""
    actions.user.extend_word_left()
    word = actions.user.selected_text()
    actions.user.delete()
    actions.user.word_left()
    actions.user.insert_via_clipboard(word)

  def push_word_right():
    """Pushes the word or symbol to the right of the cursor right by one word."""
    actions.user.extend_word_right()
    word = actions.user.selected_text()
    actions.user.delete()
    actions.user.word_right()
    actions.user.insert_via_clipboard(word)

  def flip_boolean_or_comparison():
    """Flips a boolean value or comparison in the selected text."""
    selected = actions.user.selected_text_or_word()

    replaced = selected.replace("true", "false")
    if replaced == selected:
      replaced = selected.replace("false", "true")
    if replaced == selected:
      replaced = selected.replace("True", "False")
    if replaced == selected:
      replaced = selected.replace("False", "True")
    if replaced == selected:
      replaced = selected.replace("TRUE", "FALSE")
    if replaced == selected:
      replaced = selected.replace("FALSE", "TRUE")
    if replaced == selected:
      replaced = selected.replace("<", ">")
    if replaced == selected:
      replaced = selected.replace(">", "<")

    actions.user.insert_via_clipboard(replaced)

  def replace():
    """Search and replace for text in the active editor."""
    actions.key("cmd-h")

  def replace_everywhere():
    """Search and replaces for text in the entire project."""
    actions.key("cmd-shift-h")

  def select_character_range(from_index: int, to_index: int = 0):
    """Selects a range of characters in the selected text. 1-based. If `to_index` is zero, selects the from
    character."""
    if to_index > 0 and to_index < from_index:
      return

    selected = actions.user.selected_text_or_word()
    if len(selected) == 0 or from_index <= 0 or from_index > len(selected):
      return

    effective_to = min(len(selected), to_index) if to_index > 0 else from_index
    actions.key(f"left right:{from_index - 1}")
    actions.key(f"shift-right:{effective_to - from_index + 1}")

  def sort_lines_ascending():
    """Sorts the selected lines in ascending order."""
    selected_text = actions.user.selected_text()
    selected_text = text_util.sort_lines(selected_text)
    actions.user.insert_via_clipboard(selected_text)

  def sort_lines_descending():
    """Sorts the selected lines in descending order."""
    selected_text = actions.user.selected_text()
    selected_text = text_util.sort_lines(selected_text, reverse=False)
    actions.user.insert_via_clipboard(selected_text)

  def style_title():
    """Format text as a title."""
    actions.user.style_heading(1)

  def style_subtitle():
    """Format text as a subtitle."""
    actions.user.style_heading(2)

  def style_heading(number: int):
    """Make text the specified heading level."""
    # Check if the first word on the line is a heading specifier. If so, keep it selected.
    actions.user.line_start()
    actions.user.extend_word_right()
    first_word = actions.user.selected_text()

    # Clear the word if it's on the next line.
    if first_word.startswith("\n"):
      first_word = ""

    found_heading = all(map(lambda c: c.isspace() or c == "#", first_word)) and any(map(lambda c: c == "#", first_word))

    prefix = ""
    for _ in range(number):
      prefix += "#"

    # If the line already begins with a heading specifier, just replace it (keep it selected), otherwise add new
    # specifier with trailing space.
    if not found_heading:
      prefix += " "
      actions.user.left()

    actions.insert(prefix)

  def style_body():
    """Format text as normal body text."""

  def style_bold():
    """Make text bold."""
    actions.user.surround_selected_text("**", "**")

  def style_italic():
    """"Make text italic."""
    actions.user.surround_selected_text("*", "*")

  def style_underline():
    """"Make text underlined."""
    actions.user.surround_selected_text("<ins>", "</ins>")

  def style_strikethrough():
    """"Make text strikethrough."""
    actions.user.surround_selected_text("~~", "~~")

  def style_highlight():
    """"Make text highlighted."""
    actions.user.surround_selected_text("==", "==")

  def style_bullet_list():
    """Create a bulleted list."""
    actions.user.line_start()
    actions.insert("- ")

  def style_numbered_list():
    """Create a numbered list."""
    actions.user.line_start()
    actions.insert("1. ")

  def style_checklist():
    """Create a checklist."""
    actions.user.line_start()
    actions.insert("- [ ] ")

  def style_toggle_check():
    """Toggle a checkbox."""
    actions.user.select_line_including_line_break()
    line_text = actions.user.selected_text()
    if "[ ]" in line_text:
      line_text = line_text.replace("[ ]", "[x]")
    else:
      line_text = line_text.replace("[x]", "[ ]")
    actions.user.insert_via_clipboard(line_text)

    # Go back to the original line (we just inserted a line break if it wasn't the last line in the file).
    actions.user.left()

  def surround_selected_text(prefix: str, suffix: str):
    """Surrounds the currently-selected text with the given prefix and suffix."""
    text = actions.user.selected_text()
    if text != "":
      actions.user.insert_via_clipboard(f"{prefix}{text}{suffix}")
    else:
      actions.user.insert_via_clipboard(f"{prefix}{suffix}")
      actions.key(f"left:{len(suffix)}")
