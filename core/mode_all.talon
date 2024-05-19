mode: all
-
^speech sleep [<phrase>]$: user.mode_disable_speech()
^speech wake$: user.mode_enable_speech()

# Single word, multiple-syllable speech toggles that are unique, but easily recognized.
# These toggles give audio feedback in case the screen is not currently visible.
coconut [<phrase>]$:
  user.mode_disable_speech()
  user.macos_beep()
# Mistaken recognitions for "dinosaur": Denise:5, tensor:4, venator:3, dilator:2, vanisher, then IO, donator, donate
# ^dinosaur$: user.mode_enable_speech()
# "Pavia" seems to be the most common mistaken recognition for "papaya".
^papaya$:
  user.mode_enable_speech()
  user.macos_beep()

# Switch to command mode and sleep at the same time. Without this, in dictation mode "now do coconut" results in
# switching to command mode and writing "coconut" without sleeping.
now do coconut [<phrase>]$:
  user.mode_command()
  user.mode_disable_speech()

# Allow media control without enabling speech.
media (play | pause): key(play)
