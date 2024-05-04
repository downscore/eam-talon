"""Utilities for encoding and decoding strings."""

import string


def encode_rot13(text):
  """Encodes text using ROT13."""
  # Creating translation tables for uppercase and lowercase letters
  uppercase = string.ascii_uppercase
  lowercase = string.ascii_lowercase

  # Creating mapping for ROT13 transformation
  rot13_upper = str.maketrans(uppercase, uppercase[13:] + uppercase[:13])
  rot13_lower = str.maketrans(lowercase, lowercase[13:] + lowercase[:13])

  # Applying ROT13 transformation using the translation tables
  return text.translate(rot13_upper).translate(rot13_lower)
