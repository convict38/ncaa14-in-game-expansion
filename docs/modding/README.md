# Modding knowledge base

This folder is the public version of the project's reverse-engineering notes for NCAA Football 14 (PS3, BLUS31159) and the CFB Revamped (CFBR) v21 base we mod on. It is our own analysis: function and table names, addresses, field layouts, and how each mod is built. It exists so a future contributor does not have to rediscover it.

What is not here: EA files, extracted assets, decompiled code, screenshots, saves, or anything that lets you run the game without your own copy.

## Two address spaces (do not mix them)

- STOCK: the 1.00 executable, patch tag `[01.00]`, RPCS3 PPU key `PPU-011a5e6caad2e7361265a9a230cf385f805671fb`.
- CFBR v21 / update 01.02: the live mod stack, patch tag `[01.02]`, PPU key `PPU-62e25ebc1957382b34f2778554943e40d6d84e3c`. Most CFBR globals sit at stock plus `0x10080`, but verify per function.

Most early notes were made on STOCK. Each file says which space its addresses use.

## Contents

| File | What it covers |
| --- | --- |
| [01-data-tables.md](01-data-tables.md) | TEAM, PLAY, DCHT, coach tables; recruiting objects and capacities; SCHD, conferences, dynasty stage machine, calendar and year handling; rules, playoff, coach and news structures |
| [02-functions.md](02-functions.md) | Named functions by system (teams/recruiting, schedule/dynasty, rules/playoff/rankings/news/coach) with stock/CFBR address pairs |
| [03-patches-and-caves.md](03-patches-and-caves.md) | Patch format on RPCS3, inventory of every patch bundle, C-cave toolchain, installer stage chain |
| [04-building-mods.md](04-building-mods.md) | How to add a mod today (RPCS3 and the PC port) and the ranked list of known gaps |
| [05-pc-port-hook-design.md](05-pc-port-hook-design.md) | Design sketch for a source-level mod-hook interface on the native PC build |
| [06-appendices.md](06-appendices.md) | Archives a modder needs, community mods and licensing, ps3recomp facts, open items |
| [fcs-league-feasibility.md](fcs-league-feasibility.md) | FCS as a second Dynasty league: team-count limits, designs, schedule/playoff changes, UI impact, phased plan |
| [fbs-fcs-universe-plan.md](fbs-fcs-universe-plan.md) | Full FBS+FCS universe with rostered FCS (about 266 teams): every limit with its sites and fix, architecture (active set TTYP <= 1, per-league ranks), save-size and u8-loop Phase 0 patches, phased plan |

## Honesty rules

Every fact was copied from a project note, script or patch. Items labelled static were read from analysis only; items labelled runtime-tested ran in the emulator or PC build. Check the changelog for what has actually been validated.
