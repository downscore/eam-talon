"""Talon module and context for managing abbreviations."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module
from .user_settings import load_dict_from_csv

mod = Module()
ctx = Context()

mod.list("abbreviation", desc="Common abbreviation")
ctx.lists["user.abbreviation"] = load_dict_from_csv("abbreviate.csv")
