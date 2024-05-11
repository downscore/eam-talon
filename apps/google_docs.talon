app: google_docs
-

doc history: key(cmd-alt-shift-h)

# Doc mode.
doc preview: user.google_docs_preview()
doc edit: key(cmd-alt-shift-z)
doc suggest: key(cmd-alt-shift-x)
doc view: key(cmd-alt-shift-c)

# Comments.
comment: key(cmd-alt-m)
comment next: key(ctrl-cmd-n ctrl-cmd-c)
comment last: key(ctrl-cmd-p ctrl-cmd-c)

# Header navigation.
heading next: key(ctrl-cmd-n ctrl-cmd-h)
heading last: key(ctrl-cmd-p ctrl-cmd-h)
heading <user.number_small> step: key("ctrl-cmd-n ctrl-cmd-{number_small}")
heading <user.number_small> stone: key("ctrl-cmd-p ctrl-cmd-{number_small}")

# Table navigation
# "column" gets confused with "colon"
# "row pull" gets confused with "nope"
pillar next: key(ctrl-cmd-shift-t ctrl-cmd-shift-b)
pillar last: key(ctrl-cmd-shift-t ctrl-cmd-shift-v)
pillar first: key(ctrl-cmd-shift-t ctrl-cmd-shift-j)
pillar end: key(ctrl-cmd-shift-t ctrl-cmd-shift-l)
row next: key(ctrl-cmd-shift-t ctrl-cmd-shift-m)
row last: key(ctrl-cmd-shift-t ctrl-cmd-shift-g)
row first: key(ctrl-cmd-shift-t ctrl-cmd-shift-i)
row end: key(ctrl-cmd-shift-t ctrl-cmd-shift-k)
