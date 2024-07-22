tag: user.lang_talon
-

comment inline:
  user.line_end()
  insert("  # ")
comment to do:
  insert("# TODO: ")
comment:
  insert("# ")

make insert:
  insert("insert(\"\")")
  key(left:2)
make key:
  insert("key()")
  key(left)
make user:
  insert("user.")
make app: insert("app: ")
make tag: insert("tag: ")
make declare tag: insert("tag(): ")
make or: insert(" or ")
