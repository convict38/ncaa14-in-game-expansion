# Design sketch: mod-hook interface for the PC port

Part of the [modding knowledge base](README.md). Our own analysis of NCAA Football 14 (PS3, BLUS31159) and the CFB Revamped v21 base: names, addresses, table layouts and how our mods are built. Source tags in brackets (for example TEA, CFBR) refer to private working notes that are not published; treat each statement as a compiled finding, not a re-verified fact. No game files, extracted assets or decompiled code are included.

## 6. Design sketch: a mod-hook interface for the PC port

**Design only. No PC-port code was edited or built.** Observations about the port below come from reading generated sources and docs read-only: `ps3recomp\src\recomp\ppu_recomp_011.cpp` (excerpt around `func_01BC2700`), `modbuild/*.py`, `HANDOFF_NEXT.md`, `pc-modded-build.md`.

### 6.1 What exists today (facts the design builds on)

- The lifter turns every PPU function into a C++ function `void func_XXXXXXXX(ppu_context* ctx)`; arguments and results travel in `ctx->gpr[3..10]`, `ctx->lr` is set by the caller (`ctx->lr = 0x01BC2790; func_01BC2810(ctx); DRAIN_TRAMPOLINE(ctx);`), guest memory is read and written with `vm_read8/32/64`, `vm_write64`, and indirect calls (`bctrl`, vtable/OPD calls) go through `ps3_indirect_call(ctx)`, implemented in the game project. Each lifted function spills and restores callee-saved registers itself. (`ppu_recomp_011.cpp`, `ppu_recomp.h`)
- Guest addresses are the ELF addresses used throughout this document (CFBR space). The PC build executes the very same code RPCS3 runs (`build_modded_elf.py` docstring).
- Patches are applied offline as `be32` words and a code cave must fit the segment-0 tail; the lifter is rerun on the whole modded ELF (`pc-modded-build.md`).
- Mods already exist as freestanding C that talks to the game through `cave.h` macros (`GAME_U32`, `GAME_STR`, `EA_QUERY`, `CAVE_ENTRY`) and `--defsym` names, e.g. `modern_rules_v2.c` with hooks `modern_ot_setup`, `fd_gate`, `ss_fd_clock`, `ss_ot_start`, `ss_apply`, `pr_add`, `ss_score`, `ss_scored`. (3.1 inventory, `tools/ppc-cave/caves/*.c`)

### 6.2 Goals and non-goals

Goals: (1) a mod is one or more plain `.c` files, no PPC assembly and no hand-computed branch words; (2) a mod can run code **before**, **after**, or **instead of** any named guest function; (3) adding or changing a mod does not require re-lifting the 612 MB of generated C++; (4) the same mod source keeps working for the RPCS3 build where practical; (5) conflicts and address drift are detected at build or load time.

Non-goals: runtime patching of arbitrary instructions in the middle of a function (phase 2), a scripting language, hot reload while a game runs, SPU hooks.

### 6.3 Mod source format

A mod is a directory `mods/<name>/` with `mod.json` (name, version, `elf_sha256` it targets, list of required symbols) and one or more `.c` files compiled as ordinary host C (clang-cl, same toolchain as the game). The header `mod_api.h` provides:

```c
#include "mod_api.h"          /* ppu_context, vm_* accessors, symbol table, hook macros */

/* run after the game's own function; read what it returned */
MOD_HOOK_AFTER(ss_score, ctx) {            /* name resolved via symbols.tsv */
    if (ARG(ctx, 3) == 0) { ... }
}

/* replace entirely; may call the original */
MOD_HOOK_REPLACE(pr_add, ctx, orig) {
    u32 pts = ARG(ctx, 4);
    SET_ARG(ctx, 4, pts + 1);
    CALL_ORIG(orig, ctx);                  /* optional */
    SET_RET(ctx, RET(ctx));                /* gpr[3] */
}

/* before: may veto the original */
MOD_HOOK_BEFORE(ss_apply, ctx) { return HOOK_CONTINUE; }   /* or HOOK_SKIP_ORIGINAL */

MOD_INIT() { mod_log("rules loaded"); }
```

