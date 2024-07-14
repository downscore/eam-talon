app: obsidian
tag: user.lang_cpp
-

# Override making blocks to insert extra formatting that vscode takes care of automatically but
# obsidian doesn't.
# Note: This leaves two blank lines if the block is at the first level of indentation.
make block:
  user.line_end()
  insert(" {}")
  key(left)
  key(enter)
  key(enter)
  key(up)
  key(tab)
make else:
  user.line_end()
  insert(" else {}")
  key(left)
  key(enter)
  key(enter)
  key(up)
  key(tab)
