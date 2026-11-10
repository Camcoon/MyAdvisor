# MyAdvisor — Integration Test Plan

> **Approved-allocation update ? 27 October 2026:** [Current correction record](../reports/degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.

## Supplement: approved seed and safe existing-database migration

`tests/integration/test_demo_requirement_migration.py` adds 13 variants: in-place migration while preserving every non-requirement table across five plan statuses; four custom/unknown-data rejection variants with no writes; fresh idempotent demo seed and real authenticated progress/catalogue/HTML; SQLite WAL backup and missing-source protection; actual file-backed migration with retained backup/history; backup failure preventing application. The approved category mapping is 36/18/12/18/9 = 93. The seeded result must be 6/3/84/93 and 6%, with exact category percentages 8/17/0/0/0. Existing fixture programmes with Core=30 remain independent synthetic tests. The actual complete run has 751 passes including 227 integration members; no new separate marked-integration screenshot or PostgreSQL execution is claimed.



**Correction-stage supplement ? 27 October 2026:** original IDs, inputs and expected outcomes below are retained. [Additional correction coverage](../reports/requirements-test-traceability.md) documents focused HTML role, actual-engine integrity, registration and contrast regressions. [Actual corrected-build results](../reports/audit-correction-report.md) are separate from historical marked/manual runs. [Required browser/API retests](../reports/correction-retest-guide.md) remain pending; no expected outcome has been promoted to an observation. F05 curriculum values are unchanged pending owner approval.

**Prompt 15 current disposition (27 October 2026):** historical planning/execution entries below are retained. Current implementation, evidence limitations and open defects are assessed in the [final quality audit](../final-quality-audit.md); the [official Assignment 2 source record](../official-assignment-brief.md) supplies the rubric. No original test-case expected outcome was changed.

Student implementation addendum (26 October 2026): the student portions of IT-01–04, IT-06–12, IT-14–15 and IT-18 are implemented with real login, FastAPI TestClient and per-case isolated SQLModel databases. Final execution: **59 passed, 1 warning in 4.62s**. See [student scope, IT traceability and retained results](../evidence/student-integration.md). Advisor transitions/queue assertions and repository-only cases are excluded from this new suite; the original specifications and historical statuses below are retained.

Implementation addendum (26 October 2026): Workflow 1 and catalogue JSON API tests are now implemented and executed. See [API-01–API-08 traceability and results](../evidence/workflow1-api.md), mapping R01/R02/R11/R12 and the new R15 response-contract requirement to concrete test functions. This addendum records 95 passing tests (24 new API cases); original case statuses below remain historical planning records. H3 is superseded by the verified JSON/HTML 401 behavior described in the evidence. API submission and advisor decisions remain outside this implementation.

Prepared: 26 October 2026. Version: 1.0. Execution state: **Not Run**.

## Basis and scope limitation

The request refers to a completed MyAdvisor repository audit, but no saved audit document was located in the accessible workspace. This plan therefore uses the current root repository, [existing report](../../report.md) and inspected tests as its verifiable basis; no audit findings or previous run outcomes are invented. If a separate audit becomes available, reconcile its requirement IDs and findings before execution. These are test specifications only: no tests or application code are implemented or executed by this task.

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

## Objective and integration boundary

Exercise real FastAPI routing, form/JSON parsing, cookie authentication, role dependencies, services, repositories and SQLModel persistence using an isolated database. Use the real application/router/middleware stack and real password hashing/JWT for HTTP cases. Do not override get_current_user, is_admin_dep, AuthService, AdvisingService or repository CRUD: that would conceal the interaction being tested. IT-19/20 are intentionally repository/database integration cases for constraint/rollback paths the service rejects before SQL.

## F2 — isolated SQLModel environment and data

Use a fresh `sqlite://` engine per independent test variant with StaticPool and `check_same_thread=False`. Import all model modules, enable SQLite `PRAGMA foreign_keys=ON` on every connection, and create SQLModel metadata. Use deterministic F1-equivalent data, **not** existing `database.db`, deployment data or demo accounts:

- S1 and S2: distinct usernames/emails/student numbers, role regular_user; A1: role admin. Store real test-password hashes and login via POST /login with separate cookie jars for each actor.
- Computer Science program: 93 credits; Core Courses requirement: 30 credits.
- C1: COMP 1100, Core, 3 credits, no prerequisite; C2: MATH 1000, General Education, 3 credits, no prerequisite; C3: COMP 2000, Core, 3 credits, prerequisite COMP 1100; C4: MATH 2000, Electives, 3 credits, no prerequisite; C5: COMP 3000, Electives, 3 credits, prerequisites COMP 1100 and MATH 9999.
- S1 has C1 Completed/A and C2 In Progress; C3/C4 eligible and untracked; C5 blocked. Seed distinctive S2-only activity/message data for privacy assertions. Resolve generated IDs from fixture objects; symbolic C1–C5/S1/S2/A1 names below represent those IDs.
- T1=`Year 1 semester 1`, T2=`Year 1 semester 2`. Independent variants reset their own plan histories and fixture state. Setup may insert plan statuses directly when the transition is not itself under test.

Override the exact `app.database.get_session` callable used by SessionDep, yielding a **new Session on the test engine for each request**. Close it after each request. Fresh-session assertions verify commits instead of relying on shared identity-map objects. Configure test-only settings/key, local HTTP cookie behavior and database URI before importing app/database; never print secrets.

Isolation must cover startup and database recovery too: `app.main.lifespan` calls ensure_db_and_tables/get_cli_session, and recovery middleware may initialize the configured engine. A request dependency override alone does not isolate those paths. Before starting a context-managed TestClient, rebind `app.database.engine` to the isolated engine and arrange test-only startup without demo seeding (replace only `app.main.lifespan`'s ensure_db_and_tables/get_cli_session initialization collaborators or provide a no-seed test lifespan). Keep actual request handlers, authentication and persistence real. With a test lifespan, recovery must still reference the isolated engine. Never enter the production initializer against the workspace/deployed database. Record the selected fixture approach when later implementing.

Use TestClient with follow_redirects=False, then follow only the intended Location to inspect flash/HTML. Send list-valued form course_ids as repeated form keys. Send malformed JSON as raw content. On teardown close clients/sessions, restore all overrides/settings/engine/lifespan changes in finally, and dispose the test engine. SQLite does not prove PostgreSQL-specific behavior or concurrent duplicate-plan prevention; those are outside these plans.

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

## HTTP response and persistence oracles

- Successful HTML mutations return 303 to the named page; business rejections also return 303 but with warning flashes and unchanged DB. Check message/state, not the redirect status alone.
- Framework type/path validation returns 422; malformed advisor JSON returns 400; invalid review object/field types return 422.
- Authorization follows H3 above: record the dependency's 401 intent and the current HTML/200 response separately. Denial requires no protected content and no writes.
- Snapshot relevant plan rows, links, advisor/feedback/status/timestamps before negative operations and compare in a newly opened Session afterward. A rejected mixed selection must not leave a partially inserted plan.
- Course selection before submission is browser-side behavior. HTTP tests verify catalogue eligibility and posted selections; they do not claim to exercise JavaScript selection controls.

## Integration test cases

Each listed variant is independent unless a case explicitly describes a lifecycle sequence. “Logged in” means real login/cookie setup, not dependency replacement. Evidence must identify each parameterized variant.

### IT-01 — Real login, cookie and logout

| Field | Specification |
|---|---|
| Test ID | IT-01 |
| Objective | Real login, cookie and logout. |
| Source Function or Endpoint | POST /login; GET /app; GET /logout |
| Preconditions | F2 database, separate unauthenticated client, real hash/JWT/auth dependencies. |
| Test Data | S1 correct password; wrong password; unknown username. |
| Test Steps | POST form credentials for each variant; capture cookie/redirect; with successful client GET /app; GET /logout then protected GET. |
| Expected Result | Success ->303 /app and access_token cookie, authenticated page 200; wrong/unknown ->303 /login, Incorrect username or password flash, no new access_token on clean client; logout ->303 /login, cookie removed, protected access denied under H3. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R12; E12 redirect-only baseline. Planned execution artifact: `../evidence/IT-01.md` (not yet created). |

### IT-02 — Student degree progress through HTTP

| Field | Specification |
|---|---|
| Test ID | IT-02 |
| Objective | Student degree progress through HTTP. |
| Source Function or Endpoint | GET /app?tab=degree-progress&semester=T1 |
| Preconditions | F2; login S1 using IT-01 setup. |
| Test Data | C1 Completed=3; C2 In Progress=3; 93-credit program; Core required=30; S2 distinct records. |
| Test Steps | GET page; inspect rendered totals and category; query records in fresh session. |
| Expected Result | 200; completed=3, in-progress=3, remaining=87, overall=3%; Core earned=3/30 and remaining=27; no S2 activity or profile; no database mutation. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R01,R11; E01 service baseline. Planned execution artifact: `../evidence/IT-02.md` (not yet created). |

### IT-03 — Eligible selection, submission and advisor queue

| Field | Specification |
|---|---|
| Test ID | IT-03 |
| Objective | Eligible selection, submission and advisor queue. |
| Source Function or Endpoint | GET /app?tab=plan-courses; POST /app/plan; GET /admin |
| Preconditions | F2; S1 and A1 authenticated in separate clients; no T1 plan. |
| Test Data | Repeated form course_ids=C3 and C4; semester_name=T1. |
| Test Steps | GET catalogue; inspect eligible/disabled options; POST form selection; follow redirect manually; GET /admin as A1; query saved plan/links. |
| Expected Result | Catalogue eligibility reflects completed C1 and in-progress C2; POST ->303 with semester and tab=plan-courses; success flash; exactly one Pending S1/T1 plan, two unique links, submitted_at set, advisor_id=None; appears in real advisor queue. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R02,R04,R05,R13; E05 partial. Planned execution artifact: `../evidence/IT-03.md` (not yet created). |

### IT-04 — Persistence across requests and sessions

| Field | Specification |
|---|---|
| Test ID | IT-04 |
| Objective | Persistence across requests and sessions. |
| Source Function or Endpoint | POST /app/plan; GET /app; AdvisingRepository.get_plan_for_student/get_plan_courses |
| Preconditions | F2; S1 authenticated; no T1 plan. |
| Test Data | [C3,C4],T1. |
| Test Steps | Submit through HTTP; close request-scoped session; open a fresh Session on same isolated engine; read plan/links; issue another GET. |
| Expected Result | Committed plan ID, S1, T1, Pending and both links survive session boundaries and render as selected; no reliance on Python object identity. E02/E09 do not prove full authenticated request chain. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R13; E02,E09 partial. Planned execution artifact: `../evidence/IT-04.md` (not yet created). |

### IT-05 — Advisor approval and rejection

| Field | Specification |
|---|---|
| Test ID | IT-05 |
| Objective | Advisor approval and rejection. |
| Source Function or Endpoint | POST /admin/review/{plan_id}; GET /admin; GET /app?tab=messages |
| Preconditions | F2; seed a separate Pending S1 plan for each decision; S1 and A1 logged in. |
| Test Data | approve with ''; reject with 'Please choose another course.'; JSON and form variants. |
| Test Steps | A1 POST each review; inspect redirect/flash; read row in fresh session; GET advisor queue and student messages. |
| Expected Result | 303 /admin; matching success flash; Approved or Rejected stored with A1 and stripped feedback; reviewed plan leaves Pending queue; student sees own decision/message; plan course links preserved. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R06,R07,R13; E02,E04 partial. Planned execution artifact: `../evidence/IT-05.md` (not yet created). |

### IT-06 — Request changes and resubmit

| Field | Specification |
|---|---|
| Test ID | IT-06 |
| Objective | Request changes and resubmit. |
| Source Function or Endpoint | POST /admin/review/{id}; POST /app/plan; GET /app and /admin |
| Preconditions | F2; Pending S1/T1 plan containing C3, A1/S1 authenticated. |
| Test Data | request_changes, feedback='  Choose another course.  '; replacement=[C4]. |
| Test Steps | A1 request changes through HTTP; verify persisted status/student message; S1 submit replacement for same semester; query fresh session and advisor queue. |
| Expected Result | Changes Requested, A1, trimmed feedback initially; resubmission ->303; same plan ID becomes Pending; links exactly [C4]; old C3 link removed; advisor_id=None, feedback=''; submitted_at refreshed; returns to Pending queue. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R06,R08,R13; extend E02/E04 with real auth. Planned execution artifact: `../evidence/IT-06.md` (not yet created). |

### IT-07 — Rejected plan resubmission without cancellation

| Field | Specification |
|---|---|
| Test ID | IT-07 |
| Objective | Rejected plan resubmission without cancellation. |
| Source Function or Endpoint | POST /admin/review/{id}; POST /app/plan |
| Preconditions | F2; S1/A1 authenticated; S1 Pending T1 plan containing C3. |
| Test Data | reject with feedback; replacement=[C4]. |
| Test Steps | Reject via HTTP; submit C4 for same semester without cancel; read fresh-session plan and links. |
| Expected Result | 303 for both requests; same ID reset to Pending; C4 replaces C3; feedback and advisor cleared; timestamp refreshed. Distinct from E10 cancellation/new-ID behavior. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R05,R08,R13; E10 adjacent. Planned execution artifact: `../evidence/IT-07.md` (not yet created). |

### IT-08 — Allowed cancellation and replacement

| Field | Specification |
|---|---|
| Test ID | IT-08 |
| Objective | Allowed cancellation and replacement. |
| Source Function or Endpoint | POST /app/plan/{id}/cancel; POST /app/plan; GET /admin and /app |
| Preconditions | F2; independently owned Pending, Approved and Rejected plans; S1 logged in. |
| Test Data | Each allowed status with existing [C3] links; replacement [C4], same semester. |
| Test Steps | Cancel per variant; inspect row, links, UI and advisor queue; submit replacement; query all matching plan rows. |
| Expected Result | 303; original row Cancelled and retains links/history; hidden from Pending queue; cancelled plan displays no selected/planned courses; replacement has new ID and Pending status, old Cancelled row remains. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R09,R13; extend E09/E10 through HTTP. Planned execution artifact: `../evidence/IT-08.md` (not yet created). |

### IT-09 — Forbidden cancellation statuses

| Field | Specification |
|---|---|
| Test ID | IT-09 |
| Objective | Forbidden cancellation statuses. |
| Source Function or Endpoint | POST /app/plan/{id}/cancel |
| Preconditions | F2; S1 authenticated; independently owned Changes Requested and Cancelled plans. |
| Test Data | Each disallowed status; unchanged links/feedback snapshots. |
| Test Steps | POST cancel per variant; follow redirect for warning; query fresh state. |
| Expected Result | 303 tab=plan-courses with 'Only pending, rejected, or approved plans can be cancelled.' warning; status, links and feedback unchanged. Changes Requested permits resubmission, not cancellation. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R09; gap. Planned execution artifact: `../evidence/IT-09.md` (not yet created). |

### IT-10 — Submitted course removal and last-course rule

| Field | Specification |
|---|---|
| Test ID | IT-10 |
| Objective | Submitted course removal and last-course rule. |
| Source Function or Endpoint | POST /app/plan/{id}/courses/{course_id}/remove |
| Preconditions | F2; S1 authenticated, owned Pending plan [C3,C4]; separate non-Pending variants. |
| Test Data | C4 then C3; absent course ID; each Approved/Rejected/Changes Requested/Cancelled. |
| Test Steps | Remove C4; try last C3; test absent and non-Pending variants independently; query DB after each. |
| Expected Result | First request 303/success, one C3 link remains; last-course, absent-course and non-Pending requests 303/warning without state change; no orphaned/deleted plan. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R10,R13; extend E09. Planned execution artifact: `../evidence/IT-10.md` (not yet created). |

### IT-11 — Cross-student ownership and data visibility

| Field | Specification |
|---|---|
| Test ID | IT-11 |
| Objective | Cross-student ownership and data visibility. |
| Source Function or Endpoint | GET /app?tab=degree-progress; GET /app?tab=messages; POST /app/plan/{id}/cancel; POST /app/plan/{id}/courses/{course_id}/remove; POST /app/plan |
| Preconditions | F2; S1 and S2 logged in separately; S2 owns Pending [C3,C4] and distinctive records/feedback. |
| Test Data | S1 uses S2 plan ID for cancel/remove; submits valid own selection with extra student_id=S2 field. |
| Test Steps | S1 GET dashboard/messages; POST foreign cancel/remove; POST own plan with forged student_id field; compare DB before/after. |
| Expected Result | Foreign operations ->303 warning 'Plan not found.' with S2 row/links untouched; no S2 private record/message in S1 output; new submission belongs to cookie-authenticated S1, extra form student_id does not override identity. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R11,R13; E09 only service ownership. Planned execution artifact: `../evidence/IT-11.md` (not yet created). |

### IT-12 — Unauthenticated and invalid-token access

| Field | Specification |
|---|---|
| Test ID | IT-12 |
| Objective | Unauthenticated and invalid-token access. |
| Source Function or Endpoint | GET /app; GET /admin; POST /app/plan; POST /admin/review/{id}; POST /app/plan/{id}/cancel; POST /app/plan/{id}/courses/{course_id}/remove |
| Preconditions | F2; valid target plan; clean client per token variant; no auth override. |
| Test Data | No cookie; malformed token; expired correctly signed token; wrong-signature token; valid token for nonexistent user. |
| Test Steps | Send each protected request with otherwise valid payload under each variant; compare entire relevant DB state. |
| Expected Result | Access denied, no private student/advisor data and no writes. Dependencies raise 401; current application handler returns denial HTML with HTTP 200 (H3). Record HTTP status mismatch as a known contract issue, never count 200 alone as authorization success. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R11,R12; gap. Planned execution artifact: `../evidence/IT-12.md` (not yet created). |

### IT-13 — Student cannot use advisor operations

| Field | Specification |
|---|---|
| Test ID | IT-13 |
| Objective | Student cannot use advisor operations. |
| Source Function or Endpoint | GET /admin; POST /admin/review/{id} |
| Preconditions | F2; S1 logged in; Pending S2 plan. |
| Test Data | Valid approve/reject/request_changes payloads as regular_user. |
| Test Steps | GET queue; POST each decision; query plan in fresh session. |
| Expected Result | Role guard denies access; no advisor queue/private data; no status/feedback/advisor/link changes; denial page currently HTTP 200 under H3 (dependency raises 401). |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R06,R11; E04 overrides guard. Planned execution artifact: `../evidence/IT-13.md` (not yet created). |

### IT-14 — Business-invalid submission inputs

| Field | Specification |
|---|---|
| Test ID | IT-14 |
| Objective | Business-invalid submission inputs. |
| Source Function or Endpoint | POST /app/plan |
| Preconditions | F2; S1 logged in; no plan for target semester; reset DB per variant. |
| Test Data | Omitted/empty course_ids; [C3,C3]; [999999]; [C1] completed; [C2] in progress; unmet prerequisite C5; invalid/blank semester; valid C3 plus invalid item. |
| Test Steps | POST form per variant; capture redirect; GET warning; compare SemesterPlan/PlanCourse counts. |
| Expected Result | 303 warning for each business rejection, no partial plan/links. Messages identify empty/duplicate/missing/ineligible selections or invalid semester. Whitespace around a valid semester is accepted and stored trimmed (positive control). |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R02,R03,R04,R14; E05,E07,E08 partial. Planned execution artifact: `../evidence/IT-14.md` (not yet created). |

### IT-15 — Duplicate active semester plan

| Field | Specification |
|---|---|
| Test ID | IT-15 |
| Objective | Duplicate active semester plan. |
| Source Function or Endpoint | POST /app/plan |
| Preconditions | F2; S1 logged in; owned T1 plan separately Pending or Approved. |
| Test Data | Same-semester [C4]; second positive control uses T2. |
| Test Steps | POST duplicate; snapshot row/links; then submit to T2. |
| Expected Result | Pending/Approved duplicate ->303 warning already under review or approved; original plan/links unchanged, no extra T1 plan; independent T2 submission accepted. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R05,R13; extend E05. Planned execution artifact: `../evidence/IT-15.md` (not yet created). |

### IT-16 — Invalid review payload shapes and syntax

| Field | Specification |
|---|---|
| Test ID | IT-16 |
| Objective | Invalid review payload shapes and syntax. |
| Source Function or Endpoint | POST /admin/review/{id} |
| Preconditions | F2; A1 logged in, Pending plan; reset per variant. |
| Test Data | Malformed JSON '{'; JSON [] or null; {}; decision='' or integer; feedback=null/list/integer; noninteger plan path ID; valid form control. |
| Test Steps | POST with accurate Content-Type per variant; capture raw response; compare persisted snapshot. |
| Expected Result | Malformed JSON ->400; non-object/missing-or-invalid decision/non-string feedback/noninteger path ->422; no state changes; valid form decision with string feedback ->303 and normal review. JSON syntax checks must send raw malformed bytes, not client JSON serialization. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R14; E03/E04 happy path only. Planned execution artifact: `../evidence/IT-16.md` (not yet created). |

### IT-17 — Review business validation and feedback boundary

| Field | Specification |
|---|---|
| Test ID | IT-17 |
| Objective | Review business validation and feedback boundary. |
| Source Function or Endpoint | POST /admin/review/{id} |
| Preconditions | F2; A1 authenticated; independent Pending/non-Pending/missing plan cases. |
| Test Data | Unknown decision; feedback lengths 0,499,500,501; 501 spaces; non-Pending statuses; missing integer ID. |
| Test Steps | POST JSON and form boundary variants; follow redirect for flash; query fresh state. |
| Expected Result | Business-invalid cases ->303 /admin warning, unchanged DB; valid 0/499/500 feedback accepted and trimmed; 501 rejected before trimming. Missing plan says Plan not found; non-Pending says Only pending plans can be reviewed. No invented mandatory-feedback rule. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R05,R06,R07,R14; gap. Planned execution artifact: `../evidence/IT-17.md` (not yet created). |

### IT-18 — Invalid form types and path identifiers

| Field | Specification |
|---|---|
| Test ID | IT-18 |
| Objective | Invalid form types and path identifiers. |
| Source Function or Endpoint | POST /app/plan; POST /app/plan/{id}/cancel; POST /app/plan/{id}/courses/{course_id}/remove |
| Preconditions | F2; S1 logged in, owned Pending [C3,C4]. |
| Test Data | course_ids='abc' or mixed [C3,'abc']; plan_id='abc'; course_id='abc'; missing integer plan ID 999999; missing course membership. |
| Test Steps | Send repeated form fields or path variants; capture validation response and DB snapshot. |
| Expected Result | Noninteger form/path IDs ->422 before service mutation; nonexistent integer plan or absent plan course ->303 warning; plan and links unchanged. Student submission endpoint expects form data; do not assume a JSON REST contract. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R10,R14; gap. Planned execution artifact: `../evidence/IT-18.md` (not yet created). |

### IT-19 — Database uniqueness constraints

| Field | Specification |
|---|---|
| Test ID | IT-19 |
| Objective | Database uniqueness constraints. |
| Source Function or Endpoint | PlanCourse and StudentCourse SQLModel tables; AdvisingRepository.create_plan |
| Preconditions | F2 fresh engine with foreign keys enabled; seed referenced users/courses and valid Pending plan. |
| Test Data | Duplicate (plan_id,C3); duplicate (S1,C1); invalid foreign-key link. |
| Test Steps | Use isolated repository/session boundary to insert each invalid row; catch IntegrityError; rollback; open fresh session. |
| Expected Result | Real database rejects duplicate pairs and dangling foreign key; committed valid rows remain intact. This is a DB integration case rather than HTTP; UT-10 covers the earlier service guard. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R04,R13; model constraints, no matching existing test. Planned execution artifact: `../evidence/IT-19.md` (not yet created). |

### IT-20 — Create/resubmit transaction rollback

| Field | Specification |
|---|---|
| Test ID | IT-20 |
| Objective | Create/resubmit transaction rollback. |
| Source Function or Endpoint | AdvisingRepository.create_plan; resubmit_plan |
| Preconditions | F2 real isolated DB; existing Rejected plan [C3] for resubmit case. |
| Test Data | Create with [C4,C4]; resubmit existing plan with [C4,C4] to trigger real unique-constraint failure. |
| Test Steps | Invoke repository directly to reach DB failure past service duplicate guard; catch IntegrityError; inspect a fresh session after rollback. |
| Expected Result | Failed create leaves no new plan or links; failed resubmit preserves original status/feedback/advisor/timestamp/C3 links; session usable after rollback. Keep actual DB/CRUD real; do not mock commit. Normal route persistence remains covered by IT-03/04/06. |
| Actual Result | Not Run — no execution evidence recorded. |
| Status | Not Run |
| Evidence Reference | Source/coverage: R08,R13; gap. Planned execution artifact: `../evidence/IT-20.md` (not yet created). |

## Execution, evidence and completion criteria

No tests are run or implemented in this task. Later execution should first reuse the fixture and matching existing nodes above, extending them only for missing route/authentication/session boundaries. Run pytest from the root against the actual integration node IDs introduced later; do not silently run the nested checkout or infer real-auth coverage from E04.

For each planned `../evidence/IT-xx.md`, retain commit SHA, execution date/time, environment/database type, pytest command/node IDs, input variant, HTTP status and sanitized body/Location/flash, and before/after fresh-session DB assertions. Link raw output and defect records when relevant. Redact access tokens, hashes and passwords. No evidence files exist by virtue of this plan; every Actual Result and Status remains Not Run until actual execution is recorded.

Entry: isolated startup/recovery/session setup verified by fixture design, schema/data loaded, actor login setup available, known H3 interpretation agreed. Exit: all variants executed with evidence and requirement links, negative cases prove unchanged state, cleanup completed, failures/known issues dispositioned explicitly. A known source issue is not a passed execution; any requirement for 401/403 must be evaluated separately from denial enforcement.

## Plan review

Reviewed against current routes, dependencies, services, repository transactions, model constraints and existing tests. All 20 cases contain all ten requested fields. HTTP cases retain real authentication and persistence; IT-19/20 intentionally isolate database constraints/rollback. Status transitions, cross-student denial and invalid inputs have explicit response and database oracles. Test implementation, application changes, deployment and report export remain outside this task.

## Test reporting reconciliation - 26 October 2026

Latest student-verified pytest results: **113 unit passed, 602 deselected, 1 warning; 194 integration passed, 521 deselected, 1 warning; 715 full-suite passed, 1 warning**. Each marked run collected 715 items. Historical run counts and case records above retain their original provenance; they are not latest raw exports. Six supplied screenshots were visually inspected: three in `../screenshots/Unit/` and three in `../screenshots/Integration/`, captured on 26 October 2026. They confirm actual commands, environment, warning and summaries: unit 6.23s; integration 30.52s. Complete latest raw output remains missing; both reports link and embed the actual screenshots. See the [unit report](../reports/unit-test-report.md) and [integration report](../reports/integration-test-report.md) for commands, environments and limitations.

The updated matrix preserves R01-R14 and adds cross-method mappings with actual evidence dispositions. UT group passes are supported by earlier retained output/JUnit and latest aggregate/partial-node screenshots; IT marker mappings, latest aggregate and partial-node screenshots do not provide a complete latest per-variant log. Postman request numbers identify the 90 executed requests in the verified 27 October run (470 successful assertions, zero assertion failures/errors); see the current report and screenshots. UAT mappings identify workflow coverage, **not executed passes**; API-only invalid inputs and direct database cases have no browser equivalent. See [Postman report](../reports/postman-test-report.md) and [final UAT report](../reports/uat-final-report.md).

R15, added in the [Workflow 1 API evidence](../evidence/workflow1-api.md), concerns validated public JSON contracts, allowlists and OpenAPI. Its concrete API-07/08 function mappings remain in that evidence and are outside the original UT/IT group numbering. Postman response-contract assertions include executed requests 18-20, 32 and 52; the current Runner report records 470 successful assertions overall. UAT has no direct schema/OpenAPI case. No additional UT, IT or UAT execution is invented for R15.

Current saved UAT evidence is **0 Pass / 0 Fail / 20 Not Run**. Postman Runner evidence now records 90 requests, 470 successful assertions, zero assertion failures/errors, one iteration on 27 October 2026. UAT has seven partially evidenced cases; full case outcomes remain unverified. Historical H3 is superseded by retained Student/Workflow 1 evidence verifying 401; this does not establish manual or Postman execution. The reports distinguish missing evidence from a product defect and make no overall acceptance claim.


Reporting reconciliation — 27 October 2026: [WF1–WF3 traceability and verified evidence](../reports/requirements-test-traceability.md) is the current workflow-level matrix; [inventory](../reports/evidence-inventory.md) lists inspected files. UAT Not Run means complete execution/result unverified, including partially evidenced cases. Earlier dated execution records retain their historical provenance.

## Current execution reconciliation ? 27 October 2026

The original planned inputs, expected results and preparation-stage summaries above are historical and preserved. Current authoritative [UAT execution](../reports/uat-execution.md) records **1 Pass / 0 Fail / 19 Not Run** (18 partially verified, one unverified workflow), using all 19 actual screenshots and explicit user observations. Tester Cameron Ramesar confirms October 27, 2026 execution. Actual A initial/revised data is 3 courses/9 credits, not the planned 2/6; exact substitutions, remaining substeps and acceptance issues are in the [matrix](../reports/uat-evidence-review.md). Automated outcomes remain 113 unit, 194 integration and 715 full-suite passes; Postman 90 requests/470 assertions passed.
