# MyAdvisor — Unit Test Plan

> **Approved-allocation update ? 27 October 2026:** [Current correction record](../reports/degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.

## Supplement: approved fictional requirements (current version)

The original UT-01?23 case IDs and independent synthetic fixtures are retained. `tests/unit/test_demo_requirements.py` adds three variants: exact approved configuration and sum 93; literal seeded progress/category oracles; repeated completed-course ID counted once. Expected totals are 6 completed / 3 in progress / 84 remaining / 93 required / 6%. Expected categories are Core (3,36,33,8), General Education (3,18,15,17), Electives (0,12,12,0), Major (0,18,18,0), Additional (0,9,9,0), in earned/required/remaining/percent order. These supplement the synthetic Core=30 boundary tests rather than weakening or replacing them. The genuine complete run has 751 passes with 116 unit members; no new separate marked-unit run or screenshot is claimed here.



**Correction-stage supplement ? 27 October 2026:** original IDs, inputs and expected outcomes below are retained. [Additional correction coverage](../reports/requirements-test-traceability.md) documents focused HTML role, actual-engine integrity, registration and contrast regressions. [Actual corrected-build results](../reports/audit-correction-report.md) are separate from historical marked/manual runs. [Required browser/API retests](../reports/correction-retest-guide.md) remain pending; no expected outcome has been promoted to an observation. F05 curriculum values are unchanged pending owner approval.

**Prompt 15 current disposition (27 October 2026):** historical planning/execution entries below are retained. Current implementation, evidence limitations and open defects are assessed in the [final quality audit](../final-quality-audit.md); the [official Assignment 2 source record](../official-assignment-brief.md) supplies the rubric. No original test-case expected outcome was changed.

Implementation addendum (26 October 2026): [API verification evidence](../evidence/workflow1-api.md) links R01/R02 calculation and eligibility coverage to the new HTTP integration tests, including empty records, missing program, zero denominators and caps (subsets of UT-01–UT-06). These database-backed tests are integration coverage, not mock-isolated completion of all planned unit variants. New R15 covers validated public JSON schemas; its validation test and OpenAPI checks are listed in API-07. The unit execution addendum and case statuses below now record the isolated unit run; earlier API coverage remains separate.

Prepared: 26 October 2026. Version: 1.1. Execution state: **Passed — all 23 unit groups executed (112 new variants plus retained E12 = 113 passed)**.

## Basis and scope limitation

The request refers to a completed MyAdvisor repository audit, but no saved audit document was located in the accessible workspace. This plan therefore uses the current root repository, [existing report](../../report.md) and inspected tests as its verifiable basis; no audit findings or previous run outcomes are invented. If a separate audit becomes available, reconcile its requirement IDs and findings before execution. The original planning task produced specifications only. The authorized unit implementation and actual execution are recorded below.

Primary source references: [advising service](../../../app/services/advising_service.py), [advising repository](../../../app/repositories/advising.py), [models](../../../app/models/advising.py), [student routes](../../../app/routers/user_home.py), [advisor routes](../../../app/routers/admin_home.py), [authentication service](../../../app/services/auth_service.py), [authentication dependencies](../../../app/dependencies/auth.py), [security utilities](../../../app/utilities/security.py), [login](../../../app/routers/login.py), [logout](../../../app/routers/logout.py) and [application/error handler](../../../app/main.py).

## Shared rule interpretation

- Remaining credits subtract completed **and in-progress** credits; overall progress percentage uses **completed only**. Category credits also use completed only.
- Semester names are exactly `Year 1 semester 1` through `Year 3 semester 3`; submission strips outer whitespace and then validates case-sensitively. Invalid dashboard semester queries fall back to a valid latest plan or the first option.
- Pending/Approved block same-semester submission. Rejected/Changes Requested resubmit the same plan. Cancelled permits a new plan. Cancellation itself permits only Pending/Approved/Rejected.
- All three advisor decisions allow empty feedback. The 500-character limit checks raw string length **before** stripping whitespace.
- Current advisor review is a global Pending queue; no advisor-student assignment restriction is defined. Do not invent an assignment-ownership rule.
- Student mutation routes currently use AuthDep rather than a student-role guard. The specified ownership tests check authenticated identity and foreign-plan denial; they do not claim the application prevents every advisor from creating their own plan.
- Business ValueError failures become warning flashes and 303 redirects, not generic 400/422 API responses. The review route accepts JSON or form input; student plan submission accepts form fields. No separate `/api/plans` endpoint is assumed.
- **Historical H3 (resolved before this audit):** the earlier HTML 401 handler defaulted to HTTP 200. Current `app/main.py` explicitly returns HTTP 401; authenticated wrong-role guards return HTTP 403. Existing integration tests verify status, denial content, no private data and no writes. This historical issue is distinct from the open HTML planning role gap in the [final quality audit](../final-quality-audit.md).

## Objective and isolation strategy

Verify business decisions independently of HTTP, template rendering and SQLModel persistence. Instantiate real AdvisingService with repository constructors replaced in `app.services.advising_service`, supplying autospecced repository doubles; use a nonfunctional session sentinel so accidental database access fails. Alternatively replace both service repository attributes before calling business methods. Return in-memory SQLModel objects with explicit IDs; mutation methods are spies/sentinels. Assert results, domain error messages and whether create/resubmit/update/delete was invoked. Do not mock the method being tested or compute expected answers using that method.

AuthService receives a mocked UserRepository; patch hashing/token collaborators at their import location in `app.services.auth_service` for orchestration tests. Dependency tests use synthetic Requests and mocked decoder/repository lookups. UT-23 deliberately uses real local cryptography with test-only settings and controlled time; it needs no database/network. SQL constraints, commit/rollback and actual cookie delivery belong to the integration plan.

## F1 — in-memory fixture vocabulary

S1 is a regular_user student, S2 another student, and A1 an admin advisor; use explicit distinct integer IDs. T1=`Year 1 semester 1`, T2=`Year 1 semester 2`. Catalogue: C1 (ID 101, COMP 1100, 3 credits, Core Courses), C2 (102, MATH 1000, 3 credits, General Education), C3 (103, COMP 2000, 3 credits, prerequisite COMP 1100, Core Courses), C4 (104, MATH 2000, 3 credits, no prerequisites, Electives), C5 (105, COMP 3000, 3 credits, prerequisites COMP 1100 and MATH 9999). Default S1 records: C1 Completed/A, C2 In Progress; C3/C4 untracked. Program total 93; Core required 30. Cases explicitly override these defaults. Empty plan history is the default. Mock every repository method reached by dashboard construction, including message/history lookups; do not leave implicit MagicMock return values.

## Existing coverage reviewed before planning

Existing code is coverage evidence, not execution evidence. References below identify tests already present; none is marked passed without a retained run record. All E references except E12 are in [test_advising_service.py](../../../tests/test_advising_service.py); E12 is in [test_login_routing.py](../../../tests/test_login_routing.py).

| Ref | Existing test function | Coverage and reuse decision |
|---|---|---|
| E01 | `test_degree_progress_uses_completed_and_in_progress_course_records` | Service + real SQLite; baseline credits/category totals. |
| E02 | `test_plan_submission_review_request_and_student_resubmission` | Service + SQLite; change request and same-ID resubmission. |
| E03 | `test_json_request_changes_includes_decision_and_feedback` | Template assertions + direct route call; bypasses HTTP dependency resolution. |
| E04 | `test_request_changes_json_http_route` | HTTP + SQLite; overrides is_admin_dep, so does not verify authentication. |
| E05 | `test_plan_validation_blocks_ineligible_courses_and_duplicate_plans` | Service + SQLite; in-progress course and existing Pending plan. |
| E06 | `test_semester_options_cover_three_years_and_summer_terms` | Service + SQLite; nine semester choices. |
| E07 | `test_plan_submission_rejects_legacy_semester_names` | Service + SQLite; Fall 2026 rejected. |
| E08 | `test_plan_submission_names_the_missing_prerequisite` | Service + SQLite; missing prerequisite named. |
| E09 | `test_student_can_remove_submitted_course_cancel_and_resubmit_plan` | Service + SQLite; removal/last-course guard, ownership, Pending/Approved cancellation, replacement. |
| E10 | `test_rejected_plan_can_be_cancelled_and_replaced` | Service + SQLite; Rejected cancellation and new plan ID. |
| E11 | `test_student_registration_stores_profile_and_default_degree` | AuthService + SQLite; profile and default program. |
| E12 | `test_admin_login_redirects_to_home` | Mocked direct login handler; redirect only, no real credential/token validation. |

The advising file also has template/status/navigation rendering, demo-seed idempotence, registration, favicon and schema-upgrade tests. Retain those; do not duplicate their presentation or migration assertions here. The nested `comp3613a1/` checkout contains another tests tree; these plans target the workspace-root `app/` and `tests/`, not a second product or a second test run. Existing database-backed service tests are integration-level coverage even though their filename says service. When implementing later, extend/parameterize a matching test or reuse its fixture before creating a duplicate. Planned unit variants add repository isolation; planned HTTP variants add real authentication, request parsing and fresh-session persistence.

## Requirements-to-test traceability

These R identifiers are local planning identifiers derived from the requested scope, existing report and current source. They do not claim to be official assignment/audit requirement IDs. R13/R14 capture persistence and validation obligations needed to verify the workflows.

| Requirement | Rule / objective | Unit cases | Integration cases | Source basis / existing coverage | UAT mapping / recorded outcome | Postman request mapping / runtime outcome | Reporting evidence |
|---|---|---|---|---|---|---|---|
| R01 | Degree totals, category breakdown and calculation boundaries | UT-01–UT-03 | IT-02 | E01; dashboard service; report Track Degree Progress | UAT-01; Not Run | 19; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R02 | Completed-only prerequisite eligibility and blocked tracked courses | UT-04–UT-06, UT-11 | IT-03, IT-14 | E05,E08; prerequisite_ok/get_course_availability | UAT-02-03; Not Run | 20, 25; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R03 | Nine valid semester names, trimming and invalid names | UT-07, UT-08 | IT-14 | E06,E07; SEMESTER_OPTIONS/submit_plan | UAT-02, UAT-04, UAT-10, UAT-12; Not Run | 21, 26, 31; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R04 | Nonempty, unique, existing course selections | UT-09–UT-11 | IT-03, IT-14, IT-19 | submit_plan; PlanCourse uniqueness | UAT-03-04; Not Run | 22-25, 27, 29-31; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R05 | Plan status and duplicate active-plan rules | UT-12, UT-13, UT-17 | IT-05–IT-07, IT-15, IT-17 | RESUBMITTABLE_PLAN_STATUSES; submit_plan/review_plan | UAT-04-12; UAT-06 Pass, others Not Run | 39-40, 61-80; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R06 | Advisor decision mapping and Pending-only review | UT-14, UT-15, UT-17 | IT-05–IT-07, IT-13, IT-17 | review_plan; report advisor workflow | UAT-06-09, UAT-11, UAT-20; UAT-06 Pass, others Not Run | 51-78; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R07 | Feedback type, raw length limit and trimming | UT-14, UT-16 | IT-05, IT-16, IT-17 | review_plan and admin review route | UAT-07, UAT-09, UAT-11 (visible feedback only); Not Run | 54-61, 69, 74; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R08 | Rejected/change-request resubmission resets existing plan | UT-12, UT-13 | IT-06, IT-07, IT-20 | E02; resubmit_plan | UAT-07-08; Not Run | 61-73; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R09 | Owned Pending/Approved/Rejected cancellation and replacement | UT-13, UT-18 | IT-08, IT-09, IT-11 | E09,E10; cancel_plan; report additional use cases | UAT-14-17; Not Run | 78-86; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R10 | Pending course removal, membership and last-course guard | UT-19 | IT-10, IT-18 | E09; remove_submitted_course | UAT-13; Not Run | 48-50; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R11 | Authentication, advisor role and student ownership isolation | UT-18, UT-19, UT-22 | IT-02, IT-11–IT-13 | AuthDep/AdminDep; student identity from authenticated user | UAT-18-20 (browser scope only); Not Run | 02-18, 28, 33-47, 58-59; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R12 | Credential checking, token/cookie lifecycle and logout | UT-20–UT-23 | IT-01, IT-12 | AuthService; security utilities; auth/login/logout routes | UAT-18-20; Not Run | 07-12, 87-90; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R13 | Committed plans/links, constraints and atomic persistence | UT-11, UT-12 (delegation only) | IT-03–IT-08, IT-10, IT-11, IT-15, IT-19, IT-20 | AdvisingRepository; SQLModel unique/FK constraints | UAT-04-17 (browser persistence subset); Not Run | 30-32, 47-88 (API-visible only; no direct DB constraint/rollback); executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |
| R14 | HTTP parsing, business validation and unchanged state on errors | UT-08–UT-11, UT-15–UT-17 (business guards only) | IT-14, IT-16–IT-18 | Form parameters; admin JSON/form parsing; ValueError redirects | No direct malformed-payload browser case; Not Run | 22-30, 41, 54-60; executed; successful assertions in verified 27 October Runner run | [Unit](../reports/unit-test-report.md), [Integration](../reports/integration-test-report.md), [Postman](../reports/postman-test-report.md), [UAT](../reports/uat-final-report.md) |

Ranges are inclusive. The companion plan uses the same identifiers. A mapped case is planned coverage, not evidence of a pass.

## Unit test cases

Each parameterized input is a separate execution variant under its parent ID. All per-variant outcomes are retained in the linked verbose output and JUnit results.

### UT-01 — Degree totals and category calculation

| Field | Specification |
|---|---|
| Test ID | UT-01 |
| Objective | Degree totals and category calculation. |
| Source Function or Endpoint | AdvisingService.get_student_dashboard |
| Preconditions | Mock repositories return fixture S1 and no plans. |
| Test Data | F1 baseline: completed C1=3; in-progress C2=3; program=93; Core requirement=30. |
| Test Steps | Call dashboard(S1,T1); inspect totals, percentage and category output. |
| Expected Result | Completed=3; in-progress=3; remaining=87; total=93; progress=3%; Core earned=3, remaining=27, percent=10. E01 already checks baseline persistence: add only isolated calculation assertions. |
| Actual Result | 1 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_01_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-02 — Empty academic record and missing program fallback

| Field | Specification |
|---|---|
| Test ID | UT-02 |
| Objective | Empty academic record and missing program fallback. |
| Source Function or Endpoint | AdvisingService.get_student_dashboard |
| Preconditions | Mock user/program/record lookups; no plans. |
| Test Data | Variants: existing 93-credit program with no records; missing degree program. |
| Test Steps | Call each variant with empty completed/in-progress records. |
| Expected Result | Credits=0/0, remaining=93, progress=0; category earned=0 for configured requirements; absent program uses 93 and category_progress=[]. |
| Actual Result | 2 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_02_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-03 — Progress limits, zero denominators and duplicate records

| Field | Specification |
|---|---|
| Test ID | UT-03 |
| Objective | Progress limits, zero denominators and duplicate records. |
| Source Function or Endpoint | AdvisingService.get_student_dashboard |
| Preconditions | Repository doubles only; deliberately synthetic boundary data. |
| Test Data | Variants: total=6, completed=9, in-progress=3; total=0; category required=0; repeated completed record for C1. |
| Test Steps | Call each variant; compare arithmetic independently. |
| Expected Result | Remaining never negative; progress and category percent capped at 100; zero denominator yields 0; duplicate same-status course records count its credits once. Do not claim service sanitizes all inconsistent records. |
| Actual Result | 4 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_03_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-04 — Prerequisites satisfied or absent

| Field | Specification |
|---|---|
| Test ID | UT-04 |
| Objective | Prerequisites satisfied or absent. |
| Source Function or Endpoint | AdvisingService.prerequisite_ok; get_course_availability |
| Preconditions | Mock catalogue, completed IDs and course records. |
| Test Data | C3 requires C1; C4 requires none; advanced course requires ' COMP 1100, MATH 1000 '; both completed in last variant. |
| Test Steps | Call both functions for each target; compare bool and availability message. |
| Expected Result | Untracked targets eligible if all named prerequisites completed; whitespace ignored; no prerequisites eligible; availability=(True, 'Eligible'). |
| Actual Result | 4 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_04_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-05 — Missing and in-progress prerequisites

| Field | Specification |
|---|---|
| Test ID | UT-05 |
| Objective | Missing and in-progress prerequisites. |
| Source Function or Endpoint | AdvisingService.prerequisite_ok; get_course_availability |
| Preconditions | Mock completed IDs exclude C2; C2 is In Progress. |
| Test Data | C3 requiring C2; advanced course requiring C1 and unknown MATH 9999; blank comma-separated tokens. |
| Test Steps | Evaluate both eligibility functions per variant. |
| Expected Result | In-progress prerequisite does not satisfy completion; unknown code fails; availability names only unmet codes; empty comma tokens ignored. E08 supplies DB-backed missing-code baseline. |
| Actual Result | 3 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_05_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-06 — Tracked or unknown target courses

| Field | Specification |
|---|---|
| Test ID | UT-06 |
| Objective | Tracked or unknown target courses. |
| Source Function or Endpoint | AdvisingService.prerequisite_ok; get_course_availability |
| Preconditions | Mock repository returns completed C1, in-progress C2 and absent ID 999999. |
| Test Data | Targets C1, C2, 999999. |
| Test Steps | Evaluate prerequisite_ok for all; inspect catalogue availability for C1/C2. |
| Expected Result | False for all three; C1 says Already completed; C2 says Already in progress; nonexistent course absent from availability map. |
| Actual Result | 3 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_06_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-07 — Valid semester names and trimming

| Field | Specification |
|---|---|
| Test ID | UT-07 |
| Objective | Valid semester names and trimming. |
| Source Function or Endpoint | AdvisingService.submit_plan; SEMESTER_OPTIONS |
| Preconditions | Mock eligible C3, no existing plan, create_plan sentinel. |
| Test Data | All nine Year {1..3} semester {1..3}; padded '  Year 1 semester 1  '. |
| Test Steps | Parameterize valid values; submit [C3]; inspect create_plan arguments. |
| Expected Result | Each accepted; exactly nine options including semester 3; padded input stored trimmed. E06 baseline reused rather than copied. |
| Actual Result | 10 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_07_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-08 — Invalid semester names

| Field | Specification |
|---|---|
| Test ID | UT-08 |
| Objective | Invalid semester names. |
| Source Function or Endpoint | AdvisingService.submit_plan |
| Preconditions | Mock repositories; mutation methods are spies. |
| Test Data | '', whitespace, Fall 2026, Year 0 semester 1, Year 4 semester 1, Year 1 semester 4, Year 1 Semester 1. |
| Test Steps | Submit [C3] for each input; capture exception and calls. |
| Expected Result | ValueError 'Choose a valid year and semester before submitting a plan.'; no create/resubmit call. E07 reused for its legacy-name variant. |
| Actual Result | 7 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_08_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-09 — Empty selection

| Field | Specification |
|---|---|
| Test ID | UT-09 |
| Objective | Empty selection. |
| Source Function or Endpoint | AdvisingService.submit_plan |
| Preconditions | No database; repository spies. |
| Test Data | [] with valid T1. |
| Test Steps | Call submit_plan(S1,[],T1). |
| Expected Result | ValueError 'Select at least one course for the semester plan.'; no persistence or eligibility lookup. |
| Actual Result | 1 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_09_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-10 — Duplicate selected course IDs

| Field | Specification |
|---|---|
| Test ID | UT-10 |
| Objective | Duplicate selected course IDs. |
| Source Function or Endpoint | AdvisingService.submit_plan |
| Preconditions | No database; repository spies. |
| Test Data | [C3,C3] and [C3,C4,C3] with T1. |
| Test Steps | Submit each duplicate list. |
| Expected Result | ValueError 'A course may only appear once in a semester plan.'; no create/resubmit call. Distinct from duplicate semester plan in E05. |
| Actual Result | 2 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_10_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-11 — Missing or ineligible selection aborts submission

| Field | Specification |
|---|---|
| Test ID | UT-11 |
| Objective | Missing or ineligible selection aborts submission. |
| Source Function or Endpoint | AdvisingService.submit_plan |
| Preconditions | Mock availability and course lookup, no real repository operations. |
| Test Data | [C3,999999]; [C1]; [C2]; [advanced course missing MATH 9999]. |
| Test Steps | Submit each selection; inspect all mutation spies. |
| Expected Result | Missing ID reports no longer available; ineligible selection includes course code and reason; no create/resubmit call even when earlier list item was valid. |
| Actual Result | 4 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_11_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-12 — Submission status decision table

| Field | Specification |
|---|---|
| Test ID | UT-12 |
| Objective | Submission status decision table. |
| Source Function or Endpoint | AdvisingService.submit_plan |
| Preconditions | Mock existing-plan lookup and mutation return sentinels. |
| Test Data | Existing status: none, Pending, Approved, Rejected, Changes Requested, Cancelled; valid [C3],T1. |
| Test Steps | Submit each variant separately and assert exactly which repository method is called. |
| Expected Result | None/Cancelled -> create_plan; Rejected/Changes Requested -> resubmit_plan(existing,[C3]); Pending/Approved -> ValueError already under review or approved and no mutation. Database replacement/reset details belong to integration tests. |
| Actual Result | 6 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_12_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-13 — Dashboard edit and cancelled-selection rules

| Field | Specification |
|---|---|
| Test ID | UT-13 |
| Objective | Dashboard edit and cancelled-selection rules. |
| Source Function or Endpoint | AdvisingService.get_student_dashboard |
| Preconditions | Mock current plan and its C3 link, no DB. |
| Test Data | Each status Pending, Approved, Rejected, Changes Requested, Cancelled; also no plan. |
| Test Steps | Build dashboard per variant; inspect selected IDs, planned courses, can_edit_plan. |
| Expected Result | Edit true only Rejected/Changes Requested/Cancelled; false Pending/Approved/no plan. Cancelled hides saved course links; other existing statuses retain selected C3. |
| Actual Result | 6 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_13_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-14 — Advisor decisions and feedback normalization

| Field | Specification |
|---|---|
| Test ID | UT-14 |
| Objective | Advisor decisions and feedback normalization. |
| Source Function or Endpoint | AdvisingService.review_plan |
| Preconditions | Mock Pending plan, update_plan sentinel. |
| Test Data | approve, reject, request_changes; feedback='  Review note  '; advisor=A1. |
| Test Steps | Call each decision separately; inspect update_plan keywords. |
| Expected Result | Mapped statuses Approved, Rejected, Changes Requested; feedback='Review note'; advisor_id=A1; exactly one update call. Empty feedback is allowed for every decision. |
| Actual Result | 6 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_14_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-15 — Invalid advisor decision

| Field | Specification |
|---|---|
| Test ID | UT-15 |
| Objective | Invalid advisor decision. |
| Source Function or Endpoint | AdvisingService.review_plan |
| Preconditions | Repository lookup/update spies. |
| Test Data | '', APPROVE, cancel, unknown; valid short feedback. |
| Test Steps | Call review_plan per decision. |
| Expected Result | ValueError 'Choose approve, reject, or request changes.' before persistence; no update call. |
| Actual Result | 4 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_15_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-16 — Feedback length boundary before trimming

| Field | Specification |
|---|---|
| Test ID | UT-16 |
| Objective | Feedback length boundary before trimming. |
| Source Function or Endpoint | AdvisingService.review_plan |
| Preconditions | Mock Pending plan and update spy. |
| Test Data | For each legal decision: lengths 0,499,500,501; 501 spaces; ' '+499 characters+' ' (501 total). |
| Test Steps | Call review_plan per variant; compare raw and stripped lengths. |
| Expected Result | 0/499/500 accepted, stored stripped; 501 rejected with 'Advisor feedback must be 500 characters or fewer.' even if trimming would shorten it; no update on rejection. |
| Actual Result | 18 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_16_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-17 — Review only existing Pending plans

| Field | Specification |
|---|---|
| Test ID | UT-17 |
| Objective | Review only existing Pending plans. |
| Source Function or Endpoint | AdvisingService.review_plan |
| Preconditions | Mock lookup absent or returning status variant. |
| Test Data | Missing plan; Approved, Rejected, Changes Requested, Cancelled; valid approve/feedback. |
| Test Steps | Call review_plan for each variant. |
| Expected Result | Missing -> ValueError 'Plan not found'; each non-Pending -> 'Only pending plans can be reviewed.'; no update. |
| Actual Result | 5 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_17_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-18 — Cancellation status and ownership matrix

| Field | Specification |
|---|---|
| Test ID | UT-18 |
| Objective | Cancellation status and ownership matrix. |
| Source Function or Endpoint | AdvisingService.cancel_plan |
| Preconditions | Mock owned/foreign/missing plan and cancel spy. |
| Test Data | Owned Pending, Approved, Rejected, Changes Requested, Cancelled; foreign S2 plan; missing plan. |
| Test Steps | Cancel as S1 per independent variant. |
| Expected Result | Only owned Pending/Approved/Rejected delegated to repo.cancel_plan; other owned statuses reject; foreign/missing -> 'Plan not found.'; no mutation on denial. |
| Actual Result | 7 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_18_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-19 — Remove course guard matrix

| Field | Specification |
|---|---|
| Test ID | UT-19 |
| Objective | Remove course guard matrix. |
| Source Function or Endpoint | AdvisingService.remove_submitted_course |
| Preconditions | Mock owned Pending plan with C3/C4 links and remove spy. |
| Test Data | Remove C4 from two links; last C3; absent course; non-Pending statuses; foreign or absent plan. |
| Test Steps | Call each variant independently; inspect remove_plan_course call. |
| Expected Result | Only an owned Pending plan with matching course and more than one link permits deletion; others reject with existing guard messages; no deletion on failure. |
| Actual Result | 9 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_advising.py](../../../tests/unit/test_advising.py), functions prefixed `test_UT_19_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-20 — Authentication success

| Field | Specification |
|---|---|
| Test ID | UT-20 |
| Objective | Authentication success. |
| Source Function or Endpoint | AuthService.authenticate_user |
| Preconditions | Mock UserRepository; patch verify_password and create_access_token in app.services.auth_service. |
| Test Data | Stored user id=S1, role=regular_user, password='stored-hash'; verifier=True. |
| Test Steps | Authenticate with username and plaintext; inspect calls. |
| Expected Result | Returns token sentinel; verifier receives plaintext and stored hash; token data={'sub': str(S1), 'role':'regular_user'}; no real DB/hash/JWT needed. |
| Actual Result | 1 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_auth.py](../../../tests/unit/test_auth.py), functions prefixed `test_UT_20_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-21 — Authentication failures and short circuit

