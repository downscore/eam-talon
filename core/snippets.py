"""Support for using snippets with voice commands. The snippets themselves are provided and other files based on the
current context."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import json
from pathlib import Path
import re
from talon import Context, Module, actions, resource

mod = Module()
ctx = Context()

_SNIPPETS_DIR = Path(__file__).parents[1] / "snippets"
_PRIVATE_SNIPPETS_DIR = Path(__file__).parents[2] / "private/snippets"


def _load_snippets_internal(filename: str, json_content: str) -> dict[str, str]:
  """Loads snippets from a string containing JSON data."""
  result = {}

  # Strip line comments from the JSON data then read it. Only strips lines that start with a
  # comment, so snippets may include comments.
  json_content = re.sub(r"^\w*//.*?\n", "", json_content, flags=re.MULTILINE)
  snippets = json.loads(json_content)

  # Get usable snippets from the loaded data.
  # Uses the snippet name as the spoken form. This way we can keep short, unpronounceable prefixes
  # for typing.
  for spoken, snippet in snippets.items():
    # Warn if `prefix` is missing. It's required to use the snippet with the keyboard in vscode.
    if "prefix" not in snippet:
      print(f"Snippet missing a `prefix` field: {spoken}")

    # `body` may be a string or a list of strings.
    if isinstance(snippet["body"], str):
      body = snippet["body"]
    else:
      body = "\n".join(snippet["body"])

    if spoken in result:
      print(f"Duplicate snippet spoken form: {spoken}")
    result[spoken] = body

  print(f"Loaded snippets from JSON. Snippets: {len(result)}, File: {filename}")
  return result


def load_snippets_json(filename: str) -> dict[str, str]:
  """Loads adjacent file containing snippets, and returns a dictionary snippet contents keyed by
  spoken form."""
  path = _SNIPPETS_DIR / filename
  private_path = _PRIVATE_SNIPPETS_DIR / filename

  result: dict[str, str] = {}

  # Read public file if it exists. Read via resource to take advantage of talon's ability to reload
  # this script for us when the resource changes.
  if path.exists():
    with resource.open(str(path), "r") as f:
      result.update(_load_snippets_internal(filename, f.read()))

  # Read private file if it exists.
  if private_path.exists():
    with resource.open(str(private_path), "r") as f:
      result.update(_load_snippets_internal(filename, f.read()))

  return result


@mod.action_class
class Actions:
  """Snippet actions."""

  def snippet_insert(body: str):
    """Inserts a snippet with the given body."""
    # The default implementation inserts the body with all placeholders removed and moves the cursor
    # to the location of the first placeholder (by character index, not necessarily the placeholder
    # with the lowest number).
    placeholder_regex = r"\$\{[0-9]+:[^}]*\}|\$[0-9]+"

    # Find the first placeholder.
    first_placeholder_index = None
    match = re.search(placeholder_regex, body)
    if match:
      first_placeholder_index = match.start()

    # Remove all placeholders.
    text_to_insert = re.sub(placeholder_regex, "", body)

    actions.user.insert_via_clipboard(text_to_insert)
    if first_placeholder_index is not None:
      actions.key(f"left:{len(text_to_insert) - first_placeholder_index}")
