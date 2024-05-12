<user.formatters> <user.formatter_text>$: insert(user.format_multiple(formatter_text, formatters))
<user.formatters> <user.formatter_text> anchor: insert(user.format_multiple(formatter_text, formatters))
<user.formatters> <user.formatter_text> void:
  insert(user.format_multiple(formatter_text, formatters))
  insert(" ")
<user.formatters> <user.formatter_text> arcs:
  insert(user.format_multiple(formatter_text, formatters))
  insert("()")
  key("left")
<user.formatters> <user.formatter_text> punch:
  insert(user.format_multiple(formatter_text, formatters))
  insert(".")
<user.formatters> <user.formatter_text> assign:
  insert(user.format_multiple(formatter_text, formatters))
  insert(" = ")
reformat <user.formatters>: user.format_selection(formatters)

# "phrase" is used to insert the all of the following text verbatim.
# "say/title/clause" support punctuation keywords (via "prose") and anchoring.
# Anchored "say/title/clause" commands can be chained with other commands.
say <user.prose>$: insert(prose)
say <user.prose> anchor: insert(prose)
say <user.prose> void:
  insert(prose)
  insert(" ")
phrase <user.text>$: insert(text)
reformat phrase: user.format_selection_phrase()

title <user.prose>$: insert(user.format_title_with_history(prose))
title <user.prose> anchor: insert(user.format_title_with_history(prose))
title <user.prose> void:
  insert(user.format_title_with_history(prose))
  insert(" ")
reformat title: user.format_selection_title()

clause <user.prose>$: insert(user.format_sentence(prose))
clause <user.prose> anchor: insert(user.format_sentence(prose))
clause <user.prose> void:
  insert(user.format_sentence(prose))
  insert(" ")
reformat clause: user.format_selection_sentence()

word <user.word>: insert(user.word)
ship word <user.word>: insert(user.format_title(user.word))

# Repeat the last thing a formatter output.
repeat {user.formatter}: insert(user.format_replay(formatter))
repeat title: insert(user.format_replay_title())
repeat clause: insert(user.format_replay_sentence())

# Convenience reformatting commands consistent with TextFlow commands.
bigger that: user.format_selection_title()
smaller that: user.format_selection_phrase()
biggest that: user.format_selection_single("allcaps")
