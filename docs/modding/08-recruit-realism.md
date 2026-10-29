# Recruit generation realism: design, sources, hook plan

Status: design plus generated data (2026-10-29). No game files, saves or archives were modified. Personal-use modding of a game the user owns. Everything below is statistical modelling of public aggregate data; it makes no claim about any individual. Confidence labels: confirmed / likely / guess / estimate.

Generated files: `analysis/realism/` (scripts) and `analysis/realism/out/` (data). Re-run with `python -I analysis/realism/generate_realism.py` (deterministic, seed 20261029).

## 1. What the generator reads (static analysis, CFBR addresses)

| Item | Finding | Confidence |
|---|---|---|
| Name pools | `prospect_generate_one` 0x494da8 draws a first-name index and a last-name index uniformly with the game RNG (`*(DAT_01d02ee0+0x10)(obj,n)`, n = RCFN/RCLN row count from halfwords 0x1cfe0e8 / 0x1cfe0ea). Pools are tables RCFN (8191 rows, 10-char names) and RCLN (6496 rows, 13-char names) and are weighted by repetition (stock: "Chris" 150 times, "Williams" 147 times). | confirmed (decompile plus decoded tables) |
| Body and head | RCAT slot (counter `piVar7[4]`, random start, wraps at the RCAT count 8174) is loaded by 0x494954 into the 0x1dc-byte local record. PGHE comes from that RCAT row only; position PPOS too. Name and head are chosen independently. | confirmed |
| Hometown | NOT in the generator. After generation `rcpt_hometown_assign` 0x495a00 builds a state lottery from `RCST.RPCT` (7-bit weight per state, 52 entries) and writes `STAT` and `RCHD = state*256 + (prospect_id + rand) mod townCount`. This is a data table, so state realism needs no code. | likely (decompile of 0x495a00 read this session; the weight column is RCST.RPCT, the only per-state count field) |
| Stars | 0x500800, percent table {20, 24, 45, 9.75, 1.25} (1 to 5 star). Unchanged by this plan. | confirmed |

Stock pool content (decoded this session with `analysis/realism/tdb_strings.py`): 769 distinct first names (Chris, Mike, Matt, John, Brandon, Ryan, Jason ... a 2000s mix) and 1118 distinct last names (Williams, Smith, Johnson, Brown, Jones, Davis ...). String table format (type 13): extra data after the rows holds a Huffman tree (BFS pairs, `idx==0` leaf) then per row one length byte plus byte-aligned Huffman bits; the row stores a 32-bit offset. `huffman_tool.py` re-serialises the stock trees byte-identically (round-trip verified) and can build new optimal trees.

Stock state weights (RCST.RPCT, sum 626): TX 15.3 percent, CA 11.2, FL 8.8, OH 6.2, GA 5.1, LA 4.5, AL 3.5, MI 3.5 ... SC only 1.4 and VA 1.9 (low), CA high.

## 2. Appearance model (position to head to skin tone)

### 2.1 Head id classes
PGHE is the head model id (1..246 in use). There is no skin column; skin follows the head. Calibration used (a) the community real-2026 CFBR roster (8694 players, real names, heads chosen by roster authors) and (b) well-known players as anchors (white QBs 11, 15, 24, 25, 39, 78; Black players 170, 171, 182, 191, 209, 228; Pacific Islander linemen/DB 115, 116; mixed-heritage WR/RB 134). Name-based estimates (Census surnames x Tzioumis first names) show heads 1..99 are about 90 percent white-associated and about 4 percent Black-associated, heads from 105 up are mixed or darker. Four classes (a tone ordering inferred from anchors, **guess** for the exact rendered shade; a render check is listed in section 7):

| Class | Head ids | Reading |
|---|---|---|
| T1 | 1 to 99 | light |
| T2 | 105 to 122 | light-medium / tan (Pacific Islander, Latino, mixed anchors) |
| T3 | 123 to 158 | medium-brown / mixed |
| T4 | 159 to 246 | dark (several body-type sub-ranges: 159-171, 176-188, 191-214, 219-246) |

### 2.2 Probability of head class by position group (used directly)
Derived from the roster (add-half smoothing), file `out/head_model.json` (also lists the empirical PGHE distribution inside every position and class cell, with a class-wide fallback for cells under 8 players).

