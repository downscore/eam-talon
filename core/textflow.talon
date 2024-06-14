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
<user.textflow_command_type> hatch <user.textflow_word>:
  user.textflow_execute_command(textflow_command_type, textflow_word)

# Core commands - Articles (a/the) as target. e.g. "grab indefinite".
# This is hard to do with other commands. e.g. "grab a" will select any word with the letter "a" in it.
<user.textflow_command_type> <user.textflow_definite>:
  user.textflow_execute_command(textflow_command_type, textflow_definite)
<user.textflow_command_type> <user.textflow_indefinite>:
  user.textflow_execute_command(textflow_command_type, textflow_indefinite)

# Selection commands using TextFlow modifiers.
pick sentence: user.textflow_execute_command_enum_strings("SELECT", "SENTENCE")
pick scope: user.textflow_execute_command_enum_strings("SELECT", "SCOPE")
pick argument: user.textflow_execute_command_enum_strings("SELECT", "ARG")
pick doubles: user.textflow_execute_command_enum_strings("SELECT", "STRING", "\"")
pick singles: user.textflow_execute_command_enum_strings("SELECT", "STRING", "'")
pick graves: user.textflow_execute_command_enum_strings("SELECT", "STRING", "`")
pick whitespace: user.textflow_execute_command_enum_strings("SELECT", "BETWEEN_WHITESPACE")
pick link: user.textflow_execute_command_enum_strings("SELECT", "MARKDOWN_LINK")
pick comment: user.textflow_execute_command_enum_strings("SELECT", "COMMENT")
pick brackets: user.textflow_execute_command_enum_strings("SELECT", "BRACKETS")
pick invoke: user.textflow_execute_command_enum_strings("SELECT", "CALL")

# Deletion commands using TextFlow modifiers.
chuck sentence: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "SENTENCE")
chuck scope: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "SCOPE")
chuck argument: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "ARG")
chuck doubles: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "STRING", "\"")
chuck singles: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "STRING", "'")
chuck graves: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "STRING", "`")
chuck whitespace: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "BETWEEN_WHITESPACE")
chuck link: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "MARKDOWN_LINK")
chuck comment: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "COMMENT")
chuck brackets: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "BRACKETS")
chuck invoke: user.textflow_execute_command_enum_strings("CLEAR_NO_MOVE", "CALL")

# Copy commands using TextFlow modifiers.
copy sentence:
  user.textflow_execute_command_enum_strings("SELECT", "SENTENCE")
  user.clipboard_history_copy()
copy scope:
  user.textflow_execute_command_enum_strings("SELECT", "SCOPE")
  user.clipboard_history_copy()
copy argument:
  user.textflow_execute_command_enum_strings("SELECT", "ARGUMENT")
  user.clipboard_history_copy()
copy doubles:
  user.textflow_execute_command_enum_strings("SELECT", "STRING", "\"")
  user.clipboard_history_copy()
copy singles:
  user.textflow_execute_command_enum_strings("SELECT", "STRING", "'")
  user.clipboard_history_copy()
copy graves:
  user.textflow_execute_command_enum_strings("SELECT", "STRING", "`")
  user.clipboard_history_copy()
copy whitespace:
  user.textflow_execute_command_enum_strings("SELECT", "BETWEEN_WHITESPACE")
  user.clipboard_history_copy()
copy link:
  user.textflow_execute_command_enum_strings("SELECT", "MARKDOWN_LINK")
  user.clipboard_history_copy()
copy comment:
  user.textflow_execute_command_enum_strings("SELECT", "COMMENT")
  user.clipboard_history_copy()
copy brackets:
  user.textflow_execute_command_enum_strings("SELECT", "BRACKETS")
  user.clipboard_history_copy()
copy invoke:
  user.textflow_execute_command_enum_strings("SELECT", "CALL")
  user.clipboard_history_copy()

# Cut commands using TextFlow modifiers.
cut sentence: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "SENTENCE")
cut scope: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "SCOPE")
cut argument: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "ARG")
cut doubles: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "STRING", "\"")
cut singles: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "STRING", "'")
cut graves: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "STRING", "`")
cut whitespace: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "BETWEEN_WHITESPACE")
cut link: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "MARKDOWN_LINK")
cut comment: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "COMMENT")
cut brackets: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "BRACKETS")
cut invoke: user.textflow_execute_command_enum_strings("CUT_TO_CLIPBOARD", "CALL")

# Navigating using TextFlow modifiers. These commands should be kept to a minimum, as they may make it harder to
# navigate in prose. E.g. "before sentence" can no longer be used to put the cursor in front of the word "sentence".
# The escaped version, "before hatch sentence", must be used instead.
before sentence: user.textflow_execute_command_enum_strings("MOVE_CURSOR_BEFORE", "SENTENCE")
after sentence: user.textflow_execute_command_enum_strings("MOVE_CURSOR_AFTER", "SENTENCE")

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
# Common replacement (with "in") that performs poorly in dictation mode.
swap <user.textflow_word> within: user.textflow_replace_word(textflow_word, "in")

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

# Special homophones.
phony they are: user.textflow_swap_homophone_to_word("they're")
phony over there: user.textflow_swap_homophone_to_word("there")
phony their possessive: user.textflow_swap_homophone_to_word("their")
