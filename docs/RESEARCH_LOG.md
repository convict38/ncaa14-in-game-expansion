# Research log

Evidence is classified as **static**, **runtime-tested**, or **hypothesis**. Detailed local fixtures and raw logs are retained privately in the development workspace; they are not uploaded with game data.

## Executable baseline — runtime-tested

The analyzed decrypted ELF matches the emulator's loaded module and sampled live memory, including entry code, OPD and TOC. A diagnostic thread-name patch was observed in an A/B/A run. This establishes the analysis target and controlled patching, not team or playoff functionality.

## Active team identity — runtime-tested

A prototype was added without replacing an existing team. Early fresh creation produced zero prototype games while original FBS schedules remained populated. Its TOID duplicated the donor team's identity. A controlled unique-TOID asset change produced a normal 12-game schedule; all original teams remained.

## Transfer stage — static and runtime-tested

A fixed 126-record allocation was exceeded by the expanded team/stadium join. A bounded reserve patch allowed normal rollover in candidate v3. Duplicate stadium identity was a separate relational issue; candidate v4 assigned an unused identity while keeping the donor stadium model. Fresh creation and field loading confirmed that combination. The combined v5 candidate now also passed normal rollover and cold reload with unique stadium links retained.

## Initial schedule presets — static and runtime-tested

The user observed that the added team faced only FCS opponents in year one but FBS opponents in year two. Analysis traced KnownGenerator to packaged SCHE/SKNW rows filtered by season. The table contains 726 season-zero presets and 169 season-one presets; no prototype entries.

All 726 first-year pairs and weeks matched captured stock and expanded schedules. In the captured second-year save, 158 of 169 preset pairs appeared, with 104 retaining the exact week. Later seasons therefore also have presets.

**Hypothesis:** presets and earlier generator stages fill original-team slots before remaining-game selection reaches the prototype. Eligibility exhaustion is a plausible cause of FCS fallback; the exact live eligibility sequence has not been captured.

Candidate v5 changes only selected packaged matchups while retaining all original FBS-versus-FBS games and weeks. Normal fresh generation produced 12 distinct FBS opponents, six home and six away, and all original FBS teams retained 12 games without weekly collisions. The schedule survived cold reload and a simulated regular season. This validates the bounded asset approach, not realistic full-league content or a universal scheduler solution.

## Combined v5 lifecycle — runtime-tested

Normal offseason simulation reached preseason 2014. Thirty-nine saved-system checks passed: all 132 teams/127 FBS retained; every FBS team has 12 games without weekly collisions; roster/depth references, 198 unique stadium identities, one venue link per FBS, championship history and serialized reserves passed bounded checks. Eight recruits matched prototype players on all eight checked identity fields. A broader read-only comparison found Caleb Wilson on the prototype with seven matching fields and a position change from LG (6) to RG (8). This supports a ninth recruit progressing onto its roster. The board also contains two committed recruits matching players on other teams. Therefore RECB membership plus RCPT.RCCM=1 does not prove which team secured a commitment; the earlier strict checker remains bounded and its raw report is preserved.

A separate cold run loaded preseason 2014 normally. All four save files were unchanged. The depth chart independently showed recruited freshman Blake Vogel on Expansion Test with the saved identity and attributes. Both live probes passed 526 checks. This establishes one rollover for the exact candidate, not repeated-season or full-FBS acceptance.

Observed occupancy: PLAY 8,842/9,100; DCHT 11,176/11,464; STAD 198/200; COCH 405/512; CONT 542/960. These are rows/capacities, not guarantees of safe expansion. The prototype's 2014 schedule has 11 FBS games and one FCS game.

## V6 serialized reserves - static and runtime-tested

Selected table capacities were enlarged without changing membership or the 517 executable patch words. The builder preserved prior row payloads, schemas and unrelated archive entries. Fresh creation, normal simulation through postseason/offseason, and cold reload passed bounded checks at 127 active FBS teams. All 17 expected reserve values persisted. After rollover PLAY contains 8,852/12,600 rows; DCHT 11,176/14,080; STAD 198/240; COCH 403/768; CONT 539/960. These reserves do not prove safe operation at 160 active teams.

