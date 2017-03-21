# python-musicbox
This is a simple command-line musicbox.
Put it on your path and fire it up!
# Usage
`musicbox shuffle [folders]`

Shuffles infinitely from either all folders in the directory, or the given folders.

`musicbox replace [regex pattern] [text] [folder]`

Renames files, replacing the regex pattern with the text.

`musicbox get [URL] [folder]`

Creates the folder if it does not exist, then runs `youtube-dl` in it.

`musicbox convert`

Converts all non-WAV files to WAVs.
