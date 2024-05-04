app: obsidian
-
tag(): user.multiple_cursors
tag(): user.navigation
tag(): user.tabs

# Command palette
please [<user.text>]:
  key(cmd-p)
  insert(user.text or "")

# Focus the editor.
# TODO: Make this a command usable across applications.
editor: user.obsidian("Focus on last note")

# Sidebar
bar dog: user.obsidian("Toggle left sidebar")
bar files: user.obsidian("File: Show file explorer")
bar search: user.obsidian("Search: Search in all files")
# Reusing "bookmarks" command from browsers.
bookmarks: user.obsidian("Bookmarks: Show bookmarks")

# Right sidebar
panel dog: user.obsidian("Toggle right sidebar")
panel backlinks: user.obsidian("Backlinks: Show backlinks")
panel out links: user.obsidian("Outgoing links: Show outgoing links")
panel tags: user.obsidian("Tags view: Show tags")
panel outline: user.obsidian("Outline: Show outline")
panel properties: user.obsidian("Properties view: Show all properties")
panel calendar:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2024-01-23_21.45.02.135149.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()
panel copilot:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2024-01-23_21.45.59.000813.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

# Use AI magic.
# TODO: Make this a command usable across applications.
copilot answer:
  user.obsidian("Copilot: Apply custom prompt to selection")
  sleep(100ms)
  insert("Answer question")
  sleep(100ms)
  key(enter)
copilot proofread:
  user.obsidian("Copilot: Apply custom prompt to selection")
  sleep(100ms)
  insert("Proofread Dictated")
  sleep(100ms)
  key(enter)

# Toggle source view
source dog: user.obsidian("Toggle Live Preview/Source mode")

# Open today's daily note
daily note: user.obsidian("Daily notes: Open today's daily note")

# Wiki-link syntax
make link:
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
