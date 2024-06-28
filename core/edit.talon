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
gail:
  user.down()
  user.line_end()
stone: user.word_left()
step: user.word_right()
head: user.line_start()
tail: user.line_end()
jump top: user.file_start()
jump bottom: user.file_end()
before fragment <user.number>: user.fragment_cursor_before(number)
after fragment <user.number>: user.fragment_cursor_after(number)
before car <user.number>:
  user.character_select_range(number_1, 0)
  key(left)
after car <user.number>:
  user.character_select_range(number_1, 0)
  key(right)

# Selection
# Poor recognition for "pick line", so added "icline" to help.
(pick line|icline): user.select_line_excluding_line_break()
pick left: user.extend_left()
pick right: user.extend_right()
pick up: user.extend_up()
pick down: user.extend_down()
pick page up: user.extend_page_up()
pick page down: user.extend_page_down()
pick word: user.select_word()
lefter: user.extend_word_left()
writer: user.extend_word_right()
pick everything: user.select_all()
pick head: user.extend_line_start()
pick tail: user.extend_line_end()
pick top: user.extend_file_start()
pick bottom: user.extend_file_end()
fragment <user.number> [past <user.number>]: user.fragment_select(number_1, number_2 or 0)
fragment head <user.number>: user.fragment_select_head(number)
fragment tail <user.number>: user.fragment_select_tail(number)
fragment next: user.fragment_select_next()
fragment last: user.fragment_select_previous()
car <user.number> [past <user.number>]: user.character_select_range(number_1, number_2 or 0)
car next: user.character_select_next()
car last: user.character_select_previous()
line next:
  user.down()
  user.select_line_excluding_line_break()
line last:
  user.up()
  user.line_end()
  user.select_line_excluding_line_break()


# Manipulating selections.
puffer: user.expand_selection_to_adjacent_characters()
shrinker: user.shrink_selection_by_first_and_last_characters()
sharpen: user.delete_first_and_last_characters_maintain_selection()

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
chuck everything: user.delete_all()
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
chuck fragment [<user.number>] [past <user.number>]: user.fragment_delete(number_1 or -1, number_2 or 0)
chuck car <user.number> [past <user.number>]:
  user.character_select_range(number_1, number_2 or 0)
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
copy writer:
  user.extend_word_right()
  user.clipboard_history_copy()
copy line:
  user.select_line_including_line_break()
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
cut writer:
  user.extend_word_right()
  user.clipboard_history_cut()
cut line:
  user.select_line_including_line_break()
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
pastry <user.number_small>: user.clipboard_history_paste(number_small)
paste line:
  user.line_start()
  user.line_start()
  user.paste()
# Paste clipboard contents with "insert" to bypass restrictions on pasting.
dont fuck with paste: user.paste_via_insert()

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
join lines:
  user.line_end()
  user.line_start()
  user.extend_line_start()
  key(backspace:2)
  key(space)

# Indentation
dedent: user.indent_less()
indent: user.indent_more()

# Zoom
zoom in: user.zoom_in()
zoom out: user.zoom_out()
zoom reset: user.zoom_reset()

# Surrounding text with symbols.
inside singles: user.surround_selected_text("'", "'")
inside doubles: user.surround_selected_text("\"", "\"")
inside escaped singles: user.surround_selected_text("\\'", "\\'")
inside escaped doubles: user.surround_selected_text("\\\"", "\\\"")
inside parens: user.surround_selected_text("(", ")")
inside squares: user.surround_selected_text("[", "]")
inside braces: user.surround_selected_text("{{", "}}")
inside percents: user.surround_selected_text("%", "%")
inside (graves | back ticks): user.surround_selected_text("`", "`")
inside spaces: user.surround_selected_text(" ", " ")
inside triangles: user.surround_selected_text("<", ">")
inside dollars: user.surround_selected_text("$", "$")
inside block comment: user.surround_selected_text("/*", "*/")

# Pushing symbols around.
shove left: user.push_word_left()
shove right: user.push_word_right()

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
style bullet: user.style_bullet_list()
style numbered: user.style_numbered_list()
style checklist: user.style_checklist()
style check dog: user.style_toggle_check()

# Counting/sorting lines
count lines: user.count_lines()
count words: user.count_words()
count characters: user.count_characters()
sort lines: user.sort_lines_ascending()
sort lines descending: user.sort_lines_descending()

# Insert a link or make the selected text into a link.
link insert: user.insert_link()
link paste: user.insert_link_from_clipboard()
link self: user.insert_self_link()
link browser: user.insert_link_from_browser_address()

# Flip booleans or comparisons.
flipper: user.flip_boolean_or_comparison()

# Comma and space
spam: insert(", ")

# Double tap escape
hatch: key(escape:2)

# Choose an item from a menu where the first item is highlighted by default (e.g. Intellisense menu in VS Code).
choose <user.number_small>: key("down:{number_small-1} enter")
# "choose six" has really bad recognition, so we have a special command for it.
choosix: key("down:5 enter")

# Save open file
disk: user.save()

# Default to markdown-style blocks if no language is active.
make block:
  insert("```\n\n```")
  key("left:4")

# Special characters.
hunt moji: key("cmd-ctrl-space")
moji {user.unicode}: user.insert_via_clipboard(user.unicode)
