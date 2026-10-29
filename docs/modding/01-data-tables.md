# Data tables and structures

Part of the [modding knowledge base](README.md). Our own analysis of NCAA Football 14 (PS3, BLUS31159) and the CFB Revamped v21 base: names, addresses, table layouts and how our mods are built. Source tags in brackets (for example TEA, CFBR) refer to private working notes that are not published; treat each statement as a compiled finding, not a re-verified fact. No game files, extracted assets or decompiled code are included.

## 1. Data tables and structures

Coverage map: teams (1.A.1), players/depth charts/coaches (1.A.3, field maps are thin, see gaps), schedule (1.B.1, 1.B.2), conferences (1.B.4), rules (1.C Part A), dynasty/stage machine (1.B.5), recruiting (1.A.5 to 1.A.8), calendar/year (1.B.7, 1.B.10), playoff/coach/news/stats (1.C).

### 1.A Teams, players, recruiting, capacity (STOCK addresses unless marked CFBR)

Abbreviations for sources (all under the private docs folder\ unless noted):
TEA=team-expansion-analysis.md; RFA=recruiting-first-array-relocation.md; RPC=recruiting-preference-capacity.md; RRT=recruiting-relocation-test.md; RRS=recruiting-reserve-test.md; SRT=scratch-reserve-test.md; BPT=board-pool-test.md; BRT=board-relocation-test.md; CIT=capacity-integration-test.md; FSC=fullscale-serialized-capacity.md; PIT=preference-integration-test.md; ATD=active-team-dependencies.md; ATP=additional-team-prototype.md; A127=active127-runtime-test.md; A138=active138-proto.md; RCA=active138-crash-rca.md; ANT=activeN-runtime-tooling.md; CTM=cfbr-team-input-map.md; CAA=cfbr-archive-adapter.md; CPT=cfbr-port.md; CIN=cfbr-integration.md; RL=analysis\team-expansion\recruiting-layout.json; FCI=analysis\team-expansion\fullscale-capacity-inventory.json; ACR=analysis\team-expansion\active-count-review.json; DC=analysis\dynasty-constructor\*; DO=analysis\dynasty-object\*.

Global identity: stock ELF SHA256 a486a9467c740637892df1fc407d8fea9d92d83cf11ff0de3fe464f934e47abe; PPU-011a5e6caad2e7361265a9a230cf385f805671fb (TEA, RRT). CFBR v21 / update 01.02 ELF SHA256 144dee9040da9cb1e8337844fbb685a0f06e560b8fee8d9ba1eac87b9e300c1c, PPU-62e25ebc1957382b34f2778554943e40d6d84e3c (CIN, CPT). All addresses below are stock-ELF virtual addresses unless marked CFBR. All claims are static-analysis plus the runtime tests named; "UNVERIFIED" marks anything the source itself hedges or that I could not tie to text.


#### 1.1 TEAM table (DB table TEAM; query tag appears reversed in raw strings as MAET)
- Fields named in docs: TGID (team id), TOID, TSID, TCID, TVIS, TTYP, TORD, TCRK, TMRK, TBRK, LGID, CGID, DGID, SGID, TGRP, TGPT, TSI1/TSI2/TMPI/TPIO/DCAP/OCAP (player refs), TMCP (head coach pointer), TDNA (display name), NCYN/NCYR (national-champ count / most recent year), TDNA. (ATP, A138, CTM, ATD, BRT)
- TGID <= 1006 is the valid range used by the league index fill (TEA).
- TVIS=1 optionally required by index fill (TEA). TTYP=0 = FBS; second list additionally requires TTYP=0 (TEA). TTYP values seen: 0 FBS, 1 FCS ("FCS East" etc., TGID 160-164), 7 CPU high-school team, 8 user high-school team (CTM). Also "TTYP1" for generic "FBS Generic" ID162 in CFBR autoload (CTM).
- TORD: sort key for index fill (ascending). Stock: FBS teams TORD 0..125; generic FCS entries start at TORD 428 (TEA). Expansion teams placed at TORD 126..137 before FCS (A138). "TORD is recomputed" for the prototype (A127: "TORD is recomputed27" - i.e. 127? read as recomputed to 27 UNVERIFIED wording).
- TCRK / TMRK / TBRK: saved as unsigned 8-bit fields; TCRK and TMRK already reach 131 across saved teams (FSC, FCI.rank_findings). A138 sets TCRK/TMRK = TORD+1 for added teams.
- Field widths (CTM): TGID/TOID 10 bits, CGID/DGID 5 bits, SGID 10 bits, TTYP 5 bits. "Actual bit offsets differ across roster versus Dynasty template. Schema-driven writes required; never copy packed stock rows blindly."
- Row bytes: TEAM 328 bytes/row (FCI sample).
- Capacities: roster template TEAM 141/146 (TEA); Dynasty save 132/146 (FCI); v6 reserve 192 (FSC). Roster asset has 142/146 rows with 15 non-FBS rows vs Dynasty save retains 5 (FSC). Stock Dynasty save = 131 teams (126 FBS + 5 FCS) (RRS "All 131 stock TEAM IDs, including 126 FBS"); prototype adds TGID116 -> 132 (A127/FSC). Roster 138 build: Roster TEAM 153/192; Dynasty TEAM expected 126+12+5=143 (A138, ANT).
- Non-FBS rows (15 retained): TGID 160-164 (TTYP1 FCS East/West/Northwest/Midwest/Southeast), TGID 610 (TTYP8 "User HS team"), 611-619 (TTYP7 "CPU HS team 1..9"), TOID == TGID for these (CTM).
- Identity detail: prototype clone TGID116 keeps donor Idaho (TGID34) TOID/TSID/TCID (34/34/119) at first; later prototype stadium identity separated: prototype SGID115, donor model SUID33 (A127). Added TGIDs 117..127 get own stadium SGID 116..126 cloned from SGID33 (A138).
- Duplicated-ID facts for CFBR: CFBR uses TGID 34 (Appalachian State), 61 (Coastal Carolina), 100 (Charlotte), 181 (Georgia Southern), 230 (James Madison) where stock has Idaho, New Mexico State, Connecticut, UMass, FIU (CIN).
- Source for TEAM-field use in code: 0x47af94 loops 126 FBS entries issuing TEAM-field update (TEA).

#### 1.2 League index (all-team and FBS lists) - globals
- Initializer 0x472d78 queries TEAM counts, allocates 12 bytes per entry plus spare entries (TEA).
- All-team index pointer / count globals: 0x1c76898 / 0x1c768a0. FBS index pointer / count globals: 0x1c7689c / 0x1c768a2 (TEA; 0x1c768a2 read as `lhz` in RCA).
- Fill function 0x472910: TGID <= 1006, optional TVIS=1, sorted by TORD ascending; second (FBS) list also requires TTYP=0 (TEA).
- Invariant: new FBS records must sort before FCS entries (TORD 428+) since consumers use "first N entries of all-team list" (TEA). Preference-code at 0x4bf8ac uses all-team dense index; "FBS-first index invariant requires validation" (RPC).
- CFBR FBS count global is 0x1c86922 (CPT: "FBS count 0x1c86922, decoded at three anchors"). CFBR globals = stock + 0x10080 (CPT).
- Index width: 0x4bd9d8 and 0x4b7970 truncate team index to 8 bits (fine up to 255) (A138, TEA).
- 219 reads of those 4 globals in 97 approximate functions were scanned (A138).

#### 1.3 PLAY (players) / DCHT (depth charts) / COCH, CSKL, COPS (coaches)
- Player IDs: player-ID range for a team is TGID*70 through TGID*70+70 (0x48dec4 PLAY update loop, 126 FBS entries) (TEA). Prototype players use TGID*70 + donor slot (ATP); "Player IDs use TGID*70 + Idaho's slot" (A138). PGID = player id field; PTYP, PPOS, PYEA (year), PHGT, PWGT (raw), OVR (PGID, PPOS... named in RRT/CIT). Inactive/unassigned rows have TGID 1023 with PTYP 3 (PIT).
- PLAY row bytes 120; DCHT row bytes 8 (FCI sample). DCHT = 88 rows per FBS team (FSC). Roster template PLAY 8568/9100, DCHT 8568/11464 (TEA). Dynasty 2014 PLAY 8842/9100, DCHT 11176/11464 (FSC). v6 reserve PLAY 12600, DCHT 14080 (FSC). 138 roster: PLAY 9384/12600, DCHT 9384/14080 (A138). 68 players + 68 DCHT-rows + 3 coaches per added team (ATP, ANT).
- Depth chart rebuild: 0x49b068 emits the status literal "Setting Team Depth Charts" and rebuilds per-team DCHT for exactly 126 entries (TEA). Table tag in raw query strings is reversed: THCD -> DCHT (RPC).
- COCH: roster template 403/409 (TEA); fresh/2014 saves COCH 402-406/409; recent saves only 3 unused slots (ATD); v6 reserve 768 (FSC), v2 template 512 (A127). COCH row bytes 176; CSKL 28 bytes; CSKL/COCH capacity 512 -> 768 (FCI, FSC).
- Coach IDs: CCID. Prototype coaches CCIDs 393,394,395 for HC/OC/DC (ATP); activeN 138 adds CCIDs 396..428 (A138). COPS 0,1,2 = three staff positions (HC/OC/DC) per team (ATD); COTY 0 or 2 = eligible coach types (ATD).
- Coach query/functions: 0x4d36ac selects TEAM rows where LGID=0 (query 17809d8), loops COPS 0,1,2, counts non-expired CONT records (query 1780a6c), generates contract and inserts (query 17806f0) if missing. 0x4d386c builds records from eligible COCH rows (query 1780ad0). Other contract insert sites 0x4d2b50 / 0x4d5690. CREP (coach CCID keyed) update 1765108 / insert 1765158 only after not-found status 0x17 in 0x4d68f8 and 0x46104c. Writer paths 0x471f00 / 0x4f7ea8 part of lifetime audit (ATD).
- Coach skill vector 0x4be4f4: 126x16-byte records, base r1+128, frame 2208, called from 0x503e3c and 0x4c6bbc; cursor over CSKL x COCH `COPS=0 and TGID!=1023 and SCLB>0`; data-dependent overflow risk (RCA).
- Coach scratch stores 0x4c93fc/0x4c945c are 32-bit; 0x4a4bf0 stores a 16-bit rank (FSC). Coach rank clamp words 0x4c93f0/0x4c93f8/0x4c9450/0x4c9458 (125 -> N-1) (A138).
- CPRF: coach profile table; 381 -> 387 -> 390 against capacity 409 (v5); reserve proposed 768; row bytes 12, alloc type 14 (FSC, FCI). CONT (contracts) 549/756 (ATD) or 542/960 (A127, v2 reserve); CREP 137..164/504 (ATD) -> 640 (A127). Capacity 504/756 "must not be labeled team arrays solely because they divide by 126" (ATP).
- RTPB (6 allocation type, row 8 bytes): empty at fresh creation; 127 unique FBS IDs at endseason/2014; capacity 140 -> 160 (FSC, FCI).

#### 1.4 Conferences
- TEAM fields CGID/DGID (conference/division; 5 bits each) (CTM). Prototype/clone conference + division match Idaho/Independent (A138). Existing CONF IDs resolve intended conferences "not their modern scheduling rules" (CTM).
- CFBR 138-team proposal conference counts: ACC 17, American 14, Big Ten 18, Big 12 16, CUSA 10, MAC 13, MWC 10, Pac-12 8, SEC 16, Sun Belt East 7, Sun Belt West 7, Independent 2 (CTM). 47 existing names need conference-ID changes (CTM).
- Conference history table CCHH (conference history: 20/30/40/50/60 rows seen), bowl history BCHH; both persisted across rollover (SRT, BPT, CIT, PIT). PSRA 2449/2500 per conference (A138; FCI 2448/2500 aggregate sample). Query-expression node pools of 127 entries at 0x479f08, 0x4a27d0, 0x4a2acc, 0x4a4570, 0x4a9560, 0x4a96b0; need 4xconference_team_count-1 nodes; 18 Independents need 71 nodes (A138). No conference-specific code structure otherwise documented in these docs.

