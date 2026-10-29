# Appendices: archives, community mods, PC-port facts, open items

Part of the [modding knowledge base](README.md). Our own analysis of NCAA Football 14 (PS3, BLUS31159) and the CFB Revamped v21 base: names, addresses, table layouts and how our mods are built. Source tags in brackets (for example TEA, CFBR) refer to private working notes that are not published; treat each statement as a compiled finding, not a re-verified fact. No game files, extracted assets or decompiled code are included.

## Appendix A. Assets and archives a modder needs

| archive | entries | size | content |
|---|---:|---|---|
| QKL_BOOT.AST | 827 | 90 MB | Dynasty/roster/template TDB tables (354 = nested GAMEMODE template, payload at offset 121; 355 = roster; 826 = TRPY etc.); 117 nested BGFA |
| QKL_FE2IG.AST | 4,665 | 3.29 GB | front-end/in-game art; 2,252 nested BGFA; 4664 = BOWL/TRPY copy, 2565 = GameText movie; uniforms, fields, helmets, logo decals, stadium models |
| QKL_INTERFACE.AST | 676 | 329 MB | UI chrome; 674 nested BGFA; 141 TEAMLOGOS, 123 BOWLLOGOS, 140 STADIUMSELECT, 132 MASCOTS, 143 trophy images, 338 Coach Contract movie, 459 GameText movie |
| QKL_MISC.AST | 1,593 | 214 MB | mixed: 464 nested BGFA, 542 p3R entries, 19 raw DDS, 10 PNG; entry 145 = playoff BOWL source / template copy; 150 = SCHE schedule (CFBR's is byte-identical to stock) |
| QKL_STREAM.AST | 6,588 | 1.88 GB | video/stream; 157 = 3dlogos_big (3DLOGOS_<CSAT>) |
[graphics-asset-pipeline.md 1.1; team-art-plan.md 1.2; cfbr-real2026.md]
- Index records: `flags, key(8), offset, zsize, extra`; header word 2 = count+1, word 6 = index bytes; flags&1 = zlib, flags>>8 = type table index. Top-level indexes unsorted; nested name-ordered with later additions appended. [team-art-plan.md 12.1]
- Keys: top-level and named nested = FNV-1a-64 of UPPERCASE name, little-endian (verified NDSUXX_HELMET_2022_GREEN -> 18a8f444550218c5); INTERFACE swappable libraries key = u32le(image_id) || u32le(library_tag), e.g. TEAMLOGOS tag 0x954ed745 so NDSU logo 167 -> a700000045d74e95; BOWLLOGOS tag 0xfed68f7a. [team-art-plan.md 1.1]
- Textures: INTERFACE plain `DDS `; FE2IG/MISC/DLC use `p3R\x02` = DDS header with magic replaced (CFBRevamped SDK / Ember, MIT); DXT1/3/5 blocks linear, NO swizzle (Xbox XPR2 only needs retile). [team-art-plan.md 1.1]
- Authoring specs: team logo DDS DXT5 512x512, 10 mips, 349,680 B (replace placeholder child in INTERFACE 141; fill id+340 for alt); bowl logo DXT5 256x256 9 mips 87,536 B (INTERFACE 123, id 17 free); trophy image 256x256 DXT3/5 65,664 B (INTERFACE 143, TRPY.TIID hypothesis); field DXT1 2048x4096 13 mips (CFBR) keyed by STAD.FLID; uniforms p3R DXT5 helmet 2048x1024 12 mips, Riddell 256^2 DXT1. [team-art-plan.md section 6]
- CFBR grew TEAMLOGOS 343 -> 1024 slots (595 are 144-byte placeholders). [team-art-plan.md 0, 1.2]
- Which TEAM/STAD/BOWL field drives which asset: TEAM.TLGL/TLGS (9-bit logo ids) -> menu/ticker logos; TEAM.CSAT (6-char X-padded string e.g. ARIZON, JMUXXX, NDSUXX) -> all 3D uniform/helmet/glove/goalpad/banner/cheer/3D logo/logo decal names; STAD.FLID -> field; STAD.STAA/SUID -> stadium model; STAD.SORD -> Select Stadium order; BOWL.BLGO -> bowl logo; BOWL.UTID = TRPY.UTID -> trophy name/model/image; TEAM.TCID = city id (equals STAD.SCYD), not colour; TGPT/TGRP/TSID/TMPI unproven. [team-art-plan.md 1.2, 12.1]
- A new code needs in FE2IG: <CSAT>_MixAndMatch, _logo_DECAL, _BOTH_CLUSTERCHEERLEADER_big, <FLID>_FIELD_big, <STAA>STADIUM_big; goal pads/banners/35yd/3D logos optional. Stadium code also keys FE2IG 3106 director, CLUSTERS, VIGNETTEOVERRIDES, 223 lighting. [team-art-plan.md 12.1]
- Archive editing without rewriting 3.6 GB: scripts/gfx-art/bgfa_build.py `TopDelta` (index grows into first payload space; that payload moves to end byte-identical; new/replaced payloads appended; in-place equal-size regions for changed data; rollback truncates and restores). public-repo/tools/bgfa_archive.py and scripts/inspect_bgfa.py read/replace entries (hash-verified, append-only). `rename_blob` re-keys a big. Whole-file replacement or running the stock archive builder on CFBR archives would discard CFBR changes (22 BOOT + 331 MISC payloads differ; index field widths differ). [team-art-plan.md 12.1; cfbr-integration.md; graphics-asset-pipeline.md]
- Table tools: scripts/tdb_records.py, tdb_capacity.py (schema-driven row editor + CRC); TDB signature `DB\x00\x08` (4442000801000000). [graphics-asset-pipeline.md]
4.2 DLC and EDAT
- DLC bigs and packs live under game/BLUS31159/USRDIR/DLC/: CFBR_DLC_CUSTOM, CFBR_DLC_V17/18/19, UNIF001..016, our NCAA14X_ART2 (76 plain .ast in v24; v25 union adds ~51 more), plus DLC/qkl_patch.ast.edat (CFBR title-update archive, ~499-500 MB, EDAT v3). [pc-modded-build.md section 1a; team-art-plan.md s18]
- File naming: `<ENTRY>-<TEAMCODE>_<SLOT>_<YEAR>_<COLOR>_<big|BIG>.ast.edat` and `<TEAMCODE>_Pack0_MixAndMatch.XML.edat`. .edat = PS3 NPD encryption wrapper; payload is .ast. [graphics-asset-pipeline.md 2]
- EDAT params: NPD EDAT v3, license 3 (free), flags 0x0C, block 0x4000, content id UP0006-BLUS31159_00-NCAAFOOTBALL1400. klicensee stored in the ELF: stock ELF offset 0x172eefc; CFBR ELF 0x173215c (per team-art-plan 14.4). Tool: scripts/GfxEdatDecrypt.java (findklic, decrypt; format ref RPCS3 unedat.cpp/key_vault.h GPLv2 read-only) kept OUT of public-repo (DRM key handling). [team-art-plan.md section 6, 8, 14.4]
- Loader behaviour: game probes `<name>.edat` with sceNpDrmIsAvailable and on CELL_ENOENT opens the plain `<name>`; every USRDIR/DLC/* subfolder is scanned; CFBR itself ships loose unencrypted files; so our packs go UNENCRYPTED into USRDIR/DLC/NCAA14X_ART2/ (runtime-verified art4: no EDAT encrypt step needed). Empty `MICHIG_Pack2` disables a pack. [team-art-plan.md 12.1, 18]
- Equal-size in-place EDAT delta (v21): re-encrypt only the changed blocks + their CMACs (3 regions: header/metadata CMACs 0x90..0xB0 and 2 block CMACs; entry 28 of qkl_patch.ast.edat = GameText copy served). [cfbr_real2026_runtime_v26.py; install_v21 header]
- Community pack caveat: Delaware pack author unknown; NOT redistributable until permission confirmed. [team-art-plan.md 12 / third-party/community/CREDITS.md]
4.3 GameText / year
- GameText.NCAA_RELEASE_YEAR is one byte in an APT GameText movie in three archives (qkl_boot.ast 755, qkl_fe2ig.ast 2565, qkl_interface.ast 459) AND in the served qkl_patch.ast.edat entry 28; the dyn60 stage alone has no visible year effect until the EDAT delta (v21) is applied. [install_v20/v21 headers]
- Record-book date: RBKS/RBKN.RCDD = (year-1900)<<9 | Dec 31, built as (SSYE<<9)+(113<<9) at code 0xdbf74 (school) and 0xd8e08 (NCAA); stored holder text keeps old year. [continuation-checkpoint.md 2026-10-18]
4.4 qkl_* naming details that matter
- Both stock and CFBR files are `qkl_boot.ast`, `qkl_misc.ast`, `qkl_interface.ast`, `qkl_fe2ig.ast`, `qkl_stream.ast` (CFBR originals sha: boot 1a367a14..., misc 883d13e3..., fe2ig d69c737e...). Extracted CFBR copies at third-party/cfbr-v21/extracted/entry-0006-qkl_boot.ast, entry-0009-qkl_misc.ast, entry-0007-qkl_fe2ig.ast, entry-0024-EBOOT.elf, entry-0026-qkl_patch.ast.edat, entry-2451-USR-DATA (roster 6ef52375...). [cfbr_real2026_runtime_v26.py; cfbr-real2026.md]
- Roster routing: fresh profiles have no ROSTER save; log shows only PROFILE auto-load, so BOOT entry 355 is where CFBR23V21 content goes; a profile that still holds a CFBR23V21 ROSTER save would load that save instead. [cfbr-real2026.md]
- Runtime CFBR facts: bundled CFBR23V21 roster = 126 FBS, 141 TEAM rows; qkl_patch.ast.edat does NOT override SCHE (726 season-0 SKNW presets appear exactly in saved SCHD). [cfbr-real2026.md]
- BPLO / bowl-card badge binding for ESPN bowl cards: NOT found after extensive search (team-art-plan.md 17.x, closed unresolved). UNVERIFIED which container holds it.
- Save limits: fixed USR-DATA 8,278,016 bytes; history capacities TSHS/BCHH/CCHH/CREP raised in template (dyn60). [cfbr-real2026.md; install_v20 header]


## Appendix B. Community mods and licensing notes

- College Football Revamped (CFBR): github.com/cfbrevamped/CFBR, CFBR-Easy-Installer (v21 dated 2023-09-06, PS3/PC), Kuefo/CFBRevamped tools. No explicit license; freely distributed. PS3/Xbox/RPCS3. Contents: uniforms, helmets, fields, logos, splash, lighting, models, playbooks. Notes: CFBR "no specific rules changes documented". Our staged package: 7,823,052,432 bytes, 2,452 entries (2,421 files + 31 dirs), SHA-256 837afea6...2065 (our download identity). [community-mod-survey.md; cfbr-integration.md]
- NCAA NEXT 24/25 (ncaanext): NCAA 06 PC platform (distinct from NCAA 14); 40,000+ textures, 1,200+ uniforms, modern OT, 40 s play clock, 2023+ clock rules; no license stated. Useful as reference for modern-rules behaviour, not directly portable.
- NCAA 14 In-Game Expansion (convict38/ncaa14-in-game-expansion): this IS the user's public repo (docs/public-repository.md): 127+ FBS, prototype 12-team playoff; no public installer yet.
- Tools: NCAA 14 Utility Tool 2.0 (Bowersrd; 4/8-team playoff setup, bowl editing), Dynasty Tool v2 (Bowersrd; 12-team playoff via external save steps, swaps teams into existing slots), antdroidx NCAA DB Editor, TeamCrafters Classic Roster Importer (GPL-3.0), ncaanext textures downloader, jtfresh90 NCAA 2K3/2005 editors (GameCube texture pipeline reference), NVIDIA Texture Tools Exporter (proprietary, do not redistribute), QuickBMS (Luigi Auriemma bms scripts nbajam*.bms in analysis/), Noesis (Xbox), AST Editor (CFR Discord #Tools).
- No standalone uniform packs for James Madison, Sam Houston, Liberty, Jacksonville State, Kennesaw State, Delaware, Missouri State, Sacramento State, NDSU etc. in public search at survey time; later user supplied community packs (see CREDITS.md). CFBR itself ships JMU (JMUXXX), FIU, NDSU, Sam Houston, Missouri State (XML only), UConn (XML only) assets. [graphics-asset-pipeline.md 2]
- CFBR renames 5 existing TGIDs rather than adding new ones; for 4 of 5 swaps CFBR reused donor art with only display strings changed (precedent for "rename + keep donor art"). [graphics-asset-pipeline.md 2]
- Licensing summary from survey: CFBR/NEXT/GitHub tools "safe to include with attribution and links" (survey's own recommendation, UNVERIFIED legally since no LICENSE files); NVIDIA tools link only; CFP branding assets would need permission; individual community designer assets may need creator consent; OperationSports threads: attribute and link. [community-mod-survey.md sections 7-8]
- Project policy (user memory + repo docs): community packs OK for personal non-commercial use, keep credits list; no EA files / CFBR files / decrypted executables / saves / game-derived output in public repo; Delaware pack marked do-not-redistribute pending author permission. [memory MEMORY.md community-assets-policy; third-party/community/CREDITS.md; cfbr-integration.md "No CFBR assets..."]
- Credits table authors seen: clmzntyger (Kennesaw State, Jacksonville State, Sam Houston), FootballGamer42 (NDSU field), mdotjenkins (Liberty), FTk Ray (Sacramento State), Delaware author unknown (CFBR Discord). [CREDITS.md]
- Public repo rules: github.com/convict38/ncaa14-in-game-expansion, public reviewed export at the private workspace public-repo folder; push only explicitly reviewed text/source; never push the private workspace wholesale; exclude game images, executables, archives, assets, firmware, saves, raw logs, memory dumps, decompiled code, third-party bundles, credentials, personal paths; recompute export-manifest hashes after change; update changelog/status after each validated milestone; gh CLI not authenticated, push via git credential manager works (2026-10-10 on) or GitHub connector API. Latest logged push in docs: 8e7efe7 (2026-10-13, PC build sound + analog controls; via publish42.bat). [public-repository.md]
- Related project: Dynasty/IP notes: static recompilation only defensible as a tool that translates code the user already owns, no assets/decrypted executables shipped (N64Recomp/UnleashedRecomp model); not legal advice. [windows-port-feasibility.md section 5]


## Appendix C. ps3recomp / PC-port facts

6.1 Lift of the stock EBOOT (spike, 2026-10-10)
- Source: github.com/NoahBPeterson/ps3recomp (MIT; v0.12.1 as of Sept 2026). Pipeline: ppu_loader.py -> ppu_lifter.py -> gen_hle_nids.py -> CMake/MSVC (clang-cl later). Tools at tools/ps3recomp-spike (lane A). [ps3recomp-spike.md; windows-port-feasibility.md]
- Stock ELF: entry OPD 0x1bc0e48 -> code 0x10250, module TOC 0x1c64fd0, OPD region size 0x9c198, 79,923 OPD descriptors -> 57,985 unique entry points, 2 PT_LOAD segments, 360 firmware imports in 25 libraries (95% NID-named; 17 unresolved names). Code+rodata segment filesz 29,028,584; data segment filesz 962,780 / memsz 1,642,680. [ps3recomp-spike.md; windows-port-feasibility.md]
- Lift: 104,644 functions (57,985 + 14,316 tail-entry wrappers), 43,250 call targets, 616 MB C++ in 15 chunks (~8.54M lines); first pass 6.5% functions contained unlifted instructions (mostly AltiVec/VMX: vmx_x531/x452/x1036, stvrx/stvlx, plus 41 ambiguous ld/std/rld forms); after Step 1 (~38 opcode entries added to lifter, upstreamable) 99.49% (104,115/104,644) clean, remaining 529 are reserved/unassigned bit patterns = misdecoded data. [ps3recomp-spike.md; ps3recomp-boot-log.md Step 1, Public-safe summary]
- Correctness spot check: stock 0x4CEEDC (week advance), 0x45997C (fill primitive), 0x50614C (result commit) all lift to sane functions matching playoff-engine-map.md; 0xa67320 is the generic EA-SQL query wrapper. [ps3recomp-spike.md section 5]
- SPU: only 2 embedded SPU ELFs: at 0x1931080 (5,268 B, SPURS kernel stub) and 0x1A67400 (74,580 B, 838 funcs; shuffle/fixed-point/DMA heavy, guessed to be decompression or audio, UNVERIFIED); but at runtime ~18 EA job binaries (compilejoints, ANT, dxt_encoder, sound, GameSkinning, ...) are lifted, 155 lifted SPU images in the lane E build. SPU is reached via cellSpurs; ps3recomp cellSpurs HLE was "Partial: no actual SPU execution". [ps3recomp-spike.md; pc-modded-build.md 3.3; ps3recomp-boot-log.md Step 36E]
- HLE import gaps at spike time: 27 of 360 imports (7.5%) in 4 modules had zero HLE: cellCelpEnc(9), cellCelp8Enc(9), cellSearchUtility(8), sysBdMediaId(1); Step 2 added stubs for them. [ps3recomp-spike.md section 4; boot log Step 2]
- Link: 238 MB native Windows exe via clang-cl/lld-link; fixed: D3D12 backend GUID-header include-order bug; real hang cause #1: runtime sys_semaphore table of 256 slots filled by the title's own boot (257th create silently failed; table enlarged). [ps3recomp-boot-log.md Public-safe summary]
- RSX: ps3recomp targets D3D12 (Windows), Metal (cannot load titles), CPU headless rasterizer; no Vulkan in ps3recomp. [windows-port-feasibility.md]
- Licensing: RPCS3 is GPLv2; copying its PPUTranslator/SPU/RSX/HLE code would pull the port under GPLv2; reference-only reading keeps ps3recomp MIT/clean-room. [windows-port-feasibility.md section 3]
- Effort tiers (feasibility doc, 2026-10): spike (days-weeks) -> boot-to-menu (person-months) -> playable (person-years at public tooling maturity) -> mod-friendly tier where address patches become source patches. Achieved by lane work far faster than predicted (see 6.3). [windows-port-feasibility.md section 6; boot log]

6.2 How patches are applied on the PC port (lane E, modded build)  [pc-modded-build.md]
- The PC build does not run RPCS3's patch engine. Patches are applied OFFLINE to the ELF before lifting:
  1. tools/ps3recomp-lane-e/modbuild/build_modded_elf.py imports the installer helper's patch_text() (same patch dirs, same sha pins, YAML gate, overlap check, order), checks its block is byte-for-byte inside the installed runtime/patches/patch.yml, then applies every entry with RPCS3 semantics (be32 at virtual address, file order; addresses translate within segment 0 up to align(vaddr+memsz, 64K) = the tail, or within segment 1 file data; untranslatable would be skipped and not counted: none were). 1,976 entries with manifest preimages were checked against the ELF; all match.
  2. The tail is materialised: p_filesz/p_memsz of segment 0 grow from 0x1bb26e8 to 0x1bb3080 (to 0x1bc3080 in vaddr terms per doc); segment 1's file offset keeps vaddr-offset equal to segment 0's, so the zero gap IS the tail.
  3. Re-read count check: 10/10 titles, 2,032/2,032 words (the v24 stack at that time). Output vfs/PS3_GAME/USRDIR/EBOOT.elf sha256 30ba36be6e560bdecd7c700c7e9961cf037b7ea0d634709600414fd720178e86 and modbuild/mod_elf_report.json (v24-era; not the v26 one).
  4. Lists 14 cave entry points (bl/b targets into tail and function pointers written into/out of tail); descriptors at 0x1bc3070/0x1bc3078 name 0x1bc2a00 (OT-rules setup) and 0x1bc2dc0 (pointsrules slot 0x4c pr_add).
  5. Lift: ppu_loader.py on the modded ELF (79,939 OPDs, 57,998 functions, 360 imports); modbuild/add_cave_functions.py clamps the last OPD function at last EXECINSTR section end 0x16d9f00 and adds the 14 cave functions; ppu_lifter with env PPU_LIFT_DATA_HOLES=16d9f00-1bc26e8 and lane E's lifter patch (branch targets in a data hole treated like outside --code-end; without it CFBR's in-.text literal data seeded a cascade to 130,175 functions / 68 chunks / 3.7 GB; with it 104,743 functions / 14,361 tail-entry wrappers / 15 chunks / 612 MB). The patch-code (EASP writer site 0x4aa59c) lifts as `ctx->lr = 0x004AA5A0; func_01BC2700(ctx);`.
  6. Build: clang-cl from lane A's portable LLVM, ninja -j4 via configure_game_e.bat/build_game_e.bat; modbuild/rebuild_modded.ps1 does 2-4 plus ELF step. Exe MyGameRecomp_laneE.exe (~295 MB), cwd cwd_e.
- If a patch used calloc/jump*, build_modded_elf.py refuses (needs new executable segment support). [pc-modded-build.md section 6]
- When mod changes: data only -> reinstall via RPCS3 installer (the overlay reads new files next run; delete edat_cache/ if an EDAT changed); code -> rebuild_modded.ps1 -Stage <stage>; lane A runtime fixes -> re-sync and reapply lane E source patches (apply_overlay_patch.py, apply_lifter_holes_patch.py, edat.c/edat.h/stubs.cpp blocks marked "Lane E", then remap_spu_job_eas.py --apply on a fresh jobmods_register.c; not idempotent). [pc-modded-build.md section 6]
- SPU: pm_kernel.elf and workload.elf byte-identical in CFBR EBOOT; of 18 lifted stock job binaries 7 found at stock+0x3600 (EA registrations remapped), 11 are different builds (sound jobs, GCM park job, dxt_encoder, RLEDecode, job_util_memcpy, GameSkinning, ANT_kernel, InterpJointsSQT, CrowdCull ...), later captured with SPU_JOBLOG_DUMP and lifted (images 40-50). [pc-modded-build.md 3.3; boot log Step 36E]
- Data: no game file copied. PS3_VFS_OVERLAY (sys_fs.c) "<marker>=<host dir>;..." read-only overlay: /USRDIR/DLC -> profile game/BLUS31159/USRDIR/DLC, ICON0.PNG and PARAM.SFO -> profile, /PS3_GAME and /USRDIR -> profile disc dirs; local files win; write opens on overlay refused (CELL_EACCES). EDAT: runtime decrypts NPD transparently; lane E added sceNpDrmIsAvailable/sceNpDrmIsAvailable2 HLE handlers handing the klicensee to the decryptor (edat_add_klic, verified against each file dev_hash), PS3_EDAT_KLIC fallback, PS3_EDAT_CACHE_DIR -> tools/ps3recomp-lane-e/edat_cache/. Saves: cellSaveData writes cwd_e/gamedata/...; PS3_HDD0_ROOT never set. [pc-modded-build.md section 4]
- Run: `powershell -File tools\ps3recomp-lane-e\run_e.ps1 -Name <run> -Seconds 600 -Nav [-Cap] [-Debug]`; input via tools35/press.sh (PAD_FILE), screenshots tools35/shot.sh (RSX capture). Manual-session grant protocol via harness/RUNQUEUE.md. [pc-modded-build.md section 5; pc-mode-validation.md section 0]
- NOTE: instruction was not to touch tools\ps3recomp-lane-e; only docs were read.

6.3 Boot-log milestones (ps3recomp-boot-log.md, 768 KB; searched headings and keyword counts: HLE 73 hits, hook 30, cave 16, patch.yml 2, PPU patch 0, YAML 0)
- Step 1-3: lift complete, 4 HLE stubs, link OK. Step 4-5: first run blocked; real cause = semaphore table (see above), SPU job red herring. Steps 6-13: job manager wake / null pointer / SPU interpreter test / audio soft-skip; Step 11-12 BGFA/zlib theory disproved (no zlib in SPU job; writers are lock-free primitives). Step 15-20: differential tooling against RPCS3 over GDB (watchpoints unsupported, Z0 breakpoints supported). Step 21-25: unregistered sys_memory_allocate_from_container, send_event ENOTCONN dropped user events, main-RAM->VRAM copy, GPU fence/FIFO walker semantic fixes. Step 26-33: GCM wrapper, stencil/depth, cellFsLseek 32-bit bug (TDB with SRPT lives past 2 GB in QKL_FE2IG.AST), lifter callee-save bug (75 bad reloads), unlifted dxt_encoder job, readback blit fix; field renders. Step 34D-35: mode matrix, network HLE fix, NaN players fixed. Step 35E-36E: modded build boots and plays a full season. Step 39D/39E: Super Sim score bug = 13 VMX integer emitters reading big-endian vector lanes via host-typed pointers (fixed in lifter). Step 40E-84E: frame rate ~3 -> ~9 -> ~14.8 fps, sound works, SPU FTZ/DAZ fix (Step 52E) for corrupt sim, sRGB output (62E), JOBHANG root cause stale runtime lift (53E), game speed 0.43 -> ~0.99 with fast-ANT bundle (Step 83E/84E; RT_ANT3/SPU_LOOKUP_MEMO opt-ins carry a residual ANT-module race hang risk). Tools: run queue, harness pause PLAY.LOCK, borderless+VRR (Step 82E). [ps3recomp-boot-log.md headings]
- "cave" in boot log: only Step 35E/36E refer to patch caves (tail caves lifted, 14 cave functions). "hook" hits are runtime hooks (SPU channel/event hooks, e.g. ps3_spu_job_complete_pending, g_spu_user_event_hook), not game patch hooks. [grep results]
- Continuation-checkpoint (258 KB) cave/YAML hits are about patch.yml failures and install/rollback hash verification, playoff v0 cave placement (0x459e24..0x45a618), C cave toolchain DONE note (line 1092), news-fix runtime test (line 1779-1804). [grep results]

6.4 HLE audit conclusions
- hle-audit-2026-10-12.json: 257 confirmed divergences (30 rejected) between ps3recomp HLE and RPCS3 reference across 36 units; severity field absent in confirmed entries (all '?' in my parse); doc cites medium/high levels. [hle-audit-2026-10-12.json; ps3recomp-mode-matrix.md finding 11]
- Applied in lane D tree (tools/ps3recomp-lane-d/ps3recomp/libs/network): cellNetCtl.c (GetState returns CELL_OK + Disconnected when offline, old LBP behaviour behind NETCTL_GETSTATE_LBP_HACK=1; GetInfo answers only DEVICE/ETHER_ADDR/LINK offline, else NOT_CONNECTED; NetStartDialog Load/UnloadAsync no longer lies about connecting), sceNp.c (sceNpManagerGetOnlineId, GetAccountAge return SCE_NP_ERROR_OFFLINE using the existing PS3_NP_NPID_OFFLINE gate), cellGame.c cellGameGetSizeKB real recursive directory size. Not applied: ~85 findings in sceNpTrophy/sceNpCommerce2/sceNpBasic, cellSaveData (AutoLoad2 NODATA->OK translation and AutoSave2 delegation are deliberate working compat), cellMsgDialog (never called by NCAA14: game uses its own UI), cellSysutil validation gaps, cellUserInfo SetList/ListType NIDs. cellFontOpenFontset (audit "high": returns no font data) is not applicable: NCAA14 never calls cellFont (own renderer). Never called by NCAA14: cellSaveDataDelete, cellGameCreateGameData, cellHddGameCheck. [ps3recomp-mode-matrix.md findings 7, 11, 15, 16]
- Offline route facts: Dynasty has "What's New" tutorial gate then online-connection dialog chain; Join Online Dynasty path loops "Connection Failed"; pure New Dynasty route found in round 3 (run_d.ps1 had silently never forwarded -NewTileRight). [ps3recomp-mode-matrix.md findings 2-5, 12-14]
- Known pre-existing issues listed in matrix: on-field players not rendering (lane A Step 33 at the time, later fixed in Step 34), Recruiting Board hang "Loading recruiting data..." (open at Step 29). UNVERIFIED current status.

6.5 PC-mode validation (current build, 2026-10-16, lane E)  [pc-mode-validation.md]
- A (Dynasty): hub tabs, advance Pre-Season -> Week 1, one full game, Weeks 1-7, full season through CCG/CFP/bowls (Oregon 37, Oklahoma 31 title game), awards, carousel, players leaving, draft export prompt (answered No), draft results, transfers, six offseason stages, rollover to Pre-Season 2027 all PASS; check_pc_season.py 15/15; check_pc_dynasty.py 7/7 on 2027 save; SEYR/SSYE=1. Intermittent "Autosave in Progress" stall at ADVANCING TO TRANSFER REQUESTS (not reproduced on retry; 2 transient JOBHANG lines). Finding: School Records year shows 2013 on that build (fixed in rec26 patch, needs v26 re-lift).
- A (fresh): New Dynasty, Sacramento State, 7-year contract 2026-2032 shown, hub Pre-Season 2026.
- B (Road to Glory): create player via on-screen keyboard, HS games earn recruiting points only by playing (115 -> 290 -> 415), commit to Delaware, first college game KSU 28 Delaware 12, week advance, save/reload OK.
- C (Play Now): Houston at Liberty Super Sim 22-24, realistic scoring, PAT kicks no longer all missed (Steps 39D/39E, 52E). Liberty logo/uniform correct; live field used Toledo stand-in (stadium not built).
- Earlier statement: Edit Player crashed RPCS3 once (Vulkan assertion, not reproduced twice). [pc-mode-validation.md section 2]

6.6 Fast-drive / MCP (RPCS3 side tooling)  [fast-drive.md]
- scripts/fast_drive.py drives the isolated RPCS3 via control_isolated_rpcs3.py (imports it; every identity/PID/path recheck still applies); scripts/ncaa14_mcp_server.py exposes MCP tools over stdio registered in .mcp.json at the workspace root (tools seen in this environment: advance, advance_to, dismiss_popups, press, route, save_dynasty, screenshot, state).
- tools/fast-drive/classifier.py: GDI+ ctypes screenshot decode (~30-40 ms vs ~4 s pure-Python PNG), region-crop dHash classifier v2 (header/menu/right/bottom regions, weights header 0.10, menu 0.28, right 0.05, bottom 0.57); hub labels hub_preseason / hub_regular / hub_offseason; "changing" gate for loading via LOADING-pill template.


## Appendix D. Raw gap lists and unverified items

### D.1 Teams/recruiting/capacity

2. No exhaustive coverage: 44 compare-126 sites reviewed; whole ELF still has 107 unpatched 126, 63 125, 528 127 immediates outside reviewed functions (A138). Heap/member-embedded fixed arrays sized 126 not scanned (RCA). Numeric blanket replacement invalid (TEA).
3. Unpatched suspects: UI filters 0x1e1660 (TCRK 126), 0x1e2ca0 (STDR 126), 0x1e1018 (A138); coach vector 0x4be4f4 data-dependent; grade thresholds 0x1cfe038 top out at 126 (cosmetic) (RCA).
4. CFBR-inherited gap: CFBR 0x532614 (stock 0x5309c0) builds another 126x12 temporary and passes 126 to 0x4b7a4c; CFBR 0x1257034 `li r8,0x3f0` unreviewed; CFBR data side (roster/template, remap of 5 colliding TGIDs) not built (CPT).
5. History tables: RBKS (3402/3643, risk at 138 teams x 27 = 3726 overflow), TPHS 572/572 full, per-team draft history semantics unknown, prototype TPHS ID412 has 3 rows instead of 4; RBKS RCDT 0/1/2 semantics are hypotheses; PSRA 2449/2500; SKNW 1894/1894 (A138, FSC).
6. Schedule: generator behavior with 18 Independents and repeated seasons unproven; only SESI 0 has presets for new teams; initial prototype schedule was FCS-only (fixed later by schedule-v1) (A127, A138).
7. Coach/contract lifetime: COCH has only 3 free slots in recent stock saves; CREP/CONT/CONT960 lifetime maxima, ID/sentinel allocator limits unproven; carousel availability for new teams unproven (ATD, FSC, A138).
8. Recruiting semantics: board membership + commit status does not identify destination team; RCPR not a team ID; RECV 6300 / RCPT 4305 / RECB 4410 tables outside reserve growth flagged in CFBR map (A127, CTM). Meaning of second-array fields +0xf05/+0xf06/+0xf07/+0xf2e not documented (ATD, TEA).
9. Preference object: getter 0x50c9bc can return 0xffff for missing TGID used as index without guard; all-team vs FBS-first ordering assumption for future expanded callers; getter 0x149a8d4 owner unresolved; full alias coverage not claimed (RPC, PIT). Brand-new Dynasty initial state before recruiting init has pitch flags [1,0] and uninitialized records (not a patch fault) (PIT).
10. Player ID uniqueness: 24 duplicate PGIDs (one active + one TGID1023/PTYP3 row) occur on stock too; only active-row uniqueness is a valid assertion (PIT).
11. Rank fields: TCRK/TMRK/TBRK are u8; claims about 128+ UI/API consumers and sentinels unproved; earlier "seven-bit rank" claim unsupported (FSC, FCI).
12. Container: trailing opaque save container (~4.6-5.2 MB) uninterpreted; 4200-byte template trailer with SQL/binary semantic unresolved; save HED/SFO framing for CFBR not rebuilt (FSC, TEA, CTM).
13. The dynasty-constructor/dynasty-object analysis directories contain only the Dynasty adapter install thunk list, advance-stage dispatch entries, singleton init, and 0x1c75d54..0x1c75d74 writer windows; they do not describe TEAM/PLAY/DCHT/COCH record layouts (DC, DO). No doc here describes a PLAY row field map beyond names (PGID/PTYP/PPOS/PYEA/PHGT/PWGT/OVR) or a DCHT column map; field bit layouts for those are in the TDB schemas (not in these docs).
14. Possible ambiguities in source text: ATD/A127 phrase "TORD is recomputed27" is garbled (whitespace stripped); BRT/BPT/CIT numbers show missing spaces ("4410records") - values copied as is. Integration word counts for board v2 (291 = 87 board + ? + prior sites) stated as "87 board/291 integrated words" (BRT); breakdown beyond that UNVERIFIED.

### D.2 Schedule/calendar/stage machine

- 5.1 Exact eligibility at the prototype's allocation was never observed at runtime; "preset exhaustion" is a supported hypothesis only (SI).
- 5.2 Why first-year schedules were FCS-only for the Idaho clone is explained by missing SKNW rows (supported), but a proven fix beyond the v5 MISC trial (12 different FBS opponents) is not shown for cold-load, season and rollover (SI: "pending at this entry").
- 5.3 The meaning of the decompiler output parameters in 0x1022c8/0xff7e0 is unverified (SI warns against inferring semantics from them).
- 5.4 Table-vs-style hypothesis: which flag (r5 of 0xfcab0) makes the engine use the per-conference table rather than CSST is not decoded (R26DL s5.3). R26V4 later found the CGID/CRV1 rule for EvenDivsProtectedRivals, UnevenDivs n=13 (table SMAC through CGID 7), EvenDivsNoProtectedRivals (table of CGID 9) and AllConfOpps with table size n(n-1)/2.
- 5.5 ACC 17 and Big Ten 18: no style supports them natively. EvenDivsProtectedRivalsStyle with the MISC table path is the proposal (R26V4). Runtime acceptance flagged false at the time (R26V4, R26CR).
- 5.6 CFBR generator bodies were never re-decoded; stock decoding is mapped by address (CFBR26 open question 1).
- 5.7 In-game realignment ("Custom Conferences") is untested with zeroed SCRT and with 17/18-team conferences; style selector returns null for 17+ (R26V4, R26DL, R26CR).
- 5.8 SKNW row at SESI 7 references nonexistent TGID 190 (R26DL).
- 5.9 No "Known skips intra-conference pairs" proof; stated as medium confidence (R26CR).
- 5.10 SGID 0 on all regular-season games in a fresh save is normal; stadium assignment happens when the game is reached (SI).
- 5.11 Roles of 0x102e3c, 0x102f6c, 0xffcb4, 0x101fac, 0x4456c0 etc. are from query strings / call shape only.

Calendar/year
- 5.12 `dynasty-start-year.md` marks all sections 1-8 as superseded by s9-13; its test plan and 47-word table were static-only. Runtime verification of the full start-year patch happened in later stages (e.g. v26, dyn60pc-len60 sessions), but the 60-season long-run test (SSYE 59) result for dyn60p-len60 is not in these docs (S85 s24 is a plan, "not executed").
- 5.13 What the TDB writes for SSYE >= 64 into 6-bit SEYR fields is untraced (probably masked to 0) (S85 s7.1, s16.1).
- 5.14 TDB full-table behaviour (BCHH/CCHH/TSHS) is untraced; only the insert call ignoring the return code is proven (S85 s7.1).
- 5.15 NESG/NEUT rows exist for SEYR 0..59 and 63 only; 2086..2088 would get none under len64 (S85 s16).
- 5.16 COCT=3 meaning (final-season coach state) is untraced; CCOM lookup 0x176eb50 keys on it (S85 s4, s16).
- 5.17 Dec 1 = Sunday seasons (2030, 2041, 2047, 2052, 2058, 2069, 2075, 2080 in 2026-2085) have regular-season date labels one week early (CCG labelled Nov 30) because the 2013-only anchor at 0x4d8654 is not patched (DSY s9). Weeks themselves are consistent.
- 5.18 Playoff weeks in Fri-Sun seasons (18/20/21/22) were never run with the playoff stack; runtime item (DSY s10, s12).
- 5.19 NCG/BCS host rotation 0x459acc / 0x45a390 left unpatched (host phase only) (DSY s9).
- 5.20 Trophy Room "2014 SEC CHAMPIONSHIP" shown is an old profile trophy (UTDY 14), not a bug; existing UTDY 13 trophies keep their value (SRR s6, S85 s11.4).
- 5.21 Coach Central chart axis "2010-2019" is APT (NCAA_RELEASE_YEAR=2013 + offset); fixed by dyn60/dyn60p/dyn60pc (S85 s11.3).
- 5.22 The main-menu "SEASON" tile shows an additional large "2022 SEASON" texture; art follow-up only (S85 s11.2, MTM).
- 5.23 Save-size ceiling 8,278,016: not raised; storage class (static vs heap) of its buffer not determined (DSY s7).
- 5.24 The rationale for exactly 60 seasons (BCHH 2040/34, CCHH 600/10) is the capacity theory; the code gate is the separate 0x539aa4 predicate (S85 s15.1).
- 5.25 CFBR's Dec-5 anchor equivalent is 0x4d987c; leave-alone (DSY s9 table).

Stage machine
- 5.26 Which callback bundle is active at each game phase is unverified (SAA).
- 5.27 Stage query fields in SEAI/MOIN (MCSA, MPSA, SSTG, SNPW, SNPB, SBRW, SGOW, SERB...) are only observed, not decoded (SAA, SSP).
- 5.28 Team iteration/allocation and schedule insertion were not fully traced (SAA "Remaining proof").
- 5.29 Round advancement, final champion recording and 12-team playoff in-game acceptance are tracked in other docs (not covered here).

Other
- 5.30 Edited-save loading (start_year_seyr_edit.py) is itself a [INF] caveat (DSY s12 step 10); v2 `--mode shift` is the recommended tool (S85 s5.2).
- 5.31 mode-test-matrix: Road to Glory, Play Now, Coach/Practice/One-Button/Mascot Mash Up work; Edit Player crashed once (Vulkan assertion); Schedule-driven mode (2026 Season tile) NOT TESTED (MTM).
- 5.32 FBS alignment research: Installed-baseline reconciliation of the 13 additions has no TGID assignment in ALIGN (only the proposal); real IDs are in R26DL/CFBR26 (ALIGN).

### D.3 Rules/playoff/coach/news/UI/stats

Rules (A):
1. Rules-v2 OT retest (T1-T4, MRD 9.4) outcome not recorded in docs read; R1-A (AI hint) and pr_add/ss_score effectiveness UNVERIFIED. Sim path R1 in Dynasty week sim unverified (MRD 6.6). CPU still may kick for 0 (rule-correct) instead of choosing a 2pt play; no hook on 0xdb6da0.
2. C2 two-minute stoppage graphic/event never captured; presentation key 0x26 fires in OT2; flag 7 side effect [INF]. C3 not built. C4 sim runoff unknown. Dynasty inside-2:00 case untested. No stamina/fatigue retune for extra plays.
3. Game-state score fields not located statically (cannot poke a tie). Penalty on shootout try in sim becomes fresh try. Voided kick still logs "Extra point good"/may count PAT stats.
4. Rule values (quarter length 900.0, timeouts 3, play clocks 40/25) live in NCAA clock config built by 0x111dc28 (code, not DB); no DB table for OT/clock rules (GOPT/SOPT/MOPT checked).
Playoff (B):
5. Playoff v3/v2/U2/campus/proj1/std1 all "not runtime tested" at doc time in these docs; later docs (continuation-checkpoint) may record results -- UNVERIFIED here. U failed (R26PU1); U2 job-entry assumption open.
6. UI with partial/TBD rows; one-bowl-per-team assumptions in 0x4aae90/bowl-week flow; first-match residuals (trophy 0x466890.., news text, PLAC 0x44fbf0/0x44ff78); BOWL SWPE/BMFD/BPLO/UTID semantics; BOWL cannot grow beyond 45 rows; calendar beyond 2018 assumed; stock bowls cannot be user-simmed in U2 mode.
7. Cave full (509/509): no room for proj1b, A2 enhancements; need new region with own proof.
8. SEEDING 1 (2024-25) no longer fits cave from v2 on. Bowl choice (2026 rules) and automatic site assignment are approximations. Playoff Central UI and true bracket screen not built (no APT writer).
9. Rankings: TBRK frozen in bowl weeks only [INF] (E4 unrun); other 0x4ca8a0 callers unknown; 126 literal at 0x4cea2c (activeN->138); CFBR ranking execution trace never obtained (breakpoints ineffective under LLVM).
Coaches/News/UI/Stats (C-E):
10. Coach contract cap + guard: T2 loaded wrong save; no valid runtime pass recorded here. Whether edited saves load unknown. Hire-throttle residual. Zombie-row write path untraced. Latent overruns at 0x4fae3c/0x4fc70c noted.
11. News fix margin thresholds arbitrary; tail execution under LLVM was [INF] (later news1 runs clean per PCS A.1); multi-bowl "-Q" name residual.
12. UI: other 126-capped lists (0x1a2e3c, 0x1e1018, 0x1e1660, 0x1de9b4.., 0x1e2ca0, 0x1e4cfc) unpatched.
13. Stadiums: capacities from memory; SUID thumbnails stale; HS donor crowd files missing; Select Stadium unverified at runtime; stadium creation path in Dynasty unproven (0x17ebc8 is TeamBuilder path).
14. Sim stats: home-win gap 54.6% vs 63.4%; GOPT/MOPT/UOPT/COCH undecoded; no difficulty table; TSSE-only fields unconfirmed; receiving fields ambiguous.
15. Stat/coach table names to look up in game DB by tag: CONT, COCH, STTM, TEAM, CONF, BOWL, SCHD, SEAI, GINF, BCHH, CCHH, CAPT, HEAD, MCOV, STAD, TSSE, BTES, BOFF, PSOF, TSHS, SCWE, GOPT, SOPT, MOPT, UOPT, STGE, DYNI, LEAG, DIVI (sources: PEM, CCR, CRN, SSR).

### D.4 Patch pass (D)

- Exact CFBR addresses of user-play U2 call sites (quoted addresses 0x1fba88/0x1fbab0/0x1fbabc/0x1fbac8 are stock, from user_play_u2.c). UNVERIFIED for CFBR.
- Stock-tail numbers (0x1bbf100..0x1bc0000) vs ELF segment sizes quoted in two docs differ in how they are expressed; use code-room-and-news-fix.md for authority.
- scripts for dynasty length and record date builders: names taken from manifests (build_cfbr_dynasty_length_v1.py, build_cfbr_record_date_2026.py); I did not confirm the files exist.
- docs/v26-integrated-acceptance-2026-10-26.md, record-book-year-2026.md, modern-rules-design.md, playoff-*.md, start-year-*.md were referenced but not read (only cited as sources).
- diagnostic-marker.yml content not read.
- BPLO binding (bowl-card badge) unresolved per team-art-plan 17.x.
- Whether every stage in STAGES beyond those named in installer headers (e.g. real2026-full-art2-del-ksu-nodome) is still maintained: UNVERIFIED.
- manifests show runtime_tested false even for stages later runtime-verified (v25, v26): flags were not updated.

