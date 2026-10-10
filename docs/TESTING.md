# Validation and reporting

A generated patch or a team menu entry is not a passing integration test. Every candidate records its source/output identities, coordinated patch set, conditions, observations and remaining limitations.

## Test layers

1. **Static:** verify executable preimages, instruction ownership/dataflow, database schemas, bit encodings, checksums and capacity limits. Independently check changed fields and unchanged data.
2. **Fresh Dynasty:** create normally; retain original team IDs; verify membership, rosters, depth charts, coaches, schedules, stadium joins and serialized reserves.
3. **Runtime:** verify the loaded executable and installed patch words; observe the affected game systems through normal menus/gameplay or simulation.
4. **Persistence:** save through the game, stop/restart the isolated emulator and load normally; compare preserved files and independent UI observations.
5. **Season lifecycle:** simulate games, verify scores/records/statistics/recruiting, progress through postseason and offseason, check history, roster changes and new schedules, then cold reload again.
6. **Release:** repeat on a clean supported setup using only the distributed installer and the tester's own dump; verify removal and original preservation.

## Latest evidence scope

The [archive adapter](ARCHIVE_ADAPTER.md) has 16 synthetic tests, a 4,840-entry comparison against the preexisting parser and 34 offline CFBR candidate checks. These are archive/data preservation tests; the CFBR candidate is not installed or runtime-tested. Run the public tests with `python -B -m unittest discover -s tools -p test_bgfa_archive.py -v`.

Candidate v6 now has fresh creation, exact initial scheduling, cold load, regular-season, stock-postseason, normal offseason rollover and separate preseason-2014 cold-load evidence for the same executable/asset identities. Rollover passed 46 saved-system checks; cold reload passed five; fresh, rollover and cold live probes passed 526. Independent cold UI observation confirmed Jake Bracken, recruited freshman TE #86. The larger serialized reserves were tested at unchanged 127 active FBS teams. Separate TPHS/RBKS history gaps remain outside these acceptance checks. Only one rollover is established for this exact candidate; repeated-season/full-FBS acceptance remains open. See [latest-status.json](../reports/latest-status.json) for current acceptance flags.

Report title/update version, executable hash, RPCS3 version, candidate/release version, reproducible steps, expected/observed behavior and whether the Dynasty was new or migrated. Redact personal paths/account details. Do not attach game binaries, database archives, full memory dumps, firmware or saves to public issues. A summary of the relevant values is sufficient for initial triage.

The CFBR four-word ranking patch now has its own season, rollover and cold-load evidence at126 teams:28/28/30 checks, six live reads in each of two runs, allfour save files unchanged on cold load,48 protected stock files and58 preservation checks. It is rolled back. See [CFBR compatibility](CFBR_COMPATIBILITY.md) for exact scope. The separate auto-loaded-roster leading TDB reserve has19 offline preservation checks; its outer save packaging and engine integration are untested.

The later source-only BOOT roster has 32 passing checks at unchanged 126 teams and unchanged capacities, with no code patch: exact native saved USR, all ten tables, four unchanged cold-save files, two sets of six baseline live reads, normal cold auto-load, profile rollback and protected-save preservation. Original preservation separately passes 58 checks. A premature aggregate run failed three rollback-state checks while the emulator was exiting; it remains preserved separately from the terminal passing report. [Roster pipeline](ROSTER_PIPELINE.md) distinguishes this runtime result from uninstalled reserve candidates and the 13-check container/ten-check minimal-budget audits.

The capacity-only minimal-reserve BOOT then passed 48 checks in a separate clean profile at 126 teams: no first-boot roster auto-load, native save preserving all six grown capacities, cold auto-load with four unchanged save files, two sets of six live reads, rollback, 48 protected stock files and 58 original-preservation checks. No identities were added and no code was patched.

The coordinated BOOT354 + BOOT355 minimal-reserve candidate then passed, at 126 FBS and 131 Dynasty teams: fresh offline Dynasty with all six grown capacities written, cold reload with four unchanged files (21 checks), 2013 regular season (28), postseason (28) and rollover to Pre-Season 2014 (30). Seven grown-capacity checks passed on each snapshot, with six live reads per run, rollback, 48 protected stock files and 58 original-preservation checks.
