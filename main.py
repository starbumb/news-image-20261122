#!/usr/bin/env python3
"""News-image entry for 22 November 2026 (Python 3, standard library only).

The image is the entry.png beside this file, drawn programmatically by
draw.py. This program copies it to /output/entry.png (or to
$MAKEFUN_OUTPUT_DIR when set, for local runs).
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())
