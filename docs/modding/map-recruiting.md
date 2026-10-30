# Recruiting system map (CFBR v21 addresses unless marked STOCK)

Status: first pass. Evidence = string cross-references in the CFBR ELF (`scripts/string_owners.py`, `scripts/query_owners.py`), Ghidra decompiles in `analysis/mapping-cfbr-recruiting/` (local only, not for the public repo), and the DB query strings. Names are ours, not EA symbols. Confidence: confirmed (a string literal the function itself emits, or a decompile that shows the logic), likely (query/table evidence plus call-graph position), guess (role inferred only).
Machine-readable names: `analysis/symbols/cfbr_symbols.csv` (system = recruiting).

## 1. Weekly pipeline (confirmed order)

`recruiting_week_advance` 0x4c7bc4 (confirmed; the strings `Updating Recruit Information`, `Progressing Recruits`, `Signing Commits` are all emitted here). Call order read from the decompile:

1. 0x4af390 (board/week setup, arg = week byte at RecruitMan+0x10) , 0x498078 `recruitman_pos_info` (string `RECRUITMAN POS INFO`), 0x4c7b30
2. if the "user pass" flag is set: 0x4c742c `evaluate_visits`, 0x4b304c, 0x4b2a98 (`ptip_rebuild`: `use DYND insert into PTIP set TGID,RPIT,PTCH`)
3. 0x4aed48, 0x4ac2f4, 0x4abd30 (`recruitingboard_remove_candidate_type`), 0x4c3e38 `fill_recruiting_boards`, 0x4ac874
4. 0x4bfa70, 0x4bf92c, 0x4bee10 (skipped in weeks 3 to 6), 0x4bddbc (only in weeks 3 to 6), 0x4bab40
5. string `Progressing Recruits` then 0x4ba384 `recruit_progress_recruits`
6. string `Signing Commits` then 0x4b9ffc, 0x4b8f40, and `evaluate_recruiting_classes` 0x4b6d2c (from week 3 on)
7. week byte at RecruitMan+0x10 is incremented; at week 1 `recruitman_commit_weak_players` 0x4b920c / `recruitman_week5_surplus` 0x4b9918 run first.

Other phase functions (all confirmed by their own progress string):

| Addr | Name | String |
|---|---|---|
| 0x500e58 | recruit_class_generate_driver | `Generating Prospects` (0x178cbe8); callers 0x50112 4, 0x5056c c |
| 0x500c7c | scout_prospects_phase | `Scouting Prospects` |
| 0x500800 | rank_prospects_assign_stars | `Ranking Prospects` |
| 0x4fe648 | evaluate_prospects | `Evaluating Prospects` |
| 0x5025d0 | enroll_recruits | `Enrolling Recruits` (moves signed recruits into PLAY via 0x4f63f0/0x501bb8) |
| 0x4c3e38 | fill_recruiting_boards | `Filling Recruiting Boards - %d%` |
| 0x4af4e8 | schedule_visits | `Scheduling Visits` |
| 0x4c742c | evaluate_visits | `Evaluating Visits` |
| 0x4b6d2c | evaluate_recruiting_classes | `Evaluating Recruiting Classes` (writes RCTC, see 3) |
| 0x538be8 | visit_score_breakdown | `Base Visit Score`, `Complimentary Visits (%d)`, `Competitive Visits (%d)`, `Game Goals Met`, `Total Points from Visit` |
| 0x44bf58 | franstage_type_names (likely) | `FRANSTAGE_TYPE_PRESEASCREATEPROSPECT`, `..PRESEASRECRUITING`, `..OFFSEASRECRUITING` (franchise stage types) |

## 2. Recruit generation (names, position, size, ratings, appearance)

