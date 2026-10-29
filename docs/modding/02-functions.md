# Named functions

Part of the [modding knowledge base](README.md). Our own analysis of NCAA Football 14 (PS3, BLUS31159) and the CFB Revamped v21 base: names, addresses, table layouts and how our mods are built. Source tags in brackets (for example TEA, CFBR) refer to private working notes that are not published; treat each statement as a compiled finding, not a re-verified fact. No game files, extracted assets or decompiled code are included.

## 2. Named functions by system

Names are mostly ours or inferred by the note authors, not original EA symbols. Inputs and outputs are as stated by the sources; PPC ABI is r3..r10 arguments, r3 result.

### 2.A Teams, recruiting, capacity (STOCK)

| Address | Name/role | What it does | In/Out | Mods touching | Source |
|---|---|---|---|---|---|
| 0x472d78 | league index initializer | queries TEAM counts; allocs 12 B/entry + spares; sets index/count globals 0x1c76898/0x1c768a0 (all), 0x1c7689c/0x1c768a2 (FBS) | - | none directly; consumers patched via counts | TEA |
| 0x472910 | league index fill | TGID<=1006, optional TVIS=1, sort TORD asc; 2nd list needs TTYP=0 | fills lists | none | TEA |
| 0x4d3fb8 | team-expectations init (TEXP) | stops after 126 entries; stop at 0x4d4140 | - | activeN count words | TEA |
| 0x4b57c4 | recruiting-class evaluation | stack array 7 B/team; limit 126 at 0x4b5abc; raw vector scratch use at 0x4b5a58..60 (0x430 offset) | - | scratch-reserve (frame 0x490->0x580) | TEA, SRT |
| 0x47af94 | loop of 126 FBS entries issuing TEAM-field update | - | - | audited only | TEA |
| 0x48dec4 | 126-FBS PLAY update loop; ID bounds TGID*70..TGID*70+70 | - | - | audited | TEA |
| 0x49b068 | "Setting Team Depth Charts" - rebuild DCHT for 126 teams | - | - | audited | TEA |
| 0x4d3d20, 0x4d4540, 0x4d514c, 0x4f7580 | loops over exactly 126 team-index entries | roles unproven | - | audit | TEA |
| 0x4facb8 | team sort / Coach Stability step | clamp FBS count to 126; 20-B scratch records; sort/update | - | scratch-reserve (frame a90->d40, cap 126->160 records), activeN | TEA, SRT, RCA |
| 0x4ecad0 | ranking record fill (object+0x10..+0x7f0, 16 B x126) | dynamic FBS count loop with no capacity check | from owner 0x1b41cc | scratch-reserve | TEA |
| 0x1b41cc | ranking buffer owner | frame 0x8c0 -> 0xae0, passes SP+0x90 | - | scratch-reserve | TEA, RL |
| 0x4b8db4 | clears 0x3f0 B at object+0xb08, fills 126 | first-array init | - | recruiting-relocation (160/0x500) | TEA, RFA |
| 0x4b8cd8 | first-array fill loop (limit 126 at 0x4b8da0) | - | - | not changed count | RFA |
| 0x5068d4 | gates FBS-index lookup at 126; stride 0x178 at obj+0xf05 | - | - | audit | TEA |
| 0x4b919c | leaf getter: byte +0xf05 of team record (via FBS index, bound idx<126 at 0x4b91f8) | read | team TGID -> byte | relocation (+0x110) | TEA, ATD |
| 0x507e94 | leaf incrementer of same byte (bound 0x507ee4) | increment | TGID | relocation | TEA, ATD |
| 0x4b7970 | loops 126 teams touching +0xf05/+0xf07 (index truncated to 8 bits) | - | - | relocation | TEA |
| 0x4be638 | initializes +0xf06 and +0xf2e fields (126-team loop) | - | - | relocation | TEA |
| 0x35e998 | RecruitMan + RecruitPrefMan init (allocs 0xc81c and 0x31b8) | allocation | - | relocation (alloc 0xfb1c); pref (0x3f00) | SRT, RPC |
| 0x35eaac / 0x35eacc | RecruitMan alloc size instr / call | - | - | patched | RL |
| 0x35ebc0 | `li r3,0x31b8` before 0x50c954 | pref alloc | - | preference-object plan | RPC |
| 0x5067a4 | RecruitMan constructor (STDU first, MFLR 0x5067a8) | inits vtable 0x18a8190, 126 first recs, clears second array, 12-B tail | - | relocation/reserve | SRT, RL |
| 0x5066cc | facade setter slot 0x48 | stores RecruitMan | - | - | SRT |
| 0x360d88 | facade constructor (vtable 0x18a8118; global 0x1c78cfc) | - | - | - | SRT |
| 0x1470ab8 | facade getter (slot 0x14) -> global 0x1c78d0c | - | returns RecruitMan | - | SRT |
| 0x494c48 | RecruitMan reset; 0x494c6c stores 0x3ff at +0xf00 (-> +0x1010 in relocation, word 907f1010) | callers 0x4ff634 (in 0x4ff570), 0x495fc8 (in 0x495ebc); 0x4ff754 and 0x503b74 get RecruitMan from facade +0x14 | - | relocation | RFA |
| 0x4ff570 | manager dispatch called from 0x4ff754/0x503b74 | calls 0x494c48 at 0x4ff634 | - | - | RFA, RPC |
| 0x4ff714 -> 0x4fea60 | preference path via facade +0x18; extra 126x8 temp | calls 0x4fdf58 | - | preference-object / integration | RPC |
| 0x50a80c | reads halfword base+index*8+0xb0a | - | - | unchanged offset | RFA |
| 0x50be80 | 8 B/team temp array owner | alloc 0x50bf1c, caps 0x3f0, logical end 0x50bf90 | - | integration (160 cap, 8N logical end) | RPC, A138 |
| 0x4b47c8 | RecruitPref init: three 126 x 28 B node pools, 126-word array | frame 0x2e50 -> 0x3a20 | - | preference-stack plan (79 words) | RPC, CIT |
| 0x4b47e8 | pref reset: clears 0x2f4 words to -2000 | uses 0x69ac70 | - | preference-object plan | RPC |
| 0x50c954 | RecruitPrefMan ctor (vtable 0x18a8200) | - | - | plan | RPC |
| 0x50c99c | ctor sub: clears 0x2f4 words | - | - | plan | RPC |
| 0x4b3838 / 0x3844 | pref cache setter / guard | team idx guard 126 | - | not widened | RPC, ATD |
| 0x4b3890 | pref cache getter | 126 guard | - | not widened | RPC |
| 0x50c9bc | virtual getter, 76-B record (+0xbdc) | returns 0xffff for missing TGID | TGID -> record | pref plan; CFBR +0x0c = 0x50e378 | RPC, CPT |
| 0x50ca8c, 0x50e19c, 0x50cad0 | tail/flag consumers | - | - | plan | RPC |
| 0x4b4190 | pref dispatcher across play styles using cache get/set | - | - | - | RPC |
| 0x4b464c | decompiles to zero (missing DB output arg); raw instrs authoritative | - | - | - | RPC |
| 0x4b44ac, 0x4b2f6c | use all-team list but stop at 126 | - | - | - | RPC |
| 0x4b1510 | serialize 14 per-team pitch bytes into PTIP | uses base+0xbdc / 0x4c stride | - | plan | RPC |
| 0x4b1ae0 / 0x4b1938 | clear FBS_count*0x4c at +0xbdc with TGID sentinel 0x3ff / per-team init | - | - | plan | RPC |
| 0x4bf8ac | uses all-team dense index with +0xbdc 76-B shape | caller provenance unclear | - | plan | RPC |
| 0x4f599c | retrieves RecruitPrefMan | calls 0x4c6308, 0x4b1ae0, 0x4b1510 | - | - | RPC |
| 0x4f4ca0 / 0x4f52a8 / 0x50fae8 | reset first pitch record TGID sentinel (+0xbdc) | - | - | plan (34 local sites) | RPC |
| 0x50dedc / 0x50df44 | clear flag +0x3148 / 76-B array access via all-team index | - | - | plan | RPC |
| 0x47be80 | pref destructor frees +4/+8 | - | - | plan | RPC |
| 0x4ad7c0 / 0x4ad500 | RecruitingBoard allocator / ctor | - | - | board patches | BRT |
| 0x4ad13c | RECB query | - | - | - | BRT |
| 0x4ab2ac | board destruction / refcount | - | - | - | BRT |
| 0x4acd20 (incl. 0x4acd78) | board per-team list walker (first-array lookup, 126 bound) | - | - | unaffected | BRT, ATD |
| 0x4bf02c | board list traversal (was missed in v1; fixed 0x4bf064/6c/70/114/11c) | - | - | board v2 | BRT |
| 0x4aac1c, 0x4a9fe0, 0x4aa374, 0x4aae90, 0x4c69b4 | scheduling/list object users | - | - | leads | ATP |
| 0x4c5910 | board stack scratch (38 tail pairs w/ high halves) | - | - | board-pool (406 words) | BPT |
| 0x14085d4 | allocator (null at exhaustion) preserves r7 high half | - | - | - | BPT |
| 0x146755c | specialized board ctor (caller 0x4ad704) | - | - | - | BPT |
| 0x1469284 | temp record ctor copying 8 sentinel bytes | - | - | - | CIT |
| 0x691520 | node-pool allocator; rounds buffer down to 28-B nodes | - | - | - | CIT, SRT |
| 0x13e6cec | copy helper (wrongly marked noreturn; blr at 0x13e6d50) | - | - | tooling | ATP |
| 0x4a9078 | MCOV story builder (stack 0x4900, 126x0x90) | - | - | extra-team-scratch (5 words) | ATP |
| 0x4a8918 | story insert (<=8/team; query 1776a50) | - | - | - | ATP |
| 0x4a141c | scratch 126x20 + flags | - | - | extra-team-scratch (14 words) | ATP |
| 0x4b2b58 | uses 126 in rank weighting and loop count | - | - | activeN | ATD |
| 0x4feb00 / 0x4b671c / 0x50bf90 | logical end pointers (1008 -> 8N) | - | - | activeN | A138 |
| 0x4c9030/0x4c9034 | float data 1/126 -> 1/N used by 0x4c9038 (lvlx) rank normalize (N=138: 0x3bed7304) | - | - | activeN | A138 |
| 0x47fe20, 0x4a1470, 0x4feaf0, 0x5067d0, 0x50bf7c | 126->160 storage clears/sentinel ctor | - | - | activeN | A138 |
| 0x4b2e7c | Championship Contender rating step (`cmpwi 138` fixed in v6) | - | - | activeN | RCA |
| 0x4b4dc0 | Play Time rating step (no 126 state) | - | - | - | RCA |
| 0x4b1c48 | Conference Prestige step (no team array) | - | - | - | RCA |
| 0x4b1f3c | TV Exposure step; stack vector 126x20 (CRASH at N>=128) | - | - | active138 v2 hardening (4 words) | RCA |
| 0x4fc830 | Pro Potential step (also from 0x4fca4c) | - | - | v2 (4 words) | RCA |
| 0x4f85bc | Program Tradition step (also from 0x4f9260) | - | - | v2 (4 words) | RCA |
| 0x4be4f4 | coach-skill vector (from 0x503e3c, 0x4c6bbc) | - | - | v2 (7 words) | RCA |
| 0x503700 | Rating driver ("Rating Teams - %s" at 0x176fddc; callsite of TV Exposure 0x503958; snprintf 0x5039c0) | - | - | - | RCA |
| 0x503b74 | contains caller 0x503c3c of 0x503700 | - | - | - | RCA |
| 0x698e3c / 0x698da0 / 0x6982c8 | snprintf / vsnprintf / worker | fault site | - | - | RCA |
| 0x14683a4 | qsort | - | - | - | RCA |
| 0x50ddb0 / 0x44b25c | fill grade thresholds at 0x1cfe038 (11 cumulative rank cut-offs) | - | - | not patched | RCA |
| 0x47e954 | TEAM/STAD query result list allocation (126x44+8; alloc instr 0x47e9ec -> 160*44+8) | - | - | active127 v3 | A127 |
| 0x4d36ac / 0x4d386c | coach contract ensure/generate | see 1.3 | - | none | ATD |
| 0x4d2b50, 0x4d5690, 0x4d68f8, 0x46104c, 0x471f00, 0x4f7ea8 | CONT/CREP writer paths | - | - | none | ATD |
| 0x1e1660, 0x1e2ca0, 0x1e1018 | UI filters with literal 126 (TCRK filter; STDR stadium rank filter) | unpatched leads | - | none | A138 |
| 0x479f08, 0x4a27d0, 0x4a2acc, 0x4a4570, 0x4a9560, 0x4a96b0 | 127-node query-expression pools | - | - | none | A138 |
| 0x477fd0 | compares ASCII '~' (0x7e = 126); EXCLUDE | - | - | none | ATD |
| 0x4a4bdc, 0x4a1438, 0x4a50a0, 0x4b2c64, 0x4b2de4, 0x4b8e24, 0x4facdc | other noncomparison 126 immediates (4a1438 = logical init count; 4a1470 = 160-byte clear, do not shrink) | - | - | review | ATD |
| 0x4be638 | see above | | | | TEA |
| 0x4d2b50... | (see above) | | | | |
| 0xf2d79c etc. | graphics RNADevice paths | excluded | | | RFA |


