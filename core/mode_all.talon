mode: all
-
^drowse [<phrase>]$: speech.disable()
sleepy [<phrase>]$: speech.disable()
^speech sleep [<phrase>]$: speech.disable()
^speech wake$: speech.enable()

# Single word, multiple-syllable speech toggles that are unique, but easily recognized.
penguin [<phrase>]$: speech.disable()
coconut [<phrase>]$: speech.disable()
^dinosaur$: speech.enable()

# Keyboard shortcut for toggling speech. Used for external integrations (e.g. Stream Deck).
key(shift-f13):
  speech.toggle()
  # Trigger status update as it doesn't automatically occur for keyboard shortcuts.
  user.status_file_update()

# App switching keyboard shortcuts for external integrations (e.g. Stream Deck).
# Note: Status update needs to be triggered manually as it doesn't automatically occur for keyboard shortcuts.
key(shift-f14):
  user.switcher_focus("Safari")
  user.status_file_update()
key(shift-f15):
  user.switcher_focus("Google Chrome")
  user.status_file_update()
key(shift-f16):
  user.switcher_focus("Code")
  user.status_file_update()
key(shift-f18):
  user.switcher_focus("Terminal")
  user.status_file_update()
key(shift-f19):
  user.switcher_focus("Finder")
  user.status_file_update()
key(shift-f20):
  user.switcher_focus("Notes")
  user.status_file_update()
key(cmd-shift-f13):
  user.switcher_focus("Anki")
  user.status_file_update()

# Meets shortcuts.
key(cmd-shift-f14):
  # Toggle mic.
  user.switcher_focus_google_meet()
  sleep(50ms)
  key(cmd-d)
key(cmd-shift-f15):
  # Toggle camera.
  user.switcher_focus_google_meet()
  sleep(50ms)
  key(cmd-e)
key(cmd-shift-f16):
  # Toggle chat.
  user.switcher_focus_google_meet()
  sleep(50ms)
  key(cmd-ctrl-c)
key(cmd-shift-f18):
  # Toggle participants.
  user.switcher_focus_google_meet()
  sleep(50ms)
  key(cmd-ctrl-p)
key(cmd-shift-f19):
  # Toggle raising hand.
  user.switcher_focus_google_meet()
  sleep(50ms)
  key(cmd-ctrl-h)
key(cmd-shift-f20):
  # Close meeting tab.
  user.switcher_focus_google_meet()
  sleep(50ms)
  key(cmd-w)

# Macro shortcuts.
key(ctrl-f13):
  # Record macro.
  user.macro_record()
  user.macro_display_toggle()
key(ctrl-f14):
  # Stop recording macro.
  user.macro_stop()
  user.macro_display_toggle()
key(ctrl-f15):
  # Play macro.
  user.macro_play()
