tag: user.lang_talon
-

comment inline:
  edit.line_end()
  insert("  # ")
comment to do:
  insert("# TODO: ")
comment:
  insert("# ")

make insert:
  insert("insert(\"\")")
  key(left left)
make key:
  insert("key()")
  key(left)
make user:
  insert("user.")
make edit:
  insert("edit.")
make app: insert("app: ")
make tag: insert("tag: ")
make declare tag: insert("tag(): ")