| Field | Specification |
|---|---|
| Test ID | UT-21 |
| Objective | Authentication failures and short circuit. |
| Source Function or Endpoint | AuthService.authenticate_user |
| Preconditions | Mock repository and security collaborators. |
| Test Data | Unknown username; known user with verifier=False. |
| Test Steps | Authenticate each case; inspect verifier/token calls. |
| Expected Result | Returns None; missing user never invokes verifier; neither case issues token. No token or password material recorded as evidence. |
| Actual Result | 2 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_auth.py](../../../tests/unit/test_auth.py), functions prefixed `test_UT_21_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-22 — Cookie token resolution and admin role

| Field | Specification |
|---|---|
| Test ID | UT-22 |
| Objective | Cookie token resolution and admin role. |
| Source Function or Endpoint | get_current_user; is_admin_dep in app.dependencies.auth |
| Preconditions | Synthetic Request, mocked jwt.decode/settings/UserRepository; async invocation. |
| Test Data | Missing cookie; decoder InvalidTokenError; nonexistent subject user; valid S1; valid A1. |
| Test Steps | Call current-user resolver per variant; call admin guard with resolved S1 and A1. |
| Expected Result | Missing/invalid/unresolved -> HTTPException 401; valid user returned from repository; guard denies regular_user with 403 and returns admin. The original 401 expectation is superseded by the current require_roles contract (see execution addendum). HTTP handler behavior tested separately in IT-12/13. |
| Actual Result | 5 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_auth.py](../../../tests/unit/test_auth.py), functions prefixed `test_UT_22_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

