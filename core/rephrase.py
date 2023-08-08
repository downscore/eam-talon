"""Talon code for re-running a phrase in a new context. Code originally from
https://github.com/AndreasArvidsson/andreas-talon/blob/bff8d56b3469c124ac821689be644cf4ea53c171/core/rephrase.py#L4
MIT License, Copyright (c) 2021 Andreas Arvidsson
"""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

from talon import Module, speech_system, cron
from talon.grammar import Phrase

mod = Module()

# This should usually only contain the last phrase. It is popped when a phrase completes.
# TODO: Can we just store a single phrase and clear it on post:phrase?
_phrase_stack = []


@mod.action_class
class Actions:
  """Actions for re-running a phrase in a new context."""

  def rephrase(phrase: Phrase, run_async: bool = False):
    """Re-evaluate and run phrase in the current context. The phrase may have been uttered in a different context."""
    try:
      current_phrase = _phrase_stack[-1]
      ts = current_phrase["_ts"]
      start = phrase.words[0].start - ts
      end = phrase.words[-1].end - ts
      samples = current_phrase["samples"]
      pstart = int(start * 16_000)
      pend = int(end * 16_000)
      samples = samples[pstart:pend]
    except KeyError:
      return

    if run_async:
      cron.after("0ms", lambda: speech_system._on_audio_frame(samples))  # pylint: disable=protected-access
    else:
      speech_system._on_audio_frame(samples)  # pylint: disable=protected-access


def on_pre_phrase(d):
  _phrase_stack.append(d)


def on_post_phrase(_):
  _phrase_stack.pop()


speech_system.register("pre:phrase", on_pre_phrase)
speech_system.register("post:phrase", on_post_phrase)