- `recruit_class_generate_driver` 0x500e58 (confirmed): runs `scout_prospects_phase` 0x500c7c, then `rank_prospects_assign_stars` 0x500800, then 0x500348 and `evaluate_prospects` 0x4fe648, then 0x498078. It also runs two DB statements on tags PINT and PINP at entry (purpose not decoded) and finishes with an `update TPCR set SARP` query.
- `scout_prospects_phase` 0x500c7c (confirmed): `0x500b68` returns how many prospects already exist; it loops `prospect_generate_one` 0x494da8 until the count reaches `RecruitMan+0xc` (the class size field), then calls 0x495a00.
- `prospect_generate_one` 0x494da8 (likely, decompile): one prospect per call. Evidence in the decompile:
  - RNG: virtual call at `*(DAT_01d02ee0+0x10)(obj, n)` returns an integer in 0..n-1. Name pools are indexed by that RNG against table sizes held in halfwords at `0x01cfe0e8` (first-name count), `0x01cfe0ea` (last-name count) and `0x01cfe0ee` (a third pool; a per-slot counter at `piVar7[4]` walks it sequentially and wraps to 0). These are the only name-pool sizes found; the pools are filled elsewhere.
  - Height: clamped to 0x41..0x54 (65 to 84 inches) after a random step of 0..3 up or down; weight clamped to 0xa0..0x19f (160 to 415 lb) after a random +/- 0..6 percent adjustment.
  - Ratings: a loop over attribute slots 0x48..0x73 applies a per-position noise `rand(0, p[6]+p[7]) - p[7]` percent, with floor 0x28 (40) and cap 99; slots 0x5c to 0x73 are allowed to fall to 0. The per-position record pointer `*(this+0x11*8)` has bytes +6/+7 (noise range), +8/+9 (percent chances), and a halfword +4 (the position id), so the position table drives both the rating spread and a "position change" roll (two rolls of rand(100) against bytes +8 and +9).
  - After the roll it calls `0x4943ac` to write the row.
- `prospect_insert_RCPT_row` 0x4943ac (likely): the DB insert. Its query (0x17731bc) lists 127 tags, decoded (reversed) from the ELF: PRSI PPOE PTEN POVR PFNA PLNA PPOS PWGT PHGT PHAN PHLM PFMK PVIS PEYE PBRE PNEK PMPC PFLK PBAK PLHW PLTW PTAL PTAR PREL PLEL PRHA PLHA PRWR PLWR PLSL PLSR PJER PLBB PRBB PLFB PRFB PLCB PRCB PRSH PLSO PLSH PLTH PRTH PLKN PRKN PLKL PLKR PSPL PSPR PUND PGHE BSCT BSCA BSGT BSGA BSBT BSBA BSTT BSTA BSST BSSA BSFT BSFA BSAT BSAA BSWT BSWA BSPT BSPA PTYP PPOE PSTR PAGI PSPD PACC PAWR PCTH PCAR PTHP PTHA PKPR PKAC PBTK PTAK PPBK PRBK PINJ PSTA PJMP PKRT PTRK PESV PBCV PSAR PSMV PJMV PIBL PRBS PBFW PPBS PPBF PPMV PFMV PBSH PPRS PPRC PMCV PZCV PRNS SPCT TRAF PRTR PHIT PYRS RELS RATH PDIS RPGP PYEA STAT RPAC RCCB PSTG PRAS RIWH RICR. Table: **RCPT** (prospects). Meanings (tags are the same as in PLAY where known):

| Tag(s) | Meaning | Confidence |
|---|---|---|
| PRSI | prospect id (key for RCPT, RCPR, RECB, RECV) | likely (used as the join key everywhere) |
| PFNA, PLNA | first, last name | likely (also in the bulk update query 0x16ffc5c next to STAT) |
| PPOS | position | likely (same tag as PLAY.PPOS) |
| PHGT, PWGT | height, weight | likely; the generator's clamps above match inches and pounds |
| POVR | overall rating | likely |
| PSTR PAGI PSPD PACC PAWR PCTH PCAR PTHP PTHA PKPR PKAC PBTK PTAK PPBK PRBK PINJ PJMP PKRT PTRK ... | rating attributes (strength, agility, speed, acceleration, awareness, catching, carrying, throw power, throw accuracy, kick power, kick accuracy, break tackle, tackle, pass block, run block, injury, jumping, kick return, trucking) | guess (tag letters only; same family as PLAY) |
| PHAN PHLM PFMK PVIS PEYE PBRE PNEK PMPC PFLK PBAK ... PLSL PLSR ... | appearance/equipment slots (handedness or hand gear, helmet, facemask, visor, eyeblack, breathing/neck gear, etc.) | guess |
| PGHE | generic head id, the field that selects the head model and therefore skin tone | guess (UI strings `Skin Tone Name` 0x16fc264 and `Hometown Name` 0x16fc384 exist, but no field is tied to them yet) |
| BSCT/BSCA ... BSPT/BSPA | per-skill "best/second" pairs (looks like scouting-skill masks; `PROSPECT_SKILL_MASK_HIGH/LOW` strings exist) | guess |
| STAT, RCHD | recruit status / commit state; 0x495a00 updates them with `update RCPT set STAT, RCHD where PRSI` | likely |
| PSTG, PRAS | prospect stage; "ratings adjusted/ stars" is NOT confirmed. PSTG is updated by 0x4b8ad4, 0x4be0a0, 0x500xxx; `PROSPECT_STAGE`/`PROSPECT_ADVSTAGE` strings exist | likely (PSTG), guess (PRAS) |
| RPGP | recruit position group | likely (`RECRUIT_POSGROUP` string; the query `select RCPT.RPGP, RCCB, RCOV` at 0x17945bc) |
| RCCB, RCOV | caliber (`RECRUIT_CALIBER` string) and overall | likely |
| RCRK, RCPR | recruit rank / rank-by-position; written by 0x4fe648 | likely |
| PYEA | years of eligibility / class year | guess |
| RIWH, RICR, RELS, RATH, PDIS, TRAF, SPCT, PRTR, PHIT, PYRS, PRNS ... | not interpreted | unknown |

  **Hometown and state: not found.** No RCPT tag was confidently tied to hometown/state. Candidates are RELS/RATH/PDIS/PRTR/RIWH; the UI strings `Committed from this State`, `RecruitsFrom`, `numRecruitsFromState`, `Pipeline States` prove the data exists. Next step: decompile the UI table reader for `RecruitProspectsTableData` (0x172fb28 STOCK) and the Hometown Name binding.
