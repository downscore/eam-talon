app: chrome
-
tag(): browser
tag(): user.tabs
tag(): user.navigation

# TODO: Make this a command usable across applications.
tab list [<user.text>]:
  key(cmd-shift-a)
  sleep(250ms)
  insert(text or "")
