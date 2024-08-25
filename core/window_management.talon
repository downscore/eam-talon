window (new|open): user.window_open()
window next: user.window_next()
window last: user.window_previous()
window close: user.window_close()

snap <user.window_snap_position>: user.snap_window(window_snap_position)
snap next [screen]: user.move_window_next_screen()
snap last [screen]: user.move_window_previous_screen()
snap screen <user.number>:
  user.move_window_to_screen(number)
  # Windows don't always maintain dimensions when moving between screens.
  user.snap_window_full()
snap <user.running_applications> <user.window_snap_position>:
  user.snap_app(running_applications, window_snap_position)
snap <user.running_applications> [screen] <user.number>:
  user.move_app_to_screen(running_applications, number)
  # Windows don't always maintain dimensions when moving between screens.
  user.snap_window_full()
