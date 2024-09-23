"""Talon code for managing websites and search engines."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, Context, actions, clip
from urllib.parse import quote_plus
import webbrowser
from .lib.url_util import extract_url
from .user_settings import load_dict_from_csv
from ..core.lib import scrambler_types as st
from ..core.scrambler import ScramblerMatch

mod = Module()
ctx = Context()

mod.list("website", desc="A website.")
ctx.lists["self.website"] = load_dict_from_csv("websites.csv")

mod.list("hostname", desc="A hostname for website.")
ctx.lists["self.hostname"] = load_dict_from_csv("hostnames.csv")

mod.list(
    "search_engine",
    desc="A search engine. Any instance of %s will be replaced by query text",
)
ctx.lists["self.search_engine"] = load_dict_from_csv("search_engines.csv")


@mod.action_class
class Actions:
  """Website actions."""

  def website_open_url(url: str):
    """Visits the given URL using the saved or default browser app."""
    actions.user.switcher_focus_browser()
    webbrowser.open(url)

  def website_search_with_search_engine(search_template: str, search_text: str):
    """Searches a search engine for given text."""
    url = search_template.replace("%s", quote_plus(search_text))
    actions.user.website_open_url(url)

  def website_open_link_under_cursor():
    """Opens the link under the cursor in the default browser."""
    # Get text delimited by whitespace and get url from it.
    with clip.capture() as s:
      match = ScramblerMatch([st.Modifier(st.ModifierType.BETWEEN_WHITESPACE)])
      actions.user.scrambler_run_command(st.CommandType.COPY_TO_CLIPBOARD, match)
    try:
      selected_text = s.text()
    except clip.NoChange as exc:
      raise ValueError("No text containing a URL found") from exc
    url = extract_url(selected_text)

    # Fall back to selecting the entire line if we did not find a URL.
    if not url:
      actions.user.select_line_excluding_line_break()
      selected_text = actions.user.selected_text()
      url = extract_url(selected_text)

    # Make sure there is a URL.
    if not url:
      actions.app.notify(f"No URL found: {selected_text}")
      return

    # Open the URL in the saved or default browser.
    actions.user.website_open_url(url)

  def website_open_clipboard_impl():
    """Internal implementation: Opens the URL in the clipboard in the default browser."""
    clip_text = clip.text()
    if not clip_text:
      raise ValueError("No text in clipboard")

    # Check if the clipboard looks like it contains only a URL. This can help with opening URLs with
    # unescaped spaces in them.
    if clip_text.startswith("http://") or clip_text.startswith("https://"):
      actions.user.website_open_url(clip_text)
      return

    # Check if the clipboard text contains something that looks like a URL, possibly embedded in
    # other text.
    url = extract_url(clip_text)
    if url:
      actions.user.website_open_url(url)
    else:
      # Search for the clipboard contents.
      actions.user.website_search_with_search_engine(ctx.lists["self.search_engine"]["google"],
                                                     clip_text)

  def website_open_clipboard():
    """Opens the URL in the clipboard in the default browser."""
    actions.user.website_open_clipboard_impl()