### UT-23 — Password hash and JWT utility contracts

| Field | Specification |
|---|---|
| Test ID | UT-23 |
| Objective | Password hash and JWT utility contracts. |
| Source Function or Endpoint | encrypt_password; verify_password; create_access_token |
| Preconditions | No DB; actual local hash/JWT utilities, fixed test settings and controlled clock. |
| Test Data | Test-only password; correct/wrong password; claims sub=S1,role=regular_user; explicit 5-minute lifetime. |
| Test Steps | Hash/verify locally; create token at fixed UTC time and decode with test key; compare input claims after call. |
| Expected Result | Hash differs from plaintext; correct verifies true, wrong false; signed token carries sub/role and exp at fixed time +5 minutes; input dict not mutated. Patch time/settings only, not functions under test. |
| Actual Result | 2 variants passed on 26 October 2026; see retained per-variant output and JUnit results. |
| Status | Passed |
| Evidence Reference | Implementation: [tests/unit/test_auth.py](../../../tests/unit/test_auth.py), functions prefixed `test_UT_23_`. Execution: [verbose output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml), [run details](../evidence/unit/README.md). |

## Execution, evidence and completion criteria

Executed on 26 October 2026 from the repository root with:

```text
python -m pytest -m unit -v -p no:cacheprovider --junitxml=docs/assignment2/evidence/unit/results.xml
```

