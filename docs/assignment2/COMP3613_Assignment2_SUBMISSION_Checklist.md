# COMP 3613 Assignment 2 — Submission Checklist

**Deliverable:** [COMP3613_Assignment2_SUBMISSION_corrected.pdf](COMP3613_Assignment2_SUBMISSION_corrected.pdf)
**Student:** Cameron Ramesar — 816044668
**Document date:** 4 November 2026
**PDF:** 58 pages · 6,487,090 bytes · SHA-256 `5920206aeaf60960c394a47f03354edf460d6be3f5bd9aafc58b0aa7e5c91df9`
**Superseded backup:** `COMP3613_Assignment2_SUBMISSION.pdf` (68 pages, SHA-256 `ad869fbc…`), preserved unmodified. The only difference is the §6.1 formatting correction and the UAT-20 figure crop; content, evidence, links and results are unchanged.

## Status summary

| Dimension | Status |
|---|---|
| Required PDF content | **Included** — every lecturer-required section, in the lecturer's order |
| Repository publication | **Verified** — commit `847e39a9cc6340e51bcc05c9864f75f8457021c1`; required paths, 55 UAT captures and the 90-request degree93 JSON present |
| Testing limitations | **Disclosed** — Appendix A, and in the external checklist below |
| Academic submission | **Ready** |
| Production deployment readiness | **Not claimed** |

## Lecturer deliverables — actual page numbers

| # | Lecturer deliverable | Pages | Figures |
|---|---|---:|---|
| 1 | Name & ID | 1 | — |
| 2 | Project Description | 3–4 | — |
| 3 | Use Case Diagram | 5 | 3.1 |
| 4 | Entity Relationship Diagram | 6–8 | 4.1–4.2 |
| 5 | Application Wireframe | 9–13 | 5.1–5.4 |
| 6 | Test Plans (6.1 UAT, 6.2 Unit, 6.3 Integration) | 14–30 | — |
| 7 | Implementation (7.1 repo, 7.2 unit, 7.3 integration, 7.4 Postman JSON) | 31–33 | — |
| 8 | Reports (8.1 Unit, 8.2 Integration, 8.2.1 full regression, 8.3 Postman) | 34–45 | 8.1–8.9 |
| — | 9. UAT Execution Summary | 46–56 | 9.1–9.8 |
| — | Appendix A — Testing Limitations and Future Improvements | 57 | — |
| — | Appendix B — Submission Checklist | 58 | — |

Contents page: p2. Page numbering starts at the cover (unnumbered) and runs "Page X of 58" on pp. 2–58. Section 6.1 spans pp. 14–23 (UAT-01–UAT-20), 6.2 pp. 23–26 and 6.3 pp. 27–30.

## Lecturer link and evidence checks

| Check | Result |
|---|---|
| Repository link (Sections 1 and 7.1) | `https://github.com/Camcoon/MyAdvisorWithTests` — HTTP 200 |
| Published Postman JSON (Section 7.4) | `.../docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json` — HTTP 200 |
| Five linked test files (Sections 7.2–7.3) | HTTP 200 each |
| Postman JSON path and 90-request collection | Stated in §7.4 with a clickable repository link and directory + filename, no split path cell |
| Diagrams legible and embedded | 24 figures: 3.1, 4.1–4.2, 5.1–5.4, 8.1–8.9, 9.1–9.8 |
| Internal navigation | 22 outline bookmarks; printed TOC page numbers match actual pages; 22 internal TOC links |
| Section 6.1 rendering | No raw Markdown remains: 0 pipe-table lines, 0 stray bold markers, 0 stray backticks in the extracted text (the only `**` is Python unpacking inside a §7.2 code sample) |
| UAT-20 screenshot | Figure 9.8 is a cropped detail of `UAT-20-student-403.png`; only the empty dark background is removed, the source file is unchanged |
| Secrets | No password constants, token values, private keys or database URLs in text or metadata |

## Test results reported in the PDF

| Result | Value | Provenance |
|---|---|---|
| Unit tests | 113 passed, 602 deselected, 1 warning, 6.23 s | Historical marked run, 26 October 2026 |
| Integration tests | 194 passed, 521 deselected, 1 warning, 30.52 s | Historical marked run, 26 October 2026 |
| Full regression | 751 passed, 1 warning, 0 failed/errors/skipped, 122.67 s, exit 0 | Latest verified complete run |
| Postman | 90 requests, 470 assertions, 0 failures, 0 errors, 1 iteration, 10 s 697 ms | Historical run, 27 October 2026, earlier collection revision |
| UAT | **8 PASS / 12 EXECUTED — PARTIALLY VERIFIED / 0 FAIL / 0 NOT EXECUTED** (20 cases, 55 screenshots) | Latest manual execution |

PASS: UAT-04, 05, 06, 10, 14, 15, 16, 17. Partially verified: UAT-01, 02, 03, 07, 08, 09, 11, 12, 13, 18, 19, 20 — genuine principal-workflow evidence, with the listed supplementary checks not captured or not independently proven. **The partial cases are not failures.**

## Disclosed limitations

- 12 UAT cases are classified partially verified; four before/after pairs are byte-identical (UAT-01, UAT-18, UAT-19, UAT-20) and therefore do not independently prove refresh persistence or separate signed-out role checks.
- The 90-request / 470-assertion Runner result belongs to the earlier exported collection; the published degree93 revision passed static validation but was not rerun in Postman.
- Authenticated form writes have no explicit CSRF token or Origin check; production cookie uses `SameSite=None`; logout remains a GET.
- Production signing key fallback to the public example key was not independently verified.
- Automated tests use isolated SQLite; PostgreSQL, concurrency, load and deployed cookie behaviour were not exercised.
- One Starlette/httpx deprecation warning appears in the unit and integration runs; all selected assertions passed.

## Preservation and integrity

- Earlier PDFs were not modified: `COMP3613_Assignment2_MyAdvisor.pdf` (11,916,121 bytes) and `COMP3613_Assignment2_MyAdvisor_Final.pdf` (15,707,748 bytes) retain their 4 November 2026 22:49 timestamps. The previous 68-page submission PDF is retained as the backup.
- No application code, test, UAT or Postman result was rerun or fabricated for this document; original screenshots were reused unmodified.
- The final PDF was built by `build_final_submission.py` from existing evidence. The PDFs, build scripts, verification scripts and JSON records are committed under `docs/assignment2/`.

Verification of repository publication: `final_submission_verification.json` (`"verified": true`). UAT source: `reports/uat-execution.md` and `final-review/uat_extract.json`.
