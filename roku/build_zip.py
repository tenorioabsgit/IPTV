#!/usr/bin/env python3
"""Build SepulnationTV Roku app as a deployable ZIP package."""

import os
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_ZIP = os.path.join(SCRIPT_DIR, "SepulnationTV.zip")

INCLUDE_DIRS = ["source", "components", "images"]
INCLUDE_FILES = ["manifest"]


def build():
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add top-level files
        for fname in INCLUDE_FILES:
            fpath = os.path.join(SCRIPT_DIR, fname)
            if os.path.exists(fpath):
                zf.write(fpath, fname)
                print(f"  + {fname}")

        # Add directories recursively
        for dirname in INCLUDE_DIRS:
            dirpath = os.path.join(SCRIPT_DIR, dirname)
            if not os.path.isdir(dirpath):
                print(f"  ! Missing directory: {dirname}")
                continue
            for root, _, files in os.walk(dirpath):
                for f in files:
                    filepath = os.path.join(root, f)
                    arcname = os.path.relpath(filepath, SCRIPT_DIR)
                    zf.write(filepath, arcname)
                    print(f"  + {arcname}")

    size_kb = os.path.getsize(OUTPUT_ZIP) / 1024
    print(f"\nBuild complete: {OUTPUT_ZIP} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    print("Building SepulnationTV Roku app...\n")
    build()
