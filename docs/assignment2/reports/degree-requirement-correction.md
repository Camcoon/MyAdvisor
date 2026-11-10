# Approved fictional degree correction — 27 October 2026

This record supersedes the earlier **F05 allocation approval pending** statements. The project owner explicitly approved the allocation below in this conversation. It is fictional coursework demonstration data, **not official UWI Computer Science programme requirements**. Historical evidence is retained unchanged.

| Category | Approved required credits | Seeded completed credits | Remaining in this category | Completed percentage |
|---|---:|---:|---:|---:|
| Core Courses | 36 | 3 | 33 | 8% |
| General Education | 18 | 3 | 15 | 17% |
| Electives | 12 | 0 | 12 | 0% |
| Major Requirements | 18 | 0 | 18 | 0% |
| Additional Requirements | 9 | 0 | 9 | 0% |
| **Total** | **93** | **6** | **87 category credits not completed** | |

The overall baseline remains **6 completed / 3 in progress / 84 remaining / 93 required / 6% completed**. Category remaining excludes in-progress credits; overall remaining subtracts them. Consequently category remaining totals 87 while overall remaining is 84. This is the existing defined distinction, not a remaining 93/120 mismatch. Each completed course has one category and its ID is counted once; in-progress courses do not contribute earned category credits.

## Implementation and existing databases

- `app/demo_requirements.py` holds the approved allocation and the known earlier 120-credit allocation.
- `AdvisingService.sync_demo_requirements()` validates the selected demo programme, the 93-credit overall total, categories, and known old/new per-category values **before any mutation**. Custom values, extra categories, and a different overall total require review. Other programmes are not changed.
- New demo seeding and normal startup use the same allocation. No catalogue, prerequisite, completion, in-progress, Student, or plan changes were introduced by this correction. Existing dashboard arithmetic remains unchanged.
- Existing requirement rows are updated in place in one commit; their IDs are retained. The dedicated migration never initializes, reseeds, or deletes a database. It backs up a file-backed SQLite database with SQLite's online backup API before an actual change and verifies the other tables with counts/digests. A repeat application is a no-op. Automated application to PostgreSQL is not provided or claimed.
- The Degree Progress screen explicitly identifies this as fictional coursework data.

From the `Assignment 2` project directory, first stop the application's process if migrating an older database and review the selected database privately. These commands do not print a connection URI or row contents:

```powershell
.\.venv\Scripts\python.exe manage.py degree-requirements
.\.venv\Scripts\python.exe manage.py degree-requirements --apply --report <new-result-file.json>
```

`--apply` requires the approved data, creates a fresh backup under ignored `.local-db-backups/` when changes are necessary, and reports only requirement values and table counts/digests. Never use `manage.py init` against an existing evidence database: the default init command drops tables. For a new disposable test database only, use the existing documented `init --no-drop` setup.

**Observed local database result:** the explicitly selected `Assignment 2/database.db` already contained all five approved values. The [preview](../evidence/degree-requirements-2026-10-27/local-db-before-migration.json) and [apply/no-op record](../evidence/degree-requirements-2026-10-27/local-db-approved-noop.json) both show no changed rows; no migration write or backup was necessary. The file was held by another process, so file-hash reads failed. The [qualification](../evidence/degree-requirements-2026-10-27/local-db-unchanged.json) records byte equality as **unverified**, not passed. No process was stopped and no database reset was performed. No claim is made about another running process or any deployed database.

## Actual automated evidence

Records are kept separately in [degree-requirements-2026-10-27](../evidence/degree-requirements-2026-10-27/). The earlier 735-pass build and 284-pass targeted run are historical baselines, not results of this changed source.

- First new selection: collection error from duplicate test module basenames; retained as `degree-20261028T015715Z-3a5ca51d.*`, exit 2. The integration file was renamed; no assertion was weakened.
- Subsequent selection: **44 passed, one warning**, exit 0; retained as `degree-20261028T015725Z-9c9b9733.*`.
- Final affected selection after adding migration orchestration checks: **46 passed, zero failures/errors/skips, one warning**, exit 0, 1.65s; retained as `degree-20261028T015838Z-c8b8ad82.*`.
- Complete regression: **751 passed, zero failures/errors/skips, one warning**, exit 0, **122.67s**. [Output](../evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.txt), [JUnit XML](../evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.xml), and [command/environment/source metadata](../evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.json) are retained. The 751 nodes comprise **116 marked-unit members, 227 integration members, 408 other members**; these are membership counts in one complete run, not separately executed marked runs. All **74** recorded app/test files were unchanged during execution. This run includes the existing Chromium contrast checks; neither was skipped. The single warning is the retained TestClient/httpx deprecation.

