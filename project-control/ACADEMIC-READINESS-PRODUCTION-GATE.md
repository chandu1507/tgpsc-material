# TGPSC Group I — Academic Readiness Production Gate
Date: 2026-10-26
Scope: existing 75 topics only (Papers II–VI × 3 units × 5 topics).
This is a production checklist, not academic approval. Do not set academic_status=approved from this file.

## Order of work
For EACH existing topic, finish gates R1–R8 before initiating the independent academic audit (R9). Do not add a topic or replace the preserved original PDF until the consolidated edition passes checks.

- R1 Syllabus mapping: quote exact official commission item internally; map each subpoint to specific chapter headings and evidence. Missing subpoints block readiness.
- R2 Consolidation: inventory original notes, PDFs, supplements and prior repairs; eliminate overlapping text in ONE coherent student edition, preserving original artifacts and provenance separately.
- R3 Textbook depth: write substantive nonrepetitive explanations with background, causes, chronology, mechanisms, consequences, Telangana examples, limitations and competing interpretations where applicable. One-paragraph treatment of major concepts blocks readiness.
- R4 Source verification: claim-level log of dates, laws, events, quotations, numerical data and contested interpretations; primary or reputable scholarly sources; flag inaccessible sources explicitly. No invented archival consultation or fabricated source page numbers.
- R5 Questions: check at least 25 original four-option MCQs for correct keys, plausible distractors, explanation, syllabus fit and nonduplication; label PYQ as official only with verified commission year/paper/question number.
- R6 Mains: six or more complete 200–250-word structured model answers, with headings, specific evidence, analytical balance, limitations and conclusion; separate answer blueprints.
- R7 Learning aids: accurate original diagrams, relevant timeline/maps/tables, revision sheet, practice checkpoints and source bibliography; every visual cross-checked with text.
- R8 Publication readiness: generate ONE integrated student PDF and editable master, render/visually inspect every page, validate internal links, archive CRC, hashes, original-file preservation, offline portal links and topic count exactly 75. Record GitHub commit and actual workflow artifact if published.
- R9 Independent academic audit: only after R1–R8 pass; record named independent reviewer, scope, findings, corrections and sign-off. User study acceptance is separate.

## Required evidence per topic
Maintain `project-control/academic-readiness/<paper>-<unit>-<topic>.json` with gate statuses NOT_STARTED / IN_PROGRESS / BLOCKED / PASS, objective evidence paths, outstanding issues, reviewer details, and immutable original PDF SHA256. Do not mark PASS without evidence. Keep project-wide academic approvals at zero until external sign-off.

## Current baseline (reconciled 2026-10-26, Turn17)

The repository contains **exactly 75 existing first-draft topic slots and original topic PDFs**; **zero topics** have passed all R1–R8 and **zero** have independent academic approval. The current topic-level status index is the canonical summary, not the older pilot paragraph in this document.

Five existing topics are IN_PROGRESS: 2-2-4, 2-2-5, 2-3-1, 2-3-2 and 2-3-3. Topic 2-3-4 is ASSESSED_REBUILD_REQUIRED. Sixty-nine topics remain NOT_ASSESSED. Topic 2-3-3 now has one integrated editable working master with 14 explanatory concepts, 25 original explained MCQs, six 200–250-word mains answers and two original SVG diagrams. Thirteen concepts remain under 300 words, and the direct original commission PDF retrieval was HTTP 403 in the latest run; therefore **R1–R8 remain IN_PROGRESS** and R9 NOT_STARTED. The original 7-page PDF SHA256 d935e79390c4e9d9d84c96d41f8c0d454d4e20462d64e9cd9f9a56e27478a9c9 is preserved. Rendering/publication verification is recorded separately and must not be presumed from source commits.

A substantive hydrology correction was made to existing Topic 2-3-3 notes and portal: recharge is an internal flux for a whole-catchment water budget and can be an outflow for a soil-zone budget; it must not be counted twice. The partial 11-claim source register and limitations are in `project-control/academic-readiness/2-3-3-primary-claim-and-hydrology-audit-2026-10-26.json`.

## Reconciled Topic 2-3-4 preflight (26 October 2026, Turn17)

