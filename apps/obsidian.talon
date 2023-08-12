app: obsidian
-
tag(): user.lang_markdown
tag(): user.multiple_cursors
tag(): user.navigation
tag(): user.tabs

# Command palette
please [<user.text>]:
  key(cmd-p)
  insert(user.text or "")

# TODO: Make this a command usable across applications.
copilot answer:
  user.obsidian("Copilot: Apply custom prompt to selection")
  sleep(100ms)
  insert("Answer question")
  sleep(100ms)
  key(enter)

# Toggle source view
source dog: user.obsidian("Toggle Live Preview/Source mode")

# Open today's daily note
daily note: user.obsidian("Daily notes: Open today's daily note")

# Wiki-link syntax
linker:
  insert("[[]]")
  key("left:2")
