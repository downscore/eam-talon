"""Tests for encoding utils."""

import unittest
from .encoding_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class ROT13TestCase(unittest.TestCase):
  """Test for ROT13 encoding."""

  def test_rot13_encode(self):
    self.assertEqual(encode_rot13("abc"), "nop")
    self.assertEqual(encode_rot13("nop"), "abc")
    self.assertEqual(encode_rot13("Hello, World!"), "Uryyb, Jbeyq!")
    self.assertEqual(encode_rot13("Uryyb, Jbeyq!"), "Hello, World!")
