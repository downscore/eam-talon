# Convenience commands for common actions
gail:
  user.down()
  user.line_end()
spam: insert(", ")
disk: user.save()
join lines:
  user.line_end()
  user.line_start()
  user.extend_line_start()
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
slap: user.line_insert_down()
drink line: user.line_insert_up()

# Navigation
push: user.right()
pull: user.left()
goop: user.up()
gown: user.down()
stone: user.word_left()
step: user.word_right()
head: user.line_start()
tail: user.line_end()
jump top: user.file_start()
jump bottom: user.file_end()
before fragment <user.number>: user.fragment_cursor_before(number)
after fragment <user.number>: user.fragment_cursor_after(number)
before car <user.number>:
  user.select_character_range(number_1, 0)
  key(left)
after car <user.number>:
  user.select_character_range(number_1, 0)
  key(right)

# Selection
select line: user.select_line()
select left: user.extend_left()
select right: user.extend_right()
select up: user.extend_up()
select down: user.extend_down()
select page up: user.extend_page_up()
select page down: user.extend_page_down()
select word: user.select_word()
lefter: user.extend_word_left()
writer: user.extend_word_right()
select all: user.select_all()
select head: user.extend_line_start()
select tail: user.extend_line_end()
select top: user.extend_file_start()
select bottom: user.extend_file_end()
puffer: user.expand_selection_to_adjacent_characters()
fragment <user.number>: user.fragment_select(number)
fragment head <user.number>: user.fragment_select_head(number)
fragment tail <user.number>: user.fragment_select_tail(number)
car <user.number> [past <user.number>]: user.select_character_range(number_1, number_2 or 0)

# Deleting
chuck line: user.delete_line()
chuck left: key(backspace)
chuck right: key(delete)
chuck up:
  user.extend_up()
  user.delete()
chuck down:
  user.extend_down()
  user.delete()
chuck word: user.delete_word()
scratcher: user.delete_word_left()
swallow: user.delete_word_right()
chuck head: user.delete_to_line_start()
chuck tail: user.delete_to_line_end()
chuck top:
  user.extend_file_start()
  user.delete()
chuck bottom:
  user.extend_file_end()
  user.delete()
chuck fragment <user.number>: user.fragment_delete(number)
chuck car <user.number> [past <user.number>]:
  user.select_character_range(number_1, number_2 or 0)
  user.delete()

# Copying to clipboard
copy that: user.clipboard_history_copy()
copy no history: user.copy()
copy word:
  user.select_word()
  user.clipboard_history_copy()
copy lefter:
  user.extend_word_left()
  user.clipboard_history_copy()
copy righter:
  user.extend_word_right()
  user.clipboard_history_copy()
copy line:
  user.select_line()
  user.clipboard_history_copy()
copy head:
  user.extend_line_start()
  user.clipboard_history_copy()
copy tail:
  user.extend_line_end()
  user.clipboard_history_copy()

# Cutting to clipboard
cut that: user.clipboard_history_cut()
cut no history: user.cut()
cut word:
  user.select_word()
  user.clipboard_history_cut()
cut lefter:
  user.extend_word_left()
  user.clipboard_history_cut()
cut righter:
  user.extend_word_right()
  user.clipboard_history_cut()
cut line:
  user.select_line()
  user.clipboard_history_cut()
cut head:
  user.extend_line_start()
  user.clipboard_history_cut()
cut tail:
  user.extend_line_end()
  user.clipboard_history_cut()

# Pasting from clipboard or clipboard history
pasty: user.paste()
paste match: user.paste_match_style()
paste history <user.number_small>: user.clipboard_history_paste(number_small)
paste line:
  user.line_start()
  user.line_start()
  user.paste()

# Undo and redo
nope: user.undo()
redo that: user.redo()

# Searching and replacing
hunt file: user.find()
hunt next: user.find_next()
hunt last: user.find_previous()
hunt all: user.find_everywhere()
replace file: user.replace()
replace all: user.replace_everywhere()
jump last <user.word>: user.jump_to_last_occurrence(user.word)
jump next <user.word>: user.jump_to_next_occurrence(user.word)

# Line manipulation
clone line: user.duplicate_line()
drag up: user.line_swap_up()
drag down: user.line_swap_down()

# Indentation
dedent: user.indent_less()
indent: user.indent_more()

# Zoom
zoom in: user.zoom_in()
zoom out: user.zoom_out()
zoom reset: user.zoom_reset()

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
