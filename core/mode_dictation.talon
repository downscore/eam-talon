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

# Include symbol convenience commands so they can be chained with anchored prose.
# Symbol convenience commands
args:
  insert("()")
  key(left)
subscript:
  insert("[]")
  key(left)
quads:
  insert("\"\"")
  key(left)
padding:
  insert("  ")
  key(left)
buried:
  insert("``")
  key(left)
diamond:
  insert("<>")
  key(left)
latex:
  insert("$$")
  key(left)
bracing:
  insert("{}")
  key(left)

# Escaping to type things that would otherwise be commands.
^escape <user.prose>$: user.dictation_insert_prose(prose)

# Misrecognition of "command mode".
^commandment$: user.mode_command()

# Ignore anchors that get split up from their original command.
# Note: The word "anchor" must be escaped to be written in dictation mode.
anchor: skip()

# Switch to command mode and execute a chained command.
now do [<phrase>]$:
    user.mode_command()
    user.rephrase(phrase or "")
