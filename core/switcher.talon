# Changing focus.
app <user.running_applications>: user.switcher_focus_app_by_name(running_applications)
app last: key(cmd-tab)

# Lists of applications.
app list running: user.switcher_toggle_running()
app list launch: user.switcher_toggle_launch()
app list launch next: user.switcher_launch_next_page()
app list launch last: user.switcher_launch_previous_page()

# Launching applications.
app launch <user.launch_applications>: user.switcher_launch(launch_applications)

# Saving windows for shortcuts.
app save coder: user.switcher_save_current_window_by_name("coder")
app save browser: user.switcher_save_current_window_by_name("browser")
app save terminal: user.switcher_save_current_window_by_name("terminal")

# Shortcuts to apps.
obsidian: user.switcher_focus_app_by_name("Obsidian")
chit chat: user.switcher_focus_app_by_name("ChatGPT")
coder: user.switcher_focus_coder()
browser: user.switcher_focus_window_by_type("browser", "Google Chrome", "Safari")
terminal: user.switcher_focus_terminal()

# Global shortcuts for opening a new terminal tab.
terminal new: user.switcher_new_terminal_tab()
terminal here: user.switcher_new_terminal_tab(user.app_get_current_directory())
terminal paste: user.switcher_new_terminal_tab(clip.text())

# Global shortcuts for IDE bookmarks.
jump <user.number>: user.switcher_jump_to_bookmark(user.number)
