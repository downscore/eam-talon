app: vscode
-
tag(): user.line_numbers
tag(): user.multiple_cursors
tag(): user.navigation
tag(): user.source_control
tag(): user.splits
tag(): user.tabs

# Toggle comments.
comment dog: user.vscode("editor.action.commentLine")
comment line <user.number> [past <user.number>]:
  user.select_line_range_including_line_break(number_1, number_2 or 0)
  user.vscode("editor.action.commentLine")

# Show autocomplete suggest dialogue.
suggest: user.vscode("editor.action.triggerSuggest")

# Accept suggestion.
yes: key(tab)

# Command palette
please [<user.text>]:
  # Alternative: user.vscode("workbench.action.showCommands")
  key(cmd-shift-p)
  user.insert_via_clipboard(user.text or "")
lucky <user.text>:
  # Alternative: user.vscode("workbench.action.showCommands")
  key(cmd-shift-p)
  user.insert_via_clipboard(user.text or "")
  sleep(200ms)
  key(enter)

# Jump to related files.
jump test: user.vscode_jump_to_test()
jump python: user.vscode_jump_to_related_file_with_extension(".py")
jump talon: user.vscode_jump_to_related_file_with_extension(".talon")

# Moving cursor between matches
blinker next: user.vscode("editor.action.moveSelectionToNextFindMatch")
blinker last: user.vscode("editor.action.moveSelectionToPreviousFindMatch")

# Set a numbered bookmark.
mark <user.number>: key("ctrl-shift-{number}")

# Jump to a matching bracket.
jump bracket: user.vscode("editor.action.jumpToBracket")

# Execution
test run all: user.vscode("testing.runAll")
test run file: user.vscode("testing.runCurrentFile")
test run blinker: user.vscode("testing.runAtCursor")
python run: user.vscode("python.execInTerminal")
python debug: user.vscode("python.debugInTerminal")

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

# Secondary sidebar (right side)
secondary dog: user.vscode("workbench.action.toggleAuxiliaryBar")

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

# Find symbols
sim list:
  # Alternative: user.vscode("workbench.action.gotoSymbol")
  key(cmd-shift-o)
sim list of <user.prose>:
  key(cmd-shift-o)
  user.insert_via_clipboard(prose)
sim jump <user.prose>:
  key(cmd-shift-o)
  user.insert_via_clipboard(prose)
  key(enter)
sim jump <user.formatters> <user.formatter_text>:
  key(cmd-shift-o)
  user.insert_via_clipboard(user.format_multiple(formatter_text, formatters))
  key(enter)
sim global:
  # Alternative: user.vscode("workbench.action.showAllSymbols")
  key(cmd-t)
sim global of <user.prose>:
  # Alternative: user.vscode("workbench.action.showAllSymbols")
  key(cmd-t)
  user.insert_via_clipboard(prose)

# Find usages and definitions
references: user.vscode("references-view.findReferences")
declaration: user.vscode("editor.action.revealDeclaration")
definition: user.vscode("editor.action.revealDefinition")

# Reverting changes.
revert that: user.vscode("git.revertSelectedRanges")

# Refactoring
refactor that: user.vscode("editor.action.refactor")
rename that: user.vscode("editor.action.rename")

# Copilot
copilot next: key(alt-])
copilot all: key(ctrl-enter)

# File management.
file new: user.vscode("explorer.newFile")

# Debugging
breakpoint toggle: user.vscode("editor.debug.action.toggleBreakpoint")
breakpoint next: user.vscode("editor.debug.action.jumpToNextBreakpoint")
breakpoint last: user.vscode("editor.debug.action.jumpToPreviousBreakpoint")

# Selecting search results
hunt results:
  bounding_rectangle = user.mouse_helper_calculate_relative_rect("58.0 194.0 194.0 -28.0", "active_window")
  user.mouse_helper_blob_picker(bounding_rectangle)
