# FCS as a second Dynasty league: feasibility, limits and plan

Date 2026-10-29. Static analysis only: no game launch, no Ghidra run (the run queue was busy the whole session, so the queued batch below has not run). Target build: the PC port (`tools/ps3recomp-lane-e`) on the CFBR v21 + real2026 (138 FBS) + 12-team CFP stack. All addresses are CFBR v21 (01.02) unless marked "stock". Function names are ours. Confidence tags: confirmed / likely / guess.

Evidence sources:
- **SAVE**: the latest PC Dynasty save `save_backup/20261029-bowl-endseason` (138 FBS, 5 generic FCS, bowl week). It was parsed read-only with `scripts/inspect_tdb.py`.
- **ROSTER**: `analysis/assets/QKL_BOOT-0355.db`.
- **QX**: query strings in the CFBR ELF with their xref owners. The scratch tool behind this is described in section 9.
- Existing notes: MODDING_REFERENCE (MR) 1.A/1.B/2.B, `active138-proto.md` (A138), `playoff-proto-v3.md` (PV3), `continuation-checkpoint.md` fcs165 entry (FCS165), and the decompiles in `analysis/selected-functions` and `analysis/real2026-*`.

## 0. Verdict (short)

- **All of FCS (about 128 teams) is feasible as real TEAM rows with no players: TTYP 1, LGID 1.** The engine already models FCS this way.
  - The DB still ships a league table (`LEAG`: 0 "1A", 1 "FCS"), nine FCS conference rows and a `TTYP`/`LGID` parameter in most Dynasty queries.
  - The quick sim (SuperSim) rates a game from TEAM-level ratings, so a rosterless team can be simmed. That is how today's 5 generic FCS teams already play FBS teams.
  - The data limits fit: TEAM, STTM and the per-week tables need capacity raises, which are cheap template edits. The save grows by about 150 KB against 1.25 MB of headroom.
- **One gap blocks the rest. Static analysis cannot show what happens when two rosterless teams meet, or when an FCS team is the home team.** Today a generic FCS team is never the home team: 0 of its 114 regular-season games in the save. A one-day runtime test (Phase 0) on a save copy answers this.
- **Full FCS rosters with recruiting, coaches and player stats for all 128 teams cannot be done in practice.** That would need 266 "active" teams, past several hard limits:
  - 8-bit rank fields (255);
  - the 160-team storage reserve and 8-bit index loops;
  - the 8,278,016-byte save file (more than 2 MB over);
  - recruiting sized for one league.
- **A reduced rostered set fits inside the existing 160 reserve:** up to 22 real teams in active slots 139-160, about one or two conferences. Those teams would count as FBS in every TTYP=0 query, so every poll, BCS, bowl and CFP site would need a league filter. It is an optional later phase.
- **Recommendation:** design D2 (section 4). Real FCS teams as rated, rosterless TEAM rows, with C caves for:
  - the FCS schedule;
  - a stateless FCS poll;
  - the FCS playoff;
  - yearly rating drift;
  - a guard on the game-result recorder.

  FBS games against FCS teams then use real FCS schools automatically.
- **Effort:** core D2 (Phases 0-4) is about 3-4 agent-weeks. With native UI pages it is about 6-8 weeks. Section 7 has the breakdown.

## 1. How the engine treats FCS today (facts the design builds on)

