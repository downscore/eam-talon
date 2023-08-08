mode: dictation
-
# Dictating prose with automated capitalization and spacing around punctuation.
<user.prose>$: user.dictation_insert_prose(prose)
<user.prose> anchor: user.dictation_insert_prose(prose)

# Escaping to type things that would otherwise be commands.
^escape <user.prose>$: user.dictation_insert_prose(prose)

# Misrecognition of "command mode".
^commandment$:
  mode.disable("sleep")
  mode.disable("dictation")
  mode.enable("command")

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
^<user.repeat_ordinal>$: core.repeat_command(repeat_ordinal)

# Convenience commands for common actions
^gail [<user.repeat_ordinal>]$:
  edit.down()
  repeat(repeat_ordinal or 0)
  edit.line_end()
^spam$: insert(", ")
^disk$: edit.save()

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
^enter [<user.ordinals_small>]$: key("enter:{ordinals_small or 1}")
^slap [<user.repeat_ordinal>]$:
  edit.line_insert_down()
  repeat(repeat_ordinal or 0)
^pour line$: edit.line_insert_down()
^drink line$: edit.line_insert_up()

# Navigation.
^push [<user.repeat_ordinal>]$:
  edit.right()
  repeat(repeat_ordinal or 0)
^pull [<user.repeat_ordinal>]$:
  edit.left()
  repeat(repeat_ordinal or 0)
^goop [<user.repeat_ordinal>]$:
  edit.up()
  repeat(repeat_ordinal or 0)
^gown [<user.repeat_ordinal>]$:
  edit.down()
  repeat(repeat_ordinal or 0)
^stone [<user.repeat_ordinal>]$:
  edit.word_left()
  repeat(repeat_ordinal or 0)
^step [<user.repeat_ordinal>]$:
  edit.word_right()
  repeat(repeat_ordinal or 0)
^head$: edit.line_start()
^(tail|tale)$: edit.line_end()
^jump top$: edit.file_start()
^jump bottom$: edit.file_end()

# Selection.
^take line$: edit.select_line()
^take all$: edit.select_all()
^take left [<user.repeat_ordinal>]$:
  edit.extend_left()
  repeat(repeat_ordinal or 0)
^take right [<user.repeat_ordinal>]$:
  edit.extend_right()
  repeat(repeat_ordinal or 0)
^take up [<user.repeat_ordinal>]$:
  edit.extend_line_up()
  repeat(repeat_ordinal or 0)
^take down [<user.repeat_ordinal>]$:
  edit.extend_line_down()
  repeat(repeat_ordinal or 0)
^take word$: edit.select_word()
^lefter [<user.repeat_ordinal>]$:
  edit.extend_word_left()
  repeat(repeat_ordinal or 0)
^righter [<user.repeat_ordinal>]$:
  edit.extend_word_right()
  repeat(repeat_ordinal or 0)
^take head$: edit.extend_line_start()
^take tail$: edit.extend_line_end()
^take top$: edit.extend_file_start()
^take bottom$: edit.extend_file_end()

# Deleting text.
^wiper [<user.repeat_ordinal>]$:
  key(backspace)
  repeat(repeat_ordinal or 0)
^chuck line [<user.repeat_ordinal>]$:
  edit.delete_line()
  repeat(repeat_ordinal or 0)
^chuck left [<user.repeat_ordinal>]$:
  key(backspace)
  repeat(repeat_ordinal or 0)
^chuck right [<user.repeat_ordinal>]$:
  key(delete)
  repeat(repeat_ordinal or 0)
^chuck word [<user.repeat_ordinal>]$:
  edit.delete_word()
  repeat(repeat_ordinal or 0)
^scratcher [<user.repeat_ordinal>]$:
  user.delete_word_left()
  repeat(repeat_ordinal or 0)
^swallow [<user.repeat_ordinal>]$:
  user.delete_word_right()
  repeat(repeat_ordinal or 0)
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
^nope [<user.repeat_ordinal>]$:
  edit.undo()
  repeat(repeat_ordinal or 0)
^redo that$: edit.redo()

# Line manipulation
^clone line [<user.repeat_ordinal>]$:
  user.duplicate_line()
  repeat(repeat_ordinal or 0)
^drag up [<user.repeat_ordinal>]$:
  edit.line_swap_up()
  repeat(repeat_ordinal or 0)
^drag down [<user.repeat_ordinal>]$:
  edit.line_swap_down()
  repeat(repeat_ordinal or 0)

# Indentation
^dedent [<user.repeat_ordinal>]$:
  edit.indent_less()
  repeat(repeat_ordinal or 0)
^indent [<user.repeat_ordinal>]$:
  edit.indent_more()
  repeat(repeat_ordinal or 0)

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
^moji {user.unicode} [<user.repeat_ordinal>]$:
  user.insert_via_clipboard(user.unicode)
  repeat(repeat_ordinal or 0)
