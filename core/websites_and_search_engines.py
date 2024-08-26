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
    """Visit the given URL using the saved or default browser app."""
    actions.user.switcher_focus_browser()
    webbrowser.open(url)

  def website_search_with_search_engine(search_template: str, search_text: str):
    """Search a search engine for given text"""
    url = search_template.replace("%s", quote_plus(search_text))
    actions.user.website_open_url(url)

  def website_open_link_under_cursor():
    """Open the link under the cursor in the default browser."""
    # Select text delimited by whitespace and get url from it.
    actions.user.textflow_execute_command_enum_strings("SELECT", "BETWEEN_WHITESPACE")
    selected_text = actions.user.selected_text()
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

  def website_open_clipboard():
    """Open the URL in the clipboard in the default browser."""
    url = clip.text()
    if not url:
      raise ValueError("No URL in clipboard")
    actions.user.website_open_url(url)
