# Core commands that run with any match type.
scrambler <user.scrambler_command_type> <user.scrambler_any_match>:
  user.scrambler_run_command(scrambler_command_type, scrambler_any_match)

# Commands that run starting from the current selection or cursor position.
scrambler <user.scrambler_command_type> <user.scrambler_match_from_cursor>:
  user.scrambler_run_command(scrambler_command_type, scrambler_match_from_cursor)

# Commands that run on a single word.
scrambler <user.scrambler_single_word_command_type> <user.scrambler_word>:
  user.scrambler_run_command(scrambler_single_word_command_type, scrambler_word)

# Selection commands with no command prefix (e.g. "argument 1").
scrambler (<user.scrambler_object_count>|<user.scrambler_object_movement>):
  user.scrambler_run_select_command(scrambler_object_count or scrambler_object_movement)
