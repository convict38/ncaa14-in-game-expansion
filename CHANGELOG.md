# Changelog

## 2026-10-31 (late night) - PC port: the "Autosave in Progress" hang is found and fixed in a test build; FCS recruiting levels separated

This changes only separate PC-port test builds. The normal game, its saves and its data are untouched. No game code, data or images are published.

**The autosave hang.**
- **Cause.** The PC port keeps a fixed list of 64 game threads. The game starts a short-lived helper thread for every save, every load, every trophy and every video. When such a thread finished, the PC port never gave its place in the list back. After about 63 threads in one session the list was full, the next save could not start its helper, and the game waited forever on "Autosave in Progress".
- **It is not caused by the bigger FBS+FCS universe** and it can also happen in the normal PC-port play build: after roughly 15-20 saves or loads in one sitting (fewer if trophies or videos come up). Until the fix is in the play build: if it happens, quit and restart; your last save is safe.
- **Fix (new switch, on by default in the test builds).** Finished helper threads now give their place back when the list is full. Nothing changes before the list fills up. Tested by shrinking the list on purpose: without the fix the game hung on the next load, with it the game loaded, saved at each step and played into the new season with no hang. The fix still has to be moved into the play build.

**The 2031 to 2032 off-season is finished.**
- No four- or five-star recruit signed with an FCS school; every school has full rosters and a full coaching staff, and contract numbers are clean.
- After the new season's ratings, the FCS levels are in order (team ratings 74 / 72 / 70 / 69 / 67 from top level to bottom; FBS 86).
- In the first four weeks of 2032 FCS teams won 23 % of their games against FBS (2031: 28 %), and the top level wins far more often than the bottom one. This is still above the planned rate; the new recruit classes have only just started to reach the lineups.

**Top FCS level separated from the second.**
- The last signing step used to offer only one-stars, so hundreds of two- and three-stars went unsigned while the top FCS level filled up with one-stars. A new switch lets FCS schools pick from the leftover two- and three-stars in that step, and the top level no longer takes the leftover one-stars.
- Result for the 2032 classes, top level to bottom: 61.0 / 59.5 / 57.9 / 56.2 / 53.5 overall (before: 58.0 / 58.5 / 57.3 / 55.7 / 52.9), with normal class sizes. All levels are now in order; they are about one point above the target and will be fine-tuned with existing settings.

**Still to do.**
- Move the autosave fix into the play build.
- Make the new recruiting settings the default and fine-tune the level targets.
- Keep watching the FCS win rate through the 2032 season.
- A brand-new Dynasty with the new starting rosters has not been tested yet.

## 2026-10-31 (night) - FBS+FCS universe: top recruits stay at FBS schools all year

This changes only a separate PC-port test build. The normal game, its saves and its data are untouched. No game code, data or images are published.

**What changed.**
- **No more four- and five-star recruits at FCS schools after the season (new switch, on by default).** The star check from the last update now also runs at the moment each recruit signs, in every signing step. Before, a recruit whose FBS schools were full could still drop down to an FCS school in the big signing step after the season.
- **The FCS strength check now sees the whole incoming class.** It used to miss about 40 % of the new FCS players.
- **Coach contract numbers: no problem after all.** The earlier report of repeated numbers came from the checking tool counting deleted rows. Every live contract number is unique, and every school has a full coaching staff. The tool is fixed, and a small safety pass was added that removes any contract left without a coach; it found none.

**Tested in the game (2031 season through signing).**
- From week 1 to the end of signing, no four- or five-star recruit signed with an FCS school (2030: 9). All 34 five-stars and 330 of the 334 four-stars went to FBS schools.
- FCS classes by level, strongest to weakest: 58 / 58 / 57 / 56 / 53 overall.

**Still to do.**
- The top two FCS levels sign classes of the same strength. The top level should get more two- and three-stars.
- FCS teams won 28 % of their games against FBS in 2031. The ratings still come from older rosters, so this will be checked again after the next season.
- The save after the 2031 to 2032 off-season was not written because of a known, rare autosave hang, so that step will be run again.
- A brand-new Dynasty with the new starting rosters has not been tested yet.

## 2026-10-31 (evening) - FBS+FCS universe: the new recruiting tested in the game

This changes only a separate PC-port test build. The normal game, its saves and its data are untouched. No game code, data or images are published.

**What was tested.** The test Dynasty was played from the 2029 off-season through the 2030 season, the bowls and signing day, and into the 2031 season, with the realistic recruit classes and the star-gated FCS recruiting from the previous update.

**What works.**
- **Recruit classes look like real recruiting.** Each new class has about 34 five-stars, 334 four-stars, 1,900 three-stars and about 4,500 two- and one-stars, and the stars now match how good a player is (five-stars about 80 overall, one-stars about 50). It takes about 3 seconds when the season starts.
- **Top recruits go to FBS schools.** During the season 285 of 286 four- and five-star commitments went to FBS schools. The best FBS programs still sign top-20 classes; the best FCS class ranked 95th.
- **Each FCS level recruits differently.** The final 2030 classes average 59 / 59 / 57 / 55 / 54 overall from the strongest FCS level to the weakest (FBS 68).
- **Rosters and staffs stay full** through the off-season: FBS 70 players, FCS 68-70, every school with a full coaching staff.
- The weekly check costs about one second.

**Still to do.**
- FCS schools still signed 9 four- and five-stars after the season (before: 86 a year), through a late signing step the new check does not cover yet. That gets its own switch next.
- FCS teams still beat FBS teams about 23 % of the time in 2030, because the older FCS players were signed before this change. The planned rate of about 8 % should show after a few new classes.
- Coach contract numbers have run out of room and are being reused. Nothing visible yet; it will be looked at.
- A brand-new Dynasty with the new starting rosters has not been tested yet.

## 2026-10-31 (late afternoon) - FBS+FCS universe: realistic recruit classes, and top recruits skip FCS schools (built, not yet tested in the game)

This changes only a separate PC-port test build. The normal game, its saves and its data are untouched. No game code, data or images are published.

**What changed.**
- **Recruit classes look more like real recruiting (new, switchable).**
  - Before, a class of 6,700 recruits had about 740 four- and five-stars, and stars said little about how good a player was (some one-stars were rated 85).
  - Now a class has about 34 five-stars, 335 four-stars, 1,900 three-stars and a large group of two- and one-stars, and each star level has its own overall range (five-stars about 80, one-stars about 50).
  - A bug that made the weakest third of a big class look like top recruits to the computer schools is fixed.
  - Names, faces, bodies and hometowns stay as they were.
- **Top recruits all but ignore FCS schools (new, switchable).**
  - Before, FCS schools signed 86 four- and five-stars a year, and every FCS level signed the same kind of recruits.
  - Now FCS schools drop down the list of the schools a top recruit likes. Five-stars never pick an FCS school; a four-star does only very rarely, and only at the strongest FCS level. The best FCS schools land mostly two- and three-stars, the weakest mostly one- and two-stars.
- **The earlier FCS strength step is now only a light safety limit**, and the separate FBS / FCS rating scale is off: one shared scale, as decided.
- **New Dynasties:** the FCS starting rosters in the test data are rebuilt so the first season already matches the long-term balance, with freshmen to seniors spread like real rosters.

**What it should do (a model, not yet seen in the game).** Over many seasons the FCS levels settle at about 71 / 67 / 64 / 58 / 56, the best FCS team about 77 and the weakest about 51, FBS teams about 87, and FCS teams win about 9 % of their games against FBS, close to real life. The model can be off by about 4 points.

**Not tested yet:** the game run was not possible this session (the shared test queue was busy). It is the next step.

## 2026-10-31 (afternoon) - FBS+FCS universe: FCS recruits now depend on the school's level, and fewer broken real-life series

This changes only a separate PC-port test build. The normal game, its saves and its data are untouched. No game code, data or images are published.

**What changed.**
- **FCS recruit strength now depends on the level of the school (new, switchable).**
  - Until now every FCS school signed recruits of about the same strength (about 60 overall), whether it was one of the best FCS programs or one of the weakest. Over a few seasons that made all FCS levels end up equal, and FCS teams kept getting stronger against FBS teams.
  - Now, when the new recruits join their teams, each FCS level gets its own target: by default the new players average 60, 58, 56, 54 and 52 overall from the strongest level to the weakest (FBS recruits arrive at about 66 and are not changed). A better recruit stays better than a weaker one on the same team; only the level of the whole class moves.
  - All five targets, and how spread out each class is, are settings, so the balance can be tuned without a new build.
  - **Tested in the game:** at the change from 2029 to 2030 the five FCS levels' new classes went from about 61 each to 60.0, 58.0, 56.0, 53.9 and 52.0.
- **FBS-vs-FCS schedules.**
  - No FBS team gets more than 2 FCS opponents in a season (one FBS team had 3 in 2029).
  - The step that adds FBS-vs-FCS games no longer replaces real scheduled series. The 4 FBS games it replaced in 2029 (Indiana-Ball State, Baylor-SMU, Ohio State-Tulsa, Michigan-Colorado) turned out to be real future series in the game's data. In 2030 it kept 77 such series and still reached 104 FBS-vs-FCS games, with a clean schedule.
- **The 2029 season finished.** FCS teams won 19 of 106 games against FBS teams (18 %), well above the real-life 8-12 %. That was expected: the new recruit step only starts with the 2030 class.

**What it means over many seasons (a model, not yet seen in the game).**
- New players take three to four seasons to reach the starting line-ups, so in this test Dynasty FCS results should stay close to the 2029 level until about 2033 and then settle.
- After that, the model expects the FCS levels to stay apart for as long as the Dynasty runs, because every year's class is set again.
- **The choice that is left (for the user):** the rating scale asked for (best FCS team in the low 70s, worst FCS teams 40-50) and the real-life win rate (FCS wins 8-12 % against FBS) do not fully fit together:
  - the exact asked-for scale gives FCS teams about 5 % wins;
  - the default settings give about 8 %, with the best FCS team about 76 and the worst about 51;
  - about 10 % needs the best FCS team near 78;
  - without the new step, the model expects about 24 % wins and no difference between FCS levels.
  - These model win rates can be off by about 4 points either way.
