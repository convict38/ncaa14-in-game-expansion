"""Synthetic format/negative tests; contains no game files or assets."""
import struct
import unittest
import zlib

from bgfa_archive import Archive, replace_entries, sha256


def fixture(*, widths=(3, 3, 0), shift=4, mode=1, compressed=False, name=b''):
    payloads = (b'A' * 1024, b'untouched second payload')
    flags = 1 if mode == 0 else 2
    recsize = flags + 8 + sum(widths) + len(name)
    raw = bytearray(68 + 2 * recsize)
    raw[:8] = b'BGFA1.05'
    struct.pack_into('<6I', raw, 8, 2, 2, 64, 0, 4 + 2 * recsize, 0)
    raw[32:40] = bytes((0, mode, 8, *widths, shift, 0))
    struct.pack_into('<II', raw, 40, 1, len(name))
    for i, decoded in enumerate(payloads):
        payload = zlib.compress(decoded) if compressed and i == 0 else decoded
        alignment = 1 << shift
        offset = (len(raw) + alignment - 1) & ~(alignment - 1)
        record = (0x10).to_bytes(flags, 'little') + bytes([i + 1]) * 8
        values = (offset >> shift, len(payload), len(decoded) - len(payload))
        record += b''.join(v.to_bytes(w, 'little') for v, w in zip(values, widths))
        record += name
        pos = 68 + i * recsize
        raw[pos:pos + recsize] = record
        raw.extend(bytes(offset - len(raw)))
        raw.extend(payload)
    return bytes(raw)


