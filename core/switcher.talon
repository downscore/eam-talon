app <user.running_applications>: user.switcher_focus(running_applications)
app last: key(cmd-tab)

app list running: user.switcher_toggle_running()
app list launch: user.switcher_toggle_launch()
app launch <user.launch_applications>: user.switcher_launch(launch_applications)

# Saving windows for shortcuts.
app save coder: user.switcher_save_current_window_by_name("coder")
app save browser: user.switcher_save_current_window_by_name("browser")
app save terminal: user.switcher_save_current_window_by_name("terminal")

# Shortcuts to apps.
obsidian: user.switcher_focus("Obsidian")
coder: user.switcher_focus_coder()
browser: user.switcher_focus_browser()
terminal: user.switcher_focus_terminal()
