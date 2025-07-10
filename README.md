# magnum_plover_fixes

A set of fixes to make a Magnum Steno dictionary work with the Plover
CAT software better.

Files:
- `apply_magnum_auto_fixes.py`: A script that applies (most) fixes.
    - NOTE1: A small number of Magnum entries require the
        `plover_retro_text_transform` plugin to be installed.
    - NOTE2: This script requires the Magnum Steno dictionary to be in the json
        format already (if you have only the rtf, you can convert it to json by
        right clicking on it in Plover and saving a copy of it).

- `magnum_fixes.json`: a working dictionary of fixes that aren't easily automated.

- `commands.json`: an original dictionary providing various Plover and formatting
    commands and ideally should not conflict too much with Magnum.
