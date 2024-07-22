tag: user.lang_markdown
-
make block:
  insert("```\n\n```")
  key("left:4")
make python block:
  insert("```python\n\n```")
  key("left:4")
make C P P block:
  insert("```C++\n\n```")
  key("left:4")
make jason block:
  insert("```json\n\n```")
  key("left:4")
make yaml block:
  insert("```yaml\n\n```")
  key("left:4")
make tinychart block:
  insert("```tinychart\n\n```")
  key("left:4")

lister:
  user.line_insert_down()
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
make callout to do: insert("> [!todo]\n")
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

# Big-O notation
big o constant: insert("$O(1)$")
big o linear: insert("$O(n)$")
big o quadratic: insert("$O(n^2)$")
big o cubic: insert("$O(n^3)$")
big o quartic: insert("$O(n^4)$")
big o quintic: insert("$O(n^5)$")
big o log: insert("$O(\\log{{n}})$")
big o log linear: insert("$O(n \\log{{n}})$")

# General operators
a sign: insert(" = ")
is equal: insert(" == ")
is not equal: insert(" != ")
is more equal: insert(" >= ")
is more: insert(" > ")
is less equal: insert(" <= ")
is less: insert(" < ")
make minus equal: insert(" -= ")
make minus: insert(" - ")
make plus equal: insert(" += ")
make plus: insert(" + ")
make multiply equal: insert(" *= ")
make multiply: insert(" * ")
make divide equal: insert(" /= ")
make divide: insert(" / ")
make modulo equal: insert(" %= ")
make modulo: insert(" % ")
make colon: insert(" : ")
make increment: insert("++")
make decrement: insert("--")

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