| Position | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| QB | 68.3 | 4.6 | 8.4 | 18.7 |
| RB (HB, FB) | 10.0 | 5.3 | 12.8 | 72.0 |
| WR | 13.5 | 6.4 | 16.9 | 63.2 |
| TE | 66.1 | 6.3 | 6.9 | 20.7 |
| OL | 54.1 | 7.1 | 8.7 | 30.2 |
| DL | 15.4 | 9.0 | 12.0 | 63.6 |
| LB | 26.7 | 6.5 | 11.9 | 54.9 |
| CB | 1.0 | 5.5 | 15.6 | 78.0 |
| S | 9.9 | 7.4 | 15.3 | 67.5 |
| K, P | 96.5 | 0.9 | 2.4 | 0.2 |

Weighted by the game's own RCAT position mix the class mix is T1 29.1, T2 6.5, T3 11.9, T4 52.4 percent. Cross-checks from public sources: NCAA reported Black athletes at 45.8 percent of Division I football in 2009-10 and the share has stayed in the high 40s; the well-documented position pattern (low at QB, K/P and TE, middle at OL, highest at CB, S, RB and WR) matches the table. T3+T4 exceeds the Black share because T3/T4 also carry Pacific Islander, mixed-heritage and darker-skinned Latino players. Position-level race tables by season are not freely downloadable in machine form (NCAA's dashboard is interactive, TIDES reports are PDF), so the roster is the primary empirical source; the NCAA aggregate is the sanity check.

### 2.3 Data-only application
`out/rcat_pghe_plan.csv` gives, for each of the 8174 RCAT rows (row, SPSL, PPOS), a new PGHE drawn from the model (before and after class mix: T1 37.4 to 29.2, T4 46.7 to 52.2). Only PGHE changes; ratings and bodies stay. Because the generator walks RCAT sequentially from a random start, the class mix of a generated class equals the pool mix. Position mix of RCAT (QB 5.9, RB 9.7, WR 12.1, TE 4.5, OL 17.4, DL 15.7, LB 13.8, CB 9.3, S 8.5, K/P 3.3 percent) is close to roster reality (5.1, 7.4, 12.6, 5.7, 17.6, 17.1, 11.9, 8.9, 10.5, 3.1) so positions are left alone.

## 3. Names

### 3.1 Groups and method
Five name groups: WH, BL, HI (Hispanic), PI (Pacific Islander), AS (Asian). For each group the probability of a first name is `SSA popularity (boys, births 2005 to 2008, i.e. the HS classes of 2024 to 2027) x P(group | name) / P(group)`, with P(group | name) from the Tzioumis first-name table (4,250 names; Bayes-smoothed toward the group prior with K = 40; names under 15 observations or absent get small seed-list heuristics, see `curated.py`). Last names: `Census 2010 count x pct<group>` for WH, BL, HI, AS; PI is 50 percent curated Samoan/Tongan/Hawaiian/Fijian surnames and 50 percent general surnames. First names over 10 letters use common short forms (Christopher to Chris etc.). Distributions are flattened (power 0.7) to give a longer tail, then converted to integer slot counts per group (largest remainder, repetition = weight, same convention as the stock tables).

Expected group mix of recruits (positions x head class x name group, see `out/name_group_given_posgroup_class.json`): WH 37.6, BL 45.8, HI 8.0, PI 5.3, AS 3.3 percent. Name group given head class (before the position adjustment on PI; PI multipliers OL 2.5, DL 2.0, LB 1.5, TE 1.2, RB 1.0, WR/S 0.6, QB 0.4, CB 0.3, K/P 0.2):

| Class | WH | BL | HI | PI | AS |
|---|---|---|---|---|---|
| T1 | 86.5 | 1.0 | 7.0 | 1.0 | 4.5 |
| T2 | 36 | 6 | 28 | 18 | 12 |
| T3 | 30 | 38 | 14 | 12 | 6 |
| T4 | 13 | 78 | 5 | 3 | 1 |

These conditional shares are **estimates** (author judgement fitted so the national group mix is about WH 38 / BL 46 / HI 8 / PI 5 / AS 3, near NCAA Division I football aggregates of roughly 38 to 40 white, mid-40s to 50 Black, 5 to 8 Hispanic, 2 to 3 Pacific Islander, about 1 to 3 Asian, with two-or-more-race players split across groups). Tune them in `generate_realism.py` (`BASE`, `PI_MULT`).

### 3.2 Output pools
`out/first_names_pool.tsv` (8191 slots, 1176 distinct) and `out/last_names_pool.tsv` (6496 slots, 4037 distinct), columns slot, name, group. Stock: 769 and 1118 distinct. Groups occupy contiguous slices whose lengths equal the group's expected share, so the pool is correct on its own (Tier 1, data only) and the slices also let a cave pick a slice (Tier 2). `out/name_slices.json` lists start, length, distinct count and the top names per slice.

