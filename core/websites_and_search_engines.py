"""Talon code for managing websites and search engines."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, Context
from urllib.parse import quote_plus
import webbrowser
from .user_settings import load_dict_from_csv

mod = Module()
ctx = Context()

mod.list("website", desc="A website.")
ctx.lists["self.website"] = load_dict_from_csv("websites.csv")

mod.list(
    "search_engine",
    desc="A search engine. Any instance of %s will be replaced by query text",
)
ctx.lists["self.search_engine"] = load_dict_from_csv("search_engines.csv")


@mod.action_class
class Actions:

  def open_url(url: str):
    """Visit the given URL."""
    webbrowser.open(url)

  def search_with_search_engine(search_template: str, search_text: str):
    """Search a search engine for given text"""
    url = search_template.replace("%s", quote_plus(search_text))
    webbrowser.open(url)
