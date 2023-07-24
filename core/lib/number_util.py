"""Utils for mapping words to numbers."""

from typing import Dict, Iterator, List, Union

DIGITS_BY_WORD = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}
TEENS_BY_WORD = {
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19
}
TENS_BY_WORD = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90
}
SCALES_BY_WORD = {
    "hundred": 100,
    "thousand": 1000,
    "million": 1000000,
    # Uncomment below to enable bigger numbers.
    # "billion": 10**9,
    # "trillion": 10**12,
    # "quadrillion": 10**15,
    # "quintillion": 10**18,
    # "sextillion": 10**21,
    # "septillion": 10**24,
    # "octillion": 10**27,
    # "nonillion": 10**30,
    # "decillion": 10**33
}


def _get_numbers_by_word(first_words_only: bool) -> Dict[str, int]:
  """Get a combined map of int values by word for all numbers, or just for numbers that can come first."""
  result: Dict[str, int] = DIGITS_BY_WORD.copy()
  result.update(TEENS_BY_WORD)
  result.update(TENS_BY_WORD)

  # To disallow numbers starting with, or consisting only of, "oh", only add the following if not first_words_only.
  result["oh"] = 0

  if not first_words_only:
    result.update(SCALES_BY_WORD)
  return result


# Maps of words to int values for all numbers.
NUMBERS_BY_WORD = _get_numbers_by_word(False)

# Maps of words to int values for numbers that can be said as a first word.
# Does not include, for example, "hundred". "One hundred" can be said instead.
FIRST_NUMBERS_BY_WORD = _get_numbers_by_word(True)


def _split_list(value: str, l: List[Union[str, int]]) -> Iterator:
  """Splits a list by occurrences of a given value."""
  start = 0
  while True:
    try:
      found_index = l.index(value, start)
    except ValueError:
      break

    yield l[start:found_index]
    start = found_index + 1
  yield l[start:]


def _parse_scale(scale: str, l: List[Union[str, int]]) -> List[Union[str, int]]:
  """Parses a list of mixed numbers and strings for occurrences of the following pattern:
        <multiplier> <scale> <remainder>
    where <scale> is a scale word like "hundred", "thousand", "million", etc. and multiplier and remainder are numbers
    or strings of numbers of the appropriate size. For example:
        parse_scale("hundred", [1, "hundred", 2]) -> [102]
        parse_scale("thousand", [12, "thousand", 3, 45]) -> [12345]

    We assume that all scales of lower magnitude have already been parsed. Don't call parse_scale("thousand") until
    you've called parse_scale("hundred").
    """
  scale_value = SCALES_BY_WORD[scale]
  scale_digits = len(str(scale_value))

  # Split the list on the desired scale word, then parse from left to right.
  left, *splits = _split_list(scale, l)
  for right in splits:
    # (1) Figure out the multiplier by looking to the left of the scale word. We ignore non-integers because they are
    # scale words that we haven't processed yet; this strategy means that "thousand hundred" gets parsed as 1,100
    # instead of 100,000, but "hundred thousand" is parsed correctly as 100,000.
    before = 1  # default multiplier
    if left and isinstance(left[-1], int) and left[-1] != 0:
      before = left.pop()

    # (2) Absorb numbers to the right, eg. in [1, "thousand", 1, 26], "1 thousand" absorbs ["1", "26"] to make 1,126.
    # We pull numbers off `right` until we fill up the desired number of digits.
    after = ""
    while right and isinstance(right[0], int):
      next_str = after + str(right[0])
      if len(next_str) >= scale_digits:
        break
      after = next_str
      right.pop(0)
    after_int = int(after) if after else 0

    # (3) Push the parsed number into place, append whatever was left unparsed, and continue.
    left.append(before * scale_value + after_int)
    left.extend(right)

  return left


def _scan_small_numbers(l: List[str]) -> Iterator[Union[str, int]]:
  """
    Takes a list of number words, yields a generator of mixed numbers and strings.
    Translates small number terms (<100) into corresponding numbers.
    Drops all occurrences of "and".
    Smashes digits onto tens words, eg. ["twenty", "one"] -> [21].
    But note that "ten" and "zero" are excluded, ie:
      ["ten", "three"] -> [10, 3]
      ["fifty", "zero"] -> [50, 0]
    Does nothing to scale words ("hundred", "thousand", "million", etc).
    """
  # Reversed so that repeated pop() visits in left-to-right order.
  l = [x for x in reversed(l) if x != "and"]
  while l:
    n = l.pop()
    # Fuse tens onto digits, eg. "twenty", "one" -> 21.
    if n in TENS_BY_WORD and l and DIGITS_BY_WORD.get(l[-1], 0) != 0:
      d = l.pop()
      yield NUMBERS_BY_WORD[n] + NUMBERS_BY_WORD[d]
    # Turn small number terms into corresponding numbers.
    elif n not in SCALES_BY_WORD:
      yield NUMBERS_BY_WORD[n]
    else:
      yield n


def parse_number(l: List[str]) -> str:
  """Parses a list of words into a number/digit string."""
  processed = list(_scan_small_numbers(l))
  for scale in SCALES_BY_WORD:
    processed = _parse_scale(scale, processed)
  return "".join(str(n) for n in processed)
