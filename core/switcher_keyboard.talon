# Keyboard shortcuts to apps and websites.
# Primarily using ctrl-cmd-<key> to switch to apps and websites, as it minimizes conflicts with other shortcuts.
#
# Potential conflicts (keys defined in this file have precedence):
# - macOS:
#   - ctrl-cmd-q: Lock screen.
# - VS Code:
#   - ctrl-cmd-f: Toggling fullscreen.
# - Google Meet:
#   - ctrl-cmd-h: Raising hand.
#   - ctrl-cmd-c: Chat.
#   - ctrl-cmd-p: Participants.
# - Safari:
#   - ctrl-cmd-s: Shared with you.
#   - ctrl-cmd-1: Bookmarks sidebar.
#   - ctrl-cmd-2: Reading list sidebar.
#   - ctrl-cmd-n: Empty new tab group.
#   - ctrl-cmd-w: Delete tab group.
#   - ctrl-cmd-r: Enter responsive design mode.

# Focus an application or browser tab.
key(ctrl-cmd-o): user.switcher_focus_app_by_name("Obsidian")
key(ctrl-cmd-a): user.switcher_focus_app_by_name("ChatGPT")
key(ctrl-cmd-q): user.switcher_focus_app_by_name("Google Chat")
key(ctrl-cmd-c): user.switcher_focus_coder()
key(ctrl-cmd-b): user.switcher_focus_browser()
key(ctrl-cmd-t): user.switcher_focus_terminal()
key(ctrl-cmd-g): user.cross_browser_focus_tab_by_hostname("mail.google.com")
key(ctrl-cmd-y): user.cross_browser_focus_tab_by_hostname("youtube.com")
key(ctrl-cmd-d): user.cross_browser_focus_tab_by_hostname("docs.google.com")

# Resizing the active window.
key(ctrl-cmd-z): user.snap_window_full()
key(ctrl-alt-up): user.snap_window_full()
key(ctrl-alt-down): user.snap_window_by_string("center")
key(ctrl-alt-left): user.snap_window_by_string("left")
key(ctrl-alt-right): user.snap_window_by_string("right")

# Move the active window to another screen.
key(ctrl-cmd-1): user.move_window_to_screen(1)
key(ctrl-cmd-2): user.move_window_to_screen(2)
key(ctrl-cmd-3): user.move_window_to_screen(3)