Pieces:
- **Symbol table** `symbols.tsv`: `name <TAB> cfbr_addr <TAB> stock_addr <TAB> first-8-words-hash <TAB> source note`. It is generated from the function tables in section 2 and is the one place addresses live. Hooks refer to names, never to raw numbers (a raw `HOOK_AT(0x47a14c, ...)` form is allowed but flagged).
- **Accessors** wrap the existing runtime: `GAME_U32(addr)` becomes `vm_read32(addr)`, `GAME_STR` a guest pointer constant, `EA_QUERY(...)` a call to the guest helper via `call_guest(sym("ea_sql"), args...)`. This lets today's `cave.h` mods compile unchanged for the PC target through a compatibility `cave.h` shim (`CAVE_ENTRY` becomes a hook registration).
- **State.** A mod may keep host-side state, but anything that must survive save/load has to live in guest memory or a DB table, because the PC port saves through the game's own `cellSaveData` path. State also has to be restorable after a load (hooks can re-derive it in `MOD_ON_LOAD`). **UNVERIFIED:** whether the guest save format tolerates extra table capacity for mod data (see 1.A, TDB capacity rules).

### 6.4 How hooks reach the game: lifter-emitted wrappers

A per-function runtime patch is impossible for direct calls, because direct calls are compiled into the C++ as static calls (`func_01BC2810(ctx)`). Only the lifter can intercept them. Therefore:

1. **`hookable.list`**: a text file of guest function entry addresses (CFBR space) that the lifter wraps. It is seeded from the "named functions" tables in section 2 (several hundred entries, not 104,000) and is extended by the mod scanner (6.5) when a mod asks for an unlisted function.
2. For each listed address `X`, the lifter renames the real body to `func_X__orig` and emits a thin wrapper under the original name:

```c
void func_X(ppu_context* ctx) {
    hook_slot* h = &g_hooks[HOOK_INDEX_X];          /* static table, NULL fields by default */
    if (__builtin_expect(h->any == 0, 1)) { func_X__orig(ctx); return; }
    if (h->before && h->before(ctx) == HOOK_SKIP_ORIGINAL) { /* fallthrough to after */ }
    else if (h->replace) h->replace(ctx, func_X__orig);
    else func_X__orig(ctx);
    if (h->after) h->after(ctx);
}
```

All callers, including tail-entry wrappers, see the wrapper, so direct calls, `b` tail jumps and indirect calls through OPD descriptors (resolved by `ps3_indirect_call` to the same symbol) are all covered. Unhooked listed functions cost one predictable branch. Functions not in the list cost nothing.
3. Re-lifting is needed only when `hookable.list` grows (infrequent, done in batches). Day-to-day iteration is: edit mod `.c`, compile it to a static library/object, relink (`build_game_e.bat` class build, seconds).
4. Ordering: several mods may register on one slot. `before` and `after` hooks form chains ordered by `mod.json` priority then name; only one `replace` per function is allowed unless the mod declares it chains through `orig` (conflict is a build error). `after` hooks run in reverse order of `before`.
5. Argument/return convention in `mod_api.h`: `ARG(ctx,n)` reads `gpr[n]` (n = 3..10), `FARG` reads `fpr`, `RET`/`SET_RET` use `gpr[3]`. Hooks must not change `gpr[1]` (stack), `gpr[2]` (TOC) or callee-saved registers except through `CALL_ORIG`. Calling a game function from a hook uses `call_guest(addr_or_sym, a0..a7)`, which saves/restores ctx fields and sets `lr`.

### 6.5 Build integration

