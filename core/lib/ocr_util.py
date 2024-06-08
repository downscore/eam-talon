"""Library for helping with OCR-related tasks."""

import bisect
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class OcrTextFlowContext:
  """Context for using OCRed text in TextFlow, including the screen coordinates where the text is found."""
  # The list of raw OCR results.
  ocr_results: list[Any]
  # The concatenated text of the OCR results.
  text: str
  # The character index into the text where each Ocr result begins. Each element covers the corresponding OCR result
  # plus an extra appended line break. Note: The first element must always be 0.
  start_indices: list[int]
  # The closest index to the mouse. Can be used to simulate a cursor position. Should be snapped to a word boundary to
  # avoid simulating having the cursor in the middle of a word (which can prevent finding that full word).
  mouse_index: int = 0

  def index_to_screen_coordinates(self, text_index: int) -> tuple[float, float]:
    """Converts a character index into screen coordinates. On macOS, we only get a rectangle around each result, so we
    guess at character positions using linear interpolation inside the rectangles."""
    if text_index < 0 or text_index > len(self.text) + 1:  # +1 for the implicit appended line break.
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
    assert 0 <= char_offset <= len(ocr_result.text) + 1  # +1 for the implicit appended line break.

    # We don't actually assign any width to the implicit appended line break, so treat it as if the last character was
    # requested instead.
    if char_offset > len(ocr_result.text):
      char_offset = len(ocr_result.text)

    # Linearly interpolate between the left and right edges of the OCR result rectangle.
    result_rect = ocr_result.rect
    left_x = result_rect.x
    right_x = result_rect.x + result_rect.width
    x = left_x + (right_x - left_x) * (char_offset / len(ocr_result.text))

    # Use the vertical middle of the match.
    y = result_rect.y + result_rect.height / 2

    return x, y


def get_closest_ocr_result_index(ocr_results: list[Any], x: float, y: float) -> Optional[int]:
  """Returns the index of the closest OCR result to the given screen coordinates. Returns None if no nearby result was
  found."""
  if not ocr_results:
    raise ValueError("No OCR results provided.")

  # Find the closest OCR result to the given coordinates.
  closest_index = None
  closest_distance_squared = None
  for i, result in enumerate(ocr_results):
    distance_squared = (result.rect.x + result.rect.width / 2 - x)**2 + (result.rect.y + result.rect.height / 2 - y)**2
    if closest_distance_squared is None or distance_squared < closest_distance_squared:
      closest_index = i
      closest_distance_squared = distance_squared

  return closest_index


def create_ocr_textflow_context(ocr_results: list[Any], mouse_x: float, mouse_y: float) -> OcrTextFlowContext:
  """Creates an OcrTextFlowContext from the given OCR results."""
  if not ocr_results:
    raise ValueError("No OCR results provided.")

  # Get text and start indices.
  text = ""
  start_indices = []
  for ocr_result in ocr_results:
    start_indices.append(len(text))  # +1 for the implicit appended line break.
    text += ocr_result.text + "\n"

  # Get closest result to the mouse and use its start index as the cursor position.
  mouse_index = 0
  closest_result_index = get_closest_ocr_result_index(ocr_results, mouse_x, mouse_y)
  if closest_result_index is not None:
    assert 0 <= closest_result_index < len(ocr_results)
    mouse_index = start_indices[closest_result_index]

  return OcrTextFlowContext(ocr_results, text, start_indices, mouse_index)
