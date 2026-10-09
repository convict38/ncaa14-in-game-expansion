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

Normal offseason simulation reached preseason 2014. Thirty-nine saved-system checks passed: all 132 teams/127 FBS retained; every FBS team has 12 games without weekly collisions; roster/depth references, 198 unique stadium identities, one venue link per FBS, championship history and serialized reserves passed bounded checks. Eight of nine end-season commitments matched prototype players; the ninth is not explained by this test.

A separate cold run loaded preseason 2014 normally. All four save files were unchanged. The depth chart independently showed recruited freshman Blake Vogel on Expansion Test with the saved identity and attributes. Both live probes passed 526 checks. This establishes one rollover for the exact candidate, not repeated-season or full-FBS acceptance.

Observed occupancy: PLAY 8,842/9,100; DCHT 11,176/11,464; STAD 198/200; COCH 405/512; CONT 542/960. These are rows/capacities, not guarantees of safe expansion. The prototype's 2014 schedule has 11 FBS games and one FCS game.

## Known limits and failures

- The prototype uses borrowed Idaho presentation; coach-selection filtering remains unresolved.
- A first-year FCS-only schedule was a recorded failure, not accepted as completion.
- Some recruiting-board references do not satisfy a proposed cross-table invariant in both stock and expanded fixtures. Their serialized semantics remain unproved; no blanket recruiting-integrity claim is made.
- Full-FBS and repeated-season capacities remain under audit.
- A checker initially assumed conference championship week was stored as15; the captured save stores16. The failed report was retained and rerun with the corrected observation. This was a test expectation error, not an emulator failure.
- No custom 12-team playoff is implemented yet.
