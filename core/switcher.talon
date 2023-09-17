app <user.running_applications>: user.switcher_focus(running_applications)
app last: key(cmd-tab)

app list running: user.switcher_toggle_running()
app list launch: user.switcher_toggle_launch()
app launch <user.launch_applications>: user.switcher_launch(launch_applications)

# Saving windows for shortcuts.
app save coder: user.switcher_save_current_window("coder")
app save browser: user.switcher_save_current_window("browser")

# Shortcuts to apps.
obsidian: user.switcher_focus("Obsidian")
coder: user.switcher_focus_coder()
browser: user.switcher_focus_browser()
