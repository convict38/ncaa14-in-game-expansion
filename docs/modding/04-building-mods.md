# How mods are built, and known gaps

Part of the [modding knowledge base](README.md). Our own analysis of NCAA Football 14 (PS3, BLUS31159) and the CFB Revamped v21 base: names, addresses, table layouts and how our mods are built. Source tags in brackets (for example TEA, CFBR) refer to private working notes that are not published; treat each statement as a compiled finding, not a re-verified fact. No game files, extracted assets or decompiled code are included.

## 4. How to add a mod today

There are two targets. Both consume the same patch stack: a list of `[be32, address, word]` entries written into the CFBR v21 ELF. Data mods (DB tables inside the `.ast` archives) are separate and need no code patch.

### 4.0 Decide what kind of mod it is

| Kind | Example | Route |
|---|---|---|
| Data only | roster, schedule presets (SKNW), conference tables, BOWL rows, team capacities | Edit TDB entries, repack, install via a stage (4.1) |
| Constant/word patch | change a literal (`li r6,0x7e`), a compare bound, retarget a vtable slot | `be32` entries in a `patch.yml` (4.2) |
| New logic | new rule, new playoff behaviour, news text | C cave in the CFBR segment-0 tail, plus a few hand-written site words (4.2) |
| Archive/asset | GameText strings, APT movies, textures | Equal-size in-place archive deltas (Appendix A) |

Always port by **query-string anchors and preimage checks**, not by raw numbers. Blanket numeric replacement of 126/125/127 immediates across the ELF is explicitly invalid (TEA, ATD in 1.A).

### 4.1 Data-only mods (both targets)

1. Parse and edit TDB tables with the project tools: `scripts/tdb_capacity.py` (read-only checksum validation and capacity builder), `tdb_records.edit_row`, `scripts/inspect_tdb.py` (`parse_db(path, set())` dumps all 173 tables). The TDB header CRC covers bytes +4..+35, and payload CRCs chain into the next table header (TEA, SSR). Example of a full data builder: `scripts/build_real2026_roster_v4.py`. The template archive entry has a 4,200-byte trailer after its declared TDB length that is text, not padding; keep it (TEA).
2. Archives are `QKL_*.AST` (BGFA 1.05) under `PS3_GAME/USRDIR`; BOOT entries 354/355 and MISC entry 150 carry the Dynasty template, roster and presets (Appendix A, 1.B). Changes are staged as equal-size in-place deltas, and some files are EDAT-wrapped (rollback restores a recorded hash).
3. New templates only apply to a **fresh Dynasty** (TEAM rows are copied at creation). (installer header chain, `install_cfbr_real2026_v26.ps1`)
4. **RPCS3:** wrap it in a stage: a new `scripts/cfbr_real2026_runtime_vNN.py` plus `scripts/install_cfbr_real2026_vNN.ps1`, each a copy of the previous version that adds one stage. Installers are create-only, refuse to run while a prior stage is enabled (roll back first), refuse while the isolated emulator runs, and record state in `evidence/cfbr-real2026-vNN-state.json` with backups in `patches/cfbr-real2026-vNN/runtime-backup/`. (installer header, D part 3)
5. **PC port:** the port reads the installed profile directly through a read-only VFS overlay (`PS3_VFS_OVERLAY`), so installing the data with the RPCS3 installer is enough. Delete `tools/ps3recomp-lane-e/edat_cache/` if an EDAT file changed. (`docs/pc-modded-build.md` section 4 and 6)

### 4.2 Code mods on RPCS3

Pipeline, in order. Sources: `docs/c-cave-toolchain.md`, `docs/code-room-and-news-fix.md`, `scripts/build_c_cave.py`, `tools/ppc-cave/cave.h`.

