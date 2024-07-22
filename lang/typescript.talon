tag: user.lang_typescript
-
# Terminates the current line with a semicolon and makes a new line below.
glide:
  user.line_end()
  insert(";")
  key(enter)

make if:
  insert("if ()")
  key(left)
make block:
  user.line_end()
  insert(" {}")
  key(left)
  key(enter)
make elf:
  user.line_end()
  insert(" else if ()")
  key(left)
make else:
  user.line_end()
  insert(" else {}")
  key(left)
  key(enter)
make for:
  insert("for ()")
  key(left)
# Problems recognizing "while".
make loop:
  insert("while ()")
  key(left)
make return:
  insert("return ")
make do loop:
  insert("do ")
  key(left)
make switch:
  insert("switch ()")
  key(left)
make case:
  insert("case :")
  key(left)
make default: insert("default:")
make class: insert("class ")
make break: insert("break;")
make continue: insert("continue;")
make true: insert("true")
make false: insert("false")
make const: insert("const ")
make let: insert("let ")
make private: insert("private ")
make public: insert("public ")
make async: insert("async ")
make await: insert("await ")
make function: insert("function ")

# Operators
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
make and: insert(" && ")
make or: insert(" || ")
make bitwise and: insert(" & ")
make bitwise or: insert(" | ")
make ex or: insert(" ^ ")
make left shift: insert(" << ")
make right shift: insert(" >> ")
make colon: insert(" : ")
make increment: insert("++")
make decrement: insert("--")

tip any: insert("any")
tip string: insert("string")
tip int: insert("int")
tip number: insert("number")
tip (bool|boolean|boo): insert("boolean")

hint any: insert(": any")
hint string: insert(": string")
hint int: insert(": int")
hint number: insert(": number")
hint (bool|boolean|boo): insert(": boolean")

comment inline:
  user.line_end()
  insert("  // ")
comment block:
  insert("/**/")
  key(left:2)
comment to do:
  insert("// TODO: ")
comment:
  insert("// ")
