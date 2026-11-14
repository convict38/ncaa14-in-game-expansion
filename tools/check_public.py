#!/usr/bin/env python3
"""Fail if the public repo contains content that must never be published.

Scans every tracked or untracked-but-not-ignored file under the repo root for:
  - local filesystem paths (C:\\Users\\..., C:/Users/..., /Users/<name>/, AppData)
  - the owner's email address pattern
  - forbidden file extensions (EA archives, executables, dumps, media, saves)
  - binary content (NUL bytes) in files that are not an allowed image type
  - screenshots / image files in general
  - game-derived address/function tables (over 200 hex-address+symbol lines in a file)
  - key-like files (key/klic/rap names, long hex strings labelled key or klicensee)
  - decompiler output (Ghidra FUN_/DAT_/LAB_/undefinedN, in_rN registers) in .c/.h files

Run before every commit:  python tools/check_public.py
Exit code 0 = clean, 1 = violations found.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

FORBIDDEN_EXT = {
    '.ast', '.edat', '.elf', '.self', '.sprx', '.prx', '.bin', '.iso', '.pkg',
    '.rap', '.rif', '.sfo', '.tdb', '.dat', '.usr', '.dmp', '.mem', '.core',
    '.exe', '.dll', '.sys', '.pup', '.rpcs3', '.psarc',
    '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.tga', '.dds',
    '.mp4', '.mkv', '.avi', '.wav', '.mp3', '.ogg', '.zip', '.7z', '.rar',
    '.pyc',
}
FORBIDDEN_NAMES = {'eboot.bin', 'ps3_game', 'usrdir', 'ncaa14.elf'}

CONTENT_PATTERNS = [
    ('local Windows path', re.compile(r'[A-Za-z]:[\\/]+(?:Users|Documents and Settings)[\\/]', re.I)),
    ('local Windows path', re.compile(r'[A-Za-z]:[\\/]+(?:tmp|temp)[\\/]', re.I)),
    ('local Unix home path', re.compile(r'(?:^|[\s"\'(`])/(?:Users|home)/[A-Za-z0-9_.-]+/')),
    ('AppData path', re.compile(r'AppData[\\/]', re.I)),
    ('owner email', re.compile(r'connorturley|@gmail\.com', re.I)),
    ('any email address', re.compile(r'\b[\w.+-]+@[\w-]+\.(?:com|net|org|io|edu)\b', re.I)),
    ('private key / token', re.compile(r'(?:ghp_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)')),
]

# Key-like file names (common key / klicensee / rap naming).
KEY_NAME = re.compile(r'(?:^|[/_.-])(?:klic(?:ensee)?|rap|rif|act\.dat|idps|keys?|disc_?key|eid_?root_?key)(?:[/_.-]|$)', re.I)
KEY_HEX = re.compile(r"""(?:key|klic|klicensee|rap|idps)\w*["']?\s*[:=]?\s*["']?(?:0x)?[0-9A-Fa-f]{32,}""", re.I)

# Address + symbol line, e.g. "0x00123456 FooBar" or "FooBar = 0x00123456".
ADDR_SYM = re.compile(r'(?:0x[0-9A-Fa-f]{6,8}\W+[A-Za-z_][A-Za-z0-9_:.]{3,}|[A-Za-z_][A-Za-z0-9_:.]{3,}\W+0x[0-9A-Fa-f]{6,8})')
ADDR_TABLE_LIMIT = 200

# Ghidra-style decompiler output; only checked in .c/.h files.
DECOMP = re.compile(r'(?:undefined[1-8]?|FUN_[0-9A-Fa-f]{4,}|DAT_[0-9A-Fa-f]{4,}|LAB_[0-9A-Fa-f]{4,}|in_r\d+|in_f\d+|unaff_r\d+)')

# Narrow allowlist: {relative path: {rule names}} with the reason for each entry.
ALLOW = {
    # Hand-written modding reference: our own names and notes for functions we patch
    # (207 lines, just over the limit). Not an exported table. Owner should review if it grows.
    'docs/modding/02-functions.md': {'addr-table'},
}

SKIP_DIRS = {'.git', '__pycache__'}
SELF = os.path.abspath(__file__)


def candidate_files():
    """Files git would publish: tracked plus untracked-not-ignored; fall back to a walk."""
    try:
        out = subprocess.run(
            ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
        names = [n for n in out.split('\n') if n]
        return [os.path.join(ROOT, n) for n in names if os.path.exists(os.path.join(ROOT, n))]
    except Exception:
        found = []
        for d, dirs, files in os.walk(ROOT):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            found += [os.path.join(d, f) for f in files]
        return found


def main():
    problems = []
    for path in candidate_files():
        rel = os.path.relpath(path, ROOT).replace('\\', '/')
        low = rel.lower()
        ext = os.path.splitext(low)[1]
        if ext in FORBIDDEN_EXT:
            problems.append(f'{rel}: forbidden file type {ext}')
            continue
        if any(part in FORBIDDEN_NAMES for part in low.split('/')):
            problems.append(f'{rel}: forbidden name')
            continue
        try:
            data = open(path, 'rb').read()
        except OSError as e:
            problems.append(f'{rel}: unreadable ({e})')
            continue
        if b'\x00' in data:
            problems.append(f'{rel}: binary content (NUL bytes)')
            continue
        if os.path.abspath(path) == SELF:
            continue  # this file contains the patterns themselves
        text = data.decode('utf-8', errors='replace')
        allowed = ALLOW.get(rel, set())
        if KEY_NAME.search(low) and 'key-name' not in allowed:
            problems.append(f'{rel}: file name looks like a key file')
        addr_lines = sum(1 for ln in text.splitlines() if ADDR_SYM.search(ln))
        if addr_lines > ADDR_TABLE_LIMIT and 'addr-table' not in allowed:
            problems.append(f'{rel}: {addr_lines} address+symbol lines (looks like a game-derived table, limit {ADDR_TABLE_LIMIT})')
        for lineno, line in enumerate(text.split('\n'), 1):
            for label, pat in CONTENT_PATTERNS:
                m = pat.search(line)
                if m:
                    problems.append(f'{rel}:{lineno}: {label}: {m.group(0).strip()[:60]}')
            if KEY_HEX.search(line) and 'key-hex' not in allowed:
                problems.append(f'{rel}:{lineno}: long hex string labelled as a key')
            if ext in ('.c', '.h') and 'decomp' not in allowed:
                m = DECOMP.search(line)
                if m:
                    problems.append(f'{rel}:{lineno}: decompiler output token: {m.group(0)}')
    if problems:
        print('check_public: FAILED')
        for p in problems:
            print('  ' + p)
        print(f'{len(problems)} problem(s).')
        return 1
    print('check_public: OK (no forbidden content found)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
