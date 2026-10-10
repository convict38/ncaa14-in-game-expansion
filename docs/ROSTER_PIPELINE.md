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

Next, create a fresh Dynasty on this BOOT at 126 teams and confirm that its creation, save and reload keep the grown tables. Then add the first identity rows within the reserve before combining them with a complete CFBR-specific engine recipe. Keep recruiting array width, allocation, clear lengths, indexing, temporary vectors and save capacities consistent. Active expansion still requires fresh-Dynasty, gameplay, scheduling, recruiting, postseason, rollover and cold-load validation. Graphics remain a later priority.
