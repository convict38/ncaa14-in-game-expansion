# Changelog

Entries describe the observed test scope. Candidate numbers are development iterations, not public release versions.

## 2026-10-09 — Candidate v5: initial FBS schedule experiment

- Traced first-year known matchups to SKNW in a packaged schedule database. All 726 season-zero presets exactly matched both captured stock and expanded 2013 schedules. The added team had no preset entries. Later seasons also contain presets, in smaller numbers.
- Prepared a reversible MISC asset recipe replacing 12 FCS matchup slots with 12 distinct FBS opponents for the prototype. Balanced its venues at six home/six away. Moved one matchup into the original opponent's open week because two constrained weeks otherwise required the same opponent.
- Kept the 517 executable patch words and unique-stadium BOOT candidate from v4 unchanged. Original FBS-versus-FBS matchups and weeks are preserved.
- Passed 21 offline asset/projection checks, 28 fresh-Dynasty structural checks, 12 exact-schedule checks, 12 stadium checks and five cold-load/preservation checks.
- Normal simulation completed the regular season and stock postseason. The prototype finished 0–12 with nine recruiting commitments and saved team statistics. Arizona finished 9–4. Fresh and completed-season live probes each passed 526 executable/index checks.
- Latest candidate rollover remains pending. All trial files were rolled back after preserving the end-season fixture.
- Added this public progress repository, installation-status documentation and a read-only executable-identity tool. No installable release published.

## 2026-10-09 — Candidate v4: independent stadium identity

- Assigned the prototype a separate stadium identity while retaining the donor's model.
- Normal fresh creation saved 198 unique stadium identities. Save/load preserved the result.
- Loaded the borrowed indoor stadium and players. A live kickoff/return occurred; the remainder was completed with in-game Super Sim at the user's request.
- The prototype's 33–14 result, statistics and record survived a cold reload. No full manually played game was claimed.

## 2026-10-09 — Candidate v3: transfer buffer and rollover

- Identified a transfer-stage allocation limited to 126 records. The expanded team/stadium join exceeded that allocation.
- Added a bounded reserve patch; a normally resumed Dynasty reached preseason 2014 and cold-loaded successfully.
- All 127 FBS teams retained schedules. Five committed recruits matched prototype players after rollover.
- Duplicate stadium identity and first-year FCS-only scheduling remained separate defects at that checkpoint; later candidates address them.

## 2026-10-09 — Earlier expansion iterations

- Enlarged dependent runtime storage and serialized reserves, with stock-count regression tests before active-team trials.
- The first added-team trial had no games. Correcting the prototype's duplicated TOID produced 12 games without removing an original team.
- Those first-year games were all against generic FCS opponents. This was recorded as a scheduling failure, not accepted as a realistic schedule.

## 2026-10-08 — Reproducible executable baseline

- Verified the original dump and isolated the working emulator, saves and experiments.
- Matched analyzed ELF bytes, OPD/TOC and runtime memory to the loaded module.
- Established a local Ghidra PowerPC analysis workflow without requiring REA support.
- A diagnostic thread-name patch passed an unpatched/patched/restored observation test.