Fresh v5 and v6 lack prototype TPHS and RBKS rows. After v5 rollover TPHS remains 572/572: the prototype gains one row while preexisting ID 412, outside the saved FBS set, has three rather than four. RBKS contains 18 prototype rows with types 1/2; original teams have 27 with types 0/1/2. The observed group IDs match active FBS IDs after simulation. Per-team draft history and game/season/career record interpretations are hypotheses pending constructor/pruning tracing. Full membership at 27 records per team would exceed the current RBKS limit. This is a remaining history gap, not a failure of the separately checked bowl/conference championship tables.

Saved TEAM rank fields sampled here are unsigned eight-bit values; sampled runtime rank stores are 16- or 32-bit. A universal seven-bit/127-team rank ceiling is not supported by those observations. Other consumers and sentinels remain unproved. The fixed save-container length also does not establish that opaque trailing bytes are free space.

## Known limits and failures

- The prototype uses borrowed Idaho presentation; coach-selection filtering remains unresolved.
- A first-year FCS-only schedule was a recorded failure, not accepted as completion.
- Some recruiting-board references do not satisfy a proposed cross-table invariant in both stock and expanded fixtures. Their serialized semantics remain unproved; no blanket recruiting-integrity claim is made.
- Full-FBS and repeated-season capacities remain under audit.
- A checker initially assumed conference championship week was stored as15; the captured save stores16. The failed report was retained and rerun with the corrected observation. This was a test expectation error, not an emulator failure.
- No custom 12-team playoff is implemented yet.

## CFBR compatibility investigation - 2026-10-09

The official v21 package was inventoried and selected files extracted privately. Static checks identify update 1.02, incompatible existing patch addresses, 22 changed BOOT payloads, 331 changed MISC payloads and five occupied team IDs requiring remapping. The staged rosters retain 126 active FBS entries. [Details and source links](CFBR_COMPATIBILITY.md). No integration runtime test was performed.

Separately, executable instruction tracing confirms a four-row draft-history initializer for years -4 through -1 and a rollover routine that deletes year-minus-four before inserting current-year counts. These static findings guide the next prototype-history repair; they do not establish that the missing history rows are fixed.

## Initial CFBR port component - 2026-10-09

Completed the separate 1.02 Ghidra analysis and produced a provisional 443/517 site map. Four reviewed ranking-storage words now have a non-installable recipe with 17 offline checks. A capacity-end pointer still describing 126 records must change along with the larger frame. Membership is unchanged. Complete package extraction passed nine inventory/cross-reader checks. No combined runtime test or expansion-port acceptance is claimed. See [compatibility progress](CFBR_COMPATIBILITY.md#port-progress-static-checks-only).

Original asset table labels also establish RBKS/SRRC type 0 as game records, type 1 as season records and type 2 as career records. The prototype lacks seed rows in SRRC; history initialization remains an implementation task.

## Isolated runtime baseline - 2026-10-09

An unmodified CFBR v21/update 1.02 baseline now boots in a separate development profile. The emulator's loaded ELF matches the analyzed ELF byte for byte. Six live memory comparisons passed in each of two runs, including the entry, OPD/TOC and proposed ranking-patch sites. The observed PPU key is `PPU-62e25ebc1957382b34f2778554943e40d6d84e3c`.

Normal gameplay created a fresh Alabama Dynasty. Fifteen structural checks passed: 126 FBS teams, complete 12-game regular schedules without weekly collisions, valid roster/depth references and recruiting initialization. A separate emulator run loaded the save normally; all four save files remained byte-identical. This establishes a fresh-save baseline, not full-season or expansion compatibility.

The game automatically loaded the bundled CFBR23V21 roster. An initial check expecting the built-in roster failed on team 230: the save contains James Madison, while the built-in roster says FIUtest. The auto-load log identifies the actual roster source; the corrected check passes. Future installers and tests must pin roster input as well as archives and executable.

After the test, the development profile redirect was rolled back. All 48 protected stock working-save files were unchanged; original preservation passed 58 checks. No expansion patch was applied to CFBR. Its ranking recipe still needs controlled runtime tests, and the combined mod still needs remapping, season progression and playoff implementation.

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
