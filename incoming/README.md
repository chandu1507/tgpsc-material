# Upload the validated Paper II 15-topic checkpoint here

**Required filename (keep exact):** `TGPSC_PAPER_II_15_TOPICS_REVISED_DRAFT.zip`

## Missing-upload recovery

The failed run on 22 October 2026 expected
`incoming/TGPSC_PAPER_II_15_TOPICS_REVISED_DRAFT.zip` relative to the repository root.
The workflow and importer agree on this path. The source archive was absent from
the failed run's commit. On 23 October 2026, the original checkpoint was recovered
and added here. A local run of the repository importer generated 15 chapter pages,
15 PDFs and 192 Markdown files. This validates import compatibility, not academic quality.

Archive SHA-256: `7f029e1710ace7409cafd4479952c628d02a0dd3bc635bf7c54e6f7a0a1c05ba`.

If replacing a missing or outdated archive, upload the actual validated 15-topic checkpoint using the instructions below.
Do not rename `downloads/TGPSC_GITHUB_PUBLICATION_SNAPSHOT.zip` as the source:
it is a publication backup, not the required checkpoint with 15 PDFs and source notes.

Committing the ZIP at the exact path to `main` starts a **new** import run automatically.
Alternatively, after the ZIP is committed, open **Actions → Import Paper II Full Notes →
Run workflow**, select `main`, and start a new run. Do not use **Re-run jobs** on
the old failure: it checks out the original commit, which lacks the upload.

## One-time GitHub upload

1. Download the checkpoint supplied in the TGPSC chat.
2. Open [GitHub's incoming folder](https://github.com/chandu1507/tgpsc-material/tree/main/incoming).
3. Choose **Add file → Upload files**, select the ZIP, and commit it to `main`.
4. The repository workflow [Import Paper II Full Notes](../.github/workflows/import-paper-ii.yml) validates the archive and commits all **15 complete topic HTML pages, 15 PDFs and Markdown notes**. The workflow creates a report `PAPER-II-IMPORT-REPORT.json`.
5. Inspect **Actions** and confirm the latest import workflow completed successfully. If GitHub Actions reports a permission error on push, allow GitHub Actions read/write repository permissions under **Settings → Actions → General**.

**Important:** The importer does not mark any material academically approved. It does not replace the homepage portal, and it refuses an incomplete archive.

Paper III chapters are published **individually**. Do not upload a batch of new Paper III chapters.