| Fact | Evidence | Conf. |
|---|---|---|
| A league table exists. `LEAG` has 2 rows: LGID 0 "1A" and LGID 1 "FCS". `CONF.LGID` (16 bits) puts every conference in a league | SAVE `LEAG`, `CONF` | confirmed |
| CONF has 25 of 26 rows. The FCS conferences (LGID 1) are Ivy 6, MEAC 8, SWAC 12, Atlantic 10 18, Big Sky 19, Gateway 20, Southern 21, Southland 22, Ohio Valley 23, and Generic 17. WAC 14 has LGID 5; Historic 15, Fantasy 16 and High School 24 are other leagues | SAVE `CONF` | confirmed |
| The Dynasty holds 143 TEAM rows: 138 have TTYP 0/LGID 0, and 5 generic FCS teams have TTYP 1/LGID 1/CGID 17/DGID 30 (TGID 160-164, TORD 428-432, SGID 1023 = no stadium) | SAVE `TEAM` | confirmed |
| FCS teams have no players, depth chart or coaches, even in the roster file. Dynasty creation moves their coaches to TGID 1023 | SAVE/ROSTER PLAY, DCHT, COCH counts for 160-164 are all 0; FCS165; MR 1.B.4 | confirmed |
| Adding one more TTYP-1 identity (TGID 165) was runtime-proven. It survived fresh, cold reload, season and rollover, and the 2014 generator gave it 7 games | FCS165 (continuation-checkpoint, 2026-10-10) | confirmed |
| The SuperSim team loader `supersim_load_team_ratings` 0x12f7d0 loops over the 2 sides of a game. For each side it reads TEAM `TROF TRQB TRRB TWRR TROL TRDE TRDB TRDL TRLB TRST TROV` by TGID (query 0x16f90cc). It normalises with `max/min(TROV) where TTYP = 0` (0x16f9054/0x16f9090; the bound TTYP argument is `li r8,0`) | QX + disassembly 0x12f7d0..0x12f840 | likely |
| The week sim's game cursor `week_sim_game_cursor` 0x4a0434 selects every SCHD row in the week range with an open status. There is no team or TTYP filter, so FCS-vs-FCS rows would reach the sim | QX 0x1778258 | likely |
| Generic FCS teams are never the home team: 114 of 885 regular-season games involve FCS, and 0 have an FCS home team | SAVE `SCHD` | confirmed |
| Polls are recomputed only for one TTYP. The coaches/media poll pass 0x4cee28 uses `TEAM where TTYP = ? order by TCRK/TMRK`. FCS `TCRK/TMRK` stay at their roster values 127-131 in every save | QX 0x17794a8/0x1779630; ROSTER vs SAVE TEAM | confirmed |
| The schedule generator is TTYP-parameterised. RemainingGenerator 0x102f00 uses `TOID from TEAM where TTYP = ?`, called with 0. `fcs_opponent_pick` 0x10265c draws a random `TTYP = ? and TOID != ?` team, so FBS games against FCS would draw from all real FCS rows | QX 0x16f6ebc, 0x16f6e2c; stock decompile 102850.c, 1026ec.c | confirmed (stock), likely (CFBR) |
| Many Dynasty passes take LGID as a bound parameter. They are only ever called with 0: | QX | likely |
| - 25 sites run `select LGID from CONF where CGID = ?` | | |
| - 0x4740a8 `conference_count_by_league` | | |
| - 0x45cebc `conference_standings_league_cursor`: `STTM join TEAM where STTM.CGID=? and TEAM.LGID=? order by SNCT, tscs` | | |
| - 0x4f8f3c `league_team_cursor_by_conf` | | |
| - 0x4fa20c / 0x4db644 `league_conference_cursor_a/b` | | |
| - 0x4d4794 / 0x4f9cfc `league_team_cursor_a/b` | | |
| The engine still carries code from an older full-FCS design: `GetIsTeam1AA` (UI binding 0x89d878), the style class `NoDivsMiniConfForcedFcsGamesStyle`, and `AAPL` All-American rows keyed by TTYP | QX | confirmed (strings) |

## 2. Hard limits on team count (the limits table)

"Raise" says how a limit can be lifted: **DB** = template capacity edit (BOOT 354 GAMEMODE template; a save inherits capacities at creation), **cave** = code patch or C cave, **no** = practical wall. "Hits D2?" says whether the recommended design (rosterless FCS, all ~128 teams) runs into the limit.

### 2.1 Field widths and sentinels

| Limit | Value | Where | Raise | Hits D2? |
|---|---|---|---|---|
| TGID | 10 bits; 1023 = empty sentinel. The league index fill takes `TGID <= 1006` (`li 0x3ee` at 0x473df8) | TEAM and about 70 tables; MR 1.2 | no (width) | No. Free TGIDs exist: FBS uses up to 235, high-school teams 610-619, and the STTM custom-conference placeholders 630-806, so 236-609 is free for FCS |
| TOID | 10 bits, and must equal TGID (the CCG gate counts `TOID=TGID`) | MR 1.4 | no | No |
| PGID | 16 bits; 0xffff sentinel; team = PGID // 70, so at most 936 rostered teams | MR 1.3 | no | Only for rostered designs |
| TCRK/TMRK/TBRK (polls, BCS) | **8 bits unsigned (255)** | TEAM | DB can widen the schema, but code stores them with `stb`, so effectively no | No if FCS ranks are not stored there. Several queries read ranks **without** a TTYP filter: 0x1feb08 `TGID where TCRK = ?`, 0x45b590 `TGID where TBRK = ?` (bowl/CFP), 0x478a24 `TDNA where TBRK = ?`, 0x2d9230 `TCRK <= 25`, 0x4a4ddc `TCRK <= 10`, 0x1f2e24 polls UI. FCS rows must keep TBRK 0 and TCRK/TMRK above the FBS count, e.g. 255 |
| TORD | 10 bits (1023); FCS starts at 428 | TEAM | no | No (428-555) |
| CGID / DGID | 5 bits (0..31); DGID 30 = none | TEAM, CONF, DIVI, STTM, CCHH | no | CGIDs 25-31 are free (7); with the 9 existing FCS conference rows that gives 16 FCS conference ids, enough for the 13-14 real FCS conferences |
| SEWN | 5 bits (weeks 0..31) | SCHD, BOWL | no | No |
| SGNM (game number) | 8 bits, but **127 is the sentinel** (TSCH bye rows, unassigned BOWL rows). Regular-season SGNM restarts each week; postseason SGNM is one sequence across the postseason weeks | SCHD, TSCH, BOWL; PEM via MR | no | **Yes, a real ceiling: at most about 127 games per week across both leagues.** FBS uses 54-72 per week (week 1 = 72). 128 FCS teams add about 50-60, so week 1 lands near the cap. The FCS scheduler must cap each week's total at 126. The FCS playoff SGNMs must not collide with bowl SGNMs |
| TSWI / TSLO (season W/L) | 8 / 6 bits | TEAM | no | No. Real FCS teams play 11-12 games (generic teams reach 39 losses today) |
| Season sim week mask | 15-bit free-week mask (weeks 0..14); 12-game stop rule (`0xb < count`) | stock 0x102850 | cave | No (FCS plays 11-12 games) |

