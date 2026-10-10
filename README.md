# NCAA Football 14: In-Game Expansion

An experimental PS3/RPCS3 project targeting 138 active 2026 FBS schools and a 12-team playoff that runs entirely through normal gameplay. Preserve the 125 original schools still in the target FBS field; Idaho is deferred to future FCS support. Playable teams, conferences and persistence come first, with borrowed graphics until the systems work.

**Development project — no public installable mod release yet.** The latest engine prototype (stock build) runs 138 active FBS teams, 12 of them placeholders. It does not yet include the real added schools, finished presentation, or a custom playoff.

## What has been tested

- The analyzed executable matches the module running in RPCS3. A controlled diagnostic patch passed an unpatched/patched/restored test.
- One additional active Dynasty team coexists with all original teams, with roster, recruiting, schedules, statistics and save/load evidence.
- The latest schedule experiment gives the added team 12 distinct FBS opponents, six home and six away. Every original FBS team still has 12 games; existing FBS-versus-FBS matchups and weeks are retained.
- Candidate v6 enlarges selected save capacities at unchanged 127-team membership. It passed fresh creation, cold load, a simulated regular season and stock postseason, normal 2013-to-2014 rollover, and a separate cold reload. The prototype finished 1-11 with 13 class commitments; 13 recruits matched its next-year roster.
- All 127 FBS teams retained complete next-year schedules without weekly collisions, and the checked championship metadata persisted. A recruited freshman was independently verified in the cold-loaded depth chart.
- Separate record-history initialization and capacity gaps remain under repair. Passing these bounded tests does not establish complete history, larger active counts or repeated-season safety.

The prototype borrows Idaho presentation. A separate stadium identity with the donor's stadium model passed field loading and a Super Sim game in an earlier candidate. These are bounded tests, not a finished release.

The first added team identity inside the 138-team reserve now survives Dynasty creation, cold reload, a full season and rollover in the CFBR build (still 126 FBS); see the [changelog](CHANGELOG.md).

**New:** the stock build has run 138 active FBS teams (126 originals + 12 placeholders) through a full simulated season, postseason and rollover; see the [changelog](CHANGELOG.md). Real 2026 schools and conferences, the CFBR port and the playoff are next.

## Follow development

- [Changelog](CHANGELOG.md): dated changes and validation results.
- [Roadmap](ROADMAP.md): remaining work and release gates.
- [Research log](docs/RESEARCH_LOG.md): confirmed findings, hypotheses and failures.
- [Installation status](docs/INSTALLATION.md): supported setup and what remains before distribution.
- [Testing](docs/TESTING.md) and [build identities](docs/SUPPORTED_BUILDS.md).
- [Machine-readable status](reports/latest-status.json).
- [Developer handoff](docs/DEVELOPER_HANDOFF.md): current scope, mapped systems, blockers and next steps for any contributor or coding agent.

The repository contains project-authored documentation and tools. Game images, executables, game archives, assets, firmware, saves, emulator caches, raw memory dumps and decompiled game code are not included. Players will supply their own game dump.

This is an independent community project. No affiliation with EA, the NCAA, RPCS3, or other NCAA Football mod projects is claimed. Public availability of the repository does not imply a tested installer or a completed mod.

## Revamped integration

The [archive adapter](docs/ARCHIVE_ADAPTER.md) now handles stock and CFBR archive layouts, with 16 public synthetic tests and a private reserve candidate that passes 34 offline checks. It is a development library; the candidate has not been installed or runtime-tested.

CFBR v21 is a documented compatibility target. Its four-word ranking-storage patch now passes a normal 2014 season, stock postseason, 2015 rollover and separate cold reload at unchanged 126-team membership. The trial is rolled back. Expanded membership remains blocked on the CFBR-specific engine port and coordinated data inputs. [Measured conflicts and integration gates](docs/CFBR_COMPATIBILITY.md) cover its different executable, archives and historical team-slot replacements.

A separate [roster pipeline test](docs/ROSTER_PIPELINE.md) proves BOOT source selection, native saving and cold auto-load at unchanged 126 teams. The saved USR exactly matches the intended source; 32 regression checks pass and the profile is restored. A follow-up capacity-only trial (48 checks) showed the game's own roster save keeps enlarged table capacities for the 138-team target (153 TEAM rows) and auto-loads them cold, still at 126 teams. A coordinated Dynasty-template follow-up then carried the same grown tables through fresh Dynasty creation, cold reload, a simulated 2013 season, postseason and rollover to 2014, still at 126 teams. Added identities, engine team limits and expanded CFBR membership remain untested.
