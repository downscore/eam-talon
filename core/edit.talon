# Convenience commands for common actions
gail:
  edit.down()
  edit.line_end()
spam: insert(", ")
disk: edit.save()
join lines:
  edit.line_end()
  edit.line_start()
  edit.extend_line_start()
  key(backspace:2)
  key(space)
# Double tap escape
hatch: key(escape:2)

# Pick an item from a menu where the first item is highlighted by default (e.g. Intellisense menu in VS Code).
pick <user.number_small>: key("down:{number_small-1} enter")

# Symbol convenience commands
arcs:
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
# "Latex" is commonly misheard as "playtex" in dictation mode.
(latex|playtex):
  insert("$$")
  key(left)
bracing:
  insert("{}")
  key(left)
dunder:
  insert("____")
  key(left:2)
pointer: "->"
dub pointer: "=>"

# New lines
slap: edit.line_insert_down()
drink line: edit.line_insert_up()

# Navigation
push: edit.right()
pull: edit.left()
goop: edit.up()
gown: edit.down()
stone: edit.word_left()
step: edit.word_right()
head: edit.line_start()
tail: edit.line_end()
jump top: edit.file_start()
jump bottom: edit.file_end()
before fragment <user.number>: user.fragment_cursor_before(number)
after fragment <user.number>: user.fragment_cursor_after(number)
before car <user.number>:
  user.select_character_range(number_1, 0)
  key(left)
after car <user.number>:
  user.select_character_range(number_1, 0)
  key(right)

# Selection
take line: edit.select_line()
take left: edit.extend_left()
take right: edit.extend_right()
take up: edit.extend_line_up()
take down: edit.extend_line_down()
take word: edit.select_word()
lefter: edit.extend_word_left()
writer: edit.extend_word_right()
select all: edit.select_all()
select head: edit.extend_line_start()
select tail: edit.extend_line_end()
select top: edit.extend_file_start()
select bottom: edit.extend_file_end()
puffer: user.expand_selection_to_adjacent_characters()
fragment <user.number>: user.fragment_select(number)
fragment head <user.number>: user.fragment_select_head(number)
fragment tail <user.number>: user.fragment_select_tail(number)
car <user.number> [past <user.number>]: user.select_character_range(number_1, number_2 or 0)

# Deleting
chuck line: edit.delete_line()
chuck left: key(backspace)
chuck right: key(delete)
chuck up:
  edit.extend_line_up()
  edit.delete()
chuck down:
  edit.extend_line_down()
  edit.delete()
chuck word: edit.delete_word()
scratcher: user.delete_word_left()
swallow: user.delete_word_right()
chuck head: user.delete_to_line_start()
chuck tail: user.delete_to_line_end()
chuck top:
  edit.extend_file_start()
  edit.delete()
chuck bottom:
  edit.extend_file_end()
  edit.delete()
chuck fragment <user.number>: user.fragment_delete(number)
chuck car <user.number> [past <user.number>]:
  user.select_character_range(number_1, number_2 or 0)
  edit.delete()

# Copying to clipboard
copy that: user.clipboard_history_copy()
copy no history: edit.copy()
copy word:
  edit.select_word()
  user.clipboard_history_copy()
copy lefter:
  edit.extend_word_left()
  user.clipboard_history_copy()
copy righter:
  edit.extend_word_right()
  user.clipboard_history_copy()
copy line:
  edit.select_line()
  user.clipboard_history_copy()
copy head:
  edit.extend_line_start()
  user.clipboard_history_copy()
copy tail:
  edit.extend_line_end()
  user.clipboard_history_copy()

# Cutting to clipboard
cut that: user.clipboard_history_cut()
cut no history: edit.cut()
cut word:
  edit.select_word()
  user.clipboard_history_cut()
cut lefter:
  edit.extend_word_left()
  user.clipboard_history_cut()
cut righter:
  edit.extend_word_right()
  user.clipboard_history_cut()
cut line:
  edit.select_line()
  user.clipboard_history_cut()
cut head:
  edit.extend_line_start()
  user.clipboard_history_cut()
cut tail:
  edit.extend_line_end()
  user.clipboard_history_cut()

# Pasting from clipboard or clipboard history
pasty: edit.paste()
paste match: edit.paste_match_style()
paste history <user.number_small>: user.clipboard_history_paste(number_small)
paste line:
  edit.line_start()
  edit.line_start()
  edit.paste()

# Undo and redo
nope: edit.undo()
redo that: edit.redo()

# Searching and replacing
hunt file: edit.find()
hunt next: edit.find_next()
hunt last: edit.find_previous()
hunt all: user.find_everywhere()
replace file: user.replace()
replace all: user.replace_everywhere()
jump last <user.word>: user.jump_to_last_occurrence(user.word)
jump next <user.word>: user.jump_to_next_occurrence(user.word)

# Line manipulation
clone line: user.duplicate_line()
drag up: edit.line_swap_up()
drag down: edit.line_swap_down()

# Indentation
dedent: edit.indent_less()
indent: edit.indent_more()

# Zoom
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
zoom reset: edit.zoom_reset()

# Surrounding text with symbols.
inside singles:
  user.surround_selected_text("'", "'")
inside doubles:
  user.surround_selected_text("\"", "\"")
inside escaped singles:
  user.surround_selected_text("\\'", "\\'")
inside escaped doubles:
  user.surround_selected_text("\\\"", "\\\"")
inside parens:
  user.surround_selected_text("(", ")")
inside squares:
  user.surround_selected_text("[", "]")
inside braces:
  user.surround_selected_text("{{", "}}")
inside percents:
  user.surround_selected_text("%", "%")
inside (graves | back ticks):
  user.surround_selected_text("`", "`")
inside spaces:
	user.surround_selected_text(" ", " ")
inside triangles:
  user.surround_selected_text("<", ">")
inside dollars:
  user.surround_selected_text("$", "$")

# Insert a link or make the selected text into a link.
link insert: user.insert_link()
link paste: user.insert_link_from_clipboard()

# Text styles
style title: user.style_title()
style subtitle: user.style_subtitle()
style heading <user.number_small>: user.style_heading(number_small)
style body: user.style_body()
style bold: user.style_bold()
style italic: user.style_italic()
style underline: user.style_underline()
style strike through: user.style_strikethrough()
style highlight: user.style_highlight()
style bullet list: user.style_bullet_list()
style numbered list: user.style_numbered_list()
style checklist: user.style_checklist()
style check dog: user.style_toggle_check()

# Counting/sorting lines
count lines: user.count_lines()
count words: user.count_words()
count characters: user.count_characters()
sort lines: user.sort_lines_ascending()
sort lines descending: user.sort_lines_descending()

# Special characters.
moji hunt: key("cmd-ctrl-space")
moji {user.unicode}: user.insert_via_clipboard(user.unicode)
