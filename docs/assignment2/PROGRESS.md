# Assignment 2 progress

> **Approved-allocation update ? 27 October 2026:** [Current correction record](reports/degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.

## Latest work ? UAT reporting correction and PDF refresh, 3 November 2026

- Visually inspected all **19 existing UAT screenshots**; confirmed their actual states and preserved the reversed UAT-15/UAT-16 cancellation filename mapping. No screenshots were missing or changed.
- Current historical UAT disposition: **1 Pass / 0 Fail / 18 Executed - Partially Verified / 1 Not Executed - Unverified**. UAT-06 alone is fully verified; UAT-05 remains unverified. No observed failures. The actual initial/revised A selections remain MATH 1300/2200/2250 (9 credits) and MATH 1300/2200/ENGL 1000 (9 credits); all unverified substeps are listed per case.
- The latest corrected-build full pytest result remains **751 passed, 1 warning, no failures/errors/skips**. Historical Postman evidence remains 90 requests / 470 assertions passed; the revised collection and corrected build were not rerun.
- Updated the execution sheet, final UAT report, evidence matrix, supplemental checklist, UAT plan and this progress record. Application code and automated test results were not changed.
- Regenerated the lecturer-aligned 57-page final PDF and visually checked Appendix A status tables. The corrected PDF path and verification details are recorded below after final validation.
- Final PDF: [COMP3613_Assignment2_MyAdvisor_Final.pdf](COMP3613_Assignment2_MyAdvisor_Final.pdf), **57 pages**, SHA-256 `b3854c0f7474a2ba8b67b95718bb8389ac35934d9c72fc529557cbc194f039c0`. Appendix A pages 52–54 were visually checked; the prior 57-page PDF is preserved in `final-review/previous-final-before-restructuring.pdf`, and the original 139-page PDF is unchanged. Verification: [PDF report](final-review/validation-report.json), [page review](final-review/page-review.csv).
- No UAT/Postman rerun, commit or GitHub push was performed. **Application/submission acceptance remains incomplete.**

## Historical status as of 27 October 2026 ? bounded audit corrections

**F01/F07/F08 fixed and regression-tested locally. F06 corrected and automated browser contrast passed; human retest pending.** Application changes are limited to Student-only HTML mutation dependencies, SQLite connection FK enforcement, registration email validation and scoped text/table CSS. Existing Student/Advisor workflows pass the corrected full suite. No existing assertion was weakened.

- Final affected tests: **284 passed, 1 warning, 86.42s**, exit 0; no failures/errors/skips.
- Final complete suite: **735 passed, 1 warning, 58.11s**, exit 0; no failures/errors/skips. This is 715 existing + 20 new variants. XML membership: 113 unit / 214 integration / 408 other; no new marked selections claimed.
- Unique writable temporary directories and disposable fixture databases used. Genuine output/XML/environment and 70 source hashes retained in [correction evidence](evidence/corrections-2026-10-27/README.md). Pre-fix negative results and browser sandbox timeouts remain separate history.
- F05: owner confirms fictional coursework prototype; a non-overlapping 93-credit allocation was proposed in chat and is **pending approval**. Seed, application defaults, tests, database and historical values remain unchanged. No official university curriculum claim.
- Historical Postman 90/470 and UAT **1 Pass / 0 Fail / 19 Not Run** remain unchanged. No corrected-build manual/Runner execution; all 19 UAT images preserved. [Exact retest instructions](reports/correction-retest-guide.md) map every original case's missing checks and supplemental F01/F06/F08 checks.
- F09 CSRF/F15 signing-key policy reviewed and left open with deployment-specific decisions/verification required; no live secrets/settings changed.
- Correct public main rechecked at the audited SHA; F02/F03 remain open. Wrong local origin, existing branch and dirty work preserved. [Publication plan](reports/repository-publication-plan.md) is review-only; no commit, push, remote change or deletion.
- [Correction report](reports/audit-correction-report.md), audit and checklist updated. Existing 139-page PDF unchanged; **no revised PDF generated**. **Not ready for submission-ready PDF/sign-off.** Earlier entries below are historical.

---

## Earlier progress records

**Current status ? 27 October 2026:** Prompt 15 independent quality audit complete. Material findings remain; **not ready for final PDF generation or submission sign-off**. See [final audit](final-quality-audit.md). Earlier entries are historical.

## Verified pytest result — 26 October 2026

The student reports that the pytest environment problem is resolved. A dedicated
writable temporary directory named `MyAdvisor-A2-Pytest` was configured, and the
full `tests` suite was run with verbose output and `--basetemp="$base\all"`.

**Actual reported result: 715 passed, 1 warning in 56.83s.** All automated tests
passed. There were no remaining pytest failures or setup errors in this run.
This records the student's verified execution; the suite was not rerun during
the Postman collection creation stage. The warning's cause is not supplied in
this latest result.

## Prompt 11 — Postman collection creation

**Creation complete; Postman execution pending.**

- [Collection v2.1 JSON](postman/MyAdvisor-Assignment2.postman_collection.json):
  86 sequential requests across authentication, Student and Advisor roles,
  progress/catalogue, plan submission and validation, ownership, advisor review,
  resubmission, cancellation, retained history and logout.
- [Local import and run instructions](postman/README.md), including credentials,
  dynamic variables, prerequisites, expected data changes and evidence capture.
- Requests reuse implemented routes and cookie authentication. No application
  functionality was rewritten.
- Static artifact checks are separate from runtime testing. **No Postman pass
  result is claimed.** The student must run the collection and report results.

Creation-stage static checks completed: JSON parsing; JavaScript syntax
compilation for all 88 scripts; all request template variables declared;
redirect/cookie settings and blank password defaults checked; comparison with
router declarations confirmed coverage of all 15 implemented JSON API
operations. `git diff --check` also passed for tracked changes. No HTTP requests
were made, and these checks do not execute the Postman assertions.

Work stops after collection creation. No subsequent assignment stage is started.

## Postman collection review and finalization — 26 October 2026

**Ready for manual execution; Postman/Newman results pending.** This continues
Prompt 11 without repeating Prompts 1–11 or starting UAT.

- Reviewed the existing collection and Postman README, API reference,
  FastAPI routes, request/response schemas, cookie authentication dependencies,
  service validation/transition rules, and existing Student/Advisor API and
  integration coverage. The existing source was
  `docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json`;
  `postman/MyAdvisor-A2.postman_collection.json` was absent. The existing path
  remains the single maintained collection.
- Finalized **90 ordered requests** covering Track Degree Progress, Plan Semester
  Course Selections, and Review and Approve Course Plans. All 15 implemented JSON
  API operations have matching methods and paths; supporting health/login/
  registration/logout requests also match real routes.
- Corrected the prerequisite negative case to select a course whose catalogue
  reason explicitly identifies missing prerequisites. Previously any ineligible
  course, including an already-completed course, could satisfy that fixture.
- Strengthened validation assertions to identify the expected field and Pydantic
  error type, exact 401/403 messages, domain error structures/business messages,
  nested response fields/types, authenticated Student ownership and Advisor
  attribution, and exact feedback persistence. Verified coverage of positive
  authentication, progress, catalogue, submission/list/detail, queue, approval,
  rejection, changes requested, status/feedback, and the requested negative cases.
- Added four API read-back checkpoints: invalid submissions preserve history;
  ownership/role denials preserve the Pending plan; invalid reviews leave the plan
  Pending and unassigned; forbidden edits/reviews preserve approval and feedback.
- Retained dynamically captured plan/course/account IDs and three explicit
  role-specific cookies. Cookie jars and redirects are disabled per request.
  Collection values now also control request substitutions, avoiding environment
  shadowing. Unexpected script errors stop the remaining sequence. Exported
  passwords, JWTs and generated IDs remain blank; the independent Student's
  password is generated during the run and cleared on successful completion.
- Replaced vague database preparation with exact PowerShell instructions that
  use a unique temporary SQLite database, process-local configuration/signing
  key, `init --no-drop`, and a dedicated localhost server on port 5001. These
  instructions were documented, **not executed**. Successful runs retain one
  isolation account and two Cancelled plans in the disposable database only.
  No original/production database was reset or contacted.
- Updated [Postman README](postman/README.md) with import/configuration, all 90
  Runner requests in order, one iteration, no environment/data file, expected
  outcomes, failure handling, retained data, credential handling and limitations.
  No environment template is needed: all configuration inputs are collection
  variables, with blank password defaults.
- Added [static validator](postman/validate_collection.cjs). Actual completed
  checks: JSON parsing and structural checks; **93 JavaScript scripts compile**;
  all request variables declared; normal raw JSON bodies parse; blank exported
  credentials/IDs, cookie/redirect flags, sequential numbering, method/path
  matching and coverage of **all 15 JSON API operations**. These checks do not
  download/validate an official JSON Schema or execute Postman assertions.
- Local inventory: Postman/Newman not found on PATH; usual Postman install paths
  and npm Newman shim absent; no running Postman process found; Node available,
  Newman module unavailable. The global npm listing reported the per-user npm
  directory missing. A portable install elsewhere or web Postman remains possible.
  **No Postman/Newman execution or passing result is claimed.**

The verified pytest totals remain: **113 unit tests passed**, **194 integration
tests passed**, **715 full-suite tests passed**, each reported run with one warning.
The Windows temporary-directory issue remains resolved using `--basetemp`.
No pytest tests/reports were regenerated, no application functionality was
changed, and no UAT was performed. Outstanding work is the student's manual
Postman Runner execution and recording its actual results.

## Final manual UAT materials — 26 October 2026

**Preparation complete; browser execution and acceptance pending.**

- Reviewed the existing UAT plan against the original Assignment 1 wireframe (visually), current Student/Advisor HTML templates and navigation/login, workflow routes, auth/error handling, seed data, service/repository transitions, and project documentation.
- Created [UAT execution sheet and detailed browser walkthrough](reports/uat-execution.md): all existing UAT-01–17 plus separate Student/Advisor login and demonstrable role-restriction cases UAT-18–20. Physical order follows the practical execution sequence. Every case has workflow/actor/wireframe mapping, preconditions/data, exact browser steps, expected and actual result fields, status, tester, execution date, screenshot reference and defect ID.
- All **20 cases are Not Run: 0 Pass / 0 Fail / 20 Not Run**. Actual results say Not executed; tester/dates and defect IDs are unfilled. Screenshot names are planned references only. No screenshots or successful outcomes were fabricated.
- Documented exact human-run PowerShell setup for a new temporary SQLite database, process-local configuration/signing key, `init --no-drop`, and localhost port 5002; supported seeded `bob` Student and `admin` Advisor accounts; semester A/B/C choices; profile/cookie isolation (cookies can collide across localhost ports); state dependencies, feedback capture before resubmission, blockers, clean retries and evidence retention. These setup commands were documented, not run.
- Updated [UAT plan](test-plans/uat-test-plan.md) to version 1.1 with the execution companion and review qualifications. Recorded the 120 category-credit versus 93 degree-credit source inconsistency for acceptance review. Browser role scope distinguishes Student `/admin` denial, Advisor invalid-tab fallback, and signed-out 401 behavior; no claim of complete browser security verification is made.
- Validation was static documentation/source checking only: case/field completeness, all 20 Not Run statuses, execution order, local links, and CLI flag/route/label comparison. No HTTP workflow, database preparation, pytest rerun, Postman/Newman run or manual UAT was performed. No application files were changed in this stage.

Student-reported verified automated totals remain **113 unit passed, 194 integration passed, 715 full-suite passed**. Postman is prepared with execution results pending. Next authorized activity is the student's manual browser UAT using this sheet and recording real observations/evidence. Work stops here after the execution materials; no acceptance, report export or later stage is claimed complete.

## Test reporting prepared and checked - 26 October 2026

Prepared [unit report](reports/unit-test-report.md), [integration report](reports/integration-test-report.md), [Postman report](reports/postman-test-report.md) and [final UAT report](reports/uat-final-report.md) from the plans, saved logs/JUnit, current test functions, collection and saved UAT execution sheet. Updated the synchronized requirements matrices in both automated test plans with UAT/Postman mappings, report links and actual evidence dispositions; documented R15's separate API-contract evidence.

- Latest student-verified counts: **113 unit passed, 602 deselected, 1 warning; 194 integration passed, 521 deselected, 1 warning; 715 full-suite passed, 1 warning**. Older retained unit evidence (113 passed, 408 deselected) and Student-only integration evidence (59 passed) remain historical and are not mislabelled as latest exports.
- Inspected all **six screenshots** supplied in `screenshots/Unit/` and `screenshots/Integration/`, captured **26 October 2026**. They confirm unit **6.23s** and integration **30.52s**, actual `.venv` marker commands with `--basetemp`, Python 3.14.0/pytest 9.1.1 and the Starlette TestClient/httpx deprecation. Reports link all six and embed the completed summaries. Latest complete raw exports, named tester, tested commit and numeric exit codes remain missing. Historical logs remain attributed to their own runs.
- Postman collection format v2.1.0 has **90 planned requests**. No actual Runner/Newman export or screenshot was found, including in the supplied screenshots directory; runtime request/assertion pass/fail counts and execution date remain **unknown**, not zero failures.
- The available UAT execution sheet remains **0 Pass / 0 Fail / 20 Not Run**, with no completed observations, testers, execution dates or screenshots. The student's statement that manual results are prepared does not supply those missing observations. Acceptance remains pending, including review of the 120 category-credit versus 93 degree-credit concern. No observed UAT defect/retest is invented.
- Reporting checks reconcile UT counts with XML/logs, IT marker mappings with source, all 20 UAT statuses with the sheet, collection request inventory with JSON, both requirements matrices and local report links. No pytest, Postman or browser workflow was executed for this reporting task, and no application files were changed.

**Reporting task stops here.** Evidence gaps remain explicitly open; no overall acceptance, deployment, PDF export or later assignment stage is claimed complete.

## Prompt 14 — Evidence-based Test Reporting reconciliation, 27 October 2026

Updated [unit](reports/unit-test-report.md), [integration](reports/integration-test-report.md), [Postman](reports/postman-test-report.md), [final UAT](reports/uat-final-report.md), and all 20 rows of the [execution sheet](reports/uat-execution.md). Added [evidence inventory](reports/evidence-inventory.md) and [WF1–WF3 traceability](reports/requirements-test-traceability.md); synchronized current test-plan dispositions.

- Verified latest counts remain **113 unit passed / 602 deselected / 1 warning; 194 integration passed / 521 deselected / 1 warning; full suite 715 passed / 0 failures / 0 errors / 1 warning**. These runs overlap. Older 113-unit/408-deselected and 59-Student-integration exports remain historical.
- Visually inspected **17 existing PNGs**: 3 Unit, 3 Integration, 6 Postman (including the additional summary view), 5 UAT. No placeholder is counted. Postman scroll captures cover requests 01–90, some edge rows partly clipped; capture headers show **470 assertions, 0 errors, 1 iteration, 10s 697ms**. User verifies **470 passed / 0 assertion failures / 0 execution errors**, disposable **http://127.0.0.1:5001**, captured 27 October 2026. No machine-readable Runner export found; JSON/YAML files define the collection.
- User confirms browser execution occurred. Seven cases have partial screenshot observations; no complete case result is established. **0 Pass / 0 Fail / 20 Not Run**, with Not Run explicitly meaning complete result unverified, including partial records. Preserved original IDs/expectations. Three Mathematics courses/9 credits differ from planned two-course data; substitution remains unconfirmed. Tester/per-case dates and remaining observations are requested and listed precisely in the UAT report.
- Acceptance remains pending. DATA-01 (120 category credits versus degree 93) is visible in the degree capture; Advisor table contrast requires browser confirmation; no confirmed full-case failure or manual fix/retest is invented. Latest complete pytest exports/full-suite screenshot, named testers and tested build are not retained.
- Work was performed in the nested `Assignment 2` working repository containing the supplied evidence. Its origin is `Camcoon/MyAdvisor`; the separate upload checkout points to `Camcoon/MyAdvisorWithTests` and contains six duplicate automated captures but lacks the current UAT/Postman captures. No remote, application code or test was changed; no upload, rerun or final PDF was performed.

Test Reporting is reconciled as far as the available records support. **Not ready for final quality-audit sign-off** until missing UAT outcomes, test-data variation and acceptance concerns are resolved. Stop at this stage.

### Tester-review checkpoint (latest instruction)

Prompt 14 is **not finalized**. Added [screenshot mapping and proposed 20-case review table](reports/uat-evidence-review.md): 7 Partially Verified, 13 unverified. The execution sheet/report are provisional evidence drafts, not confirmed manual results. Tester name/date placeholders remain unknown. Mathematics substitution is not classified as failure; positive submission/queue states are visible but refresh and remaining checks require confirmation. Await the user?s observations before finalizing UAT results or acceptance.

Documentation validation at this provisional checkpoint: all **12** report/plan/progress Markdown files parsed and rendered with table support; **479** local links/images resolved to existing targets; all 20 UAT IDs and execution fields checked; original UAT-01?17 expectations preserved verbatim; UT-01?23 and IT-01?20 verified against source; collection contains exactly requests 01?90; retained JUnit has 113 cases with no failures/errors. All eight report documents were checked for plaintext credential/token patterns with none found. Original plans contain documented local demo credentials, not copied into reports. Six upload-checkout automated screenshots are byte-identical duplicates. No tests were rerun.

## Prompt 14 completed reconciliation ? latest authoritative record

Tester **Cameron Ramesar** explicitly confirms personally executing all 19 UAT screenshot captures and associated workflows on **October 27, 2026**. All 19 files visually inspected and mapped; no filename-only or seeded-name inference. Actual initial A MATH 1300/2200/2250 (9 credits), revised A MATH 1300/2200/ENGL 1000 (9 credits); original plan expectations retained.

**1 Pass / 0 Fail / 19 Not Run**: UAT-06 review objective passes with documented substituted data; 18 cases partially verified, UAT-05 required Pending/relogin workflow unverified. Successful request-changes, revision, approval, rejection, removal, cancellation and new-plan outcomes are recorded individually, with remaining substeps explicit. Signed-out 401/login does not establish Student 403 or Advisor fallback. DATA-01 degree/category mismatch and UI-01 Advisor table contrast remain open.

Updated five requested reports, evidence matrix/inventory and workflow/plan traceability. Automated totals unchanged: 113 passed/602 deselected/1 warning unit; 194 passed/521 deselected/1 warning integration; 715 passed/1 warning full suite; Postman 90 requests, 470 assertions passed, zero assertion failures/errors, one iteration. Existing summary screenshots corroborate marked pytest and Postman runs; full suite is user-verified.

Ready for **Prompt 15 ? Final Quality Audit with open items**, not unconditional acceptance. No application code edits, test reruns, PDF generation or remote publication. Environment/build metadata and matrix-listed manual substeps remain unconfirmed. Work stops after Prompt 14.

### Prompt 14 tester clarification - 27 October 2026

Recorded the tester's explicit limits: logged-in Student /admin 403 and Advisor restricted-tab fallback are unverified; the screenshots do not establish every refresh. Retained all verified decision/feedback, revised queue, removal, cancellation and replacement-plan outcomes. Totals unchanged: **1 Pass / 0 Fail / 19 Not Run**, including 18 partially verified cases and UAT-05 without its required workflow evidence. Added [supplemental evidence checklist](reports/uat-supplemental-evidence.md) listing exactly which entries could change and all remaining case-specific conditions. Historical Cancelled Messages entries in UAT-17 are permitted, not a new acceptance requirement. No new evidence file is fabricated, application code changed, test run executed or acceptance granted. Prompt 15 remains ready to begin with the documented open items.

## Prompt 15 ? independent final quality audit, 27 October 2026

[Final quality audit](final-quality-audit.md) completed against the [Assignment 2 brief supplied during this review](official-assignment-brief.md): **Implementation 25%, Test Plans 25%, Test Implementation 25%, Test Reporting 25%**. No fabricated grade and no Assignment 1 rubric substituted. The two Google template links could not be retrieved; their contents remain unverified.

- **Independent full pytest rerun:** **715 passed, 0 failures/errors/skips, 1 warning in 76.25s; exit 0**. Unique safe `--basetemp`, cache disabled and separate unused bootstrap DB configuration; all test databases disposable. [Text output](evidence/audit/pytest-output.txt), [JUnit](evidence/audit/pytest-results.xml), [metadata/source hashes](evidence/audit/pytest-run.json). Contains 113 unit, 194 integration and 408 other nodes; no separate marked reruns are claimed. Existing 113/194 screenshots and previous 715/56.83s result remain their own historical executions. TestClient/httpx deprecation remains disclosed.
- **High authorization defect reproduced:** Advisor JSON submission denied 403, HTML submission allowed 303, Advisor-owned plan persisted, same Advisor approval accepted 200/Approved. [Isolated reproduction](evidence/audit/authorization-reproduction.json). No functional fix applied; recommend existing StudentDep on Student HTML mutation actions plus real-auth no-write regression tests.
- **Other reproduced defects:** actual disposable application SQLite engine leaves foreign keys disabled and accepts an orphan plan/course link; malformed registration email returns generic HTTP 500 without writing. [SQLite](evidence/audit/sqlite-integrity-reproduction.json), [registration](evidence/audit/registration-reproduction.json). No existing database was opened/reset by those probes.
- **Degree discrepancy:** verified source and display 93 overall / 120 category credits; single course category, no overlap/allocation rule. Classified **Unresolved requirements issue**. Original wireframe's illustrative 120 does not establish corrected requirements. No degree values altered. Advisor table contrast and Approved explanatory-text contrast are visually verified and remain open.
- **UAT remains 1 Pass / 0 Fail / 19 Not Run**, comprising 18 partially verified cases and UAT-05 without required workflow evidence. All 19 original UAT images reviewed; tester/date attribution and the actual three-course Mathematics deviation retained. 401/login captures do not establish logged-in Student 403. No browser UAT rerun or status upgrade.
- **Postman existing result unchanged:** 90 requests, 470 assertions passed, zero assertion failures/errors, one iteration. All six captures visually rechecked. Static validator rerun: exit 0, 90 requests, 93 scripts compile, 15 JSON operations covered. No Postman/Newman runtime rerun; JSON definition unchanged.
- **GitHub checked read-only:** public main commit `864386fe10fa5e61869e07500d84e51ff7e46b9b`; complete 430-entry tree. All 67 published top-level app/test files match local source (line-ending normalization allowed). Required Postman JSON, all UAT images, all Runner images and latest evidence reconciliation are absent/stale remotely. [Snapshot](evidence/audit/github-snapshot.json), [comparison](evidence/audit/local-remote-comparison.json). Historical screenshots still lack tested-build attestation.
- **Security:** no private-key/token/credential-URL match or tracked live `.env`/database found in scoped public-tree/text/image review; exported password/token variables blank. Public demo credentials/example key are development defaults; production secret use is unverified. HTML role gap, production-cookie CSRF protection and weak-default fallback remain findings.
- **Low-risk documentation corrections only:** actual clone target/top-level execution root and CLI instructions, Postman README recorded runtime status, historical H3/current-status wording, UAT-06 inventory/matrix disposition, cancellation/logout request mappings, and an explicit contrast/audit qualification in the historical A1 report. Original planned inputs/expected outcomes and test/collection scripts retained.
- **Final documentation checks:** 24 Markdown files rendered with table support; 679 local references resolve; all 31 execution PNGs decode; 20 unique UAT cases retain 1/0/19 dispositions. Application/test source hashes and collection hash unchanged after documentation edits. [Validation record](evidence/audit/documentation-checks.json) describes that snapshot; this final link adds one further local reference.

Material next steps: authorize minimal functional corrections; resolve degree requirements; personally execute remaining UAT checks with new dated evidence; publish the reviewed sanitized JSON/docs/images when authorized; confirm the real submission ID and then assemble the single A2 PDF. The existing Assignment 1 PDF does not satisfy A2. **No application/test source change, commit, push, history change, deployment or final PDF generation. Stop after this audit.**

## Prompt 16 — single-PDF compilation and submission verification, 27 October 2026

Created [COMP3613_Assignment2_MyAdvisor.pdf](COMP3613_Assignment2_MyAdvisor.pdf), **139 pages**, and the [final submission checklist](final-submission-checklist.md). Compilation is complete; **submission readiness remains blocked** by open High findings F01–F05. No Critical finding is verified. No numerical grade or unconditional acceptance is assigned.

- Verified Cameron Ramesar's real submission identity from the explicit original student statement in `docs/transcripts/current-report-export.md`, corroborated by the original Assignment 1 PDF cover. Used that ID on the new cover; the seeded eight-digit screenshot ID is not identity evidence. This closes the identity-recovery portion of F11; local PDF assembly is also now addressed. Original A1 artifacts remain unchanged.
- Included the cover, linked accurate contents, project description, genuine original Use Case Diagram, vector rendering of the authentic seven-entity ERD with exact cardinality/relationship table, original wireframe and readable panel enlargements, all 20 UAT specifications, all 23 UT and 20 IT specifications, implementation/environment/fixture evidence, current reports, WF1–WF3/R01–R15 traceability, complete audit limitations and references. Historical plan status/H3 text is distinguished from current execution; inputs and expected outcomes are preserved.
- Embedded all **31 genuine execution screenshots**: three Unit, three Integration, six Postman and nineteen UAT. Original full images are retained with labelled enlarged excerpts as needed. Full-suite output is genuine labelled text, not a fabricated terminal screenshot. Existing UI contrast and source screenshot clipping remain disclosed.
- **Evidence mapping correction found during visual review:** `UAT-15-rejected-cancelled.png` actually shows semester 3 Cancelled and supports case UAT-16; `UAT-16-pending-cancelled.png` shows semester 2 Cancelled with rejection feedback and supports case UAT-15. Corrected references in execution/final/matrix/audit documents and PDF captions. Inventory hashes remain bound to original files. No image renamed/modified, result upgraded or chronology inferred.
- Verified results retained: **113 unit passed / 602 deselected / 1 warning; 194 integration passed / 521 deselected / 1 warning; complete audit suite 715 passed / zero failures/errors/skips / 1 warning / 76.25s / exit 0**. Audit XML contains 715 cases; all 65 recorded app/test source hashes remain unchanged. No pytest runtime rerun was needed for documentation assembly.
- Postman remains **90 requests / 470 assertions passed / zero assertion failures or execution errors / one iteration**, executed 27 October 2026. Re-ran the existing static validator successfully: 90 requests, 93 scripts compile, all 15 JSON operations and blank exported secrets checked. Collection SHA-256 unchanged. No Postman/Newman runtime execution was performed in Prompt 16.
- UAT remains **1 Pass / 0 Fail / 19 Not Run**, including 18 partial cases and UAT-05 without its required workflow evidence. UAT-06's review-objective Pass, actual three-Mathematics-course/9-credit selection, revised Mathematics/ENGL selection, remaining substeps and tester/date attribution are preserved. No expected outcome substitutes for an observation; no browser rerun occurred.
- Opened the PDF, rendered every page and reviewed all page layouts plus full-size diagram/table/screenshot detail. Continuous footer page numbers, TOC destinations, text bounds, image availability, case IDs, totals, local references and scoped secret patterns checked. Retained [assembly/source manifest](pdf-review/assembly-manifest.json), [PDF validation report](pdf-review/validation-report.json), [working-tree status](pdf-review/working-tree-status.txt) and reproducible documentation-only build/validation scripts. Large dependency/render scratch folders are locally ignored.
- Rechecked the correct public repository `Camcoon/MyAdvisorWithTests` read-only; main remains `864386fe10fa5e61869e07500d84e51ff7e46b9b`. Required JSON and current UAT/Postman evidence/docs remain absent/stale there. Nested local origin is still `Camcoon/MyAdvisor`; all existing A2 modifications and new submission artifacts are uncommitted. Both linked course templates remain inaccessible; personal template verification remains necessary.

Remaining actions: authorize/review functional corrections and fresh affected tests, resolve 93-versus-120 credit requirements, personally execute the exact missing UAT conditions with actual new dates/build/environment, check course templates, then explicitly authorize publication to the correct repository and regenerate this PDF if evidence changes. **No working application/test source modification, original artifact removal, commit, push, remote/history change or deployment. PDF/checklist generation stops here; the submission is NOT ready while the High findings remain open.**
