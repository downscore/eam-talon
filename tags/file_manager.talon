tag: user.file_manager
-
folder parent: user.file_manager_open_parent()

folder home: user.file_manager_open_directory("~")
folder docs: user.file_manager_open_directory("~/Documents")
folder downloads: user.file_manager_open_directory("~/Downloads")
folder desktop: user.file_manager_open_directory("~/Desktop")

folder talon home: user.file_manager_open_directory(path.talon_home())
folder talon user: user.file_manager_open_directory(path.talon_user())