- A one-time adjustment of the players already on FCS rosters would remove the three-season wait. It is not built yet.

## 2026-10-31 (midday) - FBS+FCS universe: the third season finished, why team ratings keep rising, and a fixed rating scale

This changes only a separate PC-port test build. The normal game, its saves and its data are untouched. No game code, data or images are published.

**What changed.**
- **The 2028 season ran to the end, and the Dynasty moved into 2029.**
  - **Bowl and title games.** The user's bowl game was played. The SWAC title game result was used for the SWAC champion and the Celebration Bowl, and it was stored in the conference champion history like every other conference.
  - **FBS teams play enough FCS teams.** The 2029 schedule has **106** FBS-vs-FCS games, close to real life. To reach that, 4 early-season FBS-vs-FBS games were turned into FBS-vs-FCS games. The schedule is still clean: 12 games for every FBS team, 11-12 for every FCS team, and no team plays twice in one week.
  - **Rosters are full.** With the bigger recruit class (6,700 players), every school starts 2029 with 59-70 players (only 3 FCS schools at 59, down from 13).
  - **Coaching staffs are complete.** Every one of the 266 schools has its 3 coaches.
- **Why team ratings rise every year.**
  - **Player growth.** Every player improves about 4.4 points a year, at every level.
  - **First-season rosters.** The players in the first-season rosters were too close in strength from freshman to senior. As those players get older, the starting line-ups get stronger for about four seasons. After that, the ratings level off: they do not keep growing for ever.
  - **FCS recruits.** New FCS recruits arrive at about the same strength whatever the school's level, so over time the strongest and weakest FCS conferences would end up about equal.
  - **What it is not.** It is not a bonus applied every year, not something that happens during a season, and not the walk-ons.
- **A fixed rating scale (new, switchable).**
  - The test build now keeps the team overall shown in the game on a fixed scale every season: FBS from 65 to 97, FCS from 45 to 72, which is the scale the user asked for.
  - The order of the teams is unchanged; only the numbers are rescaled, and the four limits can be changed in one setting.
  - In the 2029 test it worked as designed: FBS teams averaged 82, and the FCS levels averaged 67, 61, 59, 58 and 52.
