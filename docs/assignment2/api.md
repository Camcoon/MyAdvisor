# MyAdvisor REST API

> **Approved-allocation update ? 27 October 2026:** [Current correction record](reports/degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


Implemented scope: Workflow 1 (Track Degree Progress), Workflow 2 (Plan Semester Course Selections), and Workflow 3 (Review and Approve Course Plans), including the shared course catalogue.

All endpoints reuse the existing HTML login's `access_token` cookie. Log in through `POST /login`, retain the cookie, and send it with API requests. Student endpoints require the current database role `regular_user`; advisor endpoints require `admin`, which is the existing application's advisor role. Unknown roles receive 403. Students cannot list, view, or decide plans through advisor endpoints. Missing, malformed, expired or unresolved credentials receive JSON 401, even with `Accept: text/html`. Authorization uses the database role rather than a JWT role claim, so role revocation takes effect with an existing cookie.

Student endpoint identity always comes from the authenticated session. Student endpoints accept no student selector; extra query parameters such as `student_id` and headers such as `X-Student-ID` are ignored and cannot change the identity. Successful responses include `Cache-Control: no-store` because these resources are personal. Student responses exclude account names, usernames, email addresses, student numbers, password hashes and grades. Student plan responses include only that student's own plan feedback; progress and catalogue responses exclude advisor messages. Advisor responses include the student identification needed for review, as documented below; they exclude email addresses, passwords and grades.

## GET /api/degree-progress

Returns a validated `DegreeProgressResponse` JSON object:

```json
{
  "program": {"id": 1, "name": "Computer Science", "total_credits": 93},
  "total_credits": 93,
  "completed_credits": 3,
  "in_progress_credits": 3,
  "remaining_credits": 87,
  "progress_percent": 3,
  "category_progress": [
    {"category": "Core Courses", "earned": 3, "required": 30, "remaining": 27, "percent": 10}
  ],
  "completed": [
    {"id": 1, "code": "COMP 1100", "title": "Foundations", "credits": 3,
     "category": "Core Courses", "department": "Computer Science", "prerequisite_text": ""}
  ],
  "in_progress": [
    {"id": 2, "code": "COMP 2000", "title": "Next Course", "credits": 3,
     "category": "Core Courses", "department": "Computer Science", "prerequisite_text": "COMP 1100"}
  ]
}
```

The existing `AdvisingService.get_student_dashboard` supplies the calculations:

- Remaining credits are `max(total - completed - in_progress, 0)`.
- Progress percentage uses completed credits only, rounded and capped at 100; a zero total yields 0.
- Category earned credits count completed courses only. Category remaining credits exclude in-progress credits, floor at zero, and category percentages cap at 100.
- Without an assigned program, `program` is null, total credits default to 93, and category progress is empty. Course arrays are empty when no records exist.

## GET /api/courses

Returns a JSON array of validated `CourseSelectionResponse` objects, sorted by course code. The catalogue comes from `AdvisingRepository.list_courses`; it is shared with the HTML dashboard, not seeded or duplicated by these endpoints. An empty catalogue returns `[]`.

```json
[
  {
    "id": 3,
    "code": "COMP 3000",
    "title": "Advanced Course",
    "credits": 3,
    "category": "Core Courses",
    "department": "Computer Science",
    "prerequisite_text": "COMP 1100, MATH 1000",
    "eligible": false,
    "eligibility_reason": "Missing prerequisite(s): MATH 1000"
  }
]
```

Eligibility uses `AdvisingService.get_course_availability`. Completed courses return `false / Already completed`, and current courses return `false / Already in progress`. Otherwise, every comma-separated prerequisite code must be completed. In-progress prerequisites do not qualify; unknown codes are unmet. Blocked courses name the unmet codes in `eligibility_reason`. Courses with no unmet prerequisites return `true / Eligible`. This represents prerequisite selection eligibility, not a guarantee of semester availability or enrollment.

## Workflow 2: semester plan resources

| Method and path | Success | Behavior |
|---|---|---|
| `GET /api/semester-plans` | 200 | List the authenticated student's plans, including cancelled history, ordered by submission time descending, then ID descending; `[]` when empty |
| `GET /api/semester-plans/{plan_id}` | 200 | View one owned plan |
| `POST /api/semester-plans` | 201 or 200 | Submit a new plan (201) or resubmit the latest Rejected/Changes Requested plan for that semester (200); `Location` identifies the resulting plan |
| `PUT /api/semester-plans/{plan_id}/courses` | 200 | Replace all selected courses and resubmit an owned, latest Rejected/Changes Requested plan |
| `DELETE /api/semester-plans/{plan_id}/courses/{course_id}` | 200 | Remove one selected course from an owned Pending plan, leaving at least one course |
| `DELETE /api/semester-plans/{plan_id}` | 200 | Cancel an owned Pending, Rejected, or Approved plan; retain the plan and course rows as history |

All successful item and write operations return a `SemesterPlanResponse`. The list operation returns an array of the same objects. For example:

```json
{
  "id": 12,
  "semester_name": "Year 1 semester 2",
  "status": "Pending",
  "submitted_at": "2026-10-26T14:00:00Z",
  "advisor_feedback": "",
  "courses": [
    {"id": 3, "code": "COMP 2000", "title": "Next Course", "credits": 3,
     "category": "Core Courses", "department": "Computer Science", "prerequisite_text": "COMP 1100"}
  ]
}
```

Submit using `Content-Type: application/json`:

```http
POST /api/semester-plans

{"semester_name":"Year 1 semester 2","course_ids":[3,5]}
```

Revise and immediately resubmit using:

```http
PUT /api/semester-plans/12/courses

{"course_ids":[5]}
```

The semester is fixed when revising a specific plan. Request bodies reject extra fields, including `student_id`, `status`, `advisor_id`, and `advisor_feedback`. `course_ids` must be a nonempty array of distinct positive JSON integers within the signed 64-bit ID range; strings, floats, booleans, nulls, duplicates, and unknown courses are rejected. Path IDs must be positive integers in the same range. Every submission and resubmission rechecks the existing service eligibility rules: selected courses cannot already be completed or in progress, and all prerequisites must be completed. Including a prerequisite in the same selection does not satisfy it.

Semester names retain the existing nine choices: `Year {year} semester {semester}`, with each value from 1 through 3. Surrounding whitespace is trimmed; legacy labels such as `Fall 2026` are rejected.

The API preserves these existing transitions:

| Current state | Submit for same semester | Replace selections with PUT | Remove a course | Cancel |
|---|---|---|---|---|
| No plan | Create Pending plan | 404 | 404 | 404 |
| Pending | 409 | 409 | Allowed unless last course | Allowed |
| Approved | 409 | 409 | 409 | Allowed |
| Rejected | Same ID becomes Pending | Same ID becomes Pending | 409 | Allowed |
| Changes Requested | Same ID becomes Pending | Same ID becomes Pending | 409 | 409 |
| Cancelled | Create a new Pending plan with a new ID | 409 | 409 | 409 |

Resubmission replaces course rows, clears advisor assignment and feedback, and renews the submission time. Cancelled records retain their original courses and feedback. Repeating cancellation returns 409. Foreign and nonexistent plan IDs both return the same 404 response, without exposing ownership or status. A course absent from an owned Pending plan returns 404; removing its last course returns 409 with guidance to cancel instead.

The routes call `AdvisingService`, which reuses `AdvisingRepository` for all persistence. Existing repository transactions commit plan creation/resubmission and course rows together; failures roll back rather than leave partial inserts or delete a prior selection. The API also rolls back failed removal/cancellation writes and returns sanitized JSON for database errors. Existing `/app/plan` form submissions, removal and cancellation routes continue to flash messages and return 303 browser redirects using the same services and database records.

## Workflow 3: advisor plan review

All six operations require `AdminDep`, the same database role guard used by the original `/admin` dashboard and `/admin/review/{plan_id}` form route. In this application advisors are `admin` accounts; no new role or student-to-advisor assignment policy is introduced. The dashboard already exposes a shared pending queue to all authorized advisors, so the API uses that same queue rather than filtering by a client-supplied advisor ID.

| Method and path | Success | Behavior |
|---|---|---|
| `GET /api/advisor/plans` | 200 | List available Pending plans, oldest submission first, then ID; `[]` when empty |
| `GET /api/advisor/plans/{plan_id}` | 200 | View one submitted plan, selected courses, student identification, program, and current review state; reviewed/cancelled history remains readable |
| `POST /api/advisor/plans/{plan_id}/review` | 200 | Apply `approve`, `reject`, or `request_changes` to a Pending plan |
| `POST /api/advisor/plans/{plan_id}/approve` | 200 | Apply `approve` to a Pending plan |
| `POST /api/advisor/plans/{plan_id}/reject` | 200 | Apply `reject` to a Pending plan |
| `POST /api/advisor/plans/{plan_id}/request-changes` | 200 | Apply `request_changes` to a Pending plan |

List returns an array of `AdvisorPlanResponse`; detail and decision endpoints return one `AdvisorPlanResponse`. This extends the student plan response with `advisor_id`, `student`, and `program`:

```json
{
  "id": 12,
  "semester_name": "Year 1 semester 2",
  "status": "Changes Requested",
  "submitted_at": "2026-10-26T14:00:00Z",
  "advisor_feedback": "Please reduce the course load.",
  "advisor_id": 3,
  "student": {"id": 1, "name": "Example Student", "username": "student", "student_number": "STU-1"},
  "program": {"id": 1, "name": "Computer Science", "total_credits": 93},
  "courses": [
    {"id": 3, "code": "COMP 2000", "title": "Next Course", "credits": 3,
     "category": "Core Courses", "department": "Computer Science", "prerequisite_text": "COMP 1100"}
  ]
}
```

Before review, `advisor_id` is normally null and feedback empty. `program` is null when the student has no assigned degree program. `student` is null if its account is unavailable in a legacy database. Response models allowlist these fields, including the student identification used by the existing dashboard; account emails, roles, passwords and academic grades are excluded.

Send decision requests with `Content-Type: application/json`. The generic review endpoint requires a string `decision` and accepts optional string `feedback`:

```http
POST /api/advisor/plans/12/review

{"decision":"request_changes","feedback":"Please reduce the course load."}
```

The three action endpoints accept only optional `feedback`; the action is fixed by the URL:

```http
POST /api/advisor/plans/12/approve

{"feedback":"Course selection approved."}
```

An empty object `{}` is allowed on action endpoints. Feedback retains the existing form/service rules: optional, at most 500 characters **before trimming**, surrounding whitespace stripped before persistence, and no mandatory comment even for rejection or changes requested. Exactly 500 characters is accepted; 501 characters, including whitespace, is rejected with 422. Nonstring feedback and decisions are rejected. Missing bodies, malformed JSON, missing generic `decision`, and extra fields such as `advisor_id`, `student_id`, `status`, or `advisor_feedback` return 422. An action endpoint also rejects a supplied `decision` field. Plan IDs must be positive integers within the signed 64-bit range.

The only decision transitions remain:

| Current state | Decision | Result |
|---|---|---|
| Pending | `approve` | Approved |
| Pending | `reject` | Rejected |
| Pending | `request_changes` | Changes Requested |
| Approved, Rejected, Changes Requested, or Cancelled | Any allowed decision | 409; existing record retained |

Decision strings are case-sensitive; unknown values return 422 `invalid_plan`. Missing plans return 404 `not_found`. Every successful decision saves status, trimmed feedback and the authenticated advisor ID together. Query/header identity selectors cannot change the reviewing advisor. Courses and submission time remain unchanged. The reviewed plan disappears from the pending list, remains readable by ID, and its status/feedback are immediately available through the owning student's plan API.

All decision endpoints call the existing `AdvisingService.review_plan`. Its typed errors remain `ValueError` subclasses so the original forms still flash messages and redirect with 303. `AdvisingRepository.update_plan` uses a conditional update against the expected Pending status, so a competing review or cancellation committed after the service read cannot be overwritten; the losing review returns 409. Failed database writes roll back and return sanitized 409/503 JSON through the same dependency as the student plan API. Domain errors and database failures include `Cache-Control: no-store`.

The original advisor dashboard, form action URLs, JSON form submission script, flash messages and browser redirects remain available. The existing student resubmission rules continue to apply after Rejected or Changes Requested decisions.

## Errors and schemas

| Status | JSON body | Meaning |
|---|---|---|
| 200 | Object or array described above | Authorized student or advisor request |
| 201 | `SemesterPlanResponse` with a `Location` header | New plan created |
| 401 | `{"detail":"Could not validate credentials"}` | Missing or invalid authentication |
| 403 | `{"detail":"You are not authorized to access this resource"}` | Authenticated user lacks the endpoint's required student or advisor role |
| 404 | `{"detail":{"code":"not_found","message":"Plan not found."}}` | Plan missing, or owned by another student on student routes; missing selected course has a course-specific message |
| 409 | `{"detail":{"code":"plan_conflict","message":"..."}}` | Prohibited transition/edit, last-course removal, or database integrity conflict |
| 422 | `{"detail":{"code":"invalid_plan","message":"..."}}` | Invalid semester, duplicate/unknown selections, ineligible courses, or invalid advisor decision |
| 422 | `{"detail":[{"loc":["body","course_ids"],"type":"...","msg":"..."}]}` | FastAPI request validation, including empty arrays, malformed JSON, missing fields, invalid types, excess feedback and extra fields; entries can also include `input` and `ctx` |
| 503 | `{"detail":{"code":"database_unavailable","message":"The plan operation could not be completed. Try again later."}}` | Database operation failed; internal SQL and database messages are excluded |

FastAPI validates successful responses using the allowlists in `app/schemas/advising.py`. Credits must be nonnegative and percentages must be between 0 and 100. Invalid service responses fail server-side validation rather than becoming successful malformed JSON. Live schema definitions are available at `/openapi.json` and the interactive `/docs` page. The HTML `/app` dashboard and its existing routes remain available.

Automated coverage and requirement mappings: [Workflow 1 verification evidence](evidence/workflow1-api.md), [Workflow 2 verification evidence](evidence/workflow2-api.md), and [Workflow 3 verification evidence](evidence/workflow3-api.md).
