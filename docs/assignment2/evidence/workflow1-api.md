# Workflow 1 and catalogue API verification

Executed 26 October 2026 against the working tree. Tests use isolated in-memory SQLite with real routes, JWT verification, role checks, services and repositories. Request sessions and database recovery use the test engine; production startup/demo seeding is not run. No deployed database or browser acceptance test was used.

Command from the project root:

```powershell
.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
```

Actual result: **95 passed, 1 warning in 6.08s**. This includes **24 new API test cases** and 71 existing regression cases. The warning is the existing Starlette TestClient deprecation of its httpx integration. No failing tests remain. Existing HTML login, dashboard, planning and advisor tests passed; no new submission or decision endpoints were added.

All new tests below are in [test_advising_api.py](../../../tests/test_advising_api.py). The original UT/IT plans remain broader specifications; this run does not claim that every unimplemented planned variant is covered.

| API case | Requirements / original plan relationship | Executed tests | Result |
|---|---|---|---|
| API-01 | R01; IT-02, UT-01: degree totals and completed-only categories | `test_degree_progress_structure_calculations_and_privacy` | Passed |
| API-02 | R02; IT-03/14 eligibility subset, UT-04–06: catalogue and prerequisites | `test_catalogue_structure_and_prerequisite_eligibility` (completed, in-progress, eligible, multiple/unresolved prerequisites) | Passed |
| API-03 | R11; IT-02 isolation: authenticated identity | `test_identity_cannot_be_selected_by_query_or_header` (both endpoints, distinct student records) | Passed |
| API-04 | R11/R12; IT-12: API authentication | `test_unauthenticated_requests_return_json_401` (both endpoints; missing, malformed, deleted user, expired cookie) | Passed |
| API-05 | R11: student role authorization | `test_only_database_student_role_is_authorized`, `test_role_change_revokes_access_with_existing_cookie` (both endpoints) | Passed |
| API-06 | R01; UT-02/03 boundary subsets | `test_empty_catalogue_and_no_program`, `test_progress_zero_denominators_and_caps` | Passed |
| API-07 | R15 (new): validated public JSON response contracts | `test_response_schema_rejects_invalid_progress`, `test_openapi_declares_validated_response_models`, exact field sets in API-01/02 | Passed |
| API-08 | R11/R15: private fields excluded, original HTML preserved | API-01/02 privacy assertions, `test_html_dashboard_is_preserved`; existing `test_api_security.py` cookie/login tests | Passed |

The historical H3 note in the original plans describes an earlier HTML 401 status defect. Current API tests directly verify JSON 401, and existing HTML tests verify HTML 401. R15 adds response schemas, public field allowlists and OpenAPI documentation; it does not expand the semester planning or advisor workflow scope.
