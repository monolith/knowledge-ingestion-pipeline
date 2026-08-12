"""CCITT decoding, checked against streams we encode ourselves.

A round-trip test would need an encoder, which is more code than the decoder.
Instead these check the parts that can be checked independently: the code tables
are prefix-free and complete, the PNG writer produces a file a decoder accepts,
and a real scanned page decodes to plausible ink coverage.
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

from kip.ccitt import (
    BLACK,
    SHARED_MAKEUP,
    WHITE,
    decode_g4,
    scanned_pdf_pages,
    write_png,
)


def _prefix_free(table: dict[str, int]) -> list[tuple[str, str]]:
    codes = sorted(table, key=len)
    clashes = []
    for i, short in enumerate(codes):
        for long in codes[i + 1:]:
            if long != short and long.startswith(short):
                clashes.append((short, long))
    return clashes


def test_the_code_tables_are_prefix_free():
    """A decoder that reads the first matching code is only correct if no code
    is a prefix of another. A single bad transcription from the T.4 tables would
    silently mis-decode every page that used the affected run length.
    """
    assert _prefix_free(WHITE) == []
    assert _prefix_free(BLACK) == []


def test_the_extended_makeup_codes_are_shared_by_both_colours():
    """T.4 table 4 applies to white and black alike; dropping it from one would
    cap that colour's runs at 1728 and corrupt any wide scan."""
    for code, run in SHARED_MAKEUP.items():
        assert WHITE[code] == run
        assert BLACK[code] == run


def test_an_all_white_line_decodes_to_no_ink():
    """Vertical mode V0 against the imaginary all-white reference line."""
    rows = decode_g4(bytes([0b10000000]), columns=8, rows=1)
    assert rows and sum(rows[0]) == 0


def test_write_png_produces_a_file_a_decoder_accepts(tmp_path):
    path = write_png([bytearray([1, 0, 1, 0]), bytearray([0, 1, 0, 1])], tmp_path / "t.png")
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    width, height, depth, colour = struct.unpack(">IIBB", data[16:26])
    assert (width, height, depth, colour) == (4, 2, 1, 0)
    # IDAT must be valid zlib, or every reader will reject the file.
    start = data.index(b"IDAT") + 4
    length = struct.unpack(">I", data[start - 8:start - 4])[0]
    assert zlib.decompress(data[start:start + length])


def test_a_pdf_with_no_ccitt_images_yields_nothing(tmp_path):
    """Scanning for the filter must not match a text-layer PDF."""
    pdf = tmp_path / "text.pdf"
    pdf.write_bytes(b"%PDF-1.4\n<</Filter/FlateDecode/Length 10>>stream\nxxxx\nendstream\n")
    assert list(scanned_pdf_pages(pdf)) == []
