# Workflow 3 API verification

Executed on 26 October 2026 against the active outer `Assignment 2` checkout. Scope: Review and Approve Course Plans advisor APIs, existing advisor forms, and regressions across all application tests. The nested `comp3613a1` checkout was not modified.

## Execution

```powershell
.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
.venv/Scripts/python.exe -m ruff check app/routers/advising_api.py app/schemas/advising.py app/services/advising_service.py app/repositories/advising.py tests/test_advisor_plans_api.py tests/test_semester_plans_api.py
git diff --check
```

Actual results: **409 passed** in **12.29 seconds**, comprising 216 existing tests and **193 new Workflow 3 integration cases**. All scoped Ruff checks and the diff whitespace check passed. One existing Starlette TestClient/httpx deprecation warning remains. The old Workflow 2 OpenAPI test's assertion that no advisor review endpoint exists was removed because Workflow 3 now deliberately adds those endpoints; its student endpoint/schema checks remain.

The initial targeted run had six failing expiry cases because the new test fixture passed an `exp` claim to `create_access_token`, which intentionally replaces it with a fresh expiry. Correcting the fixture to pass a negative `expires_delta` exercised actual expired cookies; all six passed in the full run. One test context-manager lint issue was also corrected before the final checks.

These are automated integration results against isolated SQLite databases, not manual browser acceptance or production/Postgres verification. The [new tests](../../../tests/test_advisor_plans_api.py) use real FastAPI routes, signed cookie verification, current database roles, schemas, services, repositories, and committed writes. Foreign keys are enabled. Only the database engine/session is replaced; startup demo seeding is not run and the application database is not changed.

## Requirement coverage

| Requirement | Exercised integration cases |
|---|---|
| View available plans | Empty queue; only Pending records; oldest-first ordering; multiple students; same queue as the advisor dashboard |
| View individual submissions | Selected courses, prerequisites, student identification and degree program; null program; reviewed/cancelled history; read operations leave rows unchanged |
| Secure advisor actions | All six endpoints reject missing, malformed, expired and unresolved cookies with JSON 401, including HTML Accept headers; students and unknown database roles receive 403 |
| Current database authority | An admin JWT claim cannot grant students advisor access; an opposing JWT role does not deny an actual database admin; role revocation applies with an existing cookie |
| Allowed decisions | Generic review and dedicated approve/reject/request-changes routes persist each existing status transition |
| Feedback | Missing/empty/whitespace feedback; exactly 500 Unicode characters accepted; 501 characters rejected before trimming; invalid types rejected |
| Request validation | Missing/invalid decisions, malformed/missing/non-object bodies, invalid path IDs, server-owned fields, and action decision overrides return JSON 422 without mutation |
| Advisor identity and persistence | Fresh sessions verify status, authenticated advisor ID and trimmed feedback; query/header advisor spoofing has no effect; course rows and submission time remain unchanged |
| No longer Pending | Every action rejects all four nonpending states with 409; another advisor cannot overwrite a completed review; deterministic competing commits after a stale Pending read cannot overwrite Approved or Cancelled status, advisor identity or feedback |
| Student visibility | The owning student's existing plan API immediately reflects the decision and feedback, while retaining its response allowlist |
| Missing resources | Detail and all four decision endpoints return JSON 404 for unknown plans |
| Failure handling | Real SQLite triggers cause integrity and operational failures during review; all prior plan/course rows remain intact; 409/503 responses omit internal details; requests succeed after removing the failure |
| Original dashboard and forms | Real `/admin` HTML rendering; all three decisions through both form and existing JSON form submission; 303 redirects; invalid/stale form submissions retain flash/redirect behavior; students cannot use the original form route |
| Shared service rules | Direct service checks retain invalid-decision and over-limit feedback validation in addition to API schemas |
| Documentation | OpenAPI exposes all six routes, success models, strict request allowlists and the feedback limit |

The pending-state decision check stays in `AdvisingService.review_plan`; persistence uses an expected-status conditional update in `AdvisingRepository`. Typed domain exceptions remain `ValueError` subclasses for existing HTML handlers. All advisors use the existing `admin` role and shared pending queue; this change adds no assignment policy, database table, dashboard redesign or deployment.

Endpoint contracts: [REST API documentation](../api.md). Existing broader planned scenarios remain in the [integration test plan](../test-plans/integration-test-plan.md); only the executed suites above establish verification here.