- `recruit_class_source_players_build_RCTN` 0x4934c8 (likely): shows the progress text `Training Players` (STOCK 0x1772e40). It runs `insert into RCTN select * from PLAY where PTYP != ...` (query 0x1772e58) then walks the result: for each row it divides the player id by 70 (0xd41d41d5 magic, i.e. `PGID / 70 = TGID`, matching the `TGID*70` rule in section 1.3 of MODDING_REFERENCE) and does per-team work. Interpretation is a guess: an annual "train/progress players" pass for the current rosters, not the class creator.
- Star and rank assignment: `rank_prospects_assign_stars` 0x500800 (confirmed from the decompile). The percentage table at stack init is `{0, 20, 24, 45, 9.75, 1.25}` indexed by star count 1..5. That means about 1.25 percent of the class become 5-star, 9.75 percent 4-star, 45 percent 3-star, 24 percent 2-star, 20 percent 1-star, applied to the ranking order (best first). The per-star cut is `class_size * (pct + (rand_float - 0.5)) * 0.01` (constants 1.25 / 0.5 / 0.01 read from the literal pool at 0x5007d8/dc/e0, where the random float comes from the virtual call at `DAT_01d02ee0+0xc`), and the loop drops a star level each time the count for that level is reached. Writes `RCPT.RCRK` through the query string at 0x178ca88 (`update RCPT set RCRK ...`). **Realistic generation hook:** the 6-entry float table and the min/max clamps in `prospect_generate_one` are the numbers to change for rating, size and star distribution.

## 3. Recruiting tables (decoded query tags)

| Table | Columns seen | Role | Confidence |
|---|---|---|---|
| RCPT | see section 2 | one row per prospect | likely |
| RCPR | PRSI RPGP PT01..PT10 PS01..PS10 PS25 PTCM PNCT NLKD | per-prospect pitch values (PT = team ids? PS = score per top team; strings `PROSPECT_TEAMID1..10`, `PROSPECT_TEAMSCORE1..10/25/50`) | likely |
| RECB | TGID PRSI PROR USEL PPSC PSCP PEPV | a team's recruiting board entries (order PROR, scholarship offered, points spent PSCP/PPSC, evaluated pitch PEPV) | likely |
| RECV | PRSI RCWK TGID NFGZ NFGM OFGP VMVP | visits (week RCWK, goals met flags, visit points VMVP) | likely |
| RCTC | TGID RVRP RC5S RC4S RC3S RC2S RC1S RCTC | team class summary: star counts and rank | likely |
| PTIP | TGID RPIT PTCH | per-team pitch values, 14 per team | confirmed (also section 1.8) |
| RCTN | copy of PLAY rows | player copy used by 0x4934c8 | guess |
| PRSC | PLNU SGNM TGID SOSS STPE | prospect scoring entries per game? | guess |
| INJY / INJR | INJY: TGID PGID INJL INJT INJR SEWN; INJR: PGID | injury rows (see players.md when written); INJL length, INJT type | likely |

## 4. Pitch, interest and commit scoring (partial)

