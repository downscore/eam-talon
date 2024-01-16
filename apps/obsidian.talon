app: obsidian
-
tag(): user.multiple_cursors
tag(): user.navigation
tag(): user.tabs

# Command palette
please [<user.text>]:
  key(cmd-p)
  insert(user.text or "")

# Show the quick open dialogue.
tab list [<user.text>]:
  key(cmd-o)
  sleep(250ms)
  insert(text or "")

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

# Create a new folder
folder new:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2023-08-15_20.09.43.016999.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

# Create a new file
file new: key(cmd-n)
