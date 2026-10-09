# NCAA Football 14: In-Game Expansion

An experimental PS3/RPCS3 project to add every FBS school while retaining existing teams, and build a 12-team playoff that runs entirely through normal gameplay.

**Development project — no public installable mod release yet.** The current prototype has 127 active FBS teams. It does not include all intended schools, finished presentation, or a custom playoff.

## What has been tested

- The analyzed executable matches the module running in RPCS3. A controlled diagnostic patch passed an unpatched/patched/restored test.
- One additional active Dynasty team coexists with all original teams, with roster, recruiting, schedules, statistics and save/load evidence.
- The latest schedule experiment gives the added team 12 distinct FBS opponents, six home and six away. Every original FBS team still has 12 games; existing FBS-versus-FBS matchups and weeks are retained.
- A fresh Dynasty, cold reload, regular season and stock postseason completed under this experiment. The prototype finished 0–12 and received nine recruiting commitments.
- A previous candidate passed 2013-to-2014 rollover and cold reload. **Rollover of the latest schedule/unique-stadium combination is still pending.**

The prototype borrows Idaho presentation. A separate stadium identity with the donor's stadium model passed field loading and a Super Sim game in an earlier candidate. These are bounded tests, not a finished release.

## Follow development

- [Changelog](CHANGELOG.md): dated changes and validation results.
- [Roadmap](ROADMAP.md): remaining work and release gates.
- [Research log](docs/RESEARCH_LOG.md): confirmed findings, hypotheses and failures.
- [Installation status](docs/INSTALLATION.md): supported setup and what remains before distribution.
- [Testing](docs/TESTING.md) and [build identities](docs/SUPPORTED_BUILDS.md).
- [Machine-readable status](reports/latest-status.json).

The repository contains project-authored documentation and tools. Game images, executables, game archives, assets, firmware, saves, emulator caches, raw memory dumps and decompiled game code are not included. Players will supply their own game dump.

This is an independent community project. No affiliation with EA, the NCAA, RPCS3, or other NCAA Football mod projects is claimed. Public availability of the repository does not imply a tested installer or a completed mod.
