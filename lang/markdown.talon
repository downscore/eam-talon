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
make note: insert("> [!note]\n")
make abstract: insert("> [!abstract]\n")
make info: insert("> [!info]\n")
make to do: insert("> [!todo]\n")
make tip: insert("> [!tip]\n")
make success: insert("> [!success]\n")
make question: insert("> [!question]\n")
make warning: insert("> [!warning]\n")
make failure: insert("> [!failure]\n")
make danger: insert("> [!danger]\n")
make error: insert("> [!error]\n")
make bug: insert("> [!bug]\n")
make example: insert("> [!example]\n")
make quote: insert("> [!quote]\n")

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
make real numbers: insert("\\mathbb{{R}}")
make complex numbers: insert("\\mathbb{{C}}")
make natural numbers: insert("\\mathbb{{N}}")
make integers: insert("\\mathbb{{Z}}")
make empty set: insert("\\emptyset")

# Latex operators
make in: insert(" \\in ")
make not in: insert(" \\notin ")
make times: insert(" \\times ")
make approximate: insert(" \\approx ")

# General operators (useful in Latex)
a sign: insert(" = ")
make equal: insert(" == ")
make not equal: insert(" != ")
make minus: insert(" - ")
make plus: insert(" + ")
make multiply: insert(" * ")
make divide: insert(" / ")
make modulo: insert(" % ")
make more: insert(" > ")
make less: insert(" < ")

# Greek letters in latex
greek alpha: insert("\\alpha")
greek beta: insert("\\beta")
greek gamma: insert("\\gamma")
greek delta: insert("\\delta")
greek epsilon: insert("\\epsilon")
greek zeta: insert("\\zeta")
greek eta: insert("\\eta")
greek theta: insert("\\theta")
greek iota: insert("\\iota")
greek kappa: insert("\\kappa")
greek lambda: insert("\\lambda")
greek mu: insert("\\mu")
greek nu: insert("\\nu")
greek xi: insert("\\xi")
greek omicron: insert("\\omicron")
greek pi: insert("\\pi")
greek rho: insert("\\rho")
greek sigma: insert("\\sigma")
greek tau: insert("\\tau")
greek upsilon: insert("\\upsilon")
greek phi: insert("\\phi")
greek chi: insert("\\chi")
greek psi: insert("\\psi")
greek omega: insert("\\omega")
greek big gamma: insert("\\Gamma")
greek big delta: insert("\\Delta")
greek big theta: insert("\\Theta")
greek big lambda: insert("\\Lambda")
greek big xi: insert("\\Xi")
greek big pi: insert("\\Pi")
greek big sigma: insert("\\Sigma")
greek big upsilon: insert("\\Upsilon")
greek big phi: insert("\\Phi")
greek big psi: insert("\\Psi")
greek big omega: insert("\\Omega")
