# Simulation, progression, draft, injuries and team-slot ceiling (items 4 and 5, static pass 2026-10-28)

Sources: string xref owners (`scripts/string_owners.py cfbr`), existing decompiles in `analysis/mapping-cfbr-recruiting/`, and TDB schemas of `QKL_MISC-0145.db` (the Dynasty template, 175 tables). Confidence tags: confirmed / likely / guess. Function names are ours.

## Item 4: offseason stage owners (from status-text strings)
| CFBR address | Name | What | Confidence |
|---|---|---|---|
| 0x481e20 | pro_draft_requests_and_redshirts | "Players Leaving" stage: runs 0x47fb8c (`Designating Redshirts`), a graduating-seniors query (`Graduating Seniors`), 0x47f758(0) (`Receiving Pro Draft Requests`), 0x4810a0 (`Receiving Transfer Requests`) | confirmed (decompile) |
| 0x489664 | leaving_status_text | formats a player's leaving status code: 1-7 Declaring (Projected Round n); 8-15 handled by 0x489500; 0x10 Staying: Pro Draft; 0x11-0x12 Staying: Transfer; 0x13-0x19 Pro Draft (Projected Round code-0x12); 0x1a Graduation. So the draft has 7 rounds and early entry is a status code, not a table | confirmed (decompile), earlier note called it "staying" only |
| 0x4835a8 | graduation_ceremonies_stage | `Commencing Graduation Ceremonies` (progress `%.0f%%`) | likely (string) |
| 0x4934c8 | recruit_class_source_players_build_RCTN | `Training Players` and `insert into RCTN select * from PLAY ...` (RCTN = 8820-row copy of players), divides PGID by 70. It is the offseason player pass that feeds recruiting-class bookkeeping; whether ratings progression happens here is NOT shown | likely (name), guess (progression role) |
| 0x4d4608 | coach_contract_update_stage | `Updating Coach Contracts - %d remaining` | likely |
| 0x1f0efc | coach_retirement_news | `has retired from coaching at age %u` | likely |
| 0x1e9598 | injury_update_news | `Injury Update: %s - %s` | likely |
| 0x46bce0 | injury_table_writer_INJY_INJR | decompile shows a mode-driven (0..6) pass over a result set, reducing injury lengths (INJL) with random 0..8 + 2 re-injury style rolls via the RNG at DAT_01cf9a78; it updates INJY and writes INJR. Looks like the weekly or stage-wise injury recovery/ageing step, not the in-game injury roll | likely (role guess) |
| 0x47362c | injury_insert_INJY | `insert into INJY set TGID, PGID, INJL, INJT, INJR, SEWN` | likely |
| 0x2dffe0 | injuries_enabled_setting | `Injuries Enabled: %d` | likely |

Injury tables: INJY (template 0/513: TGID PGID INJL INJT INJR SEWN), INJR (0/25: PGID), SINJ (0/400, season injuries, schema not yet read), PLAY.PINJ (injury rating 7b, likely) and the UI strings `Injury Length`, `Injury Rating`, `Injury Type`, 12 body-part strings ("Strained back", "Strained Achilles", ...).
Draft tables seen in the template: PPRO (0/4305, same capacity as RCPT: prospect list for the pro draft, guess), PRLU (32/34), SRET (0/750, retirees, guess), RCTN. Draft-class download strings (`Download Draft Class`) belong to the online draft-class feature.
Not located statically: the sim-time injury roll, rating progression (development) formula, early-entry decision formula, and play-calling/AI entry points. Batch 1 (below) decompiles the draft and request functions to find the first two.

