#!/usr/bin/env python3
"""Carrier for THE CAPITAL WIRE entry (news-image-20261124).

Reads entry.png from this file's own directory, verifies the bounty
gate (PNG, 1024x1024, at most 1 MiB), and writes the image bytes
exactly to stdout. Standard library only.
"""
import os
import struct
import sys

MAX_BYTES = 1024 * 1024
EXPECTED_W = 1024
EXPECTED_H = 1024


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        sys.stderr.write("entry.png exceeds 1 MiB gate\n")
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.stderr.write("entry.png is not a PNG\n")
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        sys.stderr.write("entry.png is not 1024x1024\n")
        return 1
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
