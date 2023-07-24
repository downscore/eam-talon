app <user.running_applications>: user.switcher_focus(running_applications)
app last: key(cmd-tab)

app list running: user.switcher_toggle_running()
app list launch: user.switcher_toggle_launch()
app launch <user.launch_applications>: user.switcher_launch(launch_applications)

switcher test: user.switcher_test()
