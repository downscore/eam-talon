app: warp
-
tag(): user.multiple_cursors
tag(): user.shell
tag(): user.tabs
tag(): user.splits

# Terminal input
go input: key(cmd-l)

# Command palette
please [<user.text>]:
    key(cmd-p)
    insert(user.text or "")

hunt a i: key(ctrl-`)
hunt workflow: key(ctrl-shift-r)

block up: key(cmd-up)
block down: key(cmd-down)

copy command: key(cmd-shift-c)
copy output: key(cmd-shift-alt-c)
