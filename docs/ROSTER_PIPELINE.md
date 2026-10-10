# CFBR roster source and native save pipeline

## Runtime result: source selection at 126 teams

A separate copied development profile started without a roster or Dynasty save. Its only changed game asset was BOOT entry 355, replaced with the exact leading database from the bundled CFBR23V21 roster. Counts, table capacities and executable code stayed unchanged. All 826 other BOOT entries were retained.

The game booted normally and saved a new roster through File Management. The entire 1,433,600-byte saved USR matched the intended source byte for byte. All ten tables, their schemas, capacities and decoded records matched, including 126 FBS teams, 15 other team rows, James Madison at team 230 and the source-specific Generic row at 162. This establishes which roster was selected; the built-in source has different values.

A separate emulator process automatically loaded the new roster and opened Edit Rosters normally. All four saved files remained byte-identical. Six live executable comparisons passed in each run against the unpatched CFBR baseline. After process exit, profile configuration was restored. All 48 protected stock save files, all 58 files in the prior CFBR home, and 58 original-preservation checks passed. The roster regression report has 32 passing checks.

The first rollback attempt correctly refused while the emulator was still exiting. An aggregate check run before rollback therefore failed three configuration checks; that report is preserved. Once the process exited, rollback and the complete report passed. This was an ordering error in the test workflow, not a roster load failure.

| Identity | SHA-256 |
| --- | --- |
| Source-only BOOT candidate | `6fc42fb35b1ef82e8291e0b4e54c6071cd8a4b1e64dafa720e9b9925a4475511` |
| Source and native saved USR | `6ef52375314f1db9c412cad307895ce99a30968e24c0bd5537c2de3308059aa4` |
| Native HED | `ce03d756414c8076eb11fbc53538cdc572d24f8e19580944eedd9b875e208167` |
| Completed private regression report | `4f24359db9a0f724c06dfb05cc10a86d0bfe53d083dfdb87e63b5f4583d5b456` |

No save was manually edited. These results cover source routing and ordinary roster save/load at 126 teams. They do not establish enlarged reserves, additional active teams, Dynasty creation, a season or a playoff for this candidate.

## Save-container findings

The pinned bundled roster has a 28-byte HED, a 1,433,600-byte USR, a 1,320,160-byte leading TDB and 113,440 zero trailing bytes. The HED total-size word equals HED plus USR length. A fail-closed recognizer and unchanged roundtrip passed 13 checks, including nine rejection cases. It does not write altered containers.

The game-generated HED differs from the packaged HED while the USR remains identical. Opaque HED fields and their integrity algorithm are unresolved. Static filename/reference inspection identified generic save callbacks, not the concrete header serializer. Native saving avoids inventing this framing, but changed-size acceptance remains untested. Zero bytes are not automatically usable capacity.

## Minimal reserve planning for 138 teams

An offline planning candidate preserves the existing 126-team contents and passes ten checks. Its assumptions are 70 players and 88 depth rows per FBS team, three coaches and skill rows per FBS team, 25 retained other coaches, all 15 other team rows, and 12 additional distinct stadium rows.

| Table | Existing maximum | Proposed maximum | Extra bytes |
| --- | ---: | ---: | ---: |
| TEAM | 146 | 153 | 1,820 |
| PLAY | 9,100 | 9,660 | 62,720 |
| DCHT | 11,464 | 12,144 | 5,440 |
| COCH | 409 | 439 | 3,840 |
| CSKL | 409 | 414 | 140 |
| STAD | 200 | 210 | 4,640 |
| Total | | | 78,600 |

This arithmetic leaves 34,840 bytes within the current USR length. The arithmetic alone does not show that generated/non-FBS lifecycle rows fit. Broader reserve candidates are separate artifacts and remain uninstalled.

## Runtime result: grown capacities at 126 teams

A BOOT candidate replaced only entry 355 with the minimal-reserve database above, preserving the other 826 entries, including the Dynasty template. It passed 40 offline checks before installation. It ran in a new copied profile with no inherited roster or Dynasty save; the previous source-only profile was not reused because its saved roster would auto-load.

The first boot auto-loaded only the profile save, not a roster. A roster was then saved through File Management. The game's native serializer kept every grown maximum: TEAM 153, PLAY 9,660, DCHT 12,144, COCH 439, CSKL 414 and STAD 210, with CONF 26 and DIVI 22 unchanged. It did not shrink tables back to their earlier sizes. All records and schemas remained intact, with 126 FBS and 15 other team rows. A separate process auto-loaded the saved roster normally, and all four save files stayed byte-identical. Six baseline live executable reads passed in both runs. After the emulator exited, the profile redirect was rolled back. The 48-check regression report, 48 protected stock files and 58 original-preservation checks passed.

| Identity | SHA-256 |
| --- | --- |
| Capacity-only BOOT candidate | `39420929ea9423c52a15aed6b0213f0d483c3ba6b4601f77b3f10f937d017a2b` |
| Native and cold saved USR (1,433,600 bytes) | `9d92f57c3203c239eff2373f81c0115d938094f6faed0ec3068bacc680f9958a` |
| Private regression report | `9b2c1aa819a806860b18df571e1d38c1ec66d88a539ca8e850f9ce12f75f0396` |

