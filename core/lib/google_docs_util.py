"""Util functions for Google Docs."""


def get_preview_url(edit_url: str):
  """Returns a doc's preview Url given its edit Url."""
  # Idempotent if already a preview Url.
  if edit_url.find("/preview") >= 0:
    return edit_url

  edit_index = edit_url.find("/edit")
  if edit_index >= 0:
    return edit_url[:edit_index] + "/preview"

  edit_index = edit_url.find("#")
  if edit_index >= 0:
    return edit_url[:edit_index] + "/preview"

  if edit_url[-1] == "/":
    return edit_url + "preview"
  return edit_url + "/preview"
