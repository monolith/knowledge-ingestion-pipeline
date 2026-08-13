"""CCITT Group 3/4 fax decoding, and a minimal PNG writer.

Scanned PDFs carry their pages as CCITT-encoded bilevel images with no text
layer at all, so every text extractor -- Docling, the lightweight parsers, a
plain byte scan -- returns nothing from them. That is not a rare case: it is
most pre-2000 journal archives, most scanned institutional records, and it was
the case for the first real paper this pipeline was pointed at.

There is no dependency here on purpose. Pillow would do this in one call, but
adding an image library to a text pipeline for one codec is a poor trade, and
this host has neither Pillow nor poppler. The decoder is ITU-T T.4/T.6, which
has been frozen since 1988 and is about two hundred lines including its code
tables.

Decoding gets you pixels, not words. What turns pixels into text is a vision
model, which under the handoff runtime is the agent already running the CLI --
so `pdf_page_images` writes PNGs and the caller hands them to whoever can read.
"""

from __future__ import annotations

import re
import struct
import zlib
from pathlib import Path
from typing import Any, Iterator

# --- T.4 run-length code tables -----------------------------------------------
# Terminating codes cover runs of 0-63; makeup codes cover multiples of 64 and
# are followed by a terminating code. Transcribed from ITU-T T.4 tables 2, 3
# and 4; the extended makeup codes in table 4 are shared by both colours.

WHITE_TERM = {
    "00110101": 0, "000111": 1, "0111": 2, "1000": 3, "1011": 4, "1100": 5,
    "1110": 6, "1111": 7, "10011": 8, "10100": 9, "00111": 10, "01000": 11,
    "001000": 12, "000011": 13, "110100": 14, "110101": 15, "101010": 16,
    "101011": 17, "0100111": 18, "0001100": 19, "0001000": 20, "0010111": 21,
    "0000011": 22, "0000100": 23, "0101000": 24, "0101011": 25, "0010011": 26,
    "0100100": 27, "0011000": 28, "00000010": 29, "00000011": 30, "00011010": 31,
    "00011011": 32, "00010010": 33, "00010011": 34, "00010100": 35, "00010101": 36,
    "00010110": 37, "00010111": 38, "00101000": 39, "00101001": 40, "00101010": 41,
    "00101011": 42, "00101100": 43, "00101101": 44, "00000100": 45, "00000101": 46,
    "00001010": 47, "00001011": 48, "01010010": 49, "01010011": 50, "01010100": 51,
    "01010101": 52, "00100100": 53, "00100101": 54, "01011000": 55, "01011001": 56,
    "01011010": 57, "01011011": 58, "01001010": 59, "01001011": 60, "00110010": 61,
    "00110011": 62, "00110100": 63,
}
WHITE_MAKEUP = {
    "11011": 64, "10010": 128, "010111": 192, "0110111": 256, "00110110": 320,
    "00110111": 384, "01100100": 448, "01100101": 512, "01101000": 576,
    "01100111": 640, "011001100": 704, "011001101": 768, "011010010": 832,
    "011010011": 896, "011010100": 960, "011010101": 1024, "011010110": 1088,
    "011010111": 1152, "011011000": 1216, "011011001": 1280, "011011010": 1344,
    "011011011": 1408, "010011000": 1472, "010011001": 1536, "010011010": 1600,
    "011000": 1664, "010011011": 1728,
}
BLACK_TERM = {
    "0000110111": 0, "010": 1, "11": 2, "10": 3, "011": 4, "0011": 5, "0010": 6,
    "00011": 7, "000101": 8, "000100": 9, "0000100": 10, "0000101": 11,
    "0000111": 12, "00000100": 13, "00000111": 14, "000011000": 15,
    "0000010111": 16, "0000011000": 17, "0000001000": 18, "00001100111": 19,
    "00001101000": 20, "00001101100": 21, "00000110111": 22, "00000101000": 23,
    "00000010111": 24, "00000011000": 25, "000011001010": 26, "000011001011": 27,
    "000011001100": 28, "000011001101": 29, "000001101000": 30, "000001101001": 31,
    "000001101010": 32, "000001101011": 33, "000011010010": 34, "000011010011": 35,
    "000011010100": 36, "000011010101": 37, "000011010110": 38, "000011010111": 39,
    "000001101100": 40, "000001101101": 41, "000011011010": 42, "000011011011": 43,
    "000001010100": 44, "000001010101": 45, "000001010110": 46, "000001010111": 47,
    "000001100100": 48, "000001100101": 49, "000001010010": 50, "000001010011": 51,
    "000000100100": 52, "000000110111": 53, "000000111000": 54, "000000100111": 55,
    "000000101000": 56, "000001011000": 57, "000001011001": 58, "000000101011": 59,
    "000000101100": 60, "000001011010": 61, "000001100110": 62, "000001100111": 63,
}
BLACK_MAKEUP = {
    "0000001111": 64, "000011001000": 128, "000011001001": 192,
    "000001011011": 256, "000000110011": 320, "000000110100": 384,
    "000000110101": 448, "0000001101100": 512, "0000001101101": 576,
    "0000001001010": 640, "0000001001011": 704, "0000001001100": 768,
    "0000001001101": 832, "0000001110010": 896, "0000001110011": 960,
    "0000001110100": 1024, "0000001110101": 1088, "0000001110110": 1152,
    "0000001110111": 1216, "0000001010010": 1280, "0000001010011": 1344,
    "0000001010100": 1408, "0000001010101": 1472, "0000001011010": 1536,
    "0000001011011": 1600, "0000001100100": 1664, "0000001100101": 1728,
}
SHARED_MAKEUP = {
    "00000001000": 1792, "00000001100": 1856, "00000001101": 1920,
    "000000010010": 1984, "000000010011": 2048, "000000010100": 2112,
    "000000010101": 2176, "000000010110": 2240, "000000010111": 2304,
    "000000011100": 2368, "000000011101": 2432, "000000011110": 2496,
    "000000011111": 2560,
}

