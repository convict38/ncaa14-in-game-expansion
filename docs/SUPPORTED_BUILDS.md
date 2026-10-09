# Tested development build

| Component | Recorded identity |
| --- | --- |
| Platform/title | PS3 BLUS31159; APP_VER 01.00 |
| RPCS3 | 0.0.43-20250-304d544b Alpha |
| Firmware | 4.93 |
| Ghidra analysis | 12.1.4; PowerPC:BE:64:64-32addr; 4-byte pointers |
| JDK | Temurin 21.0.12.1+1 |
| Development Python | 3.13.9 |
| Decrypted ELF SHA-256 | `a486a9467c740637892df1fc407d8fea9d92d83cf11ff0de3fe464f934e47abe` |
| Original SELF SHA-256 | `27fb330ac0134ed94ae3a7eb4f0096fc398e8752ed6d23ee41b32aa3cefe117a` |
| RPCS3 executable SHA-256 | `132bcad1ec9acffa800d5e1d7afeb9b8180e457a37f66408f35c4c69a6cb2a89` |
| RPCS3 PPU patch key | `PPU-011a5e6caad2e7361265a9a230cf385f805671fb` |

The PPU patch key is a module identity, not the whole-file ELF SHA-1. Ghidra's output is checked against raw PowerPC instructions because some compiler helpers and query out-parameters decompile incorrectly.

These identities describe the tested development build. No compatibility claim is made for other versions or an installable public release.

## Candidate v6 identities

- Manifest SHA-256: `f0bdec2c9a7313b9c27e07ac84972d40d832b466c161af9d39d7b06c3a4972a3`
- Generated BOOT SHA-256: `a0cdd4e48e909ab600d1904fe67f99f6413a7a0e184d7dca0bf0d5e164674925`
- Generated MISC SHA-256: `665c6c5e29958650bfbd7c36a9bf6028bd314ca76f0d1e752c3bfe2f0621a2c4`

Same 517 executable words as v5; selected serialized capacities enlarged. These are reproducibility identifiers, not redistributed game files or a public release.

## Investigated, not supported: CFBR v21 / update 1.02

The CFBR executable differs from the validated baseline; all 517 existing same-address preimages mismatch. Do not apply the current candidate to it. See [CFBR compatibility](CFBR_COMPATIBILITY.md) for measured identities and the required port.

The unmodified CFBR baseline now passes fresh creation and cold save/load. Loaded ELF SHA-256 is `144dee9040da9cb1e8337844fbb685a0f06e560b8fee8d9ba1eac87b9e300c1c`; observed PPU key is `PPU-62e25ebc1957382b34f2778554943e40d6d84e3c`. This does not establish expansion-patch compatibility.
