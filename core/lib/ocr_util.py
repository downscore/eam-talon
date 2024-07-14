"""Library for helping with OCR-related tasks."""

import bisect
from dataclasses import dataclass
from typing import Any, Optional

# Width values by character for Ocr rect interpolation purposes. Any character not included has a
# default width.
_DEFAULT_CHAR_WIDTH: float = 10
_WIDTHS_BY_CHAR: dict[str, float] = {
    "\n": 0,  # Newline characters have no width.
    " ": 5.5,
    "!": 5.5,
    '"': 7,
    "#": 11,
    "$": 11,
    "%": 16,
    "&": 13,
    "'": 3.5,
    "(": 6.5,
    ")": 6.5,
    "*": 8,
    "+": 11.5,
    ",": 5.5,
    "-": 6.5,
    ".": 5.5,
    "/": 5.5,
    "0": 11,
    "1": 9.5,
    "2": 11,
    "3": 11,
    "4": 11,
    "5": 11,
    "6": 11,
    "7": 11,
    "8": 11,
    "9": 11,
    ":": 5.5,
    ";": 5.5,
    "<": 11.5,
    "=": 11.5,
    ">": 11.5,
    "?": 11,
    "@": 16,
    "A": 13,
    "B": 13,
    "C": 14.5,
    "D": 14.5,
    "E": 13,
    "F": 12.2,
    "G": 15.5,
    "H": 14.5,
    "I": 5.5,
    "J": 10,
    "K": 13,
    "L": 11,
    "M": 16.5,
    "N": 14.5,
    "O": 15.5,
    "P": 13,
    "Q": 15.5,
    "R": 14.5,
    "S": 13,
    "T": 12.2,
    "U": 14.5,
    "V": 13,
    "W": 18.5,
    "X": 13,
    "Y": 13,
    "Z": 12.2,
    "[": 5.5,
    "\\": 5.5,
    "]": 5.5,
    "^": 9.5,
    "_": 11,
    "`": 6.5,
    "a": 11,
    "b": 11,
    "c": 10,
    "d": 11,
    "e": 11,
    "f": 5,
    "g": 11,
    "h": 11,
    "i": 4.4,
    "j": 4.4,
    "k": 10,
    "l": 4.4,
    "m": 16.5,
    "n": 11,
    "o": 11,
    "p": 11,
    "q": 11,
    "r": 6.5,
    "s": 10,
    "t": 5.5,
    "u": 11,
    "v": 10,
    "w": 14.5,
    "x": 10,
    "y": 10,
    "z": 10,
    "{": 6.6,
    "|": 5.1,
    "}": 6.6,
    "~": 11.5,
}


