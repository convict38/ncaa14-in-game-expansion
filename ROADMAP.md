# Roadmap and acceptance gates

## Next development work

Update 2026-10-11: priority order is a complete game first, distribution last. (1) Let users play their own playoff games (fix in test). (2) CFB Revamped port: 126-team storage, then 138 real 2026 teams, then the playoff. (3) Dynasty starting in 2026 with all 60 seasons. (4) Logos and art for the 13 additions and College Football Playoff UI branding. (5) "Choose Your First Job" showing the additions. (6) Super Sim fixes and a review of sim stat realism. (7) Realistic player names with matching appearance, for rosters and generated recruits. (8) Stretch goals: FCS alongside FBS, playoff format toggles, longer Dynasties and larger saves; 105-man rosters and the transfer portal after a brainstorm. (9) Last: licensing and attribution, installer and uninstaller, clean-machine test. Side track: native Windows build via static recompilation (feasibility spike positive, boot-to-menu attempt in progress).

Update 2026-10-10 (late): goals 1 and 2 run together on the stock build (138 real 2026 FBS teams + native 12-team playoff, one full season and rollover). In progress: v4 data with ACC/Big Ten conference schedules and enlarged history tables, under a multi-season test. Then: the CFBR port, graphics for the 13 additions and CFP UI, champion-based auto bids, and a portable installer.

Update 2026-10-10 (night): milestones 3 and 4 are runtime-proven separately on the stock build: the real 2026 lineup (138 FBS, 2026 conferences) through a full season and rollover, and the native 12-team playoff (at 126 teams). Next: fix ACC/Big Ten conference schedule counts, enlarge history tables for multi-season play, combine the playoff with the 138-team lineup, port to CFBR, then presentation (logos for additions, CFP UI) and an installer.

Update 2026-10-10 (evening): the native 12-team playoff passed a full in-game season on the stock build (v2). The real 2026 lineup (125 retained + 13 additions, 2026 conferences) is built but crashed at season start; root-causing is in progress. Next: fix the real-2026 data issues, combine playoff + 138 teams, then port to CFBR and begin presentation assets (team logos and CFP UI).

Update 2026-10-10 (later): 138 active FBS teams passed a full season and rollover on the stock build with the active-N v2 recipe (placeholder identities). Next: (a) enlarge TPHS/RBKS and run repeated seasons; (b) replace the 12 placeholders with real 2026 schools and realign the 47 conference changes; (c) port the recipe to CFBR; (d) native 12-team playoff, whose first in-game test is starting (offline-validated code hook, BOWL data and checker).

Update 2026-10-10: the first added identity (a non-FBS team inside the 138-team reserve) passed fresh Dynasty, cold reload, a full season and rollover in the CFBR build, and the engine scheduled it on its own. The immediate engine step is a 138-team proof: the runtime-validated stock 127-team recipe appears to have only 71 count-dependent words, with storage already reserved for 160 teams. An active-N version is being built offline for a stock 138-team trial; the same recipe is then ported to CFBR.

The four-word CFBR ranking patch has passed a season, rollover and cold reload at 126 teams. The immediate path is a CFBR-specific recruiting/storage port, coordinated BOOT and auto-loaded roster edits, then distinct team identities and football conferences. CFBR recruiting entries are 12 bytes where stock entries are 8; copying stock relocation values is unsafe. Offline archive and roster reserves do not close the engine or save-packaging gates. See [developer handoff](docs/DEVELOPER_HANDOFF.md).

The source-only roster trial now proves BOOT selection, native saving and cold auto-load with unchanged capacities at 126 teams. A capacity-only follow-up then passed 48 checks: native roster saving and cold auto-load kept the minimal 138-team reserves (TEAM 153, PLAY 9,660, DCHT 12,144, COCH 439, CSKL 414, STAD 210) at 126 teams. A coordinated BOOT354 Dynasty-template reserve then carried those capacities through fresh Dynasty creation, cold reload, a full simulated 2013 season and rollover to 2014 (21, 28, 28 and 30 checks). The capacity-only ladder is complete; the next bounded gate is the first added identity rows inside the reserve. Engine storage and lifecycle limits remain open. See [roster pipeline](docs/ROSTER_PIPELINE.md).

1. Extend the passed v6 reserve regression at 127 active teams to repeated seasons. Resolve missing prototype TPHS/RBKS initialization, record-type coverage and their full-membership bounds. Resolve remaining recruiting-reference semantics: commitment status plus board membership does not establish the destination team; position changes must be accounted for in identity matching.
2. Resolve coach-selection filtering and remaining presentation consumers. Audit dependent consumers and repeated-season/full-FBS capacities, including contract lifetime, history tables and the opaque save-container trailer. Larger serialized reserves alone do not establish larger active counts.
3. Add the target 138 active 2026 FBS identities: 125 original current-FBS schools plus 13 additions. Idaho is deferred to future FCS mechanics; preserve its original backups and historical mapping. Restore distinct New Mexico State, UConn, UMass and FIU identities alongside CFBR's replacement schools. Prioritize football conferences, schedules, recruiting, actual games and persistence; borrowed uniforms/logos/venues are acceptable during these tests. Complete school-specific graphics after the systems work. Membership, transition eligibility and conference rules require separate validation.
4. Implement the in-game 12-team playoff: selection, seeding/byes, first-round sites, legal dates, four rounds/11 games, results-driven advancement, championship history, awards and normal season rollover.
5. Last, after the game is complete: package and validate a portable installer and uninstaller against a clean supported user dump and isolated saves.

## Release acceptance

- Exact supported executable identities; refuse unknown builds and unexpected patch preimages.
- All 138 target identities appear exactly once, including the 125 original current-FBS schools. Added teams work in gameplay and simulation, recruiting, statistics, standings/rankings, save/load and repeated season rollover. Idaho remains an explicit deferred exception.
- No schedule collisions, missing games or invalid team/stadium references; conference scheduling rules are tested.
- Playoff selection and every round survive save/load. Re-entering a completed stage must not duplicate games, awards or championships.
- No external save editor is required between rounds or seasons.
- Installation builds changes locally from the user's own files, preserves originals, verifies outputs and supports rollback.
- A clean-machine installation and removal test passes before a public installable release.
- Distribution contains project-authored patch recipes/tools and reviewed documentation, with third-party attribution and licensing settled before release.

## Later extensions

- Super Sim reliability and realistic simulated stats (box scores and season totals against real college football averages).
- Realistic player names, with skin tone and face matched to the name, for rosters and generated recruits.
- Native Windows build via static recompilation (ps3recomp), as a side track or in collaboration with related projects.
- Dynasty starting in 2026 while keeping all 60 seasons (two base-year constants identified; test pending). Optional: unlimited Dynasty length (grow history tables, widen season fields, roll off old history) and a larger save file.
- Brainstorm before implementing: 105-man rosters (players are currently allocated about 70 per team), transfer portal and other modern-CFB rules.
Configurable playoff formats, FCS league support and custom stadium work. These remain separate from the initial acceptance scope.
