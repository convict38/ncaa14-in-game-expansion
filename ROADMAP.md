# Roadmap and acceptance gates

## Next development work

1. Extend the passed v6 reserve regression at 127 active teams to repeated seasons. Resolve missing prototype TPHS/RBKS initialization, record-type coverage and their full-membership bounds. Resolve remaining recruiting-reference semantics: commitment status plus board membership does not establish the destination team; position changes must be accounted for in identity matching.
2. Resolve coach-selection filtering and remaining presentation consumers. Audit dependent consumers and repeated-season/full-FBS capacities, including contract lifetime, history tables and the opaque save-container trailer. Larger serialized reserves alone do not establish larger active counts.
3. Add the complete target FBS membership while retaining existing teams. Implement realistic conferences, schedules, uniforms, names and team presentation. Freeze a documented target season and membership list before final content validation. Integrate [CFBR presentation and other updates](docs/CFBR_COMPATIBILITY.md) through a separately verified 1.02 executable port and team-ID remapping; retain all original schools.
4. Implement the in-game 12-team playoff: selection, seeding/byes, first-round sites, legal dates, four rounds/11 games, results-driven advancement, championship history, awards and normal season rollover.
5. Package and validate a portable installer and uninstaller against a clean supported user dump and isolated saves.

## Release acceptance

- Exact supported executable identities; refuse unknown builds and unexpected patch preimages.
- All existing teams retained; added teams work in gameplay and simulation, recruiting, statistics, standings/rankings, save/load and repeated season rollover.
- No schedule collisions, missing games or invalid team/stadium references; conference scheduling rules are tested.
- Playoff selection and every round survive save/load. Re-entering a completed stage must not duplicate games, awards or championships.
- No external save editor is required between rounds or seasons.
- Installation builds changes locally from the user's own files, preserves originals, verifies outputs and supports rollback.
- A clean-machine installation and removal test passes before a public installable release.
- Distribution contains project-authored patch recipes/tools and reviewed documentation, with third-party attribution and licensing settled before release.

## Later extensions

Configurable playoff formats, FCS league support and custom stadium work. These remain separate from the initial acceptance scope.
