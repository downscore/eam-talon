app: vscode
-
tag(): user.line_numbers
tag(): user.multiple_cursors
tag(): user.navigation
tag(): user.splits
tag(): user.tabs

# Toggle comments.
comment dog: user.vscode("editor.action.commentLine")
comment line <user.number> [past <user.number>]:
  user.select_line_range(number_1, number_2 or 0)
  user.vscode("editor.action.commentLine")

# Copy a given line to the current location.
bring line <user.number>: user.vscode_bring_line(number)

# Show autocomplete suggest dialogue.
suggest: user.vscode("editor.action.triggerSuggest")

# Command palette
please [<user.text>]:
  user.vscode("workbench.action.showCommands")
  insert(user.text or "")

# Files
tab list [<user.text>] [<user.file_extension>]:
  user.vscode("workbench.action.quickOpen")
  sleep(250ms)
  insert(text or "")
  insert(file_extension or "")
  sleep(250ms)

# Moving cursor between matches
blinker next: user.vscode("editor.action.moveSelectionToNextFindMatch")
blinker last: user.vscode("editor.action.moveSelectionToPreviousFindMatch")

# Execution
test run all: user.vscode("testing.runAll")
test run file: user.vscode("testing.runCurrentFile")
test run blinker: user.vscode("testing.runAtCursor")
python run: user.vscode("python.execInTerminal")

# Active editor
editor: user.vscode("workbench.action.focusActiveEditorGroup")
tab keep: user.vscode("workbench.action.keepEditor")

# Sidebar
bar dog: user.vscode("workbench.action.toggleSidebarVisibility")
bar files: user.vscode("workbench.view.explorer")
bar extensions: user.vscode("workbench.view.extensions")
bar outline: user.vscode("outline.focus")
bar run: user.vscode("workbench.view.debug")
bar search: user.vscode("workbench.view.search")
bar source: user.vscode("workbench.view.scm")
bar test: user.vscode("workbench.view.testing.focus")
bar copilot: user.vscode("workbench.panel.chat.view.copilot.focus")

# Lower panel
panel dog: user.vscode("workbench.action.togglePanel")
panel output: user.vscode("workbench.panel.output.focus")
panel problem: user.vscode("workbench.panel.markers.view.focus")
panel terminal: user.vscode("workbench.action.terminal.focus")

# Formatting
format dock: user.vscode("editor.action.formatDocument")
format selection: user.vscode("editor.action.formatSelection")

# File errors
problem next: user.vscode("editor.action.marker.nextInFiles")
problem last: user.vscode("editor.action.marker.prevInFiles")
problem fix: user.vscode("problems.action.showQuickFixes")
quick fix: user.vscode("editor.action.quickFix")

# Markdown
markdown preview: user.vscode("markdown.showPreviewToSide")

# Minimap
minimap dog: user.vscode("editor.action.toggleMinimap")

# Find references and symbols
symbol hunt file [<user.text>]:
  user.vscode("workbench.action.gotoSymbol")
  sleep(50ms)
  insert(text or "")
symbol hunt all [<user.text>]:
  user.vscode("workbench.action.showAllSymbols")
  sleep(50ms)
  insert(text or "")
references: user.vscode("references-view.findReferences")
declaration: user.vscode("editor.action.revealDeclaration")
definition: user.vscode("editor.action.revealDefinition")

# Refactoring
refactor that: user.vscode("editor.action.refactor")
rename that: user.vscode("editor.action.rename")

# Copilot
copilot next: key(alt-])
copilot all: key(ctrl-enter)

# Selecting search results
hunt results:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("58.0 194.0 194.0 -28.0", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)
