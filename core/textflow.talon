# Core commands - Single compound target.
<user.textflow_command_type> <user.textflow_compound_target>:
  user.textflow_execute_command(textflow_command_type, textflow_compound_target)

# Core commands - Compound target starting from the cursor position.
<user.textflow_command_type> <user.textflow_target_combo_type> <user.textflow_simple_target>:
  user.textflow_execute_command_from_cursor(textflow_command_type, textflow_target_combo_type, textflow_simple_target)

# Core commands - Single word target.
<user.textflow_command_type> <user.textflow_word>:
  user.textflow_execute_command(textflow_command_type, textflow_word)
# Escaped version of the above.
<user.textflow_command_type> scrape <user.textflow_word>:
  user.textflow_execute_command(textflow_command_type, textflow_word)

# Core commands - Articles (a/the) as target. e.g. "grab indefinite".
# This is hard to do with other commands. e.g. "grab a" will select any word with the letter "a" in it.
<user.textflow_command_type> <user.textflow_definite>:
  user.textflow_execute_command(textflow_command_type, textflow_definite)
<user.textflow_command_type> <user.textflow_indefinite>:
  user.textflow_execute_command(textflow_command_type, textflow_indefinite)

# Selection commands using TextFlow modifiers.
pick sentence: user.textflow_select_sentence()
pick scope: user.textflow_select_scope()
pick argument: user.textflow_select_argument()
pick string: user.textflow_select_string()
pick comment: user.textflow_select_comment()
pick brackets: user.textflow_select_brackets()
pick invoke: user.textflow_select_function_call()

# Deletion commands using TextFlow modifiers.
chuck sentence: user.textflow_delete_sentence()
chuck scope: user.textflow_delete_scope()
chuck argument: user.textflow_delete_argument()
chuck string: user.textflow_delete_string()
chuck comment: user.textflow_delete_comment()
chuck brackets: user.textflow_delete_brackets()
chuck invoke: user.textflow_delete_function_call()

# Copy commands using TextFlow modifiers.
copy sentence:
  user.textflow_select_sentence()
  user.clipboard_history_copy()
copy scope:
  user.textflow_select_scope()
  user.clipboard_history_copy()
copy argument:
  user.textflow_select_argument()
  user.clipboard_history_copy()
copy string:
  user.textflow_select_string()
  user.clipboard_history_copy()
copy comment:
  user.textflow_select_comment()
  user.clipboard_history_copy()
copy brackets:
  user.textflow_select_brackets()
  user.clipboard_history_copy()
copy invoke:
  user.textflow_select_function_call()
  user.clipboard_history_copy()

# Cut commands using TextFlow modifiers.
cut sentence: user.textflow_cut_sentence()
cut scope: user.textflow_cut_scope()
cut argument: user.textflow_cut_argument()
cut string: user.textflow_cut_string()
cut comment: user.textflow_cut_comment()
cut brackets: user.textflow_cut_brackets()
cut invoke: user.textflow_cut_function_call()

# Navigating using TextFlow modifiers. These commands should be kept to a minimum, as they may make it harder to
# navigate in prose. E.g. "before sentence" can no longer be used to put the cursor in front of the word "sentence".
# The escaped version, "before scrape sentence", must be used instead.
before sentence: user.textflow_move_before_sentence()
after sentence: user.textflow_move_after_sentence()

# Moving arguments left or right.
drag argument left: user.textflow_move_argument_left()
drag argument right: user.textflow_move_argument_right()

# Insert newlines relative to target.
drink <user.textflow_simple_target>: user.textflow_new_line_above(textflow_simple_target)
pour <user.textflow_simple_target>: user.textflow_new_line_below(textflow_simple_target)

# Insert newlines relative to current line without moving the cursor.
spike line: user.textflow_insert_line_above_current()
float line: user.textflow_insert_line_below_current()

# Replace a target with prose (includes punctuation).
swap <user.textflow_compound_target> with <user.prose>$: user.textflow_replace(textflow_compound_target, prose)
swap <user.textflow_compound_target> with <user.prose> anchor: user.textflow_replace(textflow_compound_target, prose)

# Single word replacement.
swap <user.textflow_word> with <user.word>: user.textflow_replace_word(textflow_word, word)

# Swap articles (a <-> the).
swap <user.textflow_definite>: user.textflow_replace_word(textflow_definite, "a")
swap <user.textflow_indefinite>: user.textflow_replace_word(textflow_indefinite, "the")

# Segmenting or joining words.
# Note: Including a match ordinal and search direction here makes parsing very ambiguous.
segment <user.word> <user.word>: user.textflow_segment_word(word_1, word_2)
join up <user.word> <user.word>: user.textflow_join_words(word_1, word_2)
hyphenate <user.word> <user.word>: user.textflow_hyphenate_words(word_1, word_2)

# Convert a number written as words to digits ("one thousand and twenty five" -> "1025").
numberize <user.number_list_of_words>: user.textflow_words_to_digits(number_list_of_words)

# Make a word possessive ("dog" -> "dog's", "its" -> "it's").
possessivize <user.textflow_word>: user.textflow_make_possessive(textflow_word)
possessivize <user.textflow_compound_target>: user.textflow_make_possessive(textflow_compound_target)

# Make a word plural ("dog" -> "dogs", "it" -> "its").
pluralize <user.textflow_word>: user.textflow_make_plural(textflow_word)
pluralize <user.textflow_compound_target>: user.textflow_make_plural(textflow_compound_target)

# Make a word singular ("dogs" -> "dog", "it's" -> "it").
singularize <user.textflow_word>: user.textflow_make_singular(textflow_word)
singularize <user.textflow_compound_target>: user.textflow_make_singular(textflow_compound_target)

# Surround a word or target in quotes.
doubleize <user.textflow_word>: user.textflow_surround_text(textflow_word, "\"")
doubleize <user.textflow_compound_target>: user.textflow_surround_text(textflow_compound_target, "\"")
singleize <user.textflow_word>: user.textflow_surround_text(textflow_word, "'")
singleize <user.textflow_compound_target>: user.textflow_surround_text(textflow_compound_target, "'")

# Add a comma after a word or target.
dripize <user.textflow_word>:user.textflow_surround_text(textflow_word, "", ",")
dripize <user.textflow_compound_target>: user.textflow_surround_text(textflow_compound_target, "", ",")

# Add markdown formatting.
boldize <user.textflow_word>: user.textflow_surround_text(textflow_word, "**")
boldize <user.textflow_compound_target>: user.textflow_surround_text(textflow_compound_target, "**")
italicize <user.textflow_word>: user.textflow_surround_text(textflow_word, "*")
italicize <user.textflow_compound_target>: user.textflow_surround_text(textflow_compound_target, "*")
strike through <user.textflow_word>: user.textflow_surround_text(textflow_word, "~~")
strike through <user.textflow_compound_target>: user.textflow_surround_text(textflow_compound_target, "~~")
