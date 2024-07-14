mode: sleep
speech.engine: wav2letter
-
# This exists solely to prevent talon from waking up super easily in sleep mode at the moment with
# wav2letter. There probably shouldn't be any other commands here.
# TODO: Is this still necessary?
<phrase>: skip()
