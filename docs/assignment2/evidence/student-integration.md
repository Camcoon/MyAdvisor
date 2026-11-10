# Student integration suite execution

Client execution date: 26 October 2026. Baseline commit: `679b9250c13f38a2f97ed4e6d08a325fe48219d3`, with existing working-tree application changes. This evidence describes the new student suite only.

From the application root (the directory containing `pyproject.toml`):

```powershell
python -m pytest tests/integration/test_student_workflow.py -m integration -v -p no:cacheprovider
```

Final actual result: **59 passed, 1 warning in 4.62s**, exit code **0**. The initial run also passed all 59 cases in 4.56s. [Retained final verbose pytest output](student-integration-pytest.txt) identifies every executed variant. Scoped `python -m ruff check tests/integration` also passed.

Environment: Windows, Python 3.14.0, pytest 9.1.1, FastAPI 0.141.1, SQLModel 0.0.42; SQLite in memory with foreign keys enabled. The warning is the installed Starlette TestClient's deprecation of its httpx transport. Dependencies and application code were unchanged by this task.

## Isolation and assertions

[Fixtures](../../../tests/integration/conftest.py) provide a fresh `sqlite://` SQLModel engine for every parameterized case, using StaticPool and `check_same_thread=False`. Generated identifiers come from deterministic F2 seed objects. SQLite foreign keys are enabled on connection. Each test starts without plans or plan-course links. The seed contains S1/S2, an advisor used only for persisted review metadata, a 93-credit program, a 30-credit Core requirement, C1–C5, and distinct S2 activity.

Test-only environment and cached settings are installed before fixture-controlled app imports. A guard on both `Engine.connect` and `Engine.raw_connection` rejects every engine except the current isolated engine before it can open a connection. The application engine is rebound too, covering recovery and CLI session access. Context-managed TestClients enter a no-seed test lifespan; production/demo initialization is never entered. An unused bootstrap SQLite filename is asserted absent.

Only the exact `database.get_session` dependency is overridden, yielding a new real Session per request. Authentication, hashing/JWT, routes, middleware, services and repositories remain real. Students authenticate through `/login`, with separate cookie jars for S1, S2 and independent repeat logins. Invalid-auth variants deliberately supply invalid tokens. Repeated form course keys are URL encoded explicitly, and redirects are inspected before manually following their intended location.

Fresh Session snapshots cover every application model table. Read-only and rejected operations assert unchanged committed data, including links, feedback and timestamps. Successful operations inspect committed plan ownership/status and exact selected course links, then retrieve them through another request/client. Teardown closes every client, restores dependency mapping, lifespan, settings and engine patches, restores an initially empty settings cache, and disposes the isolated engine, including failure paths.

No existing tests were removed or modified. The new module carries `pytest.mark.integration`; case decorators carry `pytest.mark.it("IT-xx")`. Both markers are registered in `pyproject.toml`.

## Approved-plan traceability

All function names below refer to [test_student_workflow.py](../../../tests/integration/test_student_workflow.py). Each listed student portion passed. Overlapping IDs deliberately share tests.

