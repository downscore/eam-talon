tag: user.lang_markdown
-
make block:
  insert("```\n\n```")
  key("left:4")

lister:
  edit.line_insert_down()
  insert("* ")

# Horizontal rule
make horizontal:
  insert("\n---\n")

# Footnotes
make footnote:
  insert("[^]")
  key("left")
make inline footnote:
  insert("^[]")
  key("left:1")

# Callouts
callout info: insert("> [!info]\n")
callout note: insert("> [!note]\n")
callout to do: insert("> [!todo]\n")
callout tip: insert("> [!tip]\n")
callout abstract: insert("> [!abstract]\n")
callout success: insert("> [!success]\n")
callout check: insert("> [!check]\n")
callout done: insert("> [!done]\n")
callout question: insert("> [!question]\n")
callout warning: insert("> [!warning]\n")
callout failure: insert("> [!failure]\n")
callout danger: insert("> [!danger]\n")
callout bug: insert("> [!bug]\n")
callout example: insert("> [!example]\n")
callout quote: insert("> [!quote]\n")
callout summary: insert("> [!summary]\n")
callout hint: insert("> [!hint]\n")
callout important: insert("> [!important]\n")
callout fail: insert("> [!fail]\n")
callout missing: insert("> [!missing]\n")
callout error: insert("> [!error]\n")

# Mermaid support
make mermaid block:
  insert("```mermaid\n\n```")
  key("left:4")
make connect: insert(" --> ")
make font awesome: insert("fa:fa-")

# Latex support
make latex block:
  insert("$$\n\n$$")
  key("left:3")
make in: insert("\\in ")
make not in: insert("\\notin ")
make real numbers: insert("\\mathbb{{R}}")
make complex numbers: insert("\\mathbb{{C}}")
make natural numbers: insert("\\mathbb{{N}}")
make integers: insert("\\mathbb{{Z}}")
make empty set: insert("\\emptyset")
make times: insert("\\times ")
make approximate: insert("\\approx ")

# Greek letters in latex
make alpha: insert("\\alpha ")
make beta: insert("\\beta ")
make gamma: insert("\\gamma ")
make delta: insert("\\delta ")
make epsilon: insert("\\epsilon ")
make zeta: insert("\\zeta ")
make eta: insert("\\eta ")
make theta: insert("\\theta ")
make iota: insert("\\iota ")
make kappa: insert("\\kappa ")
make lambda: insert("\\lambda ")
make mu: insert("\\mu ")
make nu: insert("\\nu ")
make xi: insert("\\xi ")
make omicron: insert("\\omicron ")
make pi: insert("\\pi ")
make rho: insert("\\rho ")
make sigma: insert("\\sigma ")
make tau: insert("\\tau ")
make upsilon: insert("\\upsilon ")
make phi: insert("\\phi ")
make chi: insert("\\chi ")
make psi: insert("\\psi ")
make omega: insert("\\omega ")
make big gamma: insert("\\Gamma ")
make big delta: insert("\\Delta ")
make big theta: insert("\\Theta ")
make big lambda: insert("\\Lambda ")
make big xi: insert("\\Xi ")
make big pi: insert("\\Pi ")
make big sigma: insert("\\Sigma ")
make big upsilon: insert("\\Upsilon ")
make big phi: insert("\\Phi ")
make big psi: insert("\\Psi ")
make big omega: insert("\\Omega ")