- Pitch names (STOCK strings 0x1735e64..0x1735f4c): PITCH_ACPRESTIGE, CAMPUSLIFE, CONFPRESTIGE, CONTENDER, FACILITIES, PROFACTORY, STABILITY, STADIUM_ATMOSPHERE, TRADITION, TV, PLAYINGSTYLE, PLAYTIME, COACHPRESTIGE (`*_VALUE`). These match the team rating steps: `rating_*` functions (STOCK 0x4b2e7c, 0x4b4dc0, 0x4b1c48, 0x4b1f3c, 0x4fc830, 0x4f85bc) driven by `rating_teams_driver` (STOCK 0x503700, CFBR 0x4b5d30 area, string `Rating Teams - %s`).
- Commit state strings: `COMMIT_SCORE`, `PROSPECT_TEAMSCORE*`, `PROSPECT_NEWCOMMIT`, `PROSPECT_TEAMIDCOMMIT`, `RECRUIT_COMMITTED`, `PROSPECT_LOCK_BROKEN`, `INSTANT_COMMIT_RANKS`. The commit decision is made in the `Signing Commits` step: `0x4b9ffc` and `0x4b8f40` (guess; not yet decompiled). `recruitman_commit_weak_players` 0x4b920c forces commits of weak prospects at week 1.
- Visit score: `visit_score_breakdown` 0x538be8 (confirmed) builds the five UI lines: Base Visit Score (via 0x4ad36c/0x4ad1a0/0x4acc78 sub-scores) minus complimentary (offset +0x84) and competitive (+0xc8) adjustments; total at +0x40. The numbers come from helper calls; formulas are not yet decoded.
- Playing-time pitch: `recruitpref_update_playtime_pitch_values` 0x4b6328 (confirmed string), writes `RECB.PEPV`.

## 5. Open items (next)

1. Decompile 0x4b9ffc / 0x4b8f40 (commit decision), 0x4ba384 (progression of interest per week), 0x4af390.
2. Locate hometown/state and skin-tone fields (RCPT columns RELS/RATH/PDIS/PRTR/RIWH are the candidates; also PGHE).
3. Fill pool addresses for the first-name, last-name and third (hometown/state?) pools around 0x1cfe0e8 in the data segment, and find their loader.
4. Position-distribution table (`*(this+0x11*8)` records of 10 bytes with fields +4 id, +6/+7 noise, +8/+9 percents).

## 6. Name pools, hometown, state (second pass; supersedes the open items in section 5 where noted)

Static work only (no Ghidra run this pass, because the run queue was active: `tools\ps3recomp-lane-e\harness\runqueue\LOCK` held by s84-ow4; earlier decompile jobs this session were about 20 s each and were started before I knew the correct queue path).

Evidence: query strings decoded from the ELF (tags are stored reversed), the table-open function 0x495ff8 and the count loader 0x4942cc (both decompiled earlier).

| Table | Columns seen | Role | Confidence |
|---|---|---|---|
| RCFN | SPFN (first name string), SPSL (slot number, indexed) | first-name pool; count in halfword 0x1cfe0e8 | confirmed (query + count loader) |
| RCLN | PRLN (last name), SPSL | last-name pool; count in 0x1cfe0ea | confirmed |
| RCAT | SPSL (unique index, descending) and more columns | pool walked sequentially with a wrapping per-slot counter (count in 0x1cfe0ee). In `prospect_generate_one` a hit here skips the random rating jitter, so RCAT looks like a table of pre-authored ("created", cf. string `RECRUIT_ISCREATED`) prospects | guess |
| RCST | STAT (state id), STNM (state name), STAB (abbreviation), STAO (order), SGID | states, count in 0x1cfe0ec | confirmed |
| RCHT | RCHD (hometown id), RCHN (hometown name), HMTX, HMTY (map coordinates) | hometowns; queried by RCHD range (`where RCHD >= .. and RCHD <= ..`) so id ranges are probably per state | likely |

Answers to the open questions:
- **Hometown:** `RCPT.RCHD` is the prospect's hometown id (it is set together with STAT by the status update, and RCHT is keyed by RCHD). Likely. The state of a prospect is obtained through RCHT/RCST; the exact link column (a STAT column in RCHT, or RCHD ranges per state) is not decoded because the table data lives in the game's database archive, not the executable.
- **Name-pool loader:** the sizes are not in the data segment; `recruit_name_pool_counts_load` 0x4942cc runs `select count(*)` on RCFN, RCLN, RCAT, RCST and stores them in 0x1cfe0e8/ea/ee/ec. `recruit_tables_open_index` 0x495ff8 opens the five tables. To change names or add hometowns edit those DB tables (rows plus consistent SPSL slots), not code.
- **Skin tone:** still not found. No table or column in the executable names it. Best candidates: RCPT.PGHE (head id) or a column of RCFN/RCLN/RCAT rows that carries appearance along with the name. Next step is to dump the RCFN/RCLN/RCAT table schemas and rows from the DB file (the TDB extraction tool named in MODDING_REFERENCE gap 1).
- **Commit decision:** not done. Needs decompiles of CFBR 0x4b9ffc, 0x4b8f40, 0x4ba384.

## 7. Appearance, hometown and state: decoded from the DB data (third pass, 2026-10-28)

