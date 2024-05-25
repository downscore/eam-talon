"""Library for helping with app-related tasks."""

from . import format_util


def filename_to_app_launch_string(filename: str, overrides: dict[str, str]) -> str:
  """Converts an app filename to a string suitable for use in an app launch command."""
  app_name = filename

  # Remove everything after the last dot in the filename.
  if "." in app_name:
    app_name = app_name.rsplit(".", 1)[0]

  # Apply overrides.
  if app_name in overrides:
    app_name = overrides[app_name]

  # Unformat the name (split on case changes, etc.).
  app_name = format_util.unformat_phrase(app_name)
  app_name = app_name.lower()

  # Remove all characters except the alphabet and spaces.
  result = ""
  for c in app_name:
    if not c.isalpha() and c != " ":
      continue
    # Don't write two spaces in a row.
    if c == " " and result.endswith(" "):
      continue
    result += c
  result = result.strip()

  # TODO: Replace numbers with spoken forms.
  return result