### 2.2 DB table capacities (SAVE values: used/capacity, row bytes)

| Table | Used/cap | Bytes/row | D2 need | Raise |
|---|---|---|---|---|
| TEAM | 143/192 | 328 | 271 (cap 320) | DB (+42 KB) |
| STTM (standings slots) | 320/400 (177 are TTYP-9 placeholder rows) | 16 | +128 (cap 560) | DB (+2.6 KB) |
| CONF | 25/26 | 28 | about 32 | DB |
| DIVI | 22/22 (full) | 44 | +0 (FCS uses DGID 30) or +2 for SWAC divisions | DB |
| SCHD | 926/2048 | 20 | about 926 + 650 FCS-only + 23 playoff = 1600 | fits |
| TSCH (team-week schedule) | **2268/2268 (full)** | 8 | about 4500 if FCS team pages are wanted | DB. **It is already full at 138 teams** (78 teams have 16 rows, 60 have 17). Check for silent truncation |
| SGIN (per-week game info) | 53/70 (in season) | 136 | about 130 per week | DB, if FCS-only games get rows (Phase 0) |
| STST (per-game team stats) | 104/140 | 100 | 2 per game | DB, same condition |
| SSUM, SWQT, S* per-week player stats | 445/2050, 209/350, ... | | no players, so likely +0 | maybe none |
| TSHS (team-season history) | 138/10240 (= 160 x 64) | 4 | 266 per season x 60 = 16k | DB (+24 KB), only if FCS history is kept |
| CCHH / BCHH | 10/1664, 34/2944 | 4 | no change if the recorder guard works (section 5.3) | none |
| STAD | 210/240 | 464 | FCS home games need an SGID: about 14 shared stadiums (one per conference), or 128 own (cap 340) | DB (+6 KB or +46 KB) |
| CSST / CNFR / SCRT (generator style tables) | 12/12, 180/180, 192/192 (all full) | | only if the stock generator is reused for FCS | DB |
| PLAY / DCHT / COCH | 9522/12600, 12144/14080, 439/768 | 120 / 8 / 176 | 0 for D2. D4b (22 rostered) fits: PLAY 11062, DCHT 14080 = exactly the cap, COCH 505 | fits |
| BOLN, BOFF, BDEF (season player stats) | **9178/9178 (full)**, 16415/16896, 26640/27028 | | 0 for D2 | existing risk at 138, separate from FCS |
| RTPB/RCTC/TEXP/TSSE, PTIP, RECB/RECV/RCPT (recruiting, FBS-only) | 138/160, 1932/2240, ... | | 0 for D2 | |
| LEAG | 2/2 | 36 | 2 | none |

### 2.3 Save file and memory

- **USR-DATA is a fixed 8,278,016 bytes** (0x7e5000, built at stock 0x334b1c/0x335554/0x3355d8).
- Most tables are stored at full capacity (alloc types 2/6/10/14). Only alloc 26/30 tables store their current rows.
- The bowl-week DB is 7,029,700 bytes, so **headroom is 1,248,316 bytes**.
- D2 growth is about 120-150 KB, which fits.
- Fully rostered FCS would add 2.2 MB or more and does not fit:
  - PLAY +9000 rows = +1.08 MB;
  - DCHT +90 KB;
  - the season player-stat tables (BOFF/BDEF/BKIC/PSxx) nearly double, +0.9 MB.