## Item 5: team-slot ceiling beyond 138 (data-structure view)
Field widths in the Dynasty template (`QKL_MISC-0145.db`) that bound a team count:
- Team id: `TGID` is 10 bits in 70 tables (max 1023, and 1023 is the empty sentinel); `TOID` 10b.
- Player id: `PGID` is 16 bits with 0xffff as a sentinel, and the rule team = PGID // 70 gives at most 936 team slots even if everything else allowed it.
- Ranks: TEAM `TCRK/TMRK/TBRK` are 8 bits (255); `TORD` 10b; `TRDE/TROF` 8b.
- Conferences: `CGID` and `DGID` are 5 bits (31 conferences/divisions; CONF has 25 of 26 rows used, DIVI 22).
- Capacities (template): TEAM 146 (v6 reserve recipe 192), PLAY 9100 (12600), DCHT 11464 (14080), COCH/CSKL 409 (768), PTIP 1764, RECB 4410, RCTC 126, TSHS 7560, RBKS 3402/3643, TPHS 572/572 full.
- Code side (from MODDING_REFERENCE 1.A and the activeN notes): literal 126 sites (BCS count 0x4cea2c, TEXP init 0x4d3fb8, UI filters 0x1e1660/0x1e2ca0/0x1e1018/0x1a2e3c, the "Choose Your First Job" view of 126 rows) and 8-byte-per-team arrays with 0x3f0 (126 x 8) capacity at 0x50be80 which activeN raises to a 160-team cap.
Conclusion (likely): the engineered ceiling is 160 teams (the activeN design cap), the next structural limits are the 8-bit rank fields (255) and PGID (936), and the conference field (31). Exceeding 160 needs every 126/160 array and the unlisted heap arrays re-scanned. Not yet verified in code beyond the earlier notes.

## Batch 1 (queued for the next runqueue gap)
Output `analysis/mapping-cfbr-batch1/` (local). Functions: commit decision 0x4b9ffc, 0x4b8f40; progression 0x4ba384; visit evaluation 0x4af390; week-1 forced commit helper 0x4b9918; visit-score sub-scores 0x4acc78, 0x4ad1a0, 0x4ad36c; RCAT row loader 0x494954; name loader 0x494884; head/appearance setter candidate 0x491560; draft/request chain 0x47f758, 0x47fb8c, 0x4810a0, 0x489500, 0x4835a8; training pass 0x4934c8.

## Item 5 update: FCS second league (2026-10-29)
Full analysis in `docs/realism/fcs-league-feasibility.md` (limits table, designs, plan). Key data points:
- The real walls are the u8 ranks TCRK/TMRK/TBRK (255; several rank queries have no TTYP filter: 0x1feb08, 0x45b590, 0x478a24, 0x2d9230, 0x4a4ddc), the 8-bit index loops (255), the SGNM sentinel 127 (about 127 games per week across all leagues), CGID 5 bits (31), PGID//70 (936 rostered teams), and USR-DATA 8,278,016 bytes. The bowl-week PC save uses 7,029,700, so headroom is 1,248,316 bytes.
- The 160 cap is the activeN storage reserve (a design choice), not a field width.
- FCS teams in Dynasty are rosterless TTYP-1/LGID-1 TEAM rows. LEAG (0 "1A", 1 "FCS") and nine FCS CONF rows ship in the DB. SuperSim reads TEAM-level ratings (0x12f7d0), and the week cursor 0x4a0434 has no team filter.
- Capacities touched by an FCS league: TEAM 143/192, STTM 320/400, CONF 25/26, DIVI 22/22, TSCH 2268/2268 (full already), SGIN 53/70, STST 104/140, STAD 210/240, SCHD 926/2048 (fits).
- ConferenceGenerator 0x10059c loops CGID 0..13 (`cmpwi 14` at 0x100618 / 0x1006f4).
- 24 names (22 functions, 2 sites) were added to `cfbr_direct_names.psv`, tagged "FCS pass 10-29".

## Batch 1 results: offseason player flow (2026-10-30, analysed from `analysis/mapping-cfbr-batch1/`, local only)
Confidence labels as elsewhere; SQL strings are read from the ELF (tags byte reversed) and are the primary evidence.

### Stage order inside "Players Leaving" (0x481e20)
`Designating Redshirts` 0x47fb8c, `Graduating Seniors` query, `Receiving Pro Draft Requests` 0x47f758(0), `Receiving Transfer Requests` 0x4810a0 (confirmed in an earlier pass); `Commencing Graduation Ceremonies` 0x4835a8 and `Training Players` 0x4934c8 are separate offseason stages (callers 0x50104c and 0x501588 respectively, both in the offseason driver region).

### Redshirts, 0x47fb8c `redshirts_designate` (likely)
`select PGID from PLAY where PRSD = 0 and PGID != 0xffff` (PRSD = redshirt state, 0 = not redshirted, 1 = redshirted/used). For each such player, if the per-player byte at `DAT_01c88188[PGID]` is zero (the player did not appear, flag filled by the season code) and the manager call 0x47cf28(handle, PGID, 4) also reports 0, the code runs `update PLAY set PRSD = 1 where PGID = ?` and decrements a per-team counter. So redshirts are assigned automatically to players who did not play; the user's team can override through the UI callbacks (DAT_01c85dbc).