Source: read-only dump of the extracted archive entries `analysis/assets/QKL_BOOT-0826.db` (also FE2IG-4664, same tables), `QKL_MISC-0145.db` (empty RCPT template) and `QKL_BOOT-0355.db` (PLAY/DCHT/COCH template) using `scripts/dump_tables.py` (wraps `inspect_tdb.parse_db`). Dumps are local in `analysis/mapping-tables/*.json`. Field dictionary with confidence: `analysis/symbols/cfbr_data_fields.csv`.

Schemas (row bytes; rows/capacity)
- RCFN (8 B; 8191/8191): SPSL 13b slot, SPFN 80b (10-char) string. RCLN (8 B; 6496/6496): SPSL, PRLN 104b (13-char) string. So first names are at most 10 chars, last names at most 13. Pools are full: adding names needs new table capacity, not just rows.
- RCAT (72 B; 8174/8174): a complete rating row (about 120 PLAY/RCPT-style tags including PGHE, PPOS, PHGT, PWGT, SPSL). No name and no hometown column. It is a pool of pre-authored prospect bodies.
- RCST (36 B; 52/52): STAB (2-char), STNM (20-char), STAT 8b state id 0..51, STAO order, SGID (a team id), STMP, RPCT, SPDN/SPUP/SPLT/SPRT. 52 = 50 states + CN (Canada) + DC.
- RCHT (36 B; 4115/4115): RCHD 14b hometown id, CYID 9b city id, RCHN 30-char name, HMTX/HMTY signed 11b map coords.
- RCPT (108 B bit-packed; template 0/4305): the 127 columns of section 2 with widths. Prospect hometown is `RCHD` (14b) and the name is PFNA 11 chars / PLNA 13 chars.

**Hometown to state (confirmed from data):** `RCHD = state_id * 256 + local_index`, and `state_id = RCST.STAT`. Evidence: the sorted RCHT ids have a gap to the next multiple of 256 after each block (51 gaps, 52 blocks), the first block (ids 0..119) is Alabama towns (Fayette, Theodore, Guntersville, Tuscumbia ...), block 2 (id 512..) holds Tolleson, Avra Valley and Cave Creek (Arizona, STAT 2), El Paso (id 10914 = 42*256+162) is in block 42 = TX, and the top id 13056 = 51*256 falls in block 51 = DC. So the state of a prospect is `RCHD >> 8`; a state holds at most 256 hometowns. `RCST.STMP` is NOT the town count (AL 113 vs 120 ids), and `RCHT.CYID` is a city id, not a state. PLAY also has an RCHD column (3010 distinct values among 8568 template players), so every rostered player has a hometown in the same encoding. Confidence: confirmed (structure and AL/AZ/TX spot checks); the per-state town counts are from the ids.

**Skin tone (answer):** no skin-tone field exists in PLAY, RCPT or RCAT. There is no PSKI/skin column; those strings in the executable are stat tables. Appearance fields are PGHE (generic head, 9b), PUHE (unique head, 10b, always 0 in the roster template), PHCL (hair color 0..4), PEYE (eye black), PHLM (helmet 1..6), PFMK (facemask), PVIS (visor), PBRE/PLSY/PSTY (always 0). The head model carries the skin tone, so **PGHE is the skin tone selector** (likely). Data check on the 8568-player roster template: 217 distinct heads in ranges 1-99, 105-122, 126-157, 159-171, 177-183, 186-188, 191-193, 198-200, 202-214, 219-232, 234-246. Position mix by range shows the head groups are body type times skin tone, not a pure skin scale: heads 1-99 are the broad group containing QB, K, P, OL and every position; 159-171 and 191-214 appear only on skill and secondary positions (WR 24-28 percent, CB 21-27 percent, HB, S) and never on OL, DL, K or P; 176-188 and 219-246 appear on DL, LB, OL and TE and never on K, P, QB or skill-only slots. Treat head ids in the same range as the same skin class, but the exact skin of each range is a guess until a head-id to render check is done (visual check in game or the head asset table, not done). How PGHE is filled for generated recruits is not traced yet (guess: taken from the RCAT row when one is used, otherwise rolled). Name and appearance are chosen independently as far as the data shows, so for consistent name and skin a mod must pick names by the PGHE group of the chosen body, or rewrite PGHE after generation; `prospect_insert_RCPT_row` 0x4943ac is the natural hook (not tested).

## 8. Weekly recruiting step order and commit decision (static call order only; NOT decompiled)

