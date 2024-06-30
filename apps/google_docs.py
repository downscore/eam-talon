"""Talon code for Google Docs support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module, actions
from ..core.lib.google_docs_util import get_preview_url

mod = Module()
ctx = Context()

mod.apps.google_docs = """
title: /Google Docs/
"""
mod.apps.google_docs = """
title: /Google Sheets/
"""
mod.apps.google_docs = """
title: /Google Slides/
"""

ctx.matches = """
app: google_docs
"""


@mod.action_class
class Actions:
  """Google docs actions."""

  def google_docs_preview():
    """Switch to preview mode for the current doc."""
    doc_url = actions.browser.address()
    actions.user.browser_go(get_preview_url(doc_url))


@ctx.action_class("user")
class ExtensionActions:
  """Action overrides."""

  def textflow_potato_get_text_before_cursor():
    # Google Docs has some unusual text selection behavior. It randomly inserts trailing new lines, and behavior inside
    # tables is unpredictable. To avoid problems, we only allow TextFlow to act on one line in Google Docs.
    actions.key("ctrl-shift-a")
    result = actions.user.selected_text()
    if len(result) > 0:
      actions.user.right()
    return result

  def textflow_potato_get_text_after_cursor():
    # See above. TextFlow only acts on one line in Google Docs.
    actions.key("ctrl-shift-e")
    result = actions.user.selected_text()
    if len(result) > 0:
      actions.user.left()
    return result

  def line_insert_up():
    actions.user.line_start()
    actions.key("enter up")

  def line_insert_down():
    actions.user.line_end()
    actions.key("enter")

  def insert_link():
    actions.key("cmd-k")

  def insert_link_from_clipboard():
    actions.key("cmd-k")
    actions.sleep("100ms")
    actions.user.paste()
    actions.sleep("100ms")
    actions.key("enter")

  def style_title():
    actions.key("ctrl-alt-o")
    actions.sleep("50ms")
    actions.key("p")
    actions.sleep("50ms")
    actions.key("t")
    actions.sleep("50ms")
    actions.key("a")

  def style_subtitle():
    actions.key("ctrl-alt-o")
    actions.sleep("50ms")
    actions.key("p")
    actions.sleep("50ms")
    actions.key("s")
    actions.sleep("50ms")
    actions.key("a")

  def style_heading(number: int):
    actions.key(f"cmd-alt-{number}")

  def style_body():
    actions.key("cmd-alt-0")

  def style_bold():
    actions.key("cmd-b")

  def style_italic():
    actions.key("cmd-i")

  def style_underline():
    actions.key("cmd-u")

  def style_strikethrough():
    actions.key("cmd-shift-x")

  def style_bullet_list():
    actions.key("cmd-shift-8")

  def style_numbered_list():
    actions.key("cmd-shift-7")

  def style_checklist():
    actions.key("cmd-shift-9")

  def style_toggle_check():
    actions.key("cmd-alt-enter")
