"""Read-only identity check for a user's decrypted NCAA14 PS3 executable.

This does not decrypt files, install patches, or validate live emulator state.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

EXPECTED = "a486a9467c740637892df1fc407d8fea9d92d83cf11ff0de3fe464f934e47abe"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    args = parser.parse_args()
    with args.executable.open("rb") as stream:
        header = stream.read(64)
        stream.seek(0)
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    checks = {
        "elf_magic": header[:4] == b"\x7fELF",
        "elf64_big_endian": header[4:6] == bytes((2, 2)),
        "powerpc64_machine": len(header) >= 20 and struct.unpack_from(">H", header, 18)[0] == 21,
        "supported_sha256": digest == EXPECTED,
    }
    result = {"supported_development_build": all(checks.values()), "sha256": digest,
              "checks": checks, "mod_installed": False,
              "scope": "File identity only. No game data is modified or uploaded."}
    print(json.dumps(result, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