Actual result: **113 passed, 408 deselected, 1 warning in 1.98s** (exit code 0). All UT-01 through UT-23 planned variants passed. The selected set contains 112 new isolated variants plus the preserved E12 direct mocked login test, now marked `unit` as a UT-20 companion. No integration tests were executed or implemented by this task. Existing database, HTTP, presentation and migration coverage is preserved.

Implementation: [advising unit tests](../../../tests/unit/test_advising.py), [auth unit tests](../../../tests/unit/test_auth.py), [shared isolated fixtures](../../../tests/unit/conftest.py), [retained login test](../../../tests/test_login_routing.py). `pyproject.toml` registers the unit marker and scopes default discovery to root `tests/`, excluding the nested historical checkout. `-p no:cacheprovider` avoids the existing inaccessible `.pytest_cache` directory.

Repository constructors are patched at their service import location using autospecced doubles and a nonfunctional session sentinel. Models exist only in memory. Unit fixtures reject SQLAlchemy database connections; no production database or HTTP server is required. Mutations are asserted as delegation only, including no mutation on validation failures. Real password hashing and JWT signing run locally with test data, a test signing key and a fixed token clock.

Plan reconciliation: UT-22's original student/admin-denial expectation was 401; the current `is_admin_dep = require_roles("admin")` explicitly returns 403 for an authenticated regular user. The test asserts 403 and also verifies that a forged admin role claim cannot override the repository role. Missing/invalid/unresolved identities still assert 401. This is a documented source-contract update, not a newly introduced application fix. The historical H3 handler concern is outside this unit execution and was not reassessed through HTTP.

