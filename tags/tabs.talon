tag: user.tabs
-
tab new: user.tab_open()
tab left: user.tab_left()
tab right: user.tab_right()
tab [<user.ordinals_small>] last: user.tab_nth_previous(ordinals_small or 1)
tab close: user.tab_close()
tab restore: user.tab_reopen()
tab numb <user.number_small>: user.tab_switch_by_index(number_small)
tab jump <user.prose>: user.tab_switch_by_name(prose)
tab list [<user.text>]: user.tab_list(text or "")
