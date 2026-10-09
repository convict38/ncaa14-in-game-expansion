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

Candidate v6 now has fresh creation, exact initial scheduling, cold load, regular-season, stock-postseason, normal offseason rollover and separate preseason-2014 cold-load evidence for the same executable/asset identities. Rollover passed 46 saved-system checks; cold reload passed five; fresh, rollover and cold live probes passed 526. Independent cold UI observation confirmed Jake Bracken, recruited freshman TE #86. The larger serialized reserves were tested at unchanged 127 active FBS teams. Separate TPHS/RBKS history gaps remain outside these acceptance checks. Only one rollover is established for this exact candidate; repeated-season/full-FBS acceptance remains open. See [latest-status.json](../reports/latest-status.json) for current acceptance flags.

Report title/update version, executable hash, RPCS3 version, candidate/release version, reproducible steps, expected/observed behavior and whether the Dynasty was new or migrated. Redact personal paths/account details. Do not attach game binaries, database archives, full memory dumps, firmware or saves to public issues. A summary of the relevant values is sufficient for initial triage.
