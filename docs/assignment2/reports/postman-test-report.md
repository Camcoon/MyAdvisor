# MyAdvisor Postman test report

> **Approved-allocation update ? 27 October 2026:** [Current correction record](degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


**Corrected-build qualification ? 27 October 2026:** the report/results below are historical. [Verified corrections](audit-correction-report.md) record **284 targeted passes and 735 complete-suite passes**, each with 1 warning and no failures/errors/skips; complete-run membership is 113 unit / 214 integration / 408 other, not new separate marked runs. New source differs from the historical screenshots. Postman and manual UAT retesting of this build remains pending; historical UAT stays **1 Pass / 0 Fail / 19 Not Run**, with all original images retained. Follow the [new-build retest guide](correction-retest-guide.md); do not infer new manual results from automation.

Prepared: 26 October 2026; finalized from supplied execution evidence on 27 October 2026. Evidence review only; no tests were rerun to prepare this report.

## Collection version and API scope

Reviewed [MyAdvisor-Assignment2.postman_collection.json](../postman/MyAdvisor-Assignment2.postman_collection.json) and [run instructions](../postman/README.md). Name: **MyAdvisor - COMP 3613 Assignment 2**. Format: **Postman Collection v2.1.0**. No separate application collection revision/version is declared; do not confuse schema format with a release version. SHA-256 of the reviewed file: `409cffa7540cd73880d74139f77346cdb47d06a18d9ae8e1b11cf70ef2c44b6d`.

There are **90 ordered requests** across five folders, covering all 15 implemented JSON API operations and supporting health, login, registration and logout. Scope follows WF1 Track Degree Progress, WF2 Plan Semester Course Selections and WF3 Review and Approve Course Plans. Cookie authentication uses separate Student/Advisor/independent-Student tokens. Dynamic IDs and read-back checkpoints verify API-visible persistence. The prescribed run uses one iteration on an isolated local SQLite-backed server, no environment/data file, redirects/cookie jar disabled, and original request order.

| Folder | Executed requests |
|---|---:|
| 01 - Local readiness and real cookie authentication | 12 |
| 02 - Role boundaries, progress and catalogue | 9 |
| 03 - Submission validation and student plan lifecycle | 29 |
| 04 - Advisor review, feedback validation and student resubmission | 26 |
| 05 - Cancellation, retained history and logout | 14 |

## Requests and assertions

All **90 requests (01–90)** in the inventory below were executed in the user-verified run; the five scroll captures show their green assertion results with zero failures. Request numbers are the collection’s actual identifiers, not newly invented test IDs. The request table records scope; it does not manufacture individual response bodies or timings. Assertions inspect expected statuses, JSON error codes/details and validation fields, public response shapes/privacy, authenticated ownership/reviewer attribution, progress calculations and eligibility, exact courses/status/feedback, read-back after denied writes, queue membership, same-ID resubmission and new-ID replacement after cancellation. Positive boundaries include 500-character feedback; negative cases cover 501 characters, malformed/invalid input, missing authentication, wrong roles and foreign-resource access. Login/logout assertions check redirects and cookies. Expected denials must match their specific 401/403/404/409/422 contract.

| Request | Method | URL template |
|---|---|---|
| 01 - Server health and initialize run variables | GET | `{{base_url}}/health` |
| 02 - Unauthenticated /api/degree-progress | GET | `{{base_url}}/api/degree-progress` |
| 03 - Unauthenticated /api/courses | GET | `{{base_url}}/api/courses` |
| 04 - Unauthenticated /api/semester-plans | GET | `{{base_url}}/api/semester-plans` |
| 05 - Unauthenticated /api/advisor/plans | GET | `{{base_url}}/api/advisor/plans` |
| 06 - Unauthenticated /api/users | GET | `{{base_url}}/api/users` |
| 07 - Malformed cookie denied | GET | `{{base_url}}/api/degree-progress` |
| 08 - Incorrect login rejected | POST | `{{base_url}}/login` |
| 09 - Student login and capture cookie | POST | `{{base_url}}/login` |
| 10 - Advisor login and capture cookie | POST | `{{base_url}}/login` |
| 11 - Register independent student for ownership checks | POST | `{{base_url}}/register` |
| 12 - Other login and capture cookie | POST | `{{base_url}}/login` |
| 13 - Student forbidden from /api/advisor/plans | GET | `{{base_url}}/api/advisor/plans` |
| 14 - Student forbidden from /api/users | GET | `{{base_url}}/api/users` |
| 15 - Advisor forbidden from /api/degree-progress | GET | `{{base_url}}/api/degree-progress` |
| 16 - Advisor forbidden from /api/courses | GET | `{{base_url}}/api/courses` |
| 17 - Advisor forbidden from /api/semester-plans | GET | `{{base_url}}/api/semester-plans` |
| 18 - Advisor users list excludes passwords | GET | `{{base_url}}/api/users` |
| 19 - Student degree progress calculations and privacy | GET | `{{base_url}}/api/degree-progress` |
| 20 - Discover eligible and blocked dynamic course IDs | GET | `{{base_url}}/api/courses` |
| 21 - Choose a semester without an existing active plan | GET | `{{base_url}}/api/semester-plans` |
| 22 - Empty selection rejected | POST | `{{base_url}}/api/semester-plans` |
| 23 - Duplicate selection rejected | POST | `{{base_url}}/api/semester-plans` |
| 24 - Unknown course rejected | POST | `{{base_url}}/api/semester-plans` |
| 25 - Missing prerequisites rejected explicitly | POST | `{{base_url}}/api/semester-plans` |
| 26 - Invalid semester rejected | POST | `{{base_url}}/api/semester-plans` |
| 27 - String course ID rejected | POST | `{{base_url}}/api/semester-plans` |
| 28 - Spoof student ID rejected | POST | `{{base_url}}/api/semester-plans` |
| 29 - Malformed JSON rejected | POST | `{{base_url}}/api/semester-plans` |
| 30 - Verify invalid submissions created no records | GET | `{{base_url}}/api/semester-plans` |
| 31 - Submit two eligible courses and capture plan ID | POST | `{{base_url}}/api/semester-plans` |
| 32 - Retrieve persisted pending plan | GET | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 33 - Other student cannot read foreign plan | GET | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 34 - Missing plan conceals ownership identically | GET | `{{base_url}}/api/semester-plans/2147483647` |
| 35 - Other student cannot revise foreign plan | PUT | `{{base_url}}/api/semester-plans/{{plan_id}}/courses` |
| 36 - Other student cannot remove foreign course | DELETE | `{{base_url}}/api/semester-plans/{{plan_id}}/courses/{{course_a_id}}` |
| 37 - Other student cannot cancel foreign plan | DELETE | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 38 - Other student list excludes foreign plan | GET | `{{base_url}}/api/semester-plans` |
| 39 - Duplicate pending submission conflicts | POST | `{{base_url}}/api/semester-plans` |
| 40 - Pending plan cannot be revised | PUT | `{{base_url}}/api/semester-plans/{{plan_id}}/courses` |
| 41 - Invalid path ID rejected | GET | `{{base_url}}/api/semester-plans/0` |
| 42 - Student denied advisor action detail | GET | `{{base_url}}/api/advisor/plans/{{plan_id}}` |
| 43 - Student denied advisor action /review | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/review` |
| 44 - Student denied advisor action /approve | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/approve` |
| 45 - Student denied advisor action /reject | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/reject` |
| 46 - Student denied advisor action /request-changes | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/request-changes` |
| 47 - Verify ownership and role denials left pending plan intact | GET | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 48 - Remove selected course from pending plan | DELETE | `{{base_url}}/api/semester-plans/{{plan_id}}/courses/{{course_b_id}}` |
| 49 - Cannot remove final course | DELETE | `{{base_url}}/api/semester-plans/{{plan_id}}/courses/{{course_a_id}}` |
| 50 - Absent selected course returns not found | DELETE | `{{base_url}}/api/semester-plans/{{plan_id}}/courses/{{course_b_id}}` |
| 51 - Advisor pending queue includes submitted plan | GET | `{{base_url}}/api/advisor/plans` |
| 52 - Advisor sees student plan detail | GET | `{{base_url}}/api/advisor/plans/{{plan_id}}` |
| 53 - Advisor missing plan returns not found | GET | `{{base_url}}/api/advisor/plans/2147483647` |
| 54 - Unknown decision rejected | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/review` |
| 55 - Missing decision rejected | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/review` |
| 56 - Oversized feedback rejected | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/approve` |
| 57 - Nonstring feedback rejected | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/reject` |
| 58 - Spoof advisor identity rejected | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/review` |
| 59 - Action cannot override decision rejected | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/approve` |
| 60 - Verify invalid reviews left pending plan unassigned | GET | `{{base_url}}/api/advisor/plans/{{plan_id}}` |
| 61 - Generic review requests changes and trims feedback | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/review` |
| 62 - Reviewed plan leaves pending queue | GET | `{{base_url}}/api/advisor/plans` |
| 63 - Student sees changes and feedback | GET | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 64 - Changes requested cannot be cancelled | DELETE | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 65 - Student revises and resubmits with same ID | PUT | `{{base_url}}/api/semester-plans/{{plan_id}}/courses` |
| 66 - Advisor assignment cleared after resubmission | GET | `{{base_url}}/api/advisor/plans/{{plan_id}}` |
| 67 - Dedicated request-changes action | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/request-changes` |
| 68 - POST resubmits existing changes-requested plan | POST | `{{base_url}}/api/semester-plans` |
| 69 - Dedicated reject action accepts 500-character boundary | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/reject` |
| 70 - Student sees rejection | GET | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 71 - Repeated review conflicts | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/approve` |
| 72 - POST resubmits rejected plan with same ID | POST | `{{base_url}}/api/semester-plans` |
| 73 - Dedicated approve action | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/approve` |
| 74 - Student sees approval and feedback | GET | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 75 - Approved plan cannot be edited | PUT | `{{base_url}}/api/semester-plans/{{plan_id}}/courses` |
| 76 - Approved plan cannot be reviewed again | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/reject` |
| 77 - Verify forbidden edits and reviews preserved approval | GET | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 78 - Cancel approved plan and retain selections | DELETE | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 79 - Repeated cancellation conflicts | DELETE | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 80 - Retrieve cancelled history | GET | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 81 - Cancelled plan remains visible to advisor | GET | `{{base_url}}/api/advisor/plans/{{plan_id}}` |
| 82 - Cancelled plan cannot be reviewed | POST | `{{base_url}}/api/advisor/plans/{{plan_id}}/approve` |
| 83 - Cancelled plan allows new submission with new ID | POST | `{{base_url}}/api/semester-plans` |
| 84 - Cancel replacement pending plan for repeatable run | DELETE | `{{base_url}}/api/semester-plans/{{plan_id}}` |
| 85 - Student list retains both cancelled records | GET | `{{base_url}}/api/semester-plans` |
| 86 - Final advisor queue excludes collection plans | GET | `{{base_url}}/api/advisor/plans` |
| 87 - Student logout clears browser cookie | GET | `{{base_url}}/logout` |
| 88 - Advisor logout clears browser cookie | GET | `{{base_url}}/logout` |
| 89 - Other logout clears browser cookie | GET | `{{base_url}}/logout` |
| 90 - No cookie after logout is denied | GET | `{{base_url}}/api/degree-progress` |

Assertions are conditional and can execute in loops. Neither 90 requests nor 93 script blocks is an actual assertion count. The existing static validator record reports 93 scripts compiled and route/structure checks; it does not run requests/assertions.

## Actual Collection Runner outcome

| Execution measure | Evidence-based value |
|---|---|
| Requests executed | **90**, user-verified; numbered rows 01–90 across the captures |
| Assertions passed / failed | **470 / 0**, user-verified and corroborated by green row counts and summary |
| Execution errors | **0**, summary Errors field and user confirmation |
| Iterations completed | **1** |
| Execution/capture date | **27 October 2026**, user-confirmed |
| Start time shown / duration | **01:25:19 AM / 10s 697ms**; screenshot clock time zone not shown |
| Average response time | **29 ms**, descriptive for this local run only |
| Source / environment selection | **Runner / none**, visible summary |
| Actual server | **http://127.0.0.1:5001**, disposable local test server, user-confirmed |
| Tester name / build / exact database | Not recorded; do not infer tester from application identities |
| Machine-readable Runner/Newman result export | **Not found**; collection JSON/YAML are definitions, not result exports |

The 470 assertions are runtime results, distinct from 90 HTTP requests and the collection’s 93 script blocks. A correctly denied negative request counts as a successful test when its assertions pass. Zero assertion failures and execution errors are observed for this one completed run; no full raw response archive or independent build identifier is available.

## Screenshot evidence

All six local Postman PNGs were opened and visually inspected; all are readable, genuine Runner views. Their headers show the same run time, duration, iteration count, assertion count and zero errors. These are overlapping scroll captures of **one run**, not six runs. Paths and hashes are recorded in the [evidence inventory](evidence-inventory.md).

| Screenshot | Readable request coverage |
|---|---|
| [012608](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012608.png) | 01–19 fully visible; 20 at lower edge; authentication, role boundaries and progress |
| [012643](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012643.png) | 21–39 fully visible; 40 at lower edge; invalid submissions, persisted plan and ownership |
| [012658](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012658.png) | 41–59 fully visible; 60 at lower edge; role denials, removal and review validation |
| [012739](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012739.png) | 61–79 fully visible; 80 at lower edge; changes requested, feedback, resubmission, rejection and approval |
| [012839](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012839.png) | 72–90; approved-state guards, cancellation/history, replacement and logout |
| [postman-results.png](../screenshots/postman-results.png) | Additional view of 72–90 and same completed summary; capture date not independently embedded |

![Completed Postman Runner summary and requests 72–90](../postman/Postman%20Screenshots/Screenshot%202026-10-27%20012839.png)

## Authentication, workflows and negative testing

Requests 02–12 and 87–90 exercise missing/malformed authentication, incorrect login, real role-specific cookie login, independent Student registration and cookie-clearing logout. Requests 13–18, 28, 33–47 and 58–59 verify role/ownership restrictions, privacy and spoofing rejection, including unchanged state after denials.

WF1 uses request 19 for degree calculations/privacy. WF2 uses catalogue/eligibility (20), semester choice and invalid input (21–30), persisted submission (31–32), duplicate/state/ownership guards (33–47), removal/last-course checks (48–50), revision and returned status (63–72), and cancellation/history/replacement (78–86). WF3 covers queue/detail (51–53), malformed or invalid review/feedback/identity (54–60), requests for changes and feedback (61–68), rejection at the 500-character boundary (69–72), approval and state guards (73–77). Read-back checkpoints verify that invalid or forbidden operations do not change the protected plan. These groups overlap and do not represent additional runs.

## Limitations, defects and conclusion

The local sequential SQLite-backed run excludes browser usability, production/PostgreSQL behavior, database outages, concurrency, load and races. API read-back demonstrates visible persistence but does not replace direct rollback/constraint tests (IT-19/20). Logout clears cookies; this does not establish revocation of a previously issued JWT. Capture headers do not independently establish the actual URL, database, tester or tested commit; URL/date are attributed to the user’s verified record. The reviewed collection hash identifies today’s definition, not a cryptographically attested executed build.

No assertion failure, execution error or Runner defect/retest is recorded for this run. **All 90 requests completed with 470 successful assertions, zero assertion failures and zero execution errors in one iteration.** API checks succeeded within that scope. Browser acceptance remains pending in the [UAT report](uat-final-report.md).

## Prompt 14 final reconciliation ? 27 October 2026

The user reconfirms 90 requests successfully executed, 470 assertions passed, zero assertion failures, zero execution errors and one iteration. Existing summary image visually rechecked; no rerun or new result export. UAT tester/date confirmation applies to the manual captures, not automatically to this API run. Manual disposition is now **1 Pass / 0 Fail / 19 Not Run**, including 18 partially verified cases; [UAT report](uat-final-report.md) records remaining checks.