- On the PC port the save HLE is ours, so the size can be raised in principle: 3 game-side constants plus the in-memory DB buffer. But the buffer's storage class is unmapped (MR D.2 5.23).

### 2.4 Code-side arrays and loops (what caps "active" teams)

| Limit | Value | Where | Raise | Hits D2? |
|---|---|---|---|---|
| activeN storage reserve | **160 active (TTYP 0) teams**. Covers RecruitMan (160 x 12 / 160 x 376), RecruitPrefMan (160 x 24 cache, 160 x 76 array), board pool 5600 = 160 x 35, ranking/sort stack frames (126x16, 126x20 -> 160) and 72 N-dependent words | `patches/cfbr-activeN-proto-138` (552 words; builder refuses N > 160) | cave: rebuild with a larger RESERVE. Stack frames grow, e.g. 0x4a9078 0x90 x N, 0x4b47c8 3 x 28 x N | No (FCS stays TTYP 1) |
| 8-bit index loops | 0x4bd9d8, 0x4b7970 (stock) truncate the team index to 8 bits: 255 | A138 | cave | No |
| BCS pool | N+1, 1/N floats, points = 127 - rank (unsigned) | 0x4cbab0 (`bcs_rank_function`); stock 0x4ca8a0 | cave | No |
| All-team list | `TEAM where TGID<=1006 [and TVIS=1] order by TORD`, 12 B per entry, heap-allocated by count. Grows 143 -> 271 under D2 | `league_index_init` 0x474260 / `league_index_fill` 0x473df8 | dynamic | **Audit needed.** Some consumers index FBS-sized (160-reserve) arrays with the **all-team** dense index: PrefMan 76-byte array via 0x50df44 / 0x4bf8ac-equivalent, and board lists via 0x4acd20 (stock). This is safe only while those callers pass FBS teams, which sort first. Today's FCS indexes 138-142 are below 160, so any bug is latent; at 271 it would overflow |
| Conference generator | loops CGIDs 0..13 only (`cmpwi r22,14` at 0x100618, `cmpwi r23,14` at 0x1006f4; stock 0xffeec `% 0xe`) | `ConferenceGenerator` 0x10059c | cave | Only if the stock generator is reused (FCS CGIDs are 6, 8, 12, 18-31) |
| Style selector | null for conferences with 17 or more teams; `cmpwi 16`/`cmpwi 15` at 0x463198/0x4631b0 | `conference_style_selector` 0x4630fc | cave | No (FCS conferences have 6-13 teams) |
| CCG gate | conference has 12 or more teams with TOID=TGID, CGID != 5, and a BOWL CCG row (BIDX 33..44) | stock 0x45c7e0/0x45b484 | data | No. FCS conferences have no BOWL CCG rows, so they never get a CCG |
| UI literal-126 filters | 0x1e1660 (TCRK 126), 0x1e2ca0 (STDR 126), 0x1e1018 (stock) | A138 | cave | FCS rows with TCRK 255 are hidden, which is wanted |

**Summary.**
- The true walls are 255 (u8 ranks and 8-bit index loops) for any one ranked list, about 127 games per week (the SGNM sentinel), 31 conference ids, the 8.28 MB save, and 936 rostered teams (PGID/70).
- The 160 figure is a chosen storage reserve, not a field width. A cave can raise it toward 255, at stack-frame cost.
- D2 sits under all of these walls because FCS teams are not "active".

## 3. Can all of FCS fit? Designs ranked by effort and risk

| # | Design | What the user gets | Effort | Risk | Verdict |
|---|---|---|---|---|---|
| D1 | **Shadow league in a cave only.** The FCS teams, ratings, schedule and results live in cave memory plus a PC-port sidecar file; FBS still plays the 5 generic FCS teams | FCS standings, scores and playoff on new pages only. FBS opponents stay "FCS East" | low-medium (2 weeks) | low | Fallback only. It does not connect to FBS schedules, and the user wants one Dynasty |
| **D2** | **Real FCS teams as rated, rosterless TTYP-1/LGID-1 TEAM rows (about 128), simmed by the engine** | Real FCS schools as FBS opponents. Full FCS schedule, standings (W/L, conference), stateless poll, playoff, champion history (cave), year-to-year rating drift. User-played FBS-vs-FCS games keep working, because the engine generates a generic roster as it does today | medium-high (3-4 weeks core) | medium; one runtime unknown | **Recommended** |
| D3 | D2, but the cave sims FCS-vs-FCS games | Same as D2 | D2 + 3-5 days | medium-low | Automatic fallback if Phase 0 shows the engine cannot sim or record a game between two rosterless teams. The cave writes GHSC/GASC/GSTA and W/L before the week cursor reaches the game |
| D4b | A real rostered FCS subset in active slots 139-160 (up to 22 teams, about 2 conferences, e.g. Big Sky 12 + MVFC 10), TTYP 0, LGID 1 conferences | Playable FCS teams with real rosters, recruiting, coaches and player stats | high (3-5 weeks on top of D2) | high. Every TTYP=0 consumer counts them as FBS (polls, BCS, CFP and bowl pools, Top 25, recruiting rankings, the RemainingGenerator), so each needs an LGID filter. The data fits the reserve | Optional later phase |
| D4 | All of FCS rostered and active (N = 266) | Everything | very high (months) | very high. It crosses u8 ranks, the 8-bit indexes, the 160 reserve (stack frames), the save size (+2.2 MB) and recruiting volume | Not practical |

