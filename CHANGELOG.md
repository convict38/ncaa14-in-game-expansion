# Changelog

## 2026-10-11 - Four-season Dynasty with 138 real 2026 teams and the 12-team playoff (stock build)

The combined mod ran four consecutive seasons (2013-2016) in one fresh Dynasty, each with conference championships, the 12-team playoff, a recorded champion and a rollover, then cold-reloaded byte-identical at Pre-Season 2017. Champions: Alabama (2013 and 2014, both 16-0), Georgia Tech (2015), South Carolina (2016). Alabama went 6-6 in 2015 and 2016 and missed the playoff, so selection follows results. There were no crashes.

The v4 data fixes held in every season: the 17-team ACC played 8 conference games and the 18-team Big Ten played 9, and enlarged history tables stayed within capacity (TPHS 576/720, RBKS 3609/4320, PLAC 3476/4100, TPRC 589/900). The save peaked around 7.01 MB of its fixed 8.28 MB. A live probe at Pre-Season 2017 passed 1,073 checks with 138 FBS teams.

Also built offline since the last update: playoff v3 (automatic bids to the conference championship game winner, in test now), a port of both the 138-team engine recipe and the playoff to the CFB Revamped executable (all words mapped and preimage-checked), and the CFB Revamped version of the 2026 lineup. Research found that the Dynasty start year comes from two code constants. Moving them to start in 2026 should keep the full 60 seasons (2026-2085); this is queued for testing.

## 2026-10-10 - 138 real 2026 FBS teams + native 12-team playoff together in one Dynasty (stock build)

The two core goals now run together in normal Dynasty play on the stock build. All 138 2026 FBS schools play in their 2026 conferences, and the native 12-team College Football Playoff decides the title. A fresh Dynasty showed CFP bowl names in the game's own bowl tie-in screen before the season, and its cold reload was byte-identical.

After a CPU-simulated 2013 season and conference championships, the playoff seeded twelve teams: Virginia Tech, Alabama, Georgia Tech, Boston College, Ohio State, Clemson, Texas A&M, Stanford, Texas, Wake Forest, Kansas State, and C-USA champion FIU. It played first-round games on Dec 11 and advanced winners through upsets: Stanford over top seed Virginia Tech, and Texas A&M over Alabama 21-18. Georgia Tech (15-0) beat Boston College for the title. The game's news and poll showed Georgia Tech as champion, and the save recorded the title once with one bowl-history row per playoff win. The rollover to 2014 kept the playoff calendar. All playoff, integrity and season checks passed. A live probe confirmed all 551 engine words and 510 playoff words with 138 FBS teams in memory (1,073 checks). There were no crashes.

The remaining failed checks are the known ACC and Big Ten conference-schedule counts. A v4 data update (ACC and Big Ten back to their table-driven schedule style, plus enlarged season-history tables) is now in a multi-season test.

## 2026-10-10 - Real 2026 FBS lineup: 138 teams in 2026 conferences complete a full Dynasty season and rollover (stock build)

All 138 2026 FBS schools now play natively in Dynasty on the stock build: the 125 original schools still in FBS plus 13 additions, in the 2026 conferences. Idaho is out of the Dynasty, with its data preserved for future FCS support. The additions use borrowed presentation from similar donor schools.

A fresh Dynasty passed 118 creation checks and a byte-identical cold reload. It then completed season start, a full CPU-simulated 2013 regular season, conference championship games and bowls (season checks 15/15 at both boundaries). Ohio State 14-0 beat Miami 45-14 for the title, and BCS order matched the media poll (rank correlation 0.999). The rollover to 2014 and a second byte-identical cold reload followed. A live probe passed 563 checks with 138 FBS teams in memory. There were no crashes or hangs.

This took the v3 engine recipe (551 words: active-N count changes, enlarged rating-sort frames, BCS constants scaled with the team count, and a bounded redshirt flag write) plus v3 data. The v3 data clears the 2013 conference membership slots used by the first-season scheduler and removes Idaho from the Dynasty.

