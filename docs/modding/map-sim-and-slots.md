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
