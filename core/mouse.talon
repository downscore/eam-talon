# Move the mouse.
slide <user.mouse_directions>: user.mouse_move_delta(mouse_directions)

# Click at current position.
mouse touch: mouse_click()
mouse right: mouse_click(1)
mouse middle: mouse_click(2)
<user.modifiers> mouse touch:
    key("{modifiers}:down")
    mouse_click(0)
    key("{modifiers}:up")
<user.modifiers> mouse right:
    key("{modifiers}:down")
    mouse_click(1)
    key("{modifiers}:up")

# Scroll mouse wheel.
scroll north: mouse_scroll(100.0)
scroll south: mouse_scroll(-100.0)
scroll up: mouse_scroll(500.0)
scroll down: mouse_scroll(-500.0)
scroll left: mouse_scroll(0.0, 100.0)
scroll right: mouse_scroll(0.0, -100.0)

# OCR mouse control.
mouser <user.prose>: user.mouse_ocr_move(prose)
toucher <user.prose>: user.mouse_ocr_click(prose)
right toucher <user.prose>: user.mouse_ocr_click(prose, 1)

# Use OCR to copy text nearest to the mouse.
copy mouse: user.mouse_ocr_copy_nearby_line()

# Interacting with labeled coordinates.
# Saving a new labeled mouse position to file cannot be chained with other commands.
^label save <user.text>$: user.mouse_save_coords(text)
labeler {user.mouse_label}: user.mouse_move_to_label(mouse_label)
label touch {user.mouse_label}: user.mouse_click_label(mouse_label)
label right {user.mouse_label}: user.mouse_click_label(mouse_label, 1)
label middle {user.mouse_label}: user.mouse_click_label(mouse_label, 2)
label drag to {user.mouse_label}: user.mouse_drag_to_label(mouse_label)