Not decompiled this pass: the run queue LOCK was held continuously (s84-ob5, then s84-ow5, with s84-ob6 and s84-ow6 pending) from 23:23 to at least 23:38, so no Ghidra job was started. What the existing decompile `analysis/mapping-cfbr-recruiting/recruit_week_adv.c` (function 0x4c7bc4, "weekly recruiting advance", callers 0x4cfff4, 0x1fc60c, 0x50133c) and `commit_recv.c` (0x4d6504, season start) already show, in call order:
1. status text `Updating Recruit Information`: 0x4af390(RecruitMan, week, 0) (evaluate visits / recompute pitch scores; also called from eval_visits.c and sched_visits.c with args 0xff,0), then 0x498078, 0x4c7b30, and a block of board maintenance (0x4aed48, 0x4ac2f4, 0x4abd30, 0x4c3e38, 0x4ac874, 0x4bfa70, 0x4bf92c, 0x4bee10 outside weeks 3 to 6, 0x4bddbc inside weeks 3 to 6, 0x4bab40).
2. status text `Progressing Recruits`: 0x4ba384(RecruitMan, week, advanceFlag, 0) (confirmed by string; called with advanceFlag=1 from the season-start function 0x4d6504). Per-week interest/score progression.
3. status text `Signing Commits`: 0x4b9ffc(RecruitMan) then 0x4b8f40(RecruitMan). These two are the commit decision (the earlier guess stands: 0x4b9ffc decides commits, 0x4b8f40 finalises or writes them), still unread.
4. If a week advance was requested: text `Advancing to week %d`; at week 1 it runs 0x4b9918 and, if that returns 0, `recruitman_commit_weak_players` 0x4b920c, then 0x4b8f40 again; then RecruitMan+0x10 (week byte) is incremented, 0x4b6d2c/0x4b75dc run for weeks under 3, 0x4b7384 and 0x4ac5c0 at week 2, else 0x4b0c14(RecruitMan, week, 0x96).
Next step when the queue is idle: `scripts/run_cfbr_ghidra_decomp.ps1 -OutDir analysis/mapping-cfbr-recruiting -Spec "commit_a:4b9ffc,commit_b:4b8f40,prog:4ba384,eval:4af390"` (BelowNormal, one JVM, about 20 s).

## 9. How generated recruits get their body and head (static read of 0x494da8, `scout_494da8.c`)
- Names: two pool indices are `(random(count) + offset) mod count` for the first-name pool (count halfword 0x1cfe0e8) and the last-name pool (0x1cfe0ea), then `0x494884(...)` copies the strings (buffers of 0xc and 0xe bytes, matching the 11-char PFNA and 13-char PLNA).
- Body: the RCAT pool is walked with a wrapping counter at `piVar7[4]` (count 0x1cfe0ee; first call picks a random start). `0x494954(slot, buf)` loads that RCAT row into a 0x1dc-byte local record that holds every RCPT-style attribute, including PGHE. No code in 0x494da8 touches the head: height (65-84 in), weight (160-415 lb) and the 0x48..0x73 rating slots are jittered only when `0x494954` returns 0, otherwise the row is used as authored.
- The record then goes to `0x4943ac` (insert), which subtracts 0xa0 from weight (in_r7[9]) before the insert. This confirms PWGT raw = lb - 160.
- Conclusion (likely): PGHE for a generated recruit is the PGHE of the RCAT row picked, independent of the name. Consistent name and skin therefore needs either a name choice keyed on the RCAT row's PGHE group, or editing the RCAT rows' PGHE in the archive (data only, no code change; RCAT has 8174 rows with PGHE values in 1..246). Next check: `0x494954`, `0x491560` in batch 1.

## 10. Static read of the commit helpers already decompiled (2026-10-29, 0x4b920c and 0x4b9918; no new Ghidra run)
Confidence: likely (pseudo-C is noisy; constants are exact).
- `recruitman_commit_weak_players` 0x4b920c (alloc tag `RecruitManCommitWeakPlayers`): loops over all teams starting at a random rotation offset (RNG vtable at 0x1d02ee0, slot +0x10), skipping team id 0x3ff. For each team it reads open scholarship count (0x4b7ebc) minus already-used count; acts only when the shortfall is under 0x14 (20). It builds a candidate list of that team's recruits (6-byte records: prospect id, interest rank, pitch/position slot), then fills open slots in up to 6 passes by rank (pass k takes entries whose rank == k), each pass decrementing per-position quota (array of 0x11 position counters, 0x12 = any position), calling vtable +0x1c on RecruitMan (the commit call) per pick. So week 1 force-commits the best-ranked weak (unwanted-by-others) prospects to teams that still have space.
- `recruitman_week5_surplus` 0x4b9918 (tag `RecruitManWeek5Surplus`): runs for each prospect with interest rows; base commit chance is 0x5a (90) percent when the prospect's top-listed rank slot is 4 or 5, else 0x50 (80); reduced by 0x32 (50) when the team's remaining need is under 5. Rolls d100 against that chance, then commits through the same vtable +0x1c call. It also contains a "signing day steal" swap: with a probability scaled by a double constant (DAT_00186780) times a computed team-score ratio (0x4b97c0), the top two candidates swap and a `CreateSigningDayStealEvent` object (vtable 0x18ac3f8, 16 bytes: type 8, prospect id, team id) is created for the news.
- `visit_score_breakdown` 0x538be8 only formats; its lines are Base Visit Score, Complimentary Visits, Competitive Visits, Game Goals Met, Total Points from Visit (struct stride 0x44, 5 lines).
- Still open: 0x4b9ffc, 0x4b8f40 (the main commit/finalise), 0x4ba384; batch 1 queued.

