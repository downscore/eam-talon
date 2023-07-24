"""Tests for datetime utils."""

import unittest
from .datetime_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class ConvertUnixTimestampTestCase(unittest.TestCase):
  """Test for converting unix timestamps."""

  def test_convert_unix_timestamp(self):
    self.assertEqual(convert_unix_timestamp("1665150638"), datetime.datetime(2022, 10, 7, 6, 50, 38))
    self.assertEqual(convert_unix_timestamp("1665150638000"), datetime.datetime(2022, 10, 7, 6, 50, 38))
    self.assertEqual(convert_unix_timestamp("1665150638.000"), datetime.datetime(2022, 10, 7, 6, 50, 38))

  def test_datetime_to_unix(self):
    self.assertEqual(datetime_to_unix(datetime.datetime(2022, 10, 7, 6, 50, 38)), 1665150638)
