# Table capacity check (138-team build)

Plain-language summary. Offline analysis of Dynasty save copies; no game was launched and the fix below is not yet runtime-tested.

## Finding

Two Dynasty tables are completely full by the bowl weeks of a 138-team season, and data is being dropped.

- **Team-week schedule table.** It was sized for 126 teams (18 rows each = 2268). With 138 teams the regular season and conference-championship week use 2208 rows. The postseason pass then fills the last 60 rows in alphabetical team order and stops. About 78 of 138 teams get no postseason rows, and roughly two thirds of postseason team-games are missing from this table. The games themselves are still scheduled, played and scored, because the sim reads the main schedule table. The loss is in the per-team schedule view (expected, not yet confirmed in game: a blank or bye line for the bowl).
- **Game-by-game player stat tables.** The offensive-line table fills at the end of the season and the defense table fills at quarter-final time in one of the two test saves. Only the last one to three postseason games lose their per-game stat rows (for example the national championship game for offensive linemen). Season totals stay correct, because they are updated separately.

Nothing carries over between seasons: these tables reset at rollover, so this is a per-season capacity limit.

## Fix (staged, not applied)

Raise four capacities in the Dynasty template, the same way the earlier history-capacity raises were done:

| Table | Old | New |
|---|---|---|
| Team-week schedule | 2268 | 3072 |
| Offensive-line game stats | 9178 | 11000 |
| Offense game stats | 16896 | 19500 |
| Defense game stats | 27028 | 31000 |

The save grows by 157,472 bytes and still has about 1.09 MB of headroom in the fixed-size save file. A new Dynasty is needed, because capacity is fixed when a save is created.

## How to validate

Create a new Dynasty with the candidate template, play through the bowls, and run the read-only checker on a copy of the save. It should report no full tables and no missing postseason rows, and a late-alphabet team's schedule page should show its bowl game.

If an FCS league is added later, the schedule table needs about 5852 rows (266 teams by 22 weeks).
