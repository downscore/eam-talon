mode: dictation
-
# Dictating prose with automated capitalization and spacing around punctuation.
<user.prose>$: user.dictation_insert_prose(prose)
<user.prose> anchor: user.dictation_insert_prose(prose)
<user.prose> void:
  user.dictation_insert_prose(prose)
  insert(" ")

# Include formatters here so they can be chained with anchored prose. Chaining does not appear to work across modes.
{user.formatter}+ <user.text>$: insert(user.format_multiple(text, formatter_list))
{user.formatter}+ <user.text> anchor: insert(user.format_multiple(text, formatter_list))
{user.formatter}+ <user.text> void:
  insert(user.format_multiple(text, formatter_list))
  insert(" ")
title <user.prose>$: insert(user.format_title(prose))
title <user.prose> anchor: insert(user.format_title(prose))
title <user.prose> void:
  insert(user.format_title(prose))
  insert(" ")

# Escaping to type things that would otherwise be commands.
^escape <user.prose>$: user.dictation_insert_prose(prose)

# Insert punctuation with automatic spacing.
scratcher punch:
  user.delete_word_left()
  user.dictation_insert_prose(".")
punch: user.dictation_insert_prose(".")
scratcher drip:
  user.delete_word_left()
  user.dictation_insert_prose(",")
drip: user.dictation_insert_prose(",")

# Fixes for some commands that are poorly recognized in dictation mode.
# "punch"
^(punt|bunch)$: user.dictation_insert_prose(".")
# "drip"
^(chip|trip)$: user.dictation_insert_prose(",")
# "args"
^arcs$:
  insert("()")
  key("left")
# "void args"
^void arcs$:
  insert(" ()")
  key("left")
# "command mode".
^commandment$: user.mode_command()

# Ignore anchors that get split up from their original command.
# Note: The word "anchor" must be escaped to be written in dictation mode.
anchor: skip()
