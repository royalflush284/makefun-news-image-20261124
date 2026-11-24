#!/usr/bin/env python3
"""THE TELEGRAPH ROOM - NI24 entry program (Final 1, build v2).

Copies the finished front page (entry.png, drawn in-session by compose.py)
to the grader output directory. Standard library only, no network, no
environment secrets. Refuses to emit an image that is not exactly
1024x1024 PNG or is over 1 MiB, so a bad build fails loudly here instead
of at the server gate.
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1048576
WANT_W, WANT_H = 1024, 1024


def read_png_size(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    if data[-12:] != struct.pack(">I", 0) + b"IEND" + b"\xaeB`\x82":
        raise SystemExit("entry.png is truncated: missing IEND trailer")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    width, height = read_png_size(data)
    if (width, height) != (WANT_W, WANT_H):
        raise SystemExit("entry.png must be 1024x1024, got %dx%d" % (width, height))
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, "entry.png")
    with open(dest, "wb") as f:
        f.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (dest, len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
