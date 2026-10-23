#!/usr/bin/env python3
"""Create a publication-only ZIP from GitHub-tracked project files.

DO NOT mistake this archive for the unpublished cumulative master checkpoint.
"""
from __future__ import annotations
import os, pathlib, subprocess, zipfile
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "downloads" / "TGPSC_GITHUB_PUBLICATION_SNAPSHOT.zip"
OUT.parent.mkdir(parents=True, exist_ok=True)
tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\0")
paths = sorted({os.fsdecode(x) for x in tracked if x})
safe = []
for name in paths:
    if name.startswith(("downloads/", ".git/")):
        continue
    path = (ROOT / name).resolve()
    if not path.is_file() or not path.is_relative_to(ROOT):
        raise RuntimeError(f"Unusable tracked path: {name}")
    safe.append((name, path))
note = (
    "TGPSC GROUP I — GITHUB PUBLICATION SNAPSHOT\n"
    "This is a ZIP of the files that are published in GitHub, NOT the full 19-topic\n"
    "master checkpoint held in the Project Library. PDFs and editable source files\n"
    "that have not been uploaded to GitHub are absent.\n"
    "The 18 expanded-draft tags in the site navigation do not imply final approval.\n"
    "Academically approved topics: 0 of 75.\n"
    f"GitHub source commit: {os.environ.get('GITHUB_SHA', 'local')}\n"
)
with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=7) as z:
    z.writestr("PUBLICATION_SCOPE.txt", note)
    for name, path in safe:
        z.write(path, name)
with zipfile.ZipFile(OUT) as z:
    bad = z.testzip()
    if bad:
        raise RuntimeError(f"Corrupt entry: {bad}")
print(f"Built {OUT} ({OUT.stat().st_size} bytes), {len(safe)} tracked source files")