1. **Find the site.** Locate the function in the CFBR ELF (section 2 tables; use stock-to-CFBR pairs in 2.6 or re-anchor by query string, since CFBR generator bodies were never re-decoded, 1.B gaps). Record the preimage word at every site you will change.
2. **Write the cave in C** (freestanding, `#include "cave.h"`). Game functions are `extern` and given with `--defsym name=0xADDR` (the code entry address, never the OPD). EA-SQL queries use `EA_QUERY(GAME_STR(0x17...), &out, ...)`, which calls the generic EA-SQL helper (stock `0xa67320`, CFBR `0xa691b0`) with r3=r4=r5=0 and the query string in r6; it returns 0 when a row is found. Fixed game memory: `GAME_U32(addr)` etc. Hard rules: no r2 (TOC) use, no writable data, no function pointers (use inline `mtctr/bctrl` asm), no libc, entries only at call sites where clobbering volatiles is safe.
3. **Build:** `python scripts/build_c_cave.py SRC.c --base 0x1bc2700 --end 0x1bd0000 --defsym ea_query=0xa691b0 [-O s]` (`--base/--end` is the CFBR tail room). Outputs `NAME.words.txt`, `NAME.manifest.json`, `NAME.patch-lines.txt`, `NAME.lst` under `tools/ppc-cave/build/<name>/`. The post-link guard rejects any relocation, opcode or branch it cannot prove safe. Toolchain: zig 0.16.0 (clang 21.1.0) at `RCPS3/tools/ziglang`.
4. **Pick free cave addresses.** CFBR tail room is `0x1bc2700..0x1bd0000` (55,552 B). Used (from 2.6): news fix `0x1bc2700..0x1bc29cc`, modern rules v2 `0x1bc2a00..0x1bc3080` (range to `0x1bc4000` reserved), campus `0x1bc4000..0x1bc40cf`, projection `0x1bcff00..0x1bcff17`. **UNVERIFIED:** whether any other stage uses `0x1bc40d0..0x1bcfeff`; check the stage manifests under `patches/*/manifest.json` and `scripts/check_patch_yaml.py --all` before using it.
5. **Write a builder script** modelled on `scripts/build_cfbr_modern_rules_v2_patch.py`: work in `(addr, preimage, new word)` triples, assert every preimage against the pinned ELF, put the cave words plus the hand-encoded site words (`bl` encodings, `li`, repoints) into `patches/<name>/patch.yml` (format in 3.1) and a `patch_config.yml`. Only `be32` entries; keep `Notes:` free of `": "` (yaml-cpp otherwise silently drops the whole file).
6. **Gate offline:** `scripts/check_patch_yaml.py <patch.yml>` (or `--all`), your emulation test (`scripts/ppc64_mini_emu.py`, integer only; no FP/VMX), and the overlap check inside the stage helper.
7. **Add to a stage:** copy the latest `cfbr_real2026_runtime_v26.py` to `vNN`, add the patch directory to the stage's list, and bump the boot-check titles and `--expect-count "TITLE=N"` list. Total words are currently 2,034.
8. **Install and boot gate:** run `install_cfbr_real2026_vNN.ps1 -Action enable -Stage <name>` with the isolated emulator stopped. After a launch, `scripts/check_patch_applied.py` reads the new RPCS3 log for `PAT: Applied patch (... description='<title>') (<- N)` per title; a smaller N than expected means some addresses did not translate. If no fresh log exists the gate is unknown, not passed. (`v26-integrated-acceptance`)
9. **Test with a fresh Dynasty**, from a backed-up fixture (`fixtures/`, `evidence/`). Launch only the isolated runtime through the project's controller route (`scripts/control_isolated_rpcs3.py`, MCP `ncaa14-fast-drive`); never touch the user's primary RPCS3 install or original saves. (`docs/fast-drive.md`, `alternate-control.md`)

RPCS3 build used: `0.0.43-20250-304d544b`. It also supports patch types `calloc`, `jump`, `jumpl`, `jumpf`, `alloc`, but no project patch uses them, and the PC-port builder refuses them (3.1).

### 4.3 Code mods on the PC port (`tools\ps3recomp-lane-e`)

The PC port does not run RPCS3's patch engine. It applies the **same stage's `be32` words offline to the ELF, then lifts the whole patched ELF to C++ and compiles it**. (`pc-modded-build.md` section 1 and 6; `modbuild/rebuild_modded.ps1`)

Mod, rebuild, test:

1. Do 4.2 steps 1 to 7 (write the cave, write the builder, add the patch to a stage). The stage must be defined by the project's installer helper, because `build_modded_elf.py` imports its `patch_text()` and checks the result byte-for-byte against the installed `runtime/patches/patch.yml`.
2. Run `powershell -File tools\ps3recomp-lane-e\modbuild\rebuild_modded.ps1 -Stage <stage>`. It performs, in order (`modbuild/rebuild_modded.ps1`, `HANDOFF_NEXT.md`):
   1. `build_modded_elf.py`: ELF + every `be32` word, counts checked against the manifest preimages, and segment 0 (`p_filesz/p_memsz`) grown over the tail room your cave uses (the zero gap in the file already exists). Writes `vfs\PS3_GAME\USRDIR\EBOOT.elf` and `modbuild/mod_elf_report.json` (per-title counts, tail range, cave entry list).
   2. `ppu_loader.py` (OPD functions and imports).
   3. `add_cave_functions.py`: clamps the last OPD function at the last EXECINSTR section end (`0x16d9f00` on the v24-era build) and registers every cave entry point from the report as a function. Branch targets inside the cave that are not listed are promoted by the lifter.
   4. `ppu_lifter.py` with `PPU_LIFT_DATA_HOLES` (rodata between `.text` and the cave) into `ps3recomp\src\recomp` (about 612 MB of C++ in 15 chunks).
   5. `restore_ppu_recomp_h.py`: the lifter regenerates `ppu_recomp.h` without the hand-maintained VM_INLINE_FAST and coherent-VMX-store blocks; this script re-adds them (Step 72E gotcha).
   6. `build_game_e.bat`: clang-cl/ninja build of `MyGameRecomp.exe`; `run_e.ps1` copies it to `MyGameRecomp_laneE.exe`.