WHITE = {**WHITE_TERM, **WHITE_MAKEUP, **SHARED_MAKEUP}
BLACK = {**BLACK_TERM, **BLACK_MAKEUP, **SHARED_MAKEUP}
WHITE_TERMINATES = set(WHITE_TERM.values())
BLACK_TERMINATES = set(BLACK_TERM.values())


class CCITTError(Exception):
    """The bitstream did not decode. Almost always a truncated stream."""


class _Bits:
    """Bit reader over a byte string, MSB first."""

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0
        self.end = len(data) * 8

    def peek(self, n: int) -> str:
        out = []
        for i in range(self.pos, min(self.pos + n, self.end)):
            out.append("1" if self.data[i >> 3] & (0x80 >> (i & 7)) else "0")
        return "".join(out)

    def take(self, n: int) -> None:
        self.pos += n

    @property
    def exhausted(self) -> bool:
        return self.pos >= self.end


def _read_run(bits: _Bits, white: bool) -> int:
    """One full run: makeup codes accumulate until a terminating code."""
    table = WHITE if white else BLACK
    terminates = WHITE_TERMINATES if white else BLACK_TERMINATES
    total = 0
    while True:
        # Codes are 2-14 bits. Longest match is unnecessary: the tables are
        # prefix-free, so the first match at increasing length is the code.
        for length in range(2, 15):
            chunk = bits.peek(length)
            if len(chunk) < length:
                raise CCITTError("stream ended mid-code")
            if chunk in table:
                bits.take(length)
                run = table[chunk]
                total += run
                if run in terminates and run < 64:
                    return total
                break
        else:
            raise CCITTError(f"no code matches {bits.peek(14)!r} at bit {bits.pos}")


def decode_g4(data: bytes, columns: int, rows: int) -> list[bytearray]:
    """Decode a Group 4 (T.6) stream into `rows` rows of 0/1 bytes, 1 = black.

    Two-dimensional coding throughout: each line is expressed as changes
    relative to the line above it, which is why a fax of mostly-repeating text
    lines compresses so well and why there is no way to decode line N without
    having decoded line N-1.
    """
    bits = _Bits(data)
    # The imaginary line above the first is all white.
    reference = [columns, columns]
    out: list[bytearray] = []

    for _ in range(rows):
        if bits.exhausted:
            break
        current: list[int] = []
        a0 = -1
        colour = 0  # 0 = white, 1 = black

        while a0 < columns:
            # b1: first changing element on the reference line to the right of
            # a0 and of opposite colour to a0's colour run.
            b1 = columns
            for index, change in enumerate(reference):
                if change > a0 and (index % 2) == colour:
                    b1 = change
                    break
            b2 = columns
            for change in reference:
                if change > b1:
                    b2 = change
                    break

            mode = bits.peek(7)
            if not mode:
                break

            if mode.startswith("0001"):            # pass
                bits.take(4)
                a0 = b2
            elif mode.startswith("001"):           # horizontal
                bits.take(3)
                run1 = _read_run(bits, white=(colour == 0))
                run2 = _read_run(bits, white=(colour != 0))
                start = a0 if a0 > 0 else 0
                a1 = min(start + run1, columns)
                a2 = min(a1 + run2, columns)
                current.extend([a1, a2])
                a0 = a2
            else:                                   # vertical
                for code, delta in (("1", 0), ("011", 1), ("010", -1),
                                    ("000011", 2), ("000010", -2),
                                    ("0000011", 3), ("0000010", -3)):
                    if mode.startswith(code):
                        bits.take(len(code))
                        a1 = max(0, min(b1 + delta, columns))
                        current.append(a1)
                        a0 = a1
                        colour ^= 1
                        break
                else:
                    # EOFB or padding: stop cleanly rather than guessing.
                    a0 = columns
                    break

        row = bytearray(columns)
        pos, value = 0, 0
        for change in current:
            if change > pos and value:
                for i in range(pos, min(change, columns)):
                    row[i] = 1
            pos = max(pos, min(change, columns))
            value ^= 1
        if value and pos < columns:
            for i in range(pos, columns):
                row[i] = 1
        out.append(row)

        reference = current + [columns, columns]

    return out


