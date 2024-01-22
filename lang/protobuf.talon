tag: user.lang_protobuf
-
# Terminates the current line with a semicolon and makes a new line below.
glide:
  edit.line_end()
  insert(";")
  key(enter)

# C++
make block:
  edit.line_end()
  insert("{}")
  key(left)
  key(enter)
make abseil: insert("absl::")
make standard: insert("std::")
make import:
  insert("import \"\";")
  key(left:2)
make message: insert("message ")
make optional: insert("optional ")
make required: insert("required ")
make repeated: insert("repeated ")
make enum: insert("enum ")
make service: insert("service ")
make rpc: insert("rpc ")
make reserved: insert("reserved ")
make todo: insert("TODO: ")

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
make packed: insert("packed = true")
make default: insert("default = ")

# Types
tip string: insert("std::string")
tip tee: insert("_t")
tip you int eight: insert("uint8")
tip int eight: insert("int8")
tip you int sixteen: insert("uint16")
tip int sixteen: insert("int16")
tip you int thirty two: insert("uint32")
tip int thirty two: insert("int32")
tip you int sixty four: insert("uint64")
tip int sixty four: insert("int64")
tip int: insert("int32")
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
