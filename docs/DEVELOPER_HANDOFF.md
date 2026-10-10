# Developer handoff

This is the agent-neutral entry point for contributors, including coding agents. Read this with [current status](../reports/latest-status.json), [CFBR compatibility](CFBR_COMPATIBILITY.md), [testing](TESTING.md) and the [roadmap](../ROADMAP.md). Historical log entries describe their own candidates; the latest result never retroactively upgrades an older test.

## Start here

In the private `mod-work` workspace, read `docs/continuation-checkpoint.md` before taking over. Check actual process identities, file/config hashes, existing test outputs and ownership of the emulator, saves and shared checkpoint. Determine whether a pending test already started or completed before launching anything; do not duplicate it or interrupt another owner.

The update below is a checkpoint through **2026-10-10 13:25 UTC**, not live process status. The linked public status report may describe an earlier checkpoint or a different candidate. Read each result's timestamp and scope before using it.

## Objective and priority

Target 138 active 2026 FBS identities: 125 stock schools still in the proposed FBS field plus 13 additions. Idaho is deferred to future separate FCS mechanics. Preserve original inputs and historical mappings. The immediate priority is playable teams with correct football conferences, schedules, recruiting and persistence. Reused graphics are acceptable during development; graphics and UI polish come last. The automatic in-game 12-team playoff remains a later required milestone, currently unimplemented.

## Current evidence

| Component | Established | Still open |
| --- | --- | --- |
| Stock expansion v6 | 127 active teams; fresh Dynasty, one season/rollover and cold load | Larger counts, repeated seasons, history initialization and finished content |
| CFBR ranking patch | Four words; normal 2014 season, stock postseason, 2015 rollover and cold load at 126 teams; rolled back | Producer execution trace and expanded membership |
| CFBR archive adapter | 16 synthetic tests, 4,840-entry parser comparison, 34 offline candidate checks | Coordinated engine installation and runtime acceptance |
| Auto-loaded CFBR roster | Source-only native-save test: 32 roster checks; capacity-only test: 48 checks with six grown capacities preserved through native save and cold auto-load at 126 teams; coordinated Dynasty-template reserve: fresh Dynasty, cold reload, 2013 season, postseason and 2014 rollover with grown tables (21/28/28/30 checks) | Added identities in the reserve, engine limits, played games and repeated seasons |
| Team/conference input map | 138 unique proposed names; 125 match stock, 13 are additions; 126 match CFBR auto-load | Destination IDs, per-team associations, conference scheduler limits and eligibility |
| Recruiting layout | CFBR first array uses 126 twelve-byte records; stock uses eight-byte records | Complete allocation, clear, indexing, relocation and serialization consumer agreement |

The 138-target comparison requires 12 identities absent from the auto-loaded roster and 47 conference-ID changes among its existing teams. Keeping all 15 non-FBS source rows requires 153 roster TEAM rows, exceeding the earlier 146-row reserve. Serialized capacity alone does not prove engine capacity. No destination IDs have been assigned. Conference IDs exist in the input tables, but 18-team conferences, divisionless championships and scheduling rules still need engine-level validation.

The ranking trial's checks were 28 regular season, 28 postseason, 30 rollover, six live reads in each of two runs, four byte-identical cold-load save files, 48 protected stock files and 58 original-preservation checks. Alabama finished 12-2; 12 recruits matched the next-year roster. These results use normal saves and simulation. They do not validate a custom playoff or 138 teams.

### Latest checkpoint

- **Source-only roster packaging:** The native-save test passed 32 roster checks and 58 preservation checks. The whole `USR-DATA` matched the intended source bytes. Cold restart auto-loaded roster Q and reached the roster screen; four save files and both protected collections were unchanged, and the VFS configuration was restored. This validates the source-only path, not enlarged reserves or 138 active teams.
- **Minimal reserve budget:** Ten offline checks reported 78,600 bytes of growth, compared with 499,452 for the broad reserve proposal. The remaining 34,840 bytes within the old USR file length are not proven padding and must not be treated as free space.
- **Capacity-only trial passed (2026-10-10 ~01:20 UTC, Cline as runtime owner):** BOOT `39420929…7a2b` changed only entry 355 to the minimal-reserve database, at 126 active teams. It ran in a new clean profile, separate from the source-only profile, whose saved roster would auto-load. The first boot had no roster auto-load. The native save of roster Q kept TEAM 153, PLAY 9,660, DCHT 12,144, COCH 439, CSKL 414 and STAD 210; saved USR is `9d92f57c…958a`. Cold auto-load left four files byte-identical, both runs had six live reads, and the 48-check report and 58 preservation checks pass. The profile redirect is rolled back and no isolated emulator is running. This does not test added identities, engine limits or Dynasty/season use of the grown tables.
- **Grown Dynasty tables passed season and rollover (2026-10-10 ~13:20 UTC, Cline as runtime owner):** A roster-only reserve BOOT left Dynasty capacities at the baseline (16 checks), so BOOT354 controls Dynasty sizes. A coordinated BOOT354 + BOOT355 candidate (16 offline checks) produced a fresh Dynasty whose autosave has TEAM 153, PLAY 9,660, DCHT 12,144, COCH 439, CSKL 414 and STAD 210; cold reload byte-identical (21 checks). The same Dynasty simulated the 2013 regular season (28), postseason (28) and rollover to Pre-Season 2014 (30), with seven grown-capacity checks per snapshot. Pre-Season 2014 USR is `7a7a434f...cc0f`. Six live reads per run; rolled back; 48 protected stock files and 58 preservation checks pass. No isolated emulator is running. This does not test added identities, engine limits, played games or recruiting with added teams.
- **Static storage work:** Lifecycle analysis passed 74 checks and the caller audit passed five. Deleted/free-list behavior was confirmed; the inspected RECB data had at most 35 live records per team. The earlier count of 41 physical records per team included deleted records. Allocator/serialization report v5 recorded 60 checks. Its packaging command returned exit 1, apparently associated with a no-Java-process check. A later integrity check matched all 230 recorded artifact hashes, and the exit 1 did not reproduce.
- **Acceptance limits:** Static analysis indicates that higher-level callers may advance counters after insertion failure; this has not been demonstrated at runtime. Peak occupancy, RCPT behavior, caller bounds and capacity acceptance remain open. There are zero accepted CFBR capacity-port patch sites. The four-word ranking patch remains validated only at 126 teams and was restored; a cold run of the restored code has not been verified.

