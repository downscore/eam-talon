# Talon API

## System Actions
* **app.bundle() -> str**
  * Get active app's bundle identifier
* **app.executable() -> str**
  * Get active app's executable name
* **app.name() -> str**
  * Get active app's name
* **app.notify(body: str = '', title: str = '', subtitle: str = '', sound: bool = False)**
  * Show a desktop notification
* **app.path() -> str**
  * Get active app's file path
* **clip.capture_text(key: str)**
  * Send key sequence and return resulting clipboard text
* **clip.clear() -> None**
  * Clear clipboard contents
* **clip.image() -> Optional[talon.skia.image.Image]**
  * Get clipboard image
* **clip.set_image(image: talon.skia.image.Image)**
  * Set clipboard image
* **clip.set_text(text: str)**
  * Set clipboard text
* **clip.text() -> str**
  * Get clipboard text
* **core.cancel_phrase__unstable()**
  * Cancel the currently running phrase
core.current_command__unstable() -> Tuple[talon.scripting.* *t*ypes.CommandImpl, talon.grammar.vm.Capture]**
  * Return the currently executing command
core.last_command() -> Tuple[talon.scripting.types.* *C*ommandImpl, talon.grammar.vm.Capture]**
  * Return the last executed command
* **core.last_phrase() -> talon.grammar.vm.Capture**
  * Return the last-spoken phrase
core.recent_commands() -> Sequence[Sequence[Tuple[talon.* *s*cripting.types.CommandImpl, talon.grammar.vm.Capture]]]**
  * Return recently executed commands (grouped by phrase)
* *core.recent_phrases() -> Sequence[talon.grammar.vm.***Capture]
  * Return recently-spoken phrases
* **core.repeat_command(times: int = 1)**
  * Repeat the last command N times
* **core.repeat_partial_phrase(times: int = 1)**
  * Repeat the previous phrase or current partial phrase N times
* **core.repeat_phrase(times: int = 1)**
  * Repeat the last phrase N times
core.replace_command(commands: Sequence[Tuple[talon.* *s*cripting.types.CommandImpl, talon.grammar.vm.Capture]])**
  * Replace the current command in history with one or more commands
core.run_command(cmd: talon.scripting.types.CommandImpl, m: * **talon.grammar.vm.Capture)**
  * Run a single command for a recognized phrase
* *core.run_hotkey(hotkey: talon.scripting.types.ScriptImpl)***
  * Run all commands for a hotkey
* **core.run_phrase(phrase: talon.grammar.vm.Capture)**
  * Run all commands for a recognized phrase
core.run_talon_script(ctx: talon.scripting.rctx.ResourceContext, script: talon.scripting.talon_script.* *T*alonScript, m: talon.grammar.vm.Capture)**
  * Run a single TalonScript for a recognized phrase
dictate.join_words(words: Sequence[str], separator: str = ' * **') -> str**
  * Join a list of words into a single string for insertion
* **dictate.lower(p: talon.grammar.vm.Phrase)**
  * Insert lowercase text with auto_insert()
* **dictate.natural(p: talon.grammar.vm.Phrase)**
  * Insert naturally-capitalized text with auto_insert()
* **dictate.parse_words(p: talon.grammar.vm.Phrase) -> Sequence* *[*str]**
  * Extract words from a spoken Capture
* **dictate.replace_words(words: Sequence[str]) -> Sequence**[str]
  * Replace words according to the dictate.word_map dictionary setting
* **auto_format(text: str) -> str**
  * Apply text formatting, such as auto spacing, for the native language
* **auto_insert(text: str)**
  * Insert text at the current cursor position, automatically formatting it using the actions.auto_format(text)
* **insert(text: str)**
  * Insert text at the current cursor position
* **key(key: str)**
  * Press one or more keys by name, space-separated
* **mimic(text: str)**
  * Simulate speaking {text}
* **mouse_click(button: int = 0)**
  * Press and release a mouse button
* **mouse_drag(button: int = 0)**
  * Hold down a mouse button
* **mouse_move(x: float, y: float)**
  * Move mouse to (x, y) coordinate
* **mouse_release(button: int = 0)**
  * Release a mouse button
