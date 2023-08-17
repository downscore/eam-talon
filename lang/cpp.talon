tag: user.lang_cpp
-
# Terminates the current line with a semicolon and makes a new line below.
glide:
  edit.line_end()
  insert(";")
  key(enter)

template:
  insert("<>")
  key(left)

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
  insert("for (int i = 0; i < ; i++)")
  key(left left left left left left)
make for const:
  insert("for (const auto& )")
  key(left)
make for ref:
  insert("for (auto& )")
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
make (null opt|nullopt):
  insert("nullopt")
make null:
  insert("nullptr")
make class:
  insert("class ")
make type deaf:
  insert("typedef ")
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
make auto ref:
  insert("auto& ")
make auto pointer:
  insert("auto* ")
make auto:
  insert("auto ")
make const:
  insert("const ")
make const auto:
  insert("const auto ")
make const ref:
  insert("const auto& ")
make constex:
  insert("constexpr ")
make static:
  insert("static ")
make include system:
  insert("#include <>")
  key(left)
make include:
  insert("#include \"\"")
  key(left)
make abseil:
  insert("absl::")
make standard:
  insert("std::")
make assert equal:
  insert("ASSERT_EQ();")
  key(left:2)
make assert true:
  insert("ASSERT_TRUE();")
  key(left:2)
make assert false:
  insert("ASSERT_FALSE();")
  key(left:2)
make assert less:
  insert("ASSERT_LT();")
  key(left:2)
make assert more:
  insert("ASSERT_GT();")
  key(left:2)
make expect equal:
  insert("EXPECT_EQ();")
  key(left:2)
make expect true:
  insert("EXPECT_TRUE();")
  key(left:2)
make expect false:
  insert("EXPECT_FALSE();")
  key(left:2)
make expect less:
  insert("EXPECT_LT();")
  key(left:2)
make expect more:
  insert("EXPECT_GT();")
  key(left:2)

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
tip string: insert("std::string")
tip tee: insert("_t")
tip you int eight: insert("uint8_t")
tip int eight: insert("int8_t")
tip you int sixteen: insert("uint16_t")
tip int sixteen: insert("int16_t")
tip you int thirty two: insert("uint32_t")
tip int thirty two: insert("int32_t")
tip you int sixty four: insert("uint64_t")
tip int sixty four: insert("int64_t")
tip int: insert("int")
tip (bool|boolean|boo): insert("bool")
tip float: insert("float")
tip double: insert("double")
tip void: insert("void")
tip optional:
  insert("absl::optional<>")
  key(left)
tip status or:
  insert("absl::StatusOr<>")
  key(left)
tip status: insert("absl::Status")

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