- A small scanner (`mods/scan_hooks.py`) reads all enabled mods, extracts `MOD_HOOK_*` names, resolves them through `symbols.tsv`, and writes `hooks.manifest` (hook index to address, kind) plus the delta to `hookable.list`. If the delta is non-empty it reports that a re-lift is needed.
- Load-time checks: for every hooked function, the runtime compares the first N words of the guest ELF image to the `first-8-words-hash` in the manifest and aborts with a clear message on mismatch (same spirit as the manifest preimage checks in `build_modded_elf.py`).
- `mods.ini` lists enabled mods and order, so users can toggle a mod without rebuilding.
- The existing `be32` path (`build_modded_elf.py`) continues to supply data-segment/word patches. Hook-based mods deliberately do not use the code cave; they lift the game as is.

### 6.6 Hooks the existing mods map to (migration checklist)

| Existing cave | Hook form on the PC port |
|---|---|
| `cfp_news_fix.c` (caption/headline picker `0x47a14c` CFBR, EASP writer `0x4aa59c`; exact patched site words are in 3.4, not re-checked here) | `MOD_HOOK_AFTER(news_pick)` or `REPLACE` |
| `modern_rules_v2.c`: `pr_add` (pointsrules vtable slot `0x4c`), `ss_score` (`bl 0xa7196c`), `ss_scored` | `REPLACE` / `AFTER` hooks on names in symbols.tsv; vtable-slot patches become direct function hooks because the slot resolves to the wrapper |
| `modern_ot.c` (OTR slot `0x3c` repoint) | `REPLACE` of `ot_setup_orig 0x111e480` |
| `user_play_u2.c` (cave functions `u2_cursor`, `u2_single`, `u2_stop`, `u2_target`; calls game functions `sim_cursor` and `sim_single`, reads global `stop_count`) | `BEFORE`/`REPLACE` hooks on `sim_cursor` and `sim_single`; `stop_count` stays a data read (CFBR addresses **UNVERIFIED**; the quoted addresses `0x49ee64`, `0x49ec48`, `0x537db8` are stock) |
| Playoff caves in the BCS-filler area (hand-assembled) | `REPLACE` hooks on the picker / `bowl_site` functions listed in 2.C |

### 6.7 Open questions and risks

- **Mid-function and non-entry sites.** Many existing patches change a literal (`li r6,0x7e`) inside a function. These stay `be32` patches in phase 1. Phase 2 would add `HOOK_SITE` support: the lifter emits a call at a given instruction address and needs a label/liveness analysis, which does not exist yet.
- **Tail-entry wrappers and falling-through code.** The lifter emits 14,000+ tail-entry wrappers; interaction with wrappers at hooked entries needs testing. **UNVERIFIED.**
- **Name/ABI uncertainty.** Many names in the notes are inferred, not original symbols (digest A note). Hooks on wrongly bounded functions (nearest-prologue guesses) would misbehave; `symbols.tsv` needs a confidence column.
- **Threading.** Guest PPU threads run as host threads; hooks must be reentrant, and mod state needs locking. The PPU call stack is the guest stack (`gpr[1]`), so hooks that call back into the guest consume guest stack. **UNVERIFIED:** that no PPU function is reentered from SPU/RSX callbacks.
- **Performance.** At roughly 22 to 24 fps in heavy gameplay, the port is CPU-bound on the RSX thread, not the PPU (`HANDOFF_NEXT.md`); a handful of wrapper branches are noise, but a hook on a per-play inner loop function would be measurable. Wrap only entries that are not per-tick.
- **Dual-target parity.** Re-using the same `.c` for RPCS3 would need an RPCS3 backend that turns `REPLACE`/`BEFORE`/`AFTER` into a cave entry stub and `be32` branch rewrites at the function entry (and LR rewriting for `AFTER`). It is feasible with the existing cave toolchain but is an additional project.
- **Coordination.** The lane is actively developed by another agent. This design should be agreed with that owner, including who owns `ppu_lifter.py` changes and the `hookable.list` format, before anyone edits code there.

