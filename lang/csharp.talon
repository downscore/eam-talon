tag: user.lang_csharp
-
# Terminates the current line with a semicolon and makes a new line below.
glide:
  edit.line_end()
  insert(";")
  key(enter)

# C#
make if:
  insert("if ()")
  key(left)
make block:
  edit.line_end()
  insert("{}")
  key(left)
  key(enter)
make elf:
  edit.line_end()
  insert(" else if ()")
  key(left)
make else:
  edit.line_end()
  insert(" else {}")
  key(left)
  key(enter)
make for zero:
  insert("for (var i = 0; i < ; i++)")
  key(left left left left left left)
make for each:
  insert("foreach ()")
  key(left)
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
make default:
  insert("default:")
make null:
  insert("null")
make class:
  insert("class ")
make struct:
  insert("struct ")
make break:
  insert("break")
make continue:
  insert("continue")
make true:
  insert("true")
make false:
  insert("false")
make var:
  insert("var ")
make const:
  insert("const ")
make static:
  insert("static ")
make to do:
  insert("// TODO: ")
make public:
  insert("public ")
make private:
  insert("private ")
make read only:
  insert("readonly ")
make new:
  insert("new ")

  # Operators
a sign: insert(" = ")
make equal: insert(" == ")
make not equal: insert(" != ")
make minus assign: insert(" -= ")
make minus: insert(" - ")
make plus assign: insert(" += ")
make plus: insert(" + ")
make multiply assign: insert(" *= ")
make multiply: insert(" * ")
make divide assign: insert(" /= ")
make divide: insert(" / ")
make modulo assign: insert(" %= ")
make modulo: insert(" % ")
make more equal: insert(" >= ")
make more: insert(" > ")
make less equal: insert(" <= ")
make less: insert(" < ")
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

# Types
tip string: insert("string")
tip byte: insert("byte")
tip signed byte: insert("sbyte")
tip short: insert("short")
tip you short: insert("ushort")
tip int: insert("int")
tip you int: insert("uint")
tip long: insert("long")
tip you long: insert("ulong")
tip you int sixteen: insert("UInt16")
tip int sixteen: insert("Int16")
tip you int thirty two: insert("UInt32")
tip int thirty two: insert("Int32")
tip you int sixty four: insert("Int64")
tip int sixty four: insert("UInt64")
tip (bool|boolean|boo): insert("bool")
tip float: insert("float")
tip double: insert("double")
tip void: insert("void")
tip optional: insert("?")
tip var: insert("var")

comment inline:
  edit.line_end()
  insert("  // ")
comment block start:
  insert("/*")
comment block end:
  insert("*/")
comment to do:
  insert("// TODO: ")
comment:
  insert("// ")
