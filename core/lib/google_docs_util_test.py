"""Tests for Google Docs utils."""

import unittest
from .google_docs_util import *  # pylint: disable=wildcard-import, unused-wildcard-import


class GetPreviewUrlTestCase(unittest.TestCase):
  """Test for counting lines in a string."""

  def test_get_preview_url(self):
    self.assertEqual(get_preview_url("/edit"), "/preview")
    self.assertEqual(
        get_preview_url("https://docs.google.com/document/d/ABCDefghiJKLMnoPqRSTUVwxyz/edit#"),
        "https://docs.google.com/document/d/ABCDefghiJKLMnoPqRSTUVwxyz/preview")
    self.assertEqual(
        get_preview_url(
            "https://docs.google.com/document/d/ABCDefgh123/edit#heading=h.abcdefg12345"),
        "https://docs.google.com/document/d/ABCDefgh123/preview")
    self.assertEqual(get_preview_url("https://docs.google.com/document/d/ABCDefgh123"),
                     "https://docs.google.com/document/d/ABCDefgh123/preview")
    self.assertEqual(get_preview_url("https://docs.google.com/document/d/ABCDefgh123/"),
                     "https://docs.google.com/document/d/ABCDefgh123/preview")
    self.assertEqual(
        get_preview_url("https://docs.google.com/document/d/ABCDefgh123#heading=h.1234"),
        "https://docs.google.com/document/d/ABCDefgh123/preview")
    # Preview URLs are idempotent.
    self.assertEqual(get_preview_url("https://docs.google.com/document/d/ABCDefgh123/preview"),
                     "https://docs.google.com/document/d/ABCDefgh123/preview")