class ArchiveTests(unittest.TestCase):
    def replace(self, raw, value):
        return replace_entries(raw, {0: value}, expected_sha256=sha256(raw),
                               expected_entries={0: sha256(Archive(raw).decode(0))})

    def test_observed_layouts_and_preservation(self):
        for widths, shift, mode, name in [((3, 3, 0), 4, 1, b''),
                                         ((4, 3, 0), 2, 1, b''),
                                         ((4, 4, 4), 0, 1, b''),
                                         ((1, 3, 3), 3, 0, b'x' * 32),
                                         ((4, 4, 4), 0, 0, b'x' * 32)]:
            with self.subTest(widths=widths, shift=shift, mode=mode):
                raw = fixture(widths=widths, shift=shift, mode=mode, name=name)
                before = Archive(raw)
                new = self.replace(raw, b'changed' * 37)
                after = Archive(new)
                self.assertEqual(after.decode(0), b'changed' * 37)
                self.assertEqual(after.entries[1], before.entries[1])
                self.assertEqual(after.decode(1), before.decode(1))
                self.assertEqual(new[before.index_end:len(raw)], raw[before.index_end:])
                field = before.entries[0].record_offset + before.pointer_delta
                end = field + sum(before.widths)
                self.assertEqual(new[:field], raw[:field])
                self.assertEqual(new[end:len(raw)], raw[end:])

    def test_noop_is_byte_exact(self):
        raw = fixture()
        self.assertEqual(self.replace(raw, Archive(raw).decode(0)), raw)
        self.assertEqual(replace_entries(raw, {}, expected_sha256=sha256(raw),
                                         expected_entries={}), raw)

    def test_compressed_replacement(self):
        raw = fixture(widths=(4, 4, 4), compressed=True)
        changed = self.replace(raw, b'B' * 4096)
        self.assertEqual(Archive(changed).decode(0), b'B' * 4096)
        self.assertGreater(Archive(changed).entries[0].extra, 0)

    def test_nested_replacement(self):
        inner = fixture(widths=(4, 4, 4), compressed=True, name=b'nested' + bytes(26))
        outer = self.replace(fixture(), inner)
        inner_after = self.replace(inner, b'C' * 2048)
        new = self.replace(outer, inner_after)
        self.assertEqual(Archive(Archive(new).decode(0)).decode(0), b'C' * 2048)

    def test_wrong_archive_identity(self):
        with self.assertRaises(ValueError):
            replace_entries(fixture(), {}, expected_sha256='0' * 64, expected_entries={})

    def test_wrong_or_missing_entry_identity(self):
        raw = fixture()
        for identities in ({}, {0: '0' * 64}):
            with self.assertRaises(ValueError):
                replace_entries(raw, {0: b'x'}, expected_sha256=sha256(raw),
                                expected_entries=identities)

    def test_invalid_indices(self):
        for index in (-1, 2, True, '0'):
            with self.assertRaises(ValueError):
                Archive(fixture()).decode(index)

    def test_truncated_header_and_index(self):
        for raw in (b'', fixture()[:63], fixture()[:90]):
            with self.assertRaises(ValueError):
                Archive(raw)

    def test_payload_out_of_bounds_or_overlapping(self):
        for value in (1, 0xffffff):
            raw = bytearray(fixture())
            raw[78:81] = value.to_bytes(3, 'little')
            with self.assertRaises(ValueError):
                Archive(raw)

    def test_unsupported_header(self):
        for pos, value in ((33, 2), (34, 0), (35, 0), (36, 9), (37, 9), (38, 17)):
            raw = bytearray(fixture())
            raw[pos] = value
            with self.assertRaises(ValueError):
                Archive(raw)

    def test_offset_overflow(self):
        raw = fixture(widths=(1, 3, 3), shift=3, mode=0, name=bytes(32))
        padded = raw + bytes(4096)
        with self.assertRaises(ValueError):
            self.replace(padded, b'x')

    def test_packed_size_overflow(self):
        raw = fixture(widths=(4, 1, 4), compressed=True)
        # Second entry is uncompressed and the stored-size field has one byte.
        with self.assertRaises(ValueError):
            replace_entries(raw, {1: b'x' * 256}, expected_sha256=sha256(raw),
                            expected_entries={1: sha256(Archive(raw).decode(1))})

    def test_compressed_framing_and_declared_size(self):
        raw = fixture(widths=(4, 4, 4), compressed=True)
        a = Archive(raw)
        e = a.entries[0]
        for delta in (-1, 1):
            damaged = bytearray(raw)
            field = e.record_offset + a.pointer_delta + 8
            damaged[field:field + 4] = (e.extra + delta).to_bytes(4, 'little')
            with self.assertRaises(ValueError):
                Archive(damaged).decode(0)
        damaged = bytearray(raw)
        damaged[e.offset] ^= 0xff
        with self.assertRaises(ValueError):
            Archive(damaged).decode(0)
        with self.assertRaises(ValueError):
            a.decode(0, max_decoded=10)

    def test_incompressible_replacement_refused(self):
        with self.assertRaises(ValueError):
            self.replace(fixture(widths=(4, 4, 4), compressed=True), b'x')

    def test_trailing_or_truncated_zlib_rejected(self):
        original = fixture(widths=(4, 4, 4), compressed=True)
        a = Archive(original)
        e = a.entries[0]
        for payload in (a.packed_payload(0) + b'junk', a.packed_payload(0)[:-1]):
            raw = bytearray(original)
            offset = len(raw)
            raw.extend(payload)
            field = e.record_offset + a.pointer_delta
            struct.pack_into('<III', raw, field, offset, len(payload), 1024 - len(payload))
            with self.assertRaises(ValueError):
                Archive(raw).decode(0)

    def test_multiple_replacements_preserve_entry_identity(self):
        raw = fixture(widths=(4, 4, 4), name=b'label')
        a = Archive(raw)
        replacements = {0: b'first changed', 1: b'second changed'}
        new = replace_entries(raw, replacements, expected_sha256=sha256(raw),
                              expected_entries={i: sha256(a.decode(i)) for i in replacements})
        b = Archive(new)
        for i, payload in replacements.items():
            self.assertEqual(b.decode(i), payload)
            self.assertEqual((a.entries[i].flags, a.entries[i].key, a.entries[i].name),
                             (b.entries[i].flags, b.entries[i].key, b.entries[i].name))


if __name__ == '__main__':
    unittest.main()
