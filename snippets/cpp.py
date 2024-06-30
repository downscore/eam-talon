"""Support for snippets."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module
from ..core.snippets import load_snippets_json

mod = Module()
ctx = Context()

mod.list("snippet_cpp", desc="Common C++ snippets")
ctx.lists["user.snippet_cpp"] = load_snippets_json("cpp.json")
