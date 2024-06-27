os: mac
-
notes close: user.notifications_close()
hidden files dog: key(cmd-shift-.)
spotlight: user.macos_spotlight()
mission control: key(ctrl-up)

# Settings pages.
settings sound: user.macos_spotlight("Sound output")
settings (privacy|security): user.macos_spotlight("Privacy & Security")
settings update: user.macos_spotlight("Software Update")

# Change audio output device.
# Note: These commands are not chainable.
^sound output built in$: user.macos_change_sound_output_device("MacBook Pro Speakers")
^sound output scarlet$: user.macos_change_sound_output_device("Scarlett")
^sound output headset$: user.macos_change_sound_output_device("Sennheiser")