Limits respected: 8191 and 6496 rows (13-bit SPSL; no new rows), first names at most 10 chars (max used 10), last names at most 13 (max used 13), letters only. Stock RCLN tree lacks capital X, so a rebuilt tree is needed for names such as Xiong/Xavier-style surnames (not used for first names: stock RCFN tree has all letters).

Encoded size (`out/size_budget.json`, `check_budget.py`): RCFN strings 36,425 bytes stock, 39,998 with the stock tree (+8.6 percent), 39,549 with a rebuilt tree; RCLN 33,029 stock, 33,449 rebuilt (+1.3 percent). RCFN therefore grows about 3.1 KB, so the implementer must be able to enlarge the table's extra-data area (or cap first names at 9 chars, which removes about 1 KB; drop the rarest PI/AS tail names for the rest).

## 4. Hometown (states)
`out/rcst_rpct_proposed.csv`: new `RCST.RPCT` per state (7 bits, max 127, total 800 so TX = 114). Targets are shares of national FBS signees: TX 14.2, FL 10.7, GA 9.4 are measured (class of 2025: 2,747 FBS signees; TX 391, FL 294, GA 257; Texas Football / Dave Campbell's, Aug 2025). All other states are **estimates** of recent 247/On3-style state totals (plus or minus 25 percent), renormalised to the remaining 65.7 percent; per-capita leaders reported for 2025 are AL, LA, FL, GA, MS, HI, DC, TX, OK, OH (FootballScoop, Mar 2025). Largest changes versus stock: CA 11.2 to 5.7 percent, OH 6.2 to 3.5, MI 3.5 to 2.1, IL 2.9 to 1.9, GA 5.1 to 9.4, FL 8.8 to 10.7, SC 1.4 to 2.6, VA 1.9 to 2.8, NC 2.6 to 3.0, NV 0.3 to 1.1, MA 0.2 to 0.9, DC 0.2 to 0.45, CN (Canada) 0.8 to 0.3. The CA reduction matters because California produces many recruits but a smaller share of FBS signees than its population; verify against On3 data if available (open question 3).
Town within the state stays uniform over the state's RCHT towns (no data for town weights).

## 5. Implementation plan (for the implementation agent)

Tier 1, data only (no code, no addresses): 
1. RCFN and RCLN: rewrite the string rows from the two pool files in slot order (SPSL = slot for RCFN; RCLN SPSL is a permutation, map slot to SPSL one to one), re-encode with a rebuilt Huffman tree (`huffman_tool.build_tree`, `serialize`) or the stock tree where the charset allows, and fix the offsets; table header counts unchanged (8191 and 6496).
2. RCAT: set PGHE per `rcat_pghe_plan.csv` (key on SPSL).
3. RCST: set RPCT from the csv.
Archive entry: `QKL_BOOT-0826.db` (also FE2IG-4664, identical tables; check which archives the game loads RCFN/RCLN/RCAT/RCST from for the CFBR + real2026 stack). Result: realistic marginal distributions of names, heads and states, but name and head stay independent of each other and of the state.

Tier 2, C cave for name to head coupling (the part data cannot express): hook the single call `bl 0x494884` at **0x495024** inside 0x494da8. At that point (static instruction read, **likely**; confirm in the Ghidra output, section 6): r4 holds the final first-name index (r27, already reduced mod RCFN count), r5 the final last-name index (r29, mod RCLN count), r30 holds the RCAT slot passed to the loader 0x494954 at 0x494fdc (the `mr r30,r29` at 0x494fd4 saves it, the call is `addi r4,r1,0x344`), and the record is at sp+0x344. Replace the `bl 0x494884` by `bl cave`; the cave reads a byte `ctx[r30]` from a table of 8174 bytes (posgroup 0..9 times 4 plus tone class 0..3; generated from `rcat_pghe_plan.csv`), draws a name group from `name_group_given_posgroup_class.json` (two calls to the game RNG exactly like the caller: `*(*(DAT_01d02ee0+0x10))(&DAT_01d02ee0, n)`; or reuse r5 scaled), sets r4 = firstStart[g] + rand(firstLen[g]) and r5 = lastStart[g] + rand(lastLen[g]) from `name_slices.json`, then tail-branches `b 0x494884` (LR is preserved by the `bl cave`, so it returns to 0x495028). No stack frame needed except for the RNG calls. Mind the table-load order: slices assume the pool files are used unchanged.

Tier 3, optional hometown coupling: a cave at 0x495a00 that picks the state lottery by name group (for example PI heavy in HI, UT, CA, WA, NV, TX; Black recruits heavier in GA, FL, TX, LA, AL, MS, SC, NC, OH, VA, MD). It needs the prospect's group, which can be recovered from the name slice (look up PFNA in the slice table) or stored by the Tier 2 cave; not designed in detail.

Not touched: star table 0x500800, rating generator, position roll 0x491560, `evaluate_prospects`.

## 6. Ghidra and verification status
A decompile job for 0x494954 (RCAT row loader), 0x494884 (name copy) and 0x491560 was queued with `scripts/wait_idle_decomp.sh` (output `analysis/realism/decomp/`, log `analysis/realism/decomp_wait.log`) but the run queue was busy for the whole session; results, if present, should be read to confirm r27/r29/r30 roles and the `bl` at 0x495024. The static PPC read in this document is from the CFBR ELF words and is consistent with `scout_494da8.c`.

## 7. Open questions
1. Exact rendered skin of each PGHE range (the T1 to T4 order is inferred from anchor players and name statistics). A render check is needed: a roster edit giving test players PGHE 1, 50, 99, 105, 115, 122, 123, 140, 158, 159, 190, 220, 246 and a screenshot of the roster view (use the run-queue protocol).
2. Does the game load RCFN, RCLN, RCAT and RCST from QKL_BOOT-0826 only, and can the extra-data area of RCFN grow 3 KB when the archive is repacked?
3. State shares other than TX, FL, GA are estimates; replace `EST` in the generator when a state-by-state 247/On3 signee count is available.
4. Does RCST.RPCT really feed the lottery in 0x495a00 (the only 7-bit per-state field, matching the stock ordering: TX 96, CA 70, FL 55)? A one-state test (set RPCT of one state to 127, others 1, generate a class, read RCHD) confirms it.
5. Do mixed-heritage and Pacific Islander players deserve a separate head class once the render check is done?
6. PGHE and body type: the plan only moves heads inside the (position group, class) cells that the roster already uses; unexplored head and body combinations are avoided.

## 8. Sources
- US Census Bureau, Frequently Occurring Surnames from the 2010 Census (names.zip, 162,254 surnames with race percentages): https://www.census.gov/topics/population/genealogy/data/2010_surnames.html
- Tzioumis, K. (2018). Demographic aspects of first names. Scientific Data 5:180025; data Harvard Dataverse doi:10.7910/DVN/TYJKEZ (4,250 first names by race and Hispanic origin).
- US Social Security Administration, Popular Baby Names (national, top 1000 per year); used through the mirror https://github.com/hadley/data-baby-names (boys, 2005 to 2008; ssa.gov blocked scripted downloads).
- NCAA, African-Americans gain first majority in Division I football (2009-10: 45.8 percent): https://ncaanewsarchive.s3.amazonaws.com/2010-news-stories/december/african-americans-gain-first-majority-in-division-i-football.html
- Texas Football / Dave Campbell's, Recruiting by the Numbers: State of Texas Reclaims Dominance (class of 2025 FBS signees by state): https://www.davecampbells.com/articles/2025/08/14/recruiting-by-the-numbers-state-of-texas-reclaims-dominance
- FootballScoop, per-capita FBS recruiting rankings and hometown map (Mar 2025): https://www.footballscoop.com/2025/03/05/chart-mapping-every-fbs-players-home-town
- Community CFBR real-2026 roster (head assignments by roster authors), used only as aggregate statistics.
- Our own tables: `docs/mapping/recruiting.md` sections 2, 6, 7, 9; `analysis/symbols/cfbr_data_fields.csv`.

## 9. Files
`analysis/realism/`: `generate_realism.py` (all model code), `curated.py` (hand lists), `roster_heads.py` (roster and name-race calibration), `tdb_strings.py` (RCFN/RCLN decoder), `huffman_tool.py` (tree build/serialise, round-trip verified), `check_budget.py`, `xlsx_min.py`; `out/`: `first_names_pool.tsv`, `last_names_pool.tsv`, `name_slices.json`, `head_model.json`, `name_group_given_posgroup_class.json`, `expected_mix.json`, `rcat_pghe_plan.csv`, `rcst_rpct_proposed.csv`, `size_budget.json`, `head_name_race_estimate.json`, `summary.json`. `src/` holds the downloaded public inputs (Census, Tzioumis, SSA mirror).

Note for the public copy: the local-only files rcat_pghe_plan.csv, rcst_rpct_proposed.csv, size_budget.json and the downloaded src/ inputs are not mirrored (they embed game table values or third-party downloads); re-create them with the generator.
