macro record: user.macro_record()
macro stop: user.macro_stop()
macro play: user.macro_play()
macro contents: user.macro_display_toggle()
macro delete <user.number>: user.macro_delete_entry(number)

# Repeating a macro should be hard to do by accident, as it could result in tons of unwanted input.
macro repeat <user.number> times: user.macro_repeat(number)

# Saving a new macro to file cannot be chained with other commands.
^macro save <user.text>$: user.macro_save(text)

# Replace the current macro with the one with the given label.
macro load {user.macro_label}: user.macro_load_label(macro_label)