No genuine business defects were exposed by these tests; no application code was modified. The single warning is the existing FastAPI/Starlette TestClient deprecation emitted during test-module collection. It did not fail any test or execute the deselected HTTP cases.

Evidence: [run details and versions](../evidence/unit/README.md), [verbose per-variant output](../evidence/unit/pytest-output.txt), [JUnit results](../evidence/unit/results.xml). These shared artifacts replace the original uncreated individual `UT-xx.md` placeholders. Each case above links its implementation and actual execution evidence. All unit exit criteria are met; actual persistence, HTTP parsing/cookies and integration authorization remain outside this run.

## Plan review

Reviewed against the root tests and named source functions. All 23 cases contain all ten requested fields; requirement IDs map to both plans; database-backed tests are identified as such; empty/duplicate selection, raw feedback boundary and real credential logic are distinguished from adjacent existing coverage. Unit implementation and execution evidence are now linked above. No application edits, report export or integration execution were performed in this unit implementation task.

## Test reporting reconciliation - 26 October 2026

Latest student-verified pytest results: **113 unit passed, 602 deselected, 1 warning; 194 integration passed, 521 deselected, 1 warning; 715 full-suite passed, 1 warning**. Each marked run collected 715 items. Historical run counts and case records above retain their original provenance; they are not latest raw exports. Six supplied screenshots were visually inspected: three in `../screenshots/Unit/` and three in `../screenshots/Integration/`, captured on 26 October 2026. They confirm actual commands, environment, warning and summaries: unit 6.23s; integration 30.52s. Complete latest raw output remains missing; both reports link and embed the actual screenshots. See the [unit report](../reports/unit-test-report.md) and [integration report](../reports/integration-test-report.md) for commands, environments and limitations.