#### 1.5 RecruitMan (recruiting manager object) - allocation and layout
- Facade constructor 0x360d88 installs vtable 0x18a8118 via global 0x1c78cfc; getter slot 0x14 -> OPD 0x1bdf110 -> code 0x1470ab8, loads recruiting global 0x1c78d0c; setter slot 0x48 -> 0x5066cc (SRT, RL).
- Init function 0x35e998 allocates 0xc81c bytes labeled "RecruitMan" (allocation size instr 0x35eaac, alloc call 0x35eacc; RL gives allocation_bytes 51228), constructs via 0x5067a4 (STDU-first; MFLR at 0x5067a8), and passes result to setter 0x5066cc. Object vtable 0x18a8190 (SRT, RL, RRT).
- Stock layout: first array +0xb08..+0xef7 (126 x 8 bytes; RL start 2824 stride 8 count 126 end 3832); intervening metadata +0xef8 (u16 at +0xef8, +0xefa; RL lists 3832, 3834, 3836, 3837) ; second array +0xf00 stride 0x178 (376) x126 ending +0xc80f (RL start 3840, end 51216); tail +0xc810..+0xc81b (12 bytes: callback pointer +0xc810, callback byte arg +0xc814, database handle +0xc818) (SRT, RRS, RL).
- First-array record 8 bytes; constructor fills sentinel 03ff000000000000 (RRT); reset 0x494c48 stores 0x3ff at +0xf00 (stock) at 0x494c6c (RFA). Halfword at base+index*8+0xb0a read by 0x50a80c (RFA).
- Second-array record (stride 0x178) fields identified: +0xf05 (byte, read by 0x4b919c, incremented by 0x507e94, relative to second-array base accessed as obj+0xf05 at stride 0x178 via FBS-index; so field offset +5 within record), +0xf06, +0xf07, +0xf2e (record fields initialized by 0x4be638 and 0x4b7970) (TEA, ATD). Record field semantic meanings: UNVERIFIED (not given).
- Runtime-observed instances: RecruitMan 0x1111ae70, facade 0x100c4e10, vtable 0x18a8190, manager/getter identities (SRT, RRS, RRT).
- Ranking buffer owner 0x1b41cc (frame 0x8c0 -> 0xae0 after reserve), object_offset 144/data_offset 16/data_bytes 2016 (126x16), callee 0x4ecad0 (RL, SRT).
- Tested relocated layout (patch recruiting-relocation, 50 words): first array +0xb08..+0x1007 (160x8), metadata +0x1008..+0x100f (moved +0x110), second array +0x1010..+0xfb0f (160 x 0x178), tail +0xfb10..+0xfb1b, allocation 0xfb1c (RFA, RRT). Active FBS count and first-array fill limit remain 126. Intermediate "second-array-only reserve" layout (14 words): second array base +0xf00, clear size 0xb910 -> 0xeb00, tail +0xfa00 (callback ptr), +0xfa04 (byte arg), +0xfa08 (db handle), allocation 0xc81c -> 0xfa0c (RRS).
- Tail accessors: 0x4ab17c, 0x509e70 read/clear db handle; 0x4ade08, 0x509d64 write it; 0x4af68c reads completion callback+arg; 0x5067a4 initializes all three (RRS). Other-array clear at 0x4c6940 (RRS).
- Excluded false matches: 0x2e16d4/0x2e1c90 and 0x6740b8..0x675288 (debug user-info object vtable 0x189cab8) (RRS); audio caller 0x6c9e38 (0x21ec HrtfFilterCurrent buffer -> 0x6d8eac); graphics ctor 0x590df0 (0x1650 RNADevice), 0xf2d79c, 0x38a440->0xf2eda8, vtable 0x0190e290+0x14 -> OPD 0x01c31518 -> 0xf2dd78 -> 0xf240e8/0xf1f268; leaf getters 0xf3079c/0xf307b4 (read base+index*4+0xf54) (RFA, RRT).
- Recruiting-class counts (per team): 0x4b57c4 stack array of 7 bytes/team (see 1.9).
- Related labeled allocs NOT team-indexed: RecruitScoutMan (2000-float array), DynastyIdMap (two 96-node pools) (SRT).

#### 1.6 RecruitPrefMan (preference manager)
- Allocated 0x31b8 bytes at 0x35e998 (alloc instr `li r3,0x31b8` at 0x35ebc0), constructed by 0x50c954, vtable 0x18a8200; facade setter slot +0x4c receives constructed pointer (RPC).
- Cache: starts +0xc; entry = team_index*24 + category*12; two categories x three 32-bit values. Cleared with -2000 via word-fill helper 0x69ac70 (0x2f4 words = 126*6) in constructor 0x50c99c and reset 0x4b47e8. Cache ends +0xbdc (126*24) (RPC).
- Setter 0x4b3838 (guard 0x4b3844), getter 0x4b3890 enforce 126-team limit; 24-byte entries (ATD).
- Adjacent second array: +0xbdc, 76 bytes/team (9 x 8-byte pairs + one 4-byte word), 126*76 = 0x2568, ends exactly at 0x3144. Virtual getter 0x50c9bc computes dense index i -> 76*i, returns 0xffff for missing TGID (no apparent local guard). The 76-byte record's PTIP-related content: 14 pitch bytes per team (RPC). Tail: +0x3144 external pointer (used by 0x50ca8c), +0x3148 flag, +0x314c..+0x319f 21-word array (used by 0x50e19c, 0x50cad0), +0x31a0 db helper, +0x31b0/+0x31b4 (RPC).
- Planned 160-team layout (installed in 185-site experiment): cache +0xc..+0xf0b, second array +0xf0c..+0x3e8b, tail +0x3e8c..+0x3eff, total 0x3f00; second-array accesses shift +0x330, tail +0xd48; clears 960 words (RPC, PIT).
- Vtable slots 0x18a8200..0x18a8220 = nine methods (RPC). Destructor 0x47be80 frees pointer fields +4/+8 (RPC).
- Provenance: 0x4f599c retrieves RecruitPrefMan via facade vtable+0x18, tests +0x31b4, invokes 0x4c6308, assigns external pointer +0x3144, calls 0x4b1ae0 then 0x4b1510 (RPC).
- Pitch serialization: DB table PTIP (raw tag PITP reversed): 1764 records = 126 teams x 14 pitch indices; each FBS team has RPIT0..13 exactly once (RPC). PTIP capacity 1778 (stock), 2240 reserve (FSC). Other reversed tags: ADPT->TPDA, THCD->DCHT, MAET->TEAM, DIGT->TGID (RPC). SOPR also noted.
- 0x4b1510 serializes 14 per-team pitch bytes into DNYD PITP table using FBS count and record base+0xbdc / stride 0x4c; 0x4b1ae0 clears FBS_count*0x4c at +0xbdc, assigns TGID sentinel 0x3ff, calls 0x4b1938 per team (RPC).
- Missed local sites: 0x4f4ca0 (leaf; writes first record TGID sentinel at +0xbdc), 0x4f52a8 and 0x50fae8 (same reset after manager dispatch), 0x50dedc (leaf clearing flag +0x3148), 0x50df44 (all-team dense index access to 76-byte array) (RPC). Getter 0x149a8d4 belongs to different object (vtables 0x18aeb44/0x18b1954); linkage slot 0x16d5f50 excluded (PIT).
- CFBR differences (CPT): preference class inserted two virtual methods: +0x08 new query helper (stock +0x08 0x50c9bc is CFBR +0x0c 0x50e378); +0x24 is 0x50f93c (stock direct-call 0x4bf8ac now virtual; stock 0x4bf978 -> CFBR 0x50fa10); stock +0x10 0x50cad0 -> CFBR +0x14 0x50e488 with bounds check and CFBR-only tail field 0x3148 read (0x50cadc -> 0x50e4ac; extra word 0x50e494 relocated to 0x3e90).

#### 1.7 RecruitingBoard (scheduling/list object, "RECB")
- Identification: allocator/constructor 0x4ad7c0 / 0x4ad500, string 0x1778038, RECB query 0x4ad13c, manager global 0x1c79308, board vtable 0x18aa530 (BRT). Lazy reference-counted allocation/destruction via 0x4ad7c0/0x4ab2ac; 0x4c69b4 allocates around simulation work then releases (BRT).
- Old layout: object 0x33d44 (+8-byte allocator header = 0x33d4c). First 126 team pointers +4..+0x1fb precede list head +0x1fc; +0x200 is another list pointer, +0x204 allocator; hash tail state +0x22964/+0x22968 (ATP). 4410 records x 20 bytes; 12-byte list/hash nodes (BRT).
- 160-pointer relocation v2 (storage-only, tail shifted +0x88=136 bytes): list +0x284, pool +0x29c, recruit records +0xd160, hash +0x229e8, buckets +0x22a18, hashpool +0x26f08, object 0x33dcc, allocation 0x33dd4 (BRT). v1 missed 0x4bf06c/0x4bf070 (+0x1fc->+0x284) and 0x4bf114/0x4bf11c (+0x204->+0x28c); crashed at PC 0x4bf064 on Start Season (BRT).
- Pool expansion (board-pool): 4410 nodes -> 5600 (160*35); two aligned node spans -> 0x1068b; object allocation 0x41cf4; hash requests 5601 buckets, picks 5503; 0x4c5910 stack record storage grows; 406 instruction words; Table RECB capacity 5600 (BPT, FSC).
- Consumers: 0x4acd20 walks board per-team list via all-team index; uses first-array lookup and 126 bounds (BRT, ATD). 0x4ad704 caller of specialized ctor 0x146755c (BPT). Specialized: external fixed-address RecruitingBoard allocator 0x14085d4 (null on exhaustion) (BPT, CIT).

#### 1.8 Recruiting DB tables (saved)
- RCTC (recruiting class / team commit counts; 16 B/row), TEXP (team expectations; 8 B/row), TSSE (52 B/row), RTPB (8 B/row), PTIP (4 B/row), MCOV (136 B/row; 8 stories per team max x teams; 1016 for 127 teams), RECB (12 B/row, alloc 30, max 5600), RECV 6300?, RCPT 4305? (CTM flags RECBmax4410 / RECV6300 / RCPT4305 as tables outside reserve growth), RCCM (commit membership; RCCM1 + RECB membership indicates commitment; "RCPR is NOT a demonstrated team ID"), RPIT (pitch id), CREP/CONT (coach rep/contracts) (A127, A138, CTM).
- Commitment interpretation correction: board membership plus commitment status does NOT establish destination team (A127 v5 section).

