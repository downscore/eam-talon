```python
from talon import app as app
from talon.api import ffi as ffi, ffi_string as ffi_string, lib as lib
from talon.lib.time import sleep as sleep
from talon.skia import Image as Image
from typing import Generator, Optional

# Check if a clipboard mode is supported.
# Useful modes: "main", "select", "find"
def has_mode(mode: str = None) -> bool: ...

# Get the text contents of the clipboard.
def text(*, mode: str = None, tries: int = None) -> Optional[str]: ...

# Set the text contents of the clipboard.
def set_text(s: str, *, mode: str = None) -> None: ...

def get() -> Optional[str]: ...
def set(s: str): ...

# Get the image contents of the clipboard.
def image(*, mode: str = None) -> Optional[Image]: ...

# Set the image contents of the clipboard.
def set_image(image: Image, *, mode: str = None) -> None: ...

# Clear the clipboard.
def clear(*, mode: str = None) -> None: ...

def serial(*, mode: str = None) -> int: ...
def await_change(timeout: float = 0.5, *, after: int = None, old: str = None, mode: str = None) -> Optional[str]: ...

class NoChange(Exception): ...

class ChangePromise:
    data: Optional[str]
    complete: bool
    def __bool__(self) -> bool: ...
    def get(self) -> str: ...

# Restore the old text of the clipboard after running a block:
# from talon import clip
# with clip.revert():
#     clip.set_text("this will only be set temporarily")
def revert(*, old: str = None, mode: str = None) -> Generator[None, None, None]: ...

# Capture a change in the clipboard, then restore the old text contents:
# from talon import actions, clip
# with clip.capture() as s:
#     actions.edit.copy()
# print(s.get())
def capture(timeout: float = 0.5, *, inc: int = 0, mode: str = None) -> Generator[ChangePromise, None, None]: ...
```