### 2.B Schedule, conferences, stage machine, calendar (STOCK, CFBR pairs given where the notes have them)

Addresses are stock unless stated. "Mods" lists patches that touch the function.

#### 2.1 Schedule generator (region 0xfe000..0x103500, outside the earlier 0x460000..0x510000 count audit) (SI)
| Address | Name/role | What it does | In/out | Mods | Source |
|---|---|---|---|---|---|
| 0x103064 | ScheduleGenerator driver (_opd_FUN_00103064) | Sets this+4 = season (param_2). Runs in order via vtable slots: ConferenceGenerator (slot +0xc, string 0x188dff8), UserVsUserGenerator (+0x14, 0x188e098), PreferenceGenerator (+0x10, 0x188e068), AnnualGenerator (+0x18, 0x188dfd0), KnownGenerator (+0x1c, 0x188e040), RemainingGenerator (+0x20, 0x188e0c8). Progress labels 0x16f3ee8 "Conference Games", 0x16f3f10 "Annual Games", 0x16f3f38 "Remaining Games". Then 0x102f6c, 0x102e3c, and query 0x16f3ec4 `update DYND set ATSG = ?` (sets GSTA) | param_1 = generator object, param_2 = season, param_3 | none directly | SEL 103064.c, SI |
| 0x102850 | RemainingGenerator main (FUN_00102850) | Creates SEWN-index (query 0x16f3c18). Fetches team list with query 0x16f3c48 (`TOID from TEAM where TTYP=0`), allocates a 12-byte-per-team array (count*0xc+0x10). Per team stores 0x3ff and a 15-bit availability mask (query 0x16f31d8 counts games per week 0..14; bit 0x4000 added if 0x459848 returns nonzero). If season > 0, calls 0x1026ec to add random FCS games. Then loops teams with the stop-at-12 rule (`0xb < count` where count from query 0x16f387c): while < 12 games calls 0x102504. Progress string 0x16f3cf8 "Remaining Games %d%" (final 0x16f3d28). Ends with 0x101d94 and index teardown | this+4 = season, this+8 = allocator, param_2 | activeN patches (count constants 0x4cea2c etc. are elsewhere), active127 schedule v1 data | SEL 102850.c, SI, QSTR |
| 0x102504 | per-team remaining-game filler | Calls 0x1023ac to pick an opponent, calls 0x10210c to pick a free shared week (retries up to 5/0xb times), on failure falls back to 0x101fac (FCS fill) then 0x10210c with 0. Inserts via 0xffcb4 | (generator, team array, count, team idx, ctx) | none | SEL 102504.c, SI |
| 0x1023ac | opponent scan | Scans candidate teams from a randomized start (0x4456c0 random(0..n)); for each calls eligibility 0x1022c8 and week finder 0x10210c; returns first opponent index with a shared free week | (gen, array, team idx, count) -> opponent index | none | SEL 1023ac.c, SI |
| 0x1022c8 | opponent eligibility | Requires 0xff7e0 true (both teams under cap), a bitset helper (func_0x000fba48), 0x459814 == 0 (not blocked), and duplicate-match query 0x16f3810 count < 1. Returns 1 if eligible | (gen, TGID a, mask a, TGID b, mask b) | none | SEL 1022c8.c, SI |
| 0x10210c | shared-week finder | Intersects two 15-bit week masks with an allowed-week mask; uses week order table at 0x16ed8e0 (15 entries) and prefers weeks adjacent to occupied weeks; returns week 0..14 or 0xff | (gen, mask a ptr, mask b ptr) -> week/0xff | none | SEL 10210c.c, SI |
| 0x1026ec | random-FCS filler (season > 0 branch) | Adds FCS games for teams with fewer than 0xc games, using week table at 0x16ed66c (4 entries), loop bound `0x23 + random(0x10)` and 100 attempts, via 0x101fac. Not an FBS enable switch | (gen, array, count, ctx) | none | SEL 1026ec.c, SI |
| 0x101fac | FCS opponent pick | Called with 0x3ff; chooses a generic FCS team | n/a | none | SEL 102504/1026ec; SI mentions "falls back via101fac to FCS" |
| 0x100200 | KnownGenerator body (FUN_00100200) | Stores output table at this+4, calls 0xff998(this, 0x574e4b53 'SKNW' logical tag, season), then runs query 0x16f36ec (`update ... 0x28`) | (this, param_2, season) | active127-v5 (MISC preset change), real2026 (MISC) | SEL 100200.c, SI |
| 0xff998 | preset inserter | Runs query 0x16f38c8 (week/home/away/date/time from SCHE selected table where SESI=season); for each row calls 0xff7e0 (feasibility) and 0xff56c (week choice), then inserts into DYND via query 0x16f3720 | (this ...) | none | SEL ff998.c, SI |
| 0xff7e0 | team-pair feasibility | Both TGIDs distinct; calls 0x459938 per team; counts games (0x16f387c / 0x16f3810) and 0x459814(0x1f,0x1f) | | none | SEL ff7e0.c |
| 0xffcb4 | schedule row insert | Insert of a game (week, team, opponent, venue) used by 0x102504/0x1026ec | | none | SEL 102504.c (call site); role UNVERIFIED in detail |
| 0xfe744 | KnownGenerator factory registration | Registers factory vtable 0x188e6e8; virtual +8 -> OPD 0x1bc6f70 -> 0x14275a0; raw body allocates 12 bytes and installs vtable 0x188e030; virtual +8 resolves via 0x1bc6c78 to 0x100200 | | none | SI |
| 0x14275a0 | KnownGenerator ctor path | Ghidra stops at an unmodeled save helper; chain proven from raw instructions | | none | SI |
| 0xffeec | ConferenceGenerator | Loops CGID starting at season mod 14; `use DYND select STNA from CSST where CGID=?` (0x16f39a0); empty STNA skipped; creates style by name through the factory finder 0xfab40; calls slot 2 generate(ctx, cgid, season) | | none | R26V4 A.1, R26DL |
| 0xfc9c4 | CGID -> MISC table map | CGID 0 SACC, 1 SBTN, 2 SBTW, 3 SBEA, 4 SCUS, 7 SMAC, 9 SMWS, 10 SPTN, 11 SSEC, 13 SSUN | | none | R26DL |
| 0xfcab0 / 0xfddfc | table path (base method) | Reads `select max(SESI)`, loads season slice; maps each row's GHTG/GATG through conference X's key list onto this conference's members. No cap bound check | | none | R26V4 A.1 |
| 0xfdcc0 / 0xfdbdc | conference member list | SCRT first, TEAM-by-TORD fallback if any slot is 0 | | real2026 data zeroes SCRT | R26CR, R26V4 |
| 0xfbd8c | base generate slot 7 | n = count(TEAM where CGID=?) query 0x1765e0c | | none | R26V4 A.1 |
| 0xfce8c / 0xfd6bc / 0xfd23c / 0xfcca8 | week assignment (slot 19), preset weeks from SKNW/SANN, free-week masks, SCHD insert | | | none | R26V4 A.1 |
| 0xf9a74 | reads CNFR RUID 14 CRV1 (query 0x16f29f8) | | | none | R26V4 |
| 0xfc4ac | RoundRobin helper | | | none | R26V4 A.1 |
| 0x1048c8 / 0x106870 / 0x103b44 | base generate entry for different style classes | | | none | R26V4 A.1 |
| 0x1039xx..0x106e2c | style schedule methods, see 1.4 table. Table-path tests: `cmpwi r30,0x0` at 0x103bc8 and 0x1047fc ({0,1,11}); 0x106304/0x106310 ({4,10}); CGID tests at 0x103bb8..0x103bd0, 0x1047ec..0x104800 | | | none | R26V4 A.1 |
| 0x102e3c | SGNM numbering (inferred from QSTR) | Declares cursor over DYND ordered by GDAT, GTOD (0x16f3d54) and updates SGNM per game (0x16f3ddc) | | none | QSTR 102e3c; role UNVERIFIED |
| 0x102f6c | week/total renumber (inferred from QSTR) | Queries max SEWN (0x16f3e30), count SEWN=0 (0x16f3e58), `update ... set SEWN=?, SEWT=? where SEWT=?` (0x16f3e88) | | none | QSTR 102f6c; role UNVERIFIED |
| 0x109210 | game-mode comparison (code 125), substitutes rank 126 for non-FBS | Static lead, not active-array bound | | none | SI |
| 0x10ab9c | scales two team values by ceil(value*255/126) | Static lead | | none | SI |
| 0x10c6c8 | probability expression, 125 constant is not a team-count bound | | | none | SI |
| 0x4456c0 / 0x4470c8 / 0x459814 / 0x459848 / 0x459938 / 0x447078 / 0x43bd90 | helpers called by the generator (random, team type, pair-block, team data, etc.) | roles UNVERIFIED | | none | SEL 1023ac.c, 102850.c |
| 0x4cea2c / 0x4cea3c | BCS count immediates patched to 138 by activeN v1 | | | activeN | R26RR s2 |
| 0x4d8df4 | "Generating Schedule" progress (string 0x1781cb4) | caller of the dynasty schedule build (QSTR 4d8df4) | | start-year #11 (0x4d8e94) | QSTR, DSY s9 |
| 0x49e190 | clears UHFG/UFFG flags per SCHD game rows for the user team's games; cursor over COCH where CUFC=1 | | | none | QSTR 49e190 |

