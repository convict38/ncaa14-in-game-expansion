# Developer handoff

This is the agent-neutral entry point for contributors, including coding agents. Read this with [current status](../reports/latest-status.json), [CFBR compatibility](CFBR_COMPATIBILITY.md), [testing](TESTING.md) and the [roadmap](../ROADMAP.md). Historical log entries describe their own candidates; the latest result never retroactively upgrades an older test.

## Objective and priority

Target 138 active 2026 FBS identities: 125 stock schools still in the proposed FBS field plus 13 additions. Idaho is deferred to future separate FCS mechanics. Preserve original inputs and historical mappings. The immediate priority is playable teams with correct football conferences, schedules, recruiting and persistence. Reused graphics are acceptable during development; graphics and UI polish come last. The automatic in-game 12-team playoff remains a later required milestone, currently unimplemented.

## Current evidence

| Component | Established | Still open |
| --- | --- | --- |
| Stock expansion v6 | 127 active teams; fresh Dynasty, one season/rollover and cold load | Larger counts, repeated seasons, history initialization and finished content |
| CFBR ranking patch | Four words; normal 2014 season, stock postseason, 2015 rollover and cold load at 126 teams; rolled back | Producer execution trace and expanded membership |
| CFBR archive adapter | 16 synthetic tests, 4,840-entry parser comparison, 34 offline candidate checks | Coordinated engine installation and runtime acceptance |
| Auto-loaded CFBR roster | Leading TDB reserve candidate passes 19 offline preservation checks | Outer save-container/HED/trailer packaging; no installable roster candidate |
| Team/conference input map | 138 unique proposed names; 125 match stock, 13 are additions; 126 match CFBR auto-load | Destination IDs, per-team associations, conference scheduler limits and eligibility |
| Recruiting layout | CFBR first array uses 126 twelve-byte records; stock uses eight-byte records | Complete allocation, clear, indexing, relocation and serialization consumer agreement |

The 138-target comparison requires 12 identities absent from the auto-loaded roster and 47 conference-ID changes among its existing teams. Keeping all 15 non-FBS source rows requires 153 roster TEAM rows, exceeding the current 146-row reserve. Serialized capacity alone does not prove engine capacity. No destination IDs have been assigned. Conference IDs exist in the input tables, but 18-team conferences, divisionless championships and scheduling rules still need engine-level validation.

The ranking trial's checks were 28 regular season, 28 postseason, 30 rollover, six live reads in each of two runs, four byte-identical cold-load save files, 48 protected stock files and 58 original-preservation checks. Alabama finished 12-2; 12 recruits matched the next-year roster. These results use normal saves and simulation. They do not validate a custom playoff or 138 teams.

## Shortest next milestones

1. Finish the CFBR-specific recruiting/storage consumer map and emit a reversible, exact-preimage recipe. Keep logical membership separate from reserve capacity. Seven new normalized-context leads are hypotheses, not accepted ports; 67 other sites still lack a lead.
2. Coordinate the BOOT template, built-in roster and actual auto-loaded CFBR23V21 roster using their individual schemas. Restore New Mexico State, UConn, UMass and FIU as distinct identities; preserve CFBR's existing added schools. Audit the roster save container before producing a loadable file.
3. First expanded CFBR trial: one additional active identity at 127 teams with the complete engine/data recipe and borrowed presentation. This is a proposed diagnostic step, not an existing safe candidate. Once it passes, populate all 138 identities and the target conferences without cosmetic work between these steps.
4. Minimum expanded-candidate checks: fresh creation; exact semantic membership and ID joins; valid rosters/depth/coaches/stadiums; complete collision-free schedules; actual game and simulation results; recruiting; normal save/restart/reload; postseason and rollover with retained history and next-year schedules. Repeat at the final 138-team conference layout before calling it playable.

## Reproduction and ownership

Public archive tests require only Python: `python -B -m unittest discover -s tools -p test_bgfa_archive.py -v`. The public identity checker is documented in [supported builds](SUPPORTED_BUILDS.md). No portable expansion installer exists.

Detailed runtime scripts, fixtures and logs remain in the private development workspace. Its `docs/continuation-checkpoint.md` records the current process/config state, exact commands and backup paths; `docs/public-repository.md` records publication procedure. Those paths are relative to the private `mod-work` directory, not files shipped here. A contributor with only this repository must use their own supported inputs and cannot reproduce the private runtime trial from public files alone.

Only one owner controls the isolated emulator, its configs/saves, shared checkpoint and publication. A parallel static lane writes separate analysis outputs; review does not authorize it to install patches. At this milestone the isolated test processes have exited and the ranking patch/profile redirect are disabled. Recheck actual process identity and config hashes before any later run; never rely on a historical PID or control the original emulator.

The public repository is updated from a reviewed export through the GitHub API. The export's local Git branch is unborn and is not a synchronized checkout. Fetch the current remote head, preserve concurrent changes, update without force using an expected head, then verify exact file contents. Publish only reviewed project-authored source/docs. Keep game binaries, assets, saves, raw logs, decompilation, credentials and private paths out of this repository.
