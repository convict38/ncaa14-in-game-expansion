# FBS + FCS universe: engineering plan (about 266 rostered teams in one Dynasty)

Date 2026-10-29. Supersedes the "rosterless sim-only FCS" recommendation (design D2) of `fcs-league-feasibility.md`. That study's facts and limits table are the starting point here. Its conclusion is replaced, because the target is the PC port, where the executable, the runtime, the memory map and save HLE are all ours.

Target: CFBR v21 + real2026 (138 FBS) + 12-team CFP, PC port `tools/ps3recomp-lane-e`. Addresses are CFBR v21 (01.02) unless marked "stock". Function names are ours. Confidence tags: confirmed / likely / guess.

Evidence for this pass (all static; no game was launched):
- **LIFT:** the lifted C, `ps3recomp/src/recomp/ppu_recomp_*.cpp` (104,750 functions, lifted from the modded CFBR ELF).
  - Scanned with `scripts/scan_team_width_lifted.py`.
  - Outputs: `analysis/fcs-universe/width-scan.json`, `u8-increment-sites.json`, `u8-loop-sites.json`.
- **ELF:** the pinned CFBR ELF `third-party/cfbr-v21/extracted/entry-0024-EBOOT.elf` (sha256 144dee90...).
  - Word-level scans.
  - All 97 TTYP query strings, with their owner functions: `analysis/fcs-universe/ttyp-queries.json`, `ttyp-owners.txt`.
- **SAVE:** read-only parse of `save_backup/20261029-bowl-endseason` USR-DATA.
  - Schema widths: `analysis/fcs-universe/save-schema-endseason.json`.
  - Capacity model: `capacity-model.json`.
- **HLE:** `ps3recomp/libs/system/cellSaveData.c` and `runtime/syscalls/sys_memory.c`, plus a boot log (`runs/input-keysB2/stderr.log`) for the guest heap layout.

## 0. Summary

**Architecture: "one DB, one roster universe, two leagues".**
- FCS schools become ordinary TEAM rows with full rosters, depth charts, coaches and stadiums:
  - TTYP 1;
  - conferences with LGID 1;
  - TGIDs in the free 236-609 range, except 300 and 400 (reserved; section 3.3).
- They stay in the same TDB, the same Dynasty and the same save.
- The engine's **active team set** (the "FBS index" that recruiting, coaching, progression, depth charts and team rankings iterate) is widened from `TTYP = 0` to `TTYP <= 1`.
  - That is three query strings in `league_index_fill` / `league_index_init`.
  - Every roster-level system then runs for FCS automatically.
- Every **league-scoped** query keeps its `TTYP = ?` binding of 0, so polls, BCS, bowls, the CFP and FBS All-Americans stay FBS-only for free.
- The FCS versions of those passes run by calling the same stock pass a second time with TTYP bound to 1, from a small C cave at the call site.
- Ranks are per league (138 and 128), so no ranked list exceeds 255.

| Wall | Chosen fix | Size of the change |
|---|---|---|
| 8-bit indexes / loops (255) | Counts are already u16. 11 team-count loops use an 8-bit counter; widen each clrlwi 24 to 16 | 11 words, **staged** (`patches/fcs-universe-p0/u8-loops-v0`) |
| u8 ranks TCRK/TMRK/TBRK | Per-league ranks (max 138 / 128). FCS poll = stock poll pass called with TTYP 1. 6 rank queries without a TTYP filter get `and TTYP = 0` | 6 string repoints + 1 cave |
| 160-team storage reserve | activeN v4: RESERVE 288 and N = active count; arrays move to a runtime-provided mod arena | builder change + about 72 regenerated words |
| Save 8,278,016 B | 17 `lis rX,0x7e` sites are the whole save size: 0x7E5000 -> 0xFE5000 (16.67 MB). The HLE has no size cap | 17 words, **staged** (`patches/fcs-universe-p0/save-grow-v0`) |
| SGNM 127 sentinel (127 games/week) | The FCS scheduler caps every week at 126 games across both leagues. FBS peak is 72; FCS averages 54 | constraint in the schedule cave; no widening |
| PGID // 70 (936 teams), TGID 10 b | Not walls: FCS TGIDs 236-399 give PGIDs up to 27,999 | none |
| CGID 5 b (31) | 11 FBS + 13-14 FCS + 4 legacy rows = 28-29 ids | CONF capacity 26 -> 32 |
| Table capacities | Template raises from the capacity model (section 2.4). Every table stays under the u16 row cap (65,535) | template edit (existing tools) |
| Memory | The game takes 208 MB in 25 fixed blocks. The runtime window 0x40000000-0x50000000 is ours: add a mod arena and grow the DB heap | runtime constant + 1 heap constant (Phase 0 locates it) |
| Sim time | Measure, then accelerate the hot TDB cursor scans natively in the runtime | Phase 7 |
| UI | League toggle on stock Top 25 / standings / team pickers (binding TTYP or LGID 1); FCS bracket page via the UI pipeline | Phase 6 |

**Phase 0 result (offline, first session):** two code patches are staged with preimage gates against the pinned ELF. Both are rebuildable and refuse to overwrite a differing output. Builder: `scripts/build_fcs_universe_p0.py`. Results: `patches/fcs-universe-p0/checks.json` (all 29 checks pass).

**Phase 0 runtime result (2026-10-29 22:53-23:25, one GRANT, separate exe; details in section 3.1): T0.1 PASS, T0.2 PASS (tight), T0.3 PASS with findings.**
- A new Dynasty saves a 16,666,624-byte USR-DATA (HED-DATA[0] = 0xFE52E8) and reloads, before and after a simulated week.
- The save buffer is not in a game heap. It sits in a transient 16 MB block that the game takes from memory container 1 for every save and load. At S = 0xFE5000 that block has 107,200 bytes to spare, so S cannot grow further without the fallback.
- A TGID-300 rostered TTYP-1 team enters the active index (count 139, then 144 once Dynasty creation makes the 5 generic FCS rows visible), survives a week and a reload, and its players get the weekly player update. Dynasty creation strips its coaches and depth chart.

**Effort:** about 50-80 agent-days (10-16 weeks) to a complete, validated universe. Section 4 has the breakdown.

## 1. Architecture

### 1.1 Team identity and data

