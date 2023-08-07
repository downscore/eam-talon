mode: dictation
-
# Dictating prose with automated capitalization and spacing around punctuation.
<user.prose>$: user.dictation_insert_prose(prose)
<user.prose> anchor: user.dictation_insert_prose(prose)

# Escaping to type things that would otherwise be commands.
^escape <user.prose>$: user.dictation_insert_prose(prose)

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

# Repeat last command.
^<user.ordinals_small>$: core.repeat_command(ordinals_small - 1)

# Symbol convenience commands
^args$:
  user.dictation_insert_prose("()")
  key(left)
^subscript$:
  user.dictation_insert_prose("[]")
  key(left)
^quads$:
  user.dictation_insert_prose("\"\"")
  key(left)
^padding$:
  user.dictation_insert_prose("  ")
  key(left)
^buried$:
  user.dictation_insert_prose("``")
  key(left)
^diamond$:
  user.dictation_insert_prose("<>")
  key(left)

# New lines.
^enter$: key("enter")
^slap$: edit.line_insert_down()
^pour line$: edit.line_insert_down()
^drink line$: edit.line_insert_up()

# Navigation.
^push$: edit.right()
^pull$: edit.left()
^goop$: edit.up()
^gown$: edit.down()
^stone$: edit.word_left()
^step$: edit.word_right()
^head$: edit.line_start()
^(tail|tale)$: edit.line_end()
^jump top$: edit.file_start()
^jump bottom$: edit.file_end()
^gail$:
  edit.down()
  edit.line_end()

# Selection.
^take line$: edit.select_line()
^take all$: edit.select_all()
^take left$: edit.extend_left()
^take right$: edit.extend_right()
^take up$: edit.extend_line_up()
^take down$: edit.extend_line_down()
^take word$: edit.select_word()
^lefter$: edit.extend_word_left()
^righter$: edit.extend_word_right()
^take head$: edit.extend_line_start()
^take tail$: edit.extend_line_end()
^take top$: edit.extend_file_start()
^take bottom$: edit.extend_file_end()

# Deleting text.
^wiper$: key(backspace)
^chuck line$: edit.delete_line()
^chuck left$: key(backspace)
^chuck right$: key(delete)
^chuck word$: edit.delete_word()
^scratcher$: user.delete_word_left()
^swallow$: user.delete_word_right()
^chuck head$: user.delete_to_line_start()
^chuck tail$: user.delete_to_line_end()

# Clipboard.
^copy that$: user.clipboard_history_copy()
^copy no history$: edit.copy()
^copy word$:
  edit.select_word()
  user.clipboard_history_copy()
^copy lefter$:
  edit.extend_word_left()
  user.clipboard_history_copy()
^copy righter$:
  edit.extend_word_right()
  user.clipboard_history_copy()
^copy line$:
  edit.select_line()
  user.clipboard_history_copy()
^copy head$:
  edit.extend_line_start()
  user.clipboard_history_copy()
^copy tail$:
  edit.extend_line_end()
  user.clipboard_history_copy()
^cut that$: user.clipboard_history_cut()
^cut no history$: edit.cut()
^cut word$:
  edit.select_word()
  user.clipboard_history_cut()
^cut lefter$:
  edit.extend_word_left()
  user.clipboard_history_cut()
^cut righter$:
  edit.extend_word_right()
  user.clipboard_history_cut()
^cut line$:
  edit.select_line()
  user.clipboard_history_cut()
^cut head$:
  edit.extend_line_start()
  user.clipboard_history_cut()
^cut tail$:
  edit.extend_line_end()
  user.clipboard_history_cut()
^pasty$: edit.paste()
^paste match$: edit.paste_match_style()
^paste history <user.number_small>$: user.clipboard_history_paste(number_small)

# Undo and redo.
^nope$: edit.undo()
^redo that$: edit.redo()

# Line manipulation
^clone line$: user.duplicate_line()
^drag up$: edit.line_swap_up()
^drag down$: edit.line_swap_down()

# Indentation
^dedent$: edit.indent_less()
^indent$: edit.indent_more()

# Text styles
^style title$: user.style_title()
^style subtitle$: user.style_subtitle()
^style heading <user.number_small>$: user.style_heading(number_small)
^style body$: user.style_body()
^style bold$: user.style_bold()
^style italic$: user.style_italic()
^style underline$: user.style_underline()
^style strike through$: user.style_strikethrough()
^style bullet list$: user.style_bullet_list()
^style numbered list$: user.style_numbered_list()
^style checklist$: user.style_checklist()
^style check dog$: user.style_toggle_check()

# Special characters.
^moji hunt$: key("cmd-ctrl-space")
^moji {user.unicode}$: user.insert_via_clipboard(user.unicode)