#### 2.2 Conference/CCG/BCS
| Address | Name/role | What it does | Mods | Source |
|---|---|---|---|---|
| 0x45c7e0 / 0x45b484 | CCG gate / CCG pairing | pairing cursor and DGID != DGID rule; hang if single DGID | activeN v1-v3 do not edit | R26DL |
| 0x461d74 | style selector | team count -> style; null for >= 17; CGID 5 -> ''. Callers 0x462138, 0x46217c; swap at 0x461f80 | none | R26DL |
| 0x4c98b0 | no-CCG CCHH path | champion recorded without CCG for conferences < 12 | none | R26DL |
| 0x45b0fc | CCG champion function (FCYR = SSYE+263 at 0x45b18c) | start-year #19 | start-year | DSY s9 |
| 0x45c074 | CCG champion trophy writer | trophy year SSYE+13 -> +26 | start-year v2 | SRR s6 |
| 0x4ca8a0 | BCS function (N-dependent pool 0x4ca858) | constants 0x4ca874 (127), 0x4ca878, 0x4ca88c | activeN v3 | R26RR |
| 0x4ce82c | calls 0x4ca8a0(week, N, vec, 1) | | activeN v1 | R26RR |
| 0x4c6308 | "Pref Team Rank Info"; constants 0x4c6300 (127), 0x4c62fc (f32 0.1) | | activeN v3 | R26RR |