## Shortest next milestones

1. Done: the capacity-only ladder passed (roster save/reload, fresh Dynasty, cold reload, season and rollover; see latest checkpoint). Next runtime gate: add the first identity rows inside the reserve, coordinated across BOOT355 roster and BOOT354 template, inactive first. Keep 153 TEAM rows when retaining all 15 non-FBS rows.
2. Finish the CFBR-specific recruiting/storage consumer map, including peak live occupancy, RCPT, caller failure handling and bounds, allocation and serialization. Emit a reversible, exact-preimage recipe only for verified sites. Keep logical membership separate from reserve capacity. Seven normalized-context leads remain hypotheses; no CFBR capacity-port patch site is accepted.
3. Coordinate the BOOT template, built-in roster and actual auto-loaded CFBR23V21 roster using their individual schemas. Restore New Mexico State, UConn, UMass and FIU as distinct identities; preserve CFBR's existing added schools. Use the validated source-only save path as a baseline, then separately establish enlarged-container and runtime acceptance.
4. First expanded CFBR trial: one additional active identity at 127 teams with the complete engine/data recipe and borrowed presentation. This is a proposed diagnostic step, not an existing safe candidate. Once it passes, populate all 138 identities and the target conferences without cosmetic work between these steps.
5. Minimum expanded-candidate checks: fresh creation; exact semantic membership and ID joins; valid rosters/depth/coaches/stadiums; complete collision-free schedules; actual game and simulation results; recruiting; normal save/restart/reload; postseason and rollover with retained history and next-year schedules. Repeat at the final 138-team conference layout before calling it playable.

## Reproduction and ownership

Public archive tests require only Python: `python -B -m unittest discover -s tools -p test_bgfa_archive.py -v`. The public identity checker is documented in [supported builds](SUPPORTED_BUILDS.md). No portable expansion installer exists.

Detailed runtime scripts, fixtures and logs remain in the private development workspace. Its `docs/continuation-checkpoint.md` records the current process/config state, exact commands and backup paths; `docs/public-repository.md` records publication procedure. Those paths are relative to the private `mod-work` directory, not files shipped here. A contributor with only this repository must use their own supported inputs and cannot reproduce the private runtime trial from public files alone.

Only one owner controls the isolated emulator, its configs/saves, shared checkpoint and publication. A parallel static lane writes separate analysis outputs; review does not authorize it to install patches. The ranking trial ended with its patch/profile redirect disabled; the later source-only roster trial reported VFS restoration. These are historical checkpoints, not proof of current process or configuration state. Recheck actual process identity and config hashes before any later run; never rely on a historical PID or control the original emulator.

The public repository has been updated from a reviewed export through the GitHub API. At the last documented publication checkpoint, the export's local Git branch was unborn and was not a synchronized checkout; inspect its current state before using Git commands. Fetch the current remote head, preserve concurrent changes, update without force using an expected head, then verify exact file contents. Publish only reviewed project-authored source/docs. Keep game binaries, assets, saves, raw logs, decompilation, credentials and private paths out of this repository.

## Coordination at checkpoints

Use this handoff and `reports/latest-status.json` as shared, reviewed checkpoints. Record the candidate, UTC timestamp, exact commit, verified results, pending or never-run checks, current ownership and next action. Keep private paths and detailed runtime evidence in the local continuation checkpoint. Update public claims only after checking the corresponding evidence. The machine-readable status report includes the grown Dynasty season/rollover trial.

GitHub provides a place for contributors and assistants to read each other's published checkpoints. Cline must be instructed to check for updates at safe task boundaries. It is not a direct live connection to Cline or another coding agent, and publication alone does not establish active synchronization or transfer runtime ownership.
