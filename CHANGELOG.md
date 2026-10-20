# Changelog

## 2026-10-20 - PC port: a character-physics SPU job now runs as native code

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Character setup job recompiled.** One of the game's SPU physics jobs (character setup, part of the character physics library) had never been recompiled, so it ran in the slow SPU interpreter and was the single largest source of interpreted SPU work in live play. It is now recompiled ahead of time like the other job binaries (the code the game loads was checked to be byte-identical to what was recompiled). In same-session tests, average frame rate rose 5-13% and the share of frames over 50 ms fell (8.2% -> 3.1% and 9.6% -> 6.5%), in both test orders.

**Also measured, not adopted:** faster SPU code lookup/verification caches (lookup work dropped from about 7% to 2% of SPU time, but frame rate was not consistently better), a tuned SPU idle backoff, and a looser verification of older recompiled SPU code (rejected: it ran wrong code and froze the game). Separately, the player launcher now pauses the automated test queue while you play, and a halftime soak found no rendering problems from the write-back optimisation.

**Validation:** automated gameplay runs (no corruption, no hangs) and visual checks.

## 2026-10-20 - PC port: two more smoothness defaults

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Higher process priority.** The game now runs at "above normal" Windows process priority, so other programs on the PC cannot starve it. With 8 busy background processes, frame rate rose 10-14% and the 3-4 second stutters (SPU jobs starved of CPU) disappeared; it is also slightly faster with nothing else running. `RSX_PCLS=0` reverts it.

**Cached render-target lookup.** A lookup the renderer did for every texture it samples (a scan of up to 160 render targets) is now cached: about 3 ms less renderer work per frame, about 15% higher average frame rate and half as many frames over 50 ms in same-session tests. `RSX_RTFIND_MEMO=0` reverts it.

**Validation:** automated gameplay runs (no corruption, no hangs) and visual checks for both.

## 2026-10-20 - PC port: smoother gameplay from finer host timer resolution

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**PC port: smoother gameplay from finer host timer resolution.** The game's polling threads sleep for 50-1000 microseconds at a time, but on Windows every such sleep was rounded up to the 1 ms timer tick (1000 us requests took about 2 ms), so the game was often late producing frames. The port now raises the timer resolution to 0.5 ms for guest sleeps (default on; `PS3_USLEEP_PREC=0` reverts).

**Measured, same-session A/B tests:** average frame rate about 25 -> about 30 fps, 99th-percentile frame time about 170 -> about 90 ms, frames over 100 ms roughly halved; slow frames caused by the game thread idling dropped sharply. Input latency is unchanged or slightly better. CPU cost is about a quarter of a core.

**Validation:** an automated gameplay run (no corruption, no hangs) and a visual check.

## 2026-10-20 - PC build: kickoff hitch reduced; threaded renderer rejected; sleep granularity is the new lead

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Kickoff hitch reduced.** Render targets are now pooled and prewarmed, so creating them at kickoff dropped from about 0.26 s to about 0.02 s.

**A cheaper write-back tracking check** gives +1-2.5% frame rate, with fewer slow frames.

**A multi-threaded render worker was tried and rejected.** It was about 4% slower and doubled input latency (about 190 ms to about 390 ms), so it stays out.

**Slow-frame analysis.** Normal frames are bound by render-thread CPU. The worst hitches are mostly the game's own threads not producing frames. The GPU is never the bottleneck.

**New lead: Windows sleep granularity.** The game's short polling sleeps (50-250 microseconds) actually take about 1 ms on Windows, so its loops run 4-20x slower than intended. A fix is being tested.

**Frame rate depends heavily on other apps running:** about 23-28 fps versus 30-35 fps on the same build, depending on what else is open. Priority and scheduling options are being tested.

## 2026-10-19 - PC build: Q2 field stripes and the "2013" label fixed; smoothness measured directly; shadows matched

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Q2 field stripes in the Super Sim overhead view fixed.** A graphics readback was copying the field's wear-and-tear image before the game had finished drawing it, leaving visible stripes in the second-quarter overhead camera. A reference run on RPCS3 confirmed the stripes were specific to the port, not something the original game does. Fixed by waiting for the draw to finish before the copy runs.

**School Records "2013" year label fixed (main mod v26).** The root cause was a packed record-date value that had 2013 baked into it instead of the dynasty's actual year. Existing v25-era save records keep the old "2013" label, since the bad value is already written into those saves; new records write the correct year. The PC build was rebuilt against v26.

**Smoothness, now measured directly.** The user reported choppy play even though the on-screen counter read 25-30 fps, so this round measures frame times and input lag instead of only an average:
- **Frames over 50 ms dropped from about 13.6% to about 6-7%,** from a bigger pool of render-target memory with least-recently-used eviction (so targets are not thrashed out and rebuilt), and from fixing dropped vertical-blank ticks so the game holds its intended 30 Hz pace instead of drifting.
- **Pipeline prewarm at boot** (preparing graphics pipelines in advance instead of on first use) cut the pipeline-creation stall on play transitions from about 1 second to 0.05-0.3 seconds, and frames over 100 ms fell by about 27%.
- **The ANT animation background job now runs mostly as native code** instead of being stepped in software, cutting that interpreted work by about 75% and shortening play-transition stalls by about 20%.
- **Input latency measured at 150-180 ms,** including the game's own 2-3 frame input pipeline (not an emulation-only figure).

**Player shadows checked against RPCS3.** A matched day game on both the PC build and a reference RPCS3 session shows the shadows match.

**Still open:** some choppiness remains from CPU-bound rendering and play-transition hitches, and an optional multi-threaded renderer change is still on the table as a further fix for both.

## 2026-10-18 - PC build: Super Sim and freeze fixed; picture and frame rate gains; game modes validated

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Super Sim results corruption fixed.** The 10-14 note calling the earlier Super Sim fix premature was right to be cautious, but the bug itself (an 80-yard run with no touchdown, "3rd & -65") is now closed. The cause was a mismatch in SPU floating-point behaviour: the real hardware (and RPCS3) flushes denormal numbers to zero on the SPUs, and the port was not doing that, so an SPU-side sim calculation diverged. With denormal flushing turned on for SPU threads, the corruption is gone (repeated clean runs, downs and distance advancing normally, game clock running).

**Kickoff freeze fixed.** The freeze right after kickoff, reported in the 10-14 note as "culprits found" but not yet resolved, is now fixed. The real cause was a background game-engine code check that should have required a function's own code to still match, but under one of its two verification modes it was accepting any function at all, so execution could wander into unrelated translated code and corrupt a loaded game module. The check is now tightened and validated clean across all test runs.

