# Requirements-to-test traceability — WF1–WF3

> **Approved-allocation update ? 27 October 2026:** [Current correction record](degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.

## Current R01/R02 correction overlay

| Requirement | New automated coverage | API/manual evidence status |
|---|---|---|
| R01 Degree totals and non-overlapping categories | `tests/unit/test_demo_requirements.py`; `tests/integration/test_demo_requirement_migration.py`. Approved 36/18/12/18/9, sum 93; exact overall/category oracles; safe migration and full history preservation. Genuine complete run: 751 passes, one warning, no failures/errors/skips. | Revised PM19 exact requirements/percentages is statically validated, runtime pending. Corrected UAT-01 refresh/images pending. F05 configuration inconsistency resolved; historical image remains unchanged. |
| R02 Completed-only prerequisites | Fresh-seed integration positively checks COMP 1201 eligibility through completed COMP 1101; prior prerequisite tests remain unchanged. | Revised PM20 known prerequisite oracle is statically validated, runtime pending. UAT-02/03 controls and positive path still need the new human run. |

The older matrix below is historical where superseded. Current JSON revision is 2026.10.27-degree93; do not attribute the old 470-assertion screenshots to it.



## Current correction coverage supplement ? 27 October 2026

Original requirement/test identifiers below are preserved. This supplement maps new regression sources without inventing original plan IDs. See [actual results](audit-correction-report.md) and [pending manual/API checks](correction-retest-guide.md).

| Workflow / concern | Added automated regression | Pending independent retest |
|---|---|---|
| WF2/WF3 ? role separation / F01 | `tests/integration/test_audit_corrections.py`: 12 role/owner/action variants, real authentication, 403, all-table snapshot unchanged; existing legitimate Student/Advisor suite passes. | Supplemental three Advisor HTML requests; UAT-04/07?17/20; collection authorization/lifecycle checks. |
| WF2/WF3 ? persistence / F07 | Same file: two actual application-engine invalid-FK variants, pooled connections, valid row retention and reconnect policy. | Full ordered collection and Student/Advisor lifecycle UAT; no browser claim of direct DB constraint proof. |
| Supporting authentication / F08 | Same file: three malformed emails reject 422 without writes; valid/duplicate registration remains controlled. | Supplemental native-browser/server validation and valid registration; collection authentication/registration. |
| WF3 ? readability / F06 | `tests/integration/test_contrast_regression.py`: real Advisor/Approved templates, pinned cascade, normal/hover contrast; two variants. | Fresh UAT-06 table normal/hover and UAT-09 full Approved paragraph screenshots. |
| WF1 ? F05/F13 | Existing arithmetic tests retained; no curriculum change authorized or new exact-category oracle asserted. | Owner approval first, then independent category expectations, Postman request 19 and UAT-01/reports. |

Final full run: **735 passed**, including all **214 integration and 113 unit nodes**, zero failures/errors/skips, 1 warning. Manual results remain historical and incomplete.

---

## Preserved traceability records

Updated **27 October 2026** from actual test source/markers, the 90-request collection, plans and inspected evidence. UT-01–23 are planned groups implemented by `test_UT_01_…` through `test_UT_23_…`; IT-01–20 use `pytest.mark.it`, including parameter marks. Request 01–90 numbers are actual collection identifiers. UAT-01–20 are the unique execution-sheet IDs. R01–R15 remain local requirement labels in the original plans, not official rubric identifiers.

| Workflow / requirements | Unit cases and actual source | Integration cases and actual source | Postman request IDs | Manual UAT cases | Existing execution evidence |
|---|---|---|---|---|---|
| **WF1 — Track Degree Progress**; R01 (totals/categories/boundaries), R02 (eligibility context), R11–12 (access), R15 (public response contracts) | UT-01–06 calculations/prerequisites in [test_advising.py](../../../tests/unit/test_advising.py); UT-20–23 supporting auth in [test_auth.py](../../../tests/unit/test_auth.py) | IT-01/02/03/12 in [Student workflow](../../../tests/integration/test_student_workflow.py), notably `test_degree_progress_through_authenticated_html_and_json`, `test_available_courses_use_completed_prerequisites_and_tracked_status` | 02, 07–10, 13–20, 25, 87–90 (shared auth boundaries included) | UAT-01; supporting UAT-18/20 | [Unit start](../screenshots/Unit/Screenshot%202026-10-26%20231703.png), [unit log](../evidence/unit/pytest-output.txt); [Student integration log](../evidence/student-integration-pytest.txt); [Postman 01–20](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012608.png); [Degree Progress](../screenshots/UAT/UAT-02.png) and [Student Home](../screenshots/UAT/UAT-01.png), partial UAT only |
| **WF2 — Plan Semester Course Selections**; R02–05, R08–10, R11–14 | UT-04–13 eligibility/selection/status, UT-18/19 cancellation/removal in [test_advising.py](../../../tests/unit/test_advising.py); UT-20–23 shared auth | IT-03/04/06–12/14/15/18 in [Student workflow](../../../tests/integration/test_student_workflow.py), including `test_valid_submission_persists_courses_and_can_be_retrieved`, `test_resubmission_reuses_plan_and_replaces_old_selection`, `test_allowed_cancellation_retains_history_and_replacement_gets_new_id`; IT-19/20 [DB constraints/rollback](../../../tests/integration/test_database_integrity.py) | 03–04, 09, 11–12, 16–17, 20–50, 63–66, 68, 70, 72, 74–90 (shared/cross-role checkpoints included) | UAT-02–05, UAT-08, UAT-10, UAT-12–17; supporting UAT-18/20 | [Unit completed](../screenshots/Unit/Screenshot%202026-10-26%20231747.png), [Integration completed](../screenshots/Integration/Screenshot%202026-10-26%20232058.png); [Postman 21–40](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012643.png), [41–60](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012658.png), [61–80](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012739.png), [72–90](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012839.png); [selection](../screenshots/UAT/UAT-03.png), [Pending submission](../screenshots/UAT/UAT-04.png), partial UAT only |
| **WF3 — Review and Approve Course Plans**; R05–08, R11–14 | UT-14–17 decision mapping/feedback/Pending guard in [test_advising.py](../../../tests/unit/test_advising.py); UT-20–23 shared auth | IT-03–08/11–13/16/17 in [Advisor workflow](../../../tests/integration/test_advisor_workflow.py), including `test_advisor_decision_persists_and_student_receives_only_own_feedback`, `test_student_resubmits_reviewed_plan_and_advisor_reviews_replacement`, `test_invalid_review_json_is_rejected_before_writes`; IT-19/20 shared persistence boundaries | 05–06, 10, 13–18, 42–47, 51–86, 88 (auth/Student delivery and state checkpoints included) | UAT-06–09, UAT-11; Advisor queue checks in UAT-12/13/16/17; supporting UAT-19/20 | [Advisor lifecycle](../screenshots/Integration/Screenshot%202026-10-26%20231956.png), [Advisor validation](../screenshots/Integration/Screenshot%202026-10-26%20232025.png); [Unit late tests](../screenshots/Unit/Screenshot%202026-10-26%20231742.png); [Postman review validation](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012658.png), [decisions](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012739.png); [Advisor Pending review](../screenshots/UAT/UAT-05.png), partial UAT only |

## Result interpretation and audit boundaries

The marked runs report **113 unit passes (602 deselected)** and **194 integration passes (521 deselected)**, each with one warning. The full suite is **715 passed, zero failures/errors, one warning**; selections overlap that full result. [Unit](unit-test-report.md) and [integration](integration-test-report.md) reports map every planned group to concrete function names and distinguish historical complete logs from latest aggregate/partial screenshots. No percentage of line/branch coverage was measured, so none is claimed. IT-19/20 source establishes constraint/rollback scope; their individual latest output is not visible in the screenshots.

[Postman](postman-test-report.md): **90 requests, 470 successful assertions, zero assertion failures/errors, one iteration**, 27 October 2026. Screenshots span 01–90; some edge rows are clipped. [UAT](uat-final-report.md): **1 Pass / 0 Fail / 19 Not Run**; 18 cases partially verified and UAT-05 required workflow unverified. All 19 screenshots map to actual manual outcomes in the [matrix](uat-evidence-review.md). WF2 now has screenshot-supported revision, removal, all three cancellations and replacement; WF3 has Changes Requested, Approved and Rejected outcomes/feedback. UAT-20 proves signed-out UI restriction only, not logged-in role checks. Cameron Ramesar confirms execution on 27 October 2026. DATA-01 and UI-01 remain open.

See the [evidence inventory](evidence-inventory.md) for every verified screenshot, readability limits, hashes and missing exports. The R-level matrices in [unit plan](../test-plans/unit-test-plan.md) and [integration plan](../test-plans/integration-test-plan.md) supplement this workflow matrix. Requirements without browser equivalents (malformed payload/schema/direct database rollback) remain automated/API scope; a mapping does not create a manual execution result.

## Additional manual lifecycle traceability

| Requirement scope | Actual manual evidence | Limitation |
|---|---|---|
| WF2 revision/resubmission | UAT-07/08: MATH 2250 replaced by ENGL 1000, 9 credits | Stored feedback clearance unconfirmed |
| WF3 feedback/decisions | UAT-07/09/11: Changes Requested, Approved, Rejected | Queue removal and Advisor confirmations unconfirmed |
| WF2 removal/cancellation/replacement | UAT-12?17: 6?3 credits, A/B/C Cancelled, C new ENGL 1000 Pending | Dismissal, persistence, Messages and queue checks as listed in matrix |
| Supporting access | UAT-20 401/login captures | Student 403 and Advisor fallback unverified |

Tester clarification on 27 October 2026 leaves current totals unchanged: **1 Pass / 0 Fail / 19 Not Run**. Existing state/feedback evidence is retained; refresh persistence and remaining role checks are not inferred. See [case-specific supplemental evidence requirements](uat-supplemental-evidence.md).