@dataclass
class OcrTextFlowContext:
  """Context for using OCRed text in TextFlow, including the screen coordinates where the text is
  found."""
  # The list of raw OCR results.
  ocr_results: list[Any]
  # The concatenated text of the OCR results.
  text: str
  # The character index into the text where each Ocr result begins. Each element covers the
  # corresponding OCR result plus an extra appended space. Note: The first element must always be 0.
  start_indices: list[int]
  # The closest index to the mouse. Can be used to simulate a cursor position. Should be snapped to
  # a word boundary to avoid simulating having the cursor in the middle of a word (which can prevent
  # finding that full word).
  mouse_index: int = 0

  def index_to_screen_coordinates(self, text_index: int) -> tuple[float, float]:
    """Converts a character index into screen coordinates. On macOS, we only get a rectangle around
    each result, so we guess at character positions using linear interpolation inside the
    rectangles."""
    if text_index < 0 or text_index > len(self.text) + 1:  # +1 for the implicit appended space.
      raise ValueError(f"Invalid text index: {text_index}")

    # Binary search start indices to find the corresponding OCR result index.
    ocr_result_index = bisect.bisect_right(self.start_indices, text_index)
    if ocr_result_index > 0:
      ocr_result_index -= 1
    assert 0 <= ocr_result_index < len(self.ocr_results)
    ocr_result = self.ocr_results[ocr_result_index]
    assert len(ocr_result.text) > 0  # Should never have an empty OCR result.

    # Get character offset in the OCR result.
    char_offset = text_index - self.start_indices[ocr_result_index]
    assert 0 <= char_offset <= len(ocr_result.text) + 1  # +1 for the implicit appended space.

    # We don't actually assign any width to the implicit appended space, so treat it as if the last
    # character was requested instead.
    if char_offset > len(ocr_result.text):
      char_offset = len(ocr_result.text)

    # Interpolate between the left and right edges of the OCR result rectangle.
    full_width = get_string_width(ocr_result.text)
    if full_width <= 0:
      raise ValueError(f"OCR result has no width: {ocr_result.text}")
    select_width = get_string_width(ocr_result.text[:char_offset])
    fraction = select_width / full_width

    result_rect = ocr_result.rect
    left_x = result_rect.x
    right_x = result_rect.x + result_rect.width
    x = left_x + (right_x - left_x) * fraction

    # Use the vertical middle of the match.
    y = result_rect.y + result_rect.height / 2

    return x, y

  def expand_range_to_ocr_results(self, start: int, end: int) -> tuple[int, int]:
    """Expand the given character range so that it covers full OCR results. Returns the expanded
    range."""
    if start < 0 or end < start or end > len(self.text) + 1:  # +1 for the implicit appended space.
      raise ValueError(f"Invalid range: [{start}, {end}]")

    # Binary search start indices to find the corresponding OCR result indices.
    start_ocr_result_index = bisect.bisect_right(self.start_indices, start)
    if start_ocr_result_index > 0:
      start_ocr_result_index -= 1
    end_ocr_result_index = bisect.bisect_right(self.start_indices, end)
    if end_ocr_result_index > 0:
      end_ocr_result_index -= 1
    assert 0 <= start_ocr_result_index < len(self.ocr_results)
    assert 0 <= end_ocr_result_index < len(self.ocr_results)

    # Expand the range to cover full OCR results.
    expanded_start = self.start_indices[start_ocr_result_index]
    expanded_end = self.start_indices[end_ocr_result_index] + len(
        self.ocr_results[end_ocr_result_index].text)

    return expanded_start, expanded_end


def get_string_width(text: str) -> float:
  """Returns the heuristic width of the given string."""
  width = 0
  for char in text:
    width += _WIDTHS_BY_CHAR.get(char, _DEFAULT_CHAR_WIDTH)
  return width


def get_closest_ocr_result_index(ocr_results: list[Any], x: float, y: float) -> Optional[int]:
  """Returns the index of the closest OCR result to the given screen coordinates. Returns None if no
  nearby result was found."""
  if not ocr_results:
    raise ValueError("No OCR results provided.")

  # Find the closest OCR result to the given coordinates.
  closest_index = None
  closest_distance_squared = None
  for i, result in enumerate(ocr_results):
    # Get rectangle bounds.
    left = result.rect.x
    right = result.rect.x + result.rect.width
    top = result.rect.y
    bottom = result.rect.y + result.rect.height

    # Check if the point is inside the rectangle.
    if left <= x <= right and top <= y <= bottom:
      distance_squared = 0
    else:
      # Calculate the distances to the rectangle edges.
      dx = max(left - x, 0, x - right)
      dy = max(top - y, 0, y - bottom)
      distance_squared = dx**2 + dy**2

    # Update closest result if necessary.
    if closest_distance_squared is None or distance_squared < closest_distance_squared:
      closest_index = i
      closest_distance_squared = distance_squared

  return closest_index


def create_ocr_textflow_context(ocr_results: list[Any], mouse_x: float,
                                mouse_y: float) -> OcrTextFlowContext:
  """Creates an OcrTextFlowContext from the given OCR results."""
  if not ocr_results:
    raise ValueError("No OCR results provided.")

  # Get text and start indices.
  text = ""
  start_indices = []
  for ocr_result in ocr_results:
    start_indices.append(len(text))  # +1 for the implicit appended space.
    text += ocr_result.text + " "

  # Get closest result to the mouse and use its start index as the cursor position.
  mouse_index = 0
  closest_result_index = get_closest_ocr_result_index(ocr_results, mouse_x, mouse_y)
  if closest_result_index is not None:
    assert 0 <= closest_result_index < len(ocr_results)
    mouse_index = start_indices[closest_result_index]

  return OcrTextFlowContext(ocr_results, text, start_indices, mouse_index)
