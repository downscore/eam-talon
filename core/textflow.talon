# Core commands - Single compound target.
<user.textflow_command_type> <user.textflow_compound_target>:
  user.textflow_execute_command(textflow_command_type, textflow_compound_target)

# Core commands - Current block as target.
<user.textflow_command_type> block:
  user.textflow_execute_command_current_block(textflow_command_type)

# Core commands - Target modified to a full line. Tries to match beginning of line first.
<user.textflow_command_type> row <user.textflow_simple_target>:
  user.textflow_execute_line_command(textflow_command_type, textflow_simple_target)

# Core commands - Compound target starting from the cursor position.
<user.textflow_command_type> <user.textflow_target_combo_type> <user.textflow_simple_target>:
  user.textflow_execute_command_from_cursor(textflow_command_type, textflow_target_combo_type, textflow_simple_target)

# Core commands - Single word target.
<user.textflow_command_type> <user.textflow_word>:
  user.textflow_execute_command(textflow_command_type, textflow_word)

# Core commands - Articles (a/the) as target. e.g. "grab indefinite".
# This is hard to do with other commands. e.g. "grab a" will select any word with the letter "a" in it.
<user.textflow_command_type> <user.textflow_definite>:
  user.textflow_execute_command(textflow_command_type, textflow_definite)
<user.textflow_command_type> <user.textflow_indefinite>:
  user.textflow_execute_command(textflow_command_type, textflow_indefinite)

# Insert newline relative to target.
drink <user.textflow_simple_target>:
  user.textflow_new_line_above(textflow_simple_target)
pour <user.textflow_simple_target>:
  user.textflow_new_line_below(textflow_simple_target)

# Replace a target with prose (includes punctuation).
swap <user.textflow_compound_target> with <user.prose>$:
  user.textflow_replace(textflow_compound_target, prose)
swap <user.textflow_compound_target> with <user.prose> anchor:
  user.textflow_replace(textflow_compound_target, prose)

# Single word replacement.
swap <user.textflow_word> with <user.word>:
  user.textflow_replace_word(textflow_word, word)

# Swap articles (a <-> the).
swap <user.textflow_definite>:
  user.textflow_replace_word(textflow_definite, "a")
swap <user.textflow_indefinite>:
  user.textflow_replace_word(textflow_indefinite, "the")

# Segmenting or joining words.
# Note: Including a match ordinal and search direction here makes parsing very ambiguous.
segment <user.word> <user.word>:
  user.textflow_segment_word(word_1, word_2)
join up <user.word> <user.word>:
  user.textflow_join_words(word_1, word_2)
hyphenate <user.word> <user.word>:
  user.textflow_hyphenate_words(word_1, word_2)

# Convert a number written as words to digits ("one thousand and twenty five" -> "1025").
numberize <user.number_list_of_words>:
  user.textflow_words_to_digits(number_list_of_words)

# Make a word possessive ("dog" -> "dog's", "its" -> "it's").
possessivize <user.textflow_word>:
  user.textflow_make_possessive(textflow_word)
possessivize <user.textflow_compound_target>:
  user.textflow_make_possessive(textflow_compound_target)

# Make a word plural ("dog" -> "dogs", "it" -> "its").
pluralize <user.textflow_word>:
  user.textflow_make_plural(textflow_word)
pluralize <user.textflow_compound_target>:
  user.textflow_make_plural(textflow_compound_target)

# Make a word singular ("dogs" -> "dog", "it's" -> "it").
singularize <user.textflow_word>:
  user.textflow_make_singular(textflow_word)
singularize <user.textflow_compound_target>:
  user.textflow_make_singular(textflow_compound_target)

# Surround a word in quotes.
doubleize <user.textflow_word>:
  user.textflow_surround_text(textflow_word, "\"")
doubleize <user.textflow_compound_target>:
  user.textflow_surround_text(textflow_compound_target, "\"")
singleize <user.textflow_word>:
  user.textflow_surround_text(textflow_word, "'")
singleize <user.textflow_compound_target>:
  user.textflow_surround_text(textflow_compound_target, "'")

# Add a comma after a word.
dripize <user.textflow_word>:
  user.textflow_surround_text(textflow_word, "", ",")
dripize <user.textflow_compound_target>:
  user.textflow_surround_text(textflow_compound_target, "", ",")

# Add markdown formatting.
boldize <user.textflow_word>:
  user.textflow_surround_text(textflow_word, "**")
boldize <user.textflow_compound_target>:
  user.textflow_surround_text(textflow_compound_target, "**")
italicize <user.textflow_word>:
  user.textflow_surround_text(textflow_word, "*")
italicize <user.textflow_compound_target>:
  user.textflow_surround_text(textflow_compound_target, "*")
strike through <user.textflow_word>:
  user.textflow_surround_text(textflow_word, "~~")
strike through <user.textflow_compound_target>:
  user.textflow_surround_text(textflow_compound_target, "~~")
