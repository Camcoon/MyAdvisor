# MyAdvisor unit test report

> **Approved-allocation update ? 27 October 2026:** [Current correction record](degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


**Corrected-build qualification ? 27 October 2026:** the report/results below are historical. [Verified corrections](audit-correction-report.md) record **284 targeted passes and 735 complete-suite passes**, each with 1 warning and no failures/errors/skips; complete-run membership is 113 unit / 214 integration / 408 other, not new separate marked runs. New source differs from the historical screenshots. Postman and manual UAT retesting of this build remains pending; historical UAT stays **1 Pass / 0 Fail / 19 Not Run**, with all original images retained. Follow the [new-build retest guide](correction-retest-guide.md); do not infer new manual results from automation.

**Prompt 15 audit addendum ? 27 October 2026:** an independent **complete-suite** rerun now records **715 passed, 0 failures/errors/skips, 1 warning in 76.25s; exit 0**. Its [text output](../evidence/audit/pytest-output.txt), [JUnit XML](../evidence/audit/pytest-results.xml) and [run metadata/source hashes](../evidence/audit/pytest-run.json) are retained. The XML includes all 113 unit and 194 integration nodes (plus 408 other nodes); this is not a separate marked-unit/integration run or a reconstruction of the older marked outputs. The historical provenance statements below describe those original runs. [Final audit](../final-quality-audit.md) records newly reproduced application defects that the passing suite misses. No application/test source was changed.

Prepared: 26 October 2026; evidence rechecked 27 October 2026. Evidence review only; no tests were rerun to prepare this report.

## Scope and objectives

Verify isolated degree-progress calculations, completed-only prerequisites, semester and selection validation, plan-state rules, advisor decisions and feedback boundaries, cancellation/removal guards, authentication orchestration, role resolution, password hashing and JWT contracts. The [unit plan](../test-plans/unit-test-plan.md) defines UT-01-UT-23 and local requirements R01-R14. Database persistence, HTTP cookie delivery and browser acceptance require separate evidence.

## Actual results and provenance

| Evidence/run | Passed | Failed | Errors | Deselected | Warnings |
|---|---:|---:|---:|---:|---:|
| Latest verified result supplied by the student for this reporting task | 113 | 0 | 0 | 602 | 1 |
| Retained earlier unit output, 26 October 2026 | 113 | 0 | 0 | 408 | 1 |
| Full-suite result supplied by the student, for context | 715 | 0 | 0 | Not applicable | 1 |

The latest unit selection totals 715 collected items (113 + 602). The retained [verbose output](../evidence/unit/pytest-output.txt), [JUnit XML](../evidence/unit/results.xml) and [run record](../evidence/unit/README.md) describe an earlier 521-item collection, completed in 1.98 seconds with exit code 0. JUnit independently records 113 tests, zero failures/errors/skips. Preserve that historical result; it is not the raw output of the latest run. The latest screenshot confirms **6.23 seconds** and the execution command. A complete latest text/JUnit export and numeric exit-code record are **missing**. Full-suite and marked totals overlap; do not add them together.

## Executed tests and UT traceability

The following per-group pass counts come from the retained unit execution and agree with its node IDs/JUnit. They total 112 variants. The retained `tests/test_login_routing.py::test_admin_login_redirects_to_home` is the additional passed UT-20 companion, yielding 113. Latest screenshots show portions of the passed node list and the final total; the complete latest per-node export is missing, so these detailed group counts are attributed to the retained run.

Functions UT-01-UT-19 are in [test_advising.py](../../../tests/unit/test_advising.py); UT-20-UT-23 are in [test_auth.py](../../../tests/unit/test_auth.py). Parameterized node suffixes and every actual result are retained in the verbose output.

| Case | Planned objective | Executed function(s) | Retained variants |
|---|---|---|---:|
| UT-01 | Degree totals and category calculation | `test_UT_01_degree_totals_and_category` | 1 passed |
| UT-02 | Empty academic record and missing program fallback | `test_UT_02_empty_record` | 2 passed |
| UT-03 | Progress limits, zero denominators and duplicate records | `test_UT_03_progress_boundaries` | 4 passed |
| UT-04 | Prerequisites satisfied or absent | `test_UT_04_satisfied_prerequisites` | 4 passed |
| UT-05 | Missing and in-progress prerequisites | `test_UT_05_missing_prerequisites` | 3 passed |
| UT-06 | Tracked or unknown target courses | `test_UT_06_tracked_and_unknown_courses` | 3 passed |
| UT-07 | Valid semester names and trimming | `test_UT_07_semesters` | 10 passed |
| UT-08 | Invalid semester names | `test_UT_08_invalid_semesters` | 7 passed |
| UT-09 | Empty selection | `test_UT_09_empty_selection` | 1 passed |
| UT-10 | Duplicate selected course IDs | `test_UT_10_duplicate_selection` | 2 passed |
| UT-11 | Missing or ineligible selection aborts submission | `test_UT_11_selection_aborts_without_writes` | 4 passed |
| UT-12 | Submission status decision table | `test_UT_12_submission_status_table` | 6 passed |
| UT-13 | Dashboard edit and cancelled-selection rules | `test_UT_13_dashboard_selection_and_edit` | 6 passed |
| UT-14 | Advisor decisions and feedback normalization | `test_UT_14_advisor_decisions` | 6 passed |
| UT-15 | Invalid advisor decision | `test_UT_15_invalid_decision` | 4 passed |
| UT-16 | Feedback length boundary before trimming | `test_UT_16_feedback_raw_length` | 18 passed |
| UT-17 | Review only existing Pending plans | `test_UT_17_review_requires_pending_plan` | 5 passed |
| UT-18 | Cancellation status and ownership matrix | `test_UT_18_cancellation_matrix` | 7 passed |
| UT-19 | Remove course guard matrix | `test_UT_19_remove_course_matrix` | 9 passed |
| UT-20 | Authentication success | `test_UT_20_authentication_success` | 1 passed |
| UT-21 | Authentication failures and short circuit | `test_UT_21_authentication_failure` | 2 passed |
| UT-22 | Cookie token resolution and admin role | `test_UT_22_identity_failures`, `test_UT_22_valid_identity_and_admin_guard` | 5 passed |
| UT-23 | Password hash and JWT utility contracts | `test_UT_23_password_hash_contract`, `test_UT_23_jwt_claims_expiry_and_input_unchanged` | 2 passed |

The requirements matrix in the linked plan now includes report references and manual/API execution dispositions.

## Execution command and environment

The latest start screenshot records this PowerShell setup and command from the repository containing `pyproject.toml`:

```powershell
$base = Join-Path $env:LOCALAPPDATA "MyAdvisor-A2-Pytest"
.\.venv\Scripts\python.exe -m pytest tests -m unit -v --basetemp="$base\unit"
```

The screenshot confirms Windows/win32, the repository `.venv` interpreter, Python **3.14.0**, pytest **9.1.1**, pluggy **1.6.0**, anyio **4.15.1** and pytest-asyncio **1.4.0**, with `pyproject.toml` configuration. It shows **715 collected / 602 deselected / 113 selected**. The final screenshot records **113 passed, 602 deselected, 1 warning in 6.23s** and a returned PowerShell prompt. A numeric exit code is not shown.

For comparison, the retained earlier command was:

```powershell
python -m pytest -m unit -v -p no:cacheprovider --junitxml=docs/assignment2/evidence/unit/results.xml
```

The earlier run started at 22:38:26 UTC-04:00 on 26 October 2026 and recorded FastAPI 0.141.1, SQLModel 0.0.42, PyJWT 2.14.0 and pwdlib 0.3.1; these dependency versions are not shown in the latest screenshots. Its baseline commit `679b9250c13f38a2f97ed4e6d08a325fe48219d3` had local changes and does not identify the latest tested snapshot. Latest build/commit and named tester are **missing**. Screenshot capture/execution date is **26 October 2026**, as confirmed by the student and filenames; the terminal has no independent execution timestamp/time-zone record.

Fixtures use in-memory objects, autospecced repositories and connection guards. Hash/signing checks use real local cryptography. The writable temporary base resolves the earlier Windows temporary-directory issue. The earlier cache-disabled command and latest command are distinct executions.

## Screenshot evidence

All three supplied Unit images were inspected visually. Capture date: **26 October 2026**.

| Evidence | What is visible |
|---|---|
| [231703: start and early tests](../screenshots/Unit/Screenshot%202026-10-26%20231703.png) | `$base` definition, actual command, environment, collection totals, UT-01 through part of UT-08 and retained login companion passing |
| [231742: later tests and warning](../screenshots/Unit/Screenshot%202026-10-26%20231742.png) | Later UT-16 through UT-23 variants passing, warning text |
| [231747: completed summary](../screenshots/Unit/Screenshot%202026-10-26%20231747.png) | Final pass/deselection/warning counts, duration and returned prompt |

![Completed unit run: 113 passed, 602 deselected, 1 warning in 6.23s](../screenshots/Unit/Screenshot%202026-10-26%20231747.png)

The screenshots cover portions of the node list rather than a complete scrollback export. The earlier text/XML remains the complete retained per-variant evidence.

## Issues, warnings and conclusion

Both the latest screenshots and retained log identify `StarletteDeprecationWarning`: using `httpx` with `starlette.testclient` is deprecated; the warning suggests `httpx2`. This is a dependency warning, not a failed assertion. No application defect or unit failure is recorded. Temporary-directory and cache access issues concern execution setup, not failed business assertions.

All 113 unit tests passed in the student's latest verified result; the older machine-readable evidence supports all 23 planned UT groups. The latest summary, command and warning are corroborated by screenshots; complete latest raw-output and build/tester metadata remain missing. Passing these isolated tests does not establish integration or manual acceptance.

## Cross-method reporting reconciliation — 27 October 2026

The latest verified full suite is **715 passed, 0 failures, 0 errors, 1 warning**. It overlaps the unit and integration selections; these totals must not be added. Screenshot readability and provenance were rechecked in the [evidence inventory](evidence-inventory.md). [Workflow traceability](requirements-test-traceability.md) links actual UT/IT IDs, collection request numbers and UAT cases. Postman is now executed: **90 requests, 470 successful assertions, 0 assertion failures, 0 execution errors, 1 iteration**, corroborated by the supplied Runner screenshots. UAT now records **1 Pass / 0 Fail / 19 Not Run**, including 18 partially verified cases and one unverified workflow; see the reconciled UAT report. Tester Cameron Ramesar confirms all 19 UAT captures/workflows were executed on 27 October 2026. No tests or application functionality were changed.

Prompt 14 final reconciliation: existing completed-summary screenshot visually rechecked; verified automated counts above unchanged. No rerun. Full-suite 715-pass result remains user-verified without a retained full-suite screenshot.
