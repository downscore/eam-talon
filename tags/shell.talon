tag: user.shell
-
tag(): user.file_manager
# tmux provides splits and tabs in the shell.
tag(): user.splits
tag(): user.tabs

# Search using fuzzy finder.
hunt command: user.shell_search_commands()
hunt tree: user.shell_search_files()

# Sent SIGINT to the current process.
signal interrupt: key("ctrl-c")

# tmux commands.
tmux: insert("tmux ")
tmux attach: insert("tmux attach")
tmux kill server: insert("tmux kill-server")

# Common commands.
seedy: insert("cd ")
l s: insert("ls ")
s s h: insert("ssh ")
code here: insert("code .")
where am i: insert("pwd")

# Pipe contents to/from clipboard
to clipboard: insert(" | pbcopy")
from clipboard: insert("pbpaste | ")

# Open file with default app
open file: insert("open ")

# Get the return value of the last command
return value: insert("echo $?")

# Git commands.
git branch: insert("git branch")
git status: insert("git status")
git checkout: insert("git checkout")
git push: insert("git push")
git pull: insert("git pull")
git fetch: insert("git fetch")
