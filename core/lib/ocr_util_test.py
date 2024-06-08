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


class CreateOcrTextflowContextTestCase(unittest.TestCase):
  """Util function tests."""

  def test_empty_ocr_results(self):
    with self.assertRaises(ValueError):
      create_ocr_textflow_context([], 0, 0)

  def test_single_ocr_result(self):
    ocr_results = [OcrResult("Test", Rect(0, 0, 10, 10))]
    context = create_ocr_textflow_context(ocr_results, 5, 5)
    self.assertEqual(context.text, "Test\n")
    self.assertEqual(context.start_indices, [0])
    self.assertEqual(context.mouse_index, 0)

  def test_multiple_ocr_results(self):
    ocr_results = [
        OcrResult("First", Rect(0, 0, 10, 10)),
        OcrResult("Second", Rect(20, 20, 10, 10)),
        OcrResult("Third", Rect(40, 40, 10, 10))
    ]
    context = create_ocr_textflow_context(ocr_results, 25, 25)
    self.assertEqual(context.text, "First\nSecond\nThird\n")
    self.assertEqual(context.start_indices, [0, 6, 13])
    self.assertEqual(context.mouse_index, 6)  # "Second" is the closest to (25, 25)

  def test_closest_result_to_mouse(self):
    ocr_results = [
        OcrResult("A", Rect(0, 0, 10, 10)),
        OcrResult("B", Rect(100, 100, 10, 10)),
        OcrResult("C", Rect(50, 50, 10, 10))
    ]
    context = create_ocr_textflow_context(ocr_results, 52, 52)
    self.assertEqual(context.text, "A\nB\nC\n")
    self.assertEqual(context.start_indices, [0, 2, 4])
    self.assertEqual(context.mouse_index, 4)  # "C" is the closest to (52, 52)


class IndexToScreenCoordinatesTestCase(unittest.TestCase):
  """Util function tests."""

  def setUp(self):
    self.ocr_results = [OcrResult("Hello", Rect(0, 0, 50, 10)), OcrResult("World", Rect(60, 0, 50, 10))]
    self.context = create_ocr_textflow_context(self.ocr_results, mouse_x=0, mouse_y=0)

  def test_valid(self):
    x, y = self.context.index_to_screen_coordinates(1)
    self.assertAlmostEqual(x, 10.0)
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
    self.assertAlmostEqual(x, 80.0)
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
