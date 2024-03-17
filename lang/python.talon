tag: user.lang_python
-
is none: insert(" is None")
is not none: insert(" is not None")
self taught: "self."
arg self:
  insert("(self)")
  key(left)

[make] dock string: insert("\"\"\"")
make if:
  insert("if :")
  key(left)
make block:
  user.line_end()
  insert(":")
  key(enter)
make elf:
  user.line_end()
  insert("elif :")
  key(left)
make else:
  user.line_end()
  insert("else:")
make for:
  insert("for :")
  key(left)
make for range:
  insert("for i in range():")
  key(left:2)
# Problems recognizing "while".
make loop:
  insert("while :")
  key(left)
make todo: insert("TODO: ")
make return: insert("return ")
make (null|none): insert("None")
make class:
  insert("class :")
  key(left)
make break: insert("break")
make continue: insert("continue")
make pass: insert("pass")
make true: insert("True")
make false: insert("False")
make deaf: insert("def ")
make funk:
  insert("def :")
  key(left)
make hint: insert(" -> ")
make (len|size):
  insert("len()")
  key(left)
make raise: insert("raise ")
make with:
  insert("with :")
  key(left)
make value error:
  insert("raise ValueError(f\"\")")
  key(left:2)
make try: insert("try:\n")
make except:
  insert("except :")
  key(left)
make assert equal:
  insert("self.assertEqual()")
  key(left)
make assert raises:
  insert("with self.assertRaises():")
  key(left:2)
make assert true:
  insert("self.assertTrue()")
  key(left)
make assert false:
  insert("self.assertFalse()")
  key(left)
make print:
  insert("print()")
  key(left)
make range:
  insert("range()")
  key(left)
make global: insert("global ")
make enumerate:
  insert("enumerate()")
  key(left)
make delete: insert("del ")
make none: insert("None")
make not: insert("not ")

# Imports
import: insert("import ")
import beautiful soup: insert("from bs4 import BeautifulSoup\n")
import collections: insert("import collections\n")
import C S V: insert("import csv\n")
import jason: insert("import json\n")
import open A I: insert("import openai\n")
import O S: insert("import os\n")
import pretty print: insert("from pprint import pprint\n")
import R E: insert("import re\n")
import requests: insert("import requests\n")
import time: insert("import time\n")
import unit test: insert("import unittest\n")

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
make and: insert(" and ")
make or: insert(" or ")
make bitwise and: insert(" & ")
make bitwise or: insert(" | ")
make ex or: insert(" ^ ")
make left shift: insert(" << ")
make right shift: insert(" >> ")
make colon: insert(" : ")
make increment: insert("++")
make decrement: insert("--")
make in: insert(" in ")
make inline for: insert(" for ")
make inline if: insert(" if ")

tip any: insert("Any")
tip string: insert("str")
tip int: insert("int")
tip float: insert("float")
tip (bool|boolean|boo): insert("bool")

hint any: insert(": Any")
hint string: insert(": str")
hint int: insert(": int")
hint float: insert(": float")
hint (bool|boolean|boo): insert(": bool")
hint list:
  insert(": list[]")
  key(left)
hint list string: insert(": list[str]")
hint list int: insert(": list[int]")
hint dictionary:
  insert(": dict[]")
  key(left)
hint optional:
  insert(": Optional[]")
  key(left)
hint tuple:
  insert(": Tuple[]")
  key(left)
hint iterator:
  insert(": Iterator[]")
  key(left)
hint generator:
  insert(": Generator[]")
  key(left)
hint set:
  insert(": Set[]")
  key(left)
hint frozen set:
  insert(": FrozenSet[]")
  key(left)
hint callable:
  insert(": Callable[]")
  key(left)
hint union:
  insert(": Union[]")
  key(left)

comment inline:
  user.line_end()
  insert("  # ")
comment to do:
  insert("# TODO: ")
comment:
  insert("# ")