**Audio is solid.** Silent audio blocks in gameplay dropped from about 90% to about 25%, and the game audio producer is now able to keep its buffer filled enough that the choppiness is gone. The user reports it sounds good.

**Picture fixes.** Several rendering bugs were tracked down and fixed: dark, crushed-looking 3D scenes are fixed by correcting the colour space of the rendered frame; crowd popping and sparse, nearly-empty stands are fixed by making colour-clear operations respect the game's intended clip region (they were wiping the crowd image data each time instead of only the part meant to be cleared); 2x supersampling is now on by default, at no measured performance cost; helmet colour is fixed (helmets were rendering orange instead of crimson because eight of the sixteen texture inputs were not being colour-corrected); a shadow-comparison direction bug is fixed; and the daytime sky and main-menu background now visually match a reference RPCS3 session.

**Frame rate: from about 9-10 fps to about 28 fps.** Heavy gameplay was about 9-10 frames per second as of the 10-14 note; it is now about 28. The contributors, each measured by itself: a cache that reuses already-converted vertex data across frames (about +63%); fixing a texture-change-tracking feature that had never actually been active (+17%, once it was working); narrowing that same tracking's scan window instead of checking everything; a shorter idle sleep in the per-frame wait loop (+6%); a faster path through the graphics command queue (+3%); and a texture-slot lookup cache (about +4%, still in testing).

**Intermittent Super Sim freeze under CPU load fixed.** A second, separate freeze showed up specifically when the host machine was under heavy CPU load during a Super Sim. The game's background job system assumes a given piece of background work will finish within two rounds of game logic, which is always true on real hardware; under our emulation, with the host machine busy, that assumption could break, and the game would re-initialize a work slot and erase a "done" signal before anything had read it, leaving two threads waiting on each other forever. The fix holds that re-initialization back until the signal has actually been read. Under artificial CPU load, this went from about 3 of every 4 runs stalling to 8 of 8 clean runs. A related, smaller correctness gap (some processor-to-coprocessor memory writes not being properly synchronized) was also closed as a precaution, though it was not the cause of this particular freeze.

**Game modes validated on the native modded build.** With the above fixes in place, a validation pass exercised the modded build directly (not just the emulator): a Dynasty from Pre-Season 2026 all the way through a season, conference championships, the 12-team playoff, the Heisman race, the full off-season, and rollover into Pre-Season 2027, including loading the history pages; a brand-new Dynasty started from scratch; Road to Glory, from creating a player through a high-school season, recruiting, signing with a school, playing college games, and checking pages and save/reload; and Play Now with Super Sim. One cosmetic bug was found and logged: the School Records page labels current-season (2026) records as "2013".

**Main mod: v25** adds community-made team art for Jacksonville State, Sam Houston, Liberty and Sacramento State, credited by handle in the project's community credits list (clmzntyger, mdotjenkins and FTk Ray). No asset files are included in this repository.

## 2026-10-18 (later) - PC build: frame rate up to about 30-36 fps

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Frame rate: about 30-36 fps in heavy gameplay,** up from the about-28 fps figure earlier today. Three changes are now on by default: the texture-slot lookup cache noted earlier as still in testing; an adaptive skip of render-target write-back for targets nothing ends up reading; and a matching skip of the CPU-side image copy that write-back would otherwise have fed.

**The write-back skip passed a wide visual check.** Menus, the Play Now intro, gameplay, replays, pause, box scores and Dynasty pages were all compared frozen-frame, 22 frames in total, with 0 pixel differences from before the skip was enabled.

**Logged as open, not fixed:** a pre-existing Super Sim overhead-view shading glitch in the second quarter.

## 2026-10-14 - PC build: players drawn correctly; freeze-causing code found; Super Sim correction

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Players are no longer bunched in one line.** Everyone used to be drawn stacked in a single line down the middle of the field. The graphics translator was treating one GPU command as matrix data, which wiped each player's sideways position. Formations, pre-snap and live plays now render correctly.

**Freeze culprits found.** Two of the background game-engine code pieces (SPU programs) that froze games just after kickoff are identified and excluded. More of the game's background work can now run as fast native code instead of slow emulation.

**Correction on Super Sim.** The earlier note that Super Sim scores were fixed was premature. Simulated plays still sometimes give impossible results, such as an 80-yard run with no touchdown or "3rd & -65". That bug is being hunted. It does not depend on the earlier memory speed option, and graphics, CPU vector math, SPU float math and the game clock have been ruled out.

**Speed.** A frame-pacing tweak was measured and made no difference, so it stays off. Gameplay is still about 9-10 frames per second. The next big step is splitting rendering across two threads (estimated +25-40%).

## 2026-10-13 (night) - PC build: sound works, analog controls, measured speed gains

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Sound works.** Game audio on the PC build used to be about 90% silent; it now keeps real time with only normal pauses (7-15% quiet in tests).

**Analog controls.** Full analog stick and trigger support for real controllers, and the automated test harness can now use the sticks too, so it performed its first kickoff with the kick meter.

**Speed measured change by change.** A new live switch turns each speed fix off mid-game on the same scene: the vertex cache and the surface lookup index are each worth about a quarter of the frame rate, indexed drawing about a tenth, and CPU/GPU overlap about 5%. Gameplay is about 9 frames per second; a larger batch of newly translated co-processor code looked faster but froze the game after kickoff, so it is disabled until fixed.

Also: a fix for a likely cause of an occasional hang when advancing a Dynasty week (not yet confirmed), and one odd Super Sim play (a 50-yard loss right as the ball reached midfield) that is being investigated.

## 2026-10-13 (later) - PC build frame rate roughly tripled

Side track (native Windows build via static recompilation). No game code, data or executables are published; everything below runs against the owner's own game files.

**From about 3 to about 9 frames per second in gameplay on the modded build.** Three changes did most of it: fixes in the graphics thread (a faster surface lookup and a cache for converted vertex data, which now reuses roughly 4 in 10 vertex fetches), two CFB Revamped SPU jobs that now run as native code instead of being interpreted, and letting the CPU and GPU work on different frames at the same time.

**An idle sleep was spinning a CPU core.** The game polls with very short sleeps, and the recompiled version of that sleep busy-waited and pinned two cores. It now waits on a timer; those threads dropped from about 97% to 16-25% CPU. Speed did not change, so it was not the limit, but it frees the machine.

Still well short of 30 frames per second (real play needs about 30). The GPU is now the limit, because each frame sends far too much vertex data; sending much less per frame is next (a first step, indexed drawing, is in).

