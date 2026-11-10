# MyAdvisor — final submission checklist

> **Approved-allocation update ? 27 October 2026:** [Current correction record](reports/degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


## Current corrected-build checklist ? 27 October 2026

**NOT submission-ready.** The 139-page PDF and its validation below are historical and unchanged. Do not use them as evidence of the corrected code. See the [verified correction report](reports/audit-correction-report.md); the original rubric rows below describe the prior assembly.

| Official rubric / submission requirement | Current status |
|---|---|
| Implementation 25% ? views / minimum viable features | Implemented; F05 fictional credit allocation pending owner approval. F06 automated contrast passed, human acceptance pending. |
| Implementation 25% ? authorization | F01 corrected locally using StudentDep before HTML writes; 12 real-auth wrong-role variants require 403 and unchanged full DB. F09 CSRF and F15 production key policy remain open security qualifications. |
| Implementation 25% ? REST conventions | Existing resource JSON API preserved; full regression suite passes. No new Postman runtime proof. |
| Test Plans 25% ? isolated unit tests | Existing detailed UT plan retained; current full run contains all 113 unit nodes. |
| Test Plans 25% ? main integration functionality | Existing IT plan plus [correction coverage](reports/requirements-test-traceability.md) includes HTML denials, actual engine FK policy and registration/contrast. |
| Test Plans 25% ? reasonable UAT tasks/criteria | Original 20 cases preserved; [focused missing checks and browser steps](reports/correction-retest-guide.md) prepared. |
| Test Implementation 25% ? according to plans | Focused regressions implemented; 20 new variants. Manual execution remains incomplete. |
| Test Implementation 25% ? unit/integration CLI | Final targeted **284 passed**; full **735 passed**, zero failures/errors/skips, 1 warning each. Real output/XML retained. |
| Test Implementation 25% ? Postman scripts | Local 90-request collection structurally validates; all 93 scripts compile; 15 JSON operations represented. No corrected-build Runner run. |
| Test Implementation 25% ? runnable Postman collection | Locally available; F02 missing JSON on intended published main remains open. Full new runtime run required. |
| Test Reporting 25% ? passing unit/integration screenshots | Six genuine historical images retained. New logs/XML cover corrected build; old images do not attest it. |
| Test Reporting 25% ? passing Postman screenshot | Six historical images retained. Corrected-build runtime/screenshot evidence pending; F03 publication open. |
| Test Reporting 25% ? completed UAT report | F04 open: historical **1 Pass / 0 Fail / 19 Not Run**, 18 partial. No promotion of observations to Pass. |
| One PDF containing listed deliverables | Prior 139-page PDF preserved; **revised PDF intentionally not generated** under current instruction. |
| Correct repository / latest files published | Wrong local origin unchanged; local corrections uncommitted. F02/F03 remain open. [Safe publication plan](reports/repository-publication-plan.md), no push/remote change. |
| Evidence and secrets | Historical images preserved; new isolated logs/source hashes retained. Scoped candidate scan and exclusions recorded; no private DB/key/cookie copied. Final staged review remains necessary. |
| Final readiness | Pending F05 owner approval, new Postman/manual evidence, publication and documented security dispositions. |

---

## Preserved Prompt 16 assembly checklist (earlier build)

Reviewed: **27 October 2026 (America/La_Paz)**. **Decision: PDF compilation completed; NOT submission-ready.** No Critical audit finding was verified. High findings **F01–F05 remain open**. No grade is assigned.

## Official Assignment 2 marking rubric

Basis: [official brief source record](official-assignment-brief.md), the student-supplied official wording retained during Prompt 15. The assessment weighting is 15%; the following four components are each 25%. I/P/T/R labels are audit tracking labels, not official rubric IDs. Both linked Google template documents remain inaccessible on the Prompt 16 access attempt, so template-specific details remain unverified. The Assignment 1 competency rubric is excluded.

| Component | Requirement | Status at final assembly | Evidence / qualification |
|---|---|---|---|
| Implementation — 25% | I1 Appropriate views facilitate minimum viable features | Partial | WF1–WF3 implemented; degree requirement discrepancy F05 and readability F06 remain. |
| Implementation — 25% | I2 Authorization implemented | Partial — High blocker | JSON roles and ownership tested; HTML Advisor submission/self-approval bypass F01 remains reproduced and unfixed. |
| Implementation — 25% | I3 Views follow REST API conventions | Satisfied in reviewed API scope | Resource paths, GET/POST/PUT/DELETE, creation Location and structured error contracts; HTML redirects documented. |
| Test Plans — 25% | P1 Unit testing of modules in isolation | Satisfied | All UT-01–UT-23 specifications, fixture vocabulary, inputs, steps and independent expected outcomes in PDF §7.2. |
| Test Plans — 25% | P2 Integration tests cover main functionality | Partial | All IT-01–IT-20 specifications and real-auth implementations; HTML wrong-role and actual-engine FK gaps remain F01/F07. |
| Test Plans — 25% | P3 UAT gives reasonable user tasks/success criteria | Satisfied as planning | Original wireframe mapping and all UAT-01–UAT-20 planned inputs/steps/expected outcomes in §7.1; this is not acceptance. |
| Test Implementation — 25% | T1 Tests implemented according to plans | Partial | All UT/IT groups have implementation mappings; audit gaps and incomplete manual conditions remain. |
| Test Implementation — 25% | T2 Unit/integration tests runnable via CLI | Satisfied | Genuine marked-run screenshots and audit complete-suite text/XML, exit 0; commands/environment in §§8–9. |
| Test Implementation — 25% | T3 All Postman API test scripts implemented | Satisfied locally, with scope limits | Existing v2.1 JSON: 90 requests, 93 script blocks compile, all 15 JSON operations. F13 assertion-depth limitation disclosed. |
| Test Implementation — 25% | T4 Postman collection runnable | Partial — publication blocker | Local collection structurally validates and retained Runner succeeds; required JSON absent from rechecked public main (F02). No new runtime run. |
| Test Reporting — 25% | R1 Screenshots of passing unit/integration tests | Satisfied | Three original Unit and three Integration screenshots embedded; 113/194 passes and warning/deselection totals preserved. |
| Test Reporting — 25% | R2 Screenshots of passing Postman collection run | Satisfied in local PDF; publication partial | All six genuine Runner captures embedded; absent from public main (F03). One run, not six independent runs. |
| Test Reporting — 25% | R3 Completed UAT report | Partial — High blocker | All 20 records included, but **1 Pass / 0 Fail / 19 Not Run**: 18 partial cases and UAT-05 required workflow unverified (F04). |
| Final deliverable | D1 One PDF containing listed submission elements | Compiled and validated locally | [COMP3613_Assignment2_MyAdvisor.pdf](COMP3613_Assignment2_MyAdvisor.pdf). Document completion does not close functional/UAT/publication blockers. |

## Required submission elements

| Element | Status / PDF location |
|---|---|
| Name and university ID | Verified from explicit original Student transcript statement and corroborated by original Assignment 1 PDF cover; included on cover. Demo screenshot ID is not used. |
| University/course details | COMP 3613 / Assignment 2 verified. University/campus and full course-title wording are omitted because reviewed project materials do not verify them. |
| Project description | §3: original system, improvements, actors, three workflows, functions and technologies. |
| Genuine Use Case Diagram | §4: original PNG embedded, unchanged. |
| Authentic ERD | §5: genuine seven-entity Mermaid source rendered as vector boxes; exact relationship/cardinality table and model correspondence included. |
| Original Assignment 1 wireframe | §6: complete original and enlarged pixel excerpts; original file preserved. |
| Detailed UAT plan | §7.1: all 20 case IDs, preconditions/data, browser tasks and expected outcomes. |
| Detailed unit plan | §7.2: UT-01–UT-23, F1 and E01–E12 baseline vocabulary; no generic replacement. |
| Detailed integration plan | §7.3: IT-01–IT-20, F2 isolation, response/persistence oracles; historical H3 expectations explicitly qualified. |
| Implementation/repository/API tests | §8 plus §13 repository link; concise authentic unit/fixture/Postman excerpts; local collection JSON exists. Remote JSON remains missing. |
| Unit, integration and full-suite reports | §§9.1–9.3, genuine terminal screenshots, retained full-suite text and XML provenance. No fabricated full-suite screenshot. |
| Postman run report screenshot | §9.4: all six genuine Runner screenshots and actual 90-request/470-assertion result. |
| UAT report | §9.5: all 20 actual-result records, statuses, remaining checks, tester/date and all 19 genuine screenshots. Completion remains partial. |
| Traceability | §10: WF1/WF2/WF3 and R01–R15 mapped to actual Unit, Integration, Postman and UAT identifiers. |
| Defects and conclusion | §§11–12: complete audit register, genuine fixes versus proposed fixes, environment issues, incomplete UAT and 93/120 ambiguity. |
| References | §13: actual project sources, correct GitHub repository and inaccessible-template qualification. |

## Verified results and evidence

- Unit: **113 passed, 602 deselected, 1 warning**, 6.23s, 26 October 2026. Three genuine terminal captures; latest marked-run full raw export/build attribution unavailable.
- Integration: **194 passed, 521 deselected, 1 warning**, 30.52s, 26 October 2026. Three genuine captures; latest marked-run full raw export/build attribution unavailable.
- Complete audit suite: **715 passed, zero failures/errors/skips, 1 warning, 76.25s, exit 0**, 27 October 2026. Retained text/XML/run metadata; all **65 recorded application/test source hashes remain unchanged**. Marked runs overlap the complete suite.
- Postman: **90 requests, 470 assertions passed, zero assertion failures, zero execution errors, one iteration**, 27 October 2026; 10s 697ms. Six original captures of that one run. Machine-readable Runner export unavailable. Collection SHA-256 unchanged: `409cffa7540cd73880d74139f77346cdb47d06a18d9ae8e1b11cf70ef2c44b6d`.
- Current static collection validation: exit 0; 90 requests; 93 JavaScript script blocks compile; all 15 JSON operations, variable/body/URL structure and blank exported secrets checked. **No Postman/Newman runtime rerun.**
- UAT: **1 Pass / 0 Fail / 19 Not Run**. UAT-06 passes the recorded review objective with substituted data; 18 cases are partially verified, and UAT-05 lacks required workflow evidence. Original A was actually three Mathematics courses / 9 credits, revised to two Mathematics courses plus ENGL 1000 / 9 credits; planned two-course / 6-credit oracles are retained separately.
- Prompt 16 visual correction: `UAT-15-rejected-cancelled.png` actually shows semester C cancellation and supports **case UAT-16**. `UAT-16-pending-cancelled.png` shows semester B cancellation with rejection feedback and supports **case UAT-15**. Sheet/report/matrix/audit references and PDF captions corrected; images and case statuses unchanged. File order is not execution chronology.
- All **31 original execution PNGs** are embedded: 3 Unit, 3 Integration, 6 Postman, 19 UAT. Full originals are retained; enlarged excerpts are labelled. Original contrast defects remain disclosed rather than altered.

## PDF and source verification

- [x] Exact output exists: `docs/assignment2/COMP3613_Assignment2_MyAdvisor.pdf`.
- [x] PDF opens without encryption and all pages render successfully.
- [x] **139 pages**, with continuous footer numbers including cover and landscape pages; accurate linked table of contents and bookmarks.
- [x] Every page visually reviewed through rendered contact sheets; full-size pages checked for diagrams, tables, plan cases, result summaries and screenshot detail.
- [x] No blank page, out-of-page text, overlapping layout, missing image or missing included-source reference found in final checks. Original screenshots retain their documented clipping/contrast limits.
- [x] Genuine original Use Case Diagram/wireframe preserved; ERD source retained in [original-erd.mmd](pdf-review/original-erd.mmd).
- [x] All 20 UAT, 23 UT and 20 IT identifiers present. XML/count/status checks reconcile; expected values are separated from observations.
- [x] PDF text scanned for plaintext demo passwords, JWT-like tokens and private-key markers; none found. Original images visually checked for passwords/session tokens; none found. No live `.env`, database or raw cookie value copied into the PDF.
- [x] Local Markdown links and included source/image paths resolve; detailed counts/checks retained in [validation-report.json](pdf-review/validation-report.json).
- [x] Build source/image hashes recorded in [assembly-manifest.json](pdf-review/assembly-manifest.json). Full-page renders are retained locally under ignored `pdf-review/rendered/`.
- [x] Assignment 1 artifacts and working application/test source unchanged by this task. No new runtime results invented; no browser execution performed.

## Repository and commit availability

- [x] Correct intended repository verified read-only: **https://github.com/Camcoon/MyAdvisorWithTests**, public, default branch `main`.
- [x] Rechecked main still points to `864386fe10fa5e61869e07500d84e51ff7e46b9b`, the Prompt 15 snapshot. Its missing JSON/current-evidence findings remain applicable.
- [ ] Latest intended materials committed/published: **not complete**. Nested working repository origin remains `https://github.com/Camcoon/MyAdvisor.git`; do not accidentally publish there. Its existing A2 work is modified/untracked. See [working-tree-status.txt](pdf-review/working-tree-status.txt).
- [ ] Required JSON and current UAT/Postman images/reconciled documentation available on intended public main: **missing/stale** (F02/F03).
- [x] New PDF/checklist/build/validation files and documentation corrections are **local and uncommitted**. New libraries and page-render scratch files are ignored by the A2 `.gitignore`.
- [x] No commit, push, remote change, deployment or history rewrite performed. Publication requires the user's instruction.

## Remaining actions before submission

1. Authorize and review the minimal F01 HTML Student-role fix with regression tests and fresh execution evidence. Passing existing tests does not close self-approval.
2. Obtain an authoritative resolution of the **93 total credits versus 120 category credits** issue (F05/DATA-01). Do not choose a number merely to satisfy tests.
3. Resolve/review F06 contrast, F07 runtime SQLite enforcement, F08 registration errors and F09/F15 security controls; retain explicit dispositions and new retests where changes occur. F10 provenance, F13 assertion depth, F14 cleanup and F16 warning limits remain disclosed; F11 identity/assembly is now partly addressed.
4. Personally execute the remaining UAT conditions in [uat-supplemental-evidence.md](reports/uat-supplemental-evidence.md) using actual new dates/build/browser/URL. Include valid/invalid login, refresh/persistence, queue/feedback reset, logged-in Student 403, Advisor tab fallback and each actor's fresh signed-out URL checks. Preserve earlier evidence and the actual data deviation.
5. Personally check the two course-linked templates for any additional required fields/formatting.
6. After review, explicitly instruct publication of the sanitized JSON, current documents, evidence and updated PDF to **MyAdvisorWithTests**, then verify a clean clone/import. No push is performed here.
7. Regenerate/revalidate the PDF when corrected code, authoritative requirements or completed UAT change the underlying evidence; then submit the reviewed single PDF through the university's required submission channel.

The local PDF is a complete, readable compilation with disclosed gaps. **It is not submission-ready while F01–F05 remain open.**
