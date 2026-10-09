# College Football Revamped compatibility

Status: investigated and staged privately; not integrated or runtime-tested. This project is independent of the CFBR team. The latest validated expansion remains the stock-build v6 trial at 127 active FBS teams.

## Upstream and intended scope

We reviewed the official [CFBR Easy Installer repository](https://github.com/cfbrevamped/CFBR-Easy-Installer/tree/9b9674a0de6102cec90ea64c2cf155ecf4752437). Its published PC/PS3 release is v21, dated September 6, 2023. We selected the [PC disc package with PS3 buttons and the older scorebug](https://github.com/cfbrevamped/CFBR-Easy-Installer/blob/9b9674a0de6102cec90ea64c2cf155ecf4752437/PC/disc/ps3-buttons.md) as the first compatibility target.

CFBR's [patch notes](https://github.com/cfbrevamped/CFBR-Easy-Installer/blob/9b9674a0de6102cec90ea64c2cf155ecf4752437/assets/release-notes/PC-PS3.md) describe uniforms, fields, logos, lighting, player models, stadium updates, playbook additions and gameplay changes. We intend to support these alongside expanded membership. Graphics, gameplay and database changes each need integration tests.

Their [Dynasty Tool v2](https://github.com/Bowersrd/NCAA14DynastyToolRelease/releases/tag/v2.0.0) provides a 12-team playoff through external save-processing steps and swaps teams into existing slots. Our requested deliverable still needs automatic in-game rounds and additional active teams.

## Measured package findings

The locally staged official linked package is 7,823,052,432 bytes and contains 2,452 entries: 2,421 files and 31 directories. SHA-256:

`837afea6338d4796251e6f70ad3fa296bb429204e9ccc2fd69803a996ce22065`

This records our download identity; no publisher-provided checksum was available for comparison. We extracted selected files into a private flat staging directory. Nothing was installed.

- The included update metadata says BLUS31159, APP_VER 01.02. Its decrypted executable SHA-256 is `144dee9040da9cb1e8337844fbb685a0f06e560b8fee8d9ba1eac87b9e300c1c`.
- None of the current 517 expansion preimages match at their existing addresses in this executable. Existing patches are incompatible; a separate analysis and port are required. A separate Ghidra project now imports this exact ELF with PowerPC big-endian decoding, a 32-bit pointer model, verified entry/TOC and successful entry-function decompilation. This is static workflow validation, not a runtime test.
- BOOT and MISC retain the same indexed key order, but 22 BOOT and 331 MISC decoded entry payloads differ from our original archives. Their archive index field widths also differ. Whole-file replacement or blindly running the stock archive builder would discard changes or damage framing.
- Both the built-in and bundled 2023 rosters still contain 126 FBS entries. Updated appearances do not establish expanded active membership.

The bundled 2023 roster confirms these occupied-ID conflicts:

| Original school retained by our project | TGID | CFBR school using that ID |
| --- | ---: | --- |
| Idaho | 34 | Appalachian State |
| New Mexico State | 61 | Coastal Carolina |
| Connecticut | 100 | Charlotte |
| UMass | 181 | Georgia Southern |
| FIU | 230 | James Madison |

CFBR's built-in roster has `FIUtest` at 230, while its bundled 2023 roster has James Madison. Loading different roster sources therefore changes identity. New destination IDs are not assigned yet.

## Integration gates

1. Analyze the separately identified 1.02 executable and port each storage/count patch with verified preimages and consumers. Preserve the tested stock target.
2. Merge archive entries and database rows with format-aware tools. Preserve all original teams; remap added schools, assets, uniforms, stadiums, logos and roster associations to distinct IDs.
3. Validate both original and added schools on the field, with correct home/away uniforms, venues and presentation. Test playbooks and gameplay changes separately.
4. Repeat fresh Dynasty, recruiting, stats/history, save/load and multiple season rollovers on the combined build. Then validate every playoff round and championship recording.
5. Publish an installer that requires a supported user-owned dump and an identified CFBR package. Keep third-party files with their upstream distribution; publish our reviewed adapter and instructions with attribution and applicable permissions settled.

No CFBR assets, executable, roster saves or decompiled code are included in this repository. No combined installable release exists yet.

## Port progress: static checks only

Full Ghidra analysis of the identified 1.02 executable completed. Signature comparison found 443 candidate locations for the 517 source patch words: 441 decoded instructions and two data constants. Of those candidates, 416 preimages match and 27 differ; 74 source sites remain unresolved. Function and data-reference review is still required before accepting any mapping.

A four-word ranking-storage recipe passed 17 offline checks. It pairs a larger caller stack frame with the array capacity pointer for 160 records, while leaving active membership unchanged. It is not installed or runtime-tested, and no executable or installable patch was emitted.

All 2,421 package files have now been extracted into private staging and hashed. Five selected files match between independent Python and Java readers. No CFBR files are published here. A separate runtime baseline with protected saves remains the next integration gate.

We currently track the pinned upstream distribution as a dependency of this repository. Forking the installer repository can help maintain installer changes later, but Git merging cannot reconcile compiled executables, archive contents or conflicting team IDs. The intended installer will combine identified local inputs using our reviewed compatibility recipes.