## 11. Batch 1 decompile results (2026-10-30; analysed from `analysis/mapping-cfbr-batch1/`, local only)
Method: the 17 decompiles plus the embedded EA-SQL strings read from the CFBR ELF (tags are stored byte reversed; a constant such as 0x504d5453 is the tag `STMP` reversed). The decompiler hides several stack arguments, so SQL strings are the reliable evidence and constants/control flow come second. Confidence labels as before.

### 11.1 Weekly step helpers
- **0x4af390 `recruitman_build_eval_indexes`** (confirmed): not a scoring function. It wraps hook callbacks (`DAT_01c85990` before, `DAT_01c85994` after) around `create index` statements: RCPT by PRSI, RCPR by PRSI, RECB by (TGID, PRSI), RECV by (PRSI, TGID), and when week != 0xff a partial RECV index `where RCWK = week`. It stores its third argument at RecruitMan+0xca10. It is called many times (eval_visits, sched_visits, the weekly advance) as a query-speed prelude.
- **0x4ba384 `recruit_progress_recruits`** (confirmed shape; the formula is elsewhere): sets RecruitMan+0x10f2 = flag and +0x10f0 = week, zeroes the 0x5e8-byte block at +0xb08 (126 team slots x 12 bytes), runs 0x4ba2a8 (fills that block) when neither flag is set, then walks the whole RCPR table (`PTCM` key) calling the per-row callback at **0x50dad4** (opd 0x1bee0e0). The per-prospect interest update therefore lives in 0x50dad4 (queued for the next batch).
- **0x4b9ffc `recruitman_sign_stage5_leaders`** (likely): `declare cursor select PRSI from RCPT where PSTG = 5 and PRAS = 1`; for each row it reads the top pitch team (`select PT01 from RCPR where PRSI = ?`) and, if the manager vtable +8 check passes for it, calls vtable +0x1c (the commit call that 0x4b9918 also uses). After the loop one statement demotes the still uncommitted rows: `update RCPT set PSTG = 2, PRAS = 2 where PSTG = 5 and PRAS = 1 and RCCM = 0`, and RecruitMan[0x2aa] is copied to [0x2ab]. So PSTG/PRAS are prospect stage / state fields (5/1 = awaiting decision) and RCCM is the committed flag. The vtable +8 predicate is not visible (the decompile shows placeholders 0x3ff/0xffff for the locals).
- **0x4b8f40 `recruitman_check_team_class_full`** (likely): loops team slots 0..0x7d (126). Team id comes from the 12-byte-stride list at `DAT_01c8691c` (count `DAT_01c86922`; 0x3ff past the end). If `0x4abc70(rm, team)` is non-zero it calls `0x4b8ad4(rm, slot)` (board refresh), always calls `0x4ab278(RECB handle, team)`, then compares the team's signed count (byte at RecruitMan + slot*0x178 + 0x10fd) with its open scholarship capacity `0x4b7ebc`; when count >= capacity and the one-shot flag at +0x10ff is 0 it calls `0x4b7c10(obj, team)` (class-full notification, guess) and sets the flag. The `< 0x7e` bound is a hard-coded 126, relevant to any team-count expansion.
- **0x4b9918 `recruitman_week5_surplus`** (extends section 10, likely): the loop is driven by `select PRSI, RCCB from RCPT where RCCB >= ? and RCCM = 0 order by RCCB desc`, so **RCCB is the commit score of the prospect** and the best uncommitted prospects resolve first. Per prospect it reads PT01..PT10 and RPGP (position group) from RCPR, counts a team's signed prospects (`select count(*) from RCPR where PTCM = team`), derives open need = capacity (0x4b7ebc) - count, and rolls d100 against chance C for each candidate team in PT01..PT10 order: C = 0x5a (90) if the prospect's rank slot value is 4 or 5, else 0x50 (80), minus 0x32 (50) when the team's open need is below 5. A roll only counts if need != 0 and the position quota allows it (RPGP == 0x12 means any position, else `0x4b904c` > 0). Coach gate: `select CFSC, CFUC from COCH where TGID = ?`; when CFSC is set and CFUC is not, a PINT lookup (`select PRSO from PINT where TGID = ? and PRSI = ?`) with PRSO 2 or 3 marks the prospect as already pledged to that program. The signing day steal (swap of the two top teams with a probability from `DAT_00186780` times the team-score ratio `0x4b97c0`, then `CreateSigningDayStealEvent`) is as in section 10.

