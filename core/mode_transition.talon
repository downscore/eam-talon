# Commands for switching between command and dictation/mixed mode.

mode: command
mode: dictation
-
# Switch to mixed mode and insert some prose at the same time.
prose [<user.prose>]$:
  user.mode_mixed()
  user.dictation_insert_prose(prose or "")

# Chainable command that switches to command mode.
now do: user.mode_command()
