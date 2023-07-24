"""Utils for mapping between ordinal words and int values."""

# Ordinal words from 0 to 20 and tens up to 90. Used as seed words for filling in missing ordinals.
_ORDINAL_SEED_WORDS_BY_NUMBER = {
    0: "zeroth",
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth",
    7: "seventh",
    8: "eighth",
    9: "ninth",
    10: "tenth",
    11: "eleventh",
    12: "twelfth",
    13: "thirteenth",
    14: "fourteenth",
    15: "fifteenth",
    16: "sixteenth",
    17: "seventeenth",
    18: "eighteenth",
    19: "nineteenth",
    20: "twentieth",
    30: "thirtieth",
    40: "fortieth",
    50: "fiftieth",
    60: "sixtieth",
    70: "seventieth",
    80: "eightieth",
    90: "ninetieth",
}

_TENS_WORDS = ["zero", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def get_ints_by_ordinal_words(up_to: int = 99) -> dict[str, int]:
  """Get a dict of ints keyed by ordinal words from one to `up_to` inclusive."""
  if up_to > 99:
    raise ValueError("Can only generate ordinals up to 99")
  if up_to <= 0:
    raise ValueError("Max ordinal value must be positive")
  result : dict[str, int] = {}
  words: str = ""
  for i in range(1, up_to + 1):
    if i in _ORDINAL_SEED_WORDS_BY_NUMBER:
      words = _ORDINAL_SEED_WORDS_BY_NUMBER[i]
    else:
      (tens, units) = divmod(i, 10)
      words = f"{_TENS_WORDS[tens]} {_ORDINAL_SEED_WORDS_BY_NUMBER[units]}"
    result[words] = i
  return result
