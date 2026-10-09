# Offline archive adapter

`tools/bgfa_archive.py` is a development library for BGFA 1.05 archives. It has no filesystem, network or emulator side effects and is not an installer. It accepts bytes and returns candidate bytes; no game files are distributed with it.

The stock archive builders used fixed positions and widths. The pinned CFBR v21 BOOT and MISC archives instead use four-byte offset, packed-size and size-difference fields with unshifted offsets. The nested GAMEMODE archive also differs: its compressed payload begins at byte 121, not stock byte 120. Its decoded template ends exactly at its declared database size; it has none of the stock template's 4,200 trailing bytes. Carrying those stock assumptions into the CFBR builder would corrupt framing or reject valid inputs.

The adapter reads these widths, offset shifts, flag width, key width and name length from each archive header. Replacements retain compression mode, flags, keys and names. New payloads are appended with the declared alignment; original payload storage remains intact. Only selected index offset/size fields change. A no-op replacement is byte-identical. Exact source archive and decoded entry hashes are required. Unsupported field widths, malformed framing, decompression length mismatches and integer overflow are rejected.

Format provenance: the project-local `inspect_bgfa.py` parser cites Luigi Auriemma's `nbajamfire.bms` 0.2.3a. The new adapter is project-authored Python, tested against that existing parser and synthetic fixtures. It contains no decompiled game code.

## Validation recorded October 9, 2026

- Sixteen synthetic tests pass, including the observed stock/CFBR layouts, nested and compressed entries, multi-entry replacement, preservation, wrong identities, truncated data, index overlap, field overflow and invalid zlib framing.
- Across four pinned stock/CFBR BOOT and MISC archives, all 4,840 decoded entries agree with the preexisting independent file parser. Empty rewrites are byte-identical.
- A private CFBR BOOT reserve candidate passes 34 checks. Only the nested Dynasty template and built-in roster entries change; the 825 other entries, original payload storage, prior database row bytes and schemas are retained. Membership remains 141 built-in roster teams, including 126 FBS teams.
- Initial candidate construction rejected a stock-only 4,200-byte trailer assumption. Inspection established zero trailing bytes in the pinned CFBR template, and the input-specific assertion was corrected before candidate creation.
- No candidate was installed. No runtime allocation, fresh-Dynasty, season, team-remapping or playoff acceptance follows from these checks. The automatically loaded bundled roster is a separate input and still needs a coordinated plan.

Run the synthetic tests with Python 3.11 or newer, from the repository root:

```text
python -B -m unittest discover -s tools -p test_bgfa_archive.py -v
```

The private capacity builder depends on reviewed local TDB tooling and user-owned game inputs. It is not part of a portable release. Runtime testing must first establish compatible engine allocations and consumers; increasing serialized capacities does not establish safe active-team expansion.