"Slots 139-159+" from the brief is D4b. It works for one or two conferences, not for all of FCS.

## 4. Recommended design D2 in detail

### 4.1 Data (Phase 1)

Each FCS school gets a TEAM row with:
- TTYP 1 and LGID 1 via its conference;
- TVIS 1 (Dynasty creation forces this anyway, per FCS165);
- TGID = TOID in 300..427;
- TORD 428 and up (after the generic FCS rows);
- CGID set to a real FCS conference, DGID 30;
- names and abbreviations;
- TROV/TROF/TRDE and the position-group ratings set from real strength (top FCS just under the FBS minimum TROV of 67; low FCS around 45-55);
- TCRK = TMRK = 255 and TBRK = 0;
- SGID set to a shared per-conference FCS stadium.

The 5 generic rows stay as filler, or are retired once the real rows schedule correctly.

Conferences: 9 CONF rows exist (rename them to the 2026 alignment) and 5-7 new ones go at CGID 25-31. CONF capacity rises to 32. TEAM, STTM, STAD, SGIN, STST, TSCH and TSHS capacities rise as in table 2.2. All of these are template edits with the existing reserve tools (`tdb_capacity.py`, the v6 reserve recipe). A **new** Dynasty is needed, because capacities are fixed per save (MR 1.B.9).

Community packs that carry FCS names and ratings can be used under the community-assets policy (credits list; no EA files in the public repo).

### 4.2 Schedule (Phase 2)

1. The stock FBS generator runs unchanged. Its FCS filler (0x102d9c `random_fcs_filler` and 0x10265c `fcs_opponent_pick`) now draws real FCS teams for FBS non-conference games. Optional refinement: weight by geography or conference tier through a cave on 0x10265c.
2. A C cave `fcs_schedule_build` hooks the end of `ScheduleGenerator_driver` 0x103714, after the FBS rows exist and before `SGNM_numbering` 0x1034ec. It:
   - builds each FCS conference round robin (or rotation for 11+ teams);
   - fills non-conference FCS-vs-FCS games up to 11 per team, honouring the FBS games already placed;
   - assigns home/away;
   - caps every week at 126 games across both leagues;
   - leaves weeks 14-15 free for FCS teams;
   - inserts through the same SCHD insert query as `schedule_row_insert` 0x100364.

   This does not reuse the stock generator for FCS: that would need the CGID-0..13 loop raised, CSST/CNFR/SCRT rows (all full) and the MISC preset tables. The model is built and checked offline first in Python, as `build_schedule138_proto.py` was.
3. Rollover: the same hook runs every season. The generator runs per season (stage 0x4da01c "Generating Schedule").

### 4.3 Season flow (Phases 0 and 3)

- **Sim.** The week cursor 0x4a0434 already picks every open SCHD row, and SuperSim needs only TEAM ratings. Phase 0 must prove three things:
  - (a) a game between two rosterless teams sims and commits (`game_result_function` 0x4f01c8 / stock 0x4ed948);
  - (b) an FCS home team with a shared SGID works;
  - (c) SGIN/STST rows for such games stay within capacity.
- **Standings.** TSWI/TSLO and the conference records update in the result commit for any team. FCS conference standings come from `conference_standings_league_cursor` 0x45cebc with LGID 1, or from a cave that computes them from SCHD. Which one depends on whether the stock standings pass loops only LGID-0 conferences (Phase 3 check).
- **FCS poll, stateless.** A cave computes the Top 25 on demand from SCHD results and TEAM ratings (win%, margin, opponent strength). Nothing is stored in TCRK/TMRK/TBRK, so the u8 rank collision is avoided. The preseason order comes from TROV.
- **Rating drift at rollover.** A cave on `season_rollover_stage` 0x5076d8 nudges FCS TROV and the group ratings: regression to the conference mean, plus a bonus for wins and playoff runs, plus noise. No rosters are involved.
- **History.** FCS champions and conference champions go to cave-owned rows. Options: a new small TDB table in the template (it must survive save/load, which Phase 0 tests), or a PC-port sidecar file per save slot. TSHS rows are kept only if TSHS is raised.

