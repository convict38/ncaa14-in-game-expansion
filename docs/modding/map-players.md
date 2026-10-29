# Players, depth charts, coaches (item 3, data-schema pass 2026-10-28)

Source: read-only dumps of the roster template `analysis/assets/QKL_BOOT-0355.db` (8568 players) with `scripts/dump_tables.py`; schemas and value statistics under `analysis/mapping-tables/` (local). Field dictionary with confidence and source for every column: `analysis/symbols/cfbr_data_fields.csv` (378 rows, 95 with a meaning). Meanings are inferred from tag letters plus per-position attribute means, so ratings are "likely" at best; the structural facts are confirmed.

## PLAY (players): 112 B/row, 133 fields, template 8568/9100
- Keys: PGID 16b (team = PGID // 70), TGID 10b, POID 16b (equal to PGID in all template rows). Template names are `POS #n` placeholders; PJEN is the jersey number (confirmed, matches the placeholder in all 8568 rows).
- PPOS (5b) enum, confirmed by attribute means: 0 QB, 1 HB, 2 FB, 3 WR, 4 TE, 5 LT, 6 LG, 7 C, 8 RG, 9 RT, 10 LE, 11 RE, 12 DT, 13 LOLB, 14 MLB, 15 ROLB, 16 CB, 17 FS, 18 SS, 19 K, 20 P (21 values).
- Size: PHGT 7b is inches (66..81), PWGT 8b is pounds minus 160 (OL mean raw 135 = 295 lb). POVR overall 45..99. PYEA 0..3 class year (guess: FR..SR).
- Ratings (7b, 0..99 scale, floor about 10 to 40): PSPD speed, PACC acceleration, PAGI agility, PSTR strength, PJMP jump, PAWR awareness, PTHP/PTHA throw power/accuracy, PKPR/PKAC kick power/accuracy, PCTH catch, PCAR carry, PBTK break tackle, PTRK trucking, PSMV spin, PJMV juke, PBCV ball-carrier vision, PTAK tackle, PHIT hit power, PMCV/PZCV man/zone coverage, PFMV/PPMV finesse/power move, PBSH block shed, PPBK/PRBK/PIBL pass/run/impact block, PRTR route running, PKRT kick return (likely). Guesses: PSTA stamina, PINJ injury, PSAR stiff arm, PPRC play recognition, PPRS pursuit, RELS release, TRAF catch in traffic, SPCT spectacular catch, the block family PBFW/PPBF/PPBS/PRBS, PESV, PIMP, PYRS, PSTM, PPRI.
- Appearance and gear: PGHE head (see recruiting.md section 7), PUHE (0), PHCL hair color 0..4, PEYE, PHLM helmet 1..6, PFMK facemask 0..46, PVIS visor, left/right accessories PLHA/PRHA, PLEL/PREL, PLWR/PRWR, PLSH/PRSH, PLTH/PRTH, PLKN/PRKN, PLBB/PRBB, PLCB/PRCB, PLFB/PRFB, PLSL/PLSR, PLHW, PLTW, PNEK, PHAN, PJER, PLKL/PLKR (all guess, tag letters only).
- Hometown: PLAY.RCHD = state*256 + index (see recruiting.md section 7). The template has 3010 distinct values.
- Always-zero columns in the template: BSWA, BSAT, BSFT, BSGT, BSWT, PUND, PHPD, PMPC, PBRE, PTAL, PSPL, PLHN, PRHN, PTYP, PTAR, PLCR, PSPR, PLSY, PSTY, sgmp.
- The BSxx pairs (BSAA/BSAT ...) are small (4-5b) per-skill codes also present in RCPT; best guess is a skill/development trait mask (see strings `PROSPECT_SKILL_MASK_*`).

## DCHT (depth chart): 8 B/row, 4 fields, template 8568/11464
PGID 16b, TGID 10b, PPOS 5b, ddep 6b. PPOS 0..20 uses the PLAY enum; 21 and 22 appear about 2.4 times per team (likely KR, PR), 23 and 24 once per team (guess: kickoff and long-snap/holder type specials). `ddep` is the depth slot (0 starter up to 5). A team with 69 players has 88 chart rows in FBS (see MODDING_REFERENCE 1.3).

## COCH (coaches): 128 B/row, 108 fields, template 403/409
Keys: CCID 16b coach id (unique, 0..709), TGID 10b. Names: CFNM and CLNM 16-char strings (confirmed); CLNA placeholder label. CAGE 26..70, CRAT overall 10..99 (guess), CDID role slot 0..5 (guess: 0 most common, head coach), CPID 0..134 (portrait/personality guess). The rating groups are suffixed letter families (CDTA/COTA/CDTR/COTR/CDTS/COTS/CDTT, CCWI/CCWS/CCLO ...) and are not decoded. The field letters `A/R/S/T/L/W/Y/M/I/C/N` look like a column-family suffix (as in Madden's coach table) but no meaning is confirmed.

## Status
Done: schemas, widths, enum, value ranges, CSV dictionary. Not done: function-level read/write maps for these tables (which functions touch PPOS, PYEA, progression), the exact meaning of the guesses above (needs either a Ghidra pass on the roster UI strings or an in-game check against an edited value), the rating-to-overall formula per position.
