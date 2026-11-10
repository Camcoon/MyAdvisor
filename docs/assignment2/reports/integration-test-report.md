# MyAdvisor integration test report

> **Approved-allocation update ? 27 October 2026:** [Current correction record](degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


**Corrected-build qualification ? 27 October 2026:** the report/results below are historical. [Verified corrections](audit-correction-report.md) record **284 targeted passes and 735 complete-suite passes**, each with 1 warning and no failures/errors/skips; complete-run membership is 113 unit / 214 integration / 408 other, not new separate marked runs. New source differs from the historical screenshots. Postman and manual UAT retesting of this build remains pending; historical UAT stays **1 Pass / 0 Fail / 19 Not Run**, with all original images retained. Follow the [new-build retest guide](correction-retest-guide.md); do not infer new manual results from automation.

**Prompt 15 audit addendum ? 27 October 2026:** an independent **complete-suite** rerun now records **715 passed, 0 failures/errors/skips, 1 warning in 76.25s; exit 0**. Its [text output](../evidence/audit/pytest-output.txt), [JUnit XML](../evidence/audit/pytest-results.xml) and [run metadata/source hashes](../evidence/audit/pytest-run.json) are retained. The XML includes all 113 unit and 194 integration nodes (plus 408 other nodes); this is not a separate marked-unit/integration run or a reconstruction of the older marked outputs. The historical provenance statements below describe those original runs. [Final audit](../final-quality-audit.md) records newly reproduced application defects that the passing suite misses. No application/test source was changed.

Prepared: 26 October 2026; evidence rechecked 27 October 2026. Evidence review only; no tests were rerun to prepare this report.

## Scope, objectives and components tested together

The [integration plan](../test-plans/integration-test-plan.md) covers IT-01-IT-20: real login and signed-cookie authentication; Student degree progress and course selection; submission and committed plan/course links; Advisor queue, approval, rejection and requests for changes; Student feedback, same-ID resubmission, cancellation and replacement; ownership and role restrictions; invalid requests; database constraints and rollback.

HTTP cases join FastAPI TestClient, routing/dependencies, cookie/JWT and current roles, request parsing, services, repositories, SQLModel and isolated SQLite. IT-19/20 exercise real database constraints and transaction rollback directly. Startup/demo seeding is isolated; no production/PostgreSQL, concurrency, or manual-browser acceptance result is claimed.

## Actual counts and evidence provenance

| Evidence/run | Passed | Failed | Errors | Deselected | Warnings |
|---|---:|---:|---:|---:|---:|
| Latest marked integration run verified by the student | 194 | 0 | 0 | 521 | 1 |
| Retained Student-only integration run, 26 October 2026 | 59 | 0 | 0 | Not reported | 1 |
| Latest full suite verified by the student, for context | 715 | 0 | 0 | Not applicable | 1 |

The latest integration selection totals 715 items (194 + 521). The latest final screenshot confirms **30.52 seconds** and the actual command. Its complete raw verbose/JUnit export and numeric exit-code record are **missing**. The [retained Student execution record](../evidence/student-integration.md) and [verbose output](../evidence/student-integration-pytest.txt) establish 59 passed in 4.62 seconds, exit code 0. They cover Student portions only, not all 194 latest cases. Do not add these overlapping runs to the latest totals. The 715 full-suite result is broader than the 113 unit and 194 marked integration selections; remaining tests are not assigned to either category here.

## IT traceability

The table maps every planned IT group to current source functions via `pytest.mark.it`, including parameter-level marks. It is implementation traceability for the latest aggregate result, not a fabricated per-variant execution log. Multiple IT IDs can share one test; table rows are not test counts. The latest screenshots show passed Advisor and Student variants and the final aggregate, but do not cover the complete scrollback. Complete latest per-variant output and per-IT executed counts are **missing**; the retained Student text log provides its historical per-node outcomes.

| Case | Planned workflow/boundary | Current implementing function(s) |
|---|---|---|
| IT-01 | Real login, cookie and logout | [test_student_login_cookie_and_logout](../../../tests/integration/test_student_workflow.py); [test_bad_credentials_never_authenticate](../../../tests/integration/test_student_workflow.py) |
| IT-02 | Student degree progress through HTTP | [test_degree_progress_through_authenticated_html_and_json](../../../tests/integration/test_student_workflow.py) |
| IT-03 | Eligible selection, submission and advisor queue | [test_advisor_queue_receives_real_student_submission_and_only_pending_plans](../../../tests/integration/test_advisor_workflow.py); [test_available_courses_use_completed_prerequisites_and_tracked_status](../../../tests/integration/test_student_workflow.py); [test_valid_submission_persists_courses_and_can_be_retrieved](../../../tests/integration/test_student_workflow.py) |
| IT-04 | Persistence across requests and sessions | [test_advisor_queue_receives_real_student_submission_and_only_pending_plans](../../../tests/integration/test_advisor_workflow.py); [test_student_resubmits_reviewed_plan_and_advisor_reviews_replacement](../../../tests/integration/test_advisor_workflow.py); [test_valid_submission_persists_courses_and_can_be_retrieved](../../../tests/integration/test_student_workflow.py) |
| IT-05 | Advisor approval and rejection | [test_advisor_decision_persists_and_student_receives_only_own_feedback](../../../tests/integration/test_advisor_workflow.py) |
| IT-06 | Request changes and resubmit | [test_advisor_decision_persists_and_student_receives_only_own_feedback](../../../tests/integration/test_advisor_workflow.py); [test_student_resubmits_reviewed_plan_and_advisor_reviews_replacement](../../../tests/integration/test_advisor_workflow.py); [test_resubmission_reuses_plan_and_replaces_old_selection](../../../tests/integration/test_student_workflow.py) |
| IT-07 | Rejected plan resubmission without cancellation | [test_student_resubmits_reviewed_plan_and_advisor_reviews_replacement](../../../tests/integration/test_advisor_workflow.py); [test_resubmission_reuses_plan_and_replaces_old_selection](../../../tests/integration/test_student_workflow.py) |
| IT-08 | Allowed cancellation and replacement | [test_cancelled_plan_leaves_advisor_queue_and_replacement_returns](../../../tests/integration/test_advisor_workflow.py); [test_allowed_cancellation_retains_history_and_replacement_gets_new_id](../../../tests/integration/test_student_workflow.py) |
| IT-09 | Forbidden cancellation statuses | [test_cancellation_rejected_for_forbidden_status](../../../tests/integration/test_student_workflow.py) |
| IT-10 | Submitted course removal and last-course rule | [test_pending_plan_can_remove_course_but_keeps_last_course](../../../tests/integration/test_student_workflow.py); [test_course_removal_rejected_for_non_pending_plan](../../../tests/integration/test_student_workflow.py) |
| IT-11 | Cross-student ownership and data visibility | [test_advisor_decision_persists_and_student_receives_only_own_feedback](../../../tests/integration/test_advisor_workflow.py); [test_other_students_plan_and_private_data_are_inaccessible](../../../tests/integration/test_student_workflow.py) |
| IT-12 | Unauthenticated and invalid-token access | [test_advisor_endpoints_deny_unauthenticated_and_invalid_tokens](../../../tests/integration/test_advisor_workflow.py); [test_protected_student_requests_deny_invalid_auth_without_writes](../../../tests/integration/test_student_workflow.py) |
| IT-13 | Student cannot use advisor operations | [test_students_cannot_access_advisor_queue_or_decisions](../../../tests/integration/test_advisor_workflow.py) |
| IT-14 | Business-invalid submission inputs | [test_invalid_semester_rejects_without_writes](../../../tests/integration/test_student_workflow.py); [test_duplicate_missing_or_ineligible_courses_are_atomic_rejections](../../../tests/integration/test_student_workflow.py); [test_invalid_resubmission_preserves_review_and_old_courses](../../../tests/integration/test_student_workflow.py) |
| IT-15 | Duplicate active semester plan | [test_active_plan_blocks_duplicate_but_allows_different_semester](../../../tests/integration/test_student_workflow.py) |
| IT-16 | Invalid review payload shapes and syntax | [test_invalid_review_json_is_rejected_before_writes](../../../tests/integration/test_advisor_workflow.py); [test_noninteger_review_path_is_rejected_without_writes](../../../tests/integration/test_advisor_workflow.py) |
| IT-17 | Review business validation and feedback boundary | [test_unknown_decision_is_rejected_without_writes](../../../tests/integration/test_advisor_workflow.py); [test_feedback_at_limit_is_accepted](../../../tests/integration/test_advisor_workflow.py); [test_feedback_over_limit_is_rejected_before_trimming](../../../tests/integration/test_advisor_workflow.py); [test_already_reviewed_plan_cannot_be_reviewed_again](../../../tests/integration/test_advisor_workflow.py); [test_nonpending_status_rejects_review](../../../tests/integration/test_advisor_workflow.py); [test_missing_plan_rejects_review](../../../tests/integration/test_advisor_workflow.py) |
| IT-18 | Invalid form types and path identifiers | [test_invalid_form_or_path_types_return_422_without_writes](../../../tests/integration/test_student_workflow.py); [test_missing_plan_or_course_warns_without_writes](../../../tests/integration/test_student_workflow.py) |
| IT-19 | Database uniqueness constraints | [test_database_constraints_preserve_committed_records](../../../tests/integration/test_database_integrity.py) |
| IT-20 | Create/resubmit transaction rollback | [test_failed_plan_transaction_rolls_back_all_changes_and_session_is_reusable](../../../tests/integration/test_database_integrity.py) |

The retained [Student IT traceability](../evidence/student-integration.md) describes actual expected-versus-observed HTTP and fresh-session state assertions for IT-01-04, Student portions of IT-06-12, IT-14-15 and IT-18. Current Advisor and database test source supplies the additional planned boundaries, and latest screenshots show Advisor lifecycle/boundary tests passing. No complete latest detailed text/JUnit export is available. Plan body fields saying Not Run and H3/earlier-scope comments are historical: the reporting addendum records their current evidence disposition without rewriting old executions.

## Execution command and environment

The latest integration screenshots show this actual PowerShell command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -m integration -v --basetemp="$base\integration"
```

The Unit start screenshot shows `$base = Join-Path $env:LOCALAPPDATA "MyAdvisor-A2-Pytest"` in the same repository terminal. The integration start confirms Windows/win32, the repository `.venv` interpreter, Python **3.14.0**, pytest **9.1.1**, pluggy **1.6.0**, anyio **4.15.1**, pytest-asyncio **1.4.0** and `pyproject.toml` configuration. It records **715 collected / 521 deselected / 194 selected**. The final screenshot shows **194 passed, 521 deselected, 1 warning in 30.52s** and the returned prompt. A numeric exit code is not displayed.

Recorded earlier Student-only command:

```powershell
python -m pytest tests/integration/test_student_workflow.py -m integration -v -p no:cacheprovider
```

The retained Student run records FastAPI 0.141.1 and SQLModel 0.0.42; these versions are not visible in the latest screenshots. Current fixtures use per-case in-memory SQLite, foreign keys, real request Sessions, separate actor clients and external-connection guards. Latest exact dependency inventory, build/commit and named tester are **missing**. Capture/execution date is **26 October 2026**, confirmed by the student and filenames; no separate terminal execution timestamp/time-zone record is shown. The older baseline commit with local changes must not identify the latest build.

For full-suite context PROGRESS retains the student's **715 passed, 1 warning in 56.83s**, using verbose execution and `--basetemp="$base\all"`; the full-suite screenshot/raw output is **missing**. These six screenshots evidence the marked runs only.

## Screenshot evidence

All three Integration images were inspected visually. Capture date: **26 October 2026**.

| Evidence | What is visible |
|---|---|
| [231956: start and Advisor lifecycle](../screenshots/Integration/Screenshot%202026-10-26%20231956.png) | Command/environment/collection totals, queue receipt, approval/rejection/changes requested, Student resubmission and cancellation variants passing |
| [232025: Advisor validation](../screenshots/Integration/Screenshot%202026-10-26%20232025.png) | Oversized feedback, repeated review and non-Pending status variants passing |
| [232058: completed summary](../screenshots/Integration/Screenshot%202026-10-26%20232058.png) | Student validation/resubmission/cancellation/security variants, exact warning, final totals and duration |

![Completed integration run: 194 passed, 521 deselected, 1 warning in 30.52s](../screenshots/Integration/Screenshot%202026-10-26%20232058.png)

Intermediate nodes, including the entire database-test output, are not all visible in these captures; no screenshot is claimed to prove every individual parameter variant.

## Defects, retests and warnings

The retained Student run passed initially (59 in 4.56s) and finally (59 in 4.62s), with no application fix claimed. Historical H3 (HTML denial returned HTTP 200) is superseded by retained executed Student 401 checks. The separate [Workflow 1 API record](../evidence/workflow1-api.md) also records current HTML/JSON 401 behavior.

The [Workflow 3 API record](../evidence/workflow3-api.md) documents six initially failing expiry cases caused by the test fixture supplying an overwritten `exp` claim. The fixture was corrected to use negative `expires_delta`; the recorded final broader run had 409 passed. This is historical automated fixture/retest evidence, not a Postman result or a defect discovered in the latest 194-test run. No dated per-defect retest export for that latest run is available.

The latest completed screenshot explicitly identifies the same `StarletteDeprecationWarning` as the earlier logs: httpx use with Starlette TestClient is deprecated, with httpx2 suggested. It is a dependency warning rather than an assertion failure. The Windows temporary-directory setup issue is recorded as resolved in PROGRESS.

## Conclusion

The student's verified latest marked integration result is **194 passed, 521 deselected, 1 warning**. Current source maps all 20 planned IT groups; older retained execution proves the documented Student subset. Latest screenshots corroborate the command, totals, duration, warning and visible variants. A complete latest per-node export remains missing, limiting independent verification of every planned variant. No manual acceptance or Collection Runner success follows from this automated result.

## Cross-method reporting reconciliation — 27 October 2026

The latest verified full suite is **715 passed, 0 failures, 0 errors, 1 warning**. It overlaps the unit and integration selections; these totals must not be added. Screenshot readability and provenance were rechecked in the [evidence inventory](evidence-inventory.md). [Workflow traceability](requirements-test-traceability.md) links actual UT/IT IDs, collection request numbers and UAT cases. Postman is now executed: **90 requests, 470 successful assertions, 0 assertion failures, 0 execution errors, 1 iteration**, corroborated by the supplied Runner screenshots. UAT now records **1 Pass / 0 Fail / 19 Not Run**, including 18 partially verified cases and one unverified workflow; see the reconciled UAT report. Tester Cameron Ramesar confirms all 19 UAT captures/workflows were executed on 27 October 2026. No tests or application functionality were changed.

Prompt 14 final reconciliation: existing completed-summary screenshot visually rechecked; verified automated counts above unchanged. No rerun. Full-suite 715-pass result remains user-verified without a retained full-suite screenshot.
