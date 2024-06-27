"""Talon code for encoding/decoding actions."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import base64

import urllib.parse
from talon import Module, actions
from .lib import encoding_util

mod = Module()


@mod.action_class
class ExtensionActions:
  """Encoding/decoding actions."""

  def base64_encode_selected():
    """Base64 encodes the selected text."""
    selected = actions.user.selected_text()
    if len(selected) == 0:
      return
    encoded_string = base64.b64encode(selected.encode("utf-8")).decode("utf-8")
    actions.user.insert_via_clipboard(encoded_string)

  def base64_decode_selected():
    """Base64 decodes the selected text."""
    selected = actions.user.selected_text()
    if len(selected) == 0:
      return
    decoded_string = base64.b64decode(selected).decode("utf-8")
    actions.user.insert_via_clipboard(decoded_string)

  def base64_decode_selected_show():
    """Base64 decodes the selected text, copies it to clipboard, and displays it."""
    selected = actions.user.selected_text()
    if len(selected) == 0:
      return
    decoded_string = base64.b64decode(selected).decode("utf-8")
    actions.user.clipboard_history_set_text(decoded_string)
    actions.app.notify(decoded_string)

  def rot13_encode_selected():
    """ROT13 encodes the selected text."""
    selected = actions.user.selected_text()
    if len(selected) == 0:
      return
    encoded_string = encoding_util.encode_rot13(selected)
    actions.user.insert_via_clipboard(encoded_string)

  def rot13_encode_selected_show():
    """ROT13 encodes the selected text, copies it to clipboard, and displays it."""
    selected = actions.user.selected_text()
    if len(selected) == 0:
      return
    encoded_string = encoding_util.encode_rot13(selected)
    actions.user.clipboard_history_set_text(encoded_string)
    actions.app.notify(encoded_string)

  def url_encode_selected():
    """URL encodes the selected text."""
    selected = actions.user.selected_text()
    if len(selected) == 0:
      return
    encoded_string = urllib.parse.quote(selected)
    actions.user.insert_via_clipboard(encoded_string)

  def url_decode_selected():
    """URL decodes the selected text."""
    selected = actions.user.selected_text()
    if len(selected) == 0:
      return
    decoded_string = urllib.parse.unquote(selected)
    actions.user.insert_via_clipboard(decoded_string)

  def url_decode_selected_show():
    """URL decodes the selected text, copies it to clipboard, and displays it."""
    selected = actions.user.selected_text()
    if len(selected) == 0:
      return
    decoded_string = urllib.parse.unquote(selected)
    actions.user.clipboard_history_set_text(decoded_string)
    actions.app.notify(decoded_string)
