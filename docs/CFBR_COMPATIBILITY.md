# College Football Revamped compatibility

An [offline archive adapter](ARCHIVE_ADAPTER.md) now handles the differing index layouts and preserves CFBR content in a serialized-reserve candidate. Its 34 offline checks pass; membership remains 126 FBS and the candidate has not been installed. The engine port and bundled-roster coordination remain separate prerequisites.

Status: isolated unmodified CFBR season/rollover passed; the first four-word patch passed a bounded install/load/rollback test. Expansion integration remains unfinished. This project is independent of the CFBR team. The latest validated expansion remains the stock-build v6 trial at 127 active FBS teams.

## Upstream and intended scope

We reviewed the official [CFBR Easy Installer repository](https://github.com/cfbrevamped/CFBR-Easy-Installer/tree/9b9674a0de6102cec90ea64c2cf155ecf4752437). Its published PC/PS3 release is v21, dated September 6, 2023. We selected the [PC disc package with PS3 buttons and the older scorebug](https://github.com/cfbrevamped/CFBR-Easy-Installer/blob/9b9674a0de6102cec90ea64c2cf155ecf4752437/PC/disc/ps3-buttons.md) as the first compatibility target.

CFBR's [patch notes](https://github.com/cfbrevamped/CFBR-Easy-Installer/blob/9b9674a0de6102cec90ea64c2cf155ecf4752437/assets/release-notes/PC-PS3.md) describe uniforms, fields, logos, lighting, player models, stadium updates, playbook additions and gameplay changes. We intend to support these alongside expanded membership. Graphics, gameplay and database changes each need integration tests.

Their [Dynasty Tool v2](https://github.com/Bowersrd/NCAA14DynastyToolRelease/releases/tag/v2.0.0) provides a 12-team playoff through external save-processing steps and swaps teams into existing slots. Our requested deliverable still needs automatic in-game rounds and additional active teams.

## Measured package findings

The locally staged official linked package is 7,823,052,432 bytes and contains 2,452 entries: 2,421 files and 31 directories. SHA-256:

`837afea6338d4796251e6f70ad3fa296bb429204e9ccc2fd69803a996ce22065`

This records our download identity; no publisher-provided checksum was available for comparison. Package files were extracted into private staging and assembled into an isolated development profile for the baseline described below.

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

A four-word ranking-storage recipe passed 17 offline checks. It pairs a larger caller stack frame with the array capacity pointer for 160 records, while leaving active membership unchanged. The initial recipe emitted no installable patch. A later guarded development patch and its bounded runtime test are recorded below.

All 2,421 package files have now been extracted into private staging and hashed. Five selected files match between independent Python and Java readers. No CFBR files are published here. The separate runtime baseline and first bounded patch test are recorded below.

We currently track the pinned upstream distribution as a dependency of this repository. Forking the installer repository can help maintain installer changes later, but Git merging cannot reconcile compiled executables, archive contents or conflicting team IDs. The intended installer will combine identified local inputs using our reviewed compatibility recipes.

## Isolated runtime baseline - 2026-10-09

An unmodified CFBR v21/update 1.02 baseline now boots in a separate development profile. The emulator's loaded ELF matches the analyzed ELF byte for byte. Six live memory comparisons passed in each of two runs, including the entry, OPD/TOC and proposed ranking-patch sites. The observed PPU key is `PPU-62e25ebc1957382b34f2778554943e40d6d84e3c`.

Normal gameplay created a fresh Alabama Dynasty. Fifteen structural checks passed: 126 FBS teams, complete 12-game regular schedules without weekly collisions, valid roster/depth references and recruiting initialization. A separate emulator run loaded the save normally; all four save files remained byte-identical. This establishes a fresh-save baseline, not full-season or expansion compatibility.

The game automatically loaded the bundled CFBR23V21 roster. An initial check expecting the built-in roster failed on team 230: the save contains James Madison, while the built-in roster says FIUtest. The auto-load log identifies the actual roster source; the corrected check passes. Future installers and tests must pin roster input as well as archives and executable.

After the test, the development profile redirect was rolled back. All 48 protected stock working-save files were unchanged; original preservation passed 58 checks. No expanded membership was enabled. The subsequent ranking-patch test is recorded below; the combined mod still needs remapping, expanded season progression and playoff implementation.

## Season control and first reversible patch - 2026-10-09

The unmodified CFBR control completed normal 2013 simulation and rollover into 2014. Regular-season and postseason snapshots each passed 28 checks. All 126 FBS teams completed 12 regular games, and every saved team record agreed with completed scores. Alabama finished 11-3 and won the Gator Bowl. Saved national-title metadata changed for Ohio State.

Rollover passed 30 checks: all 131 saved team identities and 126 FBS teams remained; each FBS team received 12 next-year regular games without weekly collisions; player/depth and stadium links were valid; checked bowl/conference histories and national-title metadata persisted. Ten Alabama recruits matched the next-year roster on eight identity fields.

A guarded four-word ranking-storage patch was then installed, observed in the emulator log and verified in live memory. The 2014 save loaded normally and its career-statistics screen opened. After removing the patch, another cold load and live probe confirmed restored instructions. All four save files stayed byte-identical through both cold runs. The original patch configuration and profile redirects were restored; 48 protected stock save files and the 58 original-preservation checks passed.

This patch test establishes installation, live-byte and cold-load compatibility only. It does not yet establish execution coverage of the ranking producer, a patched full season, or expanded active membership. Those tests remain required before combining it with the wider port. The unpatched full-season result must not be reported as a patched-season result.

One checker initially expected stored week 15 at the conference-championship screen; the save stores 16. That failed report was preserved and the corrected expectation passed. No game crash or manual save edit occurred.

## Execution tracing limitation - 2026-10-09

A requested breakpoint was acknowledged but never hit under LLVM. Matching RPCS3 source explicitly rejects LLVM PPU breakpoints; the GDB command handler does not propagate that failure. A successful protocol reply therefore does not prove breakpoint installation. See [PPU breakpoint implementation](https://github.com/RPCS3/rpcs3/blob/304d544b/rpcs3/Emu/Cell/PPUThread.cpp#L1155) and [GDB handler](https://github.com/RPCS3/rpcs3/blob/304d544b/rpcs3/Emu/GDB.cpp).

A separate Interpreter (static) configuration allowed normal save loading and viewing Championship Contenders but did not obtain the requested execution stops. A subsequent early-attach attempt stayed at the title/attract screens. Normal shutdown with a pending debugger continue hung; the emulator's termination and fatal-error dialogs were handled. These diagnostic failures are retained in the private evidence. No positive breakpoint coverage, patched full season or expanded CFBR membership is claimed.

The four-word experiment and profile redirect were rolled back. All four working Dynasty save files match before and after the interpreter experiments; 48 protected stock save files are unchanged and 58 original-preservation checks passed. The Dynasty had advanced normally to Week 1 of 2014 before those experiments. Next work prioritizes the LLVM patched-season regression; debugger compatibility will not block independent port work. A minimal positive-control trace or reversible execution marker needs separate validation.
