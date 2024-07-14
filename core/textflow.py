"""Definition of textflow actions and default (potato mode) implementations."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from dataclasses import dataclass
from typing import Optional
from talon import Context, Module, actions, grammar, types, ui
from .lib import number_util, textflow, textflow_potato
from .lib import textflow_types as tf

mod = Module()
ctx = Context()

_COMMAND_TYPES_BY_SPOKEN = {
    "pick": tf.CommandType.SELECT,
    "before": tf.CommandType.MOVE_CURSOR_BEFORE,
    "after": tf.CommandType.MOVE_CURSOR_AFTER,
    "bring": tf.CommandType.BRING,
    "chuck": tf.CommandType.CLEAR_NO_MOVE,
    "change": tf.CommandType.CLEAR_MOVE_CURSOR,
    "phony": tf.CommandType.NEXT_HOMOPHONE,
    "bigger": tf.CommandType.TITLE_CASE,
    "biggest": tf.CommandType.UPPERCASE,
    "smaller": tf.CommandType.LOWERCASE,
}
mod.list("textflow_command_type", desc="Text navigation command types")
ctx.lists["self.textflow_command_type"] = _COMMAND_TYPES_BY_SPOKEN.keys()

# Commands that act on a single word.
_SINGLE_WORD_COMMAND_TYPES_BY_SPOKEN = {
    "grab": tf.CommandType.SELECT,
    "before": tf.CommandType.MOVE_CURSOR_BEFORE,
    "after": tf.CommandType.MOVE_CURSOR_AFTER,
    "bring": tf.CommandType.BRING,
    "junker": tf.CommandType.CLEAR_NO_MOVE,
    "change": tf.CommandType.CLEAR_MOVE_CURSOR,
    "phony": tf.CommandType.NEXT_HOMOPHONE,
    "bigger": tf.CommandType.TITLE_CASE,
    "biggest": tf.CommandType.UPPERCASE,
    "smaller": tf.CommandType.LOWERCASE,
}
mod.list("textflow_single_word_command_type", desc="Text navigation command types that act on a single word")
ctx.lists["self.textflow_single_word_command_type"] = _SINGLE_WORD_COMMAND_TYPES_BY_SPOKEN.keys()

_SEARCH_DIRECTION_BY_SPOKEN = {
    "next": tf.SearchDirection.FORWARD,
    "last": tf.SearchDirection.BACKWARD,
    # Common misrecognition of "last".
    "lust": tf.SearchDirection.BACKWARD,
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
    textflow_potato.PotatoEditorActionType.GO_UP: actions.user.up,
    textflow_potato.PotatoEditorActionType.GO_DOWN: actions.user.down,
    textflow_potato.PotatoEditorActionType.GO_LEFT: actions.user.left,
    textflow_potato.PotatoEditorActionType.GO_RIGHT: actions.user.right,
    textflow_potato.PotatoEditorActionType.GO_WORD_LEFT: actions.user.word_left,
    textflow_potato.PotatoEditorActionType.GO_WORD_RIGHT: actions.user.word_right,
    textflow_potato.PotatoEditorActionType.GO_LINE_START: actions.user.line_start,
    textflow_potato.PotatoEditorActionType.GO_LINE_END: actions.user.line_end,
    textflow_potato.PotatoEditorActionType.EXTEND_UP: actions.user.extend_up,
    textflow_potato.PotatoEditorActionType.EXTEND_DOWN: actions.user.extend_down,
    textflow_potato.PotatoEditorActionType.EXTEND_LEFT: actions.user.extend_left,
    textflow_potato.PotatoEditorActionType.EXTEND_RIGHT: actions.user.extend_right,
    textflow_potato.PotatoEditorActionType.EXTEND_WORD_LEFT: actions.user.extend_word_left,
    textflow_potato.PotatoEditorActionType.EXTEND_WORD_RIGHT: actions.user.extend_word_right,
    textflow_potato.PotatoEditorActionType.EXTEND_LINE_START: actions.user.extend_line_start,
    textflow_potato.PotatoEditorActionType.EXTEND_LINE_END: actions.user.extend_line_end,
    textflow_potato.PotatoEditorActionType.CLEAR: actions.user.delete,
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
  # Whether we are in potato mode. Defaults to true to make overriding `textflow_get_context` safe by default.
  # If `textflow_get_context` is overridden but `textflow_set_selection_action` is not, the non-potato default
  # implementation is likely to fail (e.g. the overridden context action may not populate `editor_element`).
  potato_mode: bool = True
  # The starting offset of `text` in the active editor. Used when we are not operating on the entire contents of the
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
    actions.user.left()

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
    actions.user.extend_right()

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
      try:
        curr_app.element.AXEnhancedUserInterface = True
      except ui.UIErr:
        # This can throw an exception but still succeed in enabling enhanced UI.
        pass
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

  return TextFlowContext(text, selection_range, potato_mode=False, editor_element=focused_element)


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
      actions.user.delete()
    elif action.action_type == tf.EditorActionType.INSERT_TEXT:
      actions.user.insert_via_clipboard(action.text)
    elif action.action_type == tf.EditorActionType.SET_CLIPBOARD_NO_HISTORY:
      actions.clip.set_text(action.text)
    elif action.action_type == tf.EditorActionType.SET_CLIPBOARD_WITH_HISTORY:
      actions.user.clipboard_history_set_text(action.text)
    elif action.action_type == tf.EditorActionType.SET_SELECTION_RANGE:
      if action.text_range is None:
        raise ValueError("Set selection range action with missing range.")
      actions.user.textflow_set_selection_action(action, context)

    # Sleep to let the UI catch up to the commands.
    actions.sleep("50ms")


def _run_command(command: tf.Command):
  """Runs the given command and executes the resulting input actions."""
  # Get the text we are acting on, along with other context information.
  context = actions.user.textflow_get_context()

  # Collect required utility functions.
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


def _get_ordinal_and_search_direction(m):
  """Get the ordinal and search direction from a capture."""
  try:
    nth = m.ordinals_small
  except AttributeError:
    nth = 1

  try:
    direction = m.textflow_search_direction
  except AttributeError:
    direction = None

  return nth, direction


@mod.capture(rule="{self.textflow_command_type}")
def textflow_command_type(m) -> tf.CommandType:
  """Maps a spoken command to the command type."""
  return _COMMAND_TYPES_BY_SPOKEN[m.textflow_command_type]


@mod.capture(rule="{self.textflow_single_word_command_type}")
def textflow_single_word_command_type(m) -> tf.CommandType:
  """Maps a spoken command for a single to the command type."""
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
  nth, direction = _get_ordinal_and_search_direction(m)

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
  nth, direction = _get_ordinal_and_search_direction(m)
  return tf.CompoundTarget(
      tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, nth_match=nth, search=m.word), direction))


@mod.capture(rule="[<user.ordinals_small>] [<user.textflow_search_direction>] definite")
def textflow_definite(m) -> tf.CompoundTarget:
  """A textflow target matching the word "the"."""
  nth, direction = _get_ordinal_and_search_direction(m)
  return tf.CompoundTarget(
      tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.EXACT_WORD, nth_match=nth, search="the"), direction))


@mod.capture(rule="[<user.ordinals_small>] [<user.textflow_search_direction>] indefinite")
def textflow_indefinite(m) -> tf.CompoundTarget:
  """A textflow target matching the word "a"."""
  nth, direction = _get_ordinal_and_search_direction(m)
  return tf.CompoundTarget(
      tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.EXACT_WORD, nth_match=nth, search="a"), direction))


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
    return actions.user.selected_text()

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

  def textflow_execute_command_from_cursor(command_type: tf.CommandType, combo_type: tf.TargetCombinationType,
                                           simple_target: tf.SimpleTarget):
    """"Executes a textflow command using the cursor as the first simple target."""
    compound_target = tf.CompoundTarget(target_to=simple_target, target_combo=combo_type)
    command = tf.Command(command_type, compound_target)
    _run_command(command)

  def textflow_replace(target_from: tf.CompoundTarget, prose: str):
    """"Executes a textflow replace command."""
    command = tf.Command(tf.CommandType.REPLACE, target_from, insert_text=prose)
    _run_command(command)

  def textflow_replace_word(target_from: tf.CompoundTarget, word: str):
    """"Executes a textflow replace word command, matching original case."""
    command = tf.Command(tf.CommandType.REPLACE_WORD_MATCH_CASE, target_from, insert_text=word)
    _run_command(command)

  def textflow_execute_command_selection(command_type: tf.CommandType,
                                         modifier_type: tf.ModifierType = tf.ModifierType.NONE,
                                         delimiter: str = ""):
    """"Executes a textflow command on the current selection with an optional modifier."""
    command = tf.Command(command_type, tf.CompoundTarget(modifier=tf.Modifier(modifier_type, delimiter=delimiter)))
    _run_command(command)

  def textflow_modifier_type_from_string(modifier_type: str) -> tf.ModifierType:
    """Converts a string to a modifier type. "SCOPE" is a special modifier that gets the appropriate modifier for the
    current context."""
    result = tf.ModifierType.NONE
    if modifier_type:
      if modifier_type == "SCOPE":
        result = actions.user.textflow_get_scope_modifier()
      else:
        result = tf.ModifierType[modifier_type]
    return result

  def textflow_execute_command_enum_strings(command_type: str, modifier_type: str = "", delimiter: str = ""):
    """"Executes a textflow command on the current selection with an optional modifier. Uses string enum values."""
    effective_modifier_type = actions.user.textflow_modifier_type_from_string(modifier_type)
    actions.user.textflow_execute_command_selection(tf.CommandType[command_type], effective_modifier_type, delimiter)

  def textflow_get_scope_modifier() -> tf.ModifierType:
    """Gets the current scope modifier type."""
    # Default to Python-style scopes.
    return tf.ModifierType.PYTHON_SCOPE

  def textflow_move_argument_left():
    """Moves the current argument to the left."""
    actions.user.textflow_execute_command_selection(tf.CommandType.SELECT, tf.ModifierType.ARGUMENT)
    argument = actions.user.selected_text()
    if not argument:
      return
    actions.key("left")
    actions.user.textflow_execute_command_selection(tf.CommandType.CLEAR_NO_MOVE, tf.ModifierType.ARGUMENT)

    # Move before the argument that is now under the cursor.
    command = tf.Command(tf.CommandType.MOVE_CURSOR_BEFORE,
                         tf.CompoundTarget(modifier=tf.Modifier(tf.ModifierType.ARGUMENT)))
    _run_command(command)

    # Re-insert the deleted argument.
    actions.user.insert_via_clipboard(argument + ", ")

  def textflow_move_argument_right():
    """Moves the current argument to the right."""
    actions.user.textflow_execute_command_selection(tf.CommandType.SELECT, tf.ModifierType.ARGUMENT)
    argument = actions.user.selected_text()
    if not argument:
      return
    actions.key("left")
    actions.user.textflow_execute_command_selection(tf.CommandType.CLEAR_NO_MOVE, tf.ModifierType.ARGUMENT)

    # The modifier prefers to delete leading commas instead of trailing ones, so we need to move right to get to the
    # next argument. This causes odd behavior if the cursor is already in the rightmost argument, but it allows moving
    # arguments that aren't the leftmost.
    actions.key("right")

    # Move after the argument that is now under the cursor.
    command = tf.Command(tf.CommandType.MOVE_CURSOR_AFTER,
                         tf.CompoundTarget(modifier=tf.Modifier(tf.ModifierType.ARGUMENT)))
    _run_command(command)

    # Re-insert the deleted argument.
    actions.user.insert_via_clipboard(", " + argument)

  def textflow_new_line_above(simple_target: tf.SimpleTarget):
    """Inserts a new line above the given target and moves the cursor to it."""
    target_from = tf.CompoundTarget(simple_target)
    command = tf.Command(tf.CommandType.MOVE_CURSOR_BEFORE, target_from)
    _run_command(command)
    actions.user.line_insert_up()

  def textflow_new_line_below(simple_target: tf.SimpleTarget):
    """Inserts a new line below the given target and moves the cursor to it."""
    target_from = tf.CompoundTarget(simple_target)
    command = tf.Command(tf.CommandType.MOVE_CURSOR_AFTER, target_from)
    _run_command(command)
    actions.user.line_insert_down()

  def textflow_insert_line_below_current():
    """Inserts a line below the current line without moving the cursor to it."""
    target_from = tf.CompoundTarget(modifier=tf.Modifier(tf.ModifierType.END_OF_LINE))
    command = tf.Command(tf.CommandType.REPLACE, target_from, insert_text="\n")
    _run_command(command)

  def textflow_insert_line_above_current():
    """Inserts a line below the current line without moving the cursor to it."""
    target_from = tf.CompoundTarget(modifier=tf.Modifier(tf.ModifierType.START_OF_LINE))
    command = tf.Command(tf.CommandType.REPLACE, target_from, insert_text="\n")
    _run_command(command)

  def textflow_move_cursor_after_markdown_section(section_name: str):
    """Moves the cursor to the end of the given markdown section. Sections are separated by headings."""
    target_from = tf.CompoundTarget(tf.SimpleTarget(
        tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, search=f"# {section_name}\n")),
                                    modifier=tf.Modifier(tf.ModifierType.MARKDOWN_SECTION_END))
    command = tf.Command(tf.CommandType.MOVE_CURSOR_AFTER, target_from)
    _run_command(command)

  def textflow_swap_homophone_to_word(word: str):
    """Finds the nearest homophone for the given word and swaps it to the word."""
    # TODO: This will match the word itself and word substrings. Also add ordinal and search direction.
    target_from = tf.CompoundTarget(tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, search=word)))
    command = tf.Command(tf.CommandType.REPLACE, target_from, insert_text=word)
    _run_command(command)

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
    command = tf.Command(tf.CommandType.REPLACE_WITH_LAMBDA, target_from, lambda_func=lambda s: s.replace(" ", ""))
    _run_command(command)

  def textflow_hyphenate_words(word1: str, word2: str):
    """Hyphenates two words. e.g. base ball->base-ball."""
    target_from = tf.CompoundTarget(
        tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, search=f"{word1} {word2}")))
    command = tf.Command(tf.CommandType.REPLACE_WITH_LAMBDA, target_from, lambda_func=lambda s: s.replace(" ", "-"))
    _run_command(command)

  def textflow_words_to_digits(number_words: list[str]):
    """Find and convert a number written as words into digits. e.g. "one thousand and twenty five" -> "1025"."""
    if len(number_words) == 0:
      return
    number_string = number_util.parse_number(number_words)
    # If there is only one word, use an exact match. e.g. for "ten", we don't want to convert "tent" to "10".
    if len(number_words) == 1:
      target_from = tf.CompoundTarget(
          tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.EXACT_WORD, search=number_words[0])))
    else:
      target_from = tf.CompoundTarget(
          tf.SimpleTarget(tf.TokenMatchOptions(tf.TokenMatchMethod.PHRASE, search=" ".join(number_words))))
    command = tf.Command(tf.CommandType.REPLACE, target_from, insert_text=number_string)
    _run_command(command)

  def textflow_make_possessive(target_from: tf.CompoundTarget):
    """Converts a word to end in "'s". Uses existing trailing 's' if present. e.g. "dog" -> "dog's", "its" -> "it's"."""

    def _make_possessive(s: str) -> str:
      if s.endswith("'s"):
        return s
      if s.endswith("s"):
        return s[:-1] + "'" + s[-1:]
      return s + "'s"

    command = tf.Command(tf.CommandType.REPLACE_WITH_LAMBDA, target_from, lambda_func=_make_possessive)
    _run_command(command)

  def textflow_make_plural(target_from: tf.CompoundTarget):
    """Converts a word to end in "s". Uses existing trailing 's' if present. e.g. "dog" -> "dogs", "it" -> "it's"."""

    def _make_plural(s: str) -> str:
      if s.endswith("s"):
        return s
      return s + "s"

    command = tf.Command(tf.CommandType.REPLACE_WITH_LAMBDA, target_from, lambda_func=_make_plural)
    _run_command(command)

  def textflow_make_singular(target_from: tf.CompoundTarget):
    """Converts a word to not end in "s" or "'s". e.g. "dogs" -> "dog", "it's" -> "it"."""

    def _make_singular(s: str) -> str:
      if s.endswith("'s"):
        return s[:-2]
      if s.endswith("s"):
        return s[:-1]
      return s

    command = tf.Command(tf.CommandType.REPLACE_WITH_LAMBDA, target_from, lambda_func=_make_singular)
    _run_command(command)

  def textflow_select_nth_token(from_n: int, to_n: int = 0):
    """Selects the nth token from the current cursor position. from_n may be negative to search backwards.
    If to_n is 0, the selection will be a single token. If to_n is positive, the selection will be a range of tokens,
    and from_n may not be negative."""
    if from_n == 0:
      return
    if to_n > 0 and from_n < 0:
      raise ValueError("Negative from_n not allowed when to_n is positive.")
    if to_n > 0 and from_n >= to_n:
      raise ValueError("from_n must be less than to_n if to_n is provided.")
    if from_n > 0 and to_n > 0:
      target_from = tf.CompoundTarget(
          tf.SimpleTarget(tf.TokenMatchOptions(match_method=tf.TokenMatchMethod.TOKEN_COUNT, nth_match=from_n),
                          tf.SearchDirection.FORWARD),
          tf.SimpleTarget(tf.TokenMatchOptions(match_method=tf.TokenMatchMethod.TOKEN_COUNT, nth_match=to_n - from_n)))
    elif from_n > 0:
      target_from = tf.CompoundTarget(
          tf.SimpleTarget(tf.TokenMatchOptions(match_method=tf.TokenMatchMethod.TOKEN_COUNT, nth_match=from_n),
                          tf.SearchDirection.FORWARD))
    else:
      target_from = tf.CompoundTarget(
          tf.SimpleTarget(
              # pylint: disable=invalid-unary-operand-type
              tf.TokenMatchOptions(match_method=tf.TokenMatchMethod.TOKEN_COUNT, nth_match=-from_n),
              tf.SearchDirection.BACKWARD))
    command = tf.Command(tf.CommandType.SELECT, target_from)
    _run_command(command)

  def textflow_select_nth_modifier(n: int, modifier_type_string: str, delimiter: str = ""):
    """Selects the nth modifier from the current cursor position. n may be negative to search backwards."""
    if n == 0:
      return
    modifier_type = actions.user.textflow_modifier_type_from_string(modifier_type_string)
    command = tf.Command(tf.CommandType.SELECT,
                         tf.CompoundTarget(modifier=tf.Modifier(modifier_type, delimiter=delimiter, n=n)))
    _run_command(command)

  def textflow_select_nested_call():
    """Selects a function call nested in the current selected function call."""
    # Deselect the current selection to the left (start of the function call).
    if actions.user.selected_text():
      actions.key("left")

    # Move the cursor inside the next paren.
    command = tf.Command(
        tf.CommandType.MOVE_CURSOR_AFTER,
        tf.CompoundTarget(tf.SimpleTarget(tf.TokenMatchOptions(search="("), direction=tf.SearchDirection.FORWARD)))
    _run_command(command)

    # Select the next nested function call.
    command = tf.Command(tf.CommandType.SELECT, tf.CompoundTarget(modifier=tf.Modifier(tf.ModifierType.CALL_NEXT)))
    _run_command(command)

  def textflow_select_nested_brackets():
    """Selects the contents of brackets nested in the current selection."""
    # Deselect the current selection to the left.
    if actions.user.selected_text():
      actions.key("left")

    # Select the next nested brackets.
    command = tf.Command(tf.CommandType.SELECT, tf.CompoundTarget(modifier=tf.Modifier(tf.ModifierType.BRACKETS_FIRST)))
    _run_command(command)

  def textflow_surround_text(target_from: tf.CompoundTarget, before: str, after: Optional[str] = None):
    """Adds strings around a matched target. If `after` is None, it will be set to `before`."""
    if after is None:
      after = before
    command = tf.Command(tf.CommandType.REPLACE_WITH_LAMBDA, target_from, lambda_func=lambda s: f"{before}{s}{after}")
    _run_command(command)

  def textflow_potato_get_text_before_cursor():
    """"Get text before the cursor for use in textflow potato mode. Can be overridden in apps that have unusual text
    selection behavior."""
    # Select a few lines above the cursor.
    for _ in range(0, _POTATO_LINES_BEFORE):
      actions.user.extend_up()
    actions.user.extend_line_start()

    result = actions.user.selected_text()
    if len(result) > 0:
      actions.user.right()
    return result

  def textflow_potato_get_text_after_cursor():
    """"Get text after the cursor for use in textflow potato mode. Can be overridden in apps that have unusual text
    selection behavior."""
    # Select a few lines below the cursor.
    for _ in range(0, _POTATO_LINES_AFTER):
      actions.user.extend_down()
    actions.user.extend_line_end()

    result = actions.user.selected_text()
    if len(result) > 0:
      actions.user.left()
    return result

  def textflow_get_context() -> TextFlowContext:
    """Gets the context for TextFlow to act in. Can be overwritten in apps with accessibility extensions.
    If this is overwritten, `potato_mode` in the result supercedes the `textflow_force_potato_mode` action."""
    return _get_context()

  def textflow_set_selection_action(editor_action: tf.EditorAction, context: TextFlowContext):
    """Sets the selection in an editor, given a textflow context. Can be overwritten in apps with accessibility
    extensions."""
    if editor_action.text_range is None:
      raise ValueError("Set selection range action with missing range.")
    if context.editor_element is None:
      raise ValueError("Element missing for accessibility API action.")
    select_span = types.span.Span(editor_action.text_range.start + context.text_offset,
                                  editor_action.text_range.end + context.text_offset)
    context.editor_element.AXSelectedTextRange = select_span
