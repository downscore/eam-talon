"""Talon code for ChatGPT actions that can be used from other applications."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions, clip
from ..core import user_settings

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
  """ChatGPT global actions."""

  def chatgpt_run_prompt(prompt_filename: str):
    """Insert the selected text or clipboard text into the given prompt and send it to ChatGPT."""
    # Get the selected text, load the prompt, and insert the text into the prompt.
    selected_text = actions.user.selected_text()
    if not selected_text:
      selected_text = clip.text()
    if not selected_text:
      raise ValueError("No text selected.")
    prompt_template = user_settings.load_prompt(prompt_filename)
    prompt = prompt_template.replace("{SelectedText}", selected_text)

    # Focus the ChatGPT app and open a new temporary chat.
    actions.user.switcher_focus_app_by_name("ChatGPT")
    actions.user.chatgpt_new_temporary_chat()

    # Insert the prompt and send it to ChatGPT.
    actions.user.insert_via_clipboard(prompt)
    actions.key("enter")
