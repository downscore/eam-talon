mode: command
mode: user.game
tag: user.marker_ui_showing
-
(scrape|hatch):
    user.marker_ui_hide()

<user.letter>:
    user.marker_ui_mouse_move(letter)
    mouse_click(0)
    user.marker_ui_hide()

<user.number>:
    user.marker_ui_mouse_move(number)
    mouse_click(0)
    user.marker_ui_hide()

######################################
# Original commands commented below: #
######################################

# mouser <user.marker_ui_label>:
#     user.marker_ui_mouse_move(marker_ui_label)
#     user.marker_ui_hide()

# touch <user.marker_ui_label>:
#     user.marker_ui_mouse_move(marker_ui_label)
#     mouse_click(0)
#     user.marker_ui_hide()

# touch <user.marker_ui_label> restore:
#     user.mouse_helper_position_save()
#     user.marker_ui_mouse_move(marker_ui_label)
#     mouse_click(0)
#     user.marker_ui_hide()
#     user.mouse_helper_position_restore()

# right <user.marker_ui_label>:
#     user.marker_ui_mouse_move(marker_ui_label)
#     mouse_click(1)
#     user.marker_ui_hide()

# middle <user.marker_ui_label>:
#     user.marker_ui_mouse_move(marker_ui_label)
#     mouse_click(2)
#     user.marker_ui_hide()

# # Versions that don't close the overlay
# mouser <user.marker_ui_label> more:
#     user.marker_ui_mouse_move(marker_ui_label)

# touch <user.marker_ui_label> more:
#     user.marker_ui_mouse_move(marker_ui_label)
#     mouse_click(0)

# touch <user.marker_ui_label> more restore:
#     user.mouse_helper_position_save()
#     user.marker_ui_mouse_move(marker_ui_label)
#     mouse_click(0)
#     user.mouse_helper_position_restore()

# right <user.marker_ui_label> more:
#     user.marker_ui_mouse_move(marker_ui_label)
#     mouse_click(1)

# middle <user.marker_ui_label> more:
#     user.marker_ui_mouse_move(marker_ui_label)
#     mouse_click(2)
