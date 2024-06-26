tag: user.shell
-
tag(): user.file_manager
# tmux provides tab-line window management in the shell.
tag(): user.tabs

# Search using fuzzy finder.
hunt command: user.shell_search_commands()
hunt tree: user.shell_search_files()

# Sent SIGINT to the current process.
signal interrupt: key("ctrl-c")

# Common commands.
seedy: insert("cd ")
l s: insert("ls ")
s s h: insert("ssh ")
code here: insert("code .")
where am i: insert("pwd")
grep [<user.text>]:
  insert("grep \"")
  insert(text or "")
  insert("\"")
  key("left")

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
