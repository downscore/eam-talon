# YouTube is currently the only media app where we support seeking or changing the playback speed.
# Consider moving these commands if this changes in the future.
media faster:
  user.switcher_save_focus()
  user.youtube_focus()
  key(shift-.)
  user.switcher_restore_focus()

media slower:
  user.switcher_save_focus()
  user.youtube_focus()
  key(shift-,)
  user.switcher_restore_focus()

media push:
  user.switcher_save_focus()
  user.youtube_focus()
  key(l)
  user.switcher_restore_focus()

media pull:
  user.switcher_save_focus()
  user.youtube_focus()
  key(j)
  user.switcher_restore_focus()