| Item | FBS (today) | FCS (new) |
|---|---|---|
| TEAM.TTYP | 0 | 1 (the engine's own FCS type) |
| League | CONF.LGID 0 "1A" | CONF.LGID 1 "FCS" (LEAG row exists) |
| TGID / TOID | 0-235 (sparse) | 236-399 (free; high-school rows 610-619 and STTM placeholders 630-806 stay clear). TOID = TGID (the CCG gate needs it) |
| TORD (sort order, 10 b) | 0-137 | 138-265, so FBS sorts first and the FBS prefix of the active index stays contiguous |
| Players | PGID = TGID*70 + slot | same rule; PGID max 399*70+69 = 27,999 (u16 OK) |
| Coaches / stadium | COCH 3 per team, own SGID | same; SGID 241+ (10 b, 1023 sentinel) |
| TCRK/TMRK/TBRK | 1..138 | TCRK/TMRK 1..128 (FCS polls); TBRK stays 0 (no BCS) |

The 5 generic FCS rows (TGID 160-164) are retired: real FCS teams take their place as FBS non-conference opponents.

### 1.2 Active set = TTYP <= 1

- `league_index_init` 0x474260 counts, and `league_index_fill` 0x473df8 fills, the "FBS" list.
- The queries are:
  - 0x176d714 `TEAM where TGID <= ? and TVIS = ? and TTYP = ? order by TORD`;
  - 0x176d784 (the same without TVIS);
  - 0x176d81c `count(*) ... TTYP = ?`.
- They feed the FBS index/count globals 0x1c8691c / **0x1c86922 (u16)**. Changing `TTYP = ?` to `TTYP <= ?`, and binding 1, makes the index FBS (TORD 0-137) followed by FCS (138-265). This needs new strings in code room and 2 words per string to repoint lis/addi.
- **Binding sites (confirmed, decompile `f474260.c`):**
  - The active count is `0x176d81c` bound as `(TGID <= 0x3ee, TTYP = 0)`, a literal 0 argument in `league_index_init` 0x474260. One `li` word changes to 1.
  - The list fill is `league_index_fill` 0x473df8(TVIS flag), which binds TTYP for 0x176d714/0x176d784. Its `li` site is read in the next batch.
  - The all-team count is `0x176d7e4` (`TGID <= 0x3ee`, no TTYP).
- **Both index arrays are heap-allocated by count:** (count + 4) x 12 + 8 bytes from the `COMMON_LEAGUE_MANAGEMENT_MODULE` allocator. So the index itself scales to 266+ with no reserve. Only its consumers' fixed arrays need the 288 reserve.
- Every consumer of that index that is roster-level then covers FCS:
  - RecruitMan and its boards and preferences;
  - pitches, TV exposure and pro potential;
  - redshirts and transfers;
  - coach contracts and the carousel;
  - ranking record fill.
- **A second count is needed for FBS-only index consumers.** These are code that iterates the FBS index and computes 1A-only results, for example `bcs_rank_function` 0x4cbab0 (N+1 pool, f32(1/N)) and the coach-rank clamp.
  - A new mod global `N_1A` (138) holds the FBS prefix length.
  - The active count stays in 0x1c86922.
  - Classifying the 115 index/count consumer functions (`width-scan.json`: 76 FBS-count, 52 FBS-index, 46 all-count, 45 all-index reads) into "league-wide" and "1A-only" is a Phase 1 work item. 1A-only sites get their count load repointed to `N_1A`.

### 1.3 League-scoped passes (TTYP stays bound to 0)

From `ttyp-owners.txt` (owner function per query string). These keep FBS-only behaviour unchanged, and FCS gets a second call with TTYP 1 where it needs one:

| Pass | Owner | FBS (TTYP 0) | FCS second call (TTYP 1) |
|---|---|---|---|
| Coaches/media polls | `polls_update_coaches_media` 0x4cee28 (0x17794a8, 0x1779630) | unchanged | **yes**: FCS Top 25 into FCS TCRK/TMRK |
| Overall ranking cursor | `teams_by_overall_cursor` 0x4ce508 | unchanged | yes |
| BCS | `bcs_rank_function` 0x4cbab0 (0x16e7cd0) | unchanged; must use `N_1A` for its index loop | **no** (TBRK 0 for FCS) |
| Bowl / CFP candidates | 0x45aec8, 0x45cd38; CFP cave v3 | unchanged | no; the FCS playoff cave (Phase 5) |
| All-Americans | AAPL 0x2d8240 / 0x4a54b8 (literal `TTYP = 0`), 0x456dc0, 0x45740c, 0x45566c | unchanged | optional (FCS All-America) |
| Story/news by rank | `story_MCOV_builder` 0x4aa650 | unchanged | optional |
| SuperSim normalisation | 0x12f7d0 `max/min(TROV) where TTYP = 0` | unchanged | none: FCS TROV is normalised against the FBS range, as for today's generic FCS |
| Schedule generator | RemainingGenerator 0x102f00, `fcs_opponent_pick` 0x10265c | unchanged | FCS draws become real FCS teams; FCS-only games come from the schedule cave |

Queries in roster-level owners that bind TTYP and must **include** FCS:
- 0x4810a0 (transfer requests), 0x484508, 0x493928 (next to the training pass 0x4934c8), 0x47c190, 0x4ea13c / 0x4ea520, 0x4cb680, 0x4f9018, 0x4f2480;
- the coach carousel 0x4d28a8 (`TTYP != ?`, `max(TORD) where TTYP != ?`, `LEAG ... TTYP = ? order by TDNA`).

Each one is checked in Phase 1 (decompile batch queued, see 5) and either rebound to "<= 1" or given a second call. Dynasty creation runs `dynasty_create_nonfbs_coach_cleanup` 0x4f5be8. The decompile (`analysis/mapping-cfbr-fcs-universe/f4f5be8.c`, 2026-10-30) shows it binds **TTYP 2, 3, 4** (query 0x178a5e8, or 0x178a560 when the hook at `*0x1c85dbc` returns nonzero), then deletes those teams' coaches with 0x178a688. **TTYP 1 is not in the list**, so this function does not strip FCS coaches. The study's "FCS coaches moved to TGID 1023" happens elsewhere, or because the roster file has none (likely the latter: it ships 0 FCS coaches). T0.3 confirms that coaches given to a TTYP-1 team in the roster survive Dynasty creation.

### 1.4 Runtime services (PC port only)

- **Mod arena.** A guest VA range served by the runtime, outside the game's sys_memory window (for example 0x50000000-0x57FFFFFF), committed on demand like the existing window. It holds:
  - the relocated 288-entry reserves;
  - cave state;
  - optionally the save buffer (1.4 fallback).
- **Save HLE.** No change needed for size. Optional extras:
  - transparent compression of USR-DATA on disk (the file is a TDB plus zero padding; the game always sees raw bytes);
  - a per-slot sidecar for any cave-owned history that should not live in the TDB.
- **Native TDB acceleration** (Phase 7). Hot cursor scans are replaced by host C with the same results, indexed by TGID/PGID.

### 1.5 Why not the other designs

| Option | Why not chosen |
|---|---|
| Separate FCS id space through a translation layer | Every DB table already keys teams by 10-bit TGID, and 236-609 is free. A translation layer would have to intercept every TDB access and cursor. That is far more code than 3 strings |
| Two league contexts that swap RecruitMan / ranking state | RecruitMan, PrefMan and board pools are singletons with mid-season state, so swapping needs duplicated objects and their initialisation. It also splits the recruit pool, which real recruiting does not do. Kept only as the fallback for recruiting if one national market behaves badly |
| FCS as TTYP 0 (the study's D4/D4b) | Every FBS-only query (polls, BCS, bowls, CFP, AAPL, overall ranks) would need a league filter, and the single poll would rank 266 teams into u8 fields |
| Widen schema fields (TCRK, SGNM, TGID) | The schema accepts it, but code holds sentinels (127, 1023), `stb` stores and 0x3ff compares. Not needed under the per-league design |

## 2. Limits: site lists and fixes

### 2.1 8-bit team indexes, loops and ranks

**Counts and indexes.** The four globals are read 270 times in 115 lifted functions:
- 0x1c86918 all-team index pointer;
- 0x1c8691c FBS/active index pointer;
- 0x1c86920 all-team count, `lhz`;
- 0x1c86922 FBS/active count, `lhz`.

Counts are 16-bit everywhere (confirmed, LIFT), so they are not the 255 wall.

**8-bit loop counters.** Method: `addic/addi r,r,1` followed by `clrlwi r,r,24`. The scan finds this idiom in 716 lifted functions overall. 17 of them are index/count consumers, with 21 sites (`u8-loop-sites.json`, confirmed):

| Site | Function | Bound | Action |
|---|---|---|---|
| 0x4ac72c | 0x4ac5c0 (reads FBS+all count) | count register | widen (all-team count reaches 271) |
| 0x4b0c00 | 0x4b0ac8 | count register | widen |
| 0x4babe8 | 0x4bab40 | count register | widen |
| 0x4bef88 | 0x4bee10 | count register | widen |
| 0x4b9038 | `recruitman_loop_f05_f07` 0x4b8f40 (stock 0x4b7970) | 126 -> N literal | widen |
| 0x4edfec | `ranking_record_fill` 0x4edf10 | count register | widen |
| 0x4ee014, 0x4ee05c, 0x4ee09c, 0x4ee0e4 | 0x4edf10 | 126 -> N literal | widen |
| 0x504de0 | 0x504cb0 | count register | widen |
| 0x4ae0f0 | 0x4adeb0 | flag loop (`cmpwi r3,0`) | review in Phase 1 |
| 0x4c0f5c | 0x4c0ed4 | no compare follows | review in Phase 1 |
| 0x4b7bfc, 0x4b942c, 0x4b9694, 0x4c19a8, 0x4c2c24, 0x4ff284, 0x50c1cc, 0x50cba0 | various | constants 10, 17 or 7 | leave |

The 11 "widen" words are staged as `u8-loops-v0`: `rlwinm` MB 24 -> 16, which has no effect while counts are at most 255.

The scan's coverage limit:
- It only sees functions that touch the globals directly.
- Loops over a copied count, such as RecruitMan's internal arrays or the cached count in an object, need the Phase 1 extended scan. That scan follows `lhz` of 0x1c86922 into stack and object stores, and also checks `cmplwi/cmpwi 255/256`. The whole program has 267 functions with such a bound on a back edge; they are triaged against the team-index set.

**Byte fields holding a team index.** The activeN audit (stock) found no team-index `extsb`. In the CFBR scan, the RecruitMan functions 0x4c11e0 (42 byte ops) and 0x4c23e0 (34) carry the most byte loads and stores. Their records are reviewed for a stored dense team index in Phase 1. If one exists, the record grows from u8 to u16 the same way activeN grew CFBR's first array from 8 to 12 bytes (`build_cfbr_activeN_patch.py` RECRUIT/FIRST12 layout rules).

**Ranks (u8 TCRK/TMRK/TBRK).**
- Per-league ranking keeps every list at 138 or fewer.
- Rank queries without a TTYP filter would see FBS #1 and FCS #1 together. These are the study's list:
  - 0x1feb08 `TGID where TCRK = ?`;
  - 0x45b590 `TGID where TBRK = ?`;
  - 0x478a24 `TDNA where TBRK = ?`;
  - 0x2d9230 `TCRK <= 25`;
  - 0x4a4ddc `TCRK <= 10`;
  - the polls UI at 0x1f2e24.
- Each gets a repointed string with `and TTYP = 0`, or a league toggle where it is a UI list (Phase 6).
- The TBRK sites are safe anyway, because FCS TBRK is never written (BCS uses `N_1A`).

**Schema widths (SAVE, confirmed).**

| Field | Width | Notes |
|---|---|---|
| TGID / TOID / OGID / GHTG / GATG | 10 b (60, 5, 2, 5 and 5 tables) | 1023 = empty, so 266 teams fit |
| SGID | 10 b | 10 tables |
| TORD | 10 b | |
| PGID | 16 b | 71 tables |
| CCID | 16 b | |
| CGID / DGID | 5 b | 11 / 3 tables |
| SGNM | 8 b | 30 tables; 127 sentinel |
| SEWN | 5 b | |
| LGID | 16 b | |
| TTYP | 5 b | |
| Ranks | 8 b | |
| Table row count | u16 | |

No field widening is required by this design.

**The 160 storage reserve.**
- activeN (`build_cfbr_activeN_patch.py`, N 126..160) sizes every per-team engine array for 160.
- v4 changes:
  - RESERVE 288 (266 active plus spares);
  - N = the active count;
  - the relocated arrays move into the mod arena. Examples: RecruitMan 288 x 12 and 288 x 376, PrefMan 288 x 24 / 288 x 76, the board pool 288 x 35 = 10,080 nodes, and the ranking/sort frames 0x4b1f3c-style (`active138-crash-rca.md`).
- Stack frames grow by N x record. On the PC port guest stacks are ours: the CMake target reserves 256 MB.
- The 72 N-dependent words are regenerated by formula (126 -> N, 125 -> N-1, 1008 -> 8N, f32(1/N)) and split between N_active and N_1A per the 1.2 classification.
- Unreviewed literals (stock count) are 107 `126`, 63 `125` and 528 `127` immediates. These are audited by the extended lifted-C scan, which keeps only those in functions that reach the team globals or TEAM queries.

### 2.2 Save size (8,278,016 bytes)

**Where it is fixed** (confirmed, ELF + LIFT): only in the game. The whole executable text has exactly 17 `lis rX,0x7e` instructions:

| Function | Sites | Values |
|---|---|---|
| Dynasty load 0x335738 | 0x335760, 0x335784, 0x3357a8, 0x3357e4, 0x3357f8, 0x33581c, 0x335894 | S+0x260 allocation, memset, read and copy sizes; S = FNV-1 verify length (prime 0x01000193, basis 0x811C9DC5); S+8 = buffer end |
| Dynasty save 0x336148 (lifted entry alias 0x336164) | 0x33618c, 0x3361c0, 0x336230, 0x336254, 0x33625c, 0x3362d8, 0x336310, 0x336354, 0x336368 | allocation; serialize capacity to 0x3b4dbc; payload S; FNV-1 length; write size to 0x3b4c6c |
| Save-slot descriptor ctor 0x3b0c7c | 0x3b0cb0 | {0x5B, USR-DATA S, HED-DATA 0x2E8}; HED-DATA[0] on disk = 0x7E52E8 = S + 0x2E8 (confirmed on the endseason save) |

- Every site pairs `lis 0x7e` with `ori 0x5000 / 0x5008 / 0x5260`. Changing only the lis immediate moves S, S+8, S+0x260 and S+0x2E8 together.
- **Staged:** S = 0xFE5000 (16,666,624 B), `--hi` selectable. The lis immediate must stay at most 0x7FFF.

**The HLE does not cap it** (confirmed, HLE). `process_file_op` in `cellSaveData.c` writes `min(fileSize, fileBufSize)` bytes and reads the same. The stat callback sizeKB is informational, and the HLE ignores free space.

**Buffer storage class** (closes MODDING_REFERENCE gap 5.23; corrected by the Phase 0 runtime test):
- Static reading: 0x335738 and 0x336164 get the allocator from the singleton `*0x1C829C8` (getter 0x3f2240), select a sub-heap via 0x3f3790, and call its vtable allocate with S+0x260.
- **Runtime (T0.2, confirmed):** neither function ran during Dynasty creation, a menu save or a Dynasty load. Diagnostic probes after both vtable allocations never fired.
  - The buffer the save utility receives is at guest 0x4A100D40 (USR-DATA) and 0x4A100A40 (HED-DATA), with fileBufSize = 16,666,624.
  - That address lies in a 16 MB block (0x4A100000-0x4B100000) that the game takes with `sys_memory_allocate_from_container(0x1000000, cid 1)` around every save and load and frees afterwards.
  - The USR-DATA buffer ends at 0x4B0E5D40, leaving **0x1A2C0 = 107,200 bytes** in that block. The stock 8.27 MB save used half of it.
  - The 17 `lis` words still set the size: the slot descriptor (0x3b0cb0) and the serialiser that actually runs read them. The file is 16,666,624 bytes and the payload hash verifies on reload.
- So S = 0xFE5000 is the largest size that fits without more work. The 25 MB option (0x17E5000) needs one of these:
  1. a larger container request (the 0x1000000 constant and the container size); or
  2. the fallback: the container-backed buffer is replaced by a mod-arena allocation in the runtime.
- Locating the caller that requests the 16 MB block (and the serialiser that really runs) is a Phase 1 item. The old fallback note (a cave over the two vtable calls) does not apply, because those calls are not on the live path.

**Old saves.** An 8,278,016-byte file is shorter than the new fileSize. The game would read it partially, and its FNV check would most likely fail (likely; not yet observed). The universe needs a new Dynasty anyway (template capacities are fixed per save), so this matters only for keeping the user's current saves alive. Option: a migration tool (zero-pad USR-DATA to S, update HED-DATA[0], recompute the hash) once Phase 0 pins the hashed byte range.

**Budget:**
- Capacity model (2.4): the in-season DB is about 10.1 MB (+3.15 MB over the 7.03 MB bowl-week save).
- Offseason compact tables (RCTN, POCH, scaled to 266 teams) can add about 1-2.7 MB at their peak.
- So S = 16.67 MB leaves about 4 MB or more of headroom. If a 5-season soak shows growth, use 0x17E5000 (25.1 MB).

### 2.3 SGNM 127 (games per week)

- SGNM is 8 b, but 127 is the "no game" sentinel (TSCH byes, unassigned BOWL rows), so a week holds SGNM 0..126.
- Demand per week:
  - FBS is 54-72 games, 72 in week 1, including FBS-vs-FCS;
  - FCS-only regular season is about 128 x 11 / 2 = 704 games, minus about 100 FBS-vs-FCS games already counted, over 13 weeks, so about 46-54 per week.
- The fix is a constraint in the FCS schedule cave (Phase 3): total SCHD rows per SEWN at most 126.
  - Where week 1 is heavy, FCS teams get their bye there.
  - The FCS playoff uses a reserved SGNM range (100-126) in each postseason week, disjoint from BOWL SGNMs.
- Widening SGNM would mean auditing about 584 `127` literals for the sentinel role. That is not needed.

### 2.4 Other ids and table capacities

- **PGID // 70:** 936 team slots. FCS uses TGID up to 399, so this is not hit.
- **CGID 5 b:**
  - 2026 FBS has 11 ids: ACC, Big Ten, Big 12, SEC, American, C-USA, MAC, Mountain West, Sun Belt, Pac-12 and Independents (CGID 5, with special gates).
  - 2026 FCS has 13-14: Big Sky, CAA, MVFC, SoCon, Southland, Big South-OVC, Patriot, Ivy, Pioneer, NEC, MEAC, SWAC, UAC, plus FCS Independents.
  - The rows Historic 15, Fantasy 16, Generic 17 and High School 24 stay. WAC 14 is reused.
  - About 29-30 ids of 32: it fits. The nine existing LGID-1 rows (6, 8, 12, 18-23) are renamed, and the rest go to 25-31.
- **The conference generator** (CGID 0..13 loop, `cmpwi 14` at 0x100618 / 0x1006f4) is not used for FCS: the schedule cave owns FCS.

**Template capacities** (`capacity-model.json`): the endseason save scaled by teams x1.93 and games x1.79, with 15% margin. A new Dynasty is required.

| Table | Used / cap now | New cap | +bytes |
|---|---|---|---|
| PLAY | 9522 / 12600 | 21108 | 1,020,960 |
| BOFF | 16415 / 16896 | 36387 | 545,748 |
| BDEF | 26640 / 27028 | 59052 (u16 limit 65,535: watch) | 512,384 |
| MCOV | 1104 / 1280 | 2448 | 158,848 |
| BSCS | 7637 / 8706 | 15678 | 139,440 |
| DCHT | 12144 / 14080 | 26920 | 102,720 |
| BOLN | 9178 / 9178 (full) | 20345 | 89,336 |
| BKIC, PLAC, RECB, PINT, BTES, BKPR | | x1.9 | 370,000 total |
| TEAM | 143 / 192 | 317 | 41,000 |
| COCH / CSKL / CPRF | 439 / 768 | 974 / 920 / 920 | 42,000 |
| TSCH | 2268 / 2268 (full) | 5852 (266 x 22) | 28,700 |
| STTM | 320 / 400 | 710 | 4,960 |
| RTPB / RCTC / TEXP / TSSE / PTIP | 160 | 288 (= RESERVE) / PTIP 4283 | 22,000 |
| SCHD | 926 / 2048 | 2560 | 10,240 |
| STAD | 210 / 240 | 384 | 66,816 |
| CONF / DIVI | 25/26, 22/22 | 32 / 24 | small |
| Compact (stored only when used): RCTN 8820, POCH 13230, CLST 13230 | | 18620 / 27930 / 27930 | at offseason peak |

The tools are the existing `scripts/tdb_capacity.py grow_capacity` and `bgfa_archive.replace_entries` (BOOT 354, dyn60 precedent). Mirror them into the MISC 145 copy if a new Dynasty still shows old caps (`table-capacity-check.md` 5).

### 2.5 Memory

- **Facts (confirmed, boot log):** the game makes 25 `sys_memory_allocate` calls, totalling 208.3 MB, in the runtime window 0x40000000-0x50000000 (`SYS_MEM_ALLOC_BASE/END`). For example 0x2720000, 0x1720000 and 0x1260000 B, plus three 16 MB container blocks.
  - Syscall 352 reports 256 MB total / 192 MB available.
  - The guest heaps are fixed-size game partitions.
- **Needs:**
  - live DB about +3.2 MB in season (more at the offseason peak);
  - the transient save buffer +8.4 MB;
  - the reserves (about 0.3 MB).
- **Fix:**
  1. Phase 0 logs which sys_memory block holds the allocator singleton's Dynasty sub-heap. It is a diagnostic-only probe in the lifted 0x335738 return path, or a watch on the vtable allocate.
  2. Raise that heap's constant in the game's memory config, and raise `SYS_MEM_ALLOC_END` (runtime) to give it VA.
  3. Put the reserves and cave state in the mod arena.
  4. If the heap cannot grow cleanly, route the save buffer to the mod arena (2.2 fallback).

### 2.6 Sim time

- **Today:** a CPU-simmed regular-season week takes 140-241 s, typically about 205 s, for about 62 games on the PC port (`fast-drive.md`).
- **With the universe:** about 120 games per week, and player-keyed tables about 2x larger. TDB queries are cursor scans, so per-query cost grows with table size.
- **Estimate:** 2x to 3.5x, so about 7-12 minutes per week, unless optimised.
- **Plan (Phase 7):**
  1. Profile with the existing `prof40` / `sample_sym.py` tooling on a universe Dynasty.
  2. Replace the hottest TDB cursor and lookup functions with native host implementations (same row order and results, indexed by TGID/PGID; A/B checked by DB dumps).
  3. Make the remaining per-team passes (recruiting AI) cheaper with the speed bundle, already default.
  4. Optional user setting "FCS quick results": FCS-vs-FCS games use the engine's quick path.
- **Target:** at most 1.5x today's week time.

### 2.7 UI

| Screen | Today | Risk with more than 255 teams | Fix |
|---|---|---|---|
| Team pickers (Dynasty start, team select) | `ui_team_list_by_type_visible` 0x215008 / `_by_type_name` 0x1a36bc bind TTYP 0 | lists never exceed 138 per league; FCS not listed | league toggle that binds TTYP 1. Check the list-widget capacity with a 128-row probe |
| "Choose Your First Job" | literal 126 rows | FCS jobs absent | rebind to TTYP <= 1 with N rows (coach mode) |
| Conference pickers / standings | 0x196000, 0x196500, 0x197028, 0x1ab17c bind LGID 0 | none | LGID toggle; FCS conferences appear with stock standings |
| Top 25 / polls | polls UI 0x1f2e24, TCRK-ordered TTYP lists | FBS and FCS #1 mixed if unfiltered | FCS ranks are stored per league, so the stock poll page with TTYP 1 *is* the FCS Top 25. Toggle on the same page |
| Rank filters | 0x1e1660 (TCRK 126), 0x1e2ca0 (STDR 126), 0x1e1018 | ranks 127-138 hidden at 138 FBS already | 126 -> N_1A (or 255) |
| Weekly scores | all SCHD rows of the week | about 120 rows | probe list capacity; add a league filter if needed |
| Recruiting boards / "schools interested" | TGID-keyed | none (names resolve by TGID) | verify FCS names and logos |
| CFP bracket page (TU-L, `docs/ui/cfp-page.md`) | 12 teams | n/a | FCS bracket = new layout (24 teams, 5 rounds) in the same APT pipeline, fed by the FCS playoff cave's SCHD rows |

The UI page pipeline (`docs/ui/UI_SYSTEM.md`, `docs/modding/07-in-game-ui-pages.md`) already ships Play_PC pages (variant TU-L). The FCS pages reuse it.

### 2.8 Data sourcing

- **Teams and conferences (2026):** public conference membership lists; the method is `fbs-2026-alignment-research-2026-10-09.md`. There are about 128 teams in 13-14 conferences. Already-FBS moves (Sacramento State, Missouri State, Delaware, Kennesaw State and others in the 138) are excluded.
- **Ratings tiers:** from public results (last 3 seasons' FCS playoff seeds and standings). Top FCS sits just under the G5 floor (TROV 60-66); the bottom is 40-50.
- **Rosters:** generated offline per team by a Python generator using the game's own distributions.
  - It draws position counts from FBS depth-chart shapes, ratings from tier-scaled FBS distributions, and names and hometowns from the game's name pools and state links (`docs/mapping/recruiting.md` 7-9).
  - It writes PLAY / DCHT rows into the roster DB (BOOT 355) with the active138 builder pattern (`build_roster138_proto.py`).
  - Real rosters from community packs replace generated ones team by team where available.
- **Coaches:** 3 per team, generated (CCID 16 b, fits). The real head coach name where it is public.
- **Stadiums:** one STAD row per FCS home, mapped to the closest-capacity existing stadium model (SUID). Shared generic models are allowed.
- **Uniforms and logos:** the game's generic FCS sets first (`GetIsTeam1AA` path). Community packs per `community-assets-policy`.
  - A credits list is kept in `mod-work/third-party/CREDITS-fcs.md`.
  - Nothing EA-derived goes to the public repo.
  - Art pipeline: `graphics-asset-pipeline.md`, `team-art-plan.md`.

## 3. Phased plan

Each milestone runs on save copies in an isolated folder through the run queue (`harness/RUNQUEUE.md`), never play_e or cwd_e. Each has its own exit test.

| Phase | Content | Exit test (validation) | Agent-days |
|---|---|---|---|
| **0** | Offline (done): `save-grow-v0`, `u8-loops-v0`, scans, capacity model. Runtime: (T0.1) build a stage with save-grow-v0; new Dynasty; save; reload. (T0.2) heap probe: log the Dynasty sub-heap block and its free space at save time. (T0.3) one TGID-300 team (TTYP 1, 70 players, coaches, stadium) in a test roster with the 3 `TTYP <= ?` strings; new Dynasty; sim 1 week; save; reload | T0.1: USR-DATA is 16,666,624 B and HED-DATA[0] is 0xFE52E8; it reloads; a second save is byte-stable apart from the hash and time. T0.2: block id and free MB recorded. T0.3: TGID 300 in the active index (count 139); its players progress and get stats; it survives save/reload and one week. CFP pool unchanged | 3-5 |
| 1 | Engine core: activeN v4 (RESERVE 288, mod arena) and the `N_1A` global; classify the 115 index consumers; patch 1A-only sites; widen the remaining u8 records; coach-cleanup TTYP list; 6 rank-query repoints; extended lifted-C scan of literals | 266-team synthetic Dynasty (generated FCS) boots, sims 2 weeks, saves and reloads. No crash; recruiting boards hold FCS teams; BCS/CFP pools are byte-identical to an FBS-only control on the same seed | 10-15 |
| 2 | Data pack: 2026 FCS teams, conferences (CGID map), generated rosters, coaches, stadiums, ratings tiers; template capacities (2.4); offline checker | checker passes (ids, PGID rule, capacities, STAD links, TORD order); new Dynasty creates with 266+ TEAM rows, players and coaches intact | 6-9 |
| 3 | FCS schedule cave (conference round robin or rotation, non-conference fill to 11-12 games, home/away, at most 126 per week, rollover); real FCS opponents for FBS via `fcs_opponent_pick` weighting | offline model and in-game season: every FCS team 11-12 games, every week at most 126 games, FBS schedules unchanged except for opponent identities; 2 seasons | 4-6 |
| 4 | Season systems: FCS polls (second call), FCS overall ranks, standings for LGID 1, FCS awards (optional), recruiting with one national market (class sizes, star distribution by level), coach carousel across levels, transfers | 1 full season and rollover: FCS Top 25 sane; FBS recruiting class quality within ±5% of the FBS-only control; FCS classes mostly 1-2 star; no table at 100% | 6-10 |
| 5 | FCS playoff cave: 24 teams (10 auto bids + 14 at-large, top 8 byes, 5 rounds, 23 games), SGNM 100-126, recorder guard (no false CCHH/BCHH), champion news, history (sidecar or TDB table) | bracket completes in 2 seasons; champion recorded; FBS CFP and bowls unaffected | 4-7 |
| 6 | UI: league toggles (team pickers, standings, Top 25), rank filters, FCS bracket page, weekly-scores filter | all screens show live FCS data on a universe save; no list truncation; screenshots compared | 10-18 |
| 7 | Performance: profile, then native TDB acceleration and A/B DB-dump equality | week time at most 1.5x the FBS-only baseline, with identical DB results | 5-10 |
| 8 | Soak: 5 seasons, cold reloads every season, table use and save size logged | no table at 100%; save size trend under S; no crash | 3-5 |

Total: about 51-85 agent-days. Release and installer work comes after this, per the project priority.

### 3.1 Phase 0 runtime results (2026-10-29, agent fcsp0)

**Build: a separate exe, never the Play_PC exe.**
- Stage = the current `...-rec26-uiset` EBOOT (`vfs/.../EBOOT.elf`, sha256 3f494c77...) plus `save-grow-v0` and `u8-loops-v0`. That is 28 words, all preimage-checked.
  - The overlay is built by `tools/ps3recomp-lane-e/work-fcsp0/mkelf.py`, which gives `work-fcsp0/elf/EBOOT.elf` (sha256 ce5374f9...).
  - It is not added as a named stage in `cfbr_real2026_runtime_v28.py`, because the fcs-universe manifests do not use the installer's pin format.
- The lift (into `work-fcsp0/recomp`) differs from the shipped lift in exactly 3 chunks:
  - 001: 17 `0x7E -> 0xFE` immediates;
  - 011: 9 immediates (the live save entry 0x336164);
  - 002: 11 `rlwinm 24 -> 16`.
- Those 3 chunks were compiled with the game_project flags, plus diagnostics that only this exe has:
  - `[FCSP0]` heap probes after the two vtable allocations;
  - an active-index log at the end of `league_index_fill`;
  - `FCSP0_TTYP1=1` env-gated binds of the three league-index TTYP values;
  - a copy of `cellSaveData.c` that logs the guest file-buffer address.
- They were linked with the build-86 objects into `work-fcsp0/bin/MyGameRecomp_fcsp0.exe` (final sha256 9cd1f2b3...).
- `game_project/build/MyGameRecomp.exe` stayed at build 86 (2c39f32b1f99...) throughout. Play_PC never sees the fcsp0 exe.
- Launcher: `work-fcsp0/run_fcs.ps1`. It uses its own exe, an isolated cwd (it refuses cwd_e and play_e), `-Elf`, and `-Boot`, which serves a test `qkl_boot.ast` through a read-only overlay rule.

**T0.1: PASS.** Runs `fcsp0-t01a` and `t01b`; cwd `work-fcsp0/cwd/t01`, which starts with only a profile copy.
- Ran New Dynasty (Sam Houston HC) to the Pre-Season 2026 hub. Shots `runs/fcsp0-t01a/shots/a4..b3`.
- Dynasty creation autosaved, and a menu save followed.
  - Both saves: USR-DATA 16,666,624 B, HED-DATA[0] 0xFE52E8.
  - HLE log: `file op=1 name='USR-DATA' size=16666624 buf=16666624`.
  - The autosave and the menu save are byte-identical.
- A cold relaunch loaded the save to the same hub (`runs/fcsp0-t01b/shots/c4`).
- Saving again after the reload changed 275 bytes:
  - TEAM.NCDP on all 143 rows and TEAM.INPO on 128 rows, both recomputed on load;
  - the TSSE header;
  - the HED-DATA hash.
  - No other table changed.
- Copies: `work-fcsp0/save_t01_auto`, `save_t01_menu`, `save_t01_reload`.

**T0.2: PASS, but with almost no headroom.**
- The save and load buffer is in a transient 16 MB container block. It is not in a game heap; the two static allocation sites never ran. Section 2.2 has the addresses.
- Headroom at S = 0xFE5000 is 107,200 bytes.
- Fallback decision:
  - Not needed at this S.
  - Required before any larger S (the plan's 25 MB contingency).
  - Required if the universe DB ever exceeds about 16.6 MB, which is unlikely: the measured TDB is 3.7 MB at creation and 7.0 MB after week 1.
- The fallback design changes: the vtable cave is replaced by a runtime-side redirect of that container request (Phase 1, once its caller is located).

**T0.3: PASS, with findings.** Runs `fcsp0-t03a` and `t03b`; cwd `work-fcsp0/cwd/t03`.
- Test BOOT: `work-fcsp0/t03/build_t03_boot.py`, 32 checks passed.
  - Roster 355 gains TGID 300 "FCS Test", cloned from Navy 57: TTYP 1, TVIS 1, CGID 19 (Big Sky, LGID 1), DGID 30, TORD 138.
  - It also gains 69 PLAY rows (PGID 21000-21068), 88 DCHT rows, 3 COCH rows (CCID 710-712) and 3 CSKL rows.
  - Capacities: TEAM 154, DCHT 12232, COCH 442, CSKL 417.
- ELF `elf/EBOOT_t03.elf`: the three league-index queries read `'PYTT'<= ?` instead of `'PYTT' = ?` (same length, data only). Run with `FCSP0_TTYP1=1`.
- Active index:
  - `act_n=139` while the roster is loaded;
  - `act_n=144` after Dynasty creation, because Dynasty creation sets TVIS 1 on the 5 generic FCS rows (TGID 160-164), so they enter too.
  - FBS TTYP-0 rows stay at 138.
- The Dynasty created normally. Advance to Regular Season, then Week 1, then Week 2 (Sam Houston 0-1) ran without a fault. The save was 16,666,624 B. A cold reload landed on the Week 2 hub with `act_n=144` (`runs/fcsp0-t03b/shots/f3`).
- Team 300 in the saves:
  - all 69 players kept;
  - PPRI was updated by the weekly pass for 44 players, the same count as Navy, so roster-level weekly code covers it;
  - **0 coaches**: CCIDs 710-712 are kept but detached by `dynasty_create_nonfbs_coach_cleanup`, as predicted in 1.3;
  - **0 DCHT rows**, deleted in the same way as for the generic FCS rows;
  - TROV recomputed to 0, presumably because it has no depth chart;
  - no games, because the season-0 schedules are presets, so there are no stats yet.
- Not checked in one week: the CFP and BCS pool, which is only computed later in the season.

**Consequences for Phase 1:**
1. Retire or remap the 5 generic FCS rows before widening to TTYP <= 1. Otherwise rosterless teams enter the active index (144 instead of 139).
2. Take TTYP 1 out of the coach-cleanup list (0x178a560 / 0x178a5e8), and find the DCHT purge for non-FBS teams.
3. FCS teams need schedule rows (the Phase 3 cave) before progression and stats can be validated.
4. Locate the 16 MB container request and the real save serialiser. Neither 0x335738 nor 0x336164 is on the live path.

### 3.2 Phase 1, first runtime pass (2026-10-30, agent fcsp1)

PC port, separate test executable only. The Play_PC executable and the user's saves were not touched. The test Dynasty had 12 rostered FCS test schools (cloned rosters, TGIDs 236-241, 255-257, 300, 350 and 399) beside the 138 FBS teams.

| Goal | Result |
|---|---|
| Save headroom | **Works.** The transient save arena is created by a generic heap factory (0x43B2C4) from a config `size` (16 MB). The test build grows it to 32 MB, and the container is grown to match. Dynasty saves are now 25,055,232 bytes (17 size words, immediate 0x17E). Creation saved; a cold relaunch reloaded both the creation save and the week-7 autosave; every weekly autosave through week 12 stayed that size. |
| Generic FCS rows | **Retired.** Converting the 5 built-in generic rows into real schools failed: their coaches were still detached by an unfound path. The test data deletes the 5 rows and their coaches instead, and every preset reference is remapped. The active list then holds exactly 150 = 138 FBS + 12 FCS. |
| Cleanup exemption | **Coaches: works.** The detach is not 0x4F5BE8 (TTYP 2-8 only). It is 0x4F9018, which detaches the coaches of TTYP 1 and 5 teams. One word (bind 1 -> 5) exempts FCS, and all 12 test teams kept 3 coaches through creation and 12 weeks. **Depth charts: not yet.** Dynasty depth charts are built for the 138 FBS teams only, through a path that has not been found. |
| FCS schedules | **Partly.** The preset schedule gives every FCS test team 11 games and every week at most 63 (the limit is 126). The engine's season generator kept the FBS-vs-FCS games and only some FCS-vs-FCS ones, so each team got 7-9 games. FCS teams do play: without a depth chart they lose every game by shutout and record no player stats. |
| Team-count literals | **Rule found.** The engine's 72 team-count literals (activeN, 138 today) must be raised together. Raising only the 44 "league-wide" ones corrupted memory right after Dynasty creation. Raised together to 150 (only the 3 BCS-pool words stay at 138), 12 regular-season weeks ran at 33-70 s per week. One run stalled on a news/autosave panel after week 7; after a reload, weeks 7-12 ran clean. The 288-team reserve rebuild has not started. |
| Consumer classification | 114 of 115 team-list readers are league-wide. The only FBS-only one is the bowl BCS pick loop (bound set to 138). The polls, BCS and bowl selectors use their own FBS-only team queries. |
| FBS-only outputs | At creation and in weeks 1, 7 and 12: FBS poll ranks are exactly 1-138, every FCS team stays unranked, and no bowl row holds an FCS team. Conference championships, bowls and the CFP are not reached yet. |

Also found: Dynasty creation renumbers team sort order (TORD) alphabetically over every team with a coach, FCS included. So the active list is not "FBS first, then FCS". Code must not rely on list position to find FBS teams.

### 3.3 Phase 1b: depth charts and a full season (2026-10-30, agent fcsp1b)

Separate test executable only, as before. Same 12 test schools, plus a second data set with six of them moved to team ids below 236.

| Goal | Result |
|---|---|
| Depth charts | **Fixed.** Dynasty creation first wipes every team's depth chart. Then it copies each team slot's data back from the roster, and a per-slot callback (0x53C86C) removes the depth-chart table from the copy for FCS-type teams. One word (0x53C894, now a no-op) lets FCS slots copy it too. After creation all 150 teams have 88 depth-chart rows, and FCS team overalls are 67-74 instead of 0. (The full depth-chart rebuild that already covers 150 teams is skipped in a Dynasty's first season, so it did not help at creation.) |
| Full season | **Works.** Regular season, conference championship week, bowls and the 12-team playoff all ran, using multi-week advances. Five autosaves were written, all 25 MB, with no faults. The earlier stall on the "Coach News / Autosave in Progress" panel did not come back. |
| FBS-only postseason | **Holds.** 41 postseason games were played, all between FBS teams (58 distinct teams). An FBS-only control Dynasty also has 41, all FBS. No FCS team appeared in a bowl or playoff game, and none was ranked in any poll at any point. FBS poll ranks stayed exactly 1-138. |
| FCS player stats | **Not yet.** FCS teams play and their team totals are kept, and FCS-vs-FCS games have winners. But against FBS teams they score 0-14 points, and their players get no box-score or season stat rows, while their FBS opponents' players do. The game is simulated, but the FCS side does not field its real roster. Moving six FCS schools to team ids below 236 changed nothing, so the trigger is the team type, not the id range. The next step is to find the check in the weekly game setup. |
| Schedules | **Unchanged.** FBS teams get exactly 12 games. FCS teams get 7-9, and the season generator puts a few FCS teams in two games in one week. The planned FCS schedule step is still needed. |

Also found:
- Team ids 300 and 400 are reserved: a cleanup routine (0x4DAC6C) deletes everything belonging to those two ids. The FCS data pack must skip them.
- The team-schedule table (TSCH) and one player-stats table reach full capacity in this test season. Both need larger template capacities before more teams are added.

### 3.4 Phase 1c: FCS rosters play and keep stats (2026-10-30, agent fcsp1c)

Separate test executable only, as before. Same 12 test schools. Six test Dynasties or reloads, all in isolated test folders.

| Goal | Result |
|---|---|
| FCS rosters in games | **Fixed.** The stock game treats team types 1 and 7 as rosterless placeholder opponents. When a game is set up (0x46F110), the two team-copy routines (0x43F990 players, 0x466B34 depth chart) take a stand-in roster and depth chart instead of the team's own for those types. After the game, two routines (0x507930, 0x4E4520) delete or remap the stand-ins' game stats, and a per-team pass (0x44FDF4) stops unless the team is FBS. Twelve compare instructions now test for type 7 only (or let type 1 through), so type-1 FCS teams are handled like FBS teams. In a new Dynasty, FCS teams averaged 16-22 points against FBS teams, won 7 of 58 such games and were shut out 3 times through week 7 (the test schools are copies of FBS rosters, so they are stronger than real FCS teams will be). FCS players now get box-score, season and career stat rows, 23 of them reached the national top-10 stat lists, and FCS teams get season team-stat rows. Seven weeks ran without a fault. The first week after loading an older save still uses stand-ins, because that week's game rosters were prepared before the save. |
| Table capacities | **Partly done.** A data builder raises 22 table capacities in the Dynasty template, and a new Dynasty inherits all of them. But with the big box-score tables raised (about 0.8 MB more), the weekly ranking pass faults within 1-3 weeks; three runs showed it, and the same code without the raises ran 7 weeks clean. Raising only the team-schedule table (to 3,600 rows) and the conference stat-ranking table (to 3,750) ran clean. The likely cause is a fixed-size memory heap for the Dynasty database; finding and growing it is the next step. The national top-10 table that looked "full" is full by design (25 categories x 10 players). |
| Schedules | **Partly done.** The season generator throws away preset games between two teams of the same conference when that conference is not one of the 14 FBS ones. Scheduling FCS-vs-FCS presets only across conferences gives every FCS team 11-14 games (7-9 before). A test-build step that rewrites schedule inserts when an FCS team is already busy that week cut the double-booked weeks from 12 to about 6. It cannot fix them all, because the generator moves games between weeks after inserting them. FBS teams keep exactly 12 games and no week holds more than 69 games. Next: one repair pass after the generator finishes, and a way to schedule FCS conference games. |

### 3.5 Phase 1d: database memory, one schedule repair pass, a full season with FCS stats (2026-10-30, agent fcsp1d)

Separate test executable only, as before. Same 12 test schools. Four new test Dynasties and one reload, all in isolated test folders.

| Goal | Result |
|---|---|
| Bigger stat tables | **Done in the test build.** The crash is confirmed, not guessed. The weekly step that failed is the recruiting-board fill (0x4C3E38). It first sorts three database tables, and the sort asks the game's memory manager for a work buffer of 1-4 MB. With the larger tables loaded, the heap the game names `DB` (a 10 MB block plus a 2 MB block) had no room left. The game then writes its "bad alloc" marker (0xBADA110C) to address 0, and everything after that is fallout. Every earlier crash log has this marker; no clean run has it. Heap sizes come from a small key/value config that the game reads at startup (0x435E28), and the `DB` size is read more than once, so the test build changes the value at that reader. With the `DB` heap 4 MB larger, all 22 enlarged tables ran a whole season: creation, 15 weeks, conference championships, the bowls and the playoff, with no out-of-memory event. The enlarged tables are being used: at conference championship week the defensive box-score table held about 25,700 rows, which is 95% of the old size and 63% of the new one. One small table (the injury list) is full again and needs a larger size. For the full 266-team universe the heap should get about 16 MB more, as a proper runtime setting. |
| Schedules | **Done for the test.** One repair pass now runs right after the season generator finishes and before game numbers are assigned (in 0x103714, before 0x1034EC), every season. It reads the finished schedule with the game's own queries, then fixes it in order: FCS teams playing twice in a week (give the FBS opponent a free FCS team, or move the game), FCS teams over 12 games, FCS conference games, and FCS teams under 11 games. New games go through the game's own insert routine, so home/away, dates and times follow its rules. FBS-vs-FBS games are never touched and no week goes over 126 games. In four new Dynasties: every FCS team has 11-12 games, every FBS team still has 12, and the busiest week has 68 games. Three Dynasties had no double-booked weeks at all. One had 2 left in week 1, where more FBS teams want an FCS opponent than the 12 test schools can cover; with about 128 real FCS schools this should not happen. |
| FCS conference games | **Decided and built.** The repair pass schedules them. It pairs conference members that have not met (up to 8 conference games per team, later weeks first) and drops non-conference FCS games to stay at 12. Changing the game's own conference generator would also need new rows in three style tables that are already full, and that generator ignores FCS conferences anyway. |
| Full season with FCS stats | **Done.** FCS teams scored 18 points per game against FBS teams and won 26 of 74 such games, and 32 FCS-vs-FCS games were played. FCS players have box scores and season stats. Postseason: 41 bowl and playoff games, all played, all between FBS teams, the same count as an FBS-only Dynasty. No FCS school was ranked, picked for a bowl, named a Heisman finalist, named an All-American or listed as a bowl champion. Two notes: three FCS players appear in the national stat-leader lists next to FBS players (they should get their own lists later), and the FCS test conferences got conference-champion entries without a title game. |
| Not solved | Once, the end-of-season advance stopped on an "autosave in progress" panel and never saved. No error was logged. Reloading the conference-championship save and advancing one step at a time went through. This looks like an earlier unexplained stall and is the next thing to chase. The 288-team storage reserve was not started. |

### 3.6 Phase 1e: autosave stall, memory setting, first rollover, 266-team data staged (2026-10-30, agent fcsp1e)

Separate test executables only, as before. Isolated test folders. The normal game executable and saves were not touched.

| Goal | Result |
|---|---|
| End-of-season autosave stall | **Located but not reproduced; cause still open.** The two stalls seen so far (one in Phase 1, one in Phase 1d) stop at the same point. The game has allocated the 25 MB save buffer, but it never starts the thread that writes the save files. There is no error, no out-of-memory event and no crash; the game's own memory allocator has no wait or retry path that could explain it. This session made 11 more test saves from the same starting save: an end-of-season advance pressed quickly, the same advance pressed at the original pace, the off-season, the move to the next season and five more weeks. None stalled. Both real stalls happened in long sessions that had already saved several times. A watcher script now dumps every game thread's call stack automatically if a save stalls for 60 seconds, so the next occurrence will show where it waits. **Normal (FBS-only) game:** the same save code runs there, with a smaller save (8.3 MB instead of 25 MB). This stall has only been seen in the FCS test builds, but that does not prove the normal game is immune. If it ever appears, the game has not crashed: quit and load the last autosave, which is intact. |
| Database memory as a setting | **Built, not yet run.** The test build reads `NCAA_DB_HEAP_MB` at startup (also settable in the test folder's settings file). It only changes the heap whose stock size is 10 MB, the only one with that size, and is clamped to 10-64 MB. The default in this test build is 26 MB (+16 MB), the size planned for 266 teams. |
| Tables close to full | The injury list (40 of 40) and the other near-full tables are enlarged in the new 266-team data pack (injuries 120). One more table, CAPX (195 of 200), still has to be checked. |
| First off-season and rollover with FCS teams | **Runs, but FCS rosters are lost.** The off-season stages, the coaching carousel and the move to Pre-Season 2027 ran without a fault, and the schedule repair pass fixed the new season too (FCS 11-12 games, no double-booked weeks, FBS 12). But the rollover deletes every FCS player and depth chart, and the carousel hires most FCS coaches away. In 2027 the FCS teams field nobody and lose every game. Finding that clean-up step is now the first item, because no second season is valid without it. |
| Full FCS list and data pack | **Built.** 128 real FCS programs in their 2026 conferences: 13 conferences plus independents, compiled from public sources, with a 1-5 strength tier for each school. The test data gives every school a generated 69-player roster with new names from our own name pools, ratings scaled by tier (team overall about 49-70, below the weakest FBS teams), depth charts, three coaches and its real conference. Tables are sized for 266 teams. Nothing in it comes from game files except the table layout the game needs. |
| 288-team reserve and team count 266 | **Patch built offline, executable not built.** The 160-team storage reserve and the 72 team-count values were re-derived for 288 / 266, and every changed word was checked against the original program. Two work arrays cannot grow by changing numbers in the code, so the PC build moves them into spare memory instead. The scan found two more loops that count teams in a single byte and would never reach 266; both are widened. The compile was stopped part-way because the disk filled up (see below). |
| Extras staged | FBS-only national stat leaders (FCS players are left out instead of mixed in) and a last fallback for crowded weeks in the schedule repair pass. Both are in the unbuilt 266-team build. FCS conference title games are not started. |

**Disk.** Late in the session the PC's free disk space fell from about 26 GB to almost nothing. The page file grew while other memory-heavy jobs were running. This work stopped its compiles, gave back its game-run slot and removed about 9 GB of its own rebuildable files.

### 3.7 Phase 1f: the FCS roster wipe found and mostly fixed, the 266-team build runs to its first advance (2026-10-30, agent fcsp1f)

Separate test executables only, as before, in isolated test folders. The normal game executable and saves were not touched. Old build logs and superseded test files (about 12 GB) were removed first to get the disk back above its safety floor.

| Goal | Result |
|---|---|
| Where the off-season loses FCS players | **Found.** A test Dynasty went through the off-season one stage at a time, with a save check after every stage and a log of every database query that touched an FCS school or player. Graduation removes FCS seniors normally. The loss happens at the CPU roster-cut stage ("holding team tryouts"). The game first puts every player and recruit on one cut list. Then, team by team, it takes off the list the players each school keeps, and finally releases everyone still on it. That team-by-team pass only visits FBS teams, so every FCS player stayed on the list and was released. |
| Fix: FCS teams keep their players | **Works for 10 of 12 FCS schools.** A small piece of added code repeats the keep pass for FCS teams. In the test, 10 FCS schools went into the 2027 season with 60-70 players and valid depth charts, and FBS teams were unaffected. The two FCS schools that had lost every coach in the carousel still lost all their players. |
| FCS coaches | **Not fixed yet.** The game's pass that fills empty coaching jobs only looks at FBS schools. The test build now repeats it for FCS schools, but that pass turned out to run only when a Dynasty is created, not in the off-season. The off-season job filler still has to be found. FCS coaches can still be hired away in the carousel, which is fine, as long as their jobs get filled again. |
| Second season | **Blocked.** The 2027 regular season started (all 12 FCS schools got 11 games and no week had a school playing twice), but advancing past week 1 only saves and goes back to week 1. There is no crash. The cause is open; the two empty FCS schools are the first suspect. |
| Refilling FCS rosters | **Not done.** FCS schools do not recruit yet, so graduation shrinks their rosters by about a quarter each year. The plan is to give FCS schools some of the recruits nobody signed, or walk-ons. |
| 266-team build | **Built and started.** It creates a new Dynasty with all 266 teams, and the schedule check passes: every FCS school has 11-12 games, every FBS school 12, and no week has a team playing twice. The first advance hangs in the step that rates recruits for every team. A small memory request there fails, most likely because one of the game's fixed memory pools is too small for 266 teams. A larger database memory size did not help, so it is a different pool. |
| Database memory setting | **Confirmed.** The setting works at startup on 150 and 266 teams. |
| Table CAPX (195 of 200) | **No change needed.** It is the fixed list of coach goals for the player's own coach and does not grow with the number of teams. |
| Autosave stall | None in about 20 saves this session; the watcher ran in every test. |

### 3.8 Phase 1g: full FCS rosters and staffs across three seasons, the 266-team build through a regular season (2026-10-30, agent fcsp1g)

Separate test executables only, as before, in isolated test folders. The normal game executable and saves were not touched. Superseded test executables (about 7 GB) were removed when the disk got close to its safety floor.

| Goal | Result |
|---|---|
| Why the second season stopped at week 1 | **Found and fixed.** A log of every database query during the failed advance shows 22 games simulated, then the setup of a game involving an FCS school with no coaches and no players. When any game in the week has a team without a coach, the game abandons the whole week, autosaves and returns to the same week. With every staff filled (below), the 2027 and 2028 seasons advance normally. |
| Off-season coach fill | **Fixed.** At the end of the season the game posts an opening for every empty coaching job, and the carousel stage then hires into those openings. The posting step only visited FBS schools. The test build repeats it for FCS schools: after the carousel all 12 FCS schools had a head coach and both coordinators (before: 0-1 coaches). A safety net also fills any empty coaching job right before the CPU roster cuts. |
| FCS roster refill | **Not needed as a separate feature.** FCS schools already recruit (about 20 signees each per year, lower rated than FBS classes); the earlier roster-cut fix now keeps those signees. Every FCS school starts each new season with 60-70 players. Off-season player progression runs for FCS players too (returning players about +4 overall, FBS about +5). |
| Second and third season (150 teams) | **Pass.** One test Dynasty: 2026, off-season, all of 2027 (bowls and playoff included), off-season, and 2028 to week 5. Every FCS school had 60-70 players, a full depth chart and 3 coaches at the start of 2027 and of 2028, 11-12 games and no double weeks; FCS player and team stats were recorded. No crash, no autosave stall. |
| 266-team first-advance hang | **Fixed.** The "rating teams" recruiting step keeps its work in a fixed pool of 4,410 small records, which runs out with 266 teams; the game then writes through an empty pointer forever. The pool is three times larger in the test build. |
| 266-team season | **Regular season passes; end of season open.** A 266-team Dynasty played every week up to conference championship week (about 1.4 minutes per simulated week), all 128 FCS schools with 11-12 games and no double weeks. The advance to the end of the season plays the bowls and then stops in the game's own coaching-carousel step (it also stops with the FCS change switched off). Most likely another fixed-size list; this is the next item. |
| FBS-only national stat leaders | **Bug found and fixed.** The filter that keeps FCS players out of the national leader lists looked players up with a wrong query address and never removed anyone. Fixed in the newest test build, which now removes FCS players; the finished lists still have to be checked in a save. |
| Crowded-week schedule fallback | **Not needed so far.** The 266-team schedule pass reached zero double weeks without it, so it is still unexercised. |
| FCS strength | **Needs tuning.** With the 150-team test data FCS schools win about a third of their games against FBS schools (real: about 1 in 10); with the 266-team data they win 2 % and average 8 points. |
| FCS conference title games | Not started. |

### 3.9 Phase 1h: the 266-team end-of-season hang fixed, the first 266-team off-season, separate FCS stat leaders, FCS strength retuned (2026-10-30, agent fcsp1h)

Separate test executables only, in isolated test folders. The normal game executable and saves were not touched.

| Goal | Result |
|---|---|
| 266-team end-of-season hang | **Found and fixed.** Every coaching contract has an id, and the id field is 10 bits wide, so at most 1,023 contracts can exist. The game's contract table holds about 5 rows per school (current contracts, finished ones and open offers): about 780 with 150 schools, about 1,390 with 266. When the end-of-season step posted new coaching openings, the routine that looks for a free id never found one and looped forever. The fix widens the id to 11 bits in the Dynasty template (the contract table had unused bits; the coach table's rows grow by 4 bytes) and lets the id routine use the larger range, never handing out the value that means "no contract". A tool converts existing test saves. Three test runs then played the bowls and playoff and finished the end of season, with contract ids past 1,023 and no duplicate or broken links. |
| 266-team off-season | **Runs, one problem left.** The whole off-season ran to Pre-Season 2027. Every FCS school has three coaches. The coach table needed more room (about 700 free-agent coaches exist after the first carousel), so it is raised to 2,000. **Open:** the 10 FBS schools first in team order keep stale contracts for coordinators who left, so nobody is hired into those jobs; a school with no coach makes the week-1 advance give up. 266 minus 256 is 10, so this looks like one more 256-entry team loop. Two repair attempts in this session did not hire coaches outside the carousel stage. |
| Postseason | **FBS-only** (41 games, all 61 teams FBS) with 266 schools. |
| Separate FCS stat leaders | **Done (stored, no screen yet).** The national leader lists are filled twice in the same step: once for FBS players (as before) and once for FCS players only. The FCS lists use their own category numbers, so the existing screens never show them. Checked in a save: 250 FBS rows and 250 FCS rows, 25 per category. A later page can read them. |
| FCS strength | **Retuned and measured.** The first try (a full season with new 266-school data) had FCS schools winning 22 of 112 games against FBS (20 %) and scoring 14 points, while FBS teams scored only 31: FCS defenses were too strong. The second version weakens FCS defenders a bit more than the rest and lowers every tier slightly. Through week 6 (92 of the season's FBS-vs-FCS games) FCS schools won 7 (7.6 %), scored 14.9 points against 37.3, and the strongest tier won 2 of 12 while the weakest tiers won 5-7 %. That is close to the real picture (about 1 in 10 overall, 13-20 FCS points). A full season with it is still to run. |
| Recruiting with 266 schools | **Needs work.** The yearly recruit class is a fixed 2,710 prospects, so with 266 schools each school signs fewer players (FBS about 19, FCS about 13.5; with 150 schools about 25-27). Some rosters drop into the low 50s after the first off-season. Next: scale the class size with the number of schools. |
| FCS title games and playoff | **Designed, not in the game yet.** Real rules: of the FCS conferences only the SWAC plays a title game; the SWAC and MEAC champions meet in the Celebration Bowl; the Ivy League stays home; the playoff has 24 teams (10 automatic bids, 14 at-large, the top 8 seeded with a first-round bye; 23 games). A reference model picks the field from a save's standings and plays the bracket from team ratings. The plan: first write results at the end of the season (no played games, no risk to the bowl system), later play the games, starting with the SWAC title game. |

### 3.10 Phase 1i: the 266-team Dynasty into its second season, recruit classes scaled, FCS postseason results (2026-10-31, agent fcsp1i)

Separate test executables only, in isolated test folders. The normal game executable, the play build and saves were not touched.

| Goal | Result |
|---|---|
| Coaches lost at the 266-team rollover | **Found and fixed.** The end-of-season contract step collects every coaching contract into a list with room for 768. The 266-school league had 798 contracts, and the 30 left off the list were exactly the three contracts of each of the 10 schools that lost their staffs, so those contracts were never closed and no openings were posted. (The "266 minus 256" match was a coincidence.) The test build gives this list, and two similar lists in the off-season step, room for 2,048 contracts. A test Dynasty then ran from week 7 of 2026 through the bowls, the end of season, the off-season and the first three weeks of 2027: all 266 schools had three coaches, no stale contracts, clean schedules, and separate FBS and FCS stat leader lists. |
| Recruit class size | **Scaled.** The class size is the recruit table's size minus 1,595 (stock: 2,710). The test data enlarges that table and the tables that grow with it (interest, visits, boards, players), for 5,900 prospects: about 25 per FBS school and 19 per FCS school. The recruit rank field holds at most 4,095, so the test build stops ranks there. The 2027 class in the test had 5,900 prospects. The realistic recruit names, looks and home states from the play build are merged into the test data. Rosters only change at the next rollover, which is still to run. |
| FCS strength over a full season | **Measured.** FCS schools won 7 of 112 games against FBS schools (6.2 %) and scored 14.0 points against 38.1; the strength tiers stayed in order. Points match real FCS results; wins are below the 8-12 % target, so a version with the top two tiers slightly stronger is prepared. |
| FCS postseason | **Results written at the end of the season.** The test build works out the SWAC title game, the Celebration Bowl and the 24-team FCS playoff from the season's games (results decided from team strength, not played). The champions go into the save's conference-champion history and the bracket into a side file for a later screen. Checked against the reference model: same conference champions and same field. |
| New problem | With 266 schools the bowl and playoff selection picks wrong teams: a 3-9 team was placed in a playoff quarterfinal and 11 of 68 bowl spots went to teams with losing records. The final top 25 looks right. |

### 3.11 Phase 1j: bowl and playoff selection fixed, rollover into 2028, second FCS postseason (2026-10-31, agent fcsp1j)

Separate test executables only, in isolated test folders. The normal game executable, the play build and saves were not touched.

| Goal | Result |
|---|---|
| Bowl / playoff selection at 266 schools | **Found and fixed.** The weekly BCS-style ranking was built in a list sized for all 266 schools while only the 138 FBS schools are ranked, so every FBS rank was 128 too high and wrapped past 255: the ten weakest FBS schools held ranks 1-10 and were picked for the playoff and bowls. The 150-school build had the same mistake (+12). The test build sizes the list for 138 (switchable). Two postseasons checked: ranks exactly 1-138, all 58 postseason teams FBS with 6+ wins, playoff = 5 best conference champions + 7 at-large. |
| 2027 -> 2028 rollover | **Runs.** Rest of 2027, postseason, end of season, off-season and 2028 week 1. All 266 schools have 3 coaches; contracts clean. The 5,900-prospect class signed (freshmen about 26 per FBS school, 22 per FCS school). Rosters FBS 58-70, FCS 56-70 (13 of 266 below 60; 52 a year earlier with the old class). Strength tiers stay in order; 2028 schedule clean. |
| Second FCS postseason | **Matches the reference exactly** (conference champions, 24-team field, seeds, bracket). Montana champion. |
| FCS strength | 2027: 6 of 40 wins (15 %), 18 points vs 41. 2026 + 2027: 13 of 152 (8.6 %), inside the 8-12 % target; no data change yet. New problem: only 40 FBS-vs-FCS games in the 2027 schedule (2026: 112). |
| SWAC title game as a played game | **Data alone does not work**: an unused title-game slot pointed at the SWAC, with East/West divisions, was not scheduled; the list of conferences with a title game is decided in code. Next: a small code step that adds the SWAC title game to conference championship week. |

### 3.12 Phase 1k: FBS-vs-FCS games after season 1, a played SWAC title game, short rosters explained (2026-10-31, agent fcsp1k)

Separate test executables only, in isolated test folders. The normal game executable, the play build and saves were not touched.

| Goal | Result |
|---|---|
| Few FBS-vs-FCS games after season 1 | **Found.** Season 1 takes its non-conference games from the data (112 FBS-vs-FCS). From season 2 the generator's FCS filler, sized for the 5 stock placeholder FCS teams, aims for only 35-50 games, and about 48 FBS teams are already full when it runs. The test build aims it at 100-120 and tries more weeks, and caps FCS teams at 2 FBS opponents. 2028: **90** FBS-vs-FCS games (was 38), schedules clean. A quota top-up to about 105 is built (FCS25). |
| FCS strength | 2028 regular season: FCS won 11 of 90 (12.2 %). Three seasons: 24 of 242 (9.9 %). |
| SWAC title game | **Played.** A code step adds the SWAC East vs West winners to week 16, and the game is played with the other title games (Jackson State 41, Prairie View A&M 9). The FCS postseason step uses that result. |
| Rosters below 60 | **The class is too small.** The 5,900-prospect class is fully signed while the league is at 98.6 % of its roster spots. A save step raises the class to 6,700. |
| Rating scale | The shown team overall (TROV) starts season 1 on the user's scale but rises each year (FCS about 4-5, FBS about 2). |

### 3.13 Phase 1l: the third season finished, rating drift explained, a fixed team-rating scale (2026-10-31, agent fcsp1l)

Separate test executables only, in isolated test folders. The normal game executable, the play build and saves were not touched.

| Goal | Result |
|---|---|
| Bowl 2028 to Pre-Season 2029 | **Runs.** The SWAC title game result feeds the FCS postseason and is written to the conference champion history. The quota step turned 4 week-1 FBS-vs-FBS games into FBS-vs-FCS games: **106** FBS-vs-FCS games, schedules clean (FBS 12, FCS 11-12, no double weeks). With the 6,700 class, rosters are FBS 62-70 and FCS 59-70 (3 at 59). Every school has 3 coaches. |
| Why ratings rise | Players gain about 4.4 overall a year at every level. FCS recruits arrive at about 60 at every level. Season-1 rosters were too flat from freshman to senior, so starters climb for about four seasons and then level off (FBS about 84-86, every FCS tier about 70-72). No yearly bonus and no in-season change; a Pre-Season save still shows last season's team overall. The team overall is a fixed linear map of the starters (about 1.85 per point of starter overall). |
| Fixed scale (FCS26) | In the team-rating step, each team's raw overall is mapped per league from that league's min/max to FBS 65-97 and FCS 45-72, and the other team ratings get the same shift. The order is kept, and the four limits are one setting. 2029 in the game: FBS mean 82, FCS tiers 67 / 61 / 59 / 58 / 52. |
| Game results | **Not controlled by the team overall.** CPU-vs-CPU games are played from the players: FCS won 19 of 103 (18 %) in 2029 weeks 1-5 with the scale fixed. A player-level step is next (FCS recruit strength by tier, or a rollover rescale). |
| New Dynasties | Test data with the 6,700 class built and checked (not played yet). |

### 3.14 Phase 1m: FCS recruit strength by level, safer FBS-vs-FCS scheduling, model trade-offs (2026-10-31, agent fcsp1m)

Separate test executables only, in isolated test folders. The normal game executable, the play build and saves were not touched.

| Goal | Result |
|---|---|
| Why FCS levels merge | Recruits keep the ratings they were generated with, and FCS schools sign from what is left after FBS, so every FCS level gets recruits of about 60 overall. With the same yearly growth everywhere, the levels end up equal within about four seasons. |
| FCS recruit strength by level (FCS27) | When recruits join their teams, each FCS level's new class is moved to its own target average (default 60 / 58 / 56 / 54 / 52 from the strongest level to the weakest). All rating attributes of a player move by the same amount and the player overall is recomputed from the game's own per-position formula (an exact linear formula, fitted on 18,290 players). Order inside a class is kept; FBS is not changed. Targets and class spread are settings. **In the game, 2029 to 2030:** class averages about 61 each became 60.0 / 58.0 / 56.0 / 53.9 / 52.0. |
| Schedule fixes (FCS28) | No FBS team gets more than 2 FCS opponents. The quota step no longer replaces real future series from the game's data (the 4 games it replaced in 2029 were all such series). 2030 in the game: 104 FBS-vs-FCS games, clean schedule, 77 real series kept. |
| 2029 finished | FCS won 19 of 106 games against FBS (18 %), before the new step took effect. |
| Trade-offs (model) | Steady state, from the 2029 rosters: the exact asked-for scale (best FCS about 73, worst about 47) gives about 5 % FCS wins; the default about 8 % (FCS levels 70 / 67 / 63 / 59 / 56, best 76, worst 51); about 10 % needs the best FCS team near 78; without the step about 24 % with the levels merged. About +-4 points of model error. An existing Dynasty needs about three more seasons before the new classes reach the starting line-ups; a one-time adjustment of current FCS players would remove that wait (not built). |

### 3.15 Phase 1n: realistic recruit classes, star-gated FCS recruiting, starting FCS rosters on one scale (2026-10-31, agent fcsp1n)

Separate test executables only, in isolated test folders. The normal game executable, the play build and saves were not touched. **Built and checked offline; run in the game in Phase 1o (3.16).**

| Goal | Result |
|---|---|
| User decision | Middle ground: FCS levels about 70 / 67 / 63 / 59 / 56, best FCS about 76, worst 51, FBS about 86 (worst about 65), FCS wins about 8 %. One shared rating scale. Strength should come from recruiting, not from a rescale after signing. |
| What the game did (2029 class) | 6,700 recruits: 90 five-stars, 651 four-stars, 2,988 three-stars, 1,633 two-stars, 1,338 one-stars. Stars matched overall only loosely (some one-stars were rated 85). The national rank field overflows above 4,096 recruits, so the weakest third of the class looked like top recruits to the computer schools. FCS schools signed 82 four-stars and 4 five-stars, and every FCS level signed classes of about 61 overall. |
| Real life (rounded, estimates) | About 30-35 five-stars, 300-400 four-stars and roughly 2,000 three-stars a class; FCS programs sign mostly two-stars and a few low three-stars, almost never a high-school four- or five-star. |
| Realistic class (FCS29) | New star shares 0.5 / 5 / 28 / 35 / 31.5 % (five to one star), and each star level gets its own overall range (about 80 / 74 / 67 / 58.5 / 50 on average). The game's own order of the recruits is kept; a better recruit stays better. The rank overflow is fixed. Names, faces, bodies and hometowns are unchanged. All numbers are settings. |
| Star-gated FCS recruiting (FCS30) | Every week, before commitments, FCS schools are moved to the bottom of a recruit's list of favourite schools unless a per-level chance lets them stay: never for five-stars, 1-3 % for four-stars at the top FCS levels, and fewer three-stars the lower the FCS level. Recruits commit to the top of their list, so top recruits go to FBS schools. All chances are settings. |
| Older steps | The FCS recruit-strength step from Phase 1m is now only a light safety limit (it acts only if a level's class ends more than 1.5 away from its target). The separate FBS / FCS display scale is off by default. |
| Model result | FBS classes about 67.6 (as before), FCS level classes about 60 / 58 / 55 / 53 / 51, no four- or five-star in FCS. Over many seasons: FCS levels 71 / 67 / 64 / 58 / 56, best FCS 77, worst 51, FBS 87 (worst 67), FCS wins about 9 % (model error about +-4 points). |
| New Dynasties (test data v16) | The 128 FCS starting rosters are rebuilt so season 1 already sits on this scale (predicted 70 / 67 / 63 / 59 / 56), with a realistic spread from freshmen to seniors (about 13 points). FBS rosters and every other table are unchanged. |
| Next | Run in the game in Phase 1o (section 3.16). |

### 3.16 Phase 1o: the new recruiting run in the game for the first time (2026-10-31, agent fcsp1o)

Separate test executable only, in an isolated test folder. The normal game executable, the play build and saves were not touched. No new build.

| Goal | Result |
|---|---|
| Realistic class (FCS29) | Worked in the game, twice (2030 and 2031 classes): 34 five-stars, 334 four-stars, 1,876 three-stars, 2,346 two-stars, 2,110 one-stars; average overall about 80 / 74 / 67 / 59 / 50 by star; about 3.5 seconds. The class is created when the season starts. The rank overflow is fixed (the bottom of the class no longer looks like the top). |
| Star gate (FCS30) | Runs every week in about one second. During the 2030 season 285 of 286 committed four- and five-stars went to FBS schools, and each FCS level signed its own kind of recruit (top level mostly two- and three-stars, bottom level mostly one- and two-stars). |
| Top FBS programs | Still recruit at the top: the ten highest-rated programs had classes ranked 1st to 20th, each with several four-stars. The best FCS class ranked 95th. |
| Final 2030 classes | FBS 68 average; FCS levels 59.1 / 58.8 / 57.0 / 55.4 / 53.8. FCS schools signed 8 four-stars and 1 five-star in total (before: 86). These signed after the season through a step the star gate does not cover yet; the top FCS level also signed more one-stars than planned. |
| Rosters and staffs | After the 2030 to 2031 off-season every FBS roster has 70 players, FCS 68-70, and all 266 schools have full coaching staffs. |
| Results on the field | FCS teams won 23 of 99 games against FBS in 2030 (about 23 %), as expected while the older, stronger FCS players are still on the rosters; the planned rate of about 8 % needs a few new classes. |
| Found | Contract numbers for coaches have run out of room and are being reused (about 260 repeats so far, no visible effect yet). |
| Next | Close the off-season gap for four- and five-stars (as a switch), look at the contract-number reuse, then a new Dynasty with the new starting rosters. |

### 3.17 Phase 1p: top recruits no longer reach FCS schools after the season, contract numbers are fine (2026-10-31, agent fcsp1p)

Separate test executable only, in an isolated test folder. The normal game executable, the play build and saves were not touched.

| Goal | Result |
|---|---|
| Where the leak was | The game signs recruits in three passes. The star gate from Phase 1n only reordered each recruit's list of schools. In the big signing pass after the season, a recruit whose FBS schools were already full simply moved down his list to the FCS schools at the bottom. A last "fill weak teams" pass hands out only one-stars, and it was the source of the extra one-stars at the top FCS level. |
| Fix (new switch, on by default) | The same star check now also runs at the moment of each signing, in all three passes. A refused signing is treated like "that school has no room", so the school keeps filling from lower-rated recruits and every count stays right. |
| In the game, 2031 season | From week 1 to the end of signing: **no four- or five-star recruit signed with an FCS school** (2030: 9). All 34 five-stars and 330 of 334 four-stars signed with FBS schools; 4 four-stars went unsigned. The check costs well under a tenth of a second. |
| FCS classes by level | Overall averages from top level to bottom: 58.0 / 58.1 / 57.3 / 55.8 / 52.7. The bottom three levels are distinct; the top two are still level, because the top level signs few players during the season and the final fill gives it one-stars. Next step listed below. |
| FCS class counting | The level-strength check now sees the whole incoming FCS class (2,215 players; before it missed about 40 % because players inherit their roster slot's id). |
| Contract numbers | **Not being reused.** The game keeps deleted rows in its tables, and the checker counted them. Counting only live rows: every contract number is unique in every save, there is room for about twice the contracts that ever exist at once, and every school has its full staff of three coaches. A small safety pass (removes contracts whose coach no longer exists) was added; it found nothing to remove. |
| Results on the field | FCS teams won 30 of 106 games against FBS in the 2031 regular season (28 %). The team ratings still come from the older rosters; this needs a re-check after the next season's ratings. |
| Not finished | The save after the 2031 to 2032 off-season was not written (a known, rare autosave hang; the game was stopped and the earlier save is intact). The new off-season results above come from the game's own log. |
| Next | Finish that off-season step; give the top FCS level more two- and three-stars (several options, some without a rebuild); re-check the FCS win rate after the ratings update; a new Dynasty with the new starting rosters. |

### 3.18 Phase 1q: the "Autosave in Progress" hang found and fixed, the 2032 off-season finished, the top FCS level separated (2026-10-31, agent fcsp1q)

Separate test executables only, in an isolated test folder. The normal game executable, the play build and saves were not touched.

| Goal | Result |
|---|---|
| Autosave hang: cause | The PC port's runtime keeps a fixed table of 64 game threads and frees a slot only when another thread waits for the finished one. The game starts its short-lived helpers (one per save or load, per trophy, per video) as threads nobody waits for, so each one used up a slot for good. After about 63 thread starts in one session the table was full, the next save could not start its helper, and the game waited forever. Every hang seen in earlier test runs happened right after the 63rd thread start. |
| Does the normal play build have it? | Yes. It uses the same runtime and the same game code; the number of teams and the save size do not matter. Normal play has about 40 short-lived thread starts to spare per session (roughly 15-20 saves or loads, fewer with trophies and videos). If it happens: quit and restart, the last save is intact. |
| Fix (new switch, on by default in the test builds) | When the table is full, slots of finished helper threads are given back (and their stack memory reused). Nothing changes before the table fills. Reproduced on purpose with a smaller table: without the fix the next load hung; with it the same load, the off-season, the new season start and four weeks ran with 19 slots recycled and no hang. Still to be moved into the play build. |
| 2031 to 2032 off-season | Finished. No four- or five-star recruit signed with an FCS school (all 33 five-stars and 316 signed four-stars went to FBS). Rosters FBS 66-70, FCS 65-70; all 266 schools have three coaches; contract numbers clean. |
| FCS levels: top vs second | The final "fill weak teams" signing step only offered one-stars. A new switch lets FCS schools take leftover two- and three-stars there (best first), and a setting keeps the top FCS level from taking leftover one-stars. Final 2032 classes, top level to bottom: before 58.0 / 58.5 / 57.3 / 55.7 / 52.9; setting only 61.0 / 58.3 / 57.2 / 55.8 / 52.8 (top level's class shrank to 11.6 a school); new switch only 58.8 / 59.5 / 58.0 / 56.0 / 53.5; **both 61.0 / 59.5 / 57.9 / 56.2 / 53.5 with normal class sizes**. Target 59.7 / 57.6 / 55.4 / 52.8 / 51.3: the order and the gaps are right, all levels about 1-2 points high (tunable with existing settings). |
| Results on the field after the 2032 ratings update | Team ratings FBS 86; FCS levels 74 / 72 / 70 / 69 / 67, now in order. Weeks 1-4 of 2032: FCS won 27 of 116 games against FBS (23 %; by level 50 / 33 / 28 / 9 / 6 %). Still above the planned rate; most FCS starters were signed before the new recruiting. |
| Not done | A new Dynasty with the new starting rosters. |
| Next | Move the autosave fix into the play build; make the new recruiting settings the default and pull the levels down to target; follow the FCS win rate through 2032. |

## 4. Risks and effort

| Risk | Likelihood | Mitigation |
|---|---|---|
| A roster-level system uses TTYP 0 internally and silently skips FCS (progression, graduation, draft) | medium | Phase 0 T0.3 checks one rostered FCS team; Phase 1 owner review of every TTYP-bound query (`ttyp-owners.txt`) |
| An index consumer misclassified (1A-only vs league-wide), e.g. FCS teams entering the BCS | medium | byte-compare of BCS/CFP pools against an FBS-only control on the same seed (Phase 1 exit) |
| Hidden u8 team index in RecruitMan records (0x4c11e0, 0x4c23e0) | medium | Phase 1 decompile review; grow records as activeN did for CFBR's 12-byte first array |
| Save buffer outgrows its 16 MB container block (T0.2: 107,200 B spare at S = 0xFE5000) | low at this S, certain for any larger S | keep S = 0xFE5000; for more, redirect the container request to the mod arena (runtime) |
| BDEF near the u16 row cap (59k of 65,535) | low-medium | trim the margin; FCS games log fewer defenders; Phase 8 watches it |
| Week time over target | medium-high | Phase 7 native acceleration; the FCS quick-result option |
| Generator or UI list widgets with fixed capacities not yet seen | medium | Phase 6 probes per screen; fixes in the UI pipeline |
| Recruiting balance with 266 programs (FBS classes weakened) | medium | prestige and pitch tuning per level; fallback: a separate FCS recruit pool via the league-context swap (1.5) |
| Run-queue contention | high | batch probes: one manual GRANT runs T0.1-T0.3 together (max_min 90) |

Effort: about 51-85 agent-days (10-16 weeks at 5 agent-days a week). The critical path is Phases 0-1 (engine core, about 3 weeks). Data (Phase 2) can run in parallel with Phase 1.

## 5. Files

- Plan: this file. Public mirror: `public-repo/docs/modding/fbs-fcs-universe-plan.md` (no EA data, no pseudo-C).
- Scanners: `scripts/scan_team_width_lifted.py`. The u8-idiom and TTYP-owner passes were run inline. Their outputs, and enough to rerun them, are in `analysis/fcs-universe/`.
- Phase 0 builder: `scripts/build_fcs_universe_p0.py [--hi 0xFE] [--dry-run]`.
  - Outputs: `patches/fcs-universe-p0/save-grow-v0/{patch.yml,manifest.json}`, `u8-loops-v0/{patch.yml,manifest.json}`, `checks.json`.
  - None of the 28 addresses overlaps any existing patch in `patches/` or the installed `runtime/patches/patch.yml`.
- Queued decompile batch: `scripts/wait_idle_decomp.sh analysis/mapping-cfbr-fcs-universe "f474260:474260,f4f5be8:4f5be8,..."` with 474260, 4f5be8, 4cee28, 12f7d0, 4ac5c0, 4b0ac8, 4bab40, 4bee10, 4edf10, 504cb0, 4adeb0, 4c0ed4, 45cebc, 4740a8 and 4cbab0. Log: `analysis/batch-fcs-universe.log`. **The spec must be `tag:addr` pairs.** Bare addresses are rejected by `run_cfbr_ghidra_decomp.ps1` ("Invalid spec"), with no output. That is why the earlier `mapping-cfbr-fcs` batch never produced anything.

## 6. Handoff

- **Done (2026-10-29):**
  - static site lists for every limit (section 2);
  - the architecture (section 1);
  - the phased plan (section 3);
  - Phase 0 offline patches (both staged, 29/29 checks);
  - the capacity model;
  - the TTYP owner map;
  - closed MR gap 5.23: the save buffer is heap memory and the size is 17 code words.
- **For the lane E integrator (build owner):**
  1. Add a stage that appends `patches/fcs-universe-p0/save-grow-v0` (and optionally `u8-loops-v0`) to the current stage (`...-rec26-uiset`).
  2. Build under BUILD.LOCK.
  3. Give a manual GRANT (max_min 90) for T0.1/T0.2 on a copied profile.
  4. Expected: a new Dynasty's USR-DATA is 16,666,624 bytes and reloads. An old 8.27 MB save is expected to fail its check under this build: use it only to confirm the failure mode, never on the user's saves.
- **Next for this workstream:**
  1. Batch output exists (`analysis/mapping-cfbr-fcs-universe/`, 15 functions, 2026-10-30). 0x474260 and 0x4f5be8 are read and folded into 1.2/1.3. Still to read: 0x4cbab0 (BCS: does it use the index count?), 0x4cee28 (poll pass: how TTYP is bound, for the second call), the u8-loop functions (0x4ac5c0 ... 0x504cb0, to confirm counter-only use), 0x45cebc/0x4740a8 (LGID-1 standings) and 0x12f7d0. Then decompile 0x473df8 for the fill's TTYP `li`.
  2. Build the T0.3 one-team test roster and string repoints (`build_fcs_universe_p0.py` part C).
  3. Write the Phase 1 classifier for the 115 index consumers.
- **Environment:** the run queue was busy all session (GRANT tcvalidate, 3 pending). C: had 63 GB free.
- **Phase 0 runtime done (2026-10-29 23:25, agent fcsp0; section 3.1).** T0.1-T0.3 pass. The workspace is `tools/ps3recomp-lane-e/work-fcsp0/`:
  - scripts: `mkelf.py`, `mkelf_t03.py`, `probe_src.py`, `probe_idx.py`, `mkhle.py`, `mkcc.py`, `mklink.py`, `cc*.bat`, `link.bat`, `run_fcs.ps1`, `stop_fcs.ps1`, `chksave.py`, `t03/build_t03_boot.py`;
  - save copies `save_t01_*` and `save_t03_*`.
  - The 12 unchanged lift chunks were pruned (logged in `PRUNED.json`).
  - To relink after a new main build: recompile nothing, just run `link.bat` (it links the current game_project objects plus the 4 fcsp0 objects). Do this only while the main tree is still the build that the fcsp0 chunks were lifted from (uiset ELF 3f494c77...).
  - **Next:** the Phase 1 items in 3.1, starting with the generic FCS retirement and the coach and depth-chart purge list.
- **Phase 1c (2026-10-30, agent fcsp1c; section 3.4).** FCS teams now use their own rosters in every game and keep their stats (12 changed instructions). Next, in order: grow the Dynasty database memory so the box-score tables can be enlarged; replace the schedule rewrite with one repair pass after the season generator and add FCS conference games; run a full season with FCS stats to the bowls; then the 288-team storage reserve.
- **Phase 1d (2026-10-30, agent fcsp1d; section 3.5).** The Dynasty database heap is identified and can be grown, so the larger stat tables now run a whole season. One repair pass after the season generator gives FCS teams 11-12 games, adds FCS conference games and keeps FBS teams at 12. A full season with FCS stats ended with an FBS-only postseason and awards. Next, in order: the end-of-season autosave stall; the database heap size as a proper runtime setting (about 16 MB more for 266 teams) and a larger injury table; separate FCS stat-leader lists; then the 288-team storage reserve.
- **Phase 1e (2026-10-30, agent fcsp1e; section 3.6).** The autosave stall is narrowed to the step between reserving the save memory and writing the save, and a watcher now records thread stacks when it happens. The database memory size is a setting. The first rollover with FCS teams works but deletes FCS rosters. The 128-school FCS data pack and the 288/266 code changes are prepared. Next, in order: keep FCS rosters and coaches through the rollover; build and test the 266-team executable; confirm the memory setting; catch a stall with the watcher.
- **Phase 1f (2026-10-30, agent fcsp1f; section 3.7).** The off-season loss of FCS players is traced to the CPU roster-cut step and fixed for FCS schools that still have a coach. The 266-team test build is built and creates a full Dynasty. Next, in order:
  1. find out why the second season does not advance past week 1;
  2. fill FCS coaching jobs in the off-season;
  3. refill FCS rosters with recruits or walk-ons;
  4. grow the memory pool that runs out at the first 266-team advance;
  5. then a full 266-team season and rollover.
- **Phase 1h (2026-10-30, agent fcsp1h; section 3.9).** The 266-team end-of-season hang was the 10-bit coaching contract id; it is widened and the whole first 266-team off-season runs. Separate FCS stat leader lists are stored. FCS strength is retuned in the 266-team data. Next, in order:
  1. fix the 10 FBS coaching staffs lost at the 266-team rollover (likely one more 256-entry team loop);
  2. scale the recruit class with the number of schools;
  3. FCS postseason results at the end of the season, then a played SWAC title game;
  4. a screen for the FCS stat leaders.
- **Phase 1i (2026-10-31, agent fcsp1i; section 3.10).** The coaches lost at the 266-team rollover came from a 768-contract list in the end-of-season step; it is enlarged and the 266-team Dynasty now plays into 2027 with full staffs everywhere. The recruit class grows to 5,900. A full season of FCS results is measured, and the FCS postseason is written at the end of the season. Next, in order:
  1. fix the 266-team bowl and playoff selection;
  2. a second full season and the move into 2028 (rosters with the bigger classes, FCS tiers);
  3. a test season with slightly stronger top FCS tiers if wins stay below 8 %;
  4. a played SWAC title game and screens for the FCS bracket and stat leaders.
- **Phase 1j (2026-10-31, agent fcsp1j; section 3.11).** Bowl and playoff picks are correct with 266 schools; the Dynasty rolled into 2028. Next: FBS-vs-FCS game count after season 1, short rosters, the SWAC title game.
- **Phase 1k (2026-10-31, agent fcsp1k; section 3.12).** About 90 FBS-vs-FCS games from season 2, a played SWAC title game, the recruit class raised to 6,700.
- **Phase 1l (2026-10-31, agent fcsp1l; section 3.13).** 2028 finished into 2029 with 106 FBS-vs-FCS games, full rosters and staffs. Rating drift explained, and a fixed team-rating scale added. Next, in order:
  1. a player-level step so FCS win rates stay at 8-12 % over many seasons (tier-dependent FCS recruit strength, or a rollover rescale);
  2. the rest of 2029 and the 2030 rollover, measured per tier per year;
  3. the final rating scale (user decision; one setting);
  4. a new Dynasty with the 6,700-class data;
  5. screens for the FCS playoff and stat leaders.
- **Phase 1q (2026-10-31, agent fcsp1q; section 3.18).** The "Autosave in Progress" hang is a thread-slot leak in the PC port's runtime that can also hit normal play; fixed behind a switch in the test builds. The 2032 off-season is finished, and the top FCS level now signs the strongest classes. Next, in order:
  1. move the autosave fix into the play build;
  2. make the new recruiting settings the default and tune the FCS levels to target;
  3. follow the FCS win rate through the 2032 season;
  4. a new Dynasty with the new starting rosters.
