# Keyboard shortcuts to apps and websites.
# Primarily using ctrl-cmd-<key> to switch to apps and websites, as it minimizes conflicts with other shortcuts.
# Note: ctrl-cmd-f is a default shortcut for toggling fullscreen in vscode.
key(ctrl-cmd-o): user.switcher_focus_app_by_name("Obsidian")
key(ctrl-cmd-a): user.switcher_focus_app_by_name("ChatGPT")
key(ctrl-cmd-c): user.switcher_focus_coder()
key(ctrl-cmd-b): user.switcher_focus_browser()
key(ctrl-cmd-t): user.switcher_focus_terminal()
key(ctrl-cmd-g): user.cross_browser_focus_tab_by_hostname("mail.google.com")
key(ctrl-cmd-y): user.cross_browser_focus_tab_by_hostname("youtube.com")