New isolated unit checks use literal independent category/percentage expectations, including duplicate-record non-double-counting. New integration checks exercise fresh demo seeding, real authenticated HTML/JSON progress, completed-prerequisite eligibility, migration across all five plan statuses, unchanged full history, stable requirement IDs, repeat application, custom-data rejection, a real SQLite WAL backup, and backup failure preventing writes. The existing synthetic Core=30 calculation fixtures are intentionally retained; only the seed-specific scenario now explicitly uses the known demo Core=36 starting value.

## Postman revision and required rerun

The [current JSON](../postman/MyAdvisor-Assignment2.postman_collection.json) is revision **2026.10.27-degree93**, SHA-256 `6f1a8d297bb5bc4b510963b7a244b7376d60d96531edcaa59c1840f169cad4d3`.

- Request **19** now checks the literal approved five-category allocation, exact seeded-bob credit totals and percentages, and the expected completed/in-progress course codes.
- Request **20** now checks that COMP 1201 is eligible through the known completed prerequisite COMP 1101. Dynamic IDs and the existing lifecycle remain intact.
- Static validation passes: **90 requests, 93 JavaScript blocks compile, all 15 JSON operations covered**, blank exported credentials. This is not a Runner result.
- The [old JSON](../evidence/degree-requirements-2026-10-27/postman-before-approved-allocation.json), SHA-256 `409cffa7540cd73880d74139f77346cdb47d06a18d9ae8e1b11cf70ef2c44b6d`, is retained. The historical 90-request/470-assertion screenshots apply to it, not the revised collection. The workspace YAML export is also historical; import the revised JSON for the next run.
- Rerun **01–90 in order, one iteration**, on a separate disposable instance with the seeded bob baseline. Record actual new assertion counts, failures/errors, tool version, source/collection hashes and screenshots; retain a machine-readable result if available. Also record the existing supplemental three denied Advisor HTML writes, unchanged plan/queue read-backs, malformed-email registration 422, and valid/duplicate registration checks. Never predict 470 assertions for this revision.

The independent Postman oracles address F13's earlier range-only/discovery-only assertion gap in source. Runtime verification of the new assertions remains pending.

## Required human UAT evidence

- Recapture **case UAT-01 / Degree Progress**, whose original evidence filename is `screenshots/UAT/UAT-02.png`. Use a new dated filename. Capture the five corrected denominators, earned/remaining/percentage values, overall totals, fictional-data notice and recent activity, then refresh and record that values persist. Preserve the earlier 120-category-credit image and its observation.
- Repeat Degree Progress after sign-out/sign-in under UAT-18 and the relevant persistence steps, with separate Student/Advisor profiles.
- Run all corrected-build checks in [correction-retest-guide.md](correction-retest-guide.md), using this approved oracle instead of its historical unresolved-allocation criterion. The complete original 20-case coverage is still required.
- Historical acceptance remains **UAT-06 fully passed; 18 cases partially verified; UAT-05 required workflow unverified**, reported as **1 Pass / 0 Fail / 19 Not Run**. No new manual outcome was supplied or inferred from these tests.

## Disposition

**F05 / DATA-01:** allocation approved, implemented, and covered by new regression checks. The configured category total is now 93 and the observed local database matches. Fresh human Degree Progress acceptance and verification of any deployed database remain pending. **F09 CSRF/trusted-origin protection and F15 production signing-key policy remain open.** F01/F06/F07/F08 human/API retests, F10 historical provenance, F14 cleanup, F16 warning, publication of the revised work, and inaccessible lecturer template details are still disclosed.

Both existing 57-page PDFs and every original screenshot remain preserved. Their 735-build/old-collection references and old publication findings are historical. A final replacement must use the same lecturer order, refreshed source/build and publication facts, genuine new results, working links and a concise limitations appendix. It must be generated and verified without overwriting the reviewed candidate first. Final replacement remains gated by the outstanding evidence and publication checks; no submission-ready declaration is made.