3. Test with `run_e.ps1 -Name <run> -Seconds 600 -Nav` and the lane's oracle/queue harness (`harness/abrun.sh`, `harness/RUNQUEUE.md`). Saves live under `cwd_e/gamedata`. Validation scripts: `modbuild/check_pc_season.py`, `check_pc_dynasty.py`.

Constraints that matter for modders:
- A patch that uses `calloc`/`jump*` is refused by `build_modded_elf.py`. Only plain `be32`. (`pc-modded-build.md` section 6)
- Cave code must live in the segment-0 tail (up to `align(vaddr+memsz, 64 KB)`); anything else needs new executable-segment support that does not exist. (`build_modded_elf.py` docstring)
- Code changes cost a full re-lift plus a large build; runtime-only/libs-only builds take seconds, SPU-image changes 1 to 2 hours (`HANDOFF_NEXT.md`, "Builds"). **UNVERIFIED:** wall-clock time of a full PPU re-lift.
- The lane is shared. At the time of writing another agent is working in `tools\ps3recomp-lane-e` (runqueue daemon, GRANT protocol in `harness/RUNQUEUE.md`, kill rule: only by PID, path-checked). Coordinate before building or running, and do not edit session scripts while a session runs. This document's author did not touch that tree.
- Not a code-mod path: the lane's `main.cpp` env defaults, RSX/SPU flags, HLE units. Those tune the runtime, not game logic. The pre-existing `ps3_indirect_call` and `vm_read*/vm_write*` runtime functions are the only guest-memory interfaces the generated code uses (see section 6).

PC-port status (for judging risk): playable, Super Sim correct, about 22 to 24 fps in heavy gameplay (`HANDOFF_NEXT.md`); full Dynasty loop (preseason through rollover) passes (`pc-mode-validation.md`); the v26 re-lift is done in the lane ("exe 20:36") with an oracle run queued (`HANDOFF_NEXT.md`, Step 72E); see Appendix C.

## 5. Known gaps, ranked by usefulness to modders

Ranking is my judgement of how many future mods each missing piece blocks, weighted by how little is known now. Evidence for each item comes from the raw gap lists in sections 1 to 3 (tags in brackets) and the appendices. "Not mapped" means no note in the folders listed in the task describes it; it may still exist in notes I did not read (the 258 KB `docs/continuation-checkpoint.md` and 768 KB boot log were searched, not read whole).

