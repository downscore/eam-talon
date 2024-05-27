"""Library for helping with path-related tasks."""

import os


def replace_file_extension(path: str, new_extension: str) -> str:
  """Replaces the file extension of a given path."""
  if not path:
    raise ValueError("Empty path.")

  file, _ = os.path.splitext(path)
  return file + new_extension


def remove_test_suffix(path: str) -> str:
  """Removes the "_test" suffix from the given filename before extension if it is present."""
  if not path:
    raise ValueError("Empty path.")

  file, extension = os.path.splitext(path)
  if file.endswith("_test"):
    return file[:-5] + extension
  return path


def get_test_path(path: str, extension: str) -> str:
  """Returns the path to the test file associated with the given path."""
  if not path:
    raise ValueError("Empty path.")

  # Remove test suffix if it is already present.
  no_test = remove_test_suffix(path)

  file, _ = os.path.splitext(no_test)
  return file + "_test" + extension
