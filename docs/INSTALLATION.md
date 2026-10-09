# Installation status

**There is no public installable release yet.** The local development installers depend on intermediate research artifacts and are not portable. Copying a generated patch file alone is insufficient: the tested experiments coordinate executable patches with game databases.

## Intended supported starting point

A user's own NCAA Football 14 PS3 dump, title BLUS31159, application version 01.00, with the exact executable identity in [SUPPORTED_BUILDS.md](SUPPORTED_BUILDS.md). The current development baseline uses RPCS3 0.0.43-20250-304d544b and firmware 4.93. This is a tested configuration, not a recommendation to upgrade or downgrade an existing setup. Other title versions, updates, platforms and combinations with other mods are untested.

If you already have the decrypted executable, the included tool can check its identity without modifying it. Python 3.11 or newer is required:

```powershell
python tools/verify_game_identity.py "PATH_TO_YOUR_DECRYPTED_EBOOT.elf"
```

This checks file identity and ELF structure only. It does not install a mod or verify live emulator state. Do not upload the executable with a bug report.

## Planned release installation workflow

1. Download a tagged release and verify its published checksums.
2. Create an isolated working copy of the supported dump, RPCS3 configuration and saves. Keep originals separate.
3. Run the release's preflight check. It will reject unsupported builds, unexpected existing modifications and an active target emulator.
4. Generate patched databases locally from the user's own dump using the release's recipes. Verify source/output hashes and patch preimages before enabling anything.
5. Enable the coordinated runtime patches and generated assets together.
6. Create a separate test Dynasty, perform the release's smoke tests, then use only the documented save compatibility path.
7. To remove the experiment, stop that isolated emulator and restore the verified pre-install backups.

These steps describe the intended installer contract; there is currently no command claiming to complete them. Expanded Dynasties must not be loaded under stock code. Save migration/backward compatibility is not established.

Future releases will include exact commands, supported hashes, dependency versions, backup locations, verification output, rollback instructions and known limitations. Each tested release will be immutable; new changes will receive a new version.
