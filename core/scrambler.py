"""Definition of scambler actions and default implementations."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, clip, types, ui
from .lib import scrambler_potato, scrambler_run, scrambler_types as st
from .scrambler_captures import ScramblerMatch

mod = Module()
ctx = Context()

# Whether to log all commands run for debugging.
_LOG_COMMANDS = True

# Accessibility APIs appear to be limited to this many characters.
_MAX_ACCESSIBLITY_API_CHARS = 10000

# Require at least this many characters after the selection before the accessibility API limit.
_MIN_CHARS_AFTER_ACCESSIBLITY_API_LIMIT = 1000

# Lines to fetch in potato mode.
_POTATO_LINES_BEFORE = 25
_POTATO_LINES_AFTER = 10

# Input action functions keyed by potato action type.
_POTATO_INPUT_ACTIONS_BY_TYPE = {
    scrambler_potato.PotatoEditorActionType.GO_UP:
        actions.user.up,
    scrambler_potato.PotatoEditorActionType.GO_DOWN:
        actions.user.down,
    scrambler_potato.PotatoEditorActionType.GO_LEFT:
        actions.user.left,
    scrambler_potato.PotatoEditorActionType.GO_RIGHT:
        actions.user.right,
    scrambler_potato.PotatoEditorActionType.GO_WORD_LEFT:
        actions.user.word_left,
    scrambler_potato.PotatoEditorActionType.GO_WORD_RIGHT:
        actions.user.word_right,
    scrambler_potato.PotatoEditorActionType.GO_LINE_START:
        actions.user.line_start,
    scrambler_potato.PotatoEditorActionType.GO_LINE_END:
        actions.user.line_end,
    scrambler_potato.PotatoEditorActionType.EXTEND_UP:
        actions.user.extend_up,
    scrambler_potato.PotatoEditorActionType.EXTEND_DOWN:
        actions.user.extend_down,
    scrambler_potato.PotatoEditorActionType.EXTEND_LEFT:
        actions.user.extend_left,
    scrambler_potato.PotatoEditorActionType.EXTEND_RIGHT:
        actions.user.extend_right,
    scrambler_potato.PotatoEditorActionType.EXTEND_WORD_LEFT:
        actions.user.extend_word_left,
    scrambler_potato.PotatoEditorActionType.EXTEND_WORD_RIGHT:
        actions.user.extend_word_right,
    scrambler_potato.PotatoEditorActionType.EXTEND_LINE_START:
        actions.user.extend_line_start,
    scrambler_potato.PotatoEditorActionType.EXTEND_LINE_END:
        actions.user.extend_line_end,
    scrambler_potato.PotatoEditorActionType.CLEAR:
        actions.user.delete,
    scrambler_potato.PotatoEditorActionType.INSERT_TEXT:
        actions.user.insert_via_clipboard,
    scrambler_potato.PotatoEditorActionType.SET_CLIPBOARD_WITH_HISTORY:
        actions.user.clipboard_history_set_text,
    scrambler_potato.PotatoEditorActionType.SET_CLIPBOARD_NO_HISTORY:
        actions.clip.set_text,
}

# App bundles we enable AXEnhancedUserInterface for.
_ENHANCED_UI_BUNDLES = [
    "com.microsoft.VSCode", "com.microsoft.VSCodeInsiders", "com.visualstudio.code.oss",
    "md.obsidian"
]


def _get_context_potato_mode() -> st.Context:
  """Gets scrambler context in potato mode."""
  # Check if we already have a selection.
  # Note: Editors that copy the entire line when nothing is selected should override this action to
  # return an empty string. Otherwise, many actions in scrambler will break, especially for targets
  # after the cursor.
  selected_text = actions.user.scrambler_get_selected_text_potato_mode()

  # Collapse selection if necessary.
  if len(selected_text) > 0:
    actions.user.left()

  # Do not preserve the selection if it is long. Long selections are usually not useful in scrambler
  # and they can make a potato-mode command execute very slowly.
  if len(selected_text) > 150:  # Around the length of a very long line.
    selected_text = ""

  # Get text before the selection.
  text_before = actions.user.scrambler_potato_get_text_before_cursor()

  # Get text after and including the selection.
  text_after = actions.user.scrambler_potato_get_text_after_cursor()

  # Restore the selection.
  for _ in range(len(selected_text)):
    actions.user.extend_right()

  # Compute selected range.
  selection_range = st.TextRange(len(text_before), len(text_before) + len(selected_text))

  return st.Context(text_before + text_after, selection_range, potato_mode=True)


def _get_context() -> st.Context:
  """Gets context for scrambler to act in."""
  # Go straight to Potato mode if it is being forced.
  if actions.user.scrambler_force_potato_mode():
    return _get_context_potato_mode()

  # Check if we need to enable enhanced UI for the active app. Allows us to access some Electron
  # apps (such as VS Code) through the accessibility API.
  curr_app = ui.active_window().app
  if curr_app.bundle in _ENHANCED_UI_BUNDLES:
    if not curr_app.element.AXEnhancedUserInterface:
      # Display friendly message to user and log full app details.
      actions.app.notify(f"Enabling enhanced UI for {curr_app.name}")
      print(f"Scrambler: Enabling AXEnhancedUserInterface for app: {curr_app}")
      # Enable enhanced UI.
      try:
        curr_app.element.AXEnhancedUserInterface = True
      except ui.UIErr:
        # This can throw an exception but still succeed in enabling enhanced UI.
        pass
      # Pause for UI to update before we try to access the focused element.
      actions.sleep("500ms")

  # Short pause to make scrambler commands more chainable. Allows UI to update from previous
  # commands.
  actions.sleep("20ms")

  # Try to get the focused element. If we can't, we'll fallback to potato mode.
  focused_element = None
  try:
    focused_element = ui.focused_element()
  except RuntimeError:
    print("Scrambler: Unable to get focused element. Falling back to potato mode.")
    return _get_context_potato_mode()

  # Make sure we have a focused element with the required text editing attributes.
  if ("AXValue" not in focused_element.attrs or "AXSelectedText" not in focused_element.attrs or
      "AXSelectedTextRange" not in focused_element.attrs):
    print("Scrambler: Missing required accessibility API attributes. Falling back to potato mode.")
    return _get_context_potato_mode()

  # Try to get the remaining required data. Log a warning and fallback to potato mode if we can't.
  try:
    text: str = focused_element.AXValue
    selection_span: types.span.Span = focused_element.AXSelectedTextRange
    selected_text: str = focused_element.AXSelectedText
  except AttributeError:
    print("Scrambler: Unable to get attribute values from focused element. "
          "Falling back to potato mode.")
    return _get_context_potato_mode()

  # Special case encountered in Google Docs: AX attributes are present, but text is just a single
  # special character.
  if text == "\xa0":
    print("Scrambler: Encountered Google Docs special case. Falling back to potato mode.")
    return _get_context_potato_mode()

  # Accessibility APIs appear to have a character limit. If we are approaching or beyond that limit,
  # switch to potato mode.
  if (len(text) == _MAX_ACCESSIBLITY_API_CHARS and
      selection_span.right > _MAX_ACCESSIBLITY_API_CHARS - _MIN_CHARS_AFTER_ACCESSIBLITY_API_LIMIT):
    print("Scrambler: Hit accessibility API character limit. Falling back to potato mode.")
    return _get_context_potato_mode()

  # Convert selection to text range.
  selection_range = st.TextRange(selection_span.left, selection_span.right)

  # Sanity check: Make sure selected text matches text + selection range.
  if len(selected_text) != selection_range.length():
    raise ValueError("Unexpected selected text length. "
                     f"Expected: {selection_range.length()}, Actual: {len(selected_text)}")

  return st.Context(text, selection_range, potato_mode=False, editor_element=focused_element)


def _execute_editor_actions_potato_mode(editor_actions: list[st.EditorAction], context: st.Context):
  """Executes a set of editor actions in potato mode, given a scrambler context."""
  # Convert the actions to potato mode.
  potato_actions = scrambler_potato.convert_actions_to_potato_mode(editor_actions, context.text,
                                                                   context.selection_range)

  for action in potato_actions:
    for _ in range(0, action.repeat):
      # Some actions require a text argument.
      if action.action_type in (scrambler_potato.PotatoEditorActionType.INSERT_TEXT,
                                scrambler_potato.PotatoEditorActionType.SET_CLIPBOARD_WITH_HISTORY,
                                scrambler_potato.PotatoEditorActionType.SET_CLIPBOARD_NO_HISTORY):
        _POTATO_INPUT_ACTIONS_BY_TYPE[action.action_type](action.text)
      else:
        _POTATO_INPUT_ACTIONS_BY_TYPE[action.action_type]()


def _execute_editor_actions(editor_actions: list[st.EditorAction], context: st.Context):
  """Executes a set of editor actions, given a scrambler context."""
  # Execute in potato mode if necessary.
  if context.potato_mode:
    _execute_editor_actions_potato_mode(editor_actions, context)
    return

  for action in editor_actions:
    if action.action_type == st.EditorActionType.INSERT_TEXT:
      actions.user.scrambler_insert_text_action(action, context)
    elif action.action_type == st.EditorActionType.SET_CLIPBOARD_NO_HISTORY:
      actions.clip.set_text(action.text)
    elif action.action_type == st.EditorActionType.SET_CLIPBOARD_WITH_HISTORY:
      actions.user.clipboard_history_set_text(action.text)
    elif action.action_type == st.EditorActionType.SET_SELECTION_RANGE:
      if action.text_range is None:
        raise ValueError("Set selection range action with missing range.")
      actions.user.scrambler_set_selection_action(action, context)
    elif action.action_type == st.EditorActionType.DELETE_RANGE:
      if action.text_range is None:
        raise ValueError("Delete range action with missing range.")
      actions.user.scrambler_delete_range_action(action, context)

    # Sleep to let the UI catch up to the commands.
    actions.sleep("50ms")


def _run_command(command: st.Command):
  """Runs the given command and executes the resulting input actions."""
  context = actions.user.scrambler_get_context()
  if _LOG_COMMANDS:
    print(f"Scrambler command: {command}")
    print(f"Scrambler context: {context}")
  utility_functions = st.UtilityFunctions(actions.user.get_all_homophones,
                                          actions.user.get_next_homophone)
  editor_actions = scrambler_run.run_command(command, context.text, context.selection_range,
                                             utility_functions)
  if _LOG_COMMANDS:
    print(f"Scrambler editor actions: {editor_actions}")
  _execute_editor_actions(editor_actions, context)


@mod.action_class
class Actions:
  """Scrambler actions."""

  def scrambler_get_scope_modifier() -> st.ModifierType:
    """Gets the current scope modifier type."""
    # Default to C-style scopes.
    return st.ModifierType.C_SCOPE

  def scrambler_get_selected_text_potato_mode() -> str:
    """Gets the selected text. For editors that copy/cut the current line when nothing is selected,
    this should be overridden to return an empty string. Otherwise, most scrambler commands will not
    work for targets after the cursor."""
    return actions.user.selected_text()

  def scrambler_force_potato_mode() -> bool:
    """Returns whether to require potato mode even if the accessibility API is available. Required
    in some apps that do not properly implement the accessibility API."""
    return False

  def scrambler_potato_get_text_before_cursor():
    """"Get text before the cursor for use in potato mode. Can be overridden in apps that
    have unusual text selection behavior."""
    # Select a few lines above the cursor.
    for _ in range(0, _POTATO_LINES_BEFORE):
      actions.user.extend_up()
    actions.user.extend_line_start()

    result = actions.user.selected_text()
    if len(result) > 0:
      actions.user.right()
    return result

  def scrambler_potato_get_text_after_cursor():
    """"Get text after the cursor for use in potato mode. Can be overridden in apps that
    have unusual text selection behavior."""
    # Select a few lines below the cursor.
    for _ in range(0, _POTATO_LINES_AFTER):
      actions.user.extend_down()
    actions.user.extend_line_end()

    result = actions.user.selected_text()
    if len(result) > 0:
      actions.user.left()
    return result

  def scrambler_get_context() -> st.Context:
    """Gets the context for scrambler to act in. Can be overwritten in apps with accessibility
    extensions. If this is overwritten, `potato_mode` in the result supercedes the
    `scrambler_force_potato_mode` action."""
    return _get_context()

  def scrambler_set_selection_action(editor_action: st.EditorAction, context: st.Context):
    """Sets the selection in an editor, given a context."""
    if editor_action.text_range is None:
      raise ValueError("Set selection range action with missing range.")
    if context.editor_element is None:
      raise ValueError("Element missing for accessibility API action.")
    select_span = types.span.Span(editor_action.text_range.start + context.text_offset,
                                  editor_action.text_range.end + context.text_offset)
    context.editor_element.AXSelectedTextRange = select_span

  def scrambler_delete_range_action(editor_action: st.EditorAction, context: st.Context):
    """Deletes a text range in an editor, given a context."""
    if editor_action.text_range is None:
      raise ValueError("Delete range action with missing range.")
    actions.user.scrambler_set_selection_action(editor_action, context)
    actions.user.delete()

  def scrambler_insert_text_action(editor_action: st.EditorAction, context: st.Context):
    """Inserts the given text in an editor."""
    del context
    actions.user.insert_via_clipboard(editor_action.text)

  def scrambler_run_command(command_type: st.CommandType, match: ScramblerMatch):
    """Runs the given command."""
    command = st.Command(command_type, match.modifiers, match.extend_modifiers,
                         match.combination_type)
    _run_command(command)

  def scrambler_run_select_command(match: ScramblerMatch):
    """Runs a selection command on the given match."""
    command = st.Command(st.CommandType.SELECT, match.modifiers, match.extend_modifiers,
                         match.combination_type)
    _run_command(command)

  def scrambler_move_argument_left():
    """Moves the current argument to the left."""
    # Use a scrambler command to capture and delete the argument.
    command = st.Command(st.CommandType.CUT_TO_CLIPBOARD, [st.Modifier(st.ModifierType.ARGUMENT)])
    with clip.capture() as s:
      _run_command(command)
    try:
      argument = s.text()
    except clip.NoChange as exc:
      raise ValueError("No argument captured") from exc
    if not argument:
      raise ValueError("Argument is empty")

    # Move before the argument that is now under the cursor.
    command = st.Command(st.CommandType.MOVE_CURSOR_BEFORE, [st.Modifier(st.ModifierType.ARGUMENT)])
    _run_command(command)

    # Re-insert the deleted argument.
    actions.user.insert_via_clipboard(argument + ", ")

  def scrambler_move_argument_right():
    # Use a scrambler command to capture and delete the argument.
    command = st.Command(st.CommandType.CUT_TO_CLIPBOARD, [st.Modifier(st.ModifierType.ARGUMENT)])
    with clip.capture() as s:
      _run_command(command)
    try:
      argument = s.text()
    except clip.NoChange as exc:
      raise ValueError("No argument captured") from exc
    if not argument:
      raise ValueError("Argument is empty")

    # The argument modifier prefers to delete leading commas instead of trailing ones, so we need
    # to move right to get to the next argument. This causes odd behavior if the cursor is already
    # in the rightmost argument, but it allows moving arguments that aren't the leftmost.
    actions.key("right")

    # Move after the argument that is now under the cursor.
    command = st.Command(st.CommandType.MOVE_CURSOR_AFTER, [st.Modifier(st.ModifierType.ARGUMENT)])
    _run_command(command)

    # Re-insert the deleted argument.
    actions.user.insert_via_clipboard(", " + argument)
