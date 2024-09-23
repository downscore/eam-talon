"""Tests for OCR utils."""

import unittest
from .ocr_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class Rect:
  """Mock for type we can't import here."""

  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height


class OcrResult:
  """Mock for type we can't import here."""

  def __init__(self, text, rect):
    self.text = text
    self.rect = rect


class GetStringWidthTestCase(unittest.TestCase):
  """Util function tests."""

  def test_get_width(self):
    self.assertEqual(get_string_width(""), 0)
    self.assertGreater(get_string_width("WWWWW"), get_string_width("lllll"))


class GetClosestOcrResultIndexTestCase(unittest.TestCase):
  """Util function tests."""

  def test_no_ocr_results(self):
    with self.assertRaises(ValueError):
      get_closest_ocr_result_index([], 0, 0)

  def test_single_result(self):
    rect = Rect(10, 10, 10, 10)
    ocr_results = [OcrResult("", rect)]
    self.assertEqual(get_closest_ocr_result_index(ocr_results, 15, 15), 0)

  def test_multiple_results(self):
    rect1 = Rect(10, 10, 10, 10)
    rect2 = Rect(20, 20, 10, 10)
    rect3 = Rect(30, 30, 10, 10)
    ocr_results = [OcrResult("", rect1), OcrResult("", rect2), OcrResult("", rect3)]
    self.assertEqual(get_closest_ocr_result_index(ocr_results, 25, 25), 1)
    self.assertEqual(get_closest_ocr_result_index(ocr_results, 35, 35), 2)
    self.assertEqual(get_closest_ocr_result_index(ocr_results, 5, 5), 0)

  def test_equal_distance(self):
    rect1 = Rect(10, 10, 10, 10)
    rect2 = Rect(20, 20, 10, 10)
    ocr_results = [OcrResult("", rect1), OcrResult("", rect2)]
    self.assertEqual(get_closest_ocr_result_index(ocr_results, 15, 15), 0)

  def test_edge_case(self):
    rect1 = Rect(0, 0, 0, 0)
    rect2 = Rect(1, 1, 0, 0)
    ocr_results = [OcrResult("", rect1), OcrResult("", rect2)]
    self.assertEqual(get_closest_ocr_result_index(ocr_results, 0.5, 0.5), 0)


class CreateOcrScramblerContextTestCase(unittest.TestCase):
  """Util function tests."""

  def test_empty_ocr_results(self):
    with self.assertRaises(ValueError):
      create_ocr_scrambler_context([], 0, 0)

  def test_single_ocr_result(self):
    ocr_results = [OcrResult("Test", Rect(0, 0, 10, 10))]
    context = create_ocr_scrambler_context(ocr_results, 5, 5)
    self.assertEqual(context.text, "Test ")
    self.assertEqual(context.start_indices, [0])
    self.assertEqual(context.mouse_index, 0)

  def test_multiple_ocr_results(self):
    ocr_results = [
        OcrResult("First", Rect(0, 0, 10, 10)),
        OcrResult("Second", Rect(20, 20, 10, 10)),
        OcrResult("Third", Rect(40, 40, 10, 10))
    ]
    context = create_ocr_scrambler_context(ocr_results, 25, 25)
    self.assertEqual(context.text, "First Second Third ")
    self.assertEqual(context.start_indices, [0, 6, 13])
    self.assertEqual(context.mouse_index, 6)  # "Second" is the closest to (25, 25)

  def test_closest_result_to_mouse(self):
    ocr_results = [
        OcrResult("A", Rect(0, 0, 10, 10)),
        OcrResult("B", Rect(100, 100, 10, 10)),
        OcrResult("C", Rect(50, 50, 10, 10))
    ]
    context = create_ocr_scrambler_context(ocr_results, 52, 52)
    self.assertEqual(context.text, "A B C ")
    self.assertEqual(context.start_indices, [0, 2, 4])
    self.assertEqual(context.mouse_index, 4)  # "C" is the closest to (52, 52)


class IndexToScreenCoordinatesTestCase(unittest.TestCase):
  """Util function tests."""

  def setUp(self):
    self.ocr_results = [
        OcrResult("Hello", Rect(0, 0, 50, 10)),
        OcrResult("World", Rect(60, 0, 50, 10))
    ]
    self.context = create_ocr_scrambler_context(self.ocr_results, mouse_x=0, mouse_y=0)

  def test_no_width_string(self):
    bad_ocr_results = [
        OcrResult("Hello", Rect(0, 0, 50, 10)),
        OcrResult("\n\n\n\n", Rect(60, 0, 50, 10))
    ]
    bad_context = create_ocr_scrambler_context(bad_ocr_results, mouse_x=0, mouse_y=0)
    with self.assertRaises(ValueError):
      bad_context.index_to_screen_coordinates(8)

  def test_valid(self):
    x, y = self.context.index_to_screen_coordinates(1)
    self.assertAlmostEqual(x, 16.0, places=1)
    self.assertAlmostEqual(y, 5.0)

  def test_end_of_first_word(self):
    x, y = self.context.index_to_screen_coordinates(5)
    self.assertAlmostEqual(x, 50.0)
    self.assertAlmostEqual(y, 5.0)

  def test_start_of_last_word(self):
    x, y = self.context.index_to_screen_coordinates(6)
    self.assertAlmostEqual(x, 60.0)
    self.assertAlmostEqual(y, 5.0)

  def test_middle_of_last_word(self):
    x, y = self.context.index_to_screen_coordinates(8)
    self.assertAlmostEqual(x, 88.7, places=1)
    self.assertAlmostEqual(y, 5.0)

  def test_end_of_last_word(self):
    x, y = self.context.index_to_screen_coordinates(11)
    self.assertAlmostEqual(x, 110.0)
    self.assertAlmostEqual(y, 5.0)

  def test_line_break_after_last_word(self):
    x, y = self.context.index_to_screen_coordinates(12)
    self.assertAlmostEqual(x, 110.0)
    self.assertAlmostEqual(y, 5.0)

  def test_invalid_index(self):
    with self.assertRaises(ValueError):
      self.context.index_to_screen_coordinates(-1)

    with self.assertRaises(ValueError):
      self.context.index_to_screen_coordinates(len(self.context.text) + 2)


class OcrUtilTestCase(unittest.TestCase):
  """Util function tests."""

  def test_expand_range_to_ocr_results(self):
    # Create a sample OcrScramblerContext object
    ocr_results = [
        OcrResult("Hello", Rect(0, 0, 50, 20)),
        OcrResult("World", Rect(60, 0, 50, 20)),
        OcrResult("!", Rect(120, 0, 20, 20))
    ]
    ocr_context = OcrScramblerContext(ocr_results, "Hello World!", [0, 6, 12], 0)

    # Test expanding a range within the OCR text.
    start, end = ocr_context.expand_range_to_ocr_results(1, 3)
    self.assertEqual(start, 0)
    self.assertEqual(end, 5)

    # Test expanding a range that covers multiple OCR results
    start, end = ocr_context.expand_range_to_ocr_results(1, 8)
    self.assertEqual(start, 0)
    self.assertEqual(end, 11)

    # Test expanding a range that goes beyond the OCR text
    with self.assertRaises(ValueError):
      ocr_context.expand_range_to_ocr_results(1, 20)