| Rank | Gap | Why it matters | What is known / missing |
|---|---|---|---|
| 1 | **Field-level maps of player, depth-chart and coach records** (PLAY, DCHT, COCH, CSKL, COPS, and the ratings inside them) | Almost every roster, ratings, progression or coach mod needs them | Only table names, row counts and a few keys are in the notes: PLAY is addressed by `TGID*70` bounds and has PGID/PTYP/PPOS/PYEA/PHGT/PWGT/OVR; COCH is 429 records x 176 B x 155 fields, GOPT 176 B/151 fields, MOPT 24 B/64 fields, UOPT 12 B/14 fields, all undecoded. The `dynasty-constructor` and `dynasty-object` folders contain only adapter/dispatch thunks, not record layouts. No catalog of all 173 table schemas is in the docs; the schemas live in the TDB headers and can be extracted with `inspect_tdb.py`. [D.1 gap 13, 1.C E2, SSR] |
| 2 | **Simulation, AI and progression formulas** | Difficulty, realism, player development, injuries, play calling | Not mapped: play-by-play engine, CPU play-call AI, injuries, in-season/offseason player progression, draft, transfer portal logic. Only the game-clock/OT/points rules (CFBR addresses) and season-advance dispatch are known. No difficulty/slider table located; home-win rate 54.6% vs real 63.4% is unexplained. The `stock-progression` folder is save fixtures, not formulas. [D.3 item 14, D.2 gaps 5.26 to 5.28] |
| 3 | **Recruiting algorithms** | Recruiting is the core Dynasty loop and the most requested mod area | Memory layouts of RecruitMan, RecruitPrefMan and the board are mapped for capacity purposes (1.A), but pitch/interest/commit scoring, prestige and star ratings, and the destination of a commit are not (board membership plus commit status does not identify the destination team; fields `+0xf05/+0xf06/+0xf07/+0xf2e` undocumented). [D.1 gaps 8, 9] |
| 4 | **Team expansion past 138 (FCS promotion) is unmapped** | Adding more teams, FCS league | CORRECTION (main session, 2026-10-28): the old A138 crash note is out of date. 138 FBS teams now run on the PC port: `pc-modded-build.md` dynasty_check shows 138 FBS, 12 games each, and rollover into 2027. Exact-v26 RPCS3 acceptance is still open because of the RPCS3 "Not enough memory" fatal, which is not a team-count failure. Older notes for going beyond 138: 44 compare-126 sites reviewed but whole ELF still has 107 unpatched 126, 63 125, 528 127 immediates and unscanned heap arrays. Remaining UI caps (`0x1e1660`, `0x1e2ca0`, `0x1e1018`, `0x1a2e3c`...) unpatched. History tables near capacity (RBKS 3402/3643). [D.1 gaps 1 to 5, D.3 item 12] |
| 5 | **Unified CFBR symbol map** | Every future mod needs a CFBR address; most notes are STOCK-only | The CFBR ELF has no function name database. Ports are by address mapping (3.66M anchor pairs) and query-string anchors; CFBR generator bodies were never re-decoded; the CFBR ranking execution trace was never obtained. A single `symbols.tsv` (name, stock addr, CFBR addr, signature hash) would turn sections 2.A to 2.C into machine-usable input, and is a prerequisite for section 6. [D.2 gap 5.6, D.3 item 9, Appendix D] |
| 6 | **Hook/cave interface on the PC port** | Mods currently = hand-built `be32` word lists + full re-lift | Only plain `be32`, only in the segment-0 tail; no runtime hooks; each code change is a re-lift and long build. Section 6 sketches a design. [4.3, Appendix C] |
| 7 | **Rules beyond clock/OT**: penalties, quarter length, play clock UI, scoring state | Rule mods other than OT/2-pt | Rule constants live in code-built clock config at `0x111dc28` (CFBR) with no DB table; live game-state score fields not statically located, so a tied score cannot be poked; no stamina/fatigue retune for extra plays; two-minute stoppage graphic never captured. Rules v2 OT retest outcome is not in the notes read. [D.3 items 1 to 4] |
| 8 | **Schedule/conference generator for modern alignments** | Realignment, 17/18-team conferences, rivalries | Style selector returns null for 17+; flag choosing table-driven vs style-driven generation (r5 of `0xfcab0`) not decoded; "Custom Conferences" untested; SKNW row at SESI 7 references nonexistent TGID 190; Dec-1-is-Sunday seasons have labels one week early (anchor `0x4d8654`). [D.2 gaps 5.1 to 5.11, 5.17] |
| 9 | **Stage machine and offseason pipeline** | Offseason mods (draft, signing day, transfers) | Dispatch to stage functions is mapped (vtable slots `0x58/0x68/0x6c/0x22c`), but callback bundles per phase and the SEAI/MOIN stage query fields (MCSA, MPSA, SSTG, SNPW, ...) are only observed. Playoff round advancement/champion recording have their own docs but no in-game acceptance of the whole v26 stack. [D.2 gaps 5.26 to 5.29] |
| 10 | **Presentation: UI movies, stadiums, uniforms, news text** | Visual mods | Equal-size archive deltas work (GameText year, Coach Contract movie) but the APT/UI toolchain is incomplete: no playoff bracket screen (no APT writer), BPLO bowl-card badge binding unresolved, stadium creation in Dynasty unproven (`0x17ebc8` is the TeamBuilder path), SUID thumbnails stale, other 126-capped UI lists unpatched. [D.3 items 6, 8, 11 to 13, Appendix A] |
| 11 | **Recruiting/roster data edge cases**: coach lifetime, player-ID uniqueness, 8-bit rank fields | Edge failures in long dynasties | COCH has only 3 free slots in recent saves; CREP/CONT lifetimes unproven; TCRK/TMRK/TBRK are u8 and 128+ consumers unproved; save container (~4.6 to 5.2 MB trailer) opaque; save-size ceiling 8,278,016 not raised; `SEYR` values >= 64 into 6-bit fields untraced. [D.1 gaps 7, 10 to 12, D.2 gaps 5.13 to 5.15, 5.23] |
| 12 | **Exact-v26 integrated acceptance** | Confidence that the whole stack works together | Not done: RPCS3 fatal "Not enough memory" before the EBOOT on Oct 26/27; only a historical Oct 21 boot log and an earlier-stack 12-team CFP run support it. [`v26-integrated-acceptance`] |

### 5.1 Raw gap lists

The unranked, source-tagged lists that fed the ranking are reproduced in Appendix D: D.1 (teams/recruiting, referred to above as 1.A gaps), D.2 (schedule/calendar/stage machine, 1.B gaps), D.3 (rules/playoff/coach/news/UI/stats, formerly 1.C F3 items) and D.4 (patch pass). Item numbers in the ranking table refer to those lists.