#### 2.3 Dynasty stage machine / adapters (SAA, dynasty-leads references.txt)
| Address | Name | What it does | Source |
|---|---|---|---|
| 0x2da418 | broad initializer registering engine adapters; call at 0x2da5c8 passes object from 0x1c69308 to 0x8d6460 which installs at 0x1c96420 | SAA |
| 0x248a40 / 0x248960 | allocates 0x68 bytes / constructor; final vtable 0x18971c0 | SAA |
| 0x249950 -> 0x1fa8e0 | OffSeason_GameAdvanceToStage (vtable slot 0x58) | SAA |
| 0x24a760 -> 0x1fa190 | Schedule_GameAdvanceToOffseason (slot 0x68), target 0xc; submits callback 0x1fa4d8 | SAA |
| 0x2499f4 -> 0x1fb050 | Schedule_GameAdvanceToGame (slot 0x6c) | SAA |
| 0x24ff50 -> 0x1fa108 | CanAdvanceToOffseason (slot 0x22c); `0x1fa108` is "a mode test, not a season counter" | SAA, DSY s9 |
| 0x1fa4d8 | advancement callback; repeats 0x1f4604, then tests stage values | SAA |
| 0x1f4604 -> 0x44afdc | background task runner; loads callback descriptor at 0x1c75d70 and branches through its first word | SAA |
| 0x43cd14 | queries reversed tag 'ASCM' from 'NIOM' (MOIN.MCSA) then maps values via 0x43cc48 | SAA |
| 0xa67320 | DB query wrapper; decompiler often loses output pointers | SAA, SRR |
| 0x44afdc, 0x4f6d4c (Dynasty load) etc. | see start-year table | DSY s9 |
| dynasty-leads/references.txt string targets: 0x0170f918 TeamScheduleService::sPlayWeek; 0x017e1de4 AdvanceToOffSeason; 0x017e3968 GameAdvanceToOffseasonRecruitingWeek; 0x017e3ea0 OffSeason_GetListOfStages; 0x017e3ebc OffSeason_GetCurrentDynastyStage; 0x017e3ee0 OffSeason_GameAdvanceToStage; 0x017e3f4c Schedule_GameAdvanceToOffseason; 0x017e3f6c Schedule_GameAdvanceToGame; 0x017e47f8 AdvancetoPreseasonRecruiting; 0x017e4c70 CanAdvanceToOffseason; 0x016f7d8c FGGameRender (opd wrappers 0x00873dbc, 0x00882778, 0x00884f34, 0x00884fd8, 0x00885018, 0x00885068, 0x008850a8, 0x008853d8, 0x00885418, 0x008854a0, 0x008854e0, 0x00888c38, 0x0088aac4, 0x0088ab04, 0x001652a4); each calls FUN_0056b71c(.., "DynastyAdapterClass" 0x017e3ce0, name, "AdapterExtObject" 0x01887148) | dynasty-leads/references.txt + .c |
| 0x5012fc / 0x501340 | offseason stage callback (stage table 0x1c88ca4) that runs recruiting week advance 0x4c7bc4 twice (CFBR addresses) | SRR s2 |
| 0x4fccbc, 0x4fcedc, 0x4fcaa0, 0x4fc8bc, 0x4d4608 | coach carousel stages (COCT offers; CFBR addresses) | SRR s4 |
| 0x505dc8 | season rollover stage: `select SEYR,SSYE from SEAI`, `select MNSE from MOPT`, SSYE+1 always, SEYR+1 only if SEYR < MNSE-1 (cmplw at 0x505e40); update SEAI; global 0x1c87ed8 = SEYR | S85 s4 (CFBR) |
| 0x4d8d44 | final-season hook (from 0x4d92fc <- 0x4fa820, r4 = SSYE): if SSYE >= MNSE-1, `update COCH set COCT=3, COCI=? where TGID != 1023` | S85 s4 |
| 0x4f8cc0 -> 0x4d5e84 -> 0x4d5850 -> 0x4d5768 | TSHS insert chain at rollover | S85 s7.1 |
| 0x4eed88 | game-result function; BCHH/CCHH inserts (0x4eedd8 select SSYE) | S85 s7.1 |
| 0x4ecce8 | TPHS rolling-window delete at SEYR = SSYE-4 | DSY s5 |
| 0x4d893c / 0x4d8ba8 | recompute SEAI stage-week fields (SERW/SERB/SEFP/SNPW/SEOW/SESW/SNWP/SNDP/SNCP/SSTG) | DSY s9 |
| 0x4ceedc | week advance skips empty weeks (`count(*) where SEWN=?`) | DSY s10 |
| 0x46ecb8 | stage of a week from its SCHD rows | DSY s10 |
| 0x4fa820 | stage writing MOIN.MPSA/MPSC | S85 s16 |
| 0x4e9b30 | national-title commit (TEAM.NCYR = SSYE+0x107 at 0x4ea014) | DSY s1b |
| 0x4ea488 | season-end: NUMC+1, FCYR = SSYE+263 (sites 0x4eaadc, 0x4eab64) | DSY s9 |
| 0x4eaadc... etc. see patch tables | | |

