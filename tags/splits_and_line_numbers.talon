tag: user.splits
and tag: user.line_numbers
-
bring cross line <user.number> [past <user.number>]:
  user.splits_line_numbers_bring_line_range(number_1, number_2 or 0)

# Using TextFlow to bring text from another line.
bring cross line <user.number> token <user.number_small> [past <user.number_small>]:
  user.splits_line_numbers_bring_line_token(number, number_small_1, number_small_2 or 0)
bring cross line <user.number> broken <user.number_small> [past <user.number_small>]:
  user.splits_line_numbers_bring_line_token_backwards(number, number_small_1, number_small_2 or 0)
bring cross line <user.number> argument <user.number_small>:
  user.splits_line_numbers_bring_line_modifier(number, number_small, "ARGUMENT_NTH")
bring cross line <user.number> string <user.number_small>:
  user.splits_line_numbers_bring_line_modifier(number, number_small, "STRING_NTH", "'")
bring cross line <user.number> dubstring <user.number_small>:
  user.splits_line_numbers_bring_line_modifier(number, number_small, "STRING_NTH", "\"")
bring cross line <user.number> graves <user.number_small>:
  user.splits_line_numbers_bring_line_modifier(number, number_small, "STRING_NTH", "`")
bring cross line <user.number> brackets <user.number_small>:
  user.splits_line_numbers_bring_line_modifier(number, number_small, "BRACKETS_NTH")
bring cross line <user.number> invoke [<user.number_small>]:
  user.splits_line_numbers_bring_line_call(number, number_small or 1)
bring cross line <user.number> scope:
  user.splits_line_numbers_bring_line_scope(number)
