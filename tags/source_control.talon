tag: user.source_control
-
# Note: These default to tab next/last actions.
file last: user.source_control_file_previous()
file next: user.source_control_file_next()

# Commands for navigating changes within a file.
change last: user.source_control_change_previous()
change next: user.source_control_change_next()
