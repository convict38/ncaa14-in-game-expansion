# CFBR address map and symbol table

Status: first pass done (item 1 of the mapping plan). Names are ours, not EA symbols.

## Files
- `analysis/symbols/stock_symbols.csv` - 180 curated stock (1.00) names: address, name, system, confidence, source tag, note. Source: sections 2.A to 2.C of MODDING_REFERENCE (`analysis/symbols/stock_names_src.psv` is the editable source).
- `analysis/symbols/cfbr_symbols.csv` - 214 CFBR names: `cfbr_addr, name, system, confidence, match, stock_addr, anchor_votes, body_vs_stock, source`.
- `analysis/symbols/function_map_stock_to_cfbr.csv` - machine map of every stock function entry (size >= 32 B) that has a CFBR counterpart: 24,236 mapped of 29,461 candidates; 21,506 have a normalized-equal body (`eq`), 2,730 differ (`diff`). Use it to port any future stock name.
- `analysis/symbols/cfbr_direct_names.psv` - names found directly in CFBR (34).
- Scripts (all read-only): `scripts/map_names_to_cfbr.py`, `scripts/map_all_functions_to_cfbr.py`, `scripts/append_direct_names.py`, `scripts/string_owners.py`, `scripts/query_owners.py`, `scripts/string_xrefs.py`. They reuse `scripts/cfbr_port_lib.py` (anchor-window mapper from `docs/cfbr-port.md`).

## Method and confidence rules
1. Mapper: normalized 8-word windows unique in both ELFs vote a delta for the stock address; the CFBR address must hold a normalized-equal word.
2. `match=exact`: the CFBR address is a Ghidra function entry and the whole body is normalized-equal to the stock body. Confidence is kept (confirmed stays confirmed). 138 names.
3. `match=entry`: lands on a function entry but the body differs (changed logic or layout). Confidence capped at likely. 19 names.
4. `match=inside`: the stock address was a mid-function site, not an entry, so the mapped address is that site's equivalent. Confidence guess. 22 names. The `body_vs_stock` column shows the owning CFBR function (`owner=0x...`); use that owner as the function.
5. `match=none`: no anchor (AptCallbackMemAlloc 0x708260). No CFBR address is invented; the cell is empty.
6. `match=cfbr-direct`: found in CFBR with a string xref plus decompile. See recruiting.md.
- Cross-check: known pairs from MODDING_REFERENCE 2.6 reproduce: 0x45b484 -> 0x45c3fc, 0xa67320 -> 0xa691b0, 0x461d74 -> 0x4630fc style selector.
- Conflict noted: stock "recruitman_first_array_init" 0x4b8db4 mapped to 0x4ba384, but string evidence shows 0x4ba384 is the `Progressing Recruits` function. The stock label was a mid-function site; both rows are kept, the stock-derived one is downgraded to guess.
- The stock Ghidra project splits functions at save-helper calls (an entry such as 0x4ff570 is only 8 bytes), so for new work use the CFBR project, where helpers were repaired.

## How to name a new function
1. Find its stock name/site in a note. 2. Look the stock entry up in `function_map_stock_to_cfbr.csv`. 3. If the row is `eq`, copy the name with the same confidence; if `diff`, cap at likely. 4. Add to `stock_names_src.psv` or `cfbr_direct_names.psv` and rerun the two scripts.
