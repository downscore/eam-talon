tag: user.lang_markdown
-
make block:
  insert("```\n\n```")
  key("left:4")

# Mermaid Support
make mermaid block:
  insert("```mermaid\n\n```")
  key("left:4")
make connect: insert(" --> ")
make font awesome: insert("fa:fa-")

lister:
  edit.line_insert_down()
  insert("* ")
