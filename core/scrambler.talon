# Core commands that run with any match type.
scrambler <user.scrambler_command_type> <user.scrambler_any_match>:
  user.scrambler_run_command(scrambler_command_type, scrambler_any_match)

# Commands that run starting from the current selection or cursor position.
scrambler <user.scrambler_command_type> <user.scrambler_match_from_cursor>:
  user.scrambler_run_command(scrambler_command_type, scrambler_match_from_cursor)

# Commands that run on a single word.
scrambler <user.scrambler_single_word_command_type> <user.scrambler_word>:
  user.scrambler_run_command(scrambler_single_word_command_type, scrambler_word)

# Selection commands with no command prefix (e.g. "argument 1").
scrambler <user.scrambler_no_prefix_match>:
  user.scrambler_run_select_command(scrambler_no_prefix_match)

# Replace a target with prose (includes punctuation).
scrambler swap <user.scrambler_substring_range> with <user.prose>$:
  user.scrambler_replace(scrambler_substring_range, prose)
scrambler swap <user.scrambler_substring_range> with <user.prose> anchor:
  user.scrambler_replace(scrambler_substring_range, prose)

# Single word replacement.
scrambler swap <user.scrambler_word> with <user.word>:
  user.scrambler_replace_word(scrambler_word, word)
# Common replacement (with "in") that performs poorly in dictation mode.
scrambler swap <user.scrambler_word> within:
  user.scrambler_replace_word(scrambler_word, "in")

# # Swap articles (a <-> the).
scrambler swap <user.scrambler_definite>:
  user.scrambler_replace_word(scrambler_definite, "a")
scrambler swap <user.scrambler_indefinite>:
  user.scrambler_replace_word(scrambler_indefinite, "the")

# Moving arguments left or right.
scrambler drag argument left: user.scrambler_move_argument_left()
scrambler drag argument right: user.scrambler_move_argument_right()

# Insert newlines relative to current line without moving the cursor.
scrambler spike line: user.scrambler_insert_line_above_current()
scrambler float line: user.scrambler_insert_line_below_current()

# Segmenting or joining words.
# Note: Including a match ordinal and search direction here makes parsing very ambiguous.
segment <user.word> <user.word>: user.scrambler_segment_word(word_1, word_2)
join up <user.word> <user.word>: user.scrambler_join_words(word_1, word_2)
hyphenate <user.word> <user.word>: user.scrambler_hyphenate_words(word_1, word_2)

# Convert a number written as words to digits ("one thousand and twenty five" -> "1025").
numberize <user.number_list_of_words>: user.scrambler_words_to_digits(number_list_of_words)

# Make a word possessive ("dog" -> "dog's", "its" -> "it's").
possessivize <user.scrambler_text_editing_match>:
  user.scrambler_make_possessive(scrambler_text_editing_match)

# Make a word plural ("dog" -> "dogs", "it" -> "its").
pluralize <user.scrambler_text_editing_match>:
  user.scrambler_make_plural(scrambler_text_editing_match)

# Make a word singular ("dogs" -> "dog", "it's" -> "it").
singularize <user.scrambler_text_editing_match>:
  user.scrambler_make_singular(scrambler_text_editing_match)