| IT identifier | Executed test function(s) | HTTP and committed-state oracle |
|---|---|---|
| IT-01 | `test_student_login_cookie_and_logout`; `test_bad_credentials_never_authenticate` | Valid login: 303 to `/app`, HttpOnly local cookie, dashboard/API 200. Invalid credentials: 303 to `/login`, warning, no auth cookie. Logout: cookie removed and subsequent 401. Database unchanged. |
| IT-02 | `test_degree_progress_through_authenticated_html_and_json` | HTML/JSON 200; completed=3, in progress=3, remaining=87, overall=3%; Core=3/30, remaining=27. Exact owned course IDs, no S2 activity/profile, no writes. |
| IT-03 | `test_available_courses_use_completed_prerequisites_and_tracked_status`; `test_valid_submission_persists_courses_and_can_be_retrieved` | Catalogue JSON and form choices agree: C3/C4 eligible, C1/C2 tracked, C5 blocked by MATH 9999. Valid repeated-key form: 303 with semester/tab and success flash, one Pending S1 plan and exactly two unique course links. All nine semesters and outer-whitespace trimming pass. |
| IT-04 | `test_valid_submission_persists_courses_and_can_be_retrieved` | Fresh Session reads persisted plan and links; redirected HTML checks exact selected inputs. A separately logged-in client retrieves matching JSON detail/list with 200 and no writes. |
| IT-06 | `test_resubmission_reuses_plan_and_replaces_old_selection[Changes Requested]` | Seeded change request and visible private feedback; student POST returns 303; same ID becomes Pending, C4 replaces C3, advisor/feedback reset, timestamp advances, retrieval confirms replacement. |
| IT-07 | `test_resubmission_reuses_plan_and_replaces_old_selection[Rejected]` | Same committed resubmission assertions for a seeded Rejected plan without cancellation. |
| IT-08 | `test_allowed_cancellation_retains_history_and_replacement_gets_new_id` | Pending/Approved/Rejected cancel with 303 and success flash. Only status changes; historic links/metadata survive, HTML selected courses clear. Subsequent submission creates a new Pending ID and keeps the cancelled history. |
| IT-09 | `test_cancellation_rejected_for_forbidden_status` | Changes Requested/Cancelled: 303 and exact warning, every table unchanged. |
| IT-10 | `test_pending_plan_can_remove_course_but_keeps_last_course`; `test_course_removal_rejected_for_non_pending_plan` | Pending removal: 303 and success flash, one exact link remains, plan unchanged. Last-course and all four nonpending variants: warning and unchanged database. |
| IT-11 | `test_other_students_plan_and_private_data_are_inaccessible` | S2's own detail succeeds; S1's list/HTML hide S2 plan/profile/activity/messages. Foreign detail equals missing-plan 404. Foreign form cancel/remove warn; API revise/cancel/remove return 404; all data unchanged. Forged form `student_id` cannot replace authenticated S1 ownership. |
| IT-12 | `test_protected_student_requests_deny_invalid_auth_without_writes` | Missing/malformed/expired/wrong-signature/nonexistent-user tokens each deny 12 student HTML/JSON read/write requests with 401, correct denial body, no private content and unchanged database after every request. |
| IT-14 | `test_invalid_semester_rejects_without_writes`; `test_duplicate_missing_or_ineligible_courses_are_atomic_rejections`; `test_invalid_resubmission_preserves_review_and_old_courses` | Blank/legacy/out-of-range/case-invalid semesters and empty/duplicate/missing/completed/in-progress/prerequisite-blocked/mixed selections return 303 and expected warnings without partial writes. Invalid Rejected/Changes Requested resubmissions preserve prior review and courses. |
| IT-15 | `test_active_plan_blocks_duplicate_but_allows_different_semester` | Pending/Approved duplicate: 303 warning, identical prior state; independent T2 submission succeeds with a second plan and exact links. |
| IT-18 | `test_invalid_form_or_path_types_return_422_without_writes`; `test_missing_plan_or_course_warns_without_writes` | Noninteger or mixed course IDs and noninteger path IDs: JSON 422. Missing integer plan IDs/absent course membership: 303 warning. Every variant leaves the database unchanged. |

## Scope disposition

This executes the **student portions** of the approved plan. IT-03 advisor queue checks, IT-06/07 advisor review transitions and IT-08 advisor queue removal are outside this suite; review statuses are setup preconditions. IT-12 is limited to student endpoints. IT-05/13/16/17 advisor operations and IT-19/20 repository constraint/rollback cases were not added or run here. Existing coverage remains intact; this task makes no new execution claim about those tests or the complete application suite.

The plan's historical H3 status mismatch no longer applies to the current app: executed student denial cases verify actual HTTP 401 for both HTML and JSON. No production/PostgreSQL or concurrent duplicate-submission verification is claimed. Work stopped after student integration verification and its execution record.
