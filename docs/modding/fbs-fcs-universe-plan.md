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
