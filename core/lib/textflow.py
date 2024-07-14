"""API for generating input actions to manipulate text in an editor."""

from typing import Optional
from .textflow_commands import perform_command
from .textflow_modifiers import apply_modifier
from .textflow_targets import match_compound_target
from .textflow_types import Command, EditorAction, TextMatch, TextRange, UtilityFunctions


def run_command(command: Command, text: str, selection_range: TextRange,
                utility_functions: UtilityFunctions) -> list[EditorAction]:
  """Runs a command for navigating and manipulating text."""
  # Match compound targets.
  match_from = match_compound_target(command.target_from, text, selection_range, utility_functions)
  if match_from is None:
    raise ValueError(f"Could not match 'from' target: {command.target_from}")
  match_to: Optional[TextMatch] = None
  if command.target_to is not None:
    match_to = match_compound_target(command.target_to, text, selection_range, utility_functions)
    # If a 'to' target is provided it must be matched, otherwise the command may do unexpected
    # things.
    if match_to is None:
      raise ValueError(f"Could not match 'to' target: {command.target_to}")

  # Apply modifiers.
  match_from = apply_modifier(text, match_from, command.target_from.modifier)
  if match_to is not None and command.target_to is not None:
    match_to = apply_modifier(text, match_to, command.target_to.modifier)

  # Get command actions.
  return perform_command(command.command_type, text, selection_range, match_from, match_to,
                         command.insert_text, command.lambda_func, utility_functions)
