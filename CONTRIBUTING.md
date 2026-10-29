# Contributing

Use Issues to discuss findings, reproduce a problem or propose work. Label evidence as static, runtime-tested or hypothesis. Describe the exact tested build and the smallest reproducible observation.

Pull requests should explain the concrete change, its supported executable/data identities, validation, rollback behavior and remaining limits. Tests must exercise affected behavior rather than merely repeat implementation output.

This public repository is a reviewed export. The private development workspace also contains owned game data and test fixtures; it must never be pushed wholesale. Only explicitly reviewed project-authored text/source files belong here. Do not submit game dumps, extracted archives/assets, executables, firmware, saves, decompiled game code, credentials or personal data.

Licensing for a redistributable code release and any third-party components will be documented before release. Do not assume that public visibility permits redistribution of game assets or third-party mods. Compatibility with other NCAA Football mods requires its own test matrix.

## Docs layout (where things go)

- `README.md`: newcomer entry point and current status. Keep it short; put detail elsewhere.
- `CHANGELOG.md`: dated milestones with validation results. Add an entry after each milestone.
- `ROADMAP.md`: ordered plan plus a Done list. Move finished items from Next to Done; archive superseded text in `docs/ROADMAP_HISTORY.md`.
- `docs/modding/`: names, addresses, table layouts, patch inventory and build method. Our own analysis only.
- `docs/*.md`: stable topic documents (testing, builds, roster pipeline, handoff, research log).
- `tools/`: small reviewed scripts and their tests. `reports/`: machine-readable status.

Never publish: game or EA files (.ast, .edat, .elf, .self, .sprx, .bin dumps), extracted assets, decompiled pseudo-code, screenshots, saves, local paths, or personal email addresses. The `.gitignore` denies by default, so a new file type or folder must be explicitly allowed there.

Before every commit run `python tools/check_public.py`. It fails on local paths, email addresses, forbidden file types and binary content.
