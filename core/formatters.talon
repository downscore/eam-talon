{user.formatter}+ <user.text>$: insert(user.format_multiple(text, formatter_list))
{user.formatter}+ <user.text> anchor: insert(user.format_multiple(text, formatter_list))
{user.formatter}+ <user.text> void:
  insert(user.format_multiple(text, formatter_list))
  insert(" ")
reformat {user.formatter}+: user.format_selection(formatter_list)

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

title <user.prose>$: insert(user.format_title(prose))
title <user.prose> anchor: insert(user.format_title(prose))
title <user.prose> void:
  insert(user.format_title(prose))
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