* **mouse_scroll(y: float = 0, x: float = 0, by_lines: bool = False)**
  * Scroll the mouse wheel
* **mouse_x() -> float**
  * Mouse X position
* **mouse_y() -> float**
  * Mouse Y position
* **print(obj: Any)**
  * Display an object in the log
* **skip()**
  * Do nothing
* **sleep(duration: Union[float, str])**
  * Pause for some duration.
  * If you use a number, it is seconds, e.g 1.5 seconds or 0.001 seconds.
  * If you use a string, it is a timespec, such as "50ms" or "10s"
  * For performance reasons, sleep() cannot be reimplemented by a Context.
* **migrate.backup_user()**
  * Backup the .talon/user/ directory to a zip file in .talon/backups/
* **migrate.v02_all(prefix: str = '', verbose: bool = False)**
  * Perform migrations for Talon v0.2 on all files in user/
* **migrate.v02_one(path: str, verbose: bool = False)**
  * Migrate action() definitions from a .talon file to a new Python file.
* **mode.disable(mode: str)**
  * Disable a mode
* **mode.enable(mode: str)**
  * Enable a mode
* **mode.restore()**
  * Restore saved modes
* **mode.save()**
  * Save all active modes
* **mode.toggle(mode: str)**
  * Toggle a mode
* **path.talon_app() -> str**
  * Path to Talon application
* **path.talon_home() -> str**
  * Path to home/.talon
* **path.talon_user() -> str**
  * Path to Talon user
* **path.user_home() -> str**
  * Path to user home
* **speech.disable()**
  * Disable speech recognition
* **speech.enable()**
  * Enable speech recognition
* **speech.enabled() -> bool**
  * Test if speech recognition is enabled
* **speech.record_flac()**
  * Record the phrase audio to a flac file
* **speech.record_wav()**
  * Record the phrase audio to a wave file
* **speech.replay(path: str)**
  * Replay a .flac or .wav file into the speech engine
* **speech.set_microphone(name: str)**
  * Set the currently active microphone - DEPRECATED
* **speech.toggle(value: bool = None)**
  * Toggle speech recognition
* **sound.active_microphone() -> str**
  * Return active microphone name
* **sound.microphones() -> Sequence\[str\]**
  * Return a list of available microphone names
* **sound.set_microphone(name: str)**
  * Set the currently active microphone
* **win.file_ext() -> str**
  * Return the open file's extension
* **win.filename() -> str**
  * Return the open filename
* **win.title() -> str**
  * Get window title
* **menu.check_for_updates()**
  * Check for updates
* **menu.open_log()**
  * Open Talon log
* **menu.open_repl()**
  * Open Talon REPL
* **menu.open_talon_home()**
  * Open Talon config folder

## Built-in actions

* **app.preferences()**
  * Open app preferences
* **app.tab_close()**
  * Close the current tab
* **app.tab_detach()**
  * Move the current tab to a new window
* **app.tab_next()**
  * Switch to next tab for this window
* **app.tab_open()**
  * Open a new tab
* **app.tab_previous()**
  * Switch to previous tab for this window
* **app.tab_reopen()**
  * Re-open the last-closed tab
* **app.window_close()**
  * Close the current window
* **app.window_hide()**
  * Hide the current window
* **app.window_hide_others()**
  * Hide all other windows
* **app.window_next()**
  * Switch to next window for this app
* **app.window_open()**
  * Open a new window
* **app.window_previous()**
  * Switch to previous window for this app
* **browser.address() -> str**
  * Get page URL
* **browser.bookmark()**
  * Bookmark the current page
* **browser.bookmark_tabs()**
  * Bookmark all open tabs
* **browser.bookmarks()**
  * Open the Bookmarks editor
* **browser.bookmarks_bar()**
  * Toggle the bookmarks bar
* **browser.focus_address()**
  * Focus address bar
* **browser.focus_page()**
  * Focus the page body
* **browser.focus_search()**
  * Focus the search box
* **browser.go(url: str)**
  * Go to a new URL
* **browser.go_back()**
  * Go back in the history
* **browser.go_blank()**
  * Go to a blank page
* **browser.go_forward()**
  * Go forward in the history
* **browser.go_home()**
  * Go to home page