#### 1.9 Other fixed-size per-team scratch (stack / heap) buffers, stock 126-team
| Owner function | Buffer | Stock size | Source |
|---|---|---|---|
| 0x4b57c4 | recruiting-class eval, 7 bytes/team on stack SP+0xb8..SP+0x42a; vector scratch SP+0x430..43f; frame 0x490 -> 0x580 (160 recs, scratch SP+0x520) | 126 | TEA, SRT |
| 0x4ecad0 (owner 0x1b41cc, passes SP+0x90) | ranking records 16 B, object+0x10..+0x7f0; frame 0x8c0 -> 0xae0 | 126 | TEA, SRT |
| 0x4facb8 | team sort records 20 B; clamp to 126 (cmplwi r30,126 at 0x4facd4 plus li at 0x4facdc); frame 0xa90 -> 0xd40; capacity 2520 -> 3200 | 126 | TEA, SRT, RCA |
| 0x4b8db4 | clears 0x3f0 bytes at obj+0xb08 (first array), passes 126 to 0x4b8cd8; next fields +0xef8/+0xefa | 126 | TEA, RFA |
| 0x4b8cd8 | fills first-array; raw limit 126 at 0x4b8da0 | 126 | RFA |
| 0x50be80 | 8 B/team temp array; alloc 0x50bf1c, capacity end 0x50bf44, logical end 0x50bf90 = 0x3f0; init/copy limits 0x50bf7c/0x50bfe0; consumers 0x50c054/0x50c080 | 126 | RPC, A138 |
| 0x4fea60 (from 0x4ff714) | 126x8 temp; alloc/capacity/ctor 0x4fea8c/0x4feab4/0x4feaf0; logical end 0x4feb00; passed to 0x4fdf58 | 126 | RPC |
| 0x4b47c8 | 3 node pools x126 nodes x 28 B (payload 0xdc8, buffer param 0xde3); frame 0x2e50 -> 0x3a20; separate 126-word array at SP+0x2bc0 (fill bound 0x4a30 area 0x4b4a30); pools approx SP+0x180/+0x198, +0xf80/+0xf98, +0x1d80/+0x1d98 | 126 | RPC, CIT |
| 0x4a9078 | 126 recs x 0x90 stride at SP+0x178, frame 0x4900 -> 0x5c20, story context ptrs -> 0x5b78 | 126 | ATP |
| 0x4a141c | 126x20 at SP+0xb0, ends SP+0xa88; flags at SP+0xa90; frame -> 0xe30 | 126 | ATP |
| 0x4b1f3c | TV Exposure sort 126x20, base r1+132, frame 2704 | 126 | RCA |
| 0x4fc830 | Pro Potential sort 126x20, base 128, frame 2688 | 126 | RCA |
| 0x4f85bc | Program Tradition sort 126x20, base 200, frame 2784 | 126 | RCA |
| 0x4be4f4 | coach-skill vector 126x16, base 128, frame 2208 | 126 | RCA |
| 0x4c5910 | board stack temp (big offsets are stack-relative) | scaled with board | BRT, BPT |
| 0x47e954/0x47e9ec | TEAM/STAD query result list allocation 126*44+8 = 0x388015b0-loaded; patched to 160*44+8 | 126 | A127 |
| 0x4a8918 | loops <= 8 stories per team; MCOV insert query 1776a50; parent 0x4a9078 iterates FBS TEAM rows ordered by TCRK | 8/team | ATP |
(Additional 0x5068d4 FBS-lookup gate at 126, per-team data stride 0x178 at obj+0xf05; 0x4b919c / 0x507e94 leaf accessors check idx<126, bounds at 0x4b91f8 / 0x507ee4 (TEA).)

#### 1.10 TDB (database) format, CRC rules, archive containers
- Retained format refs: analysis\madden-file-tools\package\services\CRC.js and streams\TDBWriter.js (TEA).
- Table-header CRC covers bytes +4..+35 (excludes the prior-table CRC). Payload CRCs are chained into the next table header; the last is in the database footer. 660 checks passed over leading DBs in QKL_BOOT entries 355/826 and QKL_MISC entries 145/7 (TEA).
- Allocation types: type 26 uses "current-record" storage (capacity changes do not append unused rows); types 2, 6, 14, 30 appear in fixtures (TSSE alloc 2 in MISC template; others alloc 6/14/26/30). "Indexed and unsupported allocation types cannot be resized." Fixed allocations grow by appended bytes (e.g. PTIP 2240 + RCTC/TEXP/TSSE 160 adds 4488 bytes in populated 2018 copy) (TEA, PIT, FCI).
- Template entries: QKL_BOOT entry 355 = roster, nested GAMEMODE/Dynasty template = entry 354 (CAA, ATP: "both roster 355 and nested GAMEMODE 354 from BOOT"); QKL_MISC entry 145 = Dynasty template standalone (PIT, TEA); MISC schedule data in v1. The extracted Dynasty template entry has 4200 bytes after its declared TDB length (text/SQL/binary; nonzero; must be preserved as trailer) (TEA, ATP). CFBR nested payload starts at 121 (stock 120) with no trailer (CAA).
- Archive builders: append-only replacement of entries 354/355 (825 other BOOT entries unchanged); `build_active127_archive*.py`; `scripts/tdb_capacity.py`, `tdb_records.py` (standalone writer for fixed unindexed tables) (ATP, CAA).
- Save container: USR-DATA = leading TDB + opaque trailing save container (~5.2M bytes; 5,248,704 trailing in v5 and 4,655,364 in v6; HED/SFO/ICON files accompany) (FSC). Do not classify trailing data as free (FSC).
- Reserve recipe table (v6, FSC): TEAM 146->192, PLAY 9100->12600, DCHT 11464->14080, STAD 200->240, COCH/CSKL 512->768, CPRF 409->768, RTPB 140->160, SCHD 931->2048, PTIP 1778->2240, RCTC/TEXP/TSSE 127->160, MCOV 1016->1280; RECB 5600, CREP 640, CONT 960 unchanged. Observed v6 stock fresh sizes: leading TDB v5 3,029,312 vs v6 3,622,652 bytes; USR-DATA 8,278,016.
- Other capacity-tight tables: RBKS 3402/3643 stock (3618 after season 1 with 138 teams; 3726 would overflow), TPHS 572/572 (full), PSRA 2449/2500, SKNW 1894/1894 (full; round-robin rows reuse far-future presets SESI 53..59) (A138). BCHH/CCHH history rows grow annually (BCHH 68 -> 102 -> 136 -> 170 -> 198 ; CCHH 20 -> 30 -> 40 -> 50 -> 60) (SRT..PIT).

#### 1.11 Schedule/season scaffolding referenced
- Fixture conventions: SEWN (stage-week; conference-championship week SEWN 16, end-season SEWN 22/23), SCHD table (schedule), SEAI, BCHH, CCHH, NCYN, NCYR (RRT, BRT).
- Scheduling code: progress strings identify 0x103064 orchestration and 0x102850 remaining-game generation; 0x4d8df4 Dynasty schedule entry path; scheduler region 0xfe000..0x103500 (A127). 0x4aac1c, 0x4a9fe0 use the scheduling/list object (ATP).
- Dynasty advance callbacks (DC dispatch.json): OffSeason_GameAdvanceToStage (vtable 0x18971c0 slot 0x58, OPD 0x1bcd050, code 0x249950), Schedule_GameAdvanceToOffseason (slot 0x68, OPD 0x1bcd178, code 0x24a760), Schedule_GameAdvanceToGame (slot 0x6c, OPD 0x1bcd060, code 0x2499f4), CanAdvanceToOffseason (slot 0x22c, OPD 0x1bcd438, code 0x24ff50); TOC 0x1c64fd0. Status: "static constructor/vtable evidence; runtime dispatch not yet observed".
- Dynasty adapter install `candidate_dynasty_adapter_install`: body 0x2da418..0x2da87b; mfspr LR at 0x2da418; calls ~63 init fns (0x247a5c, 0x237304, 0x2484d8 ... 0x2abb1c) then 0x8d5760.. 0x8d9b60 registration thunks fed from globals 0x1c692dc..0x1c69490; reference at 0x2da5c8 `bl 0x8d6460` (DC constructor.c, instructions.txt, dispatch.json, direct-branch-candidates.json). Singleton at DAT_01c9641c / DAT_01c96418 (vtable 0x18e10e0) via 0x8d6360; global 0x1c96420 read by many .opd FUN_0088xxxx (DO references.txt). Function 0x2da38c sends ("SchoolVsSchool", "ServerErrorOccurred") strings via 0x14059dc using DAT_01c69474 (DO 002da38c.c). Roles beyond that: UNVERIFIED.
- Globals 0x1c75d54..0x1c75d74 (9-word struct) written from a 9-word source in functions 0x4f042c, 0x4f2760, 0x4f4abc, 0x4f6b38, 0x4f7054, 0x4f760c, 0x4f9454, 0x4f9e24, 0x4fa0f0, 0x4fd3c8, 0x4fffb8, 0x503d08, each followed by `bl 0x00a67320` (query) or 0x4e8548/0x470cb4/0x4464fc (DC globals.txt). Meaning of this struct UNVERIFIED (appears to be a query-arguments/record-context block; do not rely).


### 1.B Schedule, conferences, dynasty stage machine, calendar and year

# Digest B: schedule, conferences, dynasty stage machine, calendar/year (NCAA14 BLUS31159)

Scope: prose docs in the private docs folder plus analysis JSON and Ghidra .c files. Read-only digest, nothing was run.
Conventions:
- Addresses are verbatim from the sources. "stock" = stock ELF SHA256 a486a9467c740637892df1fc407d8fea9d92d83cf11ff0de3fe464f934e47abe. File offset = vaddr - 0x10000 (dynasty-start-year.md).
- "CFBR" = College Football Revamped v21 ELF. Its addresses differ from stock; stock to CFBR pairs are given where the docs give them.
- EA-SQL query strings in the ELF store 4-char table/field tags BYTE-REVERSED (season-advance-analysis.md, start-year-2085-rca.md).
  Examples from scheduling-query-strings.json: 'NWES'=SEWN, 'GTHG'=GHTG, 'GTAG'=GATG, 'TADG'=GDAT, 'DOTG'=GTOD, 'MNGS'=SGNM, 'TWES'=SEWT, 'ATSG'=GSTA, 'DNYD'=DYND, 'MAET'=TEAM, 'DIOT'=TOID, 'PYTT'=TTYP, 'DIGC'=CGID.
