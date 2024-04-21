tag: user.lang_cpp
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
make for zero:
  insert("for (int i = 0; i < ; i++)")
  key(left:6)
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
make todo: insert("TODO: ")
make default: insert("default:")
make (null opt|nullopt): insert("nullopt")
make null pointer: insert("nullptr")
make class: insert("class ")
make type deaf: insert("typedef ")
make struct: insert("struct ")
make break: insert("break;")
make continue: insert("continue;")
make true: insert("true")
make false: insert("false")
make const: insert("const ")
make constex: insert("constexpr ")
make static: insert("static ")
make include system:
  insert("#include <>")
  key(left)
make include:
  insert("#include \"\"")
  key(left)
make abseil: insert("absl::")
make standard: insert("std::")
make namespace:
  user.line_end()
  insert("namespace {}  // namespace")
  key(left:15)
  key(enter)

# Shortcuts for symbol names hard to type by voice.
snake pushback: insert("push_back")
make emplace back:
  insert("emplace_back()")
  key(left)
make emplace front:
  insert("emplace_front()")
  key(left)
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
tip auto: insert("auto ")
tip auto amper: insert("auto& ")
tip auto star: insert("auto* ")
tip string: insert("std::string ")
tip string amper: insert("std::string& ")
tip string star: insert("std::string* ")
tip int: insert("int ")
tip int amper: insert("int& ")
tip int star: insert("int* ")
tip (bool|boolean|boo): insert("bool ")
tip (bool|boolean|boo) amper: insert("bool& ")
tip (bool|boolean|boo) star: insert("bool* ")
tip float: insert("float ")
tip float amper: insert("float& ")
tip float star: insert("float* ")
tip double: insert("double ")
tip double amper: insert("double& ")
tip double star: insert("double* ")
tip void: insert("void ")
tip void star: insert("void* ")
tip char: insert("char ")
tip char amper: insert("char& ")
tip char star: insert("char* ")
tip you int eight: insert("uint8_t ")
tip int eight: insert("int8_t ")
tip you int sixteen: insert("uint16_t ")
tip int sixteen: insert("int16_t ")
tip you int thirty two: insert("uint32_t ")
tip int thirty two: insert("int32_t ")
tip you int sixty four: insert("uint64_t ")
tip int sixty four: insert("int64_t ")
tip optional:
  insert("std::optional<> ")
  key(left:2)
tip status or:
  insert("absl::StatusOr<> ")
  key(left:2)
tip status: insert("absl::Status ")
tip vector:
  insert("std::vector<> ")
  key(left:2)
tip vector amper:
  insert("std::vector<>& ")
  key(left:3)
tip vector star:
  insert("std::vector<>* ")
  key(left:3)

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
