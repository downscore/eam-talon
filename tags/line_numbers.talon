tag: user.line_numbers
-
line <user.number>: user.jump_line(number)
pour line <user.number>:
  user.jump_line(number)
  user.line_insert_down()
drink line <user.number>:
  user.jump_line(number)
  user.line_insert_up()
spike line <user.number>: user.line_numbers_insert_line_above_no_move(number)
float line <user.number>: user.line_numbers_insert_line_below_no_move(number)
pick line <user.number> [past <user.number>]:
  user.select_line_range_for_editing(number_1, number_2 or 0)
chuck line <user.number> [past <user.number>]:
  user.select_line_range_including_line_break(number_1, number_2 or 0)
  user.delete()
copy line <user.number> [past <user.number>]:
  user.select_line_range_including_line_break(number_1, number_2 or 0)
  user.clipboard_history_copy()
  user.right()
cut line <user.number> [past <user.number>]:
  user.select_line_range_including_line_break(number_1, number_2 or 0)
  user.clipboard_history_cut()
  user.right()
indent line <user.number> [past <user.number>]:
  user.select_line_range_including_line_break(number_1, number_2 or 0)
  user.indent_more()
  user.right()
dedent line <user.number> [past <user.number>]:
  user.select_line_range_including_line_break(number_1, number_2 or 0)
  user.indent_less()
  user.right()
bring line <user.number> [past <user.number>]: user.bring_line_range(number_1, number_2 or 0)

# Using TextFlow to bring text from another line.
bring line <user.number> token <user.number_small> [past <user.number_small>]:
  user.line_numbers_bring_line_token(number, number_small_1, number_small_2 or 0)
bring line <user.number> broken <user.number_small> [past <user.number_small>]:
  user.line_numbers_bring_line_token_backwards(number, number_small_1, number_small_2 or 0)
bring line <user.number> argument <user.number_small>:
  user.line_numbers_bring_line_modifier(number, number_small, "ARGUMENT_NTH")
bring line <user.number> string <user.number_small>:
  user.line_numbers_bring_line_modifier(number, number_small, "STRING", "'")
bring line <user.number> dubstring <user.number_small>:
  user.line_numbers_bring_line_modifier(number, number_small, "STRING", "\"")
bring line <user.number> graves <user.number_small>:
  user.line_numbers_bring_line_modifier(number, number_small, "STRING", "`")
bring line <user.number> brackets <user.number_small>:
  user.line_numbers_bring_line_modifier(number, number_small, "BRACKETS_NTH")
bring line <user.number> invoke [<user.number_small>]:
  user.line_numbers_bring_line_call(number, number_small or 1)
bring line <user.number> scope:
  user.line_numbers_bring_line_scope(number)
