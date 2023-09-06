mode: dictation
-
# Dictating prose with automated capitalization and spacing around punctuation.
<user.prose>$: user.dictation_insert_prose(prose)
<user.prose> anchor: user.dictation_insert_prose(prose)

# Prose ending with special formatting.
<user.prose> void:
  user.dictation_insert_prose(prose)
  insert(" ")
<user.prose> quads:
  user.dictation_insert_prose(prose)
  insert(" \"\"")
  key("left")
<user.prose> buried:
  user.dictation_insert_prose(prose)
  insert(" ``")
  key("left")
<user.prose> latex:
  user.dictation_insert_prose(prose)
  insert(" $$")
  key("left")

# Include formatters here so they can be chained with anchored prose. Chaining does not appear to work across modes.
{user.formatter}+ <user.formatter_text>$: insert(user.format_multiple(formatter_text, formatter_list))
{user.formatter}+ <user.formatter_text> anchor: insert(user.format_multiple(formatter_text, formatter_list))
{user.formatter}+ <user.formatter_text> void:
  insert(user.format_multiple(formatter_text, formatter_list))
  insert(" ")
{user.formatter}+ <user.formatter_text> (args|arcs):
  insert(user.format_multiple(formatter_text, formatter_list))
  insert("()")
  key("left")
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
^(punt|bunch|put|pudge)$: user.dictation_insert_prose(".")
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
# "now do" (chainable).
^thou do: user.mode_command()
# "style heading <number>".
^still (heading|hitting) <user.number_small>$: user.style_heading(number_small)
#"tail"
^till$: edit.line_end()
#"pasty"
^hasty$: edit.paste()

# Ignore anchors that get split up from their original command.
# Note: The word "anchor" must be escaped to be written in dictation mode.
anchor: skip()