#### 2.4 Year/calendar sites: see section 3.1 for the 47-word table (stock addr, CFBR addr, function role).

#### 2.5 Other functions touched by these docs
| Address | Role | Source |
|---|---|---|
| 0x47bbec | Players Leaving / Designating Redshirts flag array (`flags[PGID]=1`); crash site at 0x47bd54..0x47bd5c; allocates max(PGID)+1 at 0x1c78104/0x1c78108 | R26RR |
| 0x47e70c / 0x4809a0 / 0x4fb3ec / 0x4fa03c | redshirt / offseason stage chain | R26RR |
| 0x4b4dc0 | Play Time rating step (first rating step; label 0x17791d4); caches built by 0x47d274 -> 0x47cfe8(obj,A,17,C); fill 0x50c578 (query 0x178ce04); node insert 0x50c518 (no bound check) | R26CR |
| 0x472910 | builds all-team list (global 0x1c76898) | R26CR |
| 0x4c11e0, 0x4c31a0, 0x4c3738, 0x4c3e38, 0x4c7bc4, 0x4b83d4, 0x4b8ad4, 0x4b846c, 0x4b904c, 0x4c0700 | recruiting board fill chain, scheme table lookup `0x1c88db8` (20 rows x 19 bytes) (CFBR addresses; stock offsets 0x4c098c etc.) | SRR s2-s3 |
| 0x4524dc, 0x4526a8, 0x45c074, 0x467e7c, 0x4d82c4 | Trophy year writers (SSYE+13 -> +26); USDT.UTDY 7 bits from 2000 (display adds 0x7d0 at 0x2476d8/0x247988) | SRR s6 |
| 0x256590 | Coach Contract data provider (start=SSYE, value=SSYE-COCH.CTYR (0x21ac38), length=CONT.CCYR, isExtension=CONT.CIEX) | S85 s3 |
| 0x221df4 / 0x266740 | team record list (TSPH/CCPH/BCPH pre-Dynasty, TSHS with BCHH/CCHH) | S85 s3 |
| 0x41f1a8 / 0x43ba74 / 0x433bf8 / 0x433edc / 0x708260 / 0x803734 | MemoryFailure handler / write 0xbada110c to 0 / OOM dispatcher / category allocator / AptCallbackMemAlloc / APT pool | S85 s2 |
| 0x2d6714, 0x2d7724, 0x2d7c70, 0x2d8844 | news year formats ("%s wins the %d %s Championship." etc.) | DSY s9 |
| 0x45146c, 0x45d63c, 0x49e47c, 0x4d85a0, 0x1c134c, 0x3bbe14 | date displays converting G0 + 7*week back to date | DSY s9 |
| 0x45d488 | week -> date helper G0-relative | DSY s9 |
| 0x459acc / 0x45a390 | NCG host rotation (SSYE+2013)&3 / BCS host rotation (SSYE+2012)&3 into table 0x175aad8; 0x45a390 is inside playoff v3 cave [0x459e24, 0x45a614) | DSY s9 |


