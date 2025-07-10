#!/usr/bin/env python3
"""
Make Magnum Steno dictionaries work better with the Plover CAT software.

Example usage:
    python3 apply_magnum_auto_fixes.py magnum.json magnum_fixed.json
"""

import re
import argparse
import json


MAGNUM_TRANSFORMATIONS = [
    # DigitalCAT uses ^ alone as a non-breaking space. Change these to actual
    # NBSPs.
    (r"(?<!\{)\^(?!\})", "\u00a0"),
    # Question and Answer formats are translated as bare Q and A characters.
    # Format them as initials.
    (r"\\n\\nQ", r"\\n\\nQ. "),
    (r"\{\^\\n\\n\^\}Q", r"{^\\n\\n^}Q. "),
    (r"\\n\\nA", r"\\n\\nA. "),
    (r"\{\^\\n\\n\^\}A", r"{^\\n\\n^}A. "),
    # Paragraph styles don't exist in Plover. Replace with double newline to be
    # consistent with Q/A.
    (r"\{P .*?\}", r"{^\\n\\n^}"),
    # Convert DigitalCAT macros.
    (r" \"(.*?)\{@CAPWORD\(LASTWORD\)\}\"", r" \"{\*-|}\\1\""),
    # Plover doesn't have a way to 'skip' a space, so SECONDSPACE is identical
    # to FIRSTSPACE instead of replacing the second-to-last hyphen with a space.
    # Requires plover_retro_text_transform.
    (r"\{@HYPHENATE\(FIRSTSPACE\)\}", r"{:retro_replace_space:1:-}"),
    (r"\{@HYPHENATE\(SECONDSPACE\)\}", r"{:retro_replace_space:1:-}"),
    # Plover style is single-spaced. Convert double spaces to single spaces.
    ("\u00a0 ", "\u00a0"),
    (r"  ", r" "),
    # Trailing spaces result in double-spacing, remove them.
    (r" \}", r"}"),
    # NOTE: This regex is invalid, and didn't appear in the Magnum 08-28-2024
    # dictionary; so I've disabled it.
    # (r"(?<=: \".*?) \"", r"\""),
    (r" \{-|\}\"", r"{-|}\""),
]


def apply_magnum_fixes(text):
    for pattern, replacement in MAGNUM_TRANSFORMATIONS:
        text = re.sub(pattern, replacement, text)
    return text


def process_json_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key, value in data.items():
        if isinstance(value, str):
            data[key] = apply_magnum_fixes(value)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



def main():
    parser = argparse.ArgumentParser(
        description="Make DigitalCAT dictionaries work better with Plover"
    )
    parser.add_argument("input_file", help="Input JSON file")
    parser.add_argument("output_file", help="Output JSON file")
    args = parser.parse_args()

    process_json_file(args.input_file, args.output_file)
    print(f"Successfully processed {args.input_file} -> {args.output_file}")


if __name__ == "__main__":
    main()