### 4.4 Playoff (Phase 4)

See section 5.

### 4.5 What D2 does not give

FCS player rosters, player stats, recruiting, FCS coaches (carousel) and an FCS user team. Those need D4b for a subset.

## 5. Schedule generation and CFP/playoff logic for a second league

### 5.1 What exists

- The generator driver runs the conference, user-vs-user, preference, annual, known and remaining sub-generators.
- FCS appears only as filler opponents (`random_fcs_filler`, `fcs_opponent_pick`), with 35 + random(16) filler games and 100 attempts per season.
- The conference generator covers CGIDs 0..13 with CSST style names.
- There are no bounds checks against preset caps (MR 1.B.2).

### 5.2 Changes for FCS

- **Required:** the FCS schedule cave (4.2) and a weekly game-count cap of 126.
- **Optional:** weight `fcs_opponent_pick` so FBS teams draw nearby or realistic FCS opponents, and limit each FCS team to at most 2 FBS games.
- **Not needed:** CGID-loop or style changes, because FCS does not go through the stock conference generator.

### 5.3 Postseason and the game-result recorder

The recorder `game_result_function` 0x4f01c8 (stock 0x4ed948) inserts:
- a **CCHH** row (conference champion) for every game whose SEWT is 16;
- **BCHH** rows (bowl history) for games in SEWT 30-40, keyed by BOWL (SEWN, SGNM).

FCS playoff games in those weeks would write false conference titles or bowl wins for FCS teams. The fix is a small **recorder guard** cave: skip the CCHH and BCHH inserts when both teams are LGID 1. The CFP v2 "C1 recorder fix" already patches this function, so there is precedent.

FCS postseason SGNMs must be unique within the postseason sequence and must not equal any BOWL row's SGNM in that week. A reserved range such as 100-126 works.

### 5.4 FCS playoff cave

- **Bracket.** The real 24-team format is 10 automatic bids for conference champions plus 14 at-large, with the top 8 seeds getting byes, over 5 rounds and 23 games. A 16-team, 4-round version is a simpler first step.
- **Selection.** Run it after the last FCS regular-season week (SEWN 13), using the stateless FCS poll and the FCS conference standings. FCS has no CCGs.
- **Weeks.** Proposed: R1 at SEWN 14 (FBS rivalry week with about 18 games, so there is room), R2 at SEWN 15, QF at 17, SF at 18 or 19, F at 20 or 21. Each week's SEWT matches the bowl weeks, as the CFP cave does.
  - Avoid SEWN/SEWT 16, the CCHH week.
  - SEWN 15 is empty in stock and skipped by `week_advance` 0x4d00ec. Putting games there makes it a played week, and its calendar label and stage effects must be checked in Phase 4.
- **Advancement.** Same pattern as the CFP v3 cave: a hook at end of week (`end_of_week_processing` 0x4cfa3c) reads the round results (GSTA 2/3) and inserts the next round's SCHD rows.
- **Implementation.** Write it in C (the C cave direction), sharing helpers with the CFP cave but not its BOWL rows. BOWL is 45/46 with BIDX 8 bits, and FCS games do not need BOWL rows if the recorder guard is in place.
- **Champion.** Recorded in cave history (4.3) and announced by a news item, as with the CFP news fix. TEAM.NCYN/NCYR are FBS national-title fields; FCS titles should not use them.

### 5.5 CFP isolation (no change expected)

The CFP and bowl pools filter on `TTYP = ?` (0x45aec8 `bowl_at_large_candidates`, 0x45cd38) or on `TBRK = rank >= 1` (0x45b590). FCS rows keep TTYP 1 and TBRK 0, so they never enter the CFP. Phase 0 checks this on a save copy.

## 6. UI impact

