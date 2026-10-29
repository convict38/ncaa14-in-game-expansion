# Online play feasibility (NCAA14 native PC port, self-hosted)

Date: 2026-10-29. Scope: personal use with friends. No EA or third-party server is contacted by the game.
All findings come from static data (RPCS3 boot log, import tables, strings in the decrypted EBOOT, ps3recomp
sources) and public web research. No game launch was needed.

## Verdict

Feasible, in two very different sizes.

- **Online Dynasty (shared league, turn-based): feasible and cheap if we skip the game's own online mode.**
  A small server we host stores one dynasty save and passes a baton. Days of work, no reverse engineering of EA's
  protocol. Emulating the game's own Online Dynasty (Blaze `DynastyOnDemand`) is also possible but takes weeks.
- **Head-to-head: the game already contains a lockstep netcode** (input delay, desync checksums, a DESYNC screen), and
  its in-game traffic is peer-to-peer over plain `sys_net` sockets, which our runtime can already map to host Winsock.
  The hard part is only the front door: EA Blaze login, matchmaking and session setup over an SSL connection.
  Recommended path: a minimal local Blaze server (option a), gated by a cheap determinism test first. Fallback if Blaze
  proves too costly: our own lockstep (option b). Stopgap today: remote play (option c2).

## 1. What the game's online stack uses

### Imported modules (RPCS3 boot log `log/RPCS3.log`, "Imported module" lines)

| Module | Use | Our status |
|---|---|---|
| `sys_net` (about 35 imports: socket, connect, bind, listen, accept, send/recv/sendto/recvfrom, poll, select, set/getsockopt, getsockname, getpeername, gethostbyname, inet_*, `sys_net_initialize_network_ex`, `sys_net_abort_*`) | All Blaze and peer traffic (raw TCP and UDP) | `libs/network/sysNet.c` passes through to Winsock, **off by default**. `runtime/ppu/ppu_sysprx.cpp` has an offline model (everything would-block) unless env `PS3_NET_ONLINE` is set, which registers the host handlers in front of it |
| `cellNetCtl` (8 imports) | Link state, start dialog | `cellNetCtl.c`: disconnected; NetStart dialog returns DIALOG_CANCELED offline; `PS3_NET_ONLINE=1` restores "connected" |
| `sceNp` (about 60 imports) | See below | Partly real, partly fake, several unimplemented |
| `cellHttp` (Init/End, Https Init/End, cookie init/end only) | Side channel; strings contain a `gameface_recipe?nucleus_id=` URL and a bugsentry URL | `cellHttp.c` is a real winsock client without TLS |
| `cellSsl` (Init, End, `CertificateLoader`) | Loads the system CA list | `cellSsl.c` stub returning empty cert data |
| `sceNpCommerce2` | Store, DLC | Stub (log: Init then Term when the NpId lookup fails) |
| `sceNpTrophy` | Trophies | Implemented |
| `cellMic`, `cellCelpEnc`, `cellAdec` | Voice chat (CELP) | Not needed for a first version |

