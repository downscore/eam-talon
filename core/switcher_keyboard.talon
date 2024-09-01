# Keyboard shortcuts to apps and websites.
# Primarily using ctrl-cmd-<key> to switch to apps and websites, as it minimizes conflicts with
# other shortcuts.
#
# Potential conflicts (keys defined in this file have precedence):
# - macOS:
#   - ctrl-cmd-q: Lock screen.
# - VS Code:
#   - ctrl-cmd-f: Toggling fullscreen.
# - Google Meet:
#   - ctrl-cmd-h: Raising hand - overriding this will break Stream Deck button.
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
key(ctrl-cmd-p): user.switcher_focus_app_by_name("ChatGPT")
key(ctrl-cmd-a): user.switcher_focus_app_by_name("Google Chat")
key(ctrl-cmd-f): user.switcher_focus_app_by_name("Finder")
key(ctrl-cmd-c): user.switcher_focus_coder()
key(ctrl-cmd-b): user.switcher_focus_browser()
key(ctrl-cmd-t): user.switcher_focus_terminal()
key(ctrl-cmd-g): user.cross_browser_focus_tab_by_hostname("mail.google.com")
key(ctrl-cmd-y): user.cross_browser_focus_tab_by_hostname("youtube.com")
key(ctrl-cmd-d): user.cross_browser_focus_tab_by_hostname("docs.google.com")
key(ctrl-cmd-l): user.cross_browser_focus_tab_by_hostname("calendar.google.com")

# Resizing the active window.
key(ctrl-cmd-z): user.snap_window_full()
key(ctrl-alt-up): user.snap_window_by_string("top right")
key(ctrl-alt-down): user.snap_window_by_string("bottom right")
key(ctrl-alt-left): user.snap_window_by_string("left")
key(ctrl-alt-right): user.snap_window_by_string("right")

# Move the active window to another screen.
key(ctrl-cmd-1): user.move_window_to_screen(1)
key(ctrl-cmd-2): user.move_window_to_screen(2)
key(ctrl-cmd-3): user.move_window_to_screen(3)

# TODO: Move non-switcher shortcuts below to a separate file, or have one dedicated keyboard file.
key(ctrl-alt-d): speech.disable()
key(ctrl-alt-f): speech.enable()
key(ctrl-alt-g): user.mode_mixed_toggle()
key(ctrl-alt-s): user.mode_indicator_toggle()

key(ctrl-alt-w): user.macos_close_all_notifications()
key(ctrl-alt-v): user.website_open_clipboard()