* **browser.open_private_window()**
  * Open a private browsing window
* **browser.reload()**
  * Reload current page
* **browser.reload_hard()**
  * Reload current page (harder)
* **browser.reload_hardest()**
  * Reload current page (hardest)
* **browser.show_clear_cache()**
  * Show 'Clear Cache' dialog
* **browser.show_downloads()**
  * Show download list
* **browser.show_extensions()**
  * Show installed extensions
* **browser.show_history()**
  * Show recently visited pages
* **browser.submit_form()**
  * Submit the current form
* **browser.title() -> str**
  * Get page title
* **browser.toggle_dev_tools()**
  * Open or close the developer tools
* **code.complete()**
  * Trigger code autocomplete
* **code.extend_scope_end()**
  * Extend selection to end of current scope
* **code.extend_scope_in()**
  * Extend selection to start of first inner scope
* **code.extend_scope_next()**
  * Extend selection to start of next sibling scope
* **code.extend_scope_out()**
  * Extend selection to start of outer scope
* **code.extend_scope_previous()**
  * Extend selection to start of previous sibling scope
* **code.extend_scope_start()**
  * Extend selection to start of current scope
* **code.language() -> str**
  * Return the active programming language
* **code.rename(name: str)**
  * Rename selection to \<name\>
* **code.scope_end()**
  * Move cursor to end of current scope
* **code.scope_in()**
  * Move cursor to start of first inner scope
* **code.scope_next()**
  * Move cursor to start of next sibling scope
* **code.scope_out()**
  * Move cursor to start of outer scope
* **code.scope_previous()**
  * Move cursor to start of previous sibling scope
* **code.scope_start()**
  * Move cursor to start of current scope
* **code.select_scope()**
  * Select scope under cursor
* **code.toggle_comment()**
  * Toggle comments on the current line(s)
* **edit.copy()**
  * Copy selection to clipboard
* **edit.cut()**
  * Cut selection to clipboard
* **edit.delete()**
  * Delete selection
* **edit.delete_line()**
  * Delete line under cursor
* **edit.delete_paragraph()**
  * Delete paragraph under cursor
* **edit.delete_sentence()**
  * Delete sentence under cursor
* **edit.delete_word()**
  * Delete word under cursor
* **edit.down()**
  * Move cursor down one row
* **edit.extend_again()**
  * Extend selection again in the same way
* **edit.extend_column(n: int)**
  * Extend selection to column \<n\>
* **edit.extend_down()**
  * Extend selection down one row
* **edit.extend_file_end()**
  * Extend selection to end of file
* **edit.extend_file_start()**
  * Extend selection to start of file
* **edit.extend_left()**
  * Extend selection left one column
* **edit.extend_line(n: int)**
  * Extend selection to include line \<n\>
* **edit.extend_line_down()**
  * Extend selection down one full line
* **edit.extend_line_end()**
  * Extend selection to end of line
* **edit.extend_line_start()**
  * Extend selection to start of line
* **edit.extend_line_up()**
  * Extend selection up one full line
* **edit.extend_page_down()**
  * Extend selection down one page
* **edit.extend_page_up()**
  * Extend selection up one page
* **edit.extend_paragraph_end()**
  * Extend selection to the end of the current paragraph
* **edit.extend_paragraph_next()**
  * Extend selection to the start of the next paragraph
* **edit.extend_paragraph_previous()**
  * Extend selection to the start of the previous paragraph
* **edit.extend_paragraph_start()**
  * Extend selection to the start of the current paragraph
* **edit.extend_right()**
  * Extend selection right one column
* **edit.extend_sentence_end()**
  * Extend selection to the end of the current sentence
* **edit.extend_sentence_next()**
  * Extend selection to the start of the next sentence
* **edit.extend_sentence_previous()**
  * Extend selection to the start of the previous sentence
* **edit.extend_sentence_start()**
  * Extend selection to the start of the current sentence
* **edit.extend_up()**
  * Extend selection up one row
* **edit.extend_word_left()**
  * Extend selection left one word
* **edit.extend_word_right()**
  * Extend selection right one word
* **edit.file_end()**
  * Move cursor to end of file (start of line)
