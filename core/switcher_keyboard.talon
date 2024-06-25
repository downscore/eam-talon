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

key(ctrl-cmd-o): user.switcher_focus_app_by_name("Obsidian")
key(ctrl-cmd-a): user.switcher_focus_app_by_name("ChatGPT")
key(ctrl-cmd-c): user.switcher_focus_coder()
key(ctrl-cmd-b): user.switcher_focus_browser()
key(ctrl-cmd-t): user.switcher_focus_terminal()
key(ctrl-cmd-g): user.cross_browser_focus_tab_by_hostname("mail.google.com")
key(ctrl-cmd-y): user.cross_browser_focus_tab_by_hostname("youtube.com")
key(ctrl-cmd-d): user.cross_browser_focus_tab_by_hostname("docs.google.com")

# Make the active window fullscreen.
key(ctrl-cmd-f): user.snap_window_full()
