#!/usr/bin/env python3
"""news-image-20261124 entry program.

Writes one image, the front page summing up Tuesday 24 November 2026,
to /output/entry.png.

The front page itself is built by compose.py in this repository (four
clean scene panels generated for this entry, laid out with a masthead and
PIL-drawn headline bars) and shipped as entry.png. This program only
copies that image to the output path, so it is deterministic: it runs
twice and writes the same bytes both times. No network, standard library
only, Python 3.13.
"""

import hashlib
import os
import shutil
import sys

OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, OUTPUT_NAME)
    if not os.path.isfile(source):
        print("missing %s next to main.py" % OUTPUT_NAME, file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    shutil.copyfile(source, target)
    with open(target, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)"
          % (target, os.path.getsize(target), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
