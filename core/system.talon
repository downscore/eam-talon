# Repeat last command n times.
# repeat_ordinal subtracts 1 because we are repeating: The initial command counts as one.
<user.repeat_ordinal>: core.repeat_command(repeat_ordinal)

# "anchor" is used to terminate some commands that take phrases of arbitrary length. Here we handle the case where such
# a command gets fragmented and "anchor" leads the next command.
anchor: skip()

# Short pause. Can be used to insert pauses into chained commands or a macro.
stumble: sleep(250ms)

# Cancel previous or following commands.
^[<phrase>] cancel$: app.notify("Command canceled")
ignore [<phrase>]$: app.notify("Command ignored")

# System debugging commands.
speech debug context: user.system_context_ui_toggle()
speech open log: menu.open_log()
speech open rebel: menu.open_repl()

# Copy debugging data to clipboard.
copy file name:
  user.clipboard_history_set_text(win.filename())
copy window title:
  user.clipboard_history_set_text(win.title())
copy app name:
  user.clipboard_history_set_text(app.name())
copy app bundle:
  user.clipboard_history_set_text(app.bundle())