### Pro draft requests, 0x47f758 `pro_draft_requests_receive` (confirmed shape, thresholds likely)
- Loop over 17 position ids (PPOS 0..16, the loop ends at `> 0x10`). The position enum seen in the size table below is QB, HB, FB, WR, TE, T, G, C, DE, DT, OLB, MLB, CB, FS, SS, K, P.
- Per position a seven-tier quota (one tier per projected draft round, local array of 7 x 0x44 bytes) is built by 0x47f5c4; the candidate cursor is `select PLAY.PGID, TGID, PHGT, PWGT, PYEA, PRSD from PLAY join TEAM where PYEA != ? and PPOS = ? [or PPOS = ?] order by PLAY.POVR desc, TEAM.TCRK asc` (second form with two alternative positions), i.e. best overall first, ties broken by better team rank. Fetches run until the tier quotas are exhausted.
- Eligibility per candidate: (a) class year 3 with PRSD != 1 is the "must leave" case (graduating or out of eligibility; skips the random roll); (b) class year 1 requires PRSD != 0 (a non-redshirted sophomore cannot declare; redshirted sophomores can) (likely); (c) teams whose `TOID` is 1, 8, 0x39 or 0xbd are excluded (guess: service academies); (d) minimum size per position from the table at `0x1c86938` (u16 height in, u16 weight lb; weight uses PWGT + 160): QB 73/200, HB 70/175, FB 70/220, WR 70/175, TE 74/220, T 74/280, G 72/280, C 72/260, DE 72/245, DT 72/275, OLB 70/225, MLB 70/225, CB 69/170, FS 70/185, SS 70/185, K and P 0/0 (no minimum) (confirmed values; the position order is inferred); (e) in mode 0 and for non-forced players a d100 roll against `0x47f330(PGID, tier)` (the declaration probability, formula in batch 2).
- On success `update PLAY set PTYP = 3 and PLFL = code where PGID = ?` (PTYP 3 = leaving for the pro draft, PLFL = leaving status). Mode 0 writes code = tier + 1 (1..7, "Declaring (Projected Round n)"); other modes write tier + 0x13 (0x13..0x19, "Pro Draft (Projected Round n)") and also call 0x47eec0 for tiers 0x13..0x19. This matches the status text decoder 0x489664 exactly. Tier fill order: a tier advances when its per-position quota is reached (`while (quota[tier] <= taken) tier++`).
- Draft strength is therefore: how many players per position get a round (0x47f5c4), the size minima, and the declaration probability (0x47f330); the actual NFL draft order and results are not generated here.