### 2.C Rules, playoff, rankings, news, coach

#### A2. Named functions (rules) -- Address | role | what | mods | src
| Address | Name/role | Notes | Mods | Src |
|---|---|---|---|---|
| 0x111f7d8 | OTR NCAA factory | sets +0x14 threshold (li at 0x111f82c) | R1 | MRD 2.1 |
| 0x111e480 | OTR possession setup (slot 0x3c) | spot<-+0x18; +0x18<-25.0; state slots 0xf0 spot, 0x104 down 0, 0x100 LTG 35.0 | wrapped by R2 modern_ot_setup | MRD 2.1 |
| 0x111e538 | 2pt-required predicate (slot 0x44) | readers: 0xde8e1c, 0xdeb014, 0xdec3d8, 0xded228, 0x1118d90 | none directly | MRD 2.1, 5.1 |
| 0x579fd0 | OTR set spot (stfs f1,0x18(r3)) | | | MRD 2.1 |
| 0xaa9c18 | NCAA OvertimeState update | phase0 coin toss when period==1&&series FIRST (then down 5, never phase 3); phase3 setSpot(25.0)+slot 0x3c; ONLY caller of slot 0x3c | via vtable | MRD 2.1, 9.2 |
| 0xd36630 | ClockRules slot 0x70 period/possession end (also from 0xab6f7c) | Q5: advance series; COMPLETE-> series 0, period++; else game ends (state 6) | | MRD 2.1 |
| 0xd55440 / 0xd55b88 / 0xd55cc8 / 0xd55e20 / 0xd560f0 | pointsrules NCAA post-play slots | down==4 in OT -> action 1 (possession over); else kickoff (3) | | MRD 2.1 |
| 0xde8e1c | NCAAPlaybookMgr formation filter (slot 0xc) | on PAT down w/ predicate true replaces kick group with group 0 | | MRD 2.1, 5.1 |
| 0xdeb014 / 0xded228 / 0xdec3d8 | formation users (UI; 0xdec3d8 = usage counter from 0xaada28, stores +0x3b4, tally 0xaada64) | | | MRD 5.1 |
| 0xdb6da0 / 0xdb6358 / 0xdb46ac / 0xdb82c4 | CPU + SuperSim play caller / AI pick; calls filter only if no group selected | bypasses kick filter | NOT hooked (gap) | MRD 9.2, 5.1 |
| 0x1118d90 | publishes OT period to situation key 0x26 | R1-A hook at 0x1118e08 | R1-A | MRD 9.3 |
| 0x3b8ccc | UI mask; hard-coded `period > 2` for PAT entry (cmpwi r3,2 at 0x3b8f24) | presentation | none | MRD 9.2 |
| 0xd2e2f8 | played end-of-play applier | writes down (slot 0x104), spot (0xf0), LTG if down 4 | | MRD 2.3.1 |
| 0xd2e1a0 | EndPlayRules (calls 0xd371b8) | | | MRD 3.1 |
| 0xd34048 | ClockRules tick (slot 0x08): 2-min warning (<=120.0, Q2/4, flag2) and 10-s runoff (clock<120, trailing, -10.0, gate +0x4f) | 120.0 const at 0xd34030 | P-C2 enables warning | MRD 3.1 |
| 0xd34edc | ClockRules slot 0x30 first-down handler | stop test `lbz r3,0x4a(r31)` at 0xd3539c (words 0xd3539c..0xd353c8, branch from 0xd3536c); `gs.slot_cc()->+0x28 & 0x400` = first down [INF] | P-C1 | MRD 3.1, 7.3 |
| 0xd371b8 | ClockRules slot 0xa4 end-of-play handler | OOB: start on ready except inside 2.0 min -> start on snap (slot 0x38 = 0xd35508, event 0x1d) | none | MRD 3.1 |
| 0xd378dc | ClockRules slot 0xa8 timeout | | none (C3 unbuilt) | MRD 3.1, 3.4 |
| 0xa6f0a0 / 0x3665a0 | SuperSim::GameRules obj / config ctor | | S-C2 at 0x366794 | MRD 5, 3.3 |
| 0xa6f330 | sim OT period start (single bl at 0xa6f554 inside 0xa6f444) | spot 25.0, down 0, LTG +0x60 | S2 ss_ot_start | MRD 2.5 |
| 0xa75bf0 | sim result applier (callers 0xa75e10, 0xa76130) | | S2 ss_apply | MRD 2.5 |
| 0xa707e0 / 0xa71240 / 0xa713c8 (x2) / 0xa715a8 | sim OT result writers; 0xa713c8 also TD->try writer | | read-only | MRD 2.5, 2.3.1 |
| 0xa7083c | sim college clock state (never START_ON_READY; returns 2/4/0xff) | | S-C1 call at 0xa71208 | MRD 3.1, 7.3 |
| 0xa711a8 / 0xa7111c / 0xa70c9c | sim first-down (2 callers) / next-down / change of possession | | | MRD 3.1 |
| 0xa71c00 | sim two-minute check (callers 0xa82274, 0xa71d00) | quarter 2/4, flag2 clear, clock<=GameRules+0x34 | via S-C2 | MRD 3.1, 5.2 |
| 0xa71b18 -> 0xa71908 -> 0xa7132c | sim result router / OT path; 0xa7181c scoring (sole caller site 0xa7196c) | | R1-S | MRD 2.3.1, 9.3 |
| 0xa76ab4 | sim resolver scorer (7 callers 0xa76d48, 0xa77308, 0xa77558, 0xa777b4, 0xa77a98, 0xa77bf8, 0xa77d50) | | R1-S | MRD 9.3 |
| 0xa730b0 | sim play log | cosmetic try tagging | | MRD 2.3.1 |
| 0xa75b24 | sim scoring (points table GameRules+0x6c) | | | MRD 2.3.1 |
| 0xa6fd70 / 0xa6fce8 | sim OT end condition | | | MRD 2.1 |
| 0xab7114 / 0x1140e8 / 0x12dfa4 | only writers of score/quarter/OT flag into GINF; 0x46c9e0 copies GINF->SCHD (from sim job 0x1fc6f0) | evidence Dynasty CPU games run SuperSim | | MRD 5 |
| 0x361ea8 | GameplayModeMgr registers PlayGameplayMode(0) / SimGameplayMode(1); SuperSim states 0x366870; engine 0xa814f4; PlayCallState vtbl 0x1892c18 update 0x138830; OT start callers 0xa81ddc, 0xa82558 | | | MRD 5, 5.1, 5.2 |