* **edit.file_start()**
  * Move cursor to start of file
* **edit.find(text: str = None)**
  * Open Find dialog, optionally searching for text
* **edit.find_next()**
  * Select next Find result
* **edit.find_previous()**
  * Select previous Find result
* **edit.indent_less()**
  * Remove a tab stop of indentation
* **edit.indent_more()**
  * Add a tab stop of indentation
* **edit.jump_column(n: int)**
  * Move cursor to column \<n\>
* **edit.jump_line(n: int)**
  * Move cursor to line \<n\>
* **edit.left()**
  * Move cursor left one column
* **edit.line_clone()**
  * Create a new line identical to the current line
* **edit.line_down()**
  * Move cursor to start of line below
* **edit.line_end()**
  * Move cursor to end of line
* **edit.line_insert_down()**
  * Insert line below cursor
* **edit.line_insert_up()**
  * Insert line above cursor
* **edit.line_start()**
  * Move cursor to start of line
* **edit.line_swap_down()**
  * Swap the current line with the line below
* **edit.line_swap_up()**
  * Swap the current line with the line above
* **edit.line_up()**
  * Move cursor to start of line above
* **edit.move_again()**
  * Move cursor again in the same way
* **edit.page_down()**
  * Move cursor down one page
* **edit.page_up()**
  * Move cursor up one page
* **edit.paragraph_end()**
  * Move cursor to the end of the current paragraph
* **edit.paragraph_next()**
  * Move cursor to the start of the next paragraph
* **edit.paragraph_previous()**
  * Move cursor to the start of the previous paragraph
* **edit.paragraph_start()**
  * Move cursor to the start of the current paragraph
* **edit.paste()**
  * Paste clipboard at cursor
* **edit.paste_match_style()**
  * Paste clipboard without style information
* **edit.print()**
  * Open print dialog
* **edit.redo()**
  * Redo
* **edit.right()**
  * Move cursor right one column
* **edit.save()**
  * Save current document
* **edit.save_all()**
  * Save all open documents
* **edit.select_all()**
  * Select all text in the current document
* **edit.select_line(n: int = None)**
  * Select entire line \<n\>, or current line
* **edit.select_lines(a: int, b: int)**
  * Select entire lines from \<a\> to \<b\>
* **edit.select_none()**
  * Clear current selection
* **edit.select_paragraph()**
  * Select the entire nearest paragraph
* **edit.select_sentence()**
  * Select the entire nearest sentence
* **edit.select_word()**
  * Select word under cursor
* **edit.selected_text() -> str**
  * Get currently selected text
* **edit.selection_clone()**
  * Insert a copy of the current selection
* **edit.sentence_end()**
  * Move cursor to the end of the current sentence
* **edit.sentence_next()**
  * Move cursor to the start of the next sentence
* **edit.sentence_previous()**
  * Move cursor to the start of the previous sentence
* **edit.sentence_start()**
  * Move cursor to the start of the current sentence
* **edit.undo()**
  * Undo
* **edit.up()**
  * Move cursor up one row
* **edit.word_left()**
  * Move cursor left one word
* **edit.word_right()**
  * Move cursor right one word
* **edit.zoom_in()**
  * Zoom in
* **edit.zoom_out()**
  * Zoom out
* **edit.zoom_reset()**
  * Zoom to original size

## REPL Commands
* `sim("spoken phrase")`
  * Shows how a spoken phrase is matched by scripts.
* `actions.list()`
  * Lists all available actions.
* `ui.apps()`
  * List running apps.
```python
>>> ui.apps(bundle="com.apple.Safari")
[App(pid=546, "Safari")]
>>> ui.apps(name="Slack")
[App(pid=571, "Slack")]
```

## Noise
```python
from talon import noise, ctrl, actions

def pop_handler(active: bool):
  actions.mouse_drag(0)
  actions.sleep("150ms")
  actions.mouse_release(0)

noise.register("pop", pop_handler)
```

