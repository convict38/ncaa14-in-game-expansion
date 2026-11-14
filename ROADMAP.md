# Roadmap

Priority order, highest first. A complete game comes before any distribution work. Dated history of earlier plans is in [docs/ROADMAP_HISTORY.md](docs/ROADMAP_HISTORY.md).

## Next

1. **Frame rate and stutter (in progress).** The PC port now plays at real speed but is CPU-bound in heavy scenes, with play-transition hitches. Build 97 (2026-11-02) made game-thread indirect calls and atomics cheaper (about +2.5 % game speed, +2 fps). Remaining: smoother frame pacing, an optional multi-threaded renderer, input-latency work. Update 2026-11-13: the shader cache is now preloaded into memory (rc67), removing most loading pauses and kickoff hitches. The owner wants fully native, lag-free gameplay, so a native-gameplay lane has started: profile in-play host time, then port the hottest recompiled paths to readable native code behind switches, each checked by a dual-run equivalence checker. The ported logic stays private; tooling, measurements and behaviour documentation are published.
2. **In-game settings page with keyboard and keybindings.** Built into EA's own menus, not an external launcher: display options, frame cap, and rebindable keyboard and controller controls.
3. **In-game Dynasty CFP bracket page.** A bracket view in Dynasty (seeds, byes, results by round) and a weekly playoff projection during the season.
4. **Graphics check and long-run validation.** Compare PC-port graphics against RPCS3 for remaining differences. Run multi-season Dynasty and Road to Glory checks on the PC build.
5. **Recruit realism.** Realistic names, and demographic and appearance distributions (skin tone and face matched to name) for rosters and generated recruits.
6. **FCS as a separate league inside Dynasty.** Idaho and other FCS schools live in their own league rather than being absent from the FBS field.
7. **More realism.** Transfer portal, real schedules and rivalries, coaching carousel, weather, roster rules (for example 105-man rosters).
8. **Self-hosted online play and online Dynasty.** Players run their own server; no dependence on EA services.
9. **Packaged tool: your disc → native PC build + mods (last, after the game is complete).** One tool that takes the user's own disc dump and their own keys/firmware and generates the native PC build locally, then applies mods as recipes or patches rebuilt from the user's own files. No game code or data is ever distributed. Includes the portable installer and uninstaller: preserve originals, verify outputs, support rollback. Needs a clean-machine install and removal test first.

## Done

- 138 real 2026 FBS teams in 2026 conferences, through full multi-season Dynasty with rollover (stock and CFBR builds).
- Native 12-team College Football Playoff: selection, byes, fixed bracket, round names and dates, conference-champion automatic bids, user-played playoff games, champion recorded through rollover.
- Modern rules: running clock after first downs, modern overtime, runtime-confirmed in Exhibition and Dynasty.
- Dynasty starting in 2026 with 60 seasons, record-book year fix, coach contract and coaching carousel fixes.
- CFB Revamped port of the whole stack, original CFP logo art, community team-art packs.
- Native Windows build (PC port) running the full mod: Super Sim, Dynasty, Road to Glory and Play Now validated; audio solid; score corruption and freeze fixes; picture fixes (blacks, crowd, helmets, shadows); gameplay speed fixed from slow motion to real time; borderless full-screen with variable refresh and a settings file.
- Public modding knowledge base in [docs/modding/](docs/modding/README.md) and a pre-commit content check.

## Release gates (unchanged)

- Exact supported executable identities; refuse unknown builds and unexpected patch preimages.
- All 138 identities appear once; added teams work in gameplay, simulation, recruiting, statistics, standings, save/load.
- No schedule collisions or invalid references; playoff rounds survive save/load without duplicating games or awards.
- No external save editor needed between rounds or seasons.
- Installation preserves originals and supports rollback; clean-machine install and removal pass.
- Distribution contains project-authored recipes and tools only, with third-party attribution and licensing settled.