#### B2. Named functions (stock 1.00 addresses, PEM) -- Address | role | notes | mods | src
| Address | Role | What | Mods | Src |
|---|---|---|---|---|
| 0x504334 | begin-season (OPD 0x1bddf18) | sets MOIN.MCSA=7 | | PEM 2 |
| 0x4d52dc | "Starting Football Season" | SEAI SEWN=0, SEWT; calls 0x459a78 then 0x45c89c | | PEM 2 |
| 0x459a78 | copies BMFD/SGID/BPLO of bowl indexed by year-rotation table 0x175aadc into NCG row (BIDX 0x27) | | | PEM 2 |
| 0x45c89c | postseason placeholder creator | cursor `select * from BOWL where BCI1 < 18 order by BMON desc, BDAY asc, GTOD asc`; inserts SCHD GSTA=1 GHTG=GATG=0x3ff, sequential SGNM, writes BOWL SGNM/SEWN back; inactive rows SGNM=-1. SEWN from BMON/BDAY day-of-year at year 0x7dd+SSYE (base 17); SEWT=30+(week-first bowl week) cap 32, NCG 0x28; CCG SEWT 16; BIDX 25..28 inherit previous row SEWT. Helpers 0x450f88, 0x451158, 0x451224. | none | PEM 2, 5 |
| 0x45c7e0 | activity test | BIDX<0x21, >0x2c, 0x27 always active; CCG active only if BCI1<14, conf has >=12 teams (TOID=TGID), CGID!=5 | | PEM 2 |
| 0x4af79c(week,sewt) | start-of-week processing | SEWT==16 -> 0x45b484 CCG fill; SEWT==30 -> bowl-season start 0x4aae90 | | PEM 2 |
| 0x1fb8e0 (OPD 0x1bcb9e0), 0x1fb6f4 (OPD 0x1bcb9d8) | sim-to-week loop / single advance; call 0x4ceedc | Schedule_GameAdvanceToGame = 0x1fb050 | | PEM 2 |
| 0x4ceedc | week advance | 0x4ce82c end-of-week; next SEWN with count>0; SEWT via 0x46ecb8; `update SEAI`; 0x4af79c | | PEM 2 |
| 0x46ecb8 | SEWT of a week = max(SEWT) from SCHD where SEWN=week; fallback 0x0e / 0x1e (week>16); >=SEOW+SESW -> 0x96; stages 3..6 -> 0x97 | | | PEM 2 |
| 0x4ce82c | end-of-week processing: standings 0x4cc790/0x4cdc18 (SEWT<15 or ==16); BCS rank 0x4ca8a0 when (week+1>7 and SEWT<30) or week+1>=SEOW; bowl selection `cmpwi r30,0x1e` 0x4cea84 / `bge` 0x4cea88 / `bl 0x45bf44` 0x4cea8c (r31=week, r30=SEWT); then 0x4ca370->0x4c9c0c->0x4c9a7c->0x4c98b0 (CCHH for no-CCG conferences) | | HOOK HOST | PEM 2 |
| 0x45b484 | CCG fill: BIDX 0x21..0x2c except 0x27; CGID<14, >=12 teams, !=5; cursor STTM join TEAM order by tscs,TSDS; site from higher seed TEAM.SGID; calls 0x45997c | | | PEM 2 |
| 0x45bf44 | bowl/NCG selection (called end of each week SEWT<30 from week ~7; gate `0x43cf98()+1 < 8`): 0x45a618 (CCG champ table 0x1ce9860; 0x459b34 auto qualifiers; TBRK 1,2 -> 0x45997c(0x27,#1,#2); 0x45a07c BCS bowls 25..28), tie-in pass, 0x45bcc8 eligibility (SNCT<3, win% >= const 0xbc370; Notre Dame/Navy/Army TOID 0x44/0x39/8 special), 0x45bdc0 at-large | | v0 hook calls it | PEM 2 |
| 0x45997c(BIDX,GHTG,GATG) | FILL primitive: 3 queries (BOWL SGNM,SEWN; CFUC count; update SCHD GHTG,GATG,GFHU=0,GFFU=0). Does not check GSTA | | used by cave | PEM 2 |
| 0x50614c (OPD 0x1bddfb8) | result commit: 0x46b640 writes SCHD SEYR,GHSC,GASC,GSTA; SEWT<15 or 16 -> 0x4ea488; SEWT 30..40 -> 0x4e9b30 | | | PEM 2 |
| 0x4e9b30 | SEWT==0x28: NCYN+1, NCYR=SSYE+0x107 (RAW 0x4e9fd4..0x4ea018); CBOW/CBOL | v1+ C1 recorder call at 0x4e9fd4 | | PEM 2, V3 4 |
| 0x4ed948 | recorder: SEWT 30..40 -> BCHH insert (BIDX from BOWL by SGNM,SEWN); SEWT 16 -> CCHH insert (CCHH query 0x17658f4 at 0x4edc04); FBS (LGID 0) only | v3 recorder call site 0x4edb0c | | PEM 2, V3 2.1 |
| 0x4d96fc | SCHD row insert in current week (SGNM=max+1, updates GINF); reached from UI 0x23f008 | | | PEM 2 |
| 0x45da10 | bowl-selection UI labeller "<conf> Champs" (A1 precedent) | | | V3 2.1 |
| 0x45a618 | fills 0x1ce9860 from SEWN 16 games; refilled only when `0x43d104() > 14` | | | V3 2.1 |
| 0x4c98b0 | records standings champion into CCHH for no-CCG conferences | | | V3 2.1 |
| 0x45a07c | BCS tie-in filler; call at 0x45a844 `bl 0x45a07c` | disabled by v0+ (`li r3,0`) | | V0 2 |
| 0x43cf98, 0x43d104 | SEWN-ish accessors; return semantics unreliable in decompiler | | | PEM 6, V3 |


### 2.6 Stock/CFBR address pairs and cave regions

- Stock ELF a486a946...7abe (file offset = vaddr - 0x10000) vs CFBR v21 ELF 144dee90...0c1c: playoff/news/coach/UI docs give both; MRD rule addresses are CFBR v21 only (e.g. OTR factory 0x111f7d8, ClockRules 0xd33c28, SuperSim 0xa6f0a0) -- do NOT assume stock equivalents. Known stock<->CFBR pairs: bowl_site 0x111fa3c <-> 0x112252c; 0x43d104 effective SEWT <-> CFBR SEWT accessor 0x43e5c4 (pcs says 180 `bl 0x43e5c4` sites); CCG fill 0x45b484 <-> 0x45c3fc; HOOK 0x459e24 (stock cave) <-> 0x45ad9c (CFBR); hook site 0x4cea8c <-> 0x4cfc9c; picker 0x478cc4 <-> 0x47a14c; EA-SQL 0xa67320 <-> 0xa691b0; crash frame 0xa80288 <-> 0xa82118; contract pass 0x4d7814 <-> 0x4d8a3c. [PCS, CRN, CCR, PBU]
- Query-string anchors preferred for CFBR ports (not addresses): BOWL/SCHD texts at stock 0x1763be8, 0x176475c, 0x1775cd4. [PEM 5]
- Cave regions summary: stock 0x1bbf100..0x1bc0000 (news fix 0x1bbf100); CFBR tail 0x1bc2700..0x1bd0000 with news fix 0x1bc2700..0x1bc29cc, modern rules 0x1bc2a00..0x1bc3080 (v2) [0x1bc2a00,0x1bc4000 reserved], campus 0x1bc4000..0x1bc40cf, projection 0x1bcff00..0x1bcff17. Stock postseason cave [0x459e24,0x45a618) full (509/509); user-play region R2 [0x459b34,0x459e24) ~7 free words. [CRN, MRD, PCS, PBU, UPR]
- Test fixtures referenced: stock-bowl-2013, playoff-e3a-sewn17, playoff-v1-final, playoff-v2-sewn17, po1-sewn17, po4-sewn17, r26c-sewn17, pu2-final, po2-final-2013..2016, a138v2-endseason2013, active127v6-endseason2013, boot127-endseason2013, stock-preseason-2013-MODBASE, y2026-week1-snap, y2026-offseason-snap, r2026-confchamp. Save slot names: DEFAULT9 (E3-a), R26PO1/R26PO2/R26PO4, R26PU1/R26PU2, Y2026A, CFB138, STEP3A. [E3S, CPR, UPR, CCR, MRD]