The updated matrix preserves R01-R14 and adds cross-method mappings with actual evidence dispositions. UT group passes are supported by earlier retained output/JUnit and latest aggregate/partial-node screenshots; IT marker mappings, latest aggregate and partial-node screenshots do not provide a complete latest per-variant log. Postman request numbers identify the 90 executed requests in the verified 27 October run (470 successful assertions, zero assertion failures/errors); see the current report and screenshots. UAT mappings identify workflow coverage, **not executed passes**; API-only invalid inputs and direct database cases have no browser equivalent. See [Postman report](../reports/postman-test-report.md) and [final UAT report](../reports/uat-final-report.md).

R15, added in the [Workflow 1 API evidence](../evidence/workflow1-api.md), concerns validated public JSON contracts, allowlists and OpenAPI. Its concrete API-07/08 function mappings remain in that evidence and are outside the original UT/IT group numbering. Postman response-contract assertions include executed requests 18-20, 32 and 52; the current Runner report records 470 successful assertions overall. UAT has no direct schema/OpenAPI case. No additional UT, IT or UAT execution is invented for R15.

Current saved UAT evidence is **0 Pass / 0 Fail / 20 Not Run**. Postman Runner evidence now records 90 requests, 470 successful assertions, zero assertion failures/errors, one iteration on 27 October 2026. UAT has seven partially evidenced cases; full case outcomes remain unverified. Historical H3 is superseded by retained Student/Workflow 1 evidence verifying 401; this does not establish manual or Postman execution. The reports distinguish missing evidence from a product defect and make no overall acceptance claim.


Reporting reconciliation — 27 October 2026: [WF1–WF3 traceability and verified evidence](../reports/requirements-test-traceability.md) is the current workflow-level matrix; [inventory](../reports/evidence-inventory.md) lists inspected files. UAT Not Run means complete execution/result unverified, including partially evidenced cases. Earlier dated execution records retain their historical provenance.

## Current execution reconciliation ? 27 October 2026

The original planned inputs, expected results and preparation-stage summaries above are historical and preserved. Current authoritative [UAT execution](../reports/uat-execution.md) records **1 Pass / 0 Fail / 19 Not Run** (18 partially verified, one unverified workflow), using all 19 actual screenshots and explicit user observations. Tester Cameron Ramesar confirms October 27, 2026 execution. Actual A initial/revised data is 3 courses/9 credits, not the planned 2/6; exact substitutions, remaining substeps and acceptance issues are in the [matrix](../reports/uat-evidence-review.md). Automated outcomes remain 113 unit, 194 integration and 715 full-suite passes; Postman 90 requests/470 assertions passed.
