# NCAA Football 14: In-Game Expansion

A personal-use modding project for NCAA Football 14 (PS3). The goal is a complete, modern college football game built on the one the player already owns: all 138 real 2026 FBS schools in their 2026 conferences, a 12-team College Football Playoff that runs through normal Dynasty play, modern rules, and later realism features.

**Development project. There is no public installable release yet.** Installer and packaging work is deliberately last, after the game itself is complete.

## What it is

- A set of small, documented changes to the game's code and data. Most are written as C "caves" (small compiled routines patched into the executable) plus data edits.
- Built on the community CFB Revamped (CFBR) v21 base, tested on the RPCS3 emulator.
- A second track runs the same modded game as a native Windows program (a static recompilation, "the PC port"). The PC port is the intended standalone modded version.
- The repository contains only project-authored documentation and tools. It contains no game files, assets, executables, saves or decompiled code. Players supply their own game dump.

## Current status (2026-10-28)

Working and validated on the modded build:

- 138 real 2026 FBS teams with 2026 conferences, through multi-season Dynasty (full season, bowls, rollover).
- A native 12-team playoff: seeding, byes, bracket, CFP round names and dates, user-played playoff games, recorded champion.
- Modern clock and overtime rules, Dynasty starting in 2026, 60-season Dynasty length, original CFP logo art, several community team-art packs.
- PC port: the whole mod stack runs natively. Audio, Super Sim, Dynasty, Road to Glory and Play Now are validated. Live gameplay now runs at real speed (it was in slow motion); borderless full-screen with variable refresh and a display settings file are in.

In progress: frame rate and stutter on the PC port, and an FBS+FCS universe in a separate PC-port test build (150 teams in one Dynasty so far; FCS schools play with their real rosters and keep their stats, get clean 11-12 game schedules with conference games, a full season with enlarged stat tables runs to the end of the playoff, and FCS schools keep full rosters and coaching staffs across seasons, with three seasons played in a row; a 266-team test build plays a full season including the bowls and playoff, runs its first off-season and plays into its second season with full coaching staffs, recruit classes grow with the number of schools, FCS stat leaders are kept in their own lists, FCS playoff results are worked out at the end of the season, bowl and playoff picks are correct with 266 schools, the Dynasty has reached its third season, FBS teams keep playing about 100 FCS opponents a season after the first, the SWAC title game is played on the field, the Dynasty has reached its fifth season with full rosters, team ratings can be kept on a fixed scale, FCS recruit strength depends on the school's level, real-life series are kept when FBS-vs-FCS games are added, and realistic recruit classes in which top recruits skip FCS schools now work in the game: almost every four- and five-star signs with an FBS school, and each FCS level recruits its own kind of player). See the [roadmap](ROADMAP.md) for everything that follows.

Exact test evidence is in the [changelog](CHANGELOG.md). The [machine-readable status](reports/latest-status.json) lags the changelog; when they disagree, trust the changelog.

## How the pieces fit

| Piece | Where to read |
| --- | --- |
| What was done, by date, with validation | [CHANGELOG.md](CHANGELOG.md) |
| What is planned, in priority order | [ROADMAP.md](ROADMAP.md) |
| Function names, table layouts, addresses, how mods are built | [docs/modding/](docs/modding/README.md) |
| Findings, hypotheses and failures | [docs/RESEARCH_LOG.md](docs/RESEARCH_LOG.md) |
| Test method and build identities | [docs/TESTING.md](docs/TESTING.md), [docs/SUPPORTED_BUILDS.md](docs/SUPPORTED_BUILDS.md) |
| Roster, archive and CFBR compatibility | [docs/ROSTER_PIPELINE.md](docs/ROSTER_PIPELINE.md), [docs/ARCHIVE_ADAPTER.md](docs/ARCHIVE_ADAPTER.md), [docs/CFBR_COMPATIBILITY.md](docs/CFBR_COMPATIBILITY.md) |
| Handoff for new contributors or agents | [docs/DEVELOPER_HANDOFF.md](docs/DEVELOPER_HANDOFF.md) |
| Where files go | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Older README and roadmap (superseded) | [docs/README_HISTORY.md](docs/README_HISTORY.md), [docs/ROADMAP_HISTORY.md](docs/ROADMAP_HISTORY.md) |

The tools folder holds small helpers: a game-identity check, an archive reader with tests, and `check_public.py`, which must pass before every commit.

## Legal

An independent community project. No affiliation with EA, the NCAA, RPCS3 or other NCAA Football mod projects is claimed. Public availability of this repository does not imply a tested installer or a completed mod, and does not grant any right to game assets.