**Two long-standing rendering bugs fixed.** The sky above the stadium was never drawn and showed as a black hole; the face-culling defaults did not match the PS3's power-on state, and with that and two smaller fixes the night sky, clouds and light towers now render. The post-game menu tiles also draw in team colours again instead of grey. A Super Sim check after these changes still gives a normal score (Houston 18, Sam Houston 26).

## 2026-10-13 - PC build: a full modded Dynasty season runs natively; Super Sim scores fixed; faster boots

Side track (native Windows build via static recompilation). No game code, data or executables are published; everything below runs against the owner's own game files.

**The whole mod runs on the PC build.** The recompiled build now uses CFB Revamped's own executable with every code change this project makes (138 teams, 12-team playoff, user-played playoff games, 2026 start year, modern rules, 60-season Dynasty, UI and news fixes), reading the modded game data through a read-only overlay. A fresh Dynasty played a full 2026 season on it: all 14 regular-season weeks, conference title games, the 12-team CFP (Texas beat USC 34-13 in the final, champion recorded and in the ESPN news), the coaching carousel and other off-season stages, and rollover to Pre-Season 2027. The season checker passed all 15 structural checks, and the 2027 schedules were complete. Exhibition games between added schools (Kennesaw State at Delaware) load with the correct stadium, field, uniforms and conference banner.

**Super Sim scores fixed.** Super Sim games on the PC build had been ending 60-80 points a side with every extra point missed, on the stock game and the modded one alike (Dynasty week sims were normal). The cause was in the recompiler, not the mod: 13 vector integer instructions read the PS3's big-endian vector lanes in the PC's byte order. The game computes its rating-weighted sim chances with those instructions, so a kick-block chance came out around 227 % instead of about 2 %. With the instructions corrected (checked against a reference implementation on random inputs: 13 failing before, 0 after), a Super Simmed Mississippi State at Alabama ended 7-38 with every kick good and realistic team stats (526 vs 175 total yards).

**Faster, steadier boots.** Most long boots and apparent freezes at the coin toss came from the frame clock waiting on environment-variable lookups and on shader compiles. A lock-free cached lookup, a persistent shader cache and a cheaper surface search fixed them: the title screen appears in about 16-34 seconds instead of several minutes, and New Dynasty reaches the pre-season hub.

Still open on the PC build: speed (gameplay runs at roughly 2-4 frames per second; real play needs about 30), an occasional hang during a Dynasty week advance, and full playtesting of user-controlled games.

## 2026-10-12 - Modern clock rule confirmed at runtime; CFP logo installed; PC port renders the field

**Modern clock rule (CFB Revamped), runtime-tested on the installed v24 stage, no code changed.** Stock stops the game clock on every first down (verified against an old-rule baseline, frozen at 2:34 mid-second-quarter). With modern-rules v2, a first down outside the final two minutes of a half now lets the clock keep running through the pre-snap sequence; inside the final two minutes it stays stopped until right at the snap. Confirmed in an Exhibition game and separately in a fresh Dynasty game advanced to 2027. Modern overtime and the two-minute timeout, both already runtime-tested, are unaffected.

**CFP logo.** Our own original College Football Playoff artwork (First Round and National Championship marks, drawn from scratch, no traced or game-derived art) is installed, and the four first-round playoff rows now point at it in place of the donor bowls' marks. Two items are still open: a small results-list bowl badge still shows the donor bowl, since it reads a different field than the one that was changed; and the main 256x256 logo screen itself still needs an in-game visual check, since no playoff participant has reached that screen yet in this project.

**PC port (ps3recomp) side track, Step 33.** The field previously rendered as a black, speckled texture because a GPU-to-main-memory readback was being resolved into VRAM instead of main memory; with that fixed, the field now renders correctly (grass, yard lines, logos, end zones). On-field players are not drawn yet (only shadows, the HUD and a referee render); that and general image quality are the next items. Remains a side track: no game code or data is published.

## 2026-10-12 - Full 60-season Dynasty from 2026 through 2085

- **The stock game only plays 59 seasons.** A built-in check refuses Start Season at the 60th pre-season (2072 in stock, 2085 with our 2026 start). A two-word fix moves that end to Pre-Season 2086, so all 60 seasons (2026-2085) are playable.
- **Menus show 2026-based years.** Every UI screen derived its years from a hard-coded 2013, including a copy inside CFB Revamped's update archive. Patched to 2026, so the season tile reads 2026 and the career chart runs from 2023.
- **Long-Dynasty crash fixed.** Late in a 60-year Dynasty, the Coach Contract screen's chart (one column per season) ran the UI out of memory, a stock defect that only shows in very long Dynasties. The chart now shows the most recent 20 seasons.
- **History tables enlarged** for 138 teams over 60+ seasons (team, bowl and conference-championship history and coaching records), at a fixed cost of about 23 KB in a save that still has over 1.2 MB free.

Runtime test: a Dynasty moved to 2085 played the regular season, conference title game and 12-team playoff (national title 42-31), accepted a contract extension and reached Pre-Season 2086, where the "60 Year Dynasty Complete" screen appears as the intended end.

## 2026-10-12 - Modern overtime and clock rules; native build reaches the Dynasty hub

**Modern rules (CFB Revamped), runtime-tested:** after a touchdown from the second overtime a two-point try is required, and from the third overtime each possession is a two-point play from the 3-yard line. The first runtime test showed the CPU could still kick an extra point, because the original change only filtered the play-call menu; the fix scores a kicked try as zero and steers the CPU to a two-point play. Retest: three overtime games, every try worth 0 or 2, the CPU attempting two-point conversions, no crashes. The two-minute timeout at 2:00 of each half works; the running clock after first downs is in place and still being verified in isolation. Simulated games and Dynasty weeks ran without problems.

**Native Windows build (side track):** the title screen, main menu and a Dynasty hub (loaded from one of our playoff test saves) now render correctly. Starting a game is the next blocker.

## 2026-10-12 - Weekly CFP projection, campus first round, stand-in stadiums

Runtime-tested together on CFB Revamped in a fresh Dynasty through a full season, playoff and rollover with no crashes:
- **Weekly CFP projection:** from week 8 the playoff selection runs every week, so ESPN > Bowl Projections shows an "if the season ended today" bracket (CFP First Round 5 vs 12 ... 8 vs 9, quarterfinal byes for seeds 1-4). The old placeholder bowl teams are gone, and the real field replaces the projection after championship week.
- **First-round games at the higher seed's stadium,** as in the real CFP, with normal home-game presentation. Four campus first-round games were simmed without problems.
- **Stand-in stadiums:** FIU, New Mexico State and UConn have their own stadiums again; other added schools use unbranded stadiums of a fitting size (Sam Houston about 14,000 instead of 47,000).

