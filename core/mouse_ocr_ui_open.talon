mode: command
mode: user.game
tag: user.mouse_ocr_ui_open
-
# Using (scrape|hatch) doesn't properly override edit "hatch" command.
scrape: user.mouse_ocr_ui_hide()
hatch: user.mouse_ocr_ui_hide()
<user.letter>: user.mouse_ocr_ui_activate_label(letter)
<user.number>: user.mouse_ocr_ui_activate_label(number)
