# Changelog

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