### Transfers, 0x4810a0 `transfer_requests_receive` (confirmed shape, formulas open)
- Progress text `Receiving Transfer Requests... %d%%`. Candidate cursor: `select PLAY.PGID, PPOS, POVR, PYEA, CITY.CYSI, PLAY.RCHD, PRSD from PLAY join CITY on PLAY.RCHD = CITY.RCHD where <team filter> and PLAY.PYEA <= ?` run per team (teams iterated through `select TEAM.TGID, STAD.STAT, TEAM.TRIV from TEAM join STAD ... where TGID >= ? and TGID <= ? and TTYP = ? order by TORD`; TGID range 0..0x3ee). Skips players already in TRAN (`select count(*) from TRAN where PGID`), players with a pending draft entry (OSPA `POAT/POAR/SEYR` count) and a coach-turnover case.
- Each eligible player gets five component scores added to one total: playing-time score A `0x480380(team, player, cfg)`, playing-time score B `0x480580`, playing-time score C `0x4809a0`, a broken-promises score (three promise kinds 0, 2, 4, each present when `0x47cf28` and `0x47e188 == 1`, each adds a gamedata value at config offsets 0x237, 0x24c, 0x238), and a coach-leaving score `0x480ba0`. The player transfers when `total >= cfg[0x1fe]` (or when the forced flag is set).
- Reason code = the largest component: default 10 (score A), 11 (B), 13 (C), 12 (promises), 14 (coach leaving, destination = the departing coach's new team, `0x480da8`, if known). A home-sick override: when the player's state differs from the team's state byte and `rand(100) < cfg[0x245]` the reason becomes 15 and `cfg[0x202]` is added to the total; the destination is then restricted to teams of the player's home state. The strings by code (0x489500): 10, 11, 13 "Playing Time"; 12 "Broken Promises"; 14 "Coach Leaving"; 15 "Home Sick"; 8 "Transfer - %s", 9 "Transfer - %s (Leaving)".
- Destination search starts at a random entry of the candidate team list (record size 0x2c), skips the same team, enforces a per-destination incoming cap (halfword pair cap/used at +0x21c/+0x21e per entry) and accepts when the fit score `0x47dd10(...)` is above 6 and, unless the reason is 14, the second score `0x47d3fc(...)` is above 6. Then the player is written: `insert into TRAN set PGID, PTID (destination), TRYR, TRAC`, `update PLAY set PTYP = 1`, `update PLAY set PLFL = reason`, `delete from PLSS`, `insert into PLSS set PGID, WTLS (total + cfg[0x1f8]), CTSP, CSPL`. A per-run cap of transfers is the u16 at `cfg[0x200]`.
- Tuning: all thresholds sit in one 0x25a-byte gamedata record (fetched through `0x9a9168`, `DAT_00481088/90`), so the transfer rate is a data-only knob; the record's DB table has not been located yet (batch 2 follow-up: find the owner of `DAT_00481088`).

### Graduation, 0x4835a8 `graduation_ceremonies` (confirmed shape)
Status text `Commencing Graduation Ceremonies` with a percentage. Creates the DCHT index by PGID, then selects the PLAY rows with PTYP = 3 (the leaving players; a table-range filter on PLAY.PTYP 3..3, so draft entrants are included) and loops over them: per player 0x48328c(0, 0, 0x3ff, 1, 1) performs the graduation (moves the player out of the roster; the handler is in batch 2), a row of `PPRO` is deleted (`delete from PPRO where PGID = ?`), and 0x482a20 plus 0x48230c(`DYND`, `ELMT`) clean up the shared tables. It creates no ratings; it is roster bookkeeping.

### Training / progression, 0x4934c8 `players_training_progression` (likely; replaces the earlier RCTN guess)
- Status text `Training Players`. Before the loop: `0x43f6bc(0, 'ARRT'/'GPTW')` pushes two table-state markers, `0x492cd8` (the gamedata loader that fills the 3 x 17 x 49-byte archetype table at `0x1cfd6f0`) and `0x493288` run, then `insert into RCTN select * from PLAY where PTYP != 3` copies all non-leaving players into the RCTN work table (a backup/compare copy used by the training update).
- Main cursor: `select PGID, PPOE, PRSD, PPOS, PTEN from PLAY where PTYP != ?`. For each row the team is `PGID / 70` (magic multiply 0xd41d41d5). When the team changes it asks `select CCID from COCH where TGID = ? and CFUC = 1` (does the team have a coach flagged CFUC; the result sets a boolean that is passed inverted to the manager object at `DAT_01c88d7c` vtable +0xc/+8 with the team and 1) and reads a 0x68-byte tuning record via `0x9a9168` / `0x9a94a0`. The training amount for the player is `0x491878(team)` unless the manager call returns 1, in which case the record halfword at +0x52 is used (a minimum of 12 entries is required, otherwise a default record). Then `0x4929e0(&row, amount, 0x21, 1)` applies the progression to that player's ratings (batch 2).
- After the loop: `update PLAY set PGGM = 0 and ...` (reset of the games-played counters), and for each team in the list at `DAT_01c86918` (stride 0xc, count `DAT_01c86920`) `0x482940(team)` is called until one returns non-zero (post-training team pass, batch 2).
- Interpretation: one annual pass at the end of the offseason that raises ratings with a per-team training strength (coach/program based, distinct handling for coach-controlled teams), reading position/archetype tables (`0x1cfd6f0`, also used by the recruit generator). The per-attribute development kernel is therefore shared with prospect generation (0x491560, see recruiting.md section 11.5).

### Names added (see cfbr_direct_names.psv)
0x4835a8, 0x4810a0, 0x47f758, 0x47fb8c, 0x489500, 0x4934c8 (renamed), plus the recruiting names in recruiting.md section 11.