| Area | Today | With D2 | Work |
|---|---|---|---|
| Conference pickers (standings, stats) | `CONF where LGID = ?` (0x196000, 0x196500, 0x197028; the table builder 0x1ab17c) bound to LGID 0 | FCS conferences can appear by binding LGID 1. A league toggle on these pickers may expose stock standings for FCS conferences cheaply | Cave or patch on the bound LGID plus a toggle; check that the standings screen reads STTM/TEAM per CGID |
| Team lists, Play Now team select | `TEAM where TTYP = ? [and TVIS=1]` (0x215008, 0x1a36bc) | FCS not listed (TTYP 0 only) | Optional: TTYP-1 list for viewing FCS team pages |
| Weekly scores | shows all SCHD games of a week | FCS games appear among FBS scores (about 120 rows per week) | Check list capacity; possibly filter by league |
| FBS team schedules | show "FCS East" style opponents | show real FCS names | none; logos and uniforms fall back to generic FCS art (`GetIsTeam1AA`) unless community art is added |
| Top 25 / polls | TTYP-0 polls | FBS unchanged. The FCS Top 25 needs a new page fed by the cave poll | new in-game page (UI page pipeline, `docs/modding/07-in-game-ui-pages.md`) |
| Playoff bracket | CFP bracket view (playoff-bracket-ui) | needs a second bracket (FCS) | extend the bracket page with a league toggle |
| Team rankings filters | literal-126 filters 0x1e1660/0x1e2ca0/0x1e1018 | FCS with TCRK 255 hidden, as wanted | none |
| News | CFP news cave | FCS champion and upset news | small cave with new strings |
| Stats leaders, recruiting, coach screens | FBS only | unchanged (no FCS players) | none |

The user wants native in-game pages, not an overlay. The UI page pipeline (TU archive with rebuilt movies, `ui_pages`) is the route. Its Play-Game load hang (`cfp-load-hang.md`) must be fixed first, because every new page depends on it.

## 7. Phased plan and effort

| Phase | Content | Exit test | Effort (agent-days) |
|---|---|---|---|
| 0 | **Runtime feasibility on save copies, through the run-queue only.** Raise TEAM/STTM/STAD/SGIN/STST capacities in a test template and add about 128 FCS rows. On a save copy, inject FCS-vs-FCS SCHD rows (FCS home team, shared SGID) into an upcoming week. Sim the week, save, reload, roll over. Test whether a new template table survives save/load. Run the all-team-index consumer audit (271 entries vs the 160 reserve) statically first | no crash; scores, GSTA and W/L written; CFP pool unchanged; save fits | 2-3 |
| 1 | FCS data pack: names, 2026 conferences, ratings, TGIDs, CONF rows, stadium mapping. Template capacities. Offline checker | checker passes; new Dynasty boots | 3-4 |
| 2 | Schedule cave plus offline Python model; weekly cap 126; rollover | every FCS team has 11 games, at most 126 games per week, both seasons | 3-5 |
| 3 | Standings, stateless poll and rating drift caves; FCS history storage | poll and standings match the offline model | 3-5 |
| 4 | FCS playoff cave plus recorder guard plus champion news | 16-team (then 24) bracket completes; no false CCHH/BCHH rows | 4-7 |
| 5 | UI: league toggle on conference pickers; FCS Top 25 and bracket pages | pages show live data | 7-15 (depends on the UI pipeline fix) |
| 6 (optional) | D4b: one or two rostered FCS conferences in slots 139-160 with LGID filters across polls, BCS, CFP, bowls and recruiting rank | FCS teams playable and recruiting, FBS pools unchanged | 15-25 |

Core D2 (Phases 0-4) takes 15-24 agent-days, about 3-4 weeks. With UI (Phase 5) it is about 6-8 weeks. D4b adds 3-5 weeks. Release and installer work comes after a complete game, per the project priority.

## 8. Open questions and risks

1. Two rosterless teams in one game, and an FCS home team. This is the Phase 0 core. If it fails, use D3.
2. All-team-index consumers that index 160-reserve arrays (0x50df44, the 0x4bf8ac-equivalent, 0x4acd20 stock) when the list holds 271 entries. Do a static audit before Phase 1; the fallback is to raise the reserve for those arrays only.
3. SGIN/STST semantics. In-season SGIN held 53 rows for a 62-game week, so it is not "every game". Which games get rows decides whether those tables need raising.
4. TSCH is full (2268/2268) at 138 FBS. Check for truncated team-week rows now. This is independent of FCS.
5. BOLN is full (9178/9178) at bowl week. This is an existing stats-capacity risk at 138, independent of FCS.
6. Week 15 as a played week (FCS R2): calendar label and stage effects.
7. Whether stock standings and other passes run for LGID-1 conferences. Determine this from the LGID-parameter callers, using the queued decompile batch.

## 9. Function names added (cfbr_direct_names.psv)

Added this pass (system / confidence; evidence = query-string xref owner + disassembly):

