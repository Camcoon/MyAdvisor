# Workflow 2 API verification

Executed on 26 October 2026 against the working tree in the outer `Assignment 2` checkout. Scope: Plan Semester Course Selections student APIs and preservation of existing HTML workflows. Advisor decision endpoints were not added.

## Execution

```powershell
.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
.venv/Scripts/python.exe -m ruff check app/routers/advising_api.py app/schemas/advising.py app/services/advising_errors.py app/services/advising_service.py tests/test_semester_plans_api.py
```

Results: **216 passed** (95 existing tests and 121 new Workflow 2 integration cases); all scoped Ruff checks passed. One existing Starlette TestClient/httpx deprecation warning remains. The full suite completed in 8.14 seconds. These results describe automated verification, not manual browser acceptance or production database verification.

The new [integration tests](../../../tests/test_semester_plans_api.py) use the real FastAPI application, cookie verification, database role guards, request/response schemas, AdvisingService and AdvisingRepository. Each case uses an isolated in-memory SQLite database with foreign-key enforcement. Only the database session/engine is replaced; authentication and business rules are not mocked. Startup seeding is not run, and the application database is not modified. Fresh sessions read persisted rows after requests, including rejected operations.

## Requirement coverage

| Requirement | Exercised integration cases |
|---|---|
| View owned plans and details | Empty list, newest-first ordering, own feedback, cancelled history, no account fields, response schema and Location follow-up |
| Preserve semester validation | All nine valid semesters, surrounding whitespace, blank/legacy/out-of-range semesters |
| Prerequisite eligibility | Completed and in-progress courses blocked; unmet, in-progress and unknown prerequisite codes blocked; resubmission rechecks changed academic records |
| Reject invalid selections | Empty and duplicate selections, unknown IDs after valid selections, missing/malformed JSON, nulls, booleans, floats, strings, invalid ID ranges and server-owned fields |
| Student isolation and role checks | Every endpoint rejects missing/invalid/unresolved credentials and nonstudent database roles; owned-resource endpoints give identical 404s for foreign/missing plans; query/header identity spoofing cannot change ownership |
| Preserve status transitions | POST and PUT across all five statuses; Rejected/Changes Requested retain ID and return to Pending with new courses, cleared assignment/feedback and renewed submission time; Cancelled POST creates a new ID |
| Prevent prohibited edits | PUT cannot change semester or target a superseded plan; removal allowed only from Pending; absent selected course returns 404; last-course removal returns 409 |
| Preserve cancellation rules | Pending/Rejected/Approved become Cancelled and retain history/course rows; Changes Requested and Cancelled return 409; repeated cancellation remains prohibited |
| Structured errors and HTTP semantics | 200/201 and Location on successful submission, 401/403 auth failures, 404 ownership/resource errors, 409 conflicts, 422 schema/domain failures, 503 database errors; responses use JSON |
| Transactions | Real SQLite triggers fail creation after an earlier course insert, fail replacement after old selections are deleted, and reject removal/cancellation writes; all before/after plan and course rows match on failure; a later request succeeds after removing the trigger |
| Error privacy | Integrity and operational failures omit SQL and internal database messages |
| Browser compatibility | HTML submit, remove and cancel retain 303 redirects and operate on the same rows as the API; invalid form submission still redirects; dashboard renders HTML after API submission |
| Endpoint documentation | OpenAPI includes the six resource operations, request allowlists and success models; no advisor decision/review API paths |

Implementation and endpoint contracts: [student API documentation](../api.md). Existing broader planned integration scenarios remain in [the integration test plan](../test-plans/integration-test-plan.md); the execution above establishes only the cases exercised by the cited automated suites.