- **But the rescaled number does not change who wins.**
  - The computer works out CPU-vs-CPU games from the players themselves, not from the team overall. In the first five weeks of 2029, FCS teams won 19 of 103 games against FBS teams (18 %), more than the real-life 8-12 %, because FCS players keep getting stronger.
  - Keeping results realistic needs a change at the player level (for example, recruit strength that depends on the FCS school's level). That is the next step.
- **New Dynasties get the bigger recruit class.** The data for a new Dynasty now has room for the 6,700-player class (built and checked, not yet played).
- Every change has its own switch and can be turned off.

**Still open.** A player-level fix so FCS teams stay at about 8-12 % wins against FBS over many seasons; the rest of the 2029 season; the final rating scale (the user decides); screens for the FCS playoff and FCS stat leaders.

## 2026-10-31 (late morning) - Super Sim tackle stats: cause found, fix tested in a separate test version

The normal game executable, the play build and the saves are untouched. The fix exists only in a separate test version and is off unless switched on. No game code, data or images are published.

**What happened.**
- **The cause.** When you Super Sim inside a game, each simulated play is turned into stats by one routine. For every tackle it gives the tackler a solo tackle. It never gives an assisted tackle, because the simulated play only remembers one tackler. On a tackle for loss or a sack it also counts the solo tackle twice. Plays you play yourself are different: there the game decides tackle by tackle whether it was solo or assisted.
- **Measured.** We looked at three bowl games that had been super-simmed in a test Dynasty. Both teams got 39 to 63 solo tackles and no assisted tackles (except 2, from one kickoff that was played live). In the computer-simmed games of the same week, 56 % of tackles were assisted. The total number of tackles was normal. But the game's tackle leader list counts solo tackles only, so after three super-simmed games the user team already had the national leader.
- **A correction.** Our first report said a normal simmed game has about 41 % assisted tackles. That was a mix-up of the two stat columns in our reading tool. The real figure is about 59 %: the normal sim makes 6 of every 10 tackles assisted.
- **The test fix.** With the switch on, Super Sim uses the same rule as the normal sim. Each tackle is assisted 6 times in 10 and solo otherwise. A tackle for loss or a sack counts once. A sack stays a full sack, because a super-simmed play never has a second sacker.
- **Tested.** Two playoff games were super-simmed with the switch on. They came out at 54 % and 66 % assisted tackles in the first game and 55 % and 46 % in the second, about 55 % overall, in line with the computer-simmed games. Total tackles stayed normal, and the user team's players left the top 10 of the solo tackle list. A third game with the switch off gave 0 assisted tackles, the same as before. There were no crashes, and the saves read back cleanly.

**Still open.** A whole season with the fix has not been played yet, and a fixed save has not been loaded back into the game. The fix is not in the normal build yet.

## 2026-10-31 (late morning) - FBS+FCS universe: more FBS-vs-FCS games after the first season, a played SWAC title game, and why some rosters were short

This changes only a separate PC-port test build. The normal game, its saves and its data are untouched. No game code, data or images are published.

**What changed.**
- **FBS teams play FCS teams again after the first season.** In the first season the schedule comes from the data, which has about 110 FBS-vs-FCS games, close to real life. From the second season on, the game makes the schedule itself. The part that adds FCS opponents was built for the original game's 5 placeholder FCS teams, so it only aims for 35-50 such games, and about 50 FBS teams already have full schedules by the time it runs. So 2027 had only 40 FBS-vs-FCS games.
- The test build now aims that part at 100-120 games and tries more weeks. It also makes sure no FCS team gets more than 2 FBS opponents. The 2028 schedule then had **90** FBS-vs-FCS games (up from 38), and every schedule stayed clean: 12 games for each FBS team, 11-12 for each FCS team, nobody playing twice in a week.
- A last step that tops the count up to about 105 is built but not tested yet. It turns a few early-season FBS-vs-FBS non-conference games into FBS-vs-FCS games.
- **How strong FCS teams are.** In the 2028 regular season FCS teams won 11 of their 90 games against FBS teams (12 %). Over the three test seasons it is 24 of 242 (10 %); in real life it is about 8-12 %.
- **The SWAC title game is now a real game.** At the start of conference championship week, the East and West division winners of the SWAC are put on the schedule and the game is played like the other title games. In the test, Jackson State beat Prairie View A&M 41-9. The FCS playoff code then uses that result for the SWAC champion and the Celebration Bowl. If the game has no result, it falls back to its earlier strength-based pick.
- **Why 13 schools started a season with only 56-59 players.** It is not the off-season roster cut. The yearly recruit class (5,900 players) is all signed, and the league is already at 98.6 % of its roster spots, so the schools that recruit worst stay short. The test save now gets a bigger class (6,700). It takes effect with the next signing class, so it has not been measured yet.
- **Team rating scale.** The team overall shown in the game starts the first season on a sensible shared scale: the worst FBS teams around the high 60s, the best FCS teams in the low 70s and the worst FCS teams around 50. After that, FCS ratings rise about 4-5 points a year (FBS about 2). Keeping FCS teams on that scale would make them win only about 2-6 % of their games against FBS teams, so this needs a decision before any change.
- Every change has its own switch and can be turned off.

**Still open.** The end of the 2028 season and the next off-season with the new build: check the topped-up FBS-vs-FCS count, the SWAC result in the FCS playoff, and rosters with the bigger recruit class. Also open: rating inflation from season to season. Real-life 2026 schedules are planned for later (design notes only).

## 2026-10-31 (evening) - Super Sim tackles now include assists, a freeze detector, and why the slowest frames got slower

This changes the PC port's game executable. Saves and game data are untouched. No game code, data or images are published.

**What changed.**
- **Super Sim tackles are fixed and switched on.** When you let the computer play your snaps with Super Sim, every tackle used to be recorded as a solo tackle, and tackles for loss and sacks were counted twice. That put your players at the top of the tackle leader lists. Now each Super Sim tackle has a 60 % chance of being recorded as an assisted tackle, the same split the game's own whole-game sim uses, and tackles for loss and sacks count once. A test run measured 50-60 % assists in Super Sim games and showed the stock behaviour (0 assists) with the fix turned off. To turn it off, set `SSTK=0` in the environment. `SSTK_AST` changes the assist share and `SSTK_DEDUP=0` keeps the old double count.
- **Freeze detector.** In a few percent of test starts (4 of about 120 since late October), the game stopped at the opening kickoff: no picture, no crash, and nothing in the logs said why. The port now notices when the game has shown no new frame for 10 seconds. It then writes down what every game thread is waiting for and what every job processor is running, so the next time it happens we can see the cause. It only reads; it never changes the game. `PS3_HANGDUMP=0` turns it off.
- **Why the slowest frames got a little slower.** After the last two speed-ups, the slowest 1 % of frames got about 6 ms longer. We checked whether that is real. It is real but small. Hitches did not become more frequent, and the time spent in long frames did not change in a measurable way. The game's own simulation steps became much more even (far fewer slow steps). The long frames are moments when the game's render thread waits for the background job processors to finish their work. A faster game puts more work on those processors per second, so those waits get a little longer. Making the job code faster shortens them too.
- **Tried, not kept: skipping the code check inside the translated code.** We moved most of the "is this still the right code?" checks into the translated job code itself. Side by side with the old check on 7.7 billion jumps, it never disagreed, and it made animation jobs 7 % faster. But game speed rose only slightly (0.86 -> 0.88 of real time, within the noise), and one of 15 full test games froze inside an animation job, a kind of stop not seen in recent builds. Fluidity and stability come first, so it stays off and is not in the build.
- **Checked for side effects.** 7 full test games with the tackle fix and the freeze detector (8 simulated plays each), plus 15 earlier test games that also had the detector: no corrupt results, no hangs, and the clock always advanced.

**Still slow, and what is next.**
- Contact plays still run at about 0.86 of real time in our pile-up test (target 0.9 or more).
- About 11 % of animation-job time still runs in the slower interpreter. It is spread over many small pieces of code that the game loads at different places, not one hot spot. The next step is a capture run that records exactly which code that is, so it can be translated too.

## 2026-10-31 (morning) - Contact plays run faster again: all translated job code uses the quick math, and the code checks got lighter

This changes the PC port's game executable. Saves and game data are untouched. No game code, data or images are published.

**What changed.**
- **The quicker math is now part of the normal build, for every background job.** Yesterday's speed-up (four numbers per instruction in the translated animation code, same results) only covered the 40 busiest pieces of job code, and it was stitched into the executable by hand because it had to keep a second, slow copy of each piece. Now the code translator writes every piece of job code (1,215 of them) in the fast form once, and the normal build produces it. The executable got smaller instead of bigger: 1.42 GB instead of 1.84 GB, well under the size Windows refuses to load.
- **Same results, checked again.** The fast forms were compared with the original ones on a million random cases per operation, in every floating-point mode the game can use, including the PS3's special values. In the mode the game uses there were no differences at all.
- **Game speed in pile-ups went up again.** In our pile-up test scene (the carrier run straight into the line every play), the game clock ran at 0.73 of real time with yesterday's build and 0.82 with all jobs in the fast form, measured in the same game sessions by switching between them (3 sessions, 33 periods of 40 seconds; the new code was ahead in every session). Frame rate stayed about the same (39-40 fps). The slowest frames got a little slower (99th percentile 65 -> 72 ms); that is being looked at.
- **Lighter code checks.** Before the translated code jumps from one place to another, the port checks that the code it jumps to is still the code it translated (the game swaps code in and out of the job's memory). That check was the biggest cost inside an animation job. It now does the same check with less work: it remembers which memory pages each piece of code uses instead of walking a list every time. In a test run the old and new checks were run side by side on 9.75 billion jumps and never disagreed. In the same pile-up test, each animation job took 11 % less time (2.89 -> 2.57 ms) and the game clock went from 0.81 to 0.86 of real time (3 sessions, ahead in every session).
- **Checked for side effects.** 10 full test games with all jobs in the fast form and 15 more with the lighter checks as well, 8 simulated plays each: no corrupt results, no hangs, the clock always advancing, and the screenshots looked normal. One of three quick test starts of the final build stopped at the opening kickoff; it is the exact same program as the tested one (byte for byte), and the same kind of stop has happened in older builds, so it is being tracked as an old, rare problem.
- **How to turn things off** if anything looks wrong: `SPU_VCOK2=0` in the environment brings back the old code check. The fast math has no switch any more (it gives the same results); a build with the original math can still be made for testing.

**Still slow, and what is next.**
- Contact plays now run at about 0.86 of real time in our test scene (target 0.9 or more).
- Inside an animation job, the translated game code itself is now only about 28 % of the time. The rest is the port's own work: the code check (still about 14 %), code that still runs in the slower interpreter (about 11 %), and checking newly loaded code (about 19 %). Next is moving the code check into the translated code itself, so most jumps skip it entirely.

## 2026-10-31 (morning) - Super Sim tackle stats: first look (no fix yet)

This was a reading-only investigation. No game files were changed and nothing was built or run.

**What happened.**
- **The bug.** If you play a Dynasty game and let the computer play your defensive snaps with Super Sim, your defenders get no assisted tackles. All of those tackles count as solo tackles, so your team ends up on top of the tackle leader lists.
- **What the stats mean.** In the game's stat tables one field holds solo tackles and another holds assisted tackles. The total shown on screen is the two added together.
- **How a normal simmed game does it.** When the computer sims a whole game (CPU vs CPU, or Advance Week), it picks one defender for each tackle and makes it an assisted tackle 6 times in 10 and a solo tackle 4 times in 10. Three test Dynasty seasons that were simmed this way all show about 41 % assisted tackles. No game in them is missing assists.
- **Why Super Sim is different (likely, not proven yet).** Super Sim inside a game you are playing uses a separate play engine. That engine seems to choose a single tackler for each tackle and record it as a solo tackle every time.

**Still open.** We still need to find the exact place where Super Sim records the tackle. After that, a test game with Super Sim on defence will measure the problem. The planned fix is an optional switch that uses the same 60/40 split as the normal sim, built only into a separate test version.

## 2026-10-31 (morning) - FBS+FCS universe: bowl and playoff picks fixed for 266 schools, the Dynasty reaches its third season

This was done in separate PC-port test builds. Nothing changed for players: the normal game executable, the play build and the saves are untouched. No game code, data or images are published.

**What happened.**
- **Why losing teams got bowl and playoff spots.** Bowls and the College Football Playoff are picked from the game's BCS-style ranking. Each week the game builds that ranking in a list sized for "the number of schools", and in the 266-school test build that number had been raised to 266. Only the 138 FBS schools go into the list, so 128 empty entries sat at the top and every FBS school's rank was pushed down by 128. Ranks are stored in a single byte (0-255), so the ten weakest FBS schools wrapped around to ranks 1-10 and were picked first. That is how the user's 3-9 team became a playoff "#4". The 150-school build had the same mistake, only smaller (every rank off by 12).
- **The fix.** The test build now sizes that list for the FBS schools only (138). The setting can be switched back. Two full postseasons were checked: the ranking runs exactly 1 to 138 and matches the top 25; all 58 bowl and playoff teams each year are FBS schools with at least 6 wins; the 12-team playoff has the five best-ranked conference champions plus seven at-large teams.
- **Into the third season.** The test Dynasty played the rest of 2027, the bowls and playoff, the end of season and the whole off-season, then started 2028. Every one of the 266 schools has a full staff of three coaches and the contract records are clean. The bigger recruit class (5,900 prospects) signed for the first time: about 26 freshmen per FBS school and 22 per FCS school. FBS rosters are 58-70 players and FCS rosters 56-70; 13 of 266 schools are still a little under 60 (a year earlier, with the old class size, 52 were). The FCS strength tiers stayed in order, and the 2028 schedule is clean.
- **A second year of FCS postseason results.** The FCS playoff, SWAC title game and Celebration Bowl were worked out again at the end of 2027 and matched the reference rules exactly. Montana won the FCS title 41-27 over Villanova.
- **FCS strength.** In 2027 FCS schools won 6 of 40 games against FBS schools (15 %). Over both seasons that is 13 of 152 (8.6 %), inside the 8-12 % target, so the stronger-tiers data was not needed yet.
- **SWAC title game as a real game: tried, needs code.** Pointing an unused conference title-game slot at the SWAC and splitting the SWAC into East and West divisions in the save was not enough; the game decides in code which conferences get a title game. A small code addition that schedules the SWAC title game in conference championship week is designed.

**Still open.**
- In 2027 the schedule had only 40 FBS-vs-FCS games (2026: 112; real seasons have about 110). The second-season schedule maker needs a look, and FCS strength should be measured again on a full schedule.
- 13 schools start 2028 with 56-59 players.
- The SWAC title game is still result-only, and there is no screen yet for FCS playoff results or FCS stat leaders.

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.11.

## 2026-10-31 (early morning) - FBS+FCS universe: the 266-team Dynasty plays into its second season, bigger recruit classes, and FCS playoff results

This was done in separate PC-port test builds. Nothing changed for players: the normal game executable, the play build and the saves are untouched. No game code, data or images are published.

**What happened.**
- **Why ten FBS schools lost their coaches.** At the end of the season the game goes through every coaching contract once, to age contracts, fire coaches and close finished contracts. It collects the contracts into a fixed list with room for 768. A 150-school league has fewer contracts than that; the 266-school league had 798. The last 30 on the list were the contracts of the 10 schools whose staffs went missing (Air Force through Auburn, plus Appalachian State), so their contracts were never closed and their jobs were never posted. The earlier guess (a counter that stops at 256) was wrong; the match was a coincidence.
- **The fix.** The test build gives that list, and two similar lists in the off-season step, room for 2,048 contracts (more than the contract ids can number). In the test the 266-team Dynasty played the rest of the 2026 season, the bowls and playoff, the end of season, the whole off-season and the first three weeks of 2027. Every one of the 266 schools has a full staff of three coaches, no old contract was left open, every schedule was clean, and the FBS and FCS stat leader lists stayed separate.
- **Bigger recruit classes.** The class size is not a fixed number in the game: it is the size of the recruit table minus 1,595, so the stock table gives 2,710 prospects. The test data makes the table bigger, which gives 5,900 prospects (about 25 per FBS school and 19 per FCS school), and grows the related tables for recruiting interest, visits, boards and players. The recruit rank is stored in 12 bits (at most 4,095), so the test build stops the rank at 4,095 instead of letting the weakest recruits wrap around to the top of the list. The 2027 class in the test had 5,900 prospects. The realistic names, looks and home states from the play build are part of the test data too.
- **A full season of FCS results.** Over the whole 2026 regular season FCS schools won 7 of 112 games against FBS schools (6.2 %) and scored 14 points against 38. The stronger FCS tiers won more often than the weaker ones. Points are where real FCS teams are; wins are a bit low (real: about 1 in 10), so a slightly stronger top two tiers are prepared for the next test.
- **FCS postseason results.** At the end of the season the test build now works out the FCS postseason from that season's games: the SWAC title game, the Celebration Bowl between the SWAC and MEAC champions, and the 24-team FCS playoff (10 conference champions plus 14 at-large teams, top 8 seeded with a bye, 23 games). The Ivy League champion is listed but stays home. The results are decided from team strength, not played out. The champions are stored in the save's conference-champion history, and the full bracket is written to a small file for a future screen. A check against the reference model gave the same conference champions and the same 24-team field. In the test season Villanova beat Central Arkansas in the final, and Bethune-Cookman won the SWAC title and the Celebration Bowl.

**Still open.**
- Bowl and playoff picks are wrong with 266 schools. The user's 3-9 team was put into a College Football Playoff quarterfinal, and several bowls had teams with losing records. The season's top 25 itself looks right, so the problem is in how bowl and playoff teams are picked. This is next.
- The bigger recruit class first shows up on rosters after the 2027 season. A second full season and the move into 2028 are still to run.
- The FCS playoff and title games are results only; playing them as real games and a screen to show them come later.

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.10.

## 2026-10-30 (night) - More realistic recruits and bigger season tables, now in the PC play build

Both changes were tested on copies of saves first and are now switched on in the PC-port play build. No game code, data or images are published; the changes are data edits made on the owner's copy of the game.

**What changed for players.**
- **Recruit names, looks and home states are more realistic.** New recruit classes draw first names from what US boys born 2005-2008 were actually named, and last names from US Census surname data, so a class has about 800 different first names and 1,750 last names instead of about 500 and 800, and fewer 1990s-style "Mike, Chris, Matt" classes. The mix of player appearances by position follows a real current roster, and home states now follow where FBS signees really come from: Texas about 14 percent, Florida 11, Georgia 9, and California down from 11 to about 6 percent.
- **Bigger season tables for new Dynasties.** The tables for the team-by-week schedule and for per-game offensive line, offensive and defensive stats are larger, so late-alphabet teams keep their bowl and playoff lines and the last postseason box scores are no longer cut off.

**How it was checked.**
- Both of the user's existing Dynasties loaded with the new data, advanced to week 2, saved and reloaded. Not one existing player changed name or appearance, and their stats were written normally.
- In both existing Dynasties and in a new one, the new recruit class used the new name lists (about 1,100 first names and 1,500 last names that only exist in the new lists, none that only exist in the old ones), with the planned appearance and home-state mix.
- A finding along the way: a loaded Dynasty and a new Dynasty read the recruit lists from two different game archives, so both are updated.

**Good to know.**
- The bigger tables only apply to Dynasties started from now on. Existing Dynasties keep working with their old table sizes.
- Recruits that already exist keep their names and looks; only new classes change.
- Name, appearance and home state are still picked independently of each other. Linking them is the next step.
- Everything can be switched off again by removing two files; the original game data was not overwritten.

## 2026-10-30 (night) - FBS+FCS universe: the 266-team season now gets through the end of the season, and FCS stat leaders are kept separately

This was done in separate PC-port test builds. Nothing changed for players: the normal game executable and saves are untouched. No game code, data or images are published.

**What happened.**
- **Why the 266-team end of season hung.** Every coaching contract has an id number, and the game stores it in 10 bits, so there can never be more than 1,023 contracts. The game keeps about 5 contract rows per school (current contracts, finished ones and open offers). With 150 schools that is about 780 rows; with 266 schools it is about 1,390. At the end of the season the game posts new coaching openings, and the routine that looks for a free id number searched forever. It had nothing to do with the FCS changes; the game's own openings for FBS schools were already too many.
- **The fix.** The test data now stores the contract id in 11 bits (up to 2,046 contracts). The contract table had unused room in each row; the coach table's rows grow by 4 bytes. The test build lets the id routine use the bigger range and never hands out the number that means "no contract". A small tool converts existing test saves. In three test runs the 266-team Dynasty then played the bowls and the playoff, finished the end of season, and ran the whole off-season into 2027. Every FCS school has three coaches, and the postseason stayed FBS-only (41 games).
- **More room for coaches.** After the first off-season about 700 coaches are out of work at once, more than the coach table could hold, so its size went from 974 to 2,000.
- **Separate FCS stat leaders.** The game builds its national stat leader lists once a season. The test build now builds them twice: the normal lists without FCS players, then a second set with only FCS players, stored under their own category numbers so today's screens never mix them in. A test save had 250 FBS and 250 FCS leader rows (25 per category). There is no screen for the FCS lists yet; the data is ready for one.
- **FCS strength retuned.** The 266-school test data was rebuilt twice. In the first version (one full season) FCS schools beat FBS schools 20 % of the time and FBS teams scored only 31 points against them: the FCS defenses were too good. The second version makes FCS defenders a bit weaker and lowers every strength tier slightly. Through week 6, which covers most FBS-vs-FCS games, FCS schools won 7 of 92 (7.6 %) and scored 14.9 points against 37.3. The best FCS tier won about 1 in 6, the weakest about 1 in 20 or less. Real FCS teams win about 1 in 10 and score about 13-20 points, so this is close; a full season is still to run.
- **FCS title games and playoff: designed.** Only the SWAC plays a conference title game among FCS conferences; the SWAC and MEAC champions meet in the Celebration Bowl; the Ivy League stays home; the playoff has 24 teams (10 automatic bids, 14 at-large, top 8 seeded with a bye, 23 games). A reference model picks the field from a season's standings and plays out the bracket. The first in-game step will be to write these results at the end of the season.

**Still open.**
- After the first 266-team off-season, the 10 FBS schools that come first in the team order are left without coordinators (two without any coach), because their old contracts are never closed when those coaches move. A school without a coach makes the next week's simulation give up, so 2027 does not get past week 1 yet. 266 minus 256 is exactly 10, so this looks like one more counter that only goes to 256. Two repair attempts in this session did not hire coaches outside the carousel stage.
- The yearly recruit class is a fixed 2,710 prospects, so with 266 schools each school signs fewer players and some rosters shrink into the low 50s. The class size has to grow with the number of schools.

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.9.

## 2026-10-30 (evening) - Contact plays run faster: quicker math in the translated animation code

This changes the PC port's game executable. Saves and game data are untouched. No game code, data or images are published.

**What changed.**
- **Players' animation work is now about 28 % cheaper per job.** During a play the game waits each tick for a batch of about 20-28 animation jobs. We measured inside one of those jobs: almost half of its time was the translated game code itself, and that code did every floating-point step one number at a time, with several checks per number. It now handles four numbers per instruction, with exactly the same results (checked on a million random test cases per operation, including the special values the PS3 handles differently from a PC). Reads and writes of the job's working memory also lost four debug checks each, and one math step no longer calls a slow library routine.
- **Game speed in pile-ups went up.** In our pile-up test scene (the carrier run straight into the line every play), the game clock ran at 0.65 of real time before and 0.77 after, measured in the same game sessions by switching the new code on and off (3 sessions, 36 periods of 40 seconds; the new code was ahead in every session). Frame rate stayed the same (about 39 fps), and the slowest frames got slightly better (99th percentile 72 -> 69 ms).
- **Checked for side effects.** 10 full test games with the new code, 8 simulated plays each: no corrupt results, no hangs, the clock always advancing, and the screenshots looked normal (tackles, pile-ups, players, scoreboard, crowd).
- **How to turn it off** if anything looks wrong: start the game with `SPU_FASTOPS_DEFAULT=0` set in the environment.

**Still slow, and what is next.**
- Contact plays are still below full speed (target 0.9 or more). The biggest remaining cost inside an animation job is now the port's own bookkeeping that checks which translated code may run (about 44 % of the job). That is next, done carefully, because an earlier attempt there caused a freeze.
- Extending the faster math to more of the game's background jobs did not fit yet: the executable would grow past the size Windows can load. The next build will compile those parts once in the faster form instead of keeping both versions.

## 2026-10-30 (evening) - FBS+FCS universe: three seasons with full FCS rosters, and a 266-team season reaches the bowls

This was done in separate PC-port test builds. Nothing changed for players: the normal game executable and saves are untouched. No game code, data or images are published.

**What happened.**
- **Why the second season would not advance past week 1.** A log of every database query during the failed advance showed the game simulating 22 games and then giving up on the one game that involved an FCS school with no coaches (and no players) left. When any game in a week has a team without a coach, the game quietly abandons the whole week, saves, and goes back to the same week. Making sure every school has a coaching staff fixed it.
- **FCS coaching staffs are refilled now.** The game's coaching carousel works in two steps. At the end of the season it posts an opening for every empty coaching job, and in the carousel stage it hires coaches into those openings. The posting step only looked at FBS schools, so FCS jobs emptied by the carousel were never filled again. The test build now posts FCS openings too. In the test, all 12 FCS schools had a full staff (head coach and both coordinators) after the carousel, where before they had 0 or 1 coaches. A second safety net fills any empty coaching job right before the off-season roster cuts.
- **FCS rosters refill themselves.** The note from the last update was wrong: FCS schools already recruit, about 20 signees a year each, mostly lower-rated players than the FBS classes. Before the roster-cut fix those signees were cut along with everyone else. Now every FCS school starts each new season with 60-70 players, and FCS players improve in the off-season like FBS players do (about +4 overall per year).
- **Three seasons in a row with 150 teams.** A test Dynasty played the 2026 season, the off-season, all of 2027 including the bowls and playoff, a second off-season, and the first five weeks of 2028. Every FCS school had 60-70 players and three coaches in both new seasons, every FCS school got 11-12 games with nobody playing twice in a week, and FCS players kept their stats. No crash and no autosave stall.
- **The 266-team build gets through the regular season.** Its first advance had hung because the step that rates recruits uses a fixed pool of 4,410 small records, sized for about 150 teams. The pool is three times larger in the test build. A 266-team Dynasty then played every regular-season week up to conference championship week, about 1.4 minutes per week.
- **FBS-only national stat leaders.** The filter that keeps FCS players out of the national stat leader lists had a wrong address in it and never removed anyone. It is fixed in the newest test build and now removes FCS players; checking the finished lists in a save is still to do.

**Still open.**
- With 266 teams, the advance from conference championship week to the end of the season plays the bowls and then stops at the coaching-carousel step. It also stops there with the new FCS change turned off, so the cause is in the game's own carousel step at that team count, most likely another fixed-size list. That is next.
- FCS strength needs tuning. With the 150-team test data FCS schools win about a third of their games against FBS schools (real FCS teams win about 1 in 10); with the 266-team data they almost never win and average 8 points.
- FCS conference title games and separate FCS stat leader lists are not started.

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.8.

## 2026-10-30 (midday) - FBS+FCS universe: why FCS rosters vanished after a season, and the 266-team build starts

This was done in separate PC-port test builds. Nothing changed for players: the normal game executable and saves are untouched. No game code, data or images are published.

**What happened.**
- **Found why FCS players disappeared at the season rollover.** In the off-season the game puts every player on a cut list. Then, team by team, it takes off the players each school keeps, and releases whoever is left. That keep step only went through FBS teams, so every FCS player was released. The test build now runs the keep step for FCS schools too. In the test, 10 of 12 FCS schools started 2027 with 60-70 players and working depth charts. FBS teams were not affected.
- **Still open from the rollover:**
  - The two FCS schools that lost all their coaches in the carousel still lost all their players.
  - The game's pass that fills empty coaching jobs skips FCS schools. A fix is in the test build, but that pass only runs when a Dynasty is created, so the off-season job filler still has to be found.
  - FCS schools do not recruit yet, so their rosters will shrink each year until walk-ons or unsigned recruits fill them.
  - The second test season does not advance past week 1 (no crash; it saves and returns to week 1).
- **The 266-team build exists.** It was built only from the validated build 87 parts. It creates a new Dynasty with all 128 FCS schools, and every school gets a clean schedule (FCS 11-12 games, FBS 12, nobody playing twice in a week). The first advance hangs in the step that rates recruits for every team, because one of the game's fixed memory pools runs out. That pool is next.
- **Checked:** the database memory setting works. A nearly full table (CAPX) turned out to be the fixed list of coach goals and does not need to grow. No autosave stall in about 20 test saves.

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.7.

## 2026-10-30 (late morning) - FBS+FCS universe: the autosave stall pinned down, a first season rollover, the full FCS list

This was done in separate PC-port test builds. Nothing changed for players: the normal game executable and saves are untouched. No game code, data or images are published.

**What happened.**
- **The end-of-season "autosave in progress" stall.** It is narrowed to one step. The game sets aside the memory for the save but never starts writing it. There is no error and no crash. Eleven more test saves from the same starting point all worked, so it is rare and the cause is still open. A watcher now records where every game thread is waiting if a save hangs, so the next one will show the cause. It has only been seen in the FCS test builds so far. If it ever shows up in normal play, quit and load the last autosave; that save is intact.
- **Database memory is now a setting** in the test build (default +16 MB, the size the full 266-team universe needs). It is built but not yet run.
- **First season rollover with FCS teams.** A test Dynasty went through the whole off-season into 2027 and played five weeks, and the schedule clean-up worked for the new season too. The problem it found: the rollover deletes every FCS player, and the coaching carousel hires most FCS coaches away. Fixing that is now first on the list.
- **All 128 FCS programs.** A list of the real 2026 FCS schools and conferences (compiled from public sources) and a test data pack with generated FCS-level rosters, real conferences and tables sized for 266 teams.
- **The 288-team reserve.** The code changes for 266 active teams are prepared and checked offline. Two more spots that count teams in a single byte were found and fixed. The test executable is not built yet: the PC ran out of disk space during the compile.
- **Staged, not built:** FCS players are left out of the national stat-leader lists, and a last fallback for crowded schedule weeks.

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.6.

## 2026-10-30 (morning, later) - FBS+FCS universe: bigger stat tables work, cleaner FCS schedules, a full season

This was done in a separate PC-port test build. Nothing changed for players: the normal game executable and saves are untouched. No game code, data or images are published.

**What works now.**
- **The bigger stat tables no longer crash the season.** The cause was found and confirmed. Each week the game sorts some database tables while it fills the recruiting boards, and the sort needs a few megabytes of working memory. That memory comes from the game's fixed-size database heap (about 12 MB), which the larger tables had filled. The game then stopped with its own "out of memory" marker. Every earlier crash log has that marker; no clean run has it. The heap sizes come from a small settings list the game reads at startup, and the test build makes the database heap 4 MB larger. With that, all 22 enlarged tables ran a whole season with no out-of-memory event.
- **One clean-up pass for schedules.** The season generator still builds the schedule. Right after it finishes, one new pass reads the finished schedule, then:
  - gives an FCS school playing twice in one week a different week or hands that FBS opponent another free FCS school;
  - trims FCS schools with more than 12 games;
  - adds FCS conference games;
  - fills FCS schools with fewer than 11 games.

  FBS-vs-FBS games are never touched and no week goes over 126 games. In four new test Dynasties, every FCS school had 11-12 games and every FBS school kept 12. Three had no double-booked weeks at all; one had two left in the first week, where the 12 test schools are too few to go around.
- **FCS conference games are scheduled.** The clean-up pass makes them, because the game's own conference scheduler skips FCS conferences and its style tables are full.
- **A full season with FCS stats.** One test Dynasty played the regular season, conference championships, the bowls and the 12-team playoff with all tables enlarged. FCS schools averaged 18 points against FBS teams and won 26 of 74 of those games. All 41 bowl and playoff games were between FBS teams. No FCS school or player was ranked, invited to a bowl, named a Heisman finalist or named an All-American.

**Not working yet.**
- **An end-of-season stall.** Once, advancing to the end of the season stopped on an "autosave in progress" panel and never saved. Reloading the earlier save and advancing one step at a time worked. It looks like an earlier unexplained stall and is next on the list.
- **Stat leaders.** Three FCS players show up in the national stat-leader lists next to FBS players. FCS should get its own lists.
- **Still to do:** the database memory size has to become a proper setting (the full 266-team universe needs about 16 MB more). The injury table needs to be larger. The 288-team storage reserve was not started.

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.5.

## 2026-10-30 (mid-morning) - Where contact plays lose game speed

PC port. No game code, data or images are published. Nothing changed for players: the game build stays the same as the previous entries.

**Question.** In heavy contact (pile-ups) the game clock runs at about 0.5 to 0.8 of real time. Each simulation tick spends about half its time waiting for about 26 animation jobs on the five helper processors. Is the port slow to hand those jobs out, or is it the game's own job order?

**How it was measured.** A test build recorded, inside the game, when every helper job started and ended, on which helper processor and on which PC core.

**What it showed.**
- **The port hands out jobs quickly.** When an animation job started, 84% of the time no other helper processor was sitting idle. When work was queued, the gap between one job ending and the next starting was about 30 microseconds.
- **The waiting comes from the game's job order and from how long each job takes.** Each tick has one big batch of about 20 animation jobs. Most of the idle helper time is either the end of that batch (nothing left to run) or jobs waiting for an earlier job to finish.
- **The PC's slower cores are not the problem.** About 45% of animation jobs started on the CPU's efficiency cores, and they ran as fast as on the performance cores.
- **The simulation thread itself** spends about three quarters of its own time in the game's translated code and a quarter in the port's helpers. It never waits on locks. Its only waste is that a short 50-microsecond sleep in its job wait really lasts about half a millisecond.
- Some earlier helper "busy" numbers were overstated, because the old outside measurement missed the end of most animation jobs.

**Two fixes tried, neither kept.**
1. Idle helper processors pause politely instead of spinning at full speed.
2. The simulation wakes the moment its job finishes, instead of on the next timer tick.

Over three pile-up test sessions, neither raised game speed. Both came out slightly lower, by 0.04 and 0.05 of real time, which is within the noise (plus or minus about 0.03). The second fix made the worst frame times about 15 ms better, but that is not enough to make it the default while game speed may be lower. The test build was removed again.

**Next.** The remaining levers are the cost of each animation job itself, a sixth helper processor (a change to the game's own setup), and the very frequent locking of the shared job list by the render and simulation threads.

## 2026-10-30 (morning) - Faster code checks tried for contact plays, withdrawn

PC port. No game code, data or images are published. Nothing changed for players: the game build stays the same as the previous entry.

**What was tried.** When the game's SPU helper programs run as translated native code, the port keeps checking that the code in memory still matches the translation before it jumps into it. Profiles of pile-up plays showed this checking was about 15% of the helper processors' time. The cache that remembers "this code was already checked" was being thrown away on every memory transfer, even when the transfer only moved data. The test build kept the cache until a transfer actually wrote over code it depended on. It also skipped a slow lookup that ran on every transfer.

**Result.** The checks themselves got much cheaper: about 9 in 10 became a single table lookup, and a built-in self-check found no wrong answers in about a billion checks. Game speed did not improve. Over two clean pile-up test sessions, game speed with the change was within 0.01 to 0.04 of real time of the speed without it. That is well inside the noise, and frame rate was about the same.

**Why it was withdrawn.** In 2 of 7 test games with this build, one helper processor stopped with an error type never seen before, and the game froze. One of the two freezes happened while the new checks were switched off. That points at another part of the test build, a larger lookup cache that was always on, or at a timing change. The previous build had about 15 clean test games in a row, so the change was taken out and the previous build was put back. Game speed in heavy contact is still about 0.5 to 0.8 of real time.

**Next.** The remaining options are smaller or riskier. Translating more of the animation helper code is worth at most about 1% of helper time. Trimming the main simulation thread's overhead is worth about 1-2% of its time. A sixth helper processor is a bigger change to the game's own setup and is only proposed for now.

## 2026-10-30 (morning) - FBS+FCS universe: FCS teams play with their real rosters

This was done in a separate PC-port test build. Nothing changed for players: the normal game executable and saves are untouched. No game code, data or images are published.

**What works now.**
- **FCS schools field their own players.** The game had three places where it treated any FCS-type team as a nameless placeholder: it swapped in a stand-in roster when setting up a game, threw away that side's game stats afterwards, and skipped one end-of-game step for non-FBS teams. Twelve changed instructions make FCS teams go through the same path as FBS teams.
  - Scores look like real football now: in a new test Dynasty, FCS teams averaged about 16 points against FBS teams through week 7 (before: almost always 0), won 7 of 58 such games, and were shut out 3 times. The test FCS schools are copies of FBS rosters, so they are stronger than real FCS schools will be.
  - FCS players get box scores, season and career stats, and show up in the national stat leaders. FCS teams get season team stats.
  - Seven simulated weeks ran without a fault.
- **More room in two tables.** The team-schedule table (full by conference championship week in the last test) and the conference stat-leader table now have about 50% more room in the test data, and a new Dynasty keeps the larger sizes.
- **Better FCS schedules.** FCS schools now get 11-14 games instead of 7-9. The season generator turned out to drop preset games between two FCS teams of the same conference, so the test schedule now pairs FCS teams across conferences.

**Not working yet.**
- **Bigger box-score tables.** Enlarging the per-game stat tables makes the weekly ranking step crash within a few weeks. The likely cause is a fixed memory area for the Dynasty database, which has to be found and enlarged first.
- **Double-booked weeks.** A few FCS schools still have two games in one week (about 6 per Dynasty, down from 12), and some have 13-14 games. A test-build step catches part of it; the real fix is one clean-up pass after the season generator finishes.
- **FCS conference games** are not scheduled yet (see above).

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.4.

## 2026-10-30 (early morning) - Tackles and pile-ups use less CPU

PC port. No game code, data or images are published.

**What changed.** Three of the game's physics helper programs now run as translated native code by default: the contact finder (which players touch), the capsule-overlap test and the current-pose lookup. Before, they ran in the slower SPU interpreter. They matter most when several players are in contact, such as a pile-up at the line.

**Effect.** Each of the three now needs a half to a quarter of the processor time it needed before. All of that time sat inside the simulation's waits, so in principle less of it helps the game clock keep up during contact plays. Three pile-up test sessions did not show a measurable rise in game speed: averaged over all three, game speed was the same with and without the change (within about 0.03 of real time), and about 0.04 higher once the amount of contact in each stretch is allowed for, which is still within the noise. Game speed swings a lot from play to play (0.47 to 0.86 of real time here), so a small gain cannot be ruled in or out yet. Frame rate was unchanged. Game speed still falls to about 0.5 to 0.8 of real time in heavy contact, and the next steps go after that.

**How it was checked.** Ten automated test games with these programs translated: no corruption, no hangs, the game clock advanced in every one, and the screenshots (tackles, pile-ups, HUD) looked normal. To go back to the interpreter, set `SPU_CFBR_EXTRA=0`.

## 2026-10-30 (pre-dawn) - FBS+FCS universe: FCS depth charts fixed, first full season

This was done in a separate PC-port test build. Nothing changed for players: the normal game executable and saves are untouched. No game code, data or images are published.

**What works now.**
- **FCS teams keep their depth charts.** The step that dropped them was found. When a Dynasty is created, the game wipes every team's depth chart and then copies each team's data back from the roster. For FCS-type teams it skipped the depth chart. One changed instruction fixes this: all 12 test FCS schools now start the Dynasty with a full depth chart and a real team rating.
- **A full season with FBS and FCS together.** A 150-team Dynasty played the regular season, conference championships, bowls and the 12-team playoff without a crash or a stall.
- **The postseason stays FBS-only.** All 41 bowl and playoff games were between FBS teams, the same count as an FBS-only Dynasty. No FCS school was ranked or picked for a bowl.
- **The earlier autosave stall did not come back.**

**Not working yet.**
- **FCS players in games.** FCS teams are on the schedule and FCS-vs-FCS games have winners, but against FBS teams they still lose by huge margins and their players record no stats. The game appears to swap in a stand-in roster for any FCS-type team, as it does for the built-in placeholder FCS teams. A test with different team ids showed the swap depends on the team type. Finding that check is the next item.
- **Schedules.** FCS schools still get 7-9 games instead of 11-12, and a few play twice in one week. FBS schools keep 12 games.
- **Room for more teams.** Two tables hit their limits in this test season and need larger capacities. Two team ids (300 and 400) are reserved by the game and must be skipped.

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.3.

## 2026-10-30 (early morning) - FBS+FCS universe: Phase 1, first runtime pass

This was done in a separate PC-port test build. Nothing changed for players: the normal game executable and saves are untouched. No game code, data or images are published.

**What works.**
- **Room for the full-universe save.** The temporary memory block that the game sets aside for each save and load is now 32 MB instead of 16 MB. That lets Dynasty saves grow to 25 MB, which is the plan's full-universe size with margin.
  - A new Dynasty saved at 25 MB.
  - It reloaded cold twice: once at creation and once at week 7. Weekly autosaves through week 12 stayed 25 MB.
  - Every weekly autosave stayed that size.
- **FCS schools in the same Dynasty.** 12 rostered FCS test schools joined the engine's active team list beside the 138 FBS teams, for 150 in all. Four of them have team ids above 255.
  - The 5 built-in generic FCS rows are retired, so the list holds exactly FBS plus the real FCS teams.
- **FCS teams keep their coaches.** A Dynasty-creation step was found that detaches the coaches of FCS-type teams; one word now exempts them. All 12 schools kept their head coach and coordinators through creation and the season weeks that were simulated.
- **FBS-only rankings stayed FBS-only.** Through week 12:
  - FBS poll ranks were exactly 1-138;
  - every FCS school stayed unranked;
  - no bowl row held an FCS team.
- **Team-count limits must change together.** The engine has 72 team-count limits, set to 138 today. Raising only some of them corrupted memory right after Dynasty creation. Raising all of them together (to 150 for this test) ran cleanly, at about 35-70 s per simulated week.

**Not working yet.**
- **Depth charts.** Dynasty creation builds depth charts for the 138 FBS teams only, through a step that has not been found yet. Without depth charts the FCS schools take the field with nobody, lose every game by shutout and record no player stats. This is the next item.
- **Schedules.** The season generator kept only some of the FCS-vs-FCS games from the preset schedule. Each FCS school got 7-9 games instead of 11, and a few played twice in one week. The planned FCS schedule step will fill this in.
- **One stall.** One run stuck on an "Autosave in progress" news panel after week 7. After a reload the same weeks advanced normally.
- **Not reached yet.** Bowls and the playoff, and the larger team-storage reserve (288 teams).

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), section 3.2.

## 2026-10-29 (late night) - FBS+FCS universe: Phase 0 tested

PC port, test build only. Nothing changed for players: the normal game executable and saves are untouched. No game code, data or images are published.

**What was tested.** The first runtime step of the plan to put rostered FCS schools into the same Dynasty as the 138 FBS teams.
- **Bigger save file.** Dynasty saves double to 16.7 MB. A new Dynasty saved at that size, reloaded, played a week, saved and reloaded again.
- **Where the save buffer lives.** It is a temporary 16 MB block that the game reserves for each save and load. At the new size only about 105 KB of that block is left, so the save cannot grow further without moving the buffer.
- **One test FCS team with a full roster.** It joined the engine's active team list and came through Dynasty creation, a simulated week and a reload. Dynasty creation removes its coaches and depth chart, as it does for the built-in generic FCS teams, and the generic teams join the list as well. Both are next on the list.

Details: [FBS+FCS universe plan](docs/modding/fbs-fcs-universe-plan.md), Phase 0 runtime result.

## 2026-10-29 (night) - Full keyboard rebinding

PC port. No game code, data or images are published.

**What changed.** Every pad control can now be bound to any key: all 16 buttons plus the eight stick directions (left and right stick). Add a `[keys]` section to settings.ini with one `control = KEY` line per control, or `KEY+KEY2` for two keys. Mouse buttons (`MOUSE1` to `MOUSE5`) work too, and so do more key names (Insert, Home, Page Up, the numpad operators, punctuation spelled out as words and so on). Esc still quits the game and cannot be bound. Anything missing or misspelled falls back to the chosen layout (classic or WASD) and the log says which line was ignored. With no `[keys]` section the keyboard behaves exactly as before.

**For the in-game page.** A small command area in the page's settings block lets the menu set, clear or reset one binding, or ask the game to take the next key you press ("press a key"). The key you press is held back from the game while it is captured, the change is written as a single line of the `[keys]` section (other lines and comments stay), and it applies at once. The interface is documented in the project notes. The menu rows themselves are the UI work still to come.

**How it was checked.** In two test games with simulated key presses: all 24 default controls matched the old layout, bad lines were ignored, and set, press-a-key, mouse button, clear, reset, switching layout and reset-all each changed the input as expected and rewrote only the right line. A restart then picked the saved bindings back up (73 checks, 0 failures). Saves were unchanged.

## 2026-10-29 (late night) - Table capacity patch tested on a copy

PC port. No game code, data or images are published. Status: tested on an isolated copy; not installed in Play_PC (it needs a new Dynasty, which is the user's decision).

**What was tested.** The four per-season tables that overflow with 138 teams (team-week schedule, and three per-game stat tables) were given more room in the Dynasty template. A new Dynasty started from the patched template inherited the new sizes, the save stayed the same file size, reloaded cleanly and ran a full regular season. By the bowl stage the team-week schedule held rows for all 138 teams (the unpatched game keeps 60) and no played postseason game was missing stat rows.

**Not proven yet.** The national championship game's stat rows, and a second season: the game resets those tables in the same step that plays the last playoff week, so a save of that moment needs a team that is in the playoff. A few playoff-round team-week rows are still missing for a reason that is not table size.

## 2026-10-29 (night) - Bracket and Key Bindings pages installed in Play_PC

PC port. No game code, data or images are published. Status: installed; checked in game on copies of saves.

**Playoff bracket, final fixes.** A test on a played semifinal week showed the bracket's score lookup is unreliable after the quarterfinals: the Alabama-Notre Dame semifinal said "Notre Dame 38-35" (a quarterfinal score) and the national championship said "Ohio State 24-21 CHAMPS" although Alabama won 34-17. The page now shows scores only for the first two rounds, where they were right. A played semifinal shows "<winner> WON", and the final shows "<winner> - Champion". A game not yet played still says "Scheduled" (no older score leaks in). The thin white divider left of the championship column is now covered. Final-week and end-of-season brackets were checked on saves made in game.

**Installed.** The updated pages are now what Play_PC serves, together with the game build that has the Key Bindings tab (the fourth tab of System Settings, 24 controls plus "Reset All Keys"). Checked: that tab renders; a playoff semifinal, the national championship and a regular-season game all load and reach a play with the pages on.

**Not done yet.** Real scores for semifinal and final rows (needs a different score source than the weekly recap lookup). A warning on the Key Bindings page when a key is already used elsewhere.

## 2026-10-29 (evening) - Playoff bracket polish and a Key Bindings page

PC port. No game code, data or images are published. Status: built and tested in game on copies of saves; the updated pages are not installed in Play_PC yet (one last check on a semifinal-week save is pending).

**Playoff bracket.** The Dynasty > Dynasty Setup > CFP Bracket page now looks like a bracket: every game sits in an outlined box and lines join each pair of games to the game their winner plays in the next round. Played games show the final score ("Alabama 31-15"), and a game that has not been played yet says "Scheduled" (before, a quarterfinal the computer had already simulated could still say "Scheduled"). The stray cursor frame and the extra scroll bar from the underlying list are hidden. The scores come from the same Dynasty data the weekly recap uses; the page only trusts a score once the winner has moved into the next round, so a game in the current week is never filled in with an older game's score.

**Key Bindings page.** Settings > System Settings gets a fourth tab, "Key Bindings". It lists every PS3 control (the 16 buttons plus the eight stick directions) with the keyboard key it is on now. Slide a row to "Press a key...", leave the page, press the new key or mouse button, and that is the new binding; it is saved in the `[keys]` section of `settings.ini` and applied at once. "Reset All Keys" at the bottom clears every custom key. Esc is never bindable (it quits the game). A key already used elsewhere is still accepted; the page does not warn about it yet.

**How it works.** The new tab reuses the settings page of the PC Controls & Display tab: a small piece of game code answers the list and the choice, and passes the request to the PC runtime through a few bytes of shared memory. The runtime does the key capture, the bookkeeping and the file write.

**Checked in game** (copies of saves, never the real ones): the bracket page in the quarterfinal and semifinal weeks; both settings tabs; rebinding Cross to X with a simulated key press and seeing the page show X and the file gain `cross = X`; a playoff quarterfinal and a regular-season game both loading and reaching a play with the new pages on.

**Not done yet.** The semifinal-week and final-week screenshots of the bracket with the last fix (a first test showed an unplayed semifinal wrongly carrying an earlier game's score, which is what the "only trust a score once the winner has moved on" rule fixes). A thin white divider left of the championship column belongs to the underlying list; a cover for it is in the build but not yet seen.

## 2026-10-29 (evening) - Smoother gameplay: less repeated vertex work in the renderer

PC port. No game code, data or images are published.

**What changed.** About 8 % more frames per second during play (about +3 fps on top of the earlier gains, measured twice in same-session comparisons). Two pieces of repeated work are gone from the renderer:
- It used to re-check the vertex program (the small program that places each corner of a shape on screen) before every single draw, even when the game had not changed it. It now remembers the last one and only re-checks after the game actually loads a new one.
- Flat rectangles (the scoreboard and other HUD pieces, crowd cards, billboards) used to be sent to the graphics card as two triangles with 6 full corners each. They now go as their 4 real corners plus a short list saying which corners make each triangle, so a third less corner data is converted and copied.

The picture is meant to be exactly the same. Both are on by default in the game and in Play_PC.

**How it was checked.** Ten full test games with both on, plus one with both off for comparison: no corrupted frames, no hangs, the game clock advanced normally in every one, and the contact sheets (scoreboard, crowd, field, players, play log) matched the one with them off. One more test game on the final build with no settings at all confirmed they are on and clean. `RSX_VS_MEMO=0` and `RSX_ARRAY_IXD=0` turn them off if anything looks wrong.

**Also looked at, no change.** Small one-triangle-pair draws are frequent (about a quarter of the unindexed draw calls) but carry only 6 corners each, so sending them the same way would save almost nothing; left as they are.

## 2026-10-29 (afternoon) - Smoother gameplay: the renderer stops repeating identical work

PC port. No game code, data or images are published.

**What changed.** About 8 % more frames per second on an idle PC, and fewer long frames. When several things drawn in one frame reuse the same pixel-shader program, the renderer used to re-copy and re-check that program for every one of them. It now notices the program is identical to one it already handled in that frame and reuses the earlier result. The picture is meant to be exactly the same; only the repeated copying is gone. This is now on by default in the game and in Play_PC.

**How it was checked.** Ten full test games with it on, plus one with it off for comparison: no corrupted frames, no hangs, the game clock advanced normally in every one, and the contact sheets (players, uniforms, scoreboard, field) matched the one with it off. `RSX_FPSNAP_DEDUP=0` turns it off if anything looks wrong.

**Also looked at, no change.** The game waits in many short 1 ms sleeps while polling; Windows rounds each to about 1.5 ms. Switching those waits to a spin-then-sleep hybrid made no measurable difference in a same-session comparison, so the default stays.

## 2026-10-29 (afternoon) - Game-load hang fixed; PC pages are back on by default

PC port. No game code, data or images are published.

**Cause found.** The game's in-game interface checks one small EA menu script (the one our PC pages edit) and needs its list of constant strings to be exactly the size EA shipped, 12 entries. Our rebuilt copy had a different list (11 entries at first, then dozens once the pages' text was added). Any other size left the in-game interface stuck and every game load sat on the LOADING screen. The script's code, its size, its position in the file and the function style it uses do not matter. We checked each: a copy with EA's exact 12 entries and an empty body loads; the same copy with one to a few dozen extra entries hangs; the same copy padded with 200 do-nothing instructions loads.

**Fix.** The build now keeps EA's exact 12-entry list and writes every string of our own directly into the code instead of adding it to the list. The playoff quarterfinal and a regular-season game both load and play with the PC pages on.

**Play_PC.** `ui_pages = on` (the default) serves the PC Controls & Display tile and the CFP Bracket page again. `ui_pages = force` still works and means the same as `on`. The temporary "start with the stock menus" workaround is removed.

**Checked in game** (isolated copies of two saves): quarterfinal Play Game, Team Stats card, kickoff and a first play; week-10 regular-season game, kickoff and a first play; PC Controls & Display tile and its settings page; CFP Bracket page; and a game start through the real `play_pc.ps1` launcher with the setting left on.

## 2026-10-29 (late morning) - Game loads hang with the in-game PC pages; pages paused

PC port. No game code, data or images are published.

**What happened.** Choosing Play Game for the playoff quarterfinal sat on the LOADING screen forever. It is not a playoff problem: every game started from Play_PC with the in-game PC pages switched on hung the same way, regular-season games included. The pages arrived this morning and had only been tested in the menus, never through a game load.

**Cause.** The game's in-game interface has to start up and report back before a game can begin. Our edited copy of one small EA menu script (the one that adds the PC Controls & Display tile and the CFP Bracket page) stops the in-game interface from reporting back. With the original script, the same quarterfinal and a regular-season game load and play normally. Step-by-step tests showed the trigger is how our rebuilt script is laid out, not anything it does. It still hangs even when its added code is removed entirely.

**For now.** Play_PC starts with the stock menus, even when `settings.ini` says `ui_pages = on`, so games load again. The PC Controls & Display tile and the CFP Bracket page are hidden until a corrected script is ready. `ui_pages = force` brings them back (for testing only: games will not load).

**Next.** Rebuild the script so its layout matches EA's original, then check that the quarterfinal, a regular-season game and both pages all work, and switch the pages back on.

## 2026-10-29 (late morning) - The playoff page is now a bracket

Side track (EA's own menus, PC port). No game code, data or images are published.

**Bracket layout.** Dynasty > Dynasty Setup > CFP Bracket now shows the 12-team playoff as a bracket: four columns (First Round, Quarterfinals, Semifinals, National Championship), each game with both teams and its result ("Miami won", "Scheduled", "TBD", or "USC - Champion" on the final). The selected game's teams turn gold, and the game's own header card above it shows both logos, the score and the bowl logo for that game. UP/DOWN still steps through the games. It is built at runtime from the text parts EA's spreadsheet already uses, on top of the hidden spreadsheet, so it needs no new art file.

**Tested in game** on three saves: the quarterfinal week of a season where the user's team has a bye, the end of a season (every round played), and an off-season save. No crashes. The previous list page is kept and can be restored by copying one file back.

**Limits.** There are no connector lines yet: the rectangle part EA's menus use does not draw when added this way. The stock row cursor still shows as a thin outline that moves in list order. Scores of finished playoff games are not readable from the page's script once their week has passed (all five lookups we tried return a placeholder), so earlier rounds read "X won" and the score is shown in the header card. During a playoff week, CPU games that were already simulated that week can still read "Scheduled".

**Test saves.** Two new bowl-week test saves were made on the PC port (end of season, quarterfinal week). A save whose user team has no bowl game cannot stop in the playoff weeks: one Advance runs every bowl week.

## 2026-10-29 (morning) - In-game pages ship in Play_PC; CFP page names the champion

Side track (EA's own menus, PC port). No game code, data or images are published.

**On by default for players.** Play_PC now loads the in-game pages (the PC Controls & Display tile and tab, and the College Football Playoff page) every time, read-only, without changing any installed game file or save. A new `ui_pages = on | off` line in `settings.ini` switches them off again; off gives exactly the old menus. The PC Controls & Display tab saves into the player's own `settings.ini` and rewrites only its four lines (checked on a full settings file with comments and every key).

**National champion.** After the season, the final row of the playoff page now reads "<team> - Champion". It comes from the same national-title data the game's Team History page shows. Final scores outside the bowl weeks are still not available: the game does not keep them anywhere the page can read.

**Clean rebuild.** Every staged menu file was rebuilt with the fixed number encoding from the previous update.

## 2026-10-29 (later) - PC Controls & Display works in game; CFP page shows winners

Side track (EA's own menus, PC port). No game code, data or images are published.

**PC Controls & Display works.** The native settings add-on is now built into the PC executable. The tab lists Keyboard Layout, Frame Rate, Render Scale and Speed Bundle with their current values. Changing the keyboard layout or the frame-rate cap and leaving the page takes effect at once (checked in game: the new keys work, the frame cap is active) and is written to `settings.ini`; the next start picks the values up again. Render scale and speed bundle apply at the next start. "Reset to default" now resets render scale to 2x, the PC default.

**Settings tile icon.** The tile shows our own PC icon (a monitor and keyboard drawn to match the game's menu icons) instead of the Origin logo.

**College Football Playoff page.** The header card now follows the selected game. The Result column shows who won each first-round, quarterfinal and semifinal game (taken from the next round of the bracket); scores are shown when the game still holds them. During the season the first round reads "Projected" and later rounds read "TBD" instead of showing last season's teams. Still open: the champion and final scores in the off-season (the game does not keep them where the page can read them), and a true bracket layout.

**Tooling fix.** Our ActionScript assembler wrote numbers from 128 to 255 in a form the game reads as negative; it now uses the game's own encoding (this also fixed a squeezed column).

## 2026-10-29 - In-game pages: CFP page shows the playoff, PC settings tab added

Side track (EA's own menus, title-update UI archive; PC port). No game code, data or images are published.

**College Football Playoff page (Dynasty > Dynasty Setup > CFP Bracket).** The page used to say "No Data": the game's bowl-games list only has data during the bowl weeks. The page now reads each playoff game from the game's league data instead and lists all 11 games in round order (first round, quarterfinals, semifinals, championship) with real teams. In the off-season it shows the playoff that was just played. Still to do: final scores, the team header above the list, and clearer labels during the season (the rows then hold partial or last-season data).

**PC Controls & Display.** The Settings tile now opens System Settings with a third tab, "PC Controls & Display". Its options (keyboard layout, frame-rate cap, render scale, speed bundle) come from a small native add-on that is built and tested offline but not yet part of the PC executable, so the tab is empty for now. The PC side that applies a change at once and saves it to `settings.ini` is written and unit-tested. The temporary "[P]" test marker is gone.

**Bigger UI code.** Our menu code had hit a 2 KB limit of the container it lives in; the container is now rebuilt with wider index fields, a layout the game already uses elsewhere (verified in game).

## 2026-10-28 - Documentation reorganized

README rewritten for newcomers (what it is, status, how the pieces fit). ROADMAP replaced with an ordered plan (frame rate, in-game settings page, Dynasty CFP bracket page, graphics and long-run checks, recruit realism, FCS league, more realism, online play, installer last) plus a Done list; the old versions are kept as docs/README_HISTORY.md and docs/ROADMAP_HISTORY.md. New docs/modding/ holds our function and table names, addresses and build method. New tools/check_public.py scans for local paths, emails, game-file types and binary content and must pass before every commit. CONTRIBUTING gained a docs-layout section. No game code, data or assets are published.

## 2026-10-28 - PC port: live gameplay now runs at full speed (it was in slow motion)

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Gameplay ran in slow motion; it now runs at real speed.** In live play the port's players, ball and game clock moved at only about 0.4-0.6x real speed, with dips lower in busy moments. The frame counter looked fine (30+ fps) because the game draws frames and advances the simulation on separate threads. The simulation uses a fixed step: each tick advances the game by exactly 1/30 s, whatever the wall clock says. The drawing thread kept producing frames at a normal rate, but the simulation thread spent most of its time waiting for the game's animation jobs (EA's "ANT" animation system on the emulated SPUs), so it managed only about 13-18 ticks per second instead of 30. Each frame therefore showed the game a little further along, but less than a real frame's worth: smooth frames of slow-motion play.

**The fix:** the animation jobs now run much more of their code as recompiled native code (a captured set of the hot animation modules), and several exact-equivalence shortcuts in the SPU code dispatcher are now switched on (cached code lookups, faster code verification). Each animation job now takes about 2.4 ms instead of about 5 ms (median). The simulation now keeps up: about 29.5-29.8 ticks per second, i.e. 0.98-0.99x real speed (the RPCS3 emulator runs at about 1.0x on the same scenes), with no frame-rate cost (fps +3%). That figure is for a PC with nothing else busy: the animation jobs share the CPU with everything else, so heavy background work costs game speed. With other programs using a few cores on the same PC, the fast path measured about 0.7x, against 0.5x for the old path in the same session.

**Off switch.** A rare freeze remains open: in testing, an animation job very occasionally reads inconsistent input and stops (0 times in 12 automated games with this setup, but seen with related partial setups). If the players ever freeze mid-play, set `speed_bundle = off` in `play_e\settings.ini` (see README_SETTINGS.txt) to go back to the old, slower path; a settings file without the line uses the fast path. Fixing that freeze is the next task.

**Validation:** automated gameplay runs (no corruption, no hangs), visual checks, and a same-session measurement of the simulation tick rate during live play.

## 2026-10-21 - PC port: borderless full-screen with G-SYNC/FreeSync, and a display settings file

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Smooth presentation on high-refresh displays.** The port used to open a fixed 1280x720 window that Windows stretched on high-DPI screens. Such a window is always composed by the desktop, so on a 144 Hz monitor every frame snapped to whole refreshes and variable refresh (G-SYNC/FreeSync) never engaged. There is now a borderless full-screen mode at the monitor's native resolution (a 4K screen gets the 2x internal render resampled straight to 4K) and a present mode without vsync waits. On a G-SYNC 144 Hz display, each frame now stays on screen for its own duration. Measured on screen: the gap between when a frame should appear (the game's own frame spacing) and when it does fell from 9-10 ms on average (90th percentile 17-21 ms) to 3-5 ms (90th percentile 9-12 ms). There is no frame-rate cost.

**Settings file.** The player launcher now reads a small settings file: window mode (windowed / borderless / fullscreen), monitor, present mode (vsync / vrr / immediate), a frame-rate cap (60 = the game's own limit, or an even 30 or 20), and the internal resolution scale. New installs start in borderless + VRR mode; `window = windowed` restores the old behaviour.

**What limits the frame rate (measured):** the game's live gameplay is not locked to 30 fps. It renders as fast as it can up to 60, and locks to 30 only in presentation screens such as the play call. The port reaches about 35-38 fps in gameplay because the emulated graphics command thread is fully busy (about 29 ms per frame). A "60 fps patch" therefore isn't needed; 60 fps is a throughput problem. Rates above 60 are not possible for the game logic. Frame generation would need motion data the game doesn't provide.

**Validation:** automated gameplay runs in the new mode and with the 30 fps cap (no corruption, no hangs), visual checks, and an on-screen timing comparison against the old window and against the RPCS3 emulator.

## 2026-10-21 - PC port: fix for SPU code cut off mid-function, plus a current performance baseline

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Cut-off SPU functions are no longer run as native code.** The recompiler splits SPU code that the game loads at run time into chunks. When a chunk ended in the middle of a function, the recompiled copy of that last function simply stopped at the cut and returned early, skipping the rest of the real function (in one case the store of its result, which made an animation job wait forever). The safety check before running recompiled code could not catch it, because the bytes it compares all matched up to the cut. Such functions are now always run by the SPU interpreter instead. This affected about 100 small functions in the default sets (mostly the audio mixer) and was the cause of the freezes seen when testing a larger recompiled animation-system set. No frame-rate loss was measured and audio is unaffected. `SPU_VC_TRUNC=0` reverts it.

**Current baseline (default settings, normal PC load, 9 minutes of live play):** 33.9 fps average; median frame time 27 ms, 90th percentile 39 ms, 99th percentile 91 ms; 4.0% of frames take longer than 50 ms. Input latency from pressing START to the pause screen appearing: about 176 ms (median).

**Also measured, not adopted:** the larger recompiled animation-system set now runs (about 60% less interpreted SPU work) but did not make frames faster in same-session tests, so it stays off. The automated test driver no longer causes delay-of-game penalties at the play-call screen.

**Validation:** automated gameplay runs (no corruption, no hangs), audio checks and visual checks.

## 2026-10-20 - PC port: near-camera geometry is clipped again (goalpost "wedge" fixed)

Side track (native Windows build via static recompilation). No game code, data or executables are published.

**Depth clipping restored.** On low gameplay cameras (offense near its own goal line) a large flat olive or yellow-and-black shape could cover the top edge of the screen, and dark-red slabs sometimes appeared at the frame edges near the camera. The cause: the renderer created every game pipeline with depth clipping switched off, so geometry closer to the camera than the near plane (the near goalpost right beside the camera, players next to it) was flattened onto the screen instead of being clipped. The PS3 graphics chip clips by default (as the RPCS3 emulator also does). The port now follows the game's depth-clip setting. Pre-snap test frames that showed the shape 7 times in 16 now show it 0 times in 14; an RPCS3 reference of the same camera angles is clean. `RSX_DEPTH_CLIP=0` reverts it.

**Also measured, not adopted:** two more SPU physics/collision jobs (character pose, contact queries) now also have recompiled versions that were checked byte-for-byte against the code the game loads, but they did not make frames consistently faster, so they stay off by default. A capture of the hot animation-system SPU modules was recompiled as well; it ran wrong code (that module is patched while it runs) and froze the game in testing, so it stays off. The automated test driver now also handles the free kick after a safety.

**Validation:** automated gameplay runs (no corruption, no hangs) and visual checks.

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