### 11.2 Visit helpers (lists, not the formulas)
- **0x4ad36c `visit_prospects_for_team_week`** (confirmed): `select RECV.PRSI from RECV join RCPT where RECV.TGID = ? and RECV.RCWK = ? order by RCPT.RCRK asc`; fills an id array with up to N prospects of that team's visits in a week, best recruit rank first, and returns the count.
- **0x4acc78 / 0x4ad1a0** (guess): list builders over a prospect id array. For a reference prospect they walk the other ids, derive a group value for each (`0x4ac9b4` maps a prospect to an index, then the manager vtable +0x14 maps that to a group; `0x4aca74` is a validity test that must be 0 for the reference), skip ids whose group is already represented in the output vector, and append the id when a gate passes (0x4acc78: `0x4acb3c <= 0x4acb8c`; 0x4ad1a0: `0x4ace80 != 0`). They produce same-group candidate lists that feed the Complimentary / Competitive visit lines. The five visit-score numbers (Base, complimentary, competitive, game goals, total) are formatted by the 0x538xxx UI builder from RECV columns (NFGZ NFGM OFGP VMVP) and these lists; no arithmetic for the "Base Visit Score" is in these three helpers. Open: 0x4ac9b4, 0x4aca74, 0x4acb3c, 0x4acb8c, 0x4ace80 (batch 2).

### 11.3 Commit-related fields tied to code
RCPT.PSTG, PRAS, RCCM (committed flag), RCCB (commit score), RCRK (rank); RCPR.PT01..PT10 (ranked team list), PTCM (committed team), RPGP (position group); **RCST.STMP is the hometown-state weight used by 0x495a00** (not RPCT; see recruit-generation.md section 1).

### 11.4 Name and RCAT loaders (feed the recruit-realism hooks)
- **0x494884 `recruit_name_strings_load`** (confirmed): `use db select SPFN from RCFN where SPSL = idx` and `select PRLN from RCLN where SPSL = idx` into 10- and 13-char zeroed buffers, then copied to the caller buffers (sizes 0xc and 0xe). Callers: 0x495024 (generator) and 0x497230.
- **0x494954 `recruit_rcat_row_load`** (confirmed): one statement selecting 111 RCAT columns `where SPSL = slot` straight into the record at +0x20, +0x24, ... (4 bytes each, column order = the query text: PPOS, PWGT, PHGT, PHAN, PHLM, PFMK, PVIS, PEYE, ... PGHE (column 44, +0xd0), the BSxx body-shape pairs, PTYP (+0x11c), PPOE (+0x120), PSTR, PAGI, ... PDIS). On success it adds 0xa0 to the weight word: RCAT stores weight minus 160. Returns the query status (0 = found).

### 11.5 `prospect_rating_shaper` 0x491560 (likely)
Called five times from inside 0x494da8 (0x4955d0, 0x4955f0, 0x495614, 0x49570c, 0x495744). Signature: (rating array pointer, u16 seed, u8 posGroup, u8 archetype, u8 tier). For each of the 46 rating indices 1..0x2e whose slot-map byte (`0x1c8772c`, 0xff = skip) is valid it computes
`new = clamp(old * c2 + (D[archetype*49 + posGroup*147 + i] / c21) * ( lerp(rand, c10, c11) * c0 + seed * c3 + interp(tier; c26..c23 breakpoints) * c12 * c1 ), lo, hi)`
(the index arithmetic follows the decompile: stride 0x93 for the third argument, 0x31 for the fourth). D is the byte table at `0x1cfd6f0` filled by 0x492cd8 from a gamedata record (17 x 3 x 49 bytes), the c* values are float/short fields of a gamedata config record (`DAT_00491530/38`), the random float comes from the RNG vtable +0xc (`DAT_01d02ee0`), and lo/hi are literal-pool floats. It rewrites the rating slots in place, so it is the position/archetype rating adder of the generator, not a position roll. Other jitter in 0x494da8 itself: height clamped 65..84 with a +-(0..2) nudge (the 3-way roll), weight scaled by +-(0..5) percent and clamped 160..415, and per-slot noise using bytes +6/+7 of the config record when the RCAT row did not load.