Still open: the 17-team ACC gets no conference games and the 18-team Big Ten gets ten (the game's realignment schedule styles do not handle these sizes). Rolling history table TPHS is full, so multi-season play needs it enlarged. The new schools do not appear in the Choose Your First Job list. Graphics are borrowed. Next: conference scheduling, history capacity, combining with the playoff, then the CFBR port.

## 2026-10-10 - Correction: 138-team BCS rankings were wrong; real 2026 lineup plays a full season

Correction to the 138-team entry below: that run completed a season and rollover without crashing, but its BCS rankings were silently wrong. The BCS scorer turns each poll rank into points as 127 minus the rank, using constants stored next to the function. They were never updated for more than 127 teams, so teams ranked 128th or worse wrapped around to huge scores and the worst teams took the top BCS spots (the 2013 title game paired 1-12 Rutgers and 4-9 Eastern Michigan). The 127-team and stock builds are unaffected. A v3 engine recipe (551 words) scales these constants with the team count and is under runtime test.

The real 2026 FBS lineup (125 retained schools plus 13 additions in the 2026 conferences, with Idaho moved out of FBS) has now played a full 2013 season in a fresh Dynasty: season start, regular season, conference championship games and bowls, all checks passing. Two problems were found and root-caused along the way.
- Idaho was kept as a non-FBS team that still had players. Its players overflowed a 138-entry rating cache at season start. Removing its players fixed that.
- A stale conference membership table scheduled 2013 conference lineups. Clearing it fixed the schedules.

The rollover to 2014 then crashed. Idaho, now with no players, was used as a filler opponent; its games produced placeholder player rows that an unbounded write in the redshirt step turned into heap corruption. The v3 data removes Idaho from the Dynasty entirely, and v3 adds a bound check. Still open: the 17-team ACC gets no conference games and the 18-team Big Ten gets ten.

## 2026-10-10 - Native in-game 12-team playoff runs a full season and records the champion (stock build)

A native College Football Playoff now runs inside normal Dynasty play on the stock build (126 teams): no external tools or save editing. A small code hook replaces the stock BCS tie-in filler. At the end of championship week it seeds 12 teams (the five highest-ranked conference champions plus seven at-large, straight seeding by rank). It fills four first-round games (5 vs 12, 6 vs 11, 7 vs 10, 8 vs 9) at bowl sites on Dec 11, and after each round it writes the winners into the fixed bracket: quarterfinals Dec 25 (seeds 1-4 with byes), semifinals Jan 1, then the title game. The bowl calendar and CFP round names come from the Dynasty template's BOWL table.

Three runtime iterations: v0 built a correct field but its BOWL changes went to an archive new Dynasties do not read, so stock dates broke the bracket. v1 moved the data and displayed CFP names and dates and played every round, but the national title was not recorded. The game's history and champion recorders look up a team's first postseason game, which is the quarterfinal for a finalist. v2 makes those two lookups use the game's team pair instead. Final run: fresh Dynasty, CPU-simulated season and every playoff round. Alabama, seeded first, beat Notre Dame 38-17. National title count rose by one with the correct year, and every playoff win was recorded once under its own bowl. The 2014 rollover recreated the CFP rows. All checker boundaries passed, with no crashes. The patch is 510 instruction words and is verified offline by an instruction encoder, Ghidra decoding and emulation with a write-watch.

Known limits: Super Sim of a playoff game crashed once in v0 (cause unconfirmed; stock Super Sim of a bowl game works), so CPU simulation is the tested path. Trophy popup and some news text still name a team's first playoff bowl. Only straight seeding fits. Not yet combined with the 138-team build or ported to CFBR.

## 2026-10-10 - 138 active FBS teams through a full season and rollover (stock build)

For the first time the game ran with 138 active FBS teams: the 126 originals plus 12 placeholder Independents ("Expansion 01-12", Idaho-based copies). The stock-build engine recipe was generalized to a team count N. Of the 127-team recipe's 517 instruction words, 72 depend on N: 126 to N, 125 to N-1, the logical end 1008 to 8N, and one float 1/N. The rest is storage already reserved for 160 teams. A first-season schedule gives all 138 teams 12 games with no collisions, and every original FBS-vs-FBS game keeps its week.

The first 138-team run created and cold-loaded a Dynasty (143 teams; fixture/schedule/stadium checks 90/25/34; live probe 527) but crashed when the season started. Root cause: three team-rating functions (TV Exposure, Pro Potential, Program Tradition) sort teams in stack arrays sized for exactly 126 records. The size appears only as a byte count, so the earlier audit missed it, and 138 records overwrote saved registers. A coach list has the same latent pattern. A v2 recipe adds 19 words that enlarge those frames for 160 teams, following the existing 127-team fix of the same sort. With v2, the same save cold-loaded byte-identical, started the season, and simulated a full 2013 season (Alabama beat Expansion Test 38-14 and finished 14-0), the postseason and the rollover to 2014. The rollover check passed 59/59. All 12 added teams signed recruiting classes (7-15 each), and the live probe passed 546 checks with 138 FBS in memory. Two season-check failures were checker artifacts: a hardcoded user team from the 127-team trial, and a mid-season zero-commitment count for one added team that later signed 10. The rolling history tables are at or near capacity (TPHS 572/572, RBKS 3618/3643) and must be enlarged before multi-season play. Rolled back; preservation checks pass. This proves the engine path at 138 on the stock build only. It does not yet add real 2026 schools, conferences or presentation, and the CFBR build still needs the recipe ported.

## 2026-10-10 - First added team identity survives Dynasty, season and rollover

The first identity added inside the 138-team reserve passed a full ladder at unchanged 126 FBS. BOOT entry 355 gained one team row, TGID 165 "FCS Test", cloned from a shipped generic FCS row, plus three coach rows (36 offline checks). Template 354 was unchanged. A fresh Dynasty contained 132 teams instead of 131, with the new identity exactly once (20 checks). A cold reload left all four save files byte-identical. The Dynasty then simulated the 2013 regular season (28 checks), postseason (28) and rollover to Pre-Season 2014 (30). Grown capacities held at every snapshot (7 checks each), and both live code probes passed. The game's own 2014 schedule generator gave the added team seven games, so the engine treats an added identity as a schedulable team. Two checker expectations were corrected and rerun: Dynasty creation marks every generic FCS row visible (not only the new one), and the season checker now takes the team count from the prior save instead of a fixed 131. Profile rolled back; 48 protected stock files unchanged. No FBS membership change, engine patch or manual save edit. See [roster pipeline](docs/ROSTER_PIPELINE.md).

## 2026-10-10 - CFBR grown Dynasty tables survive a full season and rollover

A coordinated BOOT grew both the Dynasty template (entry 354) and the minimal-reserve roster (entry 355) to TEAM 153, PLAY 9,660, DCHT 12,144, COCH 439, CSKL 414 and STAD 210, still at 126 FBS teams. A fresh offline Dynasty saved with all six grown capacities, and a cold reload left the save files byte-identical (21 checks). The Dynasty then simulated the 2013 regular season (28 checks) and postseason (28 checks), and rolled over to Pre-Season 2014 (30 checks). Capacities never shrank (seven checks per snapshot). Six live reads passed per run. After rollback, 48 protected stock files and 58 original-preservation checks passed. A roster-only BOOT does not grow Dynasty tables; the template must change too. No added identities, code changes or manual save edits. See [roster pipeline](docs/ROSTER_PIPELINE.md).

## 2026-10-10 - CFBR grown roster capacities survive native save and cold load

An isolated capacity-only BOOT trial passed 48 checks at unchanged 126 teams. Only BOOT entry 355 changed, to the minimal 138-team reserve database: TEAM 153, PLAY 9,660, DCHT 12,144, COCH 439, CSKL 414 and STAD 210. Records, schemas and counts were unchanged. In a clean profile, the first boot had no roster auto-load; a roster was saved through File Management. The game's own serializer kept all six grown capacities. A fresh process auto-loaded the roster with all four save files byte-identical. Six baseline live reads passed in each run. After rollback, 48 protected stock files and 58 original-preservation checks passed. No added identities, code changes or manual save edits. This does not prove engine-side team limits, Dynasty creation or seasons with the grown tables. See [roster pipeline](docs/ROSTER_PIPELINE.md).

## 2026-10-09 - CFBR roster source, native save and cold load verified

An isolated source-only BOOT trial passed 32 checks at unchanged 126 teams. The game selected the intended CFBR23V21 database, wrote a roster through its own menus, and auto-loaded it in a fresh process. The complete USR matches the source; all ten tables and all four cold-save files are unchanged. Six baseline live reads passed in each run. Profile rollback completed, 48 stock save files and 58 prior CFBR home files stayed unchanged, and 58 original-preservation checks passed.

Documented a bounded container recognizer (13 checks including nine rejection cases) and a minimal reserve budget (ten offline checks, 78,600 additional bytes). Neither proves changed-container or larger-team acceptance. See [roster pipeline evidence and next gates](docs/ROSTER_PIPELINE.md). No new engine patch, expanded membership or installable release.

## 2026-10-09 - CFBR patched season passed; playable-team integration priority

The four-word ranking patch passed a normal 2014 season, stock postseason, 2015 rollover and separate cold load at 126 teams: checks 28/28/30, six live reads in each run, four unchanged cold-save files, 48 protected stock files and 58 original-preservation checks. The trial is rolled back. Producer execution coverage and expanded CFBR membership remain unproven.

Added an [agent-neutral developer handoff](docs/DEVELOPER_HANDOFF.md). Target 138 active 2026 FBS identities, with Idaho deferred and graphics last. A ten-check input map reconciles the proposed schools and conferences without assigning IDs. An offline auto-loaded-roster leading TDB reserve passes 19 preservation checks; outer save packaging remains open. Static review identified CFBR's twelve-byte recruiting records as a concrete incompatibility with stock eight-byte relocation values.

## 2026-10-09 - CFBR archive adapter and offline reserve candidate

Added a format-aware BGFA library and 16 synthetic tests. It handles stock and CFBR index widths, nested framing, compression, source/preimage checks and append-only entry replacement. All 4,840 entries across four pinned archives match the existing independent parser. A private CFBR candidate passes 34 offline checks while retaining 126 FBS membership and all 825 unrelated BOOT entries. No candidate was installed or runtime-tested. See [archive adapter evidence and limits](docs/ARCHIVE_ADAPTER.md).

The interrupted ranking-season run was no longer active when work resumed. Its save remained at the preserved Week 1 of 2014; all four save files matched. Restored the pending patch/profile configuration, with 48 protected stock save files unchanged and 58 original-preservation checks passing. A completed patched season is still unverified.

## 2026-10-09 - Debugger limitation and recovered trace experiments

Execution coverage remains unverified. RPCS3's LLVM backend rejects PPU breakpoints even though its GDB server replies OK; a separate interpreter experiment also failed to obtain the requested stops. An early-attach trial could not progress beyond title screens and hung during shutdown, requiring the emulator's termination dialog. Restored the working profile and patch configuration; all 48 protected stock save files and 58 original-preservation checks passed. Patched-season validation remains pending.

## 2026-10-09 - CFBR season control and reversible patch

Unmodified CFBR completed the 2013 season and normal rollover into 2014: 28 regular-season checks, 28 postseason checks and 30 rollover checks passed at 126 FBS teams. Ten recruits matched Alabama's next roster; checked championship histories persisted. A separate four-word ranking patch passed install/live-memory/cold-load/rollback checks with unchanged saves. Patched full-season and expanded-membership acceptance remain pending.

## 2026-10-09 - CFBR isolated baseline

Verified the running update 1.02 executable against the analyzed ELF, created a fresh Dynasty and cold-loaded it with all four save files unchanged. Fifteen structural checks passed at 126 FBS teams. Recorded automatic loading of the bundled 2023 roster and a corrected roster-source assumption. Restored profile configuration and verified 48 protected save files plus 58 original-preservation checks. Expansion and playoff integration remain unfinished.

## 2026-10-09 - CFBR integration investigation

Pinned official v21 sources and staged the PC disc package privately. Verified update 1.02 has a different executable (0/517 existing patch preimages match), measured archive changes and confirmed five school-ID conflicts in the bundled roster. Added a separate compatibility track and acceptance gates. No CFBR files published or installed; no new runtime success claimed.

Entries describe the observed test scope. Candidate numbers are development iterations, not public release versions.

## 2026-10-09 - Candidate v6: serialized reserves at 127 active FBS teams

- Enlarged selected serialized capacities while retaining the same 517 executable patch words, initial schedule recipe and 127 active FBS teams. This is not proof of 160 active teams.
- Fresh creation passed 35 checks, exact schedule and stadium checks passed 12 each, and fresh cold reload preserved all four save files.
- Normal simulation completed the regular season, stock postseason and offseason. The prototype finished 1-11 with 13 class commitments. Arizona finished 10-4 and won the Pac-12 championship.
- Normal rollover into 2014 passed 46 saved-system checks, retaining all original teams, complete schedules, roster/depth references, stadium joins, the 17 expected capacity values and the checked championship metadata. Thirteen recruits matched prototype roster identities. The prototype has 11 FBS opponents and one FCS opponent in 2014.
- Cold reload preserved all four files. The depth chart independently confirmed freshman Jake Bracken, TE #86, 6 ft 4 in, 250 lb, OVR 67. Fresh, rollover and cold live probes passed 526 checks each. Lifecycle/preservation passed 39 checks; original preservation passed 58. Trial files were rolled back.
- A separate history audit found missing prototype TPHS/RBKS rows at creation and incomplete record-type coverage after v5 simulation. Their initialization, pruning and capacity limits remain open. These gaps are not covered by the passed championship-metadata checks.
- Full membership, repeated seasons, realistic content, the custom playoff and a public installer remain unfinished.

## 2026-10-09 — Candidate v5: rollover and cold reload

- The same 517-word/BOOT/MISC candidate completed normal offseason simulation into 2014 without save edits.
- Thirty-nine saved-system checks passed: all 132 teams/127 FBS retained, complete schedules without weekly collisions, roster/depth references, unique stadium links, history and serialized reserves.
- Eight recruits matched prototype players on all checked identity fields. A ninth, Caleb Wilson, matched name, hometown, height, weight, tendency and class with a position change from LG to RG. Two other committed recruits on the prototype's board matched players on different teams; board membership plus commitment status does not identify the destination team.
- The prototype has 11 FBS opponents and one FCS opponent in 2014.
- Cold reload passed five checks with all four files unchanged. The in-game depth chart confirmed Blake Vogel, freshman TE #87, 6 ft 6 in, 265 lb, OVR 64.
- Both live probes passed 526 checks; aggregate lifecycle/preservation passed 35; original preservation passed 58. All four trial files were rolled back.
- Repeated seasons, full-FBS capacities/content, coach selection and the custom playoff remain open. No installable release.

## 2026-10-09 — Candidate v5: initial FBS schedule experiment

- Traced first-year known matchups to SKNW in a packaged schedule database. All 726 season-zero presets exactly matched both captured stock and expanded 2013 schedules. The added team had no preset entries. Later seasons also contain presets, in smaller numbers.
- Prepared a reversible MISC asset recipe replacing 12 FCS matchup slots with 12 distinct FBS opponents for the prototype. Balanced its venues at six home/six away. Moved one matchup into the original opponent's open week because two constrained weeks otherwise required the same opponent.
- Kept the 517 executable patch words and unique-stadium BOOT candidate from v4 unchanged. Original FBS-versus-FBS matchups and weeks are preserved.
- Passed 21 offline asset/projection checks, 28 fresh-Dynasty structural checks, 12 exact-schedule checks, 12 stadium checks and five cold-load/preservation checks.
- Normal simulation completed the regular season and stock postseason. The prototype finished 0–12 with nine recruiting commitments and saved team statistics. Arizona finished 9–4. Fresh and completed-season live probes each passed 526 executable/index checks.
- At this checkpoint rollover was pending. Trial files were rolled back after preserving the end-season fixture; the later rollover result appears above.
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