**Absent from the import table:** `sceNpMatching2`, `sceNpSignaling`, `sceNpScore`, `sceNpTus`, `cellRudp`. The game does
not use Sony matchmaking at all. Key consequence: **RPCN (which emulates Sony's NP matching) is not sufficient and is
mostly irrelevant**, because everything above sign-in is EA's own stack on raw sockets.

### `sceNp` imports that matter
- Sign-in and identity: `sceNpInit/Term`, `sceNpManagerGetStatus`, `Register/UnregisterCallback`, `GetNpId`, `GetOnlineId`,
  `GetSigninId`, `GetAccountRegion`, `GetChatRestrictionFlag`, `GetContentRatingFlag`, `GetNetworkTime`, `SubSignin/SubSignout`.
- **Authentication ticket:** `sceNpManagerGetTicket`, `GetTicketParam`, `RequestTicket2`. The Blaze type
  `Authentication::PS3LoginRequest` carries this ticket to EA. We control this HLE, so we can mint any ticket that a
  private server accepts.
- `sceNpLookup*` (init, title and transaction ctx, NpIdAsync, ProfileWithAvatarSizeAsync, Poll, Abort), `sceNpBasic*`
  (friends, block list, presence, messages, GetEvent, RegisterContextSensitiveHandler), entitlements
  (`GetEntitlementById/IdList`), `sceNpDrm*` (already HLE'd for the DLC path), `sceNpUtilCmpNpId`.
- In the repo, `sceNpManager*` getters, `sceNpBasic*` and a fake profile exist in `libs/network/sceNp*.c`. `GetTicket`,
  `RequestTicket2`, `sceNpLookup*`, `GetNetworkTime`, `GetEntitlement*` have no implementation (grep over `libs/` and
  `runtime/` found none), so they hit the unresolved-NID default (r3 = 0).

### EA's own layers (strings in the decrypted EBOOT)
- **Blaze client SDK** is linked in. Memory categories `Online::Blaze`, `Online::Dirtysock`, `Online::Osdk`.
  Named TDF types per component: GameManager 111, DynastyOnDemand 88, Authentication 39, Rooms 33, Stats 27, Locker 26,
  Playgroups 25, Util 24, GameReporting 24, ScoreProcessor 19, Commerce 18, Seasons 14, Redirector 12, plus OSDK settings,
  ticker and messaging, Messaging, Mail, CensusData, GridironClub, LiveBannerAd.
- **DirtySock** is the transport. SSL is EA's own (an embedded "GeoTrust SSL CA" certificate, `SSLData/SSLPool`
  allocators), not `cellSsl`. Prior art (Section 2) indicates Blaze of this era uses SSLv3.
- **Redirector flow:** strings include `gosredirector.online.ea.com`, `.stest`, `.scert`, `gosredirector.ea.com` and
  `https://gosca.ea.com:44125/redirector`. The client asks the redirector for a Blaze instance
  (`Redirector::ServerInstanceRequest`), logs in (`Authentication::PS3LoginRequest`, `ConsoleLoginResponse`,
  `ExpressLoginRequest`), then `Util::PreAuth/PostAuth/FetchClientConfig/Ping/GetTelemetryServer`.
- **Matchmaking and sessions:** `GameManager::StartMatchmaking`, `CreateGame`, `JoinGame`, `GetGameList`,
  `SetGameSettings/Attributes`, `UpdateMeshConnection`, `UpdateGameHostMigrationStatus`, `ReplayGame` (rematch),
  `RankedGameRulePrefs`; `Playgroups::*` (parties); `Rooms::*` (lobbies); `UpdatePingSiteLatency`.
  `UpdateMeshConnection` and `GetNetGameDist` indicate **peer-to-peer mesh gameplay**; Blaze only brokers it.
- **Results:** `GameReporting::SubmitGameReport` (OSDKGameReport), `Stats::*` leaderboards, `Seasons::*` (Season Showdown
  and School vs School goals; throttle `SEND_SVS_SCORE_REPORT`).
- **Gameplay sync:** strings `Begin desynced tracked buffer info`, `ChecksumTrack`, `CalculateAndAppendChecksumBuffer`,
  `CC_Desync`, `DESYNC -- DESYNC`, `BUG_SENTRY_REPORT_DESYNC`, `GetForcedScreenInputDelay`, `Input Buffer`,
  `HideLagIndicator`, `isSynced`. This is input-lockstep with checksum desync detection.

### What the game does today when you pick Online
From `docs/ps3recomp-boot-log.md` Steps 34D-2 and 34D-3 and `docs/ps3recomp-mode-matrix.md`:
- Main menu **OSDK_ONLINE tile**: dialog "NOT LOGGED IN - Login Now / Cancel". `sceNpManagerGetStatus` returns OFFLINE and
  `GetNpId` returns INVALID_STATE (env `PS3_NP_NPID_OFFLINE=1`, set in `game_project/main.cpp`, matching RPCS3's log).
- **Ultimate Team and Dynasty-new:** "CONNECTION ERROR - not connected to the EA servers" with Login Now / Continue To View
  Offline Dynasty Files Only / Cancel. Offline Dynasty works; "Join Online Dynasty" loops on the failed check (expected).
- No crash, no unresolved-NID noise on these paths. At boot the game calls `cellNetCtlInit`, `sceNpInit`,
  `sceNpManagerRegisterCallback` and `sceNpBasicRegisterContextSensitiveHandler`, then trophies.

## 2. Prior art

| Project | Offers | Licence | Reuse |
|---|---|---|---|
| **PocketRelay** (Mass Effect 3 server emulator, Rust; `PocketRelay/Server`, crates `blaze-pk`, `tdf`, `blaze-ssl-async`) | Working Blaze packet codec, TDF types, redirector, auth, matchmaking, a minimal SSLv3 server for Blaze clients | Described as MIT-style (verify each repo's LICENSE) | Best reference. Reusing the codec and SSL crate saves weeks. Different game and Blaze version, so NCAA component and command ids and TDF layouts must be re-derived |
| **BlazeSDK** (Aim4kill, C#) | Blaze 2/3 definitions, example redirector, SSLv3 workaround | Unverified | Reference for redirector and ids |
| **ME3 Private Server Emulator** (C#) | Another Blaze server | Unverified | Reference only |
| **RPCN** (RipleyTom/rpcn, Rust) with RPCS3 | Emulates Sony NP, including matching2 and signaling, for P2P titles | GPLv3 per GameTechWiki (verify) | Out of scope for this game. RPCS3's NP HLE (GPLv2 C++) is only a semantics cross-check, as in the 2026-10-12 audit. Keep GPL code out of our MIT runtime |
| Revivals of EA sports titles of this era (NCAA, Madden, FIFA) | None found. Searches returned the 2013 shutdown notices and generic RPCS3 guides | n/a | We would be first for this title. "No prior art" is unproven; check community Discords before building |

ps3recomp is MIT, so MIT-licensed PocketRelay crates are compatible. No EA binaries, certificates or captures go in the
public repo.

## 3. Head-to-head design options

### (a) Local Blaze server plus NP fakes, using the game's own online mode
1. Runtime: `PS3_NET_ONLINE` on for the modded build; NP manager reports ONLINE (status callback to signed in),
   valid `GetNpId/OnlineId`, `RequestTicket2/GetTicket` return a dummy ticket, `GetNetworkTime`, minimal `sceNpLookup*`,
   `cellNetCtl` connected with a LAN IP, `gethostbyname` maps `gosredirector.*` to our server.
2. Server (Rust on PocketRelay crates): redirector (point to ourselves), auth (accept anything), Util
   (PreAuth/PostAuth/FetchClientConfig/Ping), user sessions, GameManager (create/join/match for two players, mesh
   connection info with direct host IP and ports), GameReporting (accept), Stats/Seasons/Rooms as empty successes.
3. SSL: the game's DirtySock does its own SSL client with an embedded CA. Options: (i) server speaks SSLv3 and we patch the
   certificate check or inject our CA; (ii) hook the ProtoSSL connect/send/recv wrappers in a C cave to run plain TCP.
   (ii) needs more reverse engineering but removes the crypto dependency.
4. Peer traffic goes between the two PCs via `sysNet.c`. Needs open-NAT reports and a VPN (ZeroTier, Tailscale or LAN).
   The server can run on one friend's PC.

Effort: high, roughly 3-6 weeks (server skeleton and SSL from prior art 1 week; discovering the command sequence by letting
the game talk to our server 1-2 weeks; matchmaking and P2P session 1-2 weeks; stabilisation). Needs many game runs through
the run-queue daemon. Risks: (1) NCAA14's Blaze version and custom components (DynastyOnDemand, Seasons, GridironClub) are
undocumented and must be inferred from TDF type names and observed requests; (2) SSLv3 and cipher quirks; (3) NP ticket and
entitlement checks (`ENTITLEMENTID_ONLINE_*`, Online Pass component); (4) game speed is 0.6 to 1.0x today, and lockstep
needs both peers at full speed; (5) cross-host determinism (test below). Benefit: original UI, lobbies, rematch, results and
the game's own desync-checked netcode; the same server later hosts Online Dynasty.

### (b) Our own input-lockstep in the runtime
Hook controller reads (`cellPad` HLE) and frame progression so both peers feed identical inputs per frame with a fixed input
delay, plus a start handshake (same teams, seed, rosters, settings). Needs identical RNG seeds and wall-clock reads
(`sys_time`, `cellRtc`), no divergence from async elements (SPU jobs, audio, threads), per-N-frame state hashing (the game's
`ChecksumTrack` can be reused), and our own lobby and pre-game flow (the nav automation would have to drive the menus
identically on both sides).
Effort: medium for transport (1-2 weeks) but open-ended for determinism. Risk: bypassing Blaze bypasses whatever the
original netcode does to neutralise nondeterminism, so we inherit that problem; each desync is a deep debugging session.

### (c) Other
- **c1. Fake Blaze that always pairs the two connected clients (host/join by IP).** This is the intended minimal form of (a).
- **c2. Remote play** (Steam Remote Play Together, Parsec, Sunshine/Moonlight): one PC runs the game with two controllers,
  the friend plays over video. Zero engineering, no determinism risk. Recommended immediate stopgap and the baseline to beat.
- **c3. Rollback netplay:** not practical (no cheap state serialisation, savestates are huge).

### Determinism test (before committing to a or b)
The game proves determinism across PS3s; we must prove it across two instances of our x86 build. Run two instances with the
same save, recorded controller script and start seed, and compare the game's checksum buffers or our frame hash every N
frames for a full game. If they match, both (a) and (b) are viable. If not, find the source first (PPC `fres/frsqrte`
estimates, fused multiply-add rounding, denormals, SPU path differences, thread timing). Use the run-queue daemon
(`harness/RUNQUEUE.md`); no direct launches.

### Recommendation
1. Now: c2 for friends.
2. Phase 0 determinism test, then **(a)/c1**: a minimal Blaze server, host/join by IP over a VPN. It reuses the game's own
   lockstep and original UI. Fall back to (b) only if SSL/login discovery stalls and Phase 0 showed determinism.

## 4. Online Dynasty

### How the original worked (Blaze `DynastyOnDemand` and UI strings)
- The league lives **on EA's servers**, keyed by dynasty id. Requests: `CreateDynasty`, `FindDynasties`, `JoinDynasty`,
  `GetDynasty/GetDynastyStatus`, `SendInvitation/GetInvitations/ProcessInvitation`, `ChangeUserTeam`, `RemoveMember`,
  `TransferCommishStatus`, `SetAutopilot`, `Set/CheckDynastyPassword`, `Get/SetExtraDynastySettings`.
- Data movement is table based: `UploadTeamData/DownloadTeamData`, `GetSyncTables`, `GetTableUpdate`,
  `DodTableUpdateResponse`, `Start/EndDynastyUpdate`, `Upload/DownloadTransientSettings`, `DownloadViewDetailsData`.
  The server stores league table blobs or rows and clients sync them.
- Weekly flow: members play and `UploadGameResults` / `RetrieveGameResults`; `SetReadyToAdvance`; the commissioner
  `RequestAdvanceWeek`, `CheckAdvanceWeekStatus`, `CancelAdvanceWeek`, `SetAdvanceWeekQueueClientStatus`,
  `SetReadyToUploadAdvanceWeekData`, then uploads the advanced data. The names suggest the advance is **computed by a
  client console and uploaded**, not by a server-side sim. This is an inference to confirm by observing a session.
- Extras: recruiting calls and scholarship offers through the server (`OfferScholarship`, `VerifyProspectScout`,
  `MakeContractPick`, `ScheduleRecruitVisitConsole`), and a web site for stories and recruiting. The game also has an
  offline-files fallback.

### Replacement designs
- **Tier 1 (do first): shared dynasty save with a baton server.** A small HTTP service we host keeps the league save blob
  with a version, hash and lock holder. A launcher on each PC pulls the latest save before launch and pushes after quitting
  (rejecting stale base versions). Per week: each human plays their game in turn on their own PC and uploads; the commissioner
  advances the week when ready flags are all set. Offline Dynasty supports several user-controlled teams in one save (to
  verify in the save tables), so one save can pass between humans. Pros: no protocol work, uses the PC port's save paths.
  Cons: sequential within a week, no live notifications. Effort about 3-5 days.
- **Tier 2: results merge.** Each friend plays in their own copy; the server collects box scores and a master copy injects
  them. Needs the game-result table formats mapped. Not recommended yet.
- **Tier 3: emulate `DynastyOnDemand`** on the option (a) server so the game's own Online Dynasty screens work, storing
  tables as blobs per dynasty. Weeks of effort because schemas and sync handshakes must be discovered. Only after
  head-to-head works and only if Tier 1 is not enough.

## 5. Phased plan

| Phase | Work | Output | Effort |
|---|---|---|---|
| 0 | Remote-play guide; two-instance determinism test through the run-queue | Go/no-go for lockstep; known divergence sources | 2-4 days |
| 1 | Online Dynasty Tier 1: baton server, sync client, ready flags, status page | Shared league for friends | 3-5 days |
| 2 | Blaze groundwork: NP fakes (ONLINE, tickets, NetworkTime), DNS redirect, `PS3_NET_ONLINE` in a test build, capture first connect, choose SSL approach | Game reaches our redirector | 1-2 weeks |
| 3 | Minimal Blaze server: redirector, auth, Util, sessions to a logged-in Online menu | Online tile opens | 1-2 weeks |
| 4 | GameManager host/join by IP over VPN, mesh info, game report; test match; chase desyncs | Head-to-head works | 1-3 weeks |
| 5 | Optional: DynastyOnDemand tables, leaderboards, voice (`cellMic`/CELP) | Game's own Online Dynasty | weeks |
| 6 | Packaging, VPN guidance (after the game is complete) | Release | last |

Checkpoints: after Phase 0 (determinism), Phase 2 (past SSL), Phase 3 (original UI proceeds). If Phase 2 fails, use option (b)
only if Phase 0 showed determinism.

## Sources
- Local: `log/RPCS3.log` (imported-module, `sceNp` and `sys_net` lines), `mod-work/docs/ps3recomp-boot-log.md` (Steps 34D-2,
  34D-3), `mod-work/docs/ps3recomp-mode-matrix.md`, `mod-work/docs/hle-audit-2026-10-12.json`,
  `ps3recomp/libs/network/*.c`, `ps3recomp/runtime/ppu/ppu_sysprx.cpp`, `game_project/main.cpp`. Strings come from the
  decrypted EBOOT (not redistributed).
- Web: PocketRelay (github.com/PocketRelay/Server; crates blaze-pk, tdf), BlazeSDK (github.com/Aim4kill/BlazeSDK), RPCN
  (github.com/RipleyTom/rpcn; GameTechWiki RPCN page for GPLv3), EA 2013 retirement of online services for these PS3/360
  sports titles (GameSpot, Game Informer). Licences are quoted from secondary pages; verify before reuse.
