"""Talon code for Activity Monitor support."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Context, Module

mod = Module()
ctx = Context()

mod.apps.activity_monitor = """
os: mac
and app.bundle: com.apple.ActivityMonitor
"""

ctx.matches = r"""
app: activity_monitor
"""
