app: slack
-

code block: key(cmd-shift-alt-c)

# Quick switcher (like command palette)
please [<user.text>]:
  key(cmd-k)
  insert(user.text or "")

# Edit last message.
edit last:
  key(cmd-up)
