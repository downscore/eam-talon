* Tools (configured in workspace):
  * pylint
  * mypy
  * pytest
* Extensions:
  * Coverage Gutters
  * multi-command
  * Talon (Command server)
* Run coverage on save:
  * Bind `cmd-s` to `multiCommand.saveAndTest` in global settings.
  * Override `multiCommand.saveAndTest` to run pytest with coverage in workspace.
  * Do not add coverage flags to global/workspace pytest args, as it causes problems.
    * Prevents debugging tests from working properly.
    * Causes a zero-coverage file to be generated every time test auto-discovery runs.
* Copy Talon packagew from `Talon.app` to python lib directory. Allows VS Code to see Talon API.
```
sudo mkdir /opt/local/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages

sudo cp -R /Applications/Talon.app/Contents/Resources/python/lib/python3.9/site-packages/talon \
  /opt/local/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages
```