def _png_bytes(width: int, height: int, raw: bytes, colour_type: int) -> bytes:
    """PNG framing, shared by the bilevel and truecolour writers."""
    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (struct.pack(">I", len(payload)) + tag + payload
                + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

    depth = 1 if colour_type == 0 else 8
    header = struct.pack(">IIBBBBB", width, height, depth, colour_type, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + chunk(b"IEND", b""))


def write_png_rgb(width: int, height: int, pixels: bytes, path: Path, *,
                  channels: int = 4, bgr: bool = True, stride: int | None = None) -> Path:
    """Write an 8-bit truecolour PNG from a raw framebuffer.

    The bilevel writer below exists for decoded fax pages. This one exists for
    rendered PDF pages, which arrive as BGRA from PDFium. Same framing, colour
    type 2 instead of 0, and no bit packing.

    Still no image dependency: Pillow would do this in one call and would also
    be the only reason this pipeline needed it.
    """
    row_bytes = bytearray()
    # A renderer's rows are padded to an alignment boundary, so the distance
    # between rows is not width*channels and assuming it is walks off the end.
    stride = stride or width * channels
    for y in range(height):
        row_bytes.append(0)  # filter type: none
        start = y * stride
        row = pixels[start:start + width * channels]
        if bgr:
            # PDFium hands back BGR (or BGRA). Reorder to RGB and drop any alpha.
            for x in range(0, width * channels, channels):
                b, g, r = row[x], row[x + 1], row[x + 2]
                row_bytes.extend((r, g, b))
        elif channels == 4:
            for x in range(0, width * 4, 4):
                row_bytes.extend(row[x:x + 3])
        else:
            row_bytes.extend(row)
    path.write_bytes(_png_bytes(width, height, bytes(row_bytes), 2))
    return path


def write_png(rows: list[bytearray], path: Path) -> Path:
    """Write a 1-bit greyscale PNG. zlib is stdlib; PNG framing is a dozen lines."""
    height, width = len(rows), (len(rows[0]) if rows else 0)
    raw = bytearray()
    for row in rows:
        raw.append(0)  # filter type: none
        packed = bytearray((width + 7) // 8)
        for x, black in enumerate(row):
            if not black:  # 1 = white in this bit depth
                packed[x >> 3] |= 0x80 >> (x & 7)
        raw.extend(packed)

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (struct.pack(">I", len(payload)) + tag + payload
                + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 1, 0, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
           + chunk(b"IEND", b""))
    Path(path).write_bytes(png)
    return Path(path)


def scanned_pdf_pages(pdf: Path) -> Iterator[dict[str, Any]]:
    """Yield each CCITT-encoded page image found in a PDF, in document order."""
    data = Path(pdf).read_bytes()
    pattern = re.compile(rb"<<(.{0,600}?/Filter\s*/CCITTFaxDecode.{0,600}?)>>\s*stream\r?\n", re.S)
    for index, match in enumerate(pattern.finditer(data)):
        header = match.group(1)
        start = match.end()
        end = data.find(b"endstream", start)

        def field(name: str, default: int | None = None) -> int | None:
            found = re.search((r"/%s\s+(-?\d+)" % name).encode(), header)
            return int(found.group(1)) if found else default

        yield {
            "index": index,
            "columns": field("Columns", field("Width")) or 1728,
            "rows": field("Rows", field("Height")) or 0,
            "k": field("K", 0),
            "black_is_1": b"/BlackIs1 true" in header,
            "data": data[start:end].rstrip(b"\r\n"),
        }


def pdf_page_images(pdf: Path, out_dir: Path, *, scale: int = 3) -> list[Path]:
    """Decode a scanned PDF's pages to PNGs and return their paths.

    `scale` downsamples by an integer factor. A 4160x6296 fax page is far larger
    than a vision model needs and costs proportionally; a third of that is still
    comfortably legible for body text.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for page in scanned_pdf_pages(pdf):
        rows = decode_g4(page["data"], page["columns"], page["rows"])
        if not rows:
            continue
        if not page["black_is_1"]:
            pass  # decode_g4 already returns 1 = black
        if scale > 1:
            rows = [bytearray(
                        1 if any(rows[y][x:x + scale]) else 0
                        for x in range(0, len(rows[y]), scale))
                    for y in range(0, len(rows), scale)]
        written.append(write_png(rows, out_dir / f"page-{page['index'] + 1:03d}.png"))
    return written
