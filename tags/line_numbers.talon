tag: user.line_numbers
-
jump line <user.number>: edit.jump_line(number)
pour line <user.number>:
  edit.jump_line(number)
  edit.line_insert_down()
drink line <user.number>:
  edit.jump_line(number)
  edit.line_insert_up()
take line <user.number> [past <user.number>]:
  user.select_line_range(number_1, number_2 or 0)
chuck line <user.number> [past <user.number>]:
  user.select_line_range(number_1, number_2 or 0)
  edit.delete()
copy line <user.number> [past <user.number>]:
  user.select_line_range(number_1, number_2 or 0)
  user.clipboard_history_copy()
  edit.right()
cut line <user.number> [past <user.number>]:
  user.select_line_range(number_1, number_2 or 0)
  user.clipboard_history_cut()
  edit.right()
indent line <user.number> [past <user.number>]:
  user.select_line_range(number_1, number_2 or 0)
  edit.indent_more()
  edit.right()
dedent line <user.number> [past <user.number>]:
  user.select_line_range(number_1, number_2 or 0)
  edit.indent_less()
  edit.right()
bring line <user.number>: user.bring_line_by_number(number)
