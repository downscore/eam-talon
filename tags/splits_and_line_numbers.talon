tag: user.splits
and tag: user.line_numbers
-
bring cross line <user.number> [past <user.number>]:
  user.splits_line_numbers_bring_line_range(number_1, number_2 or 0)

# Scrambler commands using line numbers and splits.
<user.scrambler_command_type> cross line <user.number> <user.scrambler_any_match>:
  user.splits_line_numbers_scrambler_run_command(number, scrambler_command_type, scrambler_any_match, true)
