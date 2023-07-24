tag: user.shell
-
tag(): user.file_manager

hunt command: user.shell_search_commands()

folder go [<user.text>]:
  insert("cd ")
  insert(user.text or "")

make directory [<user.text>]:
  insert("mkdir ")
  insert(user.text or "")

l s: insert("ls ")
s s h: insert("ssh ")
dot net: insert("dotnet ")
code here: insert("code .")

# Open file with default app
open file: insert("open ")

# Get the return value of the last command
return value: insert("echo $?")

# Clear the whole console
reset console: insert("reset")

# Git commands.
git branch: insert("git branch")
git status: insert("git status")
git checkout: insert("git checkout")
git push: insert("git push")
git pull: insert("git pull")
git fetch: insert("git fetch")
