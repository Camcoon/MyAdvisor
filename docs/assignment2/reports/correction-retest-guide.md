# Targeted manual and Postman retesting after audit corrections

> **Approved-allocation update ? 27 October 2026:** [Current correction record](degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


Prepared **27 October 2026**. **Instructions only — none of the browser/Postman steps below has been recorded as executed.** Keep all 19 historical UAT PNGs and their observations. The historical execution remains **1 Pass / 0 Fail / 19 Not Run** (18 partial cases, UAT-05 required workflow unverified). Automated correction regressions are separate evidence and cannot fill manual fields.

The previous UAT-06 review-objective Pass remains a historical result with substituted data; its new-build readability must now be checked because F06 changed CSS. No old screenshot proves the modified application. Use a new run record and new filenames rather than overwriting original cases or backdating new checks.

## Prepare a separate corrected-build browser run

From the nested project directory containing `manage.py`, open a **new PowerShell terminal**. This prepares a new disposable database, never the existing evidence database:

```powershell
$retestRunDir = Join-Path ([System.IO.Path]::GetTempPath()) ('MyAdvisor-A2-Retest-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $retestRunDir -ErrorAction Stop | Out-Null
$retestDbPath = Join-Path $retestRunDir 'retest.sqlite3'
if (Test-Path -LiteralPath $retestDbPath) { throw 'Expected a new database; stop.' }
$env:DATABASE_URI = 'sqlite:///' + $retestDbPath.Replace('\', '/')
$env:ENV = 'uat'
$env:SECRET_KEY = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
.\.venv\Scripts\python.exe manage.py init --no-drop
if ($LASTEXITCODE -ne 0) { throw 'Initialization failed; stop.' }
.\.venv\Scripts\python.exe manage.py run --host 127.0.0.1 --port 5002 --no-reload
```

Use **http://127.0.0.1:5002** for both actors. Confirm the server announces the new database. Use one dedicated normal browser profile for Student and a separate private/profile session for Advisor. Two ordinary tabs share cookies; localhost cookies also cross ports. Do not use the Postman instance or existing UAT database. If 5002 is occupied, record and substitute another port. Use the locally supplied demo credentials privately; do not capture passwords, cookies, Authorization headers or tokens.

Record actual date/time zone, tester, browser/version, OS, base URL, new DB path, source manifest/build and uncommitted changes. The local HEAD alone does not identify this modified build; use the successful correction-run source-hash metadata. Verify the empty Home/Messages/A/B/C baseline before creating plans. Stop on a setup mismatch.

**A/B/C = Year 1 semesters 1/2/3.** For a new run, follow the **original planned** selections: E1 = COMP 1201, E2 = MATH 2250, E3 = ENGL 1000, each 3 credits. Initial A is E1+E2 (6 credits), revised A is E1+E3 (6 credits); B is E2; C initially E1+E2. This also checks the known completed-prerequisite positive path through COMP 1201. It is a **new execution with different inputs**, not a correction of the historical actual three-Mathematics-course/9-credit evidence. If using the historical three-course variant again, record the exact IDs/counts/totals and keep that deviation explicit.

## Missing conditions, in practical execution order

Run the rows in this order so earlier states are available. Each expected result below is a criterion, **not an observation**. Capture before/after refresh with a short action log; a state screenshot by itself does not prove refresh. Use new filenames such as `RETEST-<actual-date>-UAT-04-after-refresh.png`. All outcomes remain pending until personally recorded.

| Case | Exact remaining/new-build browser work |
|---|---|
| **UAT-18** | Open `/login` in the Student profile. Try an incorrect password; confirm the login error and no workspace. Sign in correctly; confirm `/app`, Student identity/navigation, no Advisor Review link. Check Home has no plan, Messages has no updates, and Plan Courses A/B/C each has no plan and zero selection. Return Home and refresh; confirm the same session. |
| **UAT-01** | For the newly approved fictional data version, click Degree Progress. Record 6 completed / 3 in progress / 84 remaining / 93 required, 6%. Categories must be Core 3/36 (33 remaining, 8%), General Education 3/18 (15, 17%), Electives 0/12, Major 0/18, Additional 0/9. Confirm the fictional-data notice and activity; refresh and compare. The old 120-credit screenshot remains historical; capture a new dated image without replacing it. The owner-approved allocation resolves the configuration discrepancy; this manual acceptance is still pending. |
| **UAT-02** | In Plan Courses inspect all nine semester choices and summer labels. Select A. Search `COMP 1201`, then `Industrial Statistics`, confirming code/title matching. Clear, select Mathematics, then search COMP 1201 with Mathematics still selected; confirm no match. Clear Filters. Search `ZZZ-UAT-NO-COURSE`; confirm no match, then Clear Filters restores all departments/catalogue. |
| **UAT-03** | With zero selection attempt Review Selected Courses; it must not advance. Try selecting completed COMP 1101, in-progress COMP 1600 and missing-prerequisite COMP 2100; controls must be disabled with reasons. Select E1/E2: count 2, review total 6. Back must preserve choices. Uncheck E2: count 1; recheck: count 2. Review again and leave A ready to submit. Record the actual count sequence. |
| **UAT-04** | Submit A once. Record confirmation, Pending, exact courses and credits. Refresh. Try standard selection/review controls; they must remain locked and cannot create a duplicate. Leave Pending Remove/Cancel untouched. These are functional regression checks after F01/F07. |
| **UAT-05** | Before any Advisor decision, navigate Home and record A Pending/count/credits; navigate Messages and record its Pending entry. Sign out and sign back in, open A in Plan Courses and confirm exact selection/status retained. Later decision Messages do not supply this missing earlier workflow. |
| **UAT-19** | In the separate Advisor profile try an incorrect password, then valid login. Confirm Advisor Home at `/app` and Advisor Review navigation without Student progress/planning links. Refresh Advisor Home and independently refresh Student Home; identities must stay separate. Open Advisor Review. |
| **UAT-06 / F06** | Find A by the recorded Student and semester. Read every course title, individual credit and prerequisite, count and total. Move the pointer over each table row and confirm text remains readable; check header/footer too. Record fresh normal/hover images. Reading must leave the plan Pending. Historical UAT-06 Pass does not verify the changed styles. |
| **F01 HTML negative checks** | While A is still Pending, execute the specific Advisor-profile form-request checks below. Every request must be 403, the queue must match its before-state, and the Student must still see the same Pending courses. No role-specific Student form may mutate data. These are supplemental security checks, not new invented UAT-01–20 cases. |
| **UAT-07** | Advisor enters `Replace MATH 2250 with ENGL 1000, then resubmit.` and clicks Request Changes. Record the action confirmation, refresh the Pending queue and confirm A is absent; open Advisor Messages. In the Student profile refresh Messages and record matching Changes Requested feedback, then open Plan Courses and confirm editable original choices and no Cancel action. |
| **UAT-08** | Student replaces E2 with E3, reviews E1/E3 and 6 credits, and resubmits. Confirm Pending in Student Plan Courses and Messages; prior feedback must be cleared from the current submission. Refresh Advisor Review: exactly one revised A entry, E1/E3/6 credits. A blank Advisor input alone is not proof of stored feedback clearance. Read/hover the revised table again. |
| **UAT-09 / F06** | Advisor approves revised A with `Revised selection approved.`. Record confirmation, Advisor Messages/feedback and absence from refreshed Pending queue. Student refreshes A and Messages: Approved, exact revised courses/feedback, locked standard editing, no Remove and Cancel available. Read the complete Approved explanatory paragraph against green and capture it. |
| **UAT-10** | Submit B with E2 only (3 credits). Switch B → A → B: A must retain Approved E1/E3, B Pending E2. Record both directions and refresh the current view. |
| **UAT-11** | Advisor rejects B with `Plan rejected for this UAT scenario; choose a different course mix.`. Record confirmation/Advisor feedback and absence from refreshed Pending queue. Student refreshes Messages and Plan Courses B: exact rejection reason, editable returned plan and Cancel available; A remains Approved. |
| **UAT-12** | Student submits C with E1/E2, 6 credits. Record Student Pending view; switch to A and B to verify Approved/Rejected unchanged. Advisor refreshes Review: C with correct courses/count/credits; read/hover its table. |
| **UAT-13** | In C click Remove beside E2, dismiss the confirmation and verify both courses unchanged. Click again and accept. Confirm success, Pending E1 only / 3 credits and no final-course Remove. Advisor refreshes Review: C shows E1 / 3 credits. |
| **UAT-14** | On Approved A click Cancel Plan, dismiss and confirm unchanged approval/courses. Click again and accept. Refresh A: Cancelled, previous approval feedback retained, zero active selection and no Cancel button. Student Messages must show Cancelled. |
| **UAT-15** | Cancel Rejected B. Refresh B and Messages: Cancelled with retained rejection feedback and zero active selection. Switch A/C to confirm A Cancelled and C still Pending. Historical case evidence is `UAT-16-pending-cancelled.png` despite that misleading filename. |
| **UAT-16** | Cancel Pending C. Refresh Student Messages: Cancelled. Advisor refreshes Review: C withdrawn; other students' queued plans, if present, unchanged. Historical case evidence is `UAT-15-rejected-cancelled.png`. Do not infer an unaffected-other-student result if no other Student exists. |
| **UAT-17** | After cancellation choose E3 only in C, review 3 credits and submit using the implemented Resubmit label. Refresh Student C: new Pending E3 only. Advisor refreshes: exactly one active new C entry, E3 / 3 credits, without the old selection. Historical Cancelled Messages entries are permitted. |
| **UAT-20** | While signed in as Student directly load `/admin`; record actual HTTP 403 (Network panel may confirm status). Return to `/app?tab=home`. In Advisor profile directly load `/app?tab=plan-courses` and `/app?tab=degree-progress`: both must fall back to Advisor Home; return Review and confirm queue unchanged. Sign out Student and freshly type `/app`, then sign out Advisor and freshly type `/admin`: record each actor/URL's 401 Session Expired result and Return to Login. Do not rely on browser Back or cached content. |

## Supplemental F01 browser requests

Use only the new disposable instance, in the **signed-in Advisor profile's** DevTools Console, after A is Pending and before reviewing it. No token is read or printed. The operations deliberately test denied writes; if a request unexpectedly succeeds, record the failure and stop before dependent workflow actions.

```javascript
const queueBefore = await fetch('/api/advisor/plans').then(r => r.json());
const planA = queueBefore.find(p => p.semester_name === 'Year 1 semester 1'
  && p.student?.username === 'bob');
if (!planA) throw new Error('Expected the fresh Student A plan; stop.');
const math = planA.courses.find(c => c.code === 'MATH 2250');
if (!math) throw new Error('Expected original two-course A data; stop.');
const checks = [
  ['/app/plan', new URLSearchParams({
    semester_name: 'Year 2 semester 1', course_ids: String(math.id)
  })],
  [`/app/plan/${planA.id}/courses/${math.id}/remove`, new URLSearchParams()],
  [`/app/plan/${planA.id}/cancel`, new URLSearchParams()]
];
for (const [url, body] of checks) {
  const response = await fetch(url, {method: 'POST', body, credentials: 'same-origin'});
  console.log(url, response.status); // Expected 403, never print cookies.
  if (response.status !== 403) throw new Error('Denied-write regression; stop.');
}
const queueAfter = await fetch('/api/advisor/plans').then(r => r.json());
console.log('Visible queue unchanged:', JSON.stringify(queueAfter) === JSON.stringify(queueBefore));
```

Then refresh Student A and confirm both selected courses remain Pending, and Advisor can still legitimately Request Changes/Approve/Reject. Queue comparison proves only visible queue equality; the automated regressions separately compare every committed fixture table, including legacy Advisor-owned plans and an unknown current DB role.

## Supplemental F08 browser validation

The browser's email input may block malformed text before it reaches the server. In a new signed-out test profile on `/register`, use DevTools Network to confirm native invalid-email submission is blocked. To test the server separately, use this local-only Console request with a disposable test password; do not screenshot the submitted password/form payload:

```javascript
const invalidRegistration = await fetch('/register', {
  method: 'POST',
  body: new URLSearchParams({username: 'invalid-email-retest',
    email: 'not-an-email', password: 'disposable-test-value',
    name: 'Registration retest', student_number: 'RETEST-INVALID'})
});
console.log('Invalid email HTTP status:', invalidRegistration.status); // Expected 422.
```

Record a controlled email-field error rather than HTTP 500. A separate valid new Student registration must still redirect to login; duplicate username/email/student-number handling must remain controlled. These supplement the original supporting authentication cases; do not invent an extra original UAT case or change its historical status. Automated tests prove no database write for invalid emails and unchanged state after duplicates.

## Postman retesting required

**Rerun the entire existing 90-request collection in order, one iteration, against a new disposable corrected-build server** using [existing setup](../postman/README.md). Run separately from browser UAT, normally on port 5001. Record actual new request/assertion counts, failures/errors, date, URL, source hashes, tool/version and screenshots; export a machine-readable result if available. Historical 470 assertions are not a prediction of the new result.

| Existing request IDs | Reason to rerun |
|---|---|
| 01–18 | Readiness, real login/cookies, registration 11 and role boundaries 13–17; F08 validation must preserve valid registration and identity setup. |
| 19–21 | Progress/catalogue contracts and semester discovery; curriculum discrepancy remains unapproved, not fixed. |
| 22–50 | Student input validation, atomic creation, ownership, duplicate-plan guards, removal and last-course protection; shared runtime FK enforcement changed (F07). |
| 51–77 | Advisor review/feedback, same-ID resubmission, approval/rejection and state guards remain legitimate after F01/F07. |
| 78–86 | Cancellation/history/new-ID replacement and queue consistency under the corrected engine. |
| 87–90 | Cookie-clearing/logout and signed-out denial regression. No JWT revocation claim. |

The original 90 requests do **not** test the three HTML wrong-role mutations or malformed-email registration. In separate local Postman requests (not silently appended to the historical collection/result), use the Advisor cookie already configured locally, disabled redirects, form URL encoding and IDs from a freshly Pending Student plan:

1. POST `/app/plan`: `semester_name=Year 2 semester 1`, `course_ids=<eligible no-prerequisite course ID>` → expected **403**.
2. POST `/app/plan/<Student plan ID>/courses/<selected course ID>/remove` → **403**.
3. POST `/app/plan/<Student plan ID>/cancel` → **403**.
4. Read back the Student plan and Advisor queue using the correct actors; status/courses/counts must be unchanged. These supplemental requests belong before the collection reviews/cancels that plan, or in a separately prepared fresh run.
5. Anonymous POST `/register` with an invalid email and a disposable account's other required fields → **422**, email-field validation detail; valid and duplicate registrations remain controlled.

Never export populated credentials or `access_token` values. The existing exported collection remains unchanged, with blank password/token defaults. Record these supplemental outcomes independently from the original 90-request run.

## Recording and acceptance

Use the original [execution sheet](uat-execution.md), [evidence matrix](uat-evidence-review.md) and [19-entry missing-condition checklist](uat-supplemental-evidence.md) as historical references. Create a new dated result record for this build with actual inputs, expected vs observed, status, tester, refresh/navigation actions and new evidence filenames. A missing condition stays unverified; an attempted mismatch is a real failure; a retest is recorded separately. Preserve the old 19 PNGs and the three-course deviation. F05 needs an approved requirement oracle; F09/F15 still need deployment decisions. No full acceptance is implied by passing automated tests.