No identities were added, no code changed and no save was edited by hand. This establishes only that grown serialized reserves survive native roster saving and cold auto-load. It does not establish engine-side team limits, use of the reserve rows, Dynasty creation, seasons, recruiting or rollover with the grown tables.

## Runtime result: grown Dynasty tables through a season and rollover

A Dynasty created on the roster-only BOOT above had the **unchanged** CFBR Dynasty capacities (TEAM 146, PLAY 9,100, DCHT 11,464, COCH 409, CSKL 409, STAD 200), the same as the unmodified baseline. This trial passed 16 checks. Dynasty table sizes come from the BOOT354 Dynasty template, not from the loaded roster.

A coordinated BOOT then grew template entry 354 to the same six capacities and kept entry 355 as the minimal-reserve roster (16 offline checks). It ran in a new clean profile at 126 FBS and 131 Dynasty teams:

| Stage | Result |
| --- | --- |
| Fresh offline Dynasty (Alabama, existing coach) | The autosave written by the game has TEAM 153, PLAY 9,660, DCHT 12,144, COCH 439, CSKL 414 and STAD 210 |
| Cold restart and Dynasty load | All four save files byte-identical; 21-check report passes |
| Regular season simulated (Alabama 6-6) | 28 season checks; 809 games |
| Postseason (bowl loss, 6-7) | 28 checks; 850 games |
| Off-season advanced to Pre-Season 2014 | 30 rollover checks; year advanced, 126 complete 12-game schedules, no collisions |
| Every snapshot | 7 grown-capacity checks; capacities never shrank |

At Pre-Season 2014 the used rows were TEAM 131, PLAY 8,694, DCHT 11,088, COCH 398, CSKL 383 and STAD 198, all within the grown tables. The coaching carousel added coach rows during the off-season. Each run passed six live code reads. After the final run, the profile redirect was rolled back; 48 protected stock files and 58 original-preservation checks passed. The draft-class save prompt was skipped.

| Identity | SHA-256 |
| --- | --- |
| Fresh and cold Dynasty USR | `b3c8ef7485cb70bf4cf60d8bcb7d71809b6cc4ee13b8f7fd84bbacb5b1d9ec18` |
| End of 2013 USR | `a7938fdc607cc474701e005a30bbf2bfa61f6bb437f834d6828232f09b102921` |
| Pre-Season 2014 USR | `7a7a434f1a763fb5cbc590e7208a6f13a83f03adb6c8f3c66a801d013536cc0f` |

No identities were added, no code changed and no save was edited by hand. This completes the capacity-only ladder: roster save and reload, fresh Dynasty, cold reload, season and rollover. It does not establish engine-side team limits, use of the reserve rows, played games, recruiting signings with added teams, or repeated seasons.

Next, add the first identity rows inside the reserve. Keep the BOOT355 roster and BOOT354 template coordinated, with unique TEAM, PLAY, DCHT, COCH, CSKL and STAD rows, and start with inactive rows. Do this before combining them with a complete CFBR-specific engine recipe. Keep recruiting array width, allocation, clear lengths, indexing, temporary vectors and save capacities consistent. Active expansion still requires fresh-Dynasty, gameplay, scheduling, recruiting, postseason, rollover and cold-load validation. Graphics remain a later priority.

## First added identity inside the reserve (runtime-tested)

The next rung appended one non-FBS identity to the auto-loaded roster (BOOT entry 355) inside the minimal 138-team reserve: TGID 165 "FCS Test", cloned field-for-field from the shipped generic FCS row TGID 164 (TTYP 1, TORD 433, coach link equal to its own ID), plus three coach rows with new coach IDs. Like the five shipped generic FCS rows, it has no players, depth chart, coach skills or stadium. The Dynasty template (entry 354) was not changed. Team lists filter on team ID and the FBS list additionally on TTYP 0, so a non-FBS identity grows the all-team list without touching the engine's fixed 126-FBS loops. This is also the first step toward FCS support.

| Step | Checks |
| --- | --- |
| Offline candidate (only entry 355 changed; size unchanged) | 36 |
| Fresh Dynasty: 132 teams, 126 FBS, new identity exactly once, capacities grown | 20 |
| Cold reload: four save files byte-identical | 4 |
| 2013 regular season / postseason / rollover to 2014 | 28 / 28 / 30 |
| Grown capacities per snapshot | 7 |

Dynasty creation sets the visibility flag on all generic FCS rows and moves their coaches into the free coach pool; the added identity behaved identically to the native rows. It had no games in the preset 2013 schedule, but the game's own 2014 schedule generator scheduled it seven times. Both live code probes passed and the profile was rolled back. This does not test added FBS teams, engine count limits, players on an added team or recruiting by an added team.

Next: added identities with rosters, and added FBS membership, which requires the engine count recipe.
