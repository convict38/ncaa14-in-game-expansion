"""Offline BGFA 1.05 entry replacement; no filesystem or installation side effects.

Field layout follows the project's inspect_bgfa parser, whose format reference is
Luigi Auriemma's nbajamfire.bms 0.2.3a. This implementation preserves flags, keys,
names, index framing and original payload storage. Only reviewed entries move.
It is a development building block, not a general archive editor or installer.
"""

from dataclasses import dataclass
import hashlib
import struct
import zlib


MAX_DECODED = 512 * 1024 * 1024


def sha256(data):
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Entry:
    index: int
    record_offset: int
    flags: int
    key: bytes
    name: bytes
    offset: int
    packed: int
    extra: int


class Archive:
    def __init__(self, data):
        self.data = bytes(data)
        if len(data) < 64 or data[:8] != b'BGFA1.05':
            raise ValueError('Expected complete BGFA 1.05 header')
        self.count, start = struct.unpack_from('<II', data, 12)
        _, mode, key, off, packed, extra, shift, _ = data[32:40]
        buckets, name = struct.unpack_from('<II', data, 40)
        if mode not in (0, 1) or not 1 <= key <= 32:
            raise ValueError('Unsupported flags or key width')
        if not 1 <= off <= 8 or not 1 <= packed <= 8 or not 0 <= extra <= 8:
            raise ValueError('Unsupported integer width')
        if shift > 16 or name > 4096 or self.count > 1_000_000:
            raise ValueError('Unsupported index limits')
        self.flag_width = 1 if mode == 0 else 2
        self.widths = (off, packed, extra)
        self.shift = shift
        self.pointer_delta = self.flag_width + key
        self.record_size = self.pointer_delta + off + packed + extra + name
        self.index_start = start + buckets * 4
        self.index_end = self.index_start + self.count * self.record_size
        if start < 64 or self.index_end > len(data):
            raise ValueError('Index outside archive')
        self.entries = []
        for i in range(self.count):
            rec = self.index_start + i * self.record_size
            cursor = rec
            flags = int.from_bytes(data[cursor:cursor + self.flag_width], 'little')
            cursor += self.flag_width
            identity = bytes(data[cursor:cursor + key])
            cursor += key
            values = []
            for width in self.widths:
                values.append(int.from_bytes(data[cursor:cursor + width], 'little'))
                cursor += width
            offset, length, growth = values
            offset <<= shift
            if offset > len(data) or offset + length > len(data):
                raise ValueError(f'Entry {i} outside archive')
            if length and offset < self.index_end:
                raise ValueError(f'Entry {i} overlaps index')
            self.entries.append(Entry(i, rec, flags, identity,
                                      bytes(data[cursor:cursor + name]),
                                      offset, length, growth))

    def packed_payload(self, index):
        if type(index) is not int or not 0 <= index < self.count:
            raise ValueError('Invalid entry index')
        e = self.entries[index]
        return self.data[e.offset:e.offset + e.packed]

    def decode(self, index, *, max_decoded=MAX_DECODED):
        packed = self.packed_payload(index)
        e = self.entries[index]
        expected = e.packed + e.extra
        if expected > max_decoded:
            raise ValueError('Decoded entry exceeds configured limit')
        if not e.extra:
            return packed
        try:
            decoder = zlib.decompressobj()
            result = decoder.decompress(packed, expected + 1)
        except zlib.error as error:
            raise ValueError('Invalid compressed entry') from error
        if (len(result) != expected or not decoder.eof or
                decoder.unused_data or decoder.unconsumed_tail):
            raise ValueError('Compressed entry length or framing mismatch')
        return result


def replace_entries(data, replacements, *, expected_sha256, expected_entries):
    """Return an append-only candidate from decoded replacement byte strings.

Require the exact archive hash and decoded preimage hash for each entry.
Compression mode is retained; compression whose size cannot fit the original
representation is rejected. Empty replacement sets return the exact input.
No source file, destination file, game data or emulator state is written here.
"""
    if sha256(data) != expected_sha256:
        raise ValueError('Archive identity mismatch')
    if set(replacements) != set(expected_entries):
        raise ValueError('Every replacement requires an entry preimage')
    archive = Archive(data)
    candidate = bytearray(data)
    for index in sorted(replacements):
        original = archive.decode(index)
        if sha256(original) != expected_entries[index]:
            raise ValueError(f'Entry {index} identity mismatch')
        replacement = replacements[index]
        if not isinstance(replacement, bytes) or len(replacement) > MAX_DECODED:
            raise ValueError('Replacement must be bounded bytes')
        if replacement == original:
            continue
        e = archive.entries[index]
        payload = zlib.compress(replacement, 9) if e.extra else replacement
        extra = len(replacement) - len(payload) if e.extra else 0
        if e.extra and extra <= 0:
            raise ValueError('Cannot retain compressed representation')
        alignment = 1 << archive.shift
        offset = (len(candidate) + alignment - 1) & ~(alignment - 1)
        values = (offset >> archive.shift, len(payload), extra)
        encoded = []
        for value, width in zip(values, archive.widths):
            if value < 0 or value >= 1 << (8 * width):
                raise ValueError('Replacement exceeds original index field width')
            encoded.append(value.to_bytes(width, 'little'))
        field = e.record_offset + archive.pointer_delta
        fields = b''.join(encoded)
        candidate[field:field + len(fields)] = fields
        candidate.extend(bytes(offset - len(candidate)))
        candidate.extend(payload)
    result = bytes(candidate)
    after = Archive(result)
    for index, replacement in replacements.items():
        if after.decode(index) != replacement:
            raise ValueError('Candidate round-trip failed')
    return result
