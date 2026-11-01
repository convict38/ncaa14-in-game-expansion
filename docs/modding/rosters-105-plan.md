# 105-player rosters: plan and Phase R0 findings

Status: Phase R0 (a read-only study of the game code) is done, 2026-11-01. Nothing in the game was changed. This page is a plain-language summary; the detailed site list stays in the private working notes.

## Goal (user decisions)

- FBS teams carry up to **105 players on one roster page**. The roster is not split into "active 70" and "reserves".
- FCS teams stay at **70**.
- A transfer-portal week comes later, after the roster work.

## How the game stores rosters today

- Every player has an ID number. The game gives each team a block of 70 numbers: team number x 70, plus the player's place on the team (0 to 69).
- So "70" is not one setting. The game works out a player's team by dividing his ID by 70, and it finds a team's players by looking for IDs in that team's block of 70.
- The study found **537 places in 236 game functions** that depend on that 70:

| Kind | Places | What it does |
|---|---|---|
| Player ID -> team (divide by 70) | 165 | 101 written out in place, 64 through one shared helper |
| Team -> first player ID (multiply by 70) | 108 | builds the start of a team's block |
| Player's place on the team | 9 | ID minus team x 70 |
| "Players of this team" searches | 208 | 104 pairs of "from the block start" and "up to start + 70" |
| Explicit roster limits | 21 | for example the Cut Players stage, enrolling recruits, transfers, "roster full" checks on screens |
| Fixed-size lists | 26 | game-day tables, roster and depth chart screens |

## Game day: the key question

When a game is set up, the game copies both teams' players into a separate game table. That table has room for **140 players, exactly 2 x 70**. There is also a game-day list of each team's players by position, sized for 70 per position. The roster and depth chart screens build lists of 70 rows, and one screen helper reports "maximum roster size = 70".

All of these are **size limits**, not deep engine rules. The code that runs during a game looks players up by ID and team as needed, so no fixed 70 was found there.

## Verdict and plan

**Feasible.** The chosen approach:
- Give every team a block of **105** IDs, FBS and FCS alike.
- Enforce the real limit per level at the roster-limit checks: **FBS 105, FCS 70**.
- Every used team number still fits in the game's 16-bit player ID.

Phase R1 (estimated 16-23 agent-days), every change behind an on/off switch:

1. **Data:** renumber every player ID in the starting data to the 105 blocks, and raise the table sizes. The main player table goes to about 27,000 rows, and the game-day table to 210.
2. **Code:** an automatic patch of the 537 places, so they use 105 instead of 70. Each patch is checked against the expected code.
3. **Limits:** FBS 105 and FCS 70 at the cut stage, at recruit enrollment, at transfers and on the roster screens.
4. **Game-day lists:** widen them to 105.
5. **Testing:**
   - start a new Dynasty;
   - play games with a 105-man team;
   - run three full off-seasons, with a check after every step that no player has landed on the wrong team.

## Costs and risks

- A save grows by about 2-3 MB at its largest point, in the off-season. The game's database memory setting goes up a little.
- **A new Dynasty is needed.** Every player ID changes, so old saves cannot be converted to the new layout by the game.
- The biggest risk is one missed place that puts a player on the wrong team without any warning. The automatic check after each step is there to catch it.
- Road to Glory, online play and Create-a-School keep their own 70-player assumptions. They are out of scope and will be checked once.

## Progress, Phase R1 (2026-11-01)

- Done: a save converter that moves every player ID to blocks of 105 and checks the result; an automatic patch of every 70-based ID calculation in the Dynasty code (switch: 70 = normal game); a re-scan that finds none left; a check that runs inside the game when switched on.
- Tested in the game: a converted Dynasty loads, shows its roster page and plays a week, and the saved file passes the ID check.
- Next: the per-level limits (FBS 105, FCS 70), the game-day tables (140 -> 210 players), the roster screens, then a new Dynasty with real 105-player FBS teams.
