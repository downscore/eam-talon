"""Talon utils for managing configurable settings."""
# Disable linter warnings caused by Talon conventions.
# pylint: disable=no-self-argument, no-method-argument, relative-beyond-top-level
# pyright: reportSelfClsParameterName=false, reportGeneralTypeIssues=false
# mypy: ignore-errors

import csv
from pathlib import Path
from typing import Dict, List, Tuple
from talon import resource

# NOTE: This requires this module to be one folder below the top-level.
_SETTINGS_DIR = Path(__file__).parents[1] / "settings"
_PRIVATE_SETTINGS_DIR = Path(__file__).parents[2] / "private"


def _should_skip_row(row: list[str]) -> bool:
  """Check if a row should be skipped while loading a csv file."""
  # Skip empty rows. Windows newlines are sometimes read as empty rows.
  if len(row) == 0 or (len(row) == 1 and row[0].isspace()):
    return True
  # Skip comments.
  if row[0].strip().startswith("#"):
    return True
  return False


def _load_dict_internal(filename: str, rows: list[list[str]]) -> Dict[str, str]:
  """Loads a dictionary from the given CSV file rows."""
  result = {}

  # Skip header row.
  for row in rows[1:]:
    if _should_skip_row(row):
      continue

    if len(row) == 1:
      # Use single value as value and key.
      row_value = row_key = row[0]
    else:
      if len(row) > 2:
        raise ValueError(f"Dictionary CSV file has a row with more than two columns: {filename}")
      row_value, row_key = row[:2]

    # Leading/trailing whitespace in spoken form can prevent recognition.
    row_key = row_key.strip()
    result[row_key] = row_value

  print(f"Loaded dict from CSV. Rows: {len(result)}, File: {filename}")
  return result


def get_settings_file_path(filename: str) -> Path:
  """Get the full path to a settings file."""
  return _SETTINGS_DIR / filename


def load_dict_from_csv(filename: str) -> Dict[str, str]:
  """Loads a dictionary from a CSV file with Talon resource monitoring.
  Strips key values. Rows with only one column use it for both key and value."""
  path = _SETTINGS_DIR / filename
  private_path = _PRIVATE_SETTINGS_DIR / filename

  # Read via resource to take advantage of talon's ability to reload this script for us when the resource changes.
  with resource.open(str(path), "r") as f:
    rows = list(csv.reader(f))
  result = _load_dict_internal(str(path), rows)

  # Read private file if it exists. Note: Specified file must exist. Private version does not have to.
  # Returned dictionary will be updated with the contents of the private file.
  if private_path.exists():
    with resource.open(str(private_path), "r") as f:
      rows = list(csv.reader(f))
    result.update(_load_dict_internal(str(private_path), rows))

  return result


def load_lists_from_csv(filename: str) -> List[List[str]]:
  """Load a list of list of strings from a CSV file.
  A list of strings is made for the values in each non-empty line, and those lists are returned in one big list.
  This function loads the full file contents into memory, so may not be appropriate for very large lists."""
  result: List[List[str]] = []
  path = _SETTINGS_DIR / filename

  # Read via resource to take advantage of talon's ability to reload this script for us when the resource changes.
  with resource.open(str(path), "r") as f:
    rows = list(csv.reader(f))

  # No header row.
  for row in rows:
    if _should_skip_row(row):
      continue
    result.append(row)

  print(f"Loaded lists from CSV. Rows: {len(result)}, File: {filename}")
  return result


def load_coords_from_csv(filename: str) -> Dict[str, Tuple[float, float]]:
  """Loads a dictionary of labeled coordinates from a CSV file with Talon resource monitoring. Strips labels."""
  path = _SETTINGS_DIR / filename

  # Read via resource to take advantage of talon's ability to reload this script for us when the resource changes.
  with resource.open(str(path), "r") as f:
    rows = list(csv.reader(f))

  result: Dict[str, Tuple[float, float]] = {}

  # Skip header row.
  for row in rows[1:]:
    if _should_skip_row(row):
      continue

    if len(row) != 3:
      raise ValueError(f"Invalid row: {row}")

    label, x_str, y_str = row[:3]
    result[label.strip()] = (float(x_str.strip()), float(y_str.strip()))

  print(f"Loaded coords from CSV. Rows: {len(result)}, File: {filename}")
  return result


def load_macros_from_csv(filename: str) -> Dict[str, list[str]]:
  """Loads a dictionary of labeled macros from a CSV file with Talon resource monitoring. Strips labels and macro
  entries."""
  path = _SETTINGS_DIR / filename

  # Read via resource to take advantage of talon's ability to reload this script for us when the resource changes.
  with resource.open(str(path), "r") as f:
    rows = list(csv.reader(f))

  result: Dict[str, list[str]] = {}

  # No header row.
  for row in rows:
    if _should_skip_row(row):
      continue

    if len(row) < 2:
      raise ValueError(f"Invalid row: {row}")

    label = row[0].strip()
    entries = row[1:]
    map(lambda x: x.strip(), entries)

    result[label] = entries

  print(f"Loaded macros from CSV. Rows: {len(result)}, File: {filename}")
  return result


def append_to_csv(filename: str, row: List[str]):
  """Append a row to an existing CSV file."""
  path = _SETTINGS_DIR / filename

  # Do not use resource.open to avoid race condition. We want file to reload after we are finished writing to it.
  with open(str(path), "a", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(row)
