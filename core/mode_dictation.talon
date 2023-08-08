mode: dictation
-
# Dictating prose with automated capitalization and spacing around punctuation.
<user.prose>$: user.dictation_insert_prose(prose)
<user.prose> anchor: user.dictation_insert_prose(prose)

# Escaping to type things that would otherwise be commands.
^escape <user.prose>$: user.dictation_insert_prose(prose)

# Misrecognition of "command mode".
^commandment$: user.mode_command()

# Formatted prose.
format title <user.prose>$: user.dictation_insert_prose(user.format_title(prose))
format title <user.prose> anchor: user.dictation_insert_prose(user.format_title(prose))
format title <user.prose> void:
  user.dictation_insert_prose(user.format_title(prose))
  insert(" ")
^reformat title$: user.format_selection_title()
format {user.formatter}+ <user.text>$: user.dictation_insert_prose(user.format_multiple(text, formatter_list))
format {user.formatter}+ <user.text> anchor: user.dictation_insert_prose(user.format_multiple(text, formatter_list))
format {user.formatter}+ <user.text> void:
  user.dictation_insert_prose(user.format_multiple(text, formatter_list))
  insert(" ")
^reformat {user.formatter}+$: user.format_selection(formatter_list)

# Ignore anchors that get split up from their original command.
# Note: The word "anchor" must be escaped to be written in dictation mode.
anchor: skip()

# Pressing keys.
^press <user.modifiers>$: key(modifiers)
^press <user.modifiers> <user.unmodified_key>$: key("{modifiers}-{unmodified_key}")
^press <user.unmodified_key>$: key("{unmodified_key}")

# Switch to command mode and execute a chained command.
now do [<phrase>]$:
    user.mode_command()
    user.rephrase(phrase or "")