## Apple Accessibility API
### Chrome URL
```python
app = ui.apps(bundle="com.google.Chrome")[0]
window = app.windows()[0]
web_area = window.element.children.find_one(AXRole='AXWebArea')
address = web_area.AXURL
```
### Safari URL
```python
# Set max_depth to prevent call from checking the entire DOM and taking too long.
address_field = window.element.children.find_one(
    AXRole='AXTextField', AXIdentifier='WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD', max_depth=2)
address = address_field.AXValue
```
```python
ui.apps(bundle="com.apple.Safari")[0].windows()[0].element.children.find_one(
    AXRole='AXTextField', AXIdentifier='WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD', max_depth=2).AXValue
```
```python
ui.apps(bundle="com.microsoft.VSCode")[0].windows()[0].element
```
### Notes
```python
add_button = notes_id.windows()[0].findAllR(AXRole='AXButton', AXRoleDescription='button', AXDescription='add')[0]
note = notes_id.windows()[0].findAllR(AXRole='AXWebArea', AXRoleDescription='HTML content', AXDescription='')[0]
```
### Attributes
```
[el.attrs for el in ui.active_window().children.find()]
```

## talon.ui
* `ui.base64.b64encode()`
* `ui.active_window().title`

## Numpad Keys
`keypad_8` etc.

## Python Libraries
`/Applications/Talon.app/Contents/Resources/python/lib/python3.9/site-packages`

## Check Function Signature
```
>>> import inspect
>>> inspect.signature
<function signature at 0x10d048040>
>>> inspect.signature(talon.clip.has_mode)
```

## Accessibility API

```
(
'AXAccessKey',
'AXBlockQuoteLevel',
'AXChildren',
'AXColumnHeaderUIElements',
'AXDescription',
'AXDOMClassList',
'AXDOMIdentifier',
'AXEditableAncestor',
'AXElementBusy',
'AXEnabled',
'AXEndTextMarker',
'AXFocusableAncestor',
'AXFocused',
'AXFrame',
'AXHelp',
'AXHighestEditableAncestor',
'AXInsertionPointLineNumber',
'AXInvalid',
'AXLinkedUIElements',
'AXNumberOfCharacters',
'AXOwns',
'AXParent',
'AXPlaceholderValue',
'AXPosition',
'AXRequired',
'AXRole',
'AXRoleDescription',
'AXSelected',
'AXSelectedText',
'AXSelectedTextMarkerRange',
'AXSelectedTextRange',
'AXSelectedTextRanges'
'AXSize',
'AXStartTextMarker',
'AXSubrole',
'AXTitle',
'AXTitleUIElement',
'AXTopLevelUIElement',
'AXURL',
'AXValue',
'AXValueAutofillAvailable',
'AXVisibleCharacterRange',
'AXVisited',
'AXWindow',
'ChromeAXNodeId',
)
```

## URLs
### Search
https://search.talonvoice.com/search/
### Cursorless
https://github.com/cursorless-dev/cursorless
### Accessibility Integration
https://github.com/phillco/talon-axkit
### Talon HUD
https://github.com/chaosparrot/talon_hud
### Knausj Forks
https://github.com/pokey/pokey_talon

API Notes
- [ ] VS Code: Set editor.accessibilityPageSize (e.g. to 150) to allow TextFlow to work in long files. Setting value appears to be total number of lines visible to accessibility API
- [ ] Canvas for onscreen rendering
- [ ] Action documentation: my_func.__doc__
- [ ] python/pip executable for Talon: ~/.talon/.venv/bin/python
- [ ] Module vs Context action class
    - [ ] Module actions define totally new actions in the user namespace
    - [ ] Context actions overwrite/implement actions from any namespace
- [ ] Tags and modes have same implementation. Only use tags?
- [ ] App-specific vocabulary: Set user.vocabulary based on context.
- [ ] Find image on screen: from talon.experimental import locate
- [ ] REPL
    - [ ] import inspect
    - [ ] inspect.signature(talon.clip.setimage)
    - [ ] inspect.getdoc(talon.clip.setimage)
    - [ ] settings.list()
    - [ ] actions.list()
    - [ ] registry.__dict__.keys()
- [ ] talon.canvas uses Skia canvases behind the scenes
- [ ] To copy actions to the clipboard from REPL: import io;old=sys.stdout;sys.stdout = io.StringIO();actions.list();clip.set_text(sys.stdout.getvalue());sys.stdout = old
