"""API for generating input actions to manipulate text in an editor."""

from .scrambler_commands import perform_command
from .scrambler_modifiers import apply_modifier
from .scrambler_types import Command, EditorAction, MatchCombinationType, TextMatch, TextRange, UtilityFunctions


def run_command(command: Command, text: str, selection_range: TextRange,
                utility_functions: UtilityFunctions) -> list[EditorAction]:
  """Runs a command for navigating and manipulating text."""
  # Start with the current selection range (or cursor position) and apply modifiers to it to get the
  # range of text we care about.
  match = TextMatch(selection_range)
  for modifier in command.modifiers:
    match = apply_modifier(text, match, modifier, utility_functions)

  # If there are any extension modifiers provided, we apply them to our current match, then extend
  # the current match to incorporate the result.
  if len(command.extend_modifiers) > 0:
    extend_match = match
    for modifier in command.extend_modifiers:
      extend_match = apply_modifier(text, extend_match, modifier, utility_functions)
    # Note: Deletion ranges are currently not supported for extended matches.
    if command.extend_type == MatchCombinationType.UP_TO_AND_INCLUDING:
      match = TextMatch(TextRange(match.text_range.start, extend_match.text_range.end))
    else:
      match = TextMatch(TextRange(match.text_range.start, extend_match.text_range.start))

  # Get a set of editor actions required to implement the command on the matched range.
  return perform_command(command.command_type, text, selection_range, match, command.insert_text,
                         command.lambda_func, utility_functions)
