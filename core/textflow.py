"""Definition of textflow actions and default (potato mode) implementations."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from dataclasses import dataclass
from typing import Optional
from talon import Context, Module, actions, grammar, types, ui
from .lib import textflow, textflow_potato
from .lib import textflow_types as tf

mod = Module()
ctx = Context()

_COMMAND_TYPES_BY_SPOKEN = {
    "take": tf.CommandType.SELECT,
    "before": tf.CommandType.MOVE_CURSOR_BEFORE,
    "after": tf.CommandType.MOVE_CURSOR_AFTER,
    "bring": tf.CommandType.BRING,
    "chuck": tf.CommandType.CLEAR_NO_MOVE,
    "phony": tf.CommandType.NEXT_HOMOPHONE,
    "bigger": tf.CommandType.TITLE_CASE,
    "biggest": tf.CommandType.UPPERCASE,
    "smaller": tf.CommandType.LOWERCASE,
}
mod.list("textflow_command_type", desc="Text navigation command types")
ctx.lists["self.textflow_command_type"] = _COMMAND_TYPES_BY_SPOKEN.keys()

_SINGLE_WORD_COMMAND_TYPES_BY_SPOKEN = {
    "grab": tf.CommandType.SELECT,
    "before": tf.CommandType.MOVE_CURSOR_BEFORE,
    "after": tf.CommandType.MOVE_CURSOR_AFTER,
    "bring": tf.CommandType.BRING,
    "junker": tf.CommandType.CLEAR_NO_MOVE,
    "phony": tf.CommandType.NEXT_HOMOPHONE,
    "bigger": tf.CommandType.TITLE_CASE,
    "biggest": tf.CommandType.UPPERCASE,
    "smaller": tf.CommandType.LOWERCASE,
}
mod.list("textflow_single_word_command_type", desc="Text navigation command types for single words")
ctx.lists["self.textflow_single_word_command_type"] = _SINGLE_WORD_COMMAND_TYPES_BY_SPOKEN.keys()

_SEARCH_DIRECTION_BY_SPOKEN = {
    "next": tf.SearchDirection.FORWARD,
    "last": tf.SearchDirection.BACKWARD,
}
mod.list("textflow_search_direction", desc="Search directions for textflow commands")
ctx.lists["self.textflow_search_direction"] = _SEARCH_DIRECTION_BY_SPOKEN.keys()

_TARGET_COMBO_TYPE_BY_SPOKEN = {
    "past": tf.TargetCombinationType.PAST_TO,
    "until": tf.TargetCombinationType.UNTIL_TO,
}
mod.list("textflow_target_combo_type", desc="Target combination types for textflow commands")
ctx.lists["self.textflow_target_combo_type"] = _TARGET_COMBO_TYPE_BY_SPOKEN.keys()

# Accessibility APIs appear to be limited to this many characters.
_MAX_ACCESSIBLITY_API_CHARS = 10000

# Require at least this many characters after the selection before the accessibility API limit.
_MIN_CHARS_AFTER_ACCESSIBLITY_API_LIMIT = 1000

# Lines to fetch in potato mode.
_POTATO_LINES_BEFORE = 25
_POTATO_LINES_AFTER = 10

# Input action functions keyed by potato action type.
_POTATO_INPUT_ACTIONS_BY_TYPE = {
    textflow_potato.PotatoEditorActionType.GO_UP: actions.edit.up,
    textflow_potato.PotatoEditorActionType.GO_DOWN: actions.edit.down,
    textflow_potato.PotatoEditorActionType.GO_LEFT: actions.edit.left,
    textflow_potato.PotatoEditorActionType.GO_RIGHT: actions.edit.right,
    textflow_potato.PotatoEditorActionType.GO_WORD_LEFT: actions.edit.word_left,
    textflow_potato.PotatoEditorActionType.GO_WORD_RIGHT: actions.edit.word_right,
    textflow_potato.PotatoEditorActionType.GO_LINE_START: actions.edit.line_start,
    textflow_potato.PotatoEditorActionType.GO_LINE_END: actions.edit.line_end,
    textflow_potato.PotatoEditorActionType.EXTEND_UP: actions.edit.extend_up,
    textflow_potato.PotatoEditorActionType.EXTEND_DOWN: actions.edit.extend_down,
    textflow_potato.PotatoEditorActionType.EXTEND_LEFT: actions.edit.extend_left,
    textflow_potato.PotatoEditorActionType.EXTEND_RIGHT: actions.edit.extend_right,
    textflow_potato.PotatoEditorActionType.EXTEND_WORD_LEFT: actions.edit.extend_word_left,
    textflow_potato.PotatoEditorActionType.EXTEND_WORD_RIGHT: actions.edit.extend_word_right,
    textflow_potato.PotatoEditorActionType.EXTEND_LINE_START: actions.edit.extend_line_start,
    textflow_potato.PotatoEditorActionType.EXTEND_LINE_END: actions.edit.extend_line_end,
    textflow_potato.PotatoEditorActionType.CLEAR: actions.edit.delete,
    textflow_potato.PotatoEditorActionType.INSERT_TEXT: actions.user.insert_via_clipboard,
    textflow_potato.PotatoEditorActionType.SET_CLIPBOARD_WITH_HISTORY: actions.user.clipboard_history_set_text,
    textflow_potato.PotatoEditorActionType.SET_CLIPBOARD_NO_HISTORY: actions.clip.set_text,
}

# App bundles we enable AXEnhancedUserInterface for.
_ENHANCED_UI_BUNDLES = [
    "com.microsoft.VSCode", "com.microsoft.VSCodeInsiders", "com.visualstudio.code.oss", "md.obsidian"
]


@dataclass
class TextFlowContext:
  """Context, including text and selection range, that TextFlow will act in."""
  text: str
  selection_range: tf.TextRange
  # Whether we are in potato mode.
  potato_mode: bool = False
  # The starting offset of `text` in the active editor. Used when we are cnot operating on the entire contents of the
  # editor. Not used in potato mode.
  text_offset: int = 0
  # The element that contains the text we are editing. Not used in potato mode.
  editor_element: Optional[ui.Element] = None


def _get_context_potato_mode() -> TextFlowContext:
  """Gets TextFlow context in potato mode."""
  # Check if we already have a selection.
  # Note: Editors that copy the entire line when nothing is selected should override this action to return an empty
  # string. Otherwise, many actions in TextFlow will break, especially for targets after the cursor.
  selected_text = actions.user.textflow_get_selected_text_potato_mode()

  # Collapse selection if necessary.
  if len(selected_text) > 0:
    actions.edit.left()

  # Do not preserve the selection if it is long. Long selections are usually not useful in TextFlow and they can make
  # a potato-mode command execute very slowly.
  if len(selected_text) > 150:  # Around the length of a very long line.
    selected_text = ""

  # Get text before the selection.
  text_before = actions.user.textflow_potato_get_text_before_cursor()

  # Get text after and including the selection.
  text_after = actions.user.textflow_potato_get_text_after_cursor()

  # Restore the selection.
  for _ in range(len(selected_text)):
    actions.edit.extend_right()

  # Compute selected range.
  selection_range = tf.TextRange(len(text_before), len(text_before) + len(selected_text))

  return TextFlowContext(text_before + text_after, selection_range, potato_mode=True)


def _get_context() -> TextFlowContext:
  """Gets context for TextFlow to act in."""
  # Go straight to Potato mode if it is being forced.
  if actions.user.textflow_force_potato_mode():
    return _get_context_potato_mode()

  # Check if we need to enable enhanced UI for the active app. Allows us to access some Electron apps (such as VS Code)
  # through the accessibility API.
  curr_app = ui.active_window().app
  if curr_app.bundle in _ENHANCED_UI_BUNDLES:
    if not curr_app.element.AXEnhancedUserInterface:
      # Display friendly message to user and log full app details.
      actions.app.notify(f"Enabling enhanced UI for {curr_app.name}")
      print(f"TextFlow: Enabling AXEnhancedUserInterface for app: {curr_app}")
      # Enable enhanced UI.
      curr_app.element.AXEnhancedUserInterface = True
      # Pause for UI to update before we try to access the focused element.
      actions.sleep("500ms")

  # Short pause to make textflow commands more chainable. Allows UI to update from previous commands.
  actions.sleep("20ms")

  # Try to get the focused element. If we can't, we'll fallback to potato mode.
  focused_element = None
  try:
    focused_element = ui.focused_element()
  except RuntimeError:
    print("TextFlow: Unable to get focused element. Falling back to potato mode.")
    return _get_context_potato_mode()

  # Make sure we have a focused element with the required text editing attributes.
  if ("AXValue" not in focused_element.attrs or "AXSelectedText" not in focused_element.attrs or
      "AXSelectedTextRange" not in focused_element.attrs):
    print("TextFlow: Missing required accessibility API attributes. Falling back to potato mode.")
    return _get_context_potato_mode()

  # Try to get the remaining required data. Log a warning and fallback to potato mode if we can't.
  try:
    text: str = focused_element.AXValue
    selection_span: types.span.Span = focused_element.AXSelectedTextRange
    selected_text: str = focused_element.AXSelectedText
  except AttributeError:
    print("TextFlow: Unable to get attribute values from focused element. Falling back to potato mode.")
    return _get_context_potato_mode()

  # Special case encountered in Google Docs: AX attributes are present, but text is just a single special character.
  if text == "\xa0":
    print("TextFlow: Encountered Google Docs special case. Falling back to potato mode.")
    return _get_context_potato_mode()

  # Accessibility APIs appear to have a character limit. If we are approaching or beyond that limit, switch to potato
  # mode.
  if (len(text) == _MAX_ACCESSIBLITY_API_CHARS and
      selection_span.right > _MAX_ACCESSIBLITY_API_CHARS - _MIN_CHARS_AFTER_ACCESSIBLITY_API_LIMIT):
    print("TextFlow: Hit accessibility API character limit. Falling back to potato mode.")
    return _get_context_potato_mode()

  # Convert selection to text range.
  selection_range = tf.TextRange(selection_span.left, selection_span.right)

  # Sanity check: Make sure selected text matches text + selection range.
  if len(selected_text) != selection_range.length():
    raise ValueError(
        f"Unexpected selected text length. Expected: {selection_range.length()}, Actual: {len(selected_text)}")

  return TextFlowContext(text, selection_range, editor_element=focused_element)


def _execute_editor_actions_potato_mode(editor_actions: list[tf.EditorAction], context: TextFlowContext):
  """Executes a set of editor actions in potato mode, given a textflow context."""
  # Convert the actions to potato mode.
  potato_actions = textflow_potato.convert_actions_to_potato_mode(editor_actions, context.text, context.selection_range)

  for action in potato_actions:
    for _ in range(0, action.repeat):
      # Some actions require a text argument.
      if action.action_type in (textflow_potato.PotatoEditorActionType.INSERT_TEXT,
                                textflow_potato.PotatoEditorActionType.SET_CLIPBOARD_WITH_HISTORY,
                                textflow_potato.PotatoEditorActionType.SET_CLIPBOARD_NO_HISTORY):
        _POTATO_INPUT_ACTIONS_BY_TYPE[action.action_type](action.text)
      else:
        _POTATO_INPUT_ACTIONS_BY_TYPE[action.action_type]()


def _execute_editor_actions(editor_actions: list[tf.EditorAction], context: TextFlowContext):
  """Executes a set of editor actions, given a textflow context."""
  # Execute in potato mode if necessary.
  if context.potato_mode:
    _execute_editor_actions_potato_mode(editor_actions, context)
    return

  for action in editor_actions:
    if action.action_type == tf.EditorActionType.CLEAR:
      actions.edit.delete()
    elif action.action_type == tf.EditorActionType.INSERT_TEXT:
      actions.user.insert_via_clipboard(action.text)
    elif action.action_type == tf.EditorActionType.SET_CLIPBOARD_NO_HISTORY:
      actions.clip.set_text(action.text)
    elif action.action_type == tf.EditorActionType.SET_CLIPBOARD_WITH_HISTORY:
      actions.user.clipboard_history_set_text(action.text)
    elif action.action_type == tf.EditorActionType.SET_SELECTION_RANGE:
      if action.text_range is None:
        raise ValueError("Set selection range action with missing range.")
      if context.editor_element is None:
        raise ValueError("Element missing for accessibility API action.")
      select_span = types.span.Span(action.text_range.start + context.text_offset,
                                    action.text_range.end + context.text_offset)

      context.editor_element.AXSelectedTextRange = select_span
    elif action.action_type == tf.EditorActionType.GO_LINE_START:
      actions.edit.line_start()
    elif action.action_type == tf.EditorActionType.GO_LINE_END:
      actions.edit.line_end()

    # Sleep to let the UI catch up to the commands.
    actions.sleep("50ms")


def _run_command(command: tf.Command):
  """Runs the given command and executes the resulting input actions."""
  # Get the text we are acting on, along with other context information.
  context = _get_context()

  # Collect required utility function.
  utility_functions = tf.UtilityFunctions(actions.user.get_all_homophones, actions.user.get_next_homophone)

  # Run the command.
  editor_actions = textflow.run_command(command, context.text, context.selection_range, utility_functions)

  # Execute the editor actions.
  _execute_editor_actions(editor_actions, context)


def _capture_to_words(m) -> list[str]:
  """Convert a capture to a list of words."""
  words = []
  for item in m:
    if isinstance(item, grammar.vm.Phrase):
      words.extend(actions.dictate.replace_words(actions.dictate.parse_words(item)))
    else:
      words.extend(item.split(" "))
  return words


@mod.capture(rule="{self.textflow_command_type}")
def textflow_command_type(m) -> tf.CommandType:
  """Maps a spoken command to the command type."""
  return _COMMAND_TYPES_BY_SPOKEN[m.textflow_command_type]


@mod.capture(rule="{self.textflow_single_word_command_type}")
def textflow_single_word_command_type(m) -> tf.CommandType:
  """Maps a spoken command to the single-word command type."""
  return _SINGLE_WORD_COMMAND_TYPES_BY_SPOKEN[m.textflow_single_word_command_type]


@mod.capture(rule="{self.textflow_search_direction}")
def textflow_search_direction(m) -> tf.SearchDirection:
  """Maps a spoken search direction to the direction enum."""
  return _SEARCH_DIRECTION_BY_SPOKEN[m.textflow_search_direction]


@mod.capture(rule="{self.textflow_target_combo_type}")
def textflow_target_combo_type(m) -> tf.TargetCombinationType:
  """Maps a spoken target combo type to the enum."""
  return _TARGET_COMBO_TYPE_BY_SPOKEN[m.textflow_target_combo_type]


@mod.capture(rule="(<user.symbol_key> | <user.letters> | <user.dictate_number>)+")
def textflow_substring(m) -> str:
  """A substring textflow target specifier."""
  return "".join(_capture_to_words(m))


@mod.capture(rule="phrase <phrase>")
def textflow_phrase(m) -> str:
  """A phrase textflow target specifier."""
  return " ".join(_capture_to_words(m.phrase))


@mod.capture(rule="[<user.ordinals_small>] [<user.textflow_search_direction>] " +
             "(<user.textflow_substring> | <user.textflow_phrase> | token)")
def textflow_simple_target(m) -> tf.SimpleTarget:
  """A textflow simple target."""
  try:
    nth = m.ordinals_small
  except AttributeError:
    nth = 1

  try:
    direction = m.textflow_search_direction
  except AttributeError:
    direction = None

  try:
    return tf.SimpleTarget(tf.TokenMatchOptions(nth_match=nth, search=m.textflow_substring), direction)
  except AttributeError:
    pass

  try:
    return tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, nth_match=nth, search=m.textflow_phrase),
                           direction)
  except AttributeError:
    pass

  return tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.TOKEN_COUNT, nth_match=nth), direction)


@mod.capture(rule="[<user.ordinals_small>] [<user.textflow_search_direction>] <user.word>")
def textflow_word(m) -> tf.CompoundTarget:
  """A textflow target matching a single word with homophones."""
  try:
    nth = m.ordinals_small
  except AttributeError:
    nth = 1

  try:
    direction = m.textflow_search_direction
  except AttributeError:
    direction = None

  return tf.CompoundTarget(
      tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, nth_match=nth, search=m.word), direction))


@mod.capture(rule="<user.textflow_simple_target> [<user.textflow_target_combo_type> <user.textflow_simple_target>]")
def textflow_compound_target(m) -> tf.CompoundTarget:
  """A textflow compound target."""
  from_target = m.textflow_simple_target_list[0]
  if len(m.textflow_simple_target_list) > 1:
    to_target = m.textflow_simple_target_list[1]
    combo_type = m.textflow_target_combo_type
  else:
    to_target = None
    combo_type = tf.TargetCombinationType.PAST_TO

  return tf.CompoundTarget(from_target, to_target, combo_type)


@mod.action_class
class Actions:
  """Textflow actions."""

  def textflow_get_selected_text_potato_mode() -> str:
    """Gets the selected text. For editors that copy/cut the current line when nothing is selected, this should be
    overridden to return an empty string. Otherwise, most textflow commands will not work for targets after the
    cursor."""
    return actions.edit.selected_text()

  def textflow_force_potato_mode() -> bool:
    """Returns whether to require potato mode even if the accessibility API is available. Required in some apps
    that do not properly implement the accessibility API."""
    return False

  def textflow_execute_command(command_type: tf.CommandType,
                               target_from: tf.CompoundTarget,
                               target_to: Optional[tf.CompoundTarget] = None):
    """"Execute a textflow command."""
    command = tf.Command(command_type, target_from, target_to)
    _run_command(command)

  def textflow_execute_line_command(command_type: tf.CommandType, simple_target: tf.SimpleTarget):
    """"Execute a textflow command on a line."""
    simple_target.match_options.match_method = tf.TokenMatchMethod.LINE_START
    target_from = tf.CompoundTarget(simple_target, modifier=tf.Modifier(tf.ModifierType.LINE))
    command = tf.Command(command_type, target_from)
    _run_command(command)

  def textflow_execute_command_from_cursor(command_type: tf.CommandType, combo_type: tf.TargetCombinationType,
                                           simple_target: tf.SimpleTarget):
    """"Executes a textflow command using the cursor as the first simple target."""
    compound_target = tf.CompoundTarget(target_to=simple_target, target_combo=combo_type)
    command = tf.Command(command_type, compound_target)
    _run_command(command)

  def textflow_execute_command_current_block(command_type: tf.CommandType):
    """"Executes a textflow command on the current block."""
    target_from = tf.CompoundTarget(modifier=tf.Modifier(tf.ModifierType.BLOCK))
    command = tf.Command(command_type, target_from)
    _run_command(command)

  def textflow_replace(target_from: tf.CompoundTarget, prose: str):
    """"Executes a textflow replace command."""
    command = tf.Command(tf.CommandType.REPLACE, target_from, insert_text=prose)
    _run_command(command)

  def textflow_replace_word(target_from: tf.CompoundTarget, word: str):
    """"Executes a textflow replace word command, matching original case."""
    command = tf.Command(tf.CommandType.REPLACE_WORD_MATCH_CASE, target_from, insert_text=word)
    _run_command(command)

  def textflow_new_line_above(simple_target: tf.SimpleTarget):
    """Inserts a new line above the given target and moves the cursor to it."""
    target_from = tf.CompoundTarget(simple_target)
    command = tf.Command(tf.CommandType.MOVE_CURSOR_BEFORE, target_from)
    _run_command(command)

    # Make this work in vscode if there is leading white space.
    actions.edit.line_end()
    actions.edit.line_start()
    actions.edit.line_start()
    actions.key("enter")
    actions.key("up")

  def textflow_new_line_below(simple_target: tf.SimpleTarget):
    """Inserts a new line below the given target and moves the cursor to it."""
    target_from = tf.CompoundTarget(simple_target)
    command = tf.Command(tf.CommandType.MOVE_CURSOR_AFTER, target_from)
    _run_command(command)
    actions.edit.line_insert_down()

  def textflow_segment_word(word1: str, word2: str):
    """Segment a word into two. e.g. overmatched->over matched."""
    target_from = tf.CompoundTarget(
        tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, search=word1 + word2)))
    command = tf.Command(tf.CommandType.REPLACE, target_from, insert_text=f"{word1} {word2}")
    _run_command(command)

  def textflow_join_words(word1: str, word2: str):
    """Joins two words into one. e.g. base ball->baseball."""
    target_from = tf.CompoundTarget(
        tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, search=f"{word1} {word2}")))
    command = tf.Command(tf.CommandType.JOIN_WORDS, target_from)
    _run_command(command)

  def textflow_hyphenate_words(word1: str, word2: str):
    """Hyphenates two words. e.g. base ball->base-ball."""
    target_from = tf.CompoundTarget(
        tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, search=f"{word1} {word2}")))
    command = tf.Command(tf.CommandType.HYPHENATE_WORDS, target_from)
    _run_command(command)

  def textflow_swap_exact_words(from_word: str, to_word: str, nth_match: int = 1, search_direction: str = ""):
    """Swaps one word for another, using exact match."""
    search_direction_enum = None
    if search_direction is not None and search_direction != "":
      search_direction_enum = _SEARCH_DIRECTION_BY_SPOKEN[search_direction]
    target_from = tf.CompoundTarget(
        tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.EXACT_WORD, search=from_word, nth_match=nth_match),
                        search_direction_enum))
    command = tf.Command(tf.CommandType.REPLACE_WORD_MATCH_CASE, target_from, insert_text=to_word)
    _run_command(command)

  def textflow_delete_exact_word(word: str, nth_match: int = 1, search_direction: str = ""):
    """Deletes the given word."""
    search_direction_enum = None
    if search_direction is not None and search_direction != "":
      search_direction_enum = _SEARCH_DIRECTION_BY_SPOKEN[search_direction]
    target_from = tf.CompoundTarget(
        tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.EXACT_WORD, search=word, nth_match=nth_match),
                        search_direction_enum))
    command = tf.Command(tf.CommandType.CLEAR_NO_MOVE, target_from)
    _run_command(command)

  def textflow_potato_get_text_before_cursor():
    """"Get text before the cursor for use in textflow potato mode. Can be overridden in apps that have unusual text
    selection behavior."""
    # Select a few lines above the cursor.
    for _ in range(0, _POTATO_LINES_BEFORE):
      actions.edit.extend_up()
    actions.edit.extend_line_start()

    result = actions.edit.selected_text()
    if len(result) > 0:
      actions.edit.right()
    return result

  def textflow_potato_get_text_after_cursor():
    """"Get text after the cursor for use in textflow potato mode. Can be overridden in apps that have unusual text
    selection behavior."""
    # Select a few lines below the cursor.
    for _ in range(0, _POTATO_LINES_AFTER):
      actions.edit.extend_down()
    actions.edit.extend_line_end()

    result = actions.edit.selected_text()
    if len(result) > 0:
      actions.edit.left()
    return result
