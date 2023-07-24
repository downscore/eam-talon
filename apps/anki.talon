app: anki
-
separator: user.insert_via_clipboard("::")

card type basic:
  key(cmd-n)
  sleep(50ms)
  insert("Basic")
  key(enter)

card type reversed:
  key(cmd-n)
  sleep(50ms)
  insert("Basic (and reversed card)")
  key(enter)

card type close:
  key(cmd-n)
  sleep(50ms)
  insert("Cloze")
  key(enter)

# Commands for adding Japanese example sentences. These may be out of date.
# -
# close that:
#   key(cmd-shift-c)
#   key(left)
#   key(left)
#   sleep(50ms)
#   user.insert_via_clipboard("::")
# furry that:
#   edit.cut()
#   sleep(50ms)
#   user.insert_via_clipboard("! !")
#   key(backspace)
#   key(left)
#   key(backspace)
#   key(right)
#   sleep(50ms)
#   edit.paste()
#   sleep(50ms)
#   user.insert_via_clipboard("[]")
#   key(left)
# get next word:
#   key(ctrl-left)
#   sleep(1000ms)
#   key(backspace)
#   key(down)
#   edit.select_line()
#   user.clipboard_history_copy()
#   key(ctrl-right)
# save and next word:
#   key(cmd-enter)
#   key(ctrl-left)
#   sleep(1000ms)
#   key(backspace)
#   key(down)
#   edit.select_line()
#   user.clipboard_history_copy()
#   key(ctrl-right)