| CFBR | Name | Evidence |
|---|---|---|
| 0x12f7d0 | supersim_load_team_ratings | queries 0x16f9054/0x16f9090 (max/min TROV, TTYP=0) and 0x16f90cc (11 team ratings by TGID); 2-side loop |
| 0x4a0434 | week_sim_game_cursor | query 0x1778258 (SCHD by SEWN range and GSTA set, ordered by SEWN, GDAT, GTOD, SGNM) |
| 0x4cee28 | polls_update_coaches_media | queries 0x17794a8/0x1779630 (TEAM where TTYP=? order by TCRK/TMRK) and the updates 0x1779580/0x17796d8 |
| 0x4ce508 | teams_by_overall_cursor | query 0x1779268 (TEAM where TTYP=? order by TROV desc) |
| 0x4740a8 | conference_count_by_league | queries 0x176d404/0x176d44c (CONF count where CGID<=? and LGID =/!= ?) |
| 0x45cebc | conference_standings_league_cursor | query 0x1767840 (STTM join TEAM where CGID=? and LGID=? order by SNCT, tscs) |
| 0x45aec8 | bowl_at_large_candidates | query 0x1766d34 (TTYP=?, CGID!=?, TBRK<=?, TSWI>=?) |
| 0x45cd38 | postseason_candidates_by_snct | query 0x17672d0 (TTYP=?, CGID!=?, order by SNCT, TBRK); role guess |
| 0x45b590 | team_by_bcs_rank | query 0x1766ed8 (TGID where TBRK=?) |
| 0x4f8f3c | league_team_cursor_by_conf | query 0x178baf4 (CONF join TEAM where CONF.LGID=?) |
| 0x4fa20c | league_conference_cursor_a | query 0x178be24 (CGID from CONF where LGID=?) |
| 0x4db644 | league_conference_cursor_b | query 0x178583c (same shape) |
| 0x4d4794 | league_team_cursor_a | query 0x1783d0c (TGID from TEAM where LGID=?); next to coach_contract_ensure |
| 0x4f9cfc | league_team_cursor_b | query 0x1783d0c |
| 0x4f5be8 | dynasty_create_nonfbs_coach_cleanup | queries 0x178a560/0x178a5e8 (TEAM where TTYP in 5/7 values) and 0x178a688 (delete COCH where TGID=?) |
| 0x89d878 | ui_GetIsTeam1AA_binding | string `GetIsTeam1AA` 0x17e9d5c |
| 0x196000 | ui_conference_list_by_league_a | query 0x170517c (CONF where LGID=?) |
| 0x196500 | ui_conference_list_by_league_b | query 0x1705290 (LGID=? and CGID!=?) |
| 0x197028 | ui_conference_list_by_league_sorted | query 0x17053e4 (order by CNAM) |
| 0x1ab17c | ui_conference_table_build_by_league | query 0x1707e38 (insert select CONF where LGID=? and CGID!=?) |
| 0x215008 | ui_team_list_by_type_visible | queries 0x16db6b8/0x1715638 (TTYP=? and TVIS=1 order by TORD) |
| 0x1a36bc | ui_team_list_by_type_name | query 0x1706b74 |

Sites (not functions): the conference-loop bounds 0x100618 / 0x1006f4 (`cmpwi 14`) in ConferenceGenerator 0x10059c, and the style-selector bounds 0x463198 / 0x4631b0.

Tool used: a scratch script that lists every NUL-terminated ELF string matching a regex, decodes reversed tags and finds lis/addi and TOC xrefs. It is the same method as `scripts/string_owners.py`, generalised to regex. It is not saved in the repo; rebuild it from `string_owners.py` if needed.

Queued Ghidra batch (`scripts/wait_idle_decomp.sh analysis/mapping-cfbr-fcs "<spec>"`, started 2026-10-29, log `analysis/batch-fcs.log`):
- 12f7d0, 10265c, 102f00, 4cee28, 4ce508, 4740a8, 45cebc, 4cbab0, 4f8f3c, 4fa20c, 4db644, 4d4794, 4d48d4, 4f9cfc, 89d878, 4630fc, 463238, 4632dc, ff8f4, 45aec8, 45cd38.
- If `analysis/mapping-cfbr-fcs/` does not exist, the queue never idled. Rerun the same command.

## 10. Handoff

- **Done:** limits table (section 2), designs (3), recommended D2 (4), schedule and playoff changes (5), UI (6), plan (7), 22 function names + 2 sites (9). Mapping docs updated (`docs/mapping/sim-and-slots.md` item 5, INDEX.md, HANDOFF.md). Public mirror `docs/modding/fcs-league-feasibility.md`, committed locally, not pushed.
- **Next, in order:**
  1. When the batch output exists, read 0x12f7d0 (does SuperSim need anything per player?), 0x45cebc and 0x4740a8 (are standings computed for LGID 1?), and 0x4cee28. Update sections 1 and 4.3.
  2. Static audit of all-team-index consumers against the 160 reserve (risk 2).
  3. Phase 0 test plan as a run-queue request on a save copy.
- **Environment:** the run queue was busy all session (LOCK held, integrator26 s86 running, 5 pending). C: had 50 GB free.
