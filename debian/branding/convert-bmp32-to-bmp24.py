#!/usr/bin/env python3
"""Convert a top-down BGRA BMP with BITFIELDS masks to an uncompressed BGR BMP."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    data = args.source.read_bytes()
    signature, declared_size, _, _, pixel_offset = struct.unpack_from("<2sIHHI", data, 0)
    dib_size, width, height, planes, bpp, compression, image_size = struct.unpack_from("<IiiHHII", data, 14)
    if signature != b"BM" or declared_size != len(data):
        raise ValueError("source is not a complete BMP")
    if (dib_size, planes, bpp, compression) != (124, 1, 32, 3):
        raise ValueError("source must be a 32-bit BITMAPV5/BI_BITFIELDS BMP")
    if height >= 0:
        raise ValueError("source must be top-down")
    height = -height
    if image_size != width * height * 4:
        raise ValueError("unexpected source pixel size")

    row_size = (width * 3 + 3) & ~3
    pixels = bytearray(row_size * height)
    for row in range(height):
        src = pixel_offset + row * width * 4
        dst = row * row_size
        for column in range(width):
            # Input masks are B=0x000000ff, G=0x0000ff00, R=0x00ff0000.
            b, g, r, _alpha = data[src + column * 4 : src + column * 4 + 4]
            pixels[dst + column * 3 : dst + column * 3 + 3] = bytes((b, g, r))

    file_size = 14 + 40 + len(pixels)
    header = struct.pack(
        "<2sIHHI", b"BM", file_size, 0, 0, 54
    ) + struct.pack(
        "<IiiHHIIiiII", 40, width, -height, 1, 24, 0, len(pixels), 0, 0, 0, 0
    )
    args.output.write_bytes(header + pixels)


if __name__ == "__main__":
    main()
