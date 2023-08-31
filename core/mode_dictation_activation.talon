not mode: sleep
-
^dictation mode$: user.mode_dictation()
^command mode$: user.mode_command()
^mixed mode$: user.mode_mixed()

# Switch to mixed mode and insert some prose at the same time.
^prose [<user.prose>]$:
  user.mode_mixed()
  user.dictation_insert_prose(prose or "")

# Chainable command that switches to command mode.
now do: user.mode_command()
