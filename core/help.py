"""Talon code for built-in help actions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from typing import Optional
from talon import Context, Module, actions, imgui, registry

mod = Module()
ctx = Context()

mod.tag("help_open", "The help GUI is open")

_MAX_LINES_PER_PAGE = 45
_MAX_COMMAND_CHARS = 30
_MAX_COMMAND_DESCRIPTION_CHARS = 50

# Help contents. Each element is one line.
_help_contents: list[str] = []

# Current page
_help_page: int = 0


def _add_context_to_help(context):
  """Add a description of the given context to the help contents."""
  # Make sure there are commands.
  if len(context.commands) == 0:
    return

  # Get context name (path fragment before .talon).
  name = ".".join(context.path.split(".")[-3:-1])

  # Add the context name.
  _help_contents.append(f"{name}:")

  # Add commands. Key is hashed command name.
  for _, command in sorted(context.commands.items()):
    # Get the formatted command name.
    command_name = command.rule.rule
    command_name = command_name.replace("user.", "")
    command_name = command_name.replace("textflow", "tf")
    command_name = command_name[:_MAX_COMMAND_CHARS]
    if len(command_name) == _MAX_COMMAND_CHARS:
      command_name = command_name[:-1] + "…"

    # Add spaces to align text.
    line = "  " + command_name + " " * (_MAX_COMMAND_CHARS - len(command_name))

    # Get the formatted description.
    description = command.script.code.replace("\n", " ")
    description = description.replace("user.", "")
    description = description.replace("textflow", "tf")
    description = description[:_MAX_COMMAND_DESCRIPTION_CHARS]
    if len(description) == _MAX_COMMAND_DESCRIPTION_CHARS:
      description = description[:-1] + "…"

    # Add the description.
    line += f"  {description}"

    _help_contents.append(line)


@imgui.open(y=0)
def help_gui(gui: imgui.GUI):  # pylint: disable=redefined-outer-name
  gui.text(f"Help ({_help_page + 1}/{len(_help_contents) // _MAX_LINES_PER_PAGE + 1}) "
           " << Help Last, Help Next >>")
  gui.line()

  page_content = _help_contents[_help_page * _MAX_LINES_PER_PAGE:(_help_page + 1) *
                                _MAX_LINES_PER_PAGE]
  for line in page_content:
    gui.text(line)

  gui.spacer()
  if gui.button("Help Hide"):
    actions.user.help_hide()


@mod.action_class
class Actions:
  """Formatter actions."""

  def help_refresh(context_filter: Optional[list[str]] = None):
    """Refreshes the active help contents."""
    global _help_contents
    global _help_page
    _help_contents = []
    _help_page = 0

    # Sort active contexts in to global and specialized sets (e.g. for a specific app).
    specialized_contexts = []
    global_contexts = []
    for context in registry.active_contexts():
      parts = context.path.split(".")
      # Only take ".talon" contexts.
      if parts[-1] != "talon":
        continue

      context_directory = parts[-3]
      context_name = parts[-2]

      # Apply filter if provided.
      if context_filter is not None and context_directory not in context_filter:  # pylint: disable=unsupported-membership-test
        continue

      if context_directory in ["apps", "tags", "private"] and not "global" in context_name:
        specialized_contexts.append(context)
      else:
        global_contexts.append(context)

    # Sort the contexts by path.
    specialized_contexts.sort(key=lambda context: context.path)
    global_contexts.sort(key=lambda context: context.path)

    # Add the specialized contexts first.
    for context in specialized_contexts:
      _add_context_to_help(context)
    for context in global_contexts:
      _add_context_to_help(context)

  def help_show(directory_filter: Optional[str] = None):
    """Shows the help GUI."""
    # Start by listing contexts.
    global _help_contents
    global _help_page
    _help_contents = []
    _help_page = 0
    # Use filter if provided.
    actions.user.help_refresh([directory_filter] if directory_filter is not None else None)
    help_gui.show()

  def help_hide():
    """Hides the help GUI."""
    global _help_contents
    global _help_page
    _help_contents = []
    _help_page = 0
    help_gui.hide()

  def help_next_page():
    """Moves to the next help page."""
    global _help_page
    _help_page = (_help_page + 1) % (len(_help_contents) // _MAX_LINES_PER_PAGE + 1)

  def help_previous_page():
    """Moves to the previous help page."""
    global _help_page
    _help_page = (_help_page - 1) % (len(_help_contents) // _MAX_LINES_PER_PAGE + 1)

  def help_set_page(page: int):
    """Jumps to a given help page."""
    global _help_page
    if page < 0:
      raise ValueError("Page must be non-negative")
    _help_page = min(page, len(_help_contents) // _MAX_LINES_PER_PAGE)