Also from this round: the CPU-sim stat review found scoring, passing and rushing averages within about 3 percent of real FBS figures. Home-field advantage is weaker than real (about 55 percent home wins versus 63), the same as in the stock game. Modern overtime and clock rules are built and in runtime testing.

## 2026-10-11 - Native Windows build side track: first real frames

The experimental native Windows build (static recompilation with ps3recomp, run against the owner's own game files) now draws the game's intro movie through DirectX 12, with no emulator involved. Getting there took fixes to system-call coverage (memory containers, SPU event ports, the default GCM command buffer, the system cache mount, network sign-in state), SPU interpreter correctness (verified against a reference opcode by opcode), SPU code speed (about 2.3x faster), and RSX command-stream handling. Input reaches the game, profiles load, and sound plays but is mostly silent until SPU speed improves. The next blocker is a graphics command corruption right after the main-menu movie. This remains a side track; no game code or data is published.

## 2026-10-11 - Own uniforms, fields and stadiums for added schools; CFP news fix; more code room

**Team art (CFB Revamped), runtime-tested:**
- Delaware: community uniform pack (7 combinations including Midnight and Blackout), its own field and Delaware Stadium, re-homed so Eastern Michigan is untouched.
- Kennesaw State: uniforms built from community textures (Home black, Away white, Black, Grey and Yellow alternates) and its own field.
- North Dakota State: its own field in a Fargodome stand-in, plus CFB Revamped's NDSU uniform pack (green and gold), with Northern Illinois unchanged.
- FIU, New Mexico State, UConn and UMass: their original NCAA 14 uniforms and art restored under new codes, so they no longer show the schools CFB Revamped repainted over them.
- Real team colours for all 17 added and restored schools (menus, matchup panels, scorebugs).
- Exhibition team list now sorts the added schools alphabetically, and the new stadiums appear in Select Stadium.

Thanks to clmzntyger (Kennesaw State) and FootballGamer42 (North Dakota State field) for community art; the Delaware pack author is being confirmed. Community and game art stay out of this repository.

**CFP news fix:** wins in the first round, quarterfinals and semifinals no longer generate "season over" stories. It is the first code placed in newly found free space after the game's code segment (about 54 KB on CFB Revamped, 3.75 KB on stock), which gives room for larger features such as playoff format options and modern rules.

## 2026-10-11 - Added schools selectable as your first job and playable on the field

- **Choose Your First Job** now lists all 138 schools. The job list was built in a 126-row table and the added schools were cut off; a one-word fix raises the cap. North Dakota State was picked and run as a user team.
- **Bowl-week header** no longer reads "WEEK 256"; it shows "BOWL WEEKS, 2026". ESPN headlines name the CFP rounds ("Cotton Bowl CFP Semifinal ...").
- **Sam Houston's logo** was mapped to Sacred Heart's; it now uses the Bearkats "SH" mark from CFB Revamped's library. The other 16 mapped logos were audited and are correct.
- **Rendered games with added schools**: exhibition games with North Dakota State (home and away), Sam Houston, Kennesaw State and Delaware (including two additions against each other), and three Dynasty weeks played from the hub plus a full Dynasty season, all loaded and played with no hangs. An earlier freeze while loading a bowl game did not reproduce.
- Added schools still use borrowed stadiums, fields and uniforms (for example Air Force's Falcon Stadium or Northern Illinois's field); their own art is the next graphics step.

Also built, not yet runtime-tested: a fix that stops CFP first-round, quarterfinal and semifinal wins from producing "season over" news. It is the first patch placed in newly found free code space after the game's code segment (about 54 KB on CFB Revamped), which gives room for larger features.

## 2026-10-11 - Added schools show their own logos

The 13 added schools and the restored ones now use their own logos from CFB Revamped's logo library instead of borrowed ones. In a fresh 2026 Dynasty with the full stack, the schedule and scores screens showed the right logo for North Dakota State, Sam Houston, Missouri State, Kennesaw State, Delaware, Liberty, Jacksonville State, UConn, FIU and New Mexico State. The season and rollover ran with no crash and all checks passed. Playoff trophies were also renamed to CFP names (data only; on-screen confirmation pending). Uniforms, fields, banners and 3D logos for the additions are the next art steps; only a few additions have uniform art in CFB Revamped.

Found along the way: added schools are not offered in the "Choose Your First Job" list, and with user-played postseason games enabled, Advance also stops at a user team's regular bowl game.

## 2026-10-11 - Two full seasons from 2026 on CFB Revamped with everything enabled

A fresh Dynasty on CFB Revamped with the whole stack (138 real 2026 FBS teams, 12-team playoff with champion auto bids, user-played postseason games, the 2026 start year and the coach-contract fix) ran 2026 and 2027 and rolled over to Pre-Season 2028 with no crashes. Florida won the 2026 title and Georgia the 2027 title, each recorded once. After each rollover all 138 FBS teams were present and no team was without a head coach or coordinator. The 2027 playoff ran in weeks 17/19/20/21 as the calendar model predicts. The user team's Texas Bowl stopped Advance for a user-played game as intended.

Still to check for the start year: the 2028 calendar shift, the 2085 end of a 60-season Dynasty, and the national-title trophy year display.

## 2026-10-11 - Dynasty starts in 2026; added schools keep their coaches

**Start year 2026.** Moving the Dynasty to 2026 took 47 code words, not the two base-year constants first identified: calendar anchors, championship history encoding and on-screen years all derive from the base year. On CFB Revamped with the full stack (138 teams, 12-team playoff, champion auto bids, user-played games), a fresh Dynasty showed Pre-Season 2026, its schedule matched real 2026 dates (opening Saturdays Aug 29 and Sep 5, conference title games Dec 5), the playoff landed in weeks 17/19/20/21 and Arkansas's title was recorded as 2026. The calendar model shows that in some later seasons (2028-2030 among them) the whole bracket shifts one week later, which the engine already handles. A follow-up fixes the national-title trophy year.

**Coachless schools.** Rolling over exposed a bug: five schools (FIU, New Mexico State, UConn, Kennesaw State and Sam Houston) lost their head coaches and a recruiting step then crashed. Root cause: the end-of-season contract step only processed the first 378 coaching contracts (126 teams x 3); the 36 contracts of the added schools were never aged or renewed, and on CFB Revamped they were released without the jobs being reopened. A 14-word fix resizes that step and two related loops, and a separate 4-word guard keeps the recruiting-board lookup in range. Retest from a saved conference-championship week: all contracts processed, no team without a head, offensive or defensive coordinator, no crash, rollover to the next season clean.

## 2026-10-11 - 138 teams and the playable 12-team playoff run on CFB Revamped

The CFB Revamped (v21) port passed every runtime stage, each in a fresh Dynasty with a CPU-simmed season and a rollover, then rolled back cleanly:

- Engine only at 126 teams: 15/15 fresh-Dynasty checks against an unmodified control, byte-identical cold reload, 28/28 season checks, 26/26 rollover checks.
- All 138 real 2026 FBS teams in CFB Revamped's database: 138 FBS present with the 2026 conferences and additions (Idaho excluded), byte-identical cold reload, ACC 8 / Big Ten 9 conference games, seven conference championship games, rollover to 2014, and a live memory probe of the patched code.
- 138 teams plus the 12-team playoff: CFP names on the bowl screens; Ohio State won the title, recorded once.
- 138 teams plus champion-based auto bids and user-played playoff games: Advance stopped at each of the user team's games (a first-round win, then a quarterfinal loss to Michigan); Washington won the title, recorded once.

The playoff and user-play patches were mapped onto CFB Revamped's executable word by word (515 and 250 words, every original instruction checked), alongside the 552-word engine change. No crashes in any stage.

The native Windows recompilation side track is parked with the game running under D3D12 but showing a black screen; the remaining blocker is one coprocessor job, likely the archive decompressor. Notes are kept for a later session.

## 2026-10-11 - Users can play their own playoff games

A user team in the 12-team playoff is now offered each of its playoff games. Previously the stock game treated bowl season as one week and took a team's first postseason game as "its" game, so later rounds were CPU-simmed. The new patch (U2, 252 words) makes Advance step through bowl weeks one at a time with normal end-of-week processing, so the bracket fills in as it goes, and stop only when the current week holds the user's next unplayed game.

Runtime test (fresh Dynasty, all 138 real 2026 FBS teams, user Alabama as the 9 seed after losing the SEC title game): Advance stopped at each round with Play Game against the right opponent. Alabama won 34-18 at Miami in the first round, upset top seed Ohio State 27-24 in the Rose Bowl quarterfinal, then lost 27-24 to Missouri in the Peach Bowl semifinal. Advance then simmed the rest; Missouri beat Notre Dame 19-17 and the title was recorded once. Games were played through the in-game Super Sim with no crashes, the ticker showed earlier-round finals, and bowl presentation (Rose Bowl field art, "CFP Quarterfinal/Semifinal" headers) appeared. Regular-season Advance is unchanged.

Known cosmetic issues: a "WEEK 256" hub header before the first-round game, trophy popups that name the stock bowl, and news text that treats the first-round win as a season-ending bowl. First-round games are played at bowl stadiums instead of the higher seed's home, a deliberate workaround for an earlier Super Sim crash at campus sites; moving them on campus is on the list.

The native Windows recompilation side track now links and runs the game's own code: DirectX 12 starts and the game issues real draw calls before stopping at its one coprocessor (SPU) job, which is the next piece to implement. No game code or data is published.

## 2026-10-11 - Champion-based playoff bids pass; user-played playoff games are the next fix

Playoff v3 passed a full in-game season with all 138 real 2026 FBS teams (fresh Dynasty, CPU sim). Conference championship game winners now take the automatic bids (Ohio State, Stanford, Texas and Oklahoma State won their title games; Oregon State took the Pac-12 bid as standings leader since that conference has no title game). Every bid matched the game's own conference-champion history. First-round upsets (Oklahoma State over Nebraska, Oregon State over Wisconsin) and a semifinal upset (Texas over Ohio State) advanced correctly. Alabama beat Texas for the title, which was recorded once, and the rollover to 2014 was clean. There were no crashes. An earlier attempt was invalid because the playoff patch file failed to load silently; installers now check patch files before installing and a post-boot check confirms every expected patch applied.

New blocker found by playtesting: a user team that makes the playoff is never offered its playoff games. The stock game treats all of bowl season as one hub week, and every lookup of "the user's game" takes the team's first postseason game, played or not. A team with several playoff games is therefore stuck on its first one, and a bye seed (whose first game has a TBD opponent) sees "Bye Week". Advance then CPU-sims the whole bracket. A 133-word fix (earliest unplayed game, Advance stops before each user round) is built and in testing.

Tooling: patch logic can now be written in C and compiled into PowerPC code caves (clang via zig, ELFv1, no TOC use, with build guards). A re-implemented playoff helper matched its hand-written version word-for-word in size and behaviour. A feasibility spike also tested statically recompiling the game to native Windows with ps3recomp: about 93.5% of functions translate cleanly and the output compiles; a boot-to-menu attempt is running as a side track. No game code or data is published.

## 2026-10-11 - Four-season Dynasty with 138 real 2026 teams and the 12-team playoff (stock build)

The combined mod ran four consecutive seasons (2013-2016) in one fresh Dynasty, each with conference championships, the 12-team playoff, a recorded champion and a rollover, then cold-reloaded byte-identical at Pre-Season 2017. Champions: Alabama (2013 and 2014, both 16-0), Georgia Tech (2015), South Carolina (2016). Alabama went 6-6 in 2015 and 2016 and missed the playoff, so selection follows results. There were no crashes.

The v4 data fixes held in every season: the 17-team ACC played 8 conference games and the 18-team Big Ten played 9, and enlarged history tables stayed within capacity (TPHS 576/720, RBKS 3609/4320, PLAC 3476/4100, TPRC 589/900). The save peaked around 7.01 MB of its fixed 8.28 MB. A live probe at Pre-Season 2017 passed 1,073 checks with 138 FBS teams.

Also built offline since the last update: playoff v3 (automatic bids to the conference championship game winner, in test now), a port of both the 138-team engine recipe and the playoff to the CFB Revamped executable (all words mapped and preimage-checked), and the CFB Revamped version of the 2026 lineup. Research found that the Dynasty start year comes from two code constants. Moving them to start in 2026 should keep the full 60 seasons (2026-2085); this is queued for testing.

## 2026-10-10 - 138 real 2026 FBS teams + native 12-team playoff together in one Dynasty (stock build)

The two core goals now run together in normal Dynasty play on the stock build. All 138 2026 FBS schools play in their 2026 conferences, and the native 12-team College Football Playoff decides the title. A fresh Dynasty showed CFP bowl names in the game's own bowl tie-in screen before the season, and its cold reload was byte-identical.

After a CPU-simulated 2013 season and conference championships, the playoff seeded twelve teams: Virginia Tech, Alabama, Georgia Tech, Boston College, Ohio State, Clemson, Texas A&M, Stanford, Texas, Wake Forest, Kansas State, and C-USA champion FIU. It played first-round games on Dec 11 and advanced winners through upsets: Stanford over top seed Virginia Tech, and Texas A&M over Alabama 21-18. Georgia Tech (15-0) beat Boston College for the title. The game's news and poll showed Georgia Tech as champion, and the save recorded the title once with one bowl-history row per playoff win. The rollover to 2014 kept the playoff calendar. All playoff, integrity and season checks passed. A live probe confirmed all 551 engine words and 510 playoff words with 138 FBS teams in memory (1,073 checks). There were no crashes.

The remaining failed checks are the known ACC and Big Ten conference-schedule counts. A v4 data update (ACC and Big Ten back to their table-driven schedule style, plus enlarged season-history tables) is now in a multi-season test.

## 2026-10-10 - Real 2026 FBS lineup: 138 teams in 2026 conferences complete a full Dynasty season and rollover (stock build)

All 138 2026 FBS schools now play natively in Dynasty on the stock build: the 125 original schools still in FBS plus 13 additions, in the 2026 conferences. Idaho is out of the Dynasty, with its data preserved for future FCS support. The additions use borrowed presentation from similar donor schools.

A fresh Dynasty passed 118 creation checks and a byte-identical cold reload. It then completed season start, a full CPU-simulated 2013 regular season, conference championship games and bowls (season checks 15/15 at both boundaries). Ohio State 14-0 beat Miami 45-14 for the title, and BCS order matched the media poll (rank correlation 0.999). The rollover to 2014 and a second byte-identical cold reload followed. A live probe passed 563 checks with 138 FBS teams in memory. There were no crashes or hangs.

This took the v3 engine recipe (551 words: active-N count changes, enlarged rating-sort frames, BCS constants scaled with the team count, and a bounded redshirt flag write) plus v3 data. The v3 data clears the 2013 conference membership slots used by the first-season scheduler and removes Idaho from the Dynasty.

Still open: the 17-team ACC gets no conference games and the 18-team Big Ten gets ten (the game's realignment schedule styles do not handle these sizes). Rolling history table TPHS is full, so multi-season play needs it enlarged. The new schools do not appear in the Choose Your First Job list. Graphics are borrowed. Next: conference scheduling, history capacity, combining with the playoff, then the CFBR port.

## 2026-10-10 - Correction: 138-team BCS rankings were wrong; real 2026 lineup plays a full season

Correction to the 138-team entry below: that run completed a season and rollover without crashing, but its BCS rankings were silently wrong. The BCS scorer turns each poll rank into points as 127 minus the rank, using constants stored next to the function. They were never updated for more than 127 teams, so teams ranked 128th or worse wrapped around to huge scores and the worst teams took the top BCS spots (the 2013 title game paired 1-12 Rutgers and 4-9 Eastern Michigan). The 127-team and stock builds are unaffected. A v3 engine recipe (551 words) scales these constants with the team count and is under runtime test.

The real 2026 FBS lineup (125 retained schools plus 13 additions in the 2026 conferences, with Idaho moved out of FBS) has now played a full 2013 season in a fresh Dynasty: season start, regular season, conference championship games and bowls, all checks passing. Two problems were found and root-caused along the way.
- Idaho was kept as a non-FBS team that still had players. Its players overflowed a 138-entry rating cache at season start. Removing its players fixed that.
- A stale conference membership table scheduled 2013 conference lineups. Clearing it fixed the schedules.

The rollover to 2014 then crashed. Idaho, now with no players, was used as a filler opponent; its games produced placeholder player rows that an unbounded write in the redshirt step turned into heap corruption. The v3 data removes Idaho from the Dynasty entirely, and v3 adds a bound check. Still open: the 17-team ACC gets no conference games and the 18-team Big Ten gets ten.

## 2026-10-10 - Native in-game 12-team playoff runs a full season and records the champion (stock build)

A native College Football Playoff now runs inside normal Dynasty play on the stock build (126 teams): no external tools or save editing. A small code hook replaces the stock BCS tie-in filler. At the end of championship week it seeds 12 teams (the five highest-ranked conference champions plus seven at-large, straight seeding by rank). It fills four first-round games (5 vs 12, 6 vs 11, 7 vs 10, 8 vs 9) at bowl sites on Dec 11, and after each round it writes the winners into the fixed bracket: quarterfinals Dec 25 (seeds 1-4 with byes), semifinals Jan 1, then the title game. The bowl calendar and CFP round names come from the Dynasty template's BOWL table.

Three runtime iterations: v0 built a correct field but its BOWL changes went to an archive new Dynasties do not read, so stock dates broke the bracket. v1 moved the data and displayed CFP names and dates and played every round, but the national title was not recorded. The game's history and champion recorders look up a team's first postseason game, which is the quarterfinal for a finalist. v2 makes those two lookups use the game's team pair instead. Final run: fresh Dynasty, CPU-simulated season and every playoff round. Alabama, seeded first, beat Notre Dame 38-17. National title count rose by one with the correct year, and every playoff win was recorded once under its own bowl. The 2014 rollover recreated the CFP rows. All checker boundaries passed, with no crashes. The patch is 510 instruction words and is verified offline by an instruction encoder, Ghidra decoding and emulation with a write-watch.

Known limits: Super Sim of a playoff game crashed once in v0 (cause unconfirmed; stock Super Sim of a bowl game works), so CPU simulation is the tested path. Trophy popup and some news text still name a team's first playoff bowl. Only straight seeding fits. Not yet combined with the 138-team build or ported to CFBR.

## 2026-10-10 - 138 active FBS teams through a full season and rollover (stock build)

For the first time the game ran with 138 active FBS teams: the 126 originals plus 12 placeholder Independents ("Expansion 01-12", Idaho-based copies). The stock-build engine recipe was generalized to a team count N. Of the 127-team recipe's 517 instruction words, 72 depend on N: 126 to N, 125 to N-1, the logical end 1008 to 8N, and one float 1/N. The rest is storage already reserved for 160 teams. A first-season schedule gives all 138 teams 12 games with no collisions, and every original FBS-vs-FBS game keeps its week.

The first 138-team run created and cold-loaded a Dynasty (143 teams; fixture/schedule/stadium checks 90/25/34; live probe 527) but crashed when the season started. Root cause: three team-rating functions (TV Exposure, Pro Potential, Program Tradition) sort teams in stack arrays sized for exactly 126 records. The size appears only as a byte count, so the earlier audit missed it, and 138 records overwrote saved registers. A coach list has the same latent pattern. A v2 recipe adds 19 words that enlarge those frames for 160 teams, following the existing 127-team fix of the same sort. With v2, the same save cold-loaded byte-identical, started the season, and simulated a full 2013 season (Alabama beat Expansion Test 38-14 and finished 14-0), the postseason and the rollover to 2014. The rollover check passed 59/59. All 12 added teams signed recruiting classes (7-15 each), and the live probe passed 546 checks with 138 FBS in memory. Two season-check failures were checker artifacts: a hardcoded user team from the 127-team trial, and a mid-season zero-commitment count for one added team that later signed 10. The rolling history tables are at or near capacity (TPHS 572/572, RBKS 3618/3643) and must be enlarged before multi-season play. Rolled back; preservation checks pass. This proves the engine path at 138 on the stock build only. It does not yet add real 2026 schools, conferences or presentation, and the CFBR build still needs the recipe ported.

## 2026-10-10 - First added team identity survives Dynasty, season and rollover

The first identity added inside the 138-team reserve passed a full ladder at unchanged 126 FBS. BOOT entry 355 gained one team row, TGID 165 "FCS Test", cloned from a shipped generic FCS row, plus three coach rows (36 offline checks). Template 354 was unchanged. A fresh Dynasty contained 132 teams instead of 131, with the new identity exactly once (20 checks). A cold reload left all four save files byte-identical. The Dynasty then simulated the 2013 regular season (28 checks), postseason (28) and rollover to Pre-Season 2014 (30). Grown capacities held at every snapshot (7 checks each), and both live code probes passed. The game's own 2014 schedule generator gave the added team seven games, so the engine treats an added identity as a schedulable team. Two checker expectations were corrected and rerun: Dynasty creation marks every generic FCS row visible (not only the new one), and the season checker now takes the team count from the prior save instead of a fixed 131. Profile rolled back; 48 protected stock files unchanged. No FBS membership change, engine patch or manual save edit. See [roster pipeline](docs/ROSTER_PIPELINE.md).

## 2026-10-10 - CFBR grown Dynasty tables survive a full season and rollover

A coordinated BOOT grew both the Dynasty template (entry 354) and the minimal-reserve roster (entry 355) to TEAM 153, PLAY 9,660, DCHT 12,144, COCH 439, CSKL 414 and STAD 210, still at 126 FBS teams. A fresh offline Dynasty saved with all six grown capacities, and a cold reload left the save files byte-identical (21 checks). The Dynasty then simulated the 2013 regular season (28 checks) and postseason (28 checks), and rolled over to Pre-Season 2014 (30 checks). Capacities never shrank (seven checks per snapshot). Six live reads passed per run. After rollback, 48 protected stock files and 58 original-preservation checks passed. A roster-only BOOT does not grow Dynasty tables; the template must change too. No added identities, code changes or manual save edits. See [roster pipeline](docs/ROSTER_PIPELINE.md).

## 2026-10-10 - CFBR grown roster capacities survive native save and cold load

An isolated capacity-only BOOT trial passed 48 checks at unchanged 126 teams. Only BOOT entry 355 changed, to the minimal 138-team reserve database: TEAM 153, PLAY 9,660, DCHT 12,144, COCH 439, CSKL 414 and STAD 210. Records, schemas and counts were unchanged. In a clean profile, the first boot had no roster auto-load; a roster was saved through File Management. The game's own serializer kept all six grown capacities. A fresh process auto-loaded the roster with all four save files byte-identical. Six baseline live reads passed in each run. After rollback, 48 protected stock files and 58 original-preservation checks passed. No added identities, code changes or manual save edits. This does not prove engine-side team limits, Dynasty creation or seasons with the grown tables. See [roster pipeline](docs/ROSTER_PIPELINE.md).

## 2026-10-09 - CFBR roster source, native save and cold load verified

An isolated source-only BOOT trial passed 32 checks at unchanged 126 teams. The game selected the intended CFBR23V21 database, wrote a roster through its own menus, and auto-loaded it in a fresh process. The complete USR matches the source; all ten tables and all four cold-save files are unchanged. Six baseline live reads passed in each run. Profile rollback completed, 48 stock save files and 58 prior CFBR home files stayed unchanged, and 58 original-preservation checks passed.

Documented a bounded container recognizer (13 checks including nine rejection cases) and a minimal reserve budget (ten offline checks, 78,600 additional bytes). Neither proves changed-container or larger-team acceptance. See [roster pipeline evidence and next gates](docs/ROSTER_PIPELINE.md). No new engine patch, expanded membership or installable release.

## 2026-10-09 - CFBR patched season passed; playable-team integration priority

The four-word ranking patch passed a normal 2014 season, stock postseason, 2015 rollover and separate cold load at 126 teams: checks 28/28/30, six live reads in each run, four unchanged cold-save files, 48 protected stock files and 58 original-preservation checks. The trial is rolled back. Producer execution coverage and expanded CFBR membership remain unproven.

Added an [agent-neutral developer handoff](docs/DEVELOPER_HANDOFF.md). Target 138 active 2026 FBS identities, with Idaho deferred and graphics last. A ten-check input map reconciles the proposed schools and conferences without assigning IDs. An offline auto-loaded-roster leading TDB reserve passes 19 preservation checks; outer save packaging remains open. Static review identified CFBR's twelve-byte recruiting records as a concrete incompatibility with stock eight-byte relocation values.

## 2026-10-09 - CFBR archive adapter and offline reserve candidate

Added a format-aware BGFA library and 16 synthetic tests. It handles stock and CFBR index widths, nested framing, compression, source/preimage checks and append-only entry replacement. All 4,840 entries across four pinned archives match the existing independent parser. A private CFBR candidate passes 34 offline checks while retaining 126 FBS membership and all 825 unrelated BOOT entries. No candidate was installed or runtime-tested. See [archive adapter evidence and limits](docs/ARCHIVE_ADAPTER.md).

The interrupted ranking-season run was no longer active when work resumed. Its save remained at the preserved Week 1 of 2014; all four save files matched. Restored the pending patch/profile configuration, with 48 protected stock save files unchanged and 58 original-preservation checks passing. A completed patched season is still unverified.

## 2026-10-09 - Debugger limitation and recovered trace experiments

Execution coverage remains unverified. RPCS3's LLVM backend rejects PPU breakpoints even though its GDB server replies OK; a separate interpreter experiment also failed to obtain the requested stops. An early-attach trial could not progress beyond title screens and hung during shutdown, requiring the emulator's termination dialog. Restored the working profile and patch configuration; all 48 protected stock save files and 58 original-preservation checks passed. Patched-season validation remains pending.

## 2026-10-09 - CFBR season control and reversible patch

Unmodified CFBR completed the 2013 season and normal rollover into 2014: 28 regular-season checks, 28 postseason checks and 30 rollover checks passed at 126 FBS teams. Ten recruits matched Alabama's next roster; checked championship histories persisted. A separate four-word ranking patch passed install/live-memory/cold-load/rollback checks with unchanged saves. Patched full-season and expanded-membership acceptance remain pending.

## 2026-10-09 - CFBR isolated baseline

Verified the running update 1.02 executable against the analyzed ELF, created a fresh Dynasty and cold-loaded it with all four save files unchanged. Fifteen structural checks passed at 126 FBS teams. Recorded automatic loading of the bundled 2023 roster and a corrected roster-source assumption. Restored profile configuration and verified 48 protected save files plus 58 original-preservation checks. Expansion and playoff integration remain unfinished.

## 2026-10-09 - CFBR integration investigation

Pinned official v21 sources and staged the PC disc package privately. Verified update 1.02 has a different executable (0/517 existing patch preimages match), measured archive changes and confirmed five school-ID conflicts in the bundled roster. Added a separate compatibility track and acceptance gates. No CFBR files published or installed; no new runtime success claimed.

Entries describe the observed test scope. Candidate numbers are development iterations, not public release versions.

## 2026-10-09 - Candidate v6: serialized reserves at 127 active FBS teams

- Enlarged selected serialized capacities while retaining the same 517 executable patch words, initial schedule recipe and 127 active FBS teams. This is not proof of 160 active teams.
- Fresh creation passed 35 checks, exact schedule and stadium checks passed 12 each, and fresh cold reload preserved all four save files.
- Normal simulation completed the regular season, stock postseason and offseason. The prototype finished 1-11 with 13 class commitments. Arizona finished 10-4 and won the Pac-12 championship.
- Normal rollover into 2014 passed 46 saved-system checks, retaining all original teams, complete schedules, roster/depth references, stadium joins, the 17 expected capacity values and the checked championship metadata. Thirteen recruits matched prototype roster identities. The prototype has 11 FBS opponents and one FCS opponent in 2014.
- Cold reload preserved all four files. The depth chart independently confirmed freshman Jake Bracken, TE #86, 6 ft 4 in, 250 lb, OVR 67. Fresh, rollover and cold live probes passed 526 checks each. Lifecycle/preservation passed 39 checks; original preservation passed 58. Trial files were rolled back.
- A separate history audit found missing prototype TPHS/RBKS rows at creation and incomplete record-type coverage after v5 simulation. Their initialization, pruning and capacity limits remain open. These gaps are not covered by the passed championship-metadata checks.
- Full membership, repeated seasons, realistic content, the custom playoff and a public installer remain unfinished.

## 2026-10-09 — Candidate v5: rollover and cold reload

- The same 517-word/BOOT/MISC candidate completed normal offseason simulation into 2014 without save edits.
- Thirty-nine saved-system checks passed: all 132 teams/127 FBS retained, complete schedules without weekly collisions, roster/depth references, unique stadium links, history and serialized reserves.
- Eight recruits matched prototype players on all checked identity fields. A ninth, Caleb Wilson, matched name, hometown, height, weight, tendency and class with a position change from LG to RG. Two other committed recruits on the prototype's board matched players on different teams; board membership plus commitment status does not identify the destination team.
- The prototype has 11 FBS opponents and one FCS opponent in 2014.
- Cold reload passed five checks with all four files unchanged. The in-game depth chart confirmed Blake Vogel, freshman TE #87, 6 ft 6 in, 265 lb, OVR 64.
- Both live probes passed 526 checks; aggregate lifecycle/preservation passed 35; original preservation passed 58. All four trial files were rolled back.
- Repeated seasons, full-FBS capacities/content, coach selection and the custom playoff remain open. No installable release.

## 2026-10-09 — Candidate v5: initial FBS schedule experiment

- Traced first-year known matchups to SKNW in a packaged schedule database. All 726 season-zero presets exactly matched both captured stock and expanded 2013 schedules. The added team had no preset entries. Later seasons also contain presets, in smaller numbers.
- Prepared a reversible MISC asset recipe replacing 12 FCS matchup slots with 12 distinct FBS opponents for the prototype. Balanced its venues at six home/six away. Moved one matchup into the original opponent's open week because two constrained weeks otherwise required the same opponent.
- Kept the 517 executable patch words and unique-stadium BOOT candidate from v4 unchanged. Original FBS-versus-FBS matchups and weeks are preserved.
- Passed 21 offline asset/projection checks, 28 fresh-Dynasty structural checks, 12 exact-schedule checks, 12 stadium checks and five cold-load/preservation checks.
- Normal simulation completed the regular season and stock postseason. The prototype finished 0–12 with nine recruiting commitments and saved team statistics. Arizona finished 9–4. Fresh and completed-season live probes each passed 526 executable/index checks.
- At this checkpoint rollover was pending. Trial files were rolled back after preserving the end-season fixture; the later rollover result appears above.
- Added this public progress repository, installation-status documentation and a read-only executable-identity tool. No installable release published.

## 2026-10-09 — Candidate v4: independent stadium identity

- Assigned the prototype a separate stadium identity while retaining the donor's model.
- Normal fresh creation saved 198 unique stadium identities. Save/load preserved the result.
- Loaded the borrowed indoor stadium and players. A live kickoff/return occurred; the remainder was completed with in-game Super Sim at the user's request.
- The prototype's 33–14 result, statistics and record survived a cold reload. No full manually played game was claimed.

## 2026-10-09 — Candidate v3: transfer buffer and rollover

- Identified a transfer-stage allocation limited to 126 records. The expanded team/stadium join exceeded that allocation.
- Added a bounded reserve patch; a normally resumed Dynasty reached preseason 2014 and cold-loaded successfully.
- All 127 FBS teams retained schedules. Five committed recruits matched prototype players after rollover.
- Duplicate stadium identity and first-year FCS-only scheduling remained separate defects at that checkpoint; later candidates address them.

## 2026-10-09 — Earlier expansion iterations

- Enlarged dependent runtime storage and serialized reserves, with stock-count regression tests before active-team trials.
- The first added-team trial had no games. Correcting the prototype's duplicated TOID produced 12 games without removing an original team.
- Those first-year games were all against generic FCS opponents. This was recorded as a scheduling failure, not accepted as a realistic schedule.

## 2026-10-08 — Reproducible executable baseline

- Verified the original dump and isolated the working emulator, saves and experiments.
- Matched analyzed ELF bytes, OPD/TOC and runtime memory to the loaded module.
- Established a local Ghidra PowerPC analysis workflow without requiring REA support.
- A diagnostic thread-name patch passed an unpatched/patched/restored observation test.
