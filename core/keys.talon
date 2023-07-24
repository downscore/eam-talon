<user.letter>: key(letter)
uppercase <user.letters>: insert(user.format_uppercase(letters))
<user.symbol_key>: key(symbol_key)
<user.function_key>: key(function_key)
<user.special_key>: key(special_key)
<user.modifiers> <user.unmodified_key>: key("{modifiers}-{unmodified_key}")

# For pressing modifiers on their own.
press <user.modifiers>: key(modifiers)

brightness up: key(brightness_up)
brightness down: key(brightness_down)

backlight up: key(backlight_up)
backlight down: key(backlight_down)

media volume up: key(volup)
media volume down: key(voldown)
media mute: key(mute)
media next: key(next)
media previous: key(prev)
media (play | pause): key(play)
