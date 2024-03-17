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
