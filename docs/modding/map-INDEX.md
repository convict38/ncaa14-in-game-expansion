# Mapping index

| System | File | Status | Names (CFBR csv) | Notes |
|---|---|---|---|---|
| CFBR address map / symbols | cfbr-symbols.md | first pass done | 214 names, 24,236 function pairs | item 1 |
| Recruiting | recruiting.md | pipeline, generation, tables, name pools, hometown-to-state link and skin/appearance (head id) mapped; commit loop, week-5 surplus, loaders and rating shaper mapped (section 11); per-week interest update (0x50dad4) open | 100 | item 2 and (a) partly |
| Players / depth chart / coach record fields | players.md | schema + enums done (data pass); no function-level map | 378 data-field rows in analysis/symbols/cfbr_data_fields.csv (95 with meaning); players 11, depthchart 1, coaches 11 function names | item 3 |
| Simulation, progression, injuries, draft | sim-and-slots.md | stage owners, leaving-status codes, redshirt/draft/transfer/graduation/training flow mapped (batch 1); numeric kernels open (batch 2) | draft 2 and injury 3 names in cfbr csv (players) | item 4; draft request/stay functions 0x481e20, 0x489664 found; INJY/INJR queries at 0x46bce0, 0x47362c |
| Team slots beyond 138 | sim-and-slots.md | field-width and capacity view done; code audit open | | item 5; see MODDING_REFERENCE 1.A and gap 4 |
| FCS second league | ../realism/fcs-league-feasibility.md | feasibility done (static); Phase 0 runtime test open | 22 functions + 2 sites (sim, rankings, league cursors, UI) | recommends rosterless TTYP-1 FCS teams + C caves |
| FBS+FCS universe (rostered FCS, about 266 teams) | ../realism/fbs-fcs-universe-plan.md | plan done; Phase 0 offline patches staged (save-grow-v0, u8-loops-v0); runtime T0.1-T0.3 open | site lists in analysis/fcs-universe/ | supersedes the sim-only D2 recommendation; active set = TTYP <= 1 |
| Schedule / postseason / dynasty | cfbr-symbols.md (csv only) | names ported from existing notes | schedule 31, postseason 20, dynasty 33 | no new analysis |

Conventions: confidence = confirmed / likely / guess. Decompiled pseudo-C stays in `analysis/mapping-cfbr-recruiting/` (local, not for the public repo).