Five existing topics remain IN_PROGRESS (2-2-4, 2-2-5, 2-3-1, 2-3-2, 2-3-3); existing Topic **2-3-4** is now **ASSESSED_REBUILD_REQUIRED**, leaving **69 NOT_ASSESSED**. The original Topic 2-3-4 8-page PDF SHA256 `5a544ab369c285c6cc54cafa7ade872bddc2b9f517a6cffe19ec1048586496d1` remains preserved and its Git blob matches the archived source. All 15 explanatory concepts are under 150 words; no original explained four-option MCQs, only two mains answers (258/244 words), zero original SVG diagrams. A six-section earlier repair exists in the consolidated source but a synchronized integrated PDF has not been demonstrated. The previous local quality-audit checklist incorrectly marked depth and diagrams complete; it has been corrected. R1/R2/R4 IN_PROGRESS, R3/R5/R6/R7/R8 BLOCKED. Evidence: `project-control/academic-readiness/2-3-4-objective-gap-assessment-2026-10-26.json`. **Exactly 75 topics, zero fully R1–R8 ready, zero independently approved.**

## Immediate production queue

Finish Topic 2-3-3 synchronized CI PDF, original-preservation/ZIP/portal QA and detailed page review. Then expand the remaining shallow concepts **substantively**, complete direct primary-source and MCQ distractor checks, and progress the next existing Paper II/III topic. Keep Topic 2-3-2's 35 concepts below 300 words and pending MCQ/mains reviews visible. Do not stall indefinitely on inaccessible Topic 2-2-5 historical originals; record R4 BLOCKED and advance other work. Never treat word count, artifact CRC or workflow success as academic approval. Independent R9 starts only after every R1–R8 gate genuinely passes.


## Topic 2-3-4 integrated working master (26 October 2026, later production cycle)

The original topic slot remains unchanged. A single editable working master has been committed in `Paper 2/Unit 3 - Geography of India and Telangana/Topic 4/source/integrated-student-edition-2026-10-26.md`, combining the existing 15 concepts, earlier six-section repair, 25 new explained original practice MCQs and six mains drafts. Four newly written mains answers have 213/211/212/222 words; the two inherited answers need review, including one previously exceeding 250 words. All 15 inherited concepts remain under 150 words; MCQ keys and distractors are NOT independently fact-checked. There is NO synchronized new PDF or verified new artifact. R1/R2/R4/R5/R6 IN_PROGRESS; R3/R7/R8 BLOCKED; no R9. Six topics IN_PROGRESS, 69 NOT_ASSESSED, ZERO R1–R8 ready, ZERO independent academic approvals.


## Current controlling reconciliation — 27 October 2026 (supersedes historical counts above)

**Exactly 75 original topic slots remain; six IN_PROGRESS** (2-2-4, 2-2-5, 2-3-1, 2-3-2, 2-3-3, 2-3-4), **one ASSESSED_REBUILD_REQUIRED** (2-3-5), **68 NOT_ASSESSED**. **Zero R1–R8 fully ready; zero independent academic approvals.** Earlier Turn17 paragraphs are retained as dated historical evidence, not current totals.

Topic 2-3-4's existing integrated Markdown was expanded in place at §§4,5,6,9 with source-critical canal/tank, Mission Kakatiya, CGWB aquifer-management and statutory SEZ distinctions. Its 19-page synchronized PDF was produced by GitHub Actions run **40382078154** (SUCCESS), SHA-256 **ecb00777352f8c5a7fdb2183d33d47b928d49a7518551651b51d71f1eae60006**. The original 8-page PDF remains preserved. **Eleven of 15 original narrative concepts remain below 150 words**. Full downloaded post-render packaging, page-by-page visual accessibility, MCQ distractor and mains source audits are still incomplete; R8 IN_PROGRESS, not PASS.

Topic 2-3-5 objective audit: preserved original 8-page PDF SHA-256 **a842add222d65564077c1451a86a6e8d2c001d88aa6c2866f320a1bb5212ea18**; all 16 original numbered concepts under 150 words, prior eight-section repair exists, **zero** explained original four-option MCQs, **two** structured mains drafts, **zero** original SVG diagrams. See `project-control/academic-readiness/2-3-5-objective-gap-assessment-2026-10-27.json`. Existing `quality-audit.md` false-positive checkboxes were corrected. Do not label official PYQs without verified commission year/paper/question number.

The readiness status index and per-topic JSON are the current operational truth. Academic approval is not implied by PDF generation, GitHub workflow success, numerical word counts or ZIP integrity.

**27 October correction to the controlling paragraph:** A page-level contact-sheet review of the first 19-page Topic 2-3-4 render found an incorrect hard-coded **Topic 3** footer/title from the reused renderer. A dedicated `scripts/render_topic_2_3_4.py` and guarded workflow corrected the footer; final render run **40382863495 SUCCESS**, new PDF SHA-256 **0412885a569938b953318ede598a95d85ec794549144d3aa47fe1a0bbf69b467**. The earlier PDF hash in the historical paragraph is superseded. Full-resolution accessibility and post-render artifact QA remain pending, R8 IN_PROGRESS.
