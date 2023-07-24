tag: user.tabs
-
tab new: app.tab_open()
tab left: user.tab_left()
tab right: user.tab_right()
tab [<user.ordinals_small>] last: user.tab_nth_previous(ordinals_small or 1)
tab close: app.tab_close()
tab restore: app.tab_reopen()
tab numb <user.number_small>: user.tab_switch_by_index(number_small)
tab jump <user.prose>: user.tab_switch_by_name(prose)
