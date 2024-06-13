tag: user.splits
-
split close: user.split_close()
split maximize: user.split_maximize()

# Creating new splits.
split new up: user.split_open_up()
split new down: user.split_open_down()
split new left: user.split_open_left()
split new right: user.split_open_right()

# Navigating between splits.
split next: user.split_next()
split last: user.split_last()
split up: user.split_switch_up()
split down: user.split_switch_down()
split left: user.split_switch_left()
split right: user.split_switch_right()
split go <user.number>: user.split_switch_by_index(number)

# Moving files between splits.
split drag up: user.split_move_file_up()
split drag down: user.split_move_file_down()
split drag left: user.split_move_file_left()
split drag right: user.split_move_file_right()