- Tags: UNVERIFIED = the source itself marks it inference, or I could not confirm it. Source file is cited in parentheses after each fact.
- Abbreviated sources: SI = scheduling-investigation.md, SAA = season-advance-analysis.md, DSY = dynasty-start-year.md, SRR = start-year-rollover-rca.md, S85 = start-year-2085-rca.md, RBY = record-book-year-2026.md, SSP = stock-season-progression.md, R26DL = real2026-data-layer.md, R26V4 = real2026-v4.md, R26RR = real2026-rollover-rca.md, R26CR = real2026-crash-rca.md, R26RS = real2026-runtime-steps.md, CFBR26 = cfbr-real2026.md, ALIGN = fbs-2026-alignment-research-2026-10-09.md, MTM = mode-test-matrix.md, CALM = analysis/start-year-2026/calendar-model.json, XCHK = analysis/stock-progression/crosscheck.json, SHC = analysis/stock-progression/stage-and-history-comparison.json, QSTR = analysis/team-expansion/scheduling-query-strings.json, SEL = analysis/selected-functions/*.c.


General container facts
- Dynasty save USR-DATA is a fixed 8,278,016 bytes (0x7E5000): one TDB followed by zero padding (R26V4 B.2; DSY s7).
- The in-save DB size varies: fresh 3.6 MB, preseason 4.6 MB, in-season about 6.9 MB (R26V4 B.2).
- Compact (alloc 26) tables are saved at FULL capacity once they hold a row (S85 s7.2).
- The constant 0x7e5000 is built from `lis 0x7e` + `ori 0x5000` at 3 candidate sites (DSY s7):
  - 0x334b1c (ori at 0x334b28), 0x335554 (ori at 0x335560), 0x3355d8 (ori at 0x3355ec).
  - Which one (if any) is the real cellSaveData size is UNVERIFIED.
- Template/Roster live in QKL_BOOT.AST: entry 354 = GAMEMODE template (nested), entry 355 = ROSTER (R26DL, CFBR26).
- Schedule data live in QKL_MISC.AST entry 150 ("SCHE", 'QKL_MISC-0150.db') (SI, R26DL).
- Entry 150 is byte-identical to stock in CFBR (CFBR26). CFBR `DLC/qkl_patch.ast.edat` does not override SCHE (CFBR26 / S85 s11).

#### 1.1 SCHD (the Dynasty schedule table, per-game rows)
- Locate: Dynasty TDB table `SCHD`; parse with scripts/inspect_tdb.py `parse_db` (S85 s26, SI).
- Row fields seen in a stock 2014 fixture (XCHK stock-preseason-2014 arizona_games[0]):
  - GSTA, GASC, GHSC, SGID, GTOD, GUTE, GATG, GHTG, SESI, CPCK, HPCK, SGNM, SEWN, SEYR, GDAT, GFOT, SEWT, GFFU, GFHU, GMFX.
  - Sample values: GTOD 1320, GATG 5, GHTG 4, SESI 1, CPCK -1, HPCK -1, SGNM 56, SEWN 13, SEYR 0, GDAT 5, SEWT 13.
- Field meanings the docs state or imply:
  - GHTG = home team TGID, GATG = away team TGID (R26DL "home = GHTG"; query strings above).
  - SGID = stadium id. It is 0 in a fresh-generated schedule and set to a venue (e.g. 115) only when the game is reached with "Sim to this Game" (SI).
  - SEWN = week number (the week-of-season index); SEWT = a running "week total" counter. Both are also SEAI fields.
  - GDAT and GTOD feed the bowl/day placement (DSY s10).
  - GSTA, GASC, GHSC (game status; away/home score): UNVERIFIED. XCHK shows Arizona 8-5 bowl-state rows with GSTA 3, GASC 17, GHSC 49 (XCHK).
  - SGNM = game order number. Query 0x16f3ddc updates it per (SEWN, GHTG, GATG) after ordering by GDAT, GTOD (QSTR 102e3c).
- Row counts:
  - Stock: 809 preseason 2013, 850 week2/bowl/end-season 2013, 778 preseason 2014 (SSP; XCHK table_counts SCHD [850, 931]; capacity 931).
  - Real2026 template SCHD capacity 2048 (R26DL); season-0 plan has 884 games (R26DL), 883 in CFBR (CFBR26).
- Index: `create ... index on SCHD order by SEWN asc` at query 0x16f3c18, built in 102850 (QSTR).
- Counting queries used by the generator:
  - 0x16f31d8 counts games for a team in a week: where SEWN=? and (GHTG=? or GATG=?).
  - 0x16f387c counts a team's total games.
  - 0x16f3810 is the duplicate-pair check (QSTR 102850, SEL 1022c8).
- Games per week is 55 to 64 for the 138-team plan (R26DL).
- 2014 fixtures: SKNW-style presets match 158/169 pairs, 104 with the same week (SI).

#### 1.2 SKNW, SANN, SACC/SBTN/SBTW/SBEA/SCUS/SMAC/SMWS/SPTN/SSEC/SSUN (preset tables inside MISC entry 150)
- Container: QKL_MISC.AST entry 150 equals QKL_MISC-0150.db (SI). Archive SHA256 48d81d6c9e7cbe632793cd285a0474408b38f0773bf3739a26fc3f13772032f4 (SI; truncated "48d81d6c" in R26RS).
- Key field SESI = season slot. Every table is queried "where SESI = season" (query 0x16f38c8 for SKNW, SI).
- SKNW ("known schedule" presets):
  - Logical tag raw 574e4b53 (SI).
  - 1894 rows total: 726 for season 0 (SESI 0), 169 for season 1, declining later (SI). Capacity 1894 (R26DL).
  - Row content: week, home, away, date, time. Query 0x16f38c8 selects week/home/away/date/time from the selected table WHERE SESI=season (SI).
  - Stock fixtures: all 726 season-0 matchups match SCHD in home team, away team and week, in both the stock 2013 and the expanded DEFAULT5 fixtures (SI).
  - No row references prototype TGID 116 (SI).
  - Every original FBS team has presets.
  - One stock row references nonexistent TGID 190 (SESI 7) (R26DL).
- SANN (annual games):
  - Keyed by TGID; SESI = season mod 2 (R26DL). 83 pairs in stock; 79 of 83 SESI-1 rows were in 2014.
  - CFBR left NMSU's and FIU's annual series on TGIDs 61 and 230; 6 rows were moved back to 117 and 116 (CFBR26).
- Per-conference preset tables:
  - Map from 0xfc9c4: CGID 0 SACC, 1 SBTN, 2 SBTW, 3 SBEA, 4 SCUS, 7 SMAC, 9 SMWS, 10 SPTN, 11 SSEC, 13 SSUN (R26DL).
  - Real2026 slices/rows/capacity: SACC 9/612/672, SBTN 5/405/480, SBTW 2/144/180, SBEA 3/168/180, SCUS 2/90/447, SMAC 4/208/208, SMWS 2/90/192, SPTN 2/56/432, SSEC 9/648/672, SSUN 2/112/112 (R26DL).
  - Stock ACC and Big Ten slices are 8-/9-regular and equal the caps 68/81 (R26V4).
- Season-to-slice rule:
  - Season 0 = SKNW SESI 0 plus SANN SESI 0.
  - Season s >= 1 = table SESI = s - floor((s-1)/max)*max, i.e. slice 1 + (s-1) mod max(SESI) (R26V4 A.1; query strings 0x16f32c4/0x16f3548).
  - Presets are keyed by season INDEX, not calendar year (DSY s4).
  - There is NO bounds check against the cap. A slice larger than count(SESI 1) overruns the game array (R26V4 A.1).
- Other tables mentioned in DSY s4 / R26V4: SACC, SBTN, SBTW, SBEA, SKNW, SANN, "SBTN" in QKL_MISC150 (also "SBTW/SBEA" etc. above). Exact SCHE table list beyond these: UNVERIFIED.
- Where the first-year data come from: the first-year schedule is mostly PACKAGED presets (726 matchups in SKNW season 0), not executable-embedded (SI).

#### 1.3 QKL_MISC entry numbers
- QKL_MISC.AST entry 150 = SCHE (SKNW/SANN/Sxxx) (SI, R26DL).
- QKL_MISC entry 145 = BOWL field list (referenced in DSY s1: "QKL_MISC entry 145 (BOWL) field list (graphics-asset-pipeline.md)"). The BOWL table is also edited in BOOT entry 354 by the playoff patches (R26DL s5.9). UNVERIFIED which copy the game serves.
- QKL_BOOT entry 354 = GAMEMODE template; 355 = ROSTER; CFBR BOOT is `entry-0006-qkl_boot.ast`, MISC `entry-0009-qkl_misc.ast` (CFBR26).
- CFBR "827 entries, only 354/355 differ" (CFBR26).
- INTERFACE movies (not MISC): 338 CoachContract, 155 HubStrategy, 119 Dynasty60Year popup, 315 Advance, 367 StoryStrategy, 500 post-sim notifications, 604 main menu, 605 library (S85).

#### 1.4 Conferences and alignment tables (GAMEMODE template entry 354 / roster entry 355)
- TEAM: fields named in the docs:
  - Identity: TGID, TOID, TORD, TDNA (22 bytes), TLNA (17), TSNA (7), TMNA/TMNC (18/17), TMCC.
  - Classification: CGID (conference), DGID (division), TTYP (0 = FBS, 1 = non-FBS), LGID, SGID (stadium), TMCP (must equal the head coach CCID).
  - Rankings: TCRK/TMRK/TBRK (coach poll / media poll / BCS rank), TVIS, TRIV (rival).
  - Title history: NCYN (national title count), NCYR (title year code), FCYR (conf title year code), ATTY (attendance record year code).
  - Presentation: CSAT, TSID, TCID, TGRP, TGPT, MSID, TSWI/TSLO (wins/losses this season) (R26DL, CFBR26, XCHK).
  - TEAM capacity in template 192; roster TEAM 154/192 (R26DL).
  - Dynasty creation renumbers FBS TORD to 1 + ASCII rank of TDNA (R26CR).
  - Dynasty creation deletes FCS depth charts and moves FCS coaches to TGID 1023 (R26CR).
  - Team indexes come from sorting by TORD (R26DL).
  - The all-team list (0x1c76898, count 0x1c768a0) is built by 0x472910 as `TEAM where TGID<=1006 [and TVIS=1] order by TORD` (R26CR).
- CONF: 14+ rows; CGIDs: 0 ACC, 1 Big Ten, 2 Big 12, 3 American, 4 C-USA, 5 Independent, 7 MAC, 9 MWC, 10 Pac-12, 11 SEC, 13 Sun Belt, 14 WAC (empty), 17 Generic (R26DL).
  - CGID 6, 8, 12 are not described in the docs: UNVERIFIED.
- DIVI (divisions): DGID 4/5 SEC East/West, 12/13 Big 12 "Div A/B", 14/15 American "Div A/B", 2/3 MAC East/West, 16/17 Sun Belt (renamed East/West), pseudo-divisions ACC 6/7, Big Ten 10/11, DGID 30 = none. DIVI 22/22 rows (R26DL).
- CSST (conference style, one row per scheduled conference): fields CGID, STNA (style class name string), RVPF (protected-rivals flag). 8 rows edited in real2026 (R26DL); 6 edited in CFBR (CFBR26).
- CNFR: 14 rows. RUID 6..13 = protected-rival pairs; RUID 14 field CRV1 selects the table path (0 = table). Read by 0xf9a74 via query 0x16f29f8 (R26DL, R26V4).
- SCRT: per-conference member slots (16 per conference), fields TIDR|TGID, SLNU, CGID.
  - Read by 0xfdcc0 with query 0x16f34ec `select TIDR|TGID from SCRT where CGID=? order by SLNU`.
  - If any of the first n slots is 0, falls back to 0xfdbdc (`TEAM where CGID=? order by TORD`, query 0x16f348c), which has no 16-slot limit.
  - Real2026 zeroes the 119 non-empty SCRT rows of the 10 scheduled conferences (R26CR, R26V4, CFBR26).
- STTM: per-team standings; STTM.CGID/DGID equal TEAM's. Used by the CCG pairing cursor `STTM join TEAM where STTM.CGID=? order by TEAM.tscs, TEAM.TSDS` fetching (TGID, STTM.DGID, SNCT) (R26DL, R26CR).
- CCHH / BCHH: see 1.6.
- Style classes (vtables, slot 25 = schedule) (R26V4 A.1):
  - EvenDivsNoProtectedRivals 0x188e130 / 0x10392c
  - EvenDivsProtectedRivalsLessConfGames 0x188e1c8 / nop
  - EvenDivsProtectedRivals 0x188e270 / 0x104764
  - NoDivsAllConfOppsPlayed 0x188e308 / 0x104b64
  - NoDivsMiniConfForcedFcsGames 0x188e3a0 / 0x104fc8
  - NoDivsProtectedRivals 0x188e440 / nop
  - NoDivsRotatingGames 0x188e4d8 / 0x105ec0
  - EvenDivsOverlappingGames 0x188e570 / 0x1062cc
  - UnevenDivs 0x188e608 / 0x106af0 (plus 0x106e2c for n = 15)
  - UnevenDivs registry address also stated as 0x188e676 in R26CR open items (UNVERIFIED which is correct).
- Engine CCG gate (0x45c7e0 / 0x45b484): row active only if BCI1 < 14, the conference has >= 12 teams with TOID=TGID, and CGID != 5 (R26DL). Each active conference needs 2 non-empty DGIDs or the CCG loop at 0x45b484 hangs.
- 2026 conference table (R26DL): ACC 17 (8 conf games), Big Ten 18 (9), Big 12 16 (9), American 14 (8), CUSA 10 (9), Independent 2 (0), MAC 13 (8), MWC 10 (9), Pac-12 8 (7), SEC 16 (9), Sun Belt 14 (8).
  - The CFBR sum is checked: 17+14+18+16+10+13+10+8+16+14+2 = 138 (ALIGN).
- Stock TGID/TOID/TSNA for retained schools are tabulated in ALIGN (baseline fixture stock-preseason-2013-MODBASE USR-DATA sha ba8f22c78e588eddd24df95239c191a9f67395c9d56fcd9d1e3bc751cce6f45b: 131 teams = 126 TTYP 0 plus 5 generic FCS).
- Real2026 additions (stock build): TGID 116..128 (App State 116, Charlotte 117, Coastal 118, Delaware 119, GaSo 120, JaxSt 121, JMU 122, Kennesaw 123, Liberty 124, MoSt 125, NDSU 126, Sac St 127, Sam Houston 128) (R26DL).
  - CFBR TGIDs differ (e.g. 34 = App State, 116 FIU, 117 NMSU, 118 UConn, 119 Delaware, 120 UMass) (CFBR26).
- Idaho (stock TGID 34) is moved out of FBS in the v1/v2 build (TTYP 1, CGID 17, TORD 433) and REMOVED entirely in v3 (R26DL, R26RR).
- Generic FCS teams = TGID 160..164 (stock). Dynasty teams: 143 = 138 FBS + 5 generic FCS in v3+ (R26RR).
- SI active127 prototype: TGID 116 clone of Idaho, TOID was 34 (collided with Idaho) and was changed to 116 by BOOTv3 (SI).

#### 1.5 Dynasty object / stage machine
SEAI (season info, 1 row) fields as saved (SHC, XCHK):
- SNPB, SERB, SSYE, SSTG, SESI, SEWN, SNCP, SNDP, SEFP, SNWP, SEYR, SEST, SEWT, SEOW, SGOW, SNPW, SBRW, SERW, SFRW, SESW.
- Observed values in the 2013 stock Dynasty: SERB 3, SSTG 1, SEFP 15, SERW 15, SNPW 7, SEOW 22, others 0 (SHC).
- Per-fixture SSYE/SEYR/SEWN/SEWT (SHC, XCHK, SSP):

| Fixture | SSYE | SEYR | SEWN | SEWT |
|---|---|---|---|---|
| preseason 2013 | 0 | 0 | 0 | 151 |
| week 2 2013 | 0 | 0 | 1 | 1 |
| bowl entry 2013 | 0 | 0 | 17 | 30 |
| end of season 2013 | 0 | 0 | 22 | 150 |
| preseason 2014 | 1 | 1 | 0 | 151 |

- SSYE = season INDEX (0,1,2...), 16 bits, never a calendar year. Query `select SSYE from SEAI` at 0x175fe14; getter 0x4453e4 (also seen as 0x443f24 in one check) (DSY s1,s9).
- SEYR = history-year index, 6 bits (0..63) in 22 tables. In SEAI it mirrors SSYE up to the clamp at MNSE-1 (S85 s4,s16).
- The offseason keeps the index of the season just played: SEWT 150 at SSYE n. The index rises only at Pre-Season (SEWT 151) (S85 s15.2).
- SEOW 22 / SNPW 7 / SERW=SEFP 15 / SERB 3 / SSTG 1 / SESW=SNWP=SNDP=SNCP 0 are the "stage-week fields". They are identical in 2026-start and 2013-start saves and are recomputed each season by 0x4d893c/0x4d8ba8 (SRR s4 1b, DSY s10).
  - Field-by-field meaning is UNVERIFIED (SAA: "Map stage query fields... remaining proof").
- SESI in SEAI = schedule-slot index (0 in the fixtures); used for table "where SESI = season" (UNVERIFIED relation to SSYE).
- MOIN (mode info, 1 row) fields: MCSA, MPSA, MISB, XUID, MONE, MNAI, MIMI, ACEN, MTYP, UDFS, MSTY.
  - MCSA: 4 at preseason 2013, 7 at week2/bowl/end-season. MPSA: 3 then 6. Meaning UNVERIFIED (SSP says "do not substitute UI labels").
  - MIMI 55854434, MTYP 2 in all fixtures.
  - MCSA/MOIN query tags are read as 'ASCM' from 'NIOM' at 0x43cd14 (SAA).
  - Stage writer 0x4fa820 writes MOIN.MPSA/MPSC; reached through stage-table entry 0x1c88ba4 (S85 s16).
- MOPT.MNSE = Dynasty length, 8 bit, 60 in every fixture. Set at 0x214da8 (`li r4,60`, field 'ESNM'); read in only two places: 'ESNM' query 0x178ac70 and tag at 0x4d8d90 (S85 s4).
- Stage callback table: offseason stage table at 0x1c88ca4 (SRR s2, per-stage callbacks 0x5012fc etc.). Callback descriptor pointer 0x1c75d70 (holds 0x1bddef0 -> code 0x50416c at the 2014 preseason snapshot); twelve writers copy callback bundles into 0x1c75d54..74 (SAA).
- Dynasty adapter object: global 0x1c96420 and 0x1c69308 both point to heap 0x100cf960; vtable 0x18971c0; TOC 0x1c64fd0 (SAA). Another global: adapter object pointer `*0x1ca64a0` and vtable `0x189a750` set by constructor 0x2494a0 (S85 s15.1).
- Year bases (no data field): see section 1.7.
- TSHS (team-season history, 4 bytes/row), BCHH (bowl+NCG history, 4 bytes), CCHH (conf-champ history, 4 bytes), CREP (8 bytes): keys are raw SSYE (not clamped SEYR); never pruned (S85 s7.1).

| Table | Fields | Old cap | New cap (dyn60) | Per-season growth |
|---|---|---|---|---|
| BCHH | TGID, SEYR, BIDX | 2040 | 2944 (46 BOWL x 64) | +34 (33 bowls + NCG) |
| CCHH | CGID, TGID, SEYR | 600 | 1664 (26 CONF x 64) | +10 |
| TSHS | TGID, SEYR, WINS, LOSE | 7560 | 10240 (160 x 64) | +138 FBS rows/season |
| CREP | per coach CCID | 640 | 1280 | +6.3 (138) / +13.2 (126) |

  - BCHH/CCHH row layout also: (S85 s7, XCHK). TSHS insert `TSHS (TGID, SEYR=SSYE, 0, 0)` at 0x1783edc, loop 0x4d57f0 -> 0x4d5768. BCHH insert 0x1789560 at 0x4eefa4 (weeks 30-40). CCHH insert 0x1768be4 at 0x4ef054 (week 16). Select `WINS, LOSE from TSHS` 0x1789508 at 0x4eee84.
  - TPHS (8 B): 572 stock / 720 v4; rolling delete at SEYR = SSYE-4 by FUN_004ecce8 (DSY s5; R26V4 B.1).
  - RBKS (112 B): 3643 stock / 4320 v4. PLAC (20 B): 3208 / 4100. TPRC (4 B): 750 / 900 (R26V4).
- Dynasty length wall: BCHH 2040/34 = 60 and CCHH 600/10 = 60 (DSY s4).
  - The CODE gate is the native predicate at 0x539aa4 (see 2.4, patch len60).
- Record book: see 1.8.
- Template tables PTIP/MCOV/RCTC/TEXP/TSSE/RTPB/DCHT/PLAY: capacity sized for 138 FBS (R26DL). Allocation-10/2 tables (AAPL, NEUT) have spare capacity in stock (R26V4).
- Team history tables TPHS/TPDA etc: TPDA rows scanned in full at 0x17889fc (R26RR).

#### 1.6 Postseason/champion tables
- BOWL (template entry 354 and/or MISC 145): fields BIDX, BNME, BMON, BDAY, SGNM, SGID, SWPE, GTOD (play-time), UTID (trophy id), BCI1. 354 BOOT playoff rows: FR 12/11, QF 12/25, SF 1/1, final 1/6 (DSY s10, CALM playoff_dates).
- NCG BIDX 39; CCG rows 33..44; FR 29..32 (SGID 166/185/186/251, SWPE 1); QF 25..28; SF 12 and 17; final 39 in CFBR (CFBR26 s4).
- BCS function 0x4ca8a0 takes N; points = (127 - rank) unsigned (R26RR s2).
- NCYR (TEAM): 10-bit; stock formula SSYE + 0x107 (263), shown as code + 1750. Ohio State NCYR 252 -> 263 after the 2013 title (SHC, DSY s1b). NCYN 7 -> 8.

#### 1.7 Calendar / year handling (no base-year data field)
- No "base year" row in BOOT/MISC/SEAI/BOWL/TEAM schemas (DSY s1, s3).
- NCAA_RELEASE_YEAR is a UI constant in an APT movie (asset key df67693bd6f8c1fd, 108,834 bytes). Literal PushShort `b6 07 dd` (2013) at decoded aptdata 0x6e99. NCAA_TITLE_YEAR = NCAA_RELEASE_YEAR + 1 (S85 s6.1).
  - Four copies: BOOT 755, FE2IG 2565, INTERFACE 459, and DLC/qkl_patch.ast.edat entry 28 (the served one) (S85 s11).
- Three native year encodings (DSY s9):
  - Calendar year = SSYE + 0x7dd (2013); also +0x7dc (previous season, 2012) and +0x7de (next season, 2014).
  - Stored title-year code (TEAM.NCYR / FCYR / ATTY, 10-bit) = SSYE + 0x107 (263), shown as code + 1750.
  - Decoders use code + 0x6d6 (1750).
- G0 = half-word at 0x1c787a0 (day anchor), written only by 0x4d863c(year, G1). G1 = byte at 0x1c787a2 = max(SEWN where SEWN < 16) + 1 from 0x4d8760 (DSY s9). Readers: 0x451158/0x451224 (G1/G0) (DSY s9).
- Calendar helper functions (DSY s10, CALM model_source): 0x4a1b58 weekday (Zeller, Monday=0); 0x450f88 days-in-month (month table 0x175dc74 plus Gregorian leap test); 0x4d8760 (G1); 0x4d863c (G0); 0x45c89c (bowl placement); 0x45146c (current-week date); 0x451020 (G0-relative day).
- Week formula: week = ((doy - G0) + 1) * 0x9249 >> 18 = floor((doy - G0)/7). Resulting SEWN = 16 + (weekday(Dec 1) + days_after_Dec_1) // 7, 16 bumped to 17 (DSY s10).
  - Extra rules: January rows with BDAY > 1 early in the week move back one week; NCG (BIDX 39) with BDAY <= 7 moves forward one week when weekday >= BDAY-1; CCG rows keep SEWN 16 and get SEWT 16 and GDAT 5.
- CALM structure: keys elf_sha256, model_source, validation{passed, fixtures[13]}, g1_used (15), base_fixture, playoff_dates, playoff_2026_2085{seasons[60], patterns, ...}, alternative_dates_fr_dec8_qf_dec22_sf_dec29_final_jan5, dec1_sunday_seasons_general_rule, quirk_cmpwi_0x4d8654, stock_bowls_first5, stock_bowls_max_sewn_2026_2085.
  - Per-season entry: ssye, year, G0, dec1_weekday, first_round, quarterfinal, semifinal, final, final_sewt, max_sewn, ccg_saturday, sewn0_saturday, sewn1_saturday, last_regular_saturday, ok.
  - Example 2026 (ssye 0): G0 236, dec1_weekday 1 (Tue), FR 17 / QF 19 / SF 20 / final 21, final_sewt 40, max_sewn 21, CCG Sat 2026-12-05, SEWN 0 Sat 2026-08-29, SEWN 1 Sat 2026-09-05.
  - Stock week2 2013 fixture: G1 15, G0 238, 41 active BOWL rows; sewn rows 29/25/12/39 -> 18/20/20/21 (CALM validation).
  - Mon-Thu Dec 1: 34 seasons, 17/19/20/21. Fri-Sun: 26 seasons, 18/20/21/22 (CALM).
  - quirk_cmpwi_0x4d8654.differing_seasons is empty (CALM).
- G0 first-5-season table in DSY s10: SEWN 0 Sat Aug 29 (2026), Aug 28 (2027), Aug 26 (2028), Aug 25 (2029), Aug 24 (2030).

#### 1.8 Record book (RBKS / RBKN)
- Table RBKS (school records, 112 B/row, 3643 stock cap, 3402 used at stock = 126 x 27 with RCDT 0/1/2 x 9) and RBKN (NCAA records) (R26V4, RBY).
- Field RCDD (32-bit) = (year - 1900) << 9 | month << 5 | day. Holder text RCDH uses "%d %s" from (RCDD >> 9) + 1900 (RBY s1).
- Date build: function 0xdbf38 (RBKS, school records) and copy 0xd8dd8 (RBKN). Caller 0xdc2f0 passes the value to the RBKS insert/update 0xdbcb0; holder text formatted at 0xdc31c.
- Encoder (stock before patch): `ori r4,r4,0xe200` = 113 << 9 (113 = 2013 - 1900); `ori r3,r3,0x19f` = December 31. Year code is SSYE + 113; SSYE obtained via `bl 0x4453e4` at 0dbf68 (RBY).
- Decoders mask `(RCDD >> 9) & 0x8fffff` (RBY).
- The 2013-only constant was missed by the earlier 0x7dd/0x107/0x6d6 scan (DSY s9 note).

#### 1.9 GAMEMODE template tables TSHS/BCHH/CCHH/CREP
- Live in BOOT entry 354 (the GAMEMODE template). The saved Dynasty inherits `max_records` at creation (S85 s26, s26.1): capacity is fixed per save and cannot be retrofitted by start_year_seyr_edit.py.
- Verified at runtime: a fresh Dynasty "CAP60" created under dyn60pc-len60 holds TSHS 138/10240, BCHH 0/2944, CCHH 0/1664, CREP 0/1280 (S85 s26.1).
- Tables with 6-bit SEYR (22): SEAI, BCHH, CCHH, TSHS, TEAH, TSWP, TRGA, TRSE, TPRC, PLAC, OSPA, AAPL, six PSxx stat tables, SCHD, SCHT, NESG, NEUT (S85 s16.1).
- NESG/NEUT (season-keyed neutral-site slates) have rows for SEYR 0..59 and 63 only (S85 s16 option b).
- CBS/other "TPHS/BCHH/CCHH/CREP" per-team stat history: NCYR formula above.

#### 1.10 Dynasty length / "NCAA_RELEASE_YEAR"
- MOPT.MNSE = 60 (see 1.5). Predicate 0x539aa4 `DynastyAdapter::GameJustFinished60YearDynasty`: `select SSYE from SEAI` (0x1763138), `addic r3,r3,1; cmpwi r3,0x3c; bne; li r31,1` at 0x539adc..0x539ae8 (S85 s15.1).
- Stock allows seasons index 0..58 (59 played seasons); hub refuses Start Season at Pre-Season index 59 (S85 s15.2).


### 1.C Rules, playoff, coach, news, UI, stats (CFBR addresses for rules; playoff/news/coach mix stock and CFBR, see 2.6)

### PART A. MODERN RULES (OT, clock, PAT/2pt, timeouts)

#### A1. Data structures (where rule values/state live)
- Rules registry global `0x1cac994` (ClockRules, EndPlayRules, pointsrules, OT-rules hang off it). `0x1cac994 -> +0x1c` = OT-rules object (OTR). `0x1cac994 -> +8` = live game-state object used for set-spot/down/line-to-gain vtable calls. [MRD 2.1]
- Game state global `0x1cac7b8`: `+4` quarter (1..4, 5=OT, 6=final); `+0x18 -> +0x1c` game clock (f32 s); `+0x14` play clock. Pending spot adjustment `0x1cac7ac -> +0x80`. `0x1cac7bc` slot 0x15c = OT intro/camera. [MRD 3.1, 7.2, 2.3]
- OTR (NCAA class): vtable `0x192d430`, factory `0x111f7d8`, base ctor `0xd539b0`. Fields: `+0x08` type (3); `+0x0d` OT period (u8, 1-based); `+0x10` series (0 FIRST, 1 LAST, 2 COMPLETE->0xff); `+0x14` first period that requires a 2pt try (stock 3; set by `li r4,3` at 0x111f82c, stored `stb r4,0x14(r31)` at 0x111f83c); `+0x18` possession start spot f32 (25.0); `+0x1c/+0x1d` per-team flags. [MRD 2.1]
- OTR vtable slots: 0x24 period (0xd53a70), 0x2c period++ (0xd53a80), 0x30 series (0xd53a90), 0x34 set series, 0x38 series advance (0xd53aa4), 0x3c possession setup (0x111e480; slot word at 0x192d46c), 0x40 set spot (0x579fd0), 0x44 two-point-required predicate (0x111e538: quarter==5 && period(+0x0d) >= +0x14), 0x48 first possession (0x111e56c). [MRD 2.1]
- Stock descriptor for slot 0x3c: `0x1c5d620 = {0x111e480, 0x1c75050}`; TOC 0x1c75050 used by all cave descriptors. [MRD 2.3, 7.2]
- Field coordinates: yards past midfield toward attacked goal: 25.0 = opp 25, 47.0 = 3-yd line, 50.0 = goal line. Down enum string table `0x17a1e40`: 0..3 = 1st..4th, 4 = PAT, 5 = kickoff. NCAA FieldRule `0x111f91c`: PAT spot 47.0 (`lis 0x423c` at 0x111fa64), kickoff -15, touchback 25. [MRD 2.1]
- Game-state vtable slots used: 0x70 read down, 0xf0 set spot, 0x100 set line-to-gain, 0x104 set down, 0x180 goal. [MRD 2.3.1, 7.2]
- ClockRules: base vtable `0x1905a80`, NCAA vtable `0x192d290`, ctor `0xd33c28`, NCAA instance `0x111dde0`, config built by `0x111dc28`. Flags at +0x1c via slots 0x14 test / 0x18 set / 0x1c clear: flag0 start-on-snap, flag1 start-on-ready, flag2 two-minute warning given, flag9 timeout since snap; slot 0xc4 = stop until snap. [MRD 3.1]
- NCAA clock config (0x111dc28 -> copied by 0xd33c28): +0x04 900.0 quarter length; +0x08 =0 two-min warning enabled (ClockRules +0x44); +0x0a =3 timeouts/half (+0x46); +0x0e =1 first-down-stops-clock (+0x4a); +0x11 =1 late-game runoff (+0x4f); +0x14/+0x18 40.0/25.0 play clocks (+0x58/+0x5c); +0x24/+0x28 2.0/2.0 OOB-restart thresholds (+0x68/+0x6c); +0x2c =0 (+0x70). [MRD 3.1]
- Timeouts: ClockRules +0x38/+0x3c decremented by slot 0xa8 (0xd378dc); caller 0xd6bd90 ignores return and stops clock; snap handler slot 0x24 (0xd34aac) clears flags 0,1,3,5,8,9. SuperSim adapter slot 0xb0 sets timeouts (0x12f278). [MRD 3.1, 5]
- SuperSim::GameRules (object 0xa6f0a0, config built at 0x3665a0): quarter 900.0; +0x4 =1 college mode; +0xc goal LTG; +0x34 two-min threshold (0 for NCAA; `stw r29,0xc8(r1)` at 0x366794); +0x50 PAT spot 47.0; +0x60 LTG 10 yd; +0x6c points table; +0x74 =1 point (score config [6,3,1,2,2,2,1] at r1+0x100.., ctor 0xa6f1c0/0xa6f1d0); +0x8c OT spot 25.0; +0x9c OT type 2 EQUAL_POSSESSIONS. [MRD 3.1, 5, 9.3]
- SuperSim state: quarter `+0x528`, clock `+0x548`, `+0x534` down of last play. Result struct: [1]=down, [2], [3]=spot, [4]=LTG, [5]=new-possession flag, [11]; stock TD->try writes [1]=4,[2]=0,[3]=GameRules+0x50,[11]=0. [MRD 2.3.1, 7.2]
- SuperSim adapter vtable `0x1892980`: slot 0x14 quarter; 0x20 OTR period (0x12e0bc); 0x2c set OT series (0x12e1b0); 0x44 clock state from flags (0x12e468); 0x48 write clock state (0x12e590: 0 clear flags, 1 flag1, 2/3 flag0, 4 running, 5 zero); 0x5c flag2 read; 0x90 spot; 0x98 LTG; 0xa0 down; 0xb0 timeouts; 0xbc spot adj; 0xc0. [MRD 5, 7.3]
- Situation object vtable `0x192da78`: key 0x26 = OT period, set by 0x1118d90 only while predicate true; exposed to AI scripts as GETOTCOUNT (binding 0x1118abc, name string 0x17af520, getter 0x1118b30). [MRD 9.2]
- NCAAPlaybookMgr: vtable `0x18ff0c0` slot 0xc = 0xde8e1c (wrapper 0xab8d1c), ctor 0xab5144 (init 0x361394), global `0x1cad75c` (0xde7d58). [MRD 5.1]
- NCAA pointsrules vtable `0x192d4e0` (slot 0x4c at 0x192d52c = add-points; stock descriptor 0x1c37850 -> 0xd548fc). [MRD 9.3]
- Offline DB: no OT rule tables. GOPT/SOPT/MOPT read from BOOT 359 / MISC 145; GINF/SCHD/SGIN carry results only (SCHD GFOT=1 marks OT game). AI scripts compressed in qkl_*.ast (not read). [MRD 9.2, 6.0]
- Tail code room (segment-0 tail beyond p_filesz): rules cave base 0x1bc2a00, region [0x1bc2a00,0x1bc4000); CFP news cave ends 0x1bc29cc; playoff campus cave 0x1bc4000; projection cave 0x1bcff00; 54,784 B left after ot-v1. [MRD 2.3, 4, 7.2]

### PART B. PLAYOFF (stock engine map, proto v0/v1/v3) -- PEM = playoff-engine-map.md, V0 = playoff-proto-v0.md, V1 = playoff-proto-v1.md, V3 = playoff-proto-v3.md

#### B1. Data structures
- **BOWL table**: Dynasty template DB `QKL_MISC` entry 145 (`analysis/assets/QKL_MISC-0145.db`), copied into each save's leading TDB. 45 rows, capacity 45/45 (full). Fields/bit widths: BIDX 8, BNME 232, BCI1 5, BCR1 4, BCI2 5, BCR2 4, BMON 4, BDAY 5, GTOD 16, SGID 10, SEWN 5, SGNM 8, SWPE 1, BMFD 16, BLGO 16, BPLO 6, UTID 7. Template SEWN=31 / SGNM=127 = unassigned sentinels; CCG rows carry SEWN=16. [PEM 1]
- **BUT**: a NEW Dynasty does NOT read MISC 145; it reads **QKL_BOOT entry 354 (nested GAMEMODE)** (runtime-proven via docs/archive-template-test.md A/B). Nested BGFA in 354 has a 1-byte offset field (framing `01 00 08 01 03 03 03 00`), so `bgfa_archive.replace_entries` cannot append; rebuilt in place (payload at offset 120, only entry 0's packed/extra size bytes change); outer archive has 827 entries, entry 354 replaced (append 16-aligned, repoint). [V1 1, 3]
- BIDX roles (hard-coded in code): 0..32 = 33 bowls (25..28 = Rose, Fiesta, Sugar, Orange = BCS); 33..44 except 39 = conference championship games (BCI1=BCR1=CGID/1); 39 = BCS National Championship (BCI 17/0). BCIn = conference CGID, BCRn = finishing place; BCI=17 Generic with BCR=0 = at-large/NCG. CCG rows in r26c: 33 Pac-12, 34 MAC, 35 SEC, 36 ACC, 37 C-USA, 38 Big Ten, 40 Big 12, 41 American, 42 Sun Belt, 43 WAC, 44 MWC (BCI1 = CGID; BIDX 39 BCI1=17). [PEM 1, V3 4]
- SCHD (stock 2013, 850 rows): SEWN 0..14 regular; 15 empty (skipped); 16 CCGs (SEWT 16, 7 games, SGNM 0..6); 17 (SEWT 30, 2 bowls, SGNM 7..8); 18 (SEWT 31, 4 bowls 9..12); 19 (SEWT 32, 12 bowls 13..24); 20 (SEWT 32, 15 bowls/BCS 25..39); 21 (SEWT 40, NCG SGNM 40). Postseason SGNM is one sequence across postseason weeks; regular-season SGNM restarts per week. Game key = (SEWN, SGNM). SCHD placeholders: GHTG=GATG=1023 (0x3ff), GSTA=1 unplayed; GSTA 3 = home won, 2 = away won. Fields seen: SEYR, GHSC, GASC, GSTA, GHTG, GATG, GFHU, GFFU, SGID, GTOD, GDAT, GFOT. [PEM 1, 2]
- SEAI (season state): SEWN, SEWT, MCSA (4 preseason, 7 in-season), SEOW=22, SERW=15. SEWT 150 offseason/151 preseason. [PEM 1]
- History: BCHH (winner TGID, SEYR, BIDX) 34 rows after bowls; CCHH (TGID, SEYR, CGID) 10 rows; team NCYN (national titles) 7->8 and NCYR = SSYE+0x107 (263; 1750+263=2013); CBOW/CBOL bowl W/L. [PEM 1]
- SCWE (25 rows PPRD/SEWN/PRAR/SEST): no query string in ELF; role unknown (probably recruiting periods) [INF]. [PEM 1]
- Cave working globals: `0x1ce98d8` (33 bowls x 2 slots), used list `0x1c765f4` (count byte `0x1c7672c`), BCS list `0x1c7658c`; CCG winner table `0x1ce9860`; live FBS count `lhz 0x1c768a2` (126 stock, 138 under activeN); progress callback `*0x1c75d28` (+0x1c75d40); bowl year rotation table `0x175aadc`; win% constant `0xbc370`. [PEM 2, V0 2/7]
- Stock queries (EA-SQL strings): 0x1763c54 TEAM TGID by TBRK; 0x177e378 TEAM CGID,tscs by TGID; 0x1776368 TEAM TBRK by TGID; 0x1763b40 BOWL SGNM,SEWN by BIDX; 0x17641cc SCHD GHTG,GATG by SEWN,SGNM; 0x1775670 SCHD GSTA by SEWN,SGNM; 0x16dad3c TEAM SGID by TGID; 0x17640cc BOWL SWPE by SGID; 0x1764104 update BOWL SGID,SWPE; 0x1764144 update SCHD SGID; 0x1764ddc BOWL SGNM where BCI1 and SEWN=16 (Q_CCGSG, used by 0x45da10 at 0x45dc78..0x45dc98); 0x1764e24 SCHD teams/scores/GSTA; 0x17658f4 CCHH insert (at 0x4edc04); 0x176392c/0x176396c SEWN 16 cursor; 0x1763be8, 0x176475c, 0x1775cd4 BOWL/SCHD texts (CFBR anchors); query wrapper 0xa67320. No select query on CCHH exists in ELF. [V0 2, V3 2.1, PEM 5]
- Rankings: TBRK/TBPR written by BCS ranking 0x4ca8a0 (team count `li r4,0x7e` = 126 hard-coded at 0x4cea2c, activeN changes to 0x8a = 138; also 0x4cea3c). Ranks frozen during bowl weeks until final poll [INF]. Other callers of 0x4ca8a0: 0x1e0a50, 0x2d8748, 0x2fbbd0 (unknown whether they recompute TBRK in bowl weeks). Team fields: tscs (conference standing), SNCT, CGID, TGID, TOID, TTYP, TBRK. [PEM 2, 6; V0 2, 7]

### PART C. COACH / CAROUSEL / CONTRACTS -- src: coachless-carousel-rca.md (CCR); analysis\coachless\*.json

#### C1. Data structures
- Tables: CONT (coach contracts; fields seen: CNID contract id/row, CCID coach id (0xffff = none), TGID, COPS (position: head coach / OC / DC; free pool by COPS 0,1,2), CCIE, CIEX (extension flag), SIND (current=1, opening row SIND=0), CAGE?). COCH (coaches; fields seen: CCFY contract-final-year, CAGE age, CFUC user-coach flag, CPRF/CSKL prestige/skills, CNTW national titles, CBLW/CBLL bowl W/L, TGID (1023 = unemployed/released)). TEAM (TGID, TTYP). Other: SSYE season start year. [CCR 1, 3]
- Capacity facts: CONT 960 entries capacity; CONT occupancy max seen 694; current contracts = 3 per team (HC/OC/DC) in TEAM order: 126 teams -> 378 contracts, 138 teams -> 414 contracts (added teams TEAM rows 126-137 -> CONT rows 378-413). COCH 433/768 after rollover. CFBR has 234 CCFY-0 coaches of its own; 29 of 36 added-team coaches inherit CCFY=0 from donors (all 24 added coordinators + 5 head coaches: FIU, New Mexico State, UConn, Kennesaw State, Sam Houston; other 7 added HCs have CCFY 1-6). [CCR 1]
- Root cause: contract pass CFBR `0x4d8a3c` / stock `0x4d7814` copies current contracts (query "select CNID, CCID from CONT where CCID != 0xffff") via `0x4d8870` into a 378 x 20-byte stack array (r1+0x8c, frame 0x1e70, `li r4/r5,0x17a`) and processes only 378 -> skips 36 contracts every year at 138 teams (stock too from year 2 on, ~13-36 random teams). Expiry release (CFBR `0x4fc70c` / stock `0x4fae3c`; "CONT join COCH where CCFY <= SSYE and CFUC = 0") then releases (TGID/CNID 1023) CCFY<=SSYE coaches including the 29 unaged ones, leaving 29 zombie CONT rows (CNID 378-413) so opening creation `0x4d48d4` (insert CONT SIND=0 row only if count(CONT where TGID, COPS, CCIE=0, CIEX=0)=0) never opens those seats; hire loop `0x4d20f4` (-> `0x4d1b18` / `0x4d14e8` generate coach) iterates openings only. Result: coachless teams [116,117,118,123,128] after rollover in both CFBR 2013 and 2026 runs (all 12 added teams lack OC and DC). Crash if coachless team reaches recruiting boards: access violation at `0x4c1c2c` (`0x4b83d4` scheme-table row). [CCR 1-3, 7]
- Functions (CFBR / stock): 0x4d8a3c / 0x4d7814 yearly contract pass (sub: 0x4d8870 fill, 0x4d84b0 age/years, 0x4d8118, dispatch 0x4d3528 / 0x4d6d88); 0x4fc70c / 0x4fae3c expiry release (378 x 4 B at r1+0xac, no bound check, frame 0x6e0); 0x4fc8bc / 0x4fafec extension pass ("CONT where CIEX = 1" -> 0x4d3778; 378 x 8 B; frame 0xca0; memset 0xbd0); 0x4fccbc "Updating Coach Contracts" stage (offers <=0x20 rounds -> 0x4fc8bc -> delete CIEX=1 -> 0x4fc70c -> CFBR-only 0x4fb8ac); 0x4d5850 -> 0x4d48d4 opening creation; 0x4d20f4 -> 0x4d1b18 / 0x4d14e8 hire loop (2 openings per call; CFBR adds vector bound in 0x4d1b18); 0x1c41ec (UI arg 0x17a) and 0x2d3118 other 0x17a hits unreviewed; activeN Coach Stability sort epilogue near stock 0x4facb8. Other coach consumers: 0x505748 coach recorder (CBLW/CNTW). [CCR 3, 4A; PCR 2.6]
- Census data in analysis\coachless\emulation.json (generator scripts/coachless_carousel_tools.py emulate): 13 before/after pairs (kind pass/rollover): y2026-week1->offseason (378 aged, 0 disagree, skipped TGIDs 116-121,123-128), y2026-offseason->y2026-v2-preseason2027-live (29 predicted/29 observed expiries; predicted CNIDs 393..428), r2026-confchamp->r2026-end2013, r2026-end2013->r2026-pre2014, po2-final-2013..2016 -> preseason (378 aged each), a138v2-conference2013->preseason2014, cfbr-ranking-end2014->preseason2015, cfbr-dm-regular2013->pre2014, cfbr-dm-end2013->pre2014, po2-final-2013->po2-preseason2014; cap768 skipped_tgids = [] in all. Census includes per-fixture fbs/coch counts, no_head_coach/no_oc/no_dc lists, free_pool_by_cops, zombie rows (a138v2-conference2013: fbs 138, coch 429, no coachless; a138v2-preseason2014: coch 450; cfbr-dm-end2013 fbs 126, coch 396, 40 teams without HC mid-carousel). [emulation.json]
- selftest-v6.json (installer v6 selftest): report_checks 85 passed; stage word counts: storage126 475, real2026 552, real2026-playoff 1062, real2026-playoff-v3-u2 1317, ...-y2026 1364, ...-y2026v2 1373 (sha ba65b7f4...), real2026-cc 566 (a6c85209...), real2026-playoff-v3-u2-y2026v2-cc 1387 (71f7a33a...), real2026-cc-guard 570 (2f025386...), real2026-playoff-v3-u2-cc-guard 1335 (608e61ad...); passed true. BOOT 461fa3fa..., boot_po 32c7a09d..., MISC 9fef8dd7.... [selftest-v6.json]
- t2-crash\RPCS3-real2026-cc-t2.log (sha a3d12411...): T2 run loaded WRONG save (Y2026A via cellSaveDataFixedLoad2 line 70809, USR-DATA 8,278,016 B, not CFB138) so cap patch not truly tested; crash = known access violation 0x4c1c2c; fault address 0x44c9087b = table base + 19 x stale pointer; no register dump; first coachless team in TTYP-0 order (FIU 116) hit first. [CCR 7]
- y2026-offseason-ccfy-repair\: repair of Y2026A save (CCFY=SSYE+1 on 29 coaches; USR-DATA e96a2e62...; original 377196d6...; repair json sha 048a0b91...). Whether game accepts edited USR-DATA: UNVERIFIED. [CCR 4B]

### PART D. NEWS (CFP "season over" fix) + CODE ROOM -- src: code-room-and-news-fix.md (CRN)
- RPCS3 build v0.0.43-20250-304d544b (2026-10-08) supports patch types calloc, jump, jumpl, jumpf, alloc (not used by any project patch). rpcs3.exe sha256 132bcad1...2a89. Segment-0 tail used for caves: stock 0x1bbf100..0x1bc0000 (3,840 B = 960 words; segment 0 = 0x10000..0x1bbf0e8; next seg 0x1bc0000); CFBR 0x1bc2700..0x1bd0000 (55,552 B = 13,888 words; segment 0 = 0x10000..0x1bc26e8; next 0x1bd0000; live log p_filesz=0x1bb26e8 UNVERIFIED mismatch vs 0x1bc26e8 in same doc table). calloc predicted stock 0x1d60000 / CFBR 0x1d70000 [INF]. Free caves status: playoff v3 cave 509/509 full; U2 R2 ~7 free words; ui-fixes W left 7 dead words at stock 0x1fe9fc. LLVM runs tail via ppu_recompiler_fallback [INF -> later confirmed? news fix boot gate: "news1" clean per PCS A.1]. [CRN 1]
- News data: CAPT (captions: `select * from CAPT where CPST, CPPO`), HEAD (`HEAD where CPST, TOID`), MCOV (news stories; SGNM/SEWN stored from story record bytes r1+0x17c SGNM, r1+0x17e SEWN; slots 0xc8 / 0xd0), EASP writer. Season-ending types: CAPT 2984/2987 (CPST 503), 2940 (492), 2942 (493), 2961 (498), 2966/2968/2969 (499); HEAD 3062 "Finishing the Job", 3064 "... Ends with a Win!", 3066 "<team> Finish 'Em Off!" (503); neutral types 500 close, 501 convincing, 502 blowout (CID0 2970..2981, HID0 3023..3043). BOOT entry 826 holds templates. Story record = 0xa0 bytes copied to r1+0xe0; picker reads caller frame 0x74/0x7c/0x84/0x8c; CPST in r8 from `lhz 0x160(r1)`. [CRN 2.1]
- Functions stock / CFBR: caption/headline picker 0x478cc4 / 0x47a14c; callers MCOV writer 0x4a8aa8 / 0x4aa080 and EASP writer 0x4a8fc4 / 0x4aa59c; EA-SQL helper 0xa67320 / 0xa691b0; `select BIDX from BOWL where SGNM, SEWN` 0x1762880 / 0x1765b04; `select GHTG,GATG,GHSC,GASC,GSTA from SCHD where SEWN, SGNM` 0x1764e24 / 0x17680a8; weekly news loop 0x4a9078 / 0x4aa650. [CRN 2.1, 3]
- **cfp-news-fix-v1 (stock "NCAA14 experimental CFP news fix v1", patches/cfp-news-fix-v1/patch.yml sha 5de0127c...) and cfbr-cfp-news-fix-v1 (CFBR "NCAA14 CFBR CFP news fix v1", patches/cfbr-cfp-news-fix-v1/patch.yml sha 1db4f312...)**: 182 words each = 180 cave words (cfp_news_pick 68, cfp_story_type 82, 2 leaf helpers, nops) + 2 site words (both picker call sites -> `bl cfp_news_pick`); entry at tail base (stock 0x1bbf100, CFBR 0x1bc2700; CFBR cave ends 0x1bc29cc/0x1bc29cf); C source tools/ppc-cave/caves/cfp_news_fix.c; builder scripts/build_cfp_news_fix_patch.py; 48 gates/ELF; 2,408 emu scenarios. Logic: if CPST in {503,492,493,498,499} and SGNM<127, BIDX in {29..32, 25..28, 12, 17} (CFP non-final rounds) -> CPST remapped by margin: <=8 -> 500, 9..20 -> 501, >=21 -> 502 (score query fail -> 501); else unchanged. Final (39) and regular bowls unchanged. Trade-off: rematch/old-team/comeback flavour lost in non-final CFP rounds. Checker scripts/check_cfp_news_fixture.py (fixtures pu2-final, po1/po2/po4 finals, playoff-v1/v2-final: 0 flagged). Boot expect "NCAA14 CFBR CFP news fix v1" count 182. check_patch_applied.py extended with --expect-count, --expect-calloc (sha 1be89af6...). Runtime: news1 boot gate clean per later docs (PCS A.1 "news1 / art1 ... clean" -- indirect evidence). [CRN 2-5; PCS A.1]
- Gaps D: margin thresholds cosmetic/unknown vs engine; `-Q` bowl name text may name first playoff bowl; existing story records unchanged; installer stage for news fix not written at doc time.

### PART E. UI FIXES, SIM STATS, SPEED, CONTROL

#### E1. UI fixes v1 -- src: ui-fixes-v1.md (UIF)
- **cfbr-ui-fixes-v1** ("NCAA14 CFBR UI fixes v1", 23 words, 26 gates; patch.yml sha cf59c5b5...ba61; manifest 143875c9...) and **ui-fixes-v1** stock ("NCAA14 experimental UI fixes v1", 23 words; patch.yml cf559fbe...0714); builder scripts/build_ui_fixes_v1_patch.py; installer scripts/install_cfbr_real2026_v8.ps1 stage real2026-full-art1-ui1 (1,410 words; merged sha 3d206836...57de; config e73baf90...; full-art1 block 71f7a33a... unchanged; state evidence/cfbr-real2026-v8-state.json). [UIF top, 4]
- **Fix J (1 word)**: "Choose Your First Job" list is a temp DB view with fixed capacity 126 rows filled in STTM order, so STTM FBS rows 126..137 (12 added schools) fail to insert. View spec (stock 0x1c666ac / CFBR 0x1c7672c, 0x50 B): TGID, PSun ("User Controlled Team"), CNAM, TPRX. Screen class stock 0x1ba570 / CFBR 0x1bae60; constructor `0xa55e50(0, db, spec, max_rows, 0)` (CFBR 0xa57ce0, 179 call sites); fill CFBR 0x1bacb4 (strings stock 0x1ba434/0x1ba46c, CFBR 0x1bad24/0x1bad5c); cursor `select STTM.TGID, STTM.CGID, STTM.CFUC, TEAM.TPRX from STTM join TEAM where STTM.TTYP = x and TEAM.TPRX <= y` (stock 0x1705e14 / CFBR 0x1709098); insert string stock 0x1705f04 / CFBR 0x1709188. Patch: CFBR 0x001baebc `38c0007e` (li r6,0x7e) -> `38c000c8` (li r6,0xc8); stock 0x001ba5cc same. STTM capacity 400. Needs fresh Dynasty to test. [UIF 1]
- Other 126-capped leads NOT patched: stock 0x1a2e3c `cmplwi r26,0x7e` + 0x1a2f18 `li r6,0x7e` (TEAM list order by TDNA); 0x1e1018 `li r6,0x7e` + 0x1e1660 `li r8,0x7e` (rankings view TCRK/TMRK/TBRK, "show 126"); 0x1de9b4 / 0x1dea90 / 0x1debf4 (TGID/DPRO view with 126-entry stack array); 0x1e2ca0, 0x1e4cfc `li r8,0x7e` (STDR stadium ranking). OK lists: coach carousel candidates view 0x1c240c (COCH capacity via 0x43be98('COCH')); user contract view 0x1c38a0 (378, holds user's current contract + <=2 offers; fill area 0x1c34c0); weekly news loop stock 0x4a9078 (126, patched by activeN 138). [UIF 1.4]
- **Fix W (22 words, no cave)**: hub header "WEEK 256, 2013" in bowl season: header builder stock 0x1fe7fc (CFBR 0x1ff1c4) uses r27 = 0x43d104() (stock call 0x1fe848, `mr r27,r3` 0x1fe850): 30..40 -> "Bowl Weeks, %d"; 16 -> "Conf Champ Week, %d"; 0x96 -> "End Of Season, %d"; else "Week %d, %d" with r27+1 (0x1fea18). 0x43d104 returns default 0xff (`li r3,0xff` at 0x43d17c) when GINF.GHTG team has no SEWT 30..40 row -> 255+1 = 256. Fix rewrites type dispatch block stock 0x1fe9a4 / CFBR 0x1ff36c (22 words, 29 stock words checked) adding `cmpwi r27,0xff; beq BOWL`; 7 trailing words unreachable. Only stack word nearby: start-year v2 at stock 0x1fe840 / CFBR 0x1ff208 (`addic r28,r3,...` header year). [UIF 2]
- **Playoff news text** (issue 3) not patched here: CFP FR/QF win says "caps off successful season with bowl win" (story type 503 = generic bowl win; CAPT 2984 "-b caps off successful season with bowl win.", 2987 "-J end their season with -; -L---M victory over -d in the -Q."; neutral 2982, 2983, 2985, 2986; 492/493 rematch/old team, 498/499 comebacks; 494-497, 500-502 neutral; 507 bowl loss correct). Types chosen by data-driven rules engine: 45-field condition vector builder stock 0x4a5888 / CFBR 0x4a6e60 -> engine stock `bl 0xa8ff3c` at 0x4a88e0 / CFBR `bl 0xa91fec` at 0x4a9eb8 (rules data not located); captions via query 0x176b128 (CAPT CPST, CPPO), headlines 0x176b180 (HEAD CPST, TOID x2); writer stock 0x4a8aa8/0x4a8fc4. Options A (data edit of CAPT/HEAD in BOOT 826 + FE2IG 4664 copy), B (code remap -> became the news fix, PART D), C, D. [UIF 3]
- Gaps E1: remaining 126-cap list leads; "WEEK 256" GINF team at that moment runtime-only; Fix J pass/fail runtime result UNVERIFIED in these docs.

#### E2. Sim stats review -- src: sim-stats-review.md (SSR); fixtures in fixtures\ (po2-final-2013..2016, boot127-endseason2013, active127v6-endseason2013, a138v2-endseason2013, pu2-final, stock-preseason-2013-MODBASE)
- Save format: USR-DATA = raw EA TDB v8 big-endian DB (header `DB\x00\x08\x01`), 173 table tags; parse via scripts/inspect_tdb.py parse_db(path, set()) (empty selection dumps all). Default selection only TEAM, CONF, DIVI, BOWL, SCHD, LEAG, STGE, DYNI, SEAI, TSSE, CONT. [SSR 1]
- SCHD (20-byte rows): GATG/GHTG away/home TGID, GASC/GHSC scores, SEWN/SEYR week/year, GSTA 2 = away win, 3 = home win, SGID, GFOT. [SSR 1, 1a]
- **BTES** (per-game team box score, 48 bytes, 1852 current / 2688 max): CONFIRMED exact vs known Alabama 34-18 Miami (SEWN 17, SGNM 8, rows 1794/1795): ts1d first downs, tsor rush yds, tsop pass yds, tsoy = tsor+tsop total off yds, tspt time of possession in SECONDS, tspi INT thrown + tsfl fumbles lost = turnovers, tsTy = tsoy+tskr+tspr all-purpose yds. Plausible only: tspc completions, tspe penalty COUNT, tsPy penalty YARDS (NOT pass yards; earlier report's mapping was wrong), tsof fumbles. [SSR 1a]
- **TSSE** (team season stats, 52-byte rows, 37 fields) shares tags with BTES (season totals): tspa/tsra attempts, ts1d, ts3c/ts3d, ts4c/ts4d, tspi, tsfl, tsop, tsor, tsPy, tsTy, tsoy, tsPt, tsot, tsrt. TSSE-only unconfirmed: tssa, tsta, tspd, tsdf, tsDi, tsPi, tssk (~32/season sacks?), tsdp, tsdr, tsfr, tsdt, tsdy, tsty. [SSR 1a, 8]
- **BOFF** (game-level player offense) CONFIRMED: gaya pass yds, gaat attempts, gacm completions, gatd TDs, guya rush yds (PGID 248 Alabama QB gaya=272). **PSOF** (player season offense, 28-byte rows) mapping by analogy: saya pass yds, saat att, sacm comp, satd TD, suya rush yds, suat rush att, sutd, sain INTs, sufu fumbles lost. PLAY.PFNA/PLNA keyed by PGID names. PSDE/PSKI/PSKP (20/28/16 B), BSCS/SSUM, TSHS (4 B: TGID, WINS, LOSE, SEYR) exist. Receiving fields (gcya/gcyc/scya/scyc) ambiguous. [SSR 1, 1a]
- **TEAM.TROV** (8-bit 60-99) = real team overall (TOVR is uniformly 0 = dead). TEAM names TSNA/TDNA. [SSR 1a, 3a]
- Results (R26PO2 138-team, 4 CPU-sim seasons): PPG 27.73 avg (real 27.78 in 2023), home win 54.6% (real 63.4%, gap -8.8 pts; present in pre-expansion builds too: boot127 58.7%, active127v6 55.1%, a138v2 54.4%), pass 233.0 / rush 160.7 / total 393.8 yds per team-game (real 229.55 / 156.15 / 385.70), 1st downs 20.5/g, turnovers 1.51/g, penalty yds 62.0/g, YPA 7.07, YPC 4.48, blowout (>=21) 30.2%, one-score (<=8) 36.5%, shutouts ~2.0%; drift over 4 seasons: PPG 25.56 -> 29.65, pass yds 215.1 -> 244.1, turnovers 1.63 -> 1.34. Upset rate by TROV gap: 0-4 47.1%, 5-9 38.9%, 10-14 21.0%, 15-19 17.4%, 20+ 5.9%. TROV mean/stdev: boot127 80.3/8.8, active127v6 80.2/8.9, a138v2 78.8/9.7. Conclusion: 138-team expansion does not distort sim stats. [SSR 2-4, 3a, 7]
- Candidate tuning tables UNDECODED: GOPT (1 record, 176 B, 151 fields), MOPT (1 record, 24 B, 64 fields), UOPT (12 B, 14 fields), COCH (429 records, 176 B, 155 fields), STGE. No slider/difficulty table located. Cross-ref: MRD 9.2 says GOPT/SOPT/MOPT were read from BOOT 359 and MISC 145 and carry no OT rules. Hypotheses for home-win gap: Advance/sim-week path distinct from played games; base-game tuning; clock rules unknown. Scratch script `...\scratchpad\sim_stats.py` (session-scoped, may not persist). [SSR 5-6, 8; MRD 9.2]
- Gaps E2: season completion %, receiving leaders, TSSE-only fields, no national averages for sacks/penalties/completion%/turnovers/close-game rate; 2024/2025 real aggregates missing; stale/carry-over SCHD rows (~40 appearances/team in 2013) uninvestigated.

#### E3. Speed settings + alternate control -- src: speed-settings-proposal.md (SSP), alternate-control.md (ALT)
- SSP (docs only, not applied): the isolated RPCS3 config.yml current Frame limit Auto, Resolution Scale 100, Vblank Rate 60, Clocks scale 100. Low risk: Frame limit Off; Resolution Scale 50-75 (blurs text; keep 100 for screenshot reading). Medium: MSAA disabled (current value unchecked). High risk (do not use for baseline-comparable runs): Vblank Rate >60, Clocks scale >100 (alters game-logic timing). Tool: fast_drive.py hash-based classifier downscales to 9x8. [SSP]
- ALT: control_isolated_rpcs3.py (list/capture --label/press --key/--sequence up to 24/--hold 0.05-2 s default 0.12) verifies HWND/PID/exe = the isolated rpcs3.exe, single visible window containing [BLUS31159]; keymap Start=Enter, Cross=X, Circle=C, D-pad=arrows, L1=Q, R1=E, L2=R, R2=T; F12 screenshots 1280x720 into evidence/gameplay (control.jsonl, input-attempts.jsonl); capture_isolated_window.py (bounded client clicks on host dialogs), close_isolated_rpcs3.py (WM_CLOSE, may need Exit Game confirmation; no force kill). Validated 2026-10-08: new offline Dynasty (Arizona, Jeff Jones), save MODBASE separate from DEFAULT, reload verified (FixedLoad2 prefix BLUS31159-DYNASTY-MODBASE, USR-DATA 8,278,016 B, sha BA8F22C7...5B), snapshot fixtures/stock-preseason-2013-MODBASE. Default rules observed: Varsity skill, injuries/fatigue/play clock/home-field on, 5-minute quarters, normal speed, min-speed threshold 50. Early title-screen Start sometimes needs --hold 0.8. RPCS3 source commit 304d544b in analysis/rpcs3-input. Outstanding at doc time: season progression/rollover tests. [ALT]


