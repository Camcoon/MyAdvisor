# MyAdvisor Assignment 2 — Manual UAT execution sheet and browser walkthrough

> **Approved-allocation update ? 27 October 2026:** [Current correction record](degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


**Corrected-build qualification ? 28 October 2026:** the UAT observations and screenshots below are historical browser evidence and do not establish retesting of the corrected build. The latest corrected-build full pytest run is **751 passed, 1 warning, no failures/errors/skips**; its 116 unit / 227 integration / 408 other node counts are membership in that one run, not separate marked executions. The historical Postman run remains 90 requests / 470 assertions passed; the revised collection has not been rerun. Keep those results distinct from this manual UAT.

Evidence reconciliation: **27 October 2026**. Tester: **Cameron Ramesar**, explicitly confirmed by the user (not inferred from the seeded account). All 19 documented captures and associated workflows were personally executed on **27 October 2026**, user-confirmed; review/submission cards corroborate that date. Individual capture times/time zone are not independently recorded.

**Full-case totals: 1 Pass / 0 Fail / 18 Executed - Partially Verified / 1 Not Executed - Unverified (20 cases).** The tester confirmed performing the 18 partial workflows; their screenshots or supplied observations establish primary outcomes but not every planned substep. UAT-05 remains unverified because no adequate observation establishes its Pending Home/Messages and sign-out/sign-in workflow. UAT-06 passes its documented review objective with the actual substituted selection. There are no observed failures; unverified checks and data deviations are not failures. No test was rerun.

The original planned steps and expected outcomes remain unchanged in the execution companion and original plan. Actual course substitutions satisfy positive selection/submission/review/revision objectives but do not prove the exact planned two-course inputs or nonempty prerequisite path for initial A. User-supplied observations are attributed to the user's October 27/Prompt 14 record; screenshot findings below were independently visually inspected. No additional observation is assumed to confirm unmentioned substeps.

This is the execution companion to the [UAT plan](../test-plans/uat-test-plan.md). Existing UAT-01–17 identifiers are preserved; UAT-18/19 separate login from workflow testing and UAT-20 adds demonstrable role restrictions. Run in the order below, not numeric order.

## Accuracy review of the UAT plan

Reviewed the original wireframe visually, current Student/Advisor templates and sidebar/login, HTML workflow routes, auth/error handling, service/repository transitions and seed data, [Assignment 1 workflow definitions](../../report.md), [project setup](../../../README.md), [API documentation](../api.md), and [Postman isolation instructions](../postman/README.md).

- The three original workflows are WF1 Track Degree Progress (Student), WF2 Plan Semester Course Selections (Student), WF3 Review and Approve Course Plan (Advisor).
- The wireframe's **Next**, **Student Plans**, **Approve** and **Reject** correspond to **Review Selected Courses**, **Advisor Review**, **Approve Plan** and **Reject Plan**. Use current labels. Login is supporting authentication, not a drawn wireframe panel. Cancellation and resubmission extend the original workflows; their controls are not drawn explicitly.
- No Reports screen, bell notifications, inline selected-course chips, academic-record editor, separate Advisor login page, or semester-year text entry is required by these tests. Use the implemented sidebar, checkboxes, selection count and review step.
- Semesters are the nine fixed **Year 1–3 semester 1–3** choices, not the mockup's calendar year. Semester 3 is summer. Seeded academic values replace the mockup's illustrative values.
- Only Pending plans appear in Advisor Review. Pending and Approved plans lock standard selection. Rejected and Changes Requested plans are editable. Cancellation is allowed for Pending, Rejected and Approved, and is absent for Changes Requested and Cancelled.
- Resubmitting a returned plan clears its previous feedback and Advisor assignment. Cancelling retains history but clears the active selection; the next submission creates a new plan even though the button says **Resubmit Plan for Advisor Review**.
- Source review identifies category requirements totalling 120 versus degree total 93. This is an unresolved acceptance concern, not an observed UAT failure. Do not silently change the expected total or mark acceptance complete merely because the seed matches.
- Browser role coverage is limited to real navigation and direct GET access. Hidden links alone do not prove backend security; no browser-only claim is made for cross-student ownership or all write endpoints. Automated/API checks are separate.
## Purpose and basis

Verify that a Student can understand degree progress, choose eligible courses, submit and revise semester plans, see advisor decisions, and cancel plans where permitted; and that an Advisor can review submissions and request changes, approve, or reject them. All execution is manual through the browser. Expected results remain the original planned oracles. Actual-result rows below distinguish observed screenshot states from unverified checks.

Original Assignment 1 reference: [Three-Panel Student Advisor Dashboard Mockup](../../wireframes/Three-Panel%20Student%20Advisor%20Dashboard%20Mockup.png).

| Reference | Original wireframe component | Current browser equivalent |
|---|---|---|
| W1 | Panel 1: Track Degree Progress (Student); Overall Progress, four credit cards, Requirement Breakdown, Recent Activity | **Degree Progress**; Overall progress, Completed, In progress, Remaining, Total required, Requirement breakdown, Recent course activity |
| W2 | Panel 2: Plan Semester Course Selections (Student); semester dropdown, search, department filter, course checkboxes, Selected Courses, Next, Review Plan, Submit | **Plan Courses**; Semester, Search by code or course name, All departments, course checkboxes, selection count, Review Selected Courses, Back to course selection, Submit Plan for Advisor Review |
| W3 | Panel 3: Review and Approve Course Plan (Advisor); Student Plans, student summary, selected-course table, Comments (optional), Approve, Reject, Request Changes | **Advisor Review**; Student plan review, student summary, Selected courses, Comments (optional), Approve Plan, Reject Plan, Request Changes |
| W4 | Student Messages navigation in panels 1–2; feedback implied by panel 3 decisions | **Messages** and Plan Courses status/feedback; Home latest-plan summary |
| W5 | Extension of panel 2 planning and panel 3 decision workflow; cancellation/resubmission controls are not drawn explicitly | **Cancel Plan**, browser confirmation, editable returned plan, Resubmit Plan for Advisor Review |

Implementation references: [student template](../../../app/templates/myadvisor_dashboard.html), [advisor template](../../../app/templates/advisor_dashboard.html), [navigation](../../../app/templates/authenticated-base.html), [workflow rules and demo data](../../../app/services/advising_service.py), [student routes](../../../app/routers/user_home.py), and [advisor routes](../../../app/routers/admin_home.py). Labels and sample values in the original mockup are illustrative: use the actual seeded course codes, semesters, and degree totals below.

## Original safe local setup instructions (actual setup execution unconfirmed)

1. Open a **new PowerShell terminal**. From the workspace root, run `Set-Location -LiteralPath '.\Assignment 2'`. Confirm `manage.py`, `app` and `docs` are in this directory. If already in the repository containing `manage.py`, stay there. Use the existing project virtual environment; if dependencies are missing, follow the project README first.
2. Keep ordinary and Postman servers separate. Use port **5002** for this UAT server. If occupied, select an unused port, change `--port` below, record it, and substitute that port in every browser URL in this sheet.
3. Run this block in that same terminal. It creates a new temporary directory and SQLite database and uses process-local environment overrides. It does not edit `.env` or reset an existing database.

```powershell
$uatRunDir = Join-Path ([System.IO.Path]::GetTempPath()) ('MyAdvisor-A2-UAT-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $uatRunDir -ErrorAction Stop | Out-Null
$uatDbPath = Join-Path $uatRunDir 'uat.sqlite3'
if (Test-Path -LiteralPath $uatDbPath) { throw 'Expected a new UAT database; stop.' }
$env:DATABASE_URI = 'sqlite:///' + $uatDbPath.Replace('\', '/')
$env:ENV = 'uat'
$env:SECRET_KEY = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
Write-Host "Disposable UAT database: $uatDbPath"
.\.venv\Scripts\python.exe manage.py init --no-drop
if ($LASTEXITCODE -ne 0) { throw 'UAT initialization failed; stop before browser execution.' }
.\.venv\Scripts\python.exe manage.py run --host 127.0.0.1 --port 5002 --no-reload
```

4. Confirm initialization names this exact new SQLite path and creates [Student test account] and [Advisor test account]; save the path in the run record. If initialization skips existing users on this supposedly new database, or names a different database, stop and investigate configuration. `init --no-drop` seeds data but does not repair an existing password/role or erase plans. Never use plain `init` on a database you need.
5. Leave the terminal running. Use **http://127.0.0.1:5002** consistently, with JavaScript enabled. HTML depends on external CSS/JS resources; record missing styling/scripts as an environment blocker if they prevent interaction. Do not use localhost for one actor and 127.0.0.1 for the other.
6. Use a normal browser profile/window for Student and a private window or different browser profile for Advisor. Two normal tabs share cookies. Cookies are host scoped, not port scoped: other MyAdvisor sessions on 127.0.0.1 at ports 5000/5001 can overwrite this login. Use profiles dedicated to UAT; close other MyAdvisor tabs in those profiles and clear old site cookies before starting. Two private windows in the same private session may also share cookies.
7. Use **one `/login` page** for both roles. Student: Username supplied for the Student test account, Password `[Student test password]`, **Sign in**; expected seeded identity Cameron Ramesar, Student ID `12345678`, Computer Science. Advisor: Username supplied for the Advisor test account, Password `[Advisor test password]`, **Sign in**; expected seeded identity Dr. Williams, Advisor workspace. These credentials are for this newly seeded local database only. Do not use registration to create an Advisor.
8. In UAT-18 confirm the empty Home and Messages baseline, then inspect **Plan Courses** for each A/B/C semester before any submission: no status banner or selected-course list, zero selected. A = **Year 1 semester 1**; B = **Year 1 semester 2**; C = **Year 1 semester 3**. If any has an old plan, stop and prepare a fresh isolated run; do not cancel an unrelated record to make this sheet fit. Return to A.

### Actual run record (confirmed execution; remaining environment metadata required)

| Field | Value |
|---|---|
| Run ID | Not supplied; no invented execution identifier |
| Base URL | Planned: http://127.0.0.1:5002; actual: unconfirmed |
| Build/commit and local changes | ___ |
| Disposable database path | ___ |
| Browser/version and OS | ___ |
| Student identity/ID | ___ |
| Advisor identity | ___ |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date/time zone | ___ (record actual date; America/La_Paz, UTC−04:00 if used) |
| Evidence directory | Actual supplied images: [screenshots/UAT](../screenshots/UAT/); no separate completed run export found |

### Practical execution sequence and interference control

| Order | Cases | State required/created |
|---|---|---|
| 1 | UAT-18, UAT-01–05 | Student login, empty baseline, progress/catalogue, A submitted Pending |
| 2 | UAT-19, UAT-06–09 | Advisor login/review; A Changes Requested → revised Pending → Approved |
| 3 | UAT-10–11 | B Pending → Rejected; leave A Approved |
| 4 | UAT-12–13 | C Pending with E1/E2 → Pending with E1 |
| 5 | UAT-14–16 | Cancel A Approved, B Rejected, C Pending |
| 6 | UAT-17 | New C Pending with E3; preserve old Cancelled history |
| 7 | UAT-20 | Role restrictions and sign-out protection; no plan writes |

Run one sequence per fresh database. Do not run Postman against this UAT database or let another tester change it. Do not repeat submission/decision clicks to recover an unclear result: refresh and inspect state first. After the other actor acts, refresh the receiving window; updates are not assumed to be live. Always reselect the exact semester after sidebar navigation, which can default to the latest plan. Match queue cards by Student name/ID **and semester**, never position.

Pending/Approved selection controls are locked; use the separate Remove/Cancel actions only when the case calls for them. Capture feedback before resubmitting, because it is cleared. Retained Cancelled Messages entries are expected and must not be mistaken for the current plan. Courses may be reused across A/B/C; approval does not mark them academically completed.

If a case fails, record the observed state and defect before continuing. Use **NOT EXECUTED / UNVERIFIED** only when no adequate observation establishes the workflow; do not downgrade a genuinely executed, partially evidenced workflow to that label. Do not improvise new states or silently clean up records. Resume independent cases only when their stated preconditions hold. For a clean retry, stop the UAT server with Ctrl+C, preserve its database/evidence, then run the setup block again to create a new path and run ID. Sign out/clear stale cookies before logging into the new run. Keep the old sheet as that run's record.

For any collapsed sidebar use **Toggle sidebar**. Scroll within the course list to find courses. Select semesters using **Semester** and wait for the automatic reload; unsent checkbox choices need not survive reload. Confirmation dialogs use the browser's **OK/Cancel** (or equivalent localized labels).
### Test data baseline

These values come from the existing demo-data implementation and must be confirmed for the chosen test environment before execution. A mismatch is a setup discrepancy, not evidence of a passed test.

| Data | Expected baseline |
|---|---|
| Student program | Computer Science, 93 total credits |
| Recorded courses | COMP 1101 Introduction to Programming: Completed, 3 credits; MATH 1200 Discrete Mathematics: Completed, 3 credits; COMP 1600 Data Structures: In Progress, 3 credits |
| Progress | Completed 6; In progress 3; Remaining 84; Total required 93; Overall progress 6 / 93 (6%) |
| Category breakdown | Core Courses 3/36, 33 remaining; General Education 3/18, 15 remaining; Electives 0/18, 18 remaining; Major Requirements 0/24, 24 remaining; Additional Requirements 0/24, 24 remaining |
| E1 | COMP 1201 Object-Oriented Programming, 3 credits, Computer Science, prerequisite COMP 1101; eligible |
| E2 | MATH 2250 Industrial Statistics, 3 credits, Mathematics, no prerequisites; eligible |
| E3 | ENGL 1000 Academic Writing, 3 credits, English, no prerequisites; eligible |
| Ineligible examples | COMP 1101: Already completed; COMP 1600: Already in progress; COMP 2100 Database Design: Missing prerequisite(s): COMP 1600 |

The seeded category requirements total 120 while the degree total is 93. This is a source/data inconsistency identified during planning, not an executed failure. Record whether the resulting breakdown is understandable and raise it for review; do not replace the degree total with the mockup's 120 or invent corrected data. If acceptance requires reconciled category totals, this remains an acceptance issue even if the screen matches the current seed.

## Verified screenshot evidence

All **19** UAT PNGs exist, were opened and visually inspected, and are embedded in the final PDF. See the [complete screenshot/case matrix](uat-evidence-review.md). Earlier filenames UAT-01 through UAT-05 are presentation order, not case IDs. Actual initial A used MATH 1300/2200/2250 (9 credits); revised A used MATH 1300/2200/ENGL 1000 (9 credits). Original planned data below is retained unchanged.

## Case-by-case execution classification

| Case | Main workflow executed | Core acceptance objective demonstrated | Status |
|---|---|---|---|
| UAT-01 | Yes | Partially: degree totals/activity are visible; refresh and approved category-data acceptance remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-02 | Yes | Partially: catalogue search/filter state and eligible Mathematics courses are visible; other filters/search outcomes remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-03 | Yes | Partially: three eligible selections and selection count are visible; empty/ineligible/review/back checks remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-04 | Yes | Partially: successful submission, Pending state and locked selection are visible; refresh/duplicate prevention remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-05 | Not established | No: required Pending Home/Messages and sign-out/sign-in observation is absent. | NOT EXECUTED / UNVERIFIED |
| UAT-06 | Yes | Yes: the Pending Advisor review objective is fully shown with the actual three-course selection. | PASS |
| UAT-07 | Yes | Partially: Changes Requested and the same feedback in the Advisor/Student views are visible; action confirmation/queue removal remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-08 | Yes | Partially: the revised three-course Pending Advisor queue is visible; Student-side reset/current feedback and refreshed uniqueness remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-09 | Yes | Partially: Approved state, feedback and selected courses are visible; Advisor-side confirmation/queue removal and refresh remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-10 | Yes | Partially: the separate semester-2 Pending plan is visible; switching/persistence checks remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-11 | Yes | Partially: semester-2 rejection and feedback are visible; Advisor confirmation/queue removal and edit/cancel checks remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-12 | Yes | Partially: the semester-3 Pending review is visible; Student-side state and unaffected A/B checks remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-13 | Yes | Partially: course-removal success and final-course guard are visible; dismissal/no-change and refreshed queue remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-14 | Yes | Partially: approved semester-1 cancellation and cleared selection are visible; dismiss/refresh/Messages checks remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-15 | Yes | Partially: rejected semester-2 cancellation and retained feedback are visible; refresh/Messages and unaffected-plan checks remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-16 | Yes | Partially: pending semester-3 cancellation and cleared selection are visible; Student Messages/queue checks remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-17 | Yes | Partially: the new semester-3 Pending ENGL 1000 plan is visible; refresh and unique active queue entry remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-18 | Yes | Partially: authenticated Student Home/baseline is visible; invalid login and other baseline/refresh checks remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-19 | Yes | Partially: authenticated Advisor navigation is visible; invalid login and separate-session checks remain unverified. | EXECUTED - PARTIALLY VERIFIED |
| UAT-20 | Yes | Partially: signed-out 401 and login screen are visible; logged-in role restrictions and actor-specific protected URLs remain unverified. | EXECUTED - PARTIALLY VERIFIED |

### UAT-18 — Student login and clean-run baseline (execute first)

| Field | Detail |
|---|---|
| UAT ID | UAT-18 |
| Objective | Verify Student login, identity, empty baseline and persistent session. |
| Original workflow covered | Supporting Student authentication for WF1 Track Degree Progress and WF2 Plan Semester Course Selections |
| Actor | Student |
| Wireframe component | Student identity/sidebar in panels 1–2; login form is outside the original wireframe |
| Preconditions | Safe local setup complete; fresh database; dedicated Student browser profile signed out; server running |
| Test data | [Student test account] / [Student test password]; invalid password [invalid Student test password]; semesters A/B/C |

**Exact browser steps**

1. In the Student window open `http://127.0.0.1:5002/login`.
2. Enter [Student test account] in **Username**, `[invalid Student test password]` in **Password**, then click **Sign in**. Inspect the response.
3. Enter [Student test account] and `[Student test password]` and click **Sign in**.
4. Confirm **Student workspace**, Home, Cameron Ramesar and Student ID `12345678`/Computer Science. Click **Profile** if needed to read **Username**, **Student ID** and degree program.
5. Click **Home** and confirm the no-submitted-plan message in **Latest semester plan**. Click **Messages** and confirm **No advisor updates yet**.
6. Click **Plan Courses**. Choose **Year 1 semester 1**, then **Year 1 semester 2**, then **Year 1 semester 3**, waiting for each reload. Confirm each has zero selected courses and no existing plan status banner or selected-course list. Return to **Year 1 semester 1**.
7. Click **Home** and refresh. Confirm the Student remains signed in. Continue with UAT-01.

**Expected result:** Invalid credentials show **Incorrect username or password** on the login page without opening the workspace. Valid credentials open `/app` as the Student, with the seeded identity, Student navigation and no Advisor Review link. Home, Messages and A/B/C have the fresh empty baseline. Refresh preserves the authenticated Student session. If the baseline is occupied, record a setup blocker and do not begin dependent cases.

| Execution field | Value |
|---|---|
| Actual result | Student Home shows the seeded identity and Student navigation, no submitted semester plan and 0 updates. This is authenticated-state evidence, not a capture of the login attempts. Data deviation: No demonstrated course-data deviation for this case; unobserved inputs are not claimed executed. Remaining: Confirm incorrect-login denial, valid-login destination, initial empty Messages/all A/B/C semesters and refresh retaining session. |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-01.png](../screenshots/UAT/UAT-01.png) |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |

### UAT-01 — View degree progress

| Field | Detail |
|---|---|
| UAT ID | UAT-01 |
| Actor | Student |
| Original workflow covered | WF1 — Track Degree Progress (Student) |
| Objective | Understand completed, current, and remaining degree requirements. |
| Relevant wireframe component | W1: Overall Progress, credit cards, Requirement Breakdown, Recent Activity. |
| Preconditions | Local setup and UAT-18 completed; Student signed in; compare displayed data with the documented seed baseline. |
| Test data | Student demo account; baseline progress and category values above. |

**Exact browser steps**

1. In the signed-in Student window click **Degree Progress** in the sidebar.
2. Read Overall progress, all four credit cards, every Requirement breakdown row, and Recent course activity. Capture the displayed values.
3. Refresh the page and compare the values again.

**Expected result:** Student workspace opens. Credits are 6 completed, 3 in progress, 84 remaining, and 93 required; overall progress is 6 / 93 (6%). Breakdown matches the baseline and distinguishes completed from in-progress courses. Recent activity shows the three recorded courses with their correct statuses. Refresh preserves the values. Record the category-total inconsistency noted above for acceptance review.

| Execution field | Value |
|---|---|
| Actual result | Degree Progress shows 6 completed, 3 in progress, 84 remaining, 93 required and 6/93 (6%); category denominators total 120; recent academic activity is visible. Data deviation: No demonstrated course-data deviation for this case; unobserved inputs are not claimed executed. Remaining: Confirm totals/activity after refresh; reviewer disposition of DATA-01 (120 category credits versus 93 degree credits). |
| Defect ID if applicable | DATA-01 |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-02.png](../screenshots/UAT/UAT-02.png) |

### UAT-02 — Browse, search, and filter available courses

| Field | Detail |
|---|---|
| UAT ID | UAT-02 |
| Actor | Student |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Find courses and understand their credits, prerequisites, and eligibility. |
| Relevant wireframe component | W2: semester dropdown, search, department filter, course list. |
| Preconditions | UAT-01 completed; Student signed in; A has no plan. |
| Test data | A; E1/E2; search `COMP 1201`, `Industrial Statistics`, and `ZZZ-UAT-NO-COURSE`. |

**Exact browser steps**

1. Click **Plan Courses**. Open **Semester** and inspect the nine Year 1–3/semester 1–3 options; choose **Year 1 semester 1**.
2. Scroll the course list and inspect course codes, titles, credits, departments, prerequisites, and eligibility messages.
3. Enter `COMP 1201` in **Search by code or course name**; inspect the matching row.
4. Replace the search with `Industrial Statistics`; inspect MATH 2250.
5. Clear the search and choose **Mathematics** in the department dropdown; inspect the remaining rows.
6. With Mathematics still selected, search `COMP 1201`; inspect the no-match message, then click **Clear Filters**.
7. Search `ZZZ-UAT-NO-COURSE`; inspect the no-match message and click **Clear Filters** again.

**Expected result:** The chosen semester loads, and semester 3 is identified as summer. E1 and E2 show their documented details. Search matches code or title, and the department filter restricts results. Combined incompatible filters and the nonexistent search show “No courses match your search and department filters.” Clear Filters restores the catalog and All departments. No plan is submitted.

| Execution field | Value |
|---|---|
| Actual result | Year 1 semester 1, math search and All departments are visible; MATH 1300, MATH 2200 and MATH 2250 are Eligible, each 3 credits; MATH 1200 is already completed. Data deviation: Actual A initial: MATH 1300/2200/2250, 3 courses/9 credits; planned COMP 1201 + MATH 2250, 2 courses/6 credits. Remaining: Confirm semester switching, code and title searches, department and combined filters, no-match search and Clear Filters outcomes. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-03.png](../screenshots/UAT/UAT-03.png) |

### UAT-03 — Select only eligible courses and review the selection

| Field | Detail |
|---|---|
| UAT ID | UAT-03 |
| Actor | Student |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Prevent an empty or ineligible selection and check the proposed credit load. |
| Relevant wireframe component | W2: checkboxes, Selected Courses, Next/Review Plan. |
| Preconditions | UAT-02 completed; A selected; filters clear; no boxes selected. |
| Test data | E1 and E2 (6 credits); ineligible baseline examples. |

**Exact browser steps**

1. Observe **0 courses selected** and attempt to click **Review Selected Courses**.
2. Locate COMP 1101, COMP 1600, and COMP 2100, scrolling as necessary. Read their eligibility messages and attempt to select each checkbox.
3. Select COMP 1201 and MATH 2250. Check the count, then click **Review Selected Courses**.
4. Read the two reviewed courses, their prerequisites, and **Total selected credits**.
5. Click **Back to course selection**, uncheck MATH 2250, and check the count. Recheck it and click **Review Selected Courses** again.

**Expected result:** Empty selection cannot advance. The three ineligible checkboxes are disabled with the documented reasons; an in-progress prerequisite does not count as completed. Only E1/E2 are selected. The count moves 0 → 2 → 1 → 2; review shows exactly E1/E2 and 6 credits. Returning to selection retains choices. Nothing is submitted yet; leave the browser on review for UAT-04.

| Execution field | Value |
|---|---|
| Actual result | Three eligible Mathematics courses are selected; selection count is 3. Completed-course restriction is visible. Post-submission image also shows in-progress and missing-prerequisite reasons, but that form is locked. Data deviation: Actual A initial: MATH 1300/2200/2250, 3 courses/9 credits; planned COMP 1201 + MATH 2250, 2 courses/6 credits. Remaining: Confirm empty-selection prevention, pre-submission ineligible controls, actual count changes, review total and Back preserving choices; exact planned 0?2?1?2 sequence was not established. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-03.png](../screenshots/UAT/UAT-03.png); [UAT-04.png](../screenshots/UAT/UAT-04.png) |

### UAT-04 — Submit semester plan A

| Field | Detail |
|---|---|
| UAT ID | UAT-04 |
| Actor | Student |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Send the reviewed selection to an Advisor. |
| Relevant wireframe component | W2: Review Plan and Submit. |
| Preconditions | UAT-03 left E1/E2 on the review step for A; no existing A plan. |
| Test data | A; E1/E2, 6 credits. |

**Exact browser steps**

1. Confirm E1/E2 and 6 credits on **Review your selection**.
2. Click **Submit Plan for Advisor Review** once.
3. Read the confirmation, semester/status banner, and **Selected courses for Year 1 semester 1** list.
4. Refresh the page. Attempt to alter a course checkbox and click **Review Selected Courses**.

**Expected result:** “Semester plan submitted for advisor review.” appears. A is Pending with exactly E1/E2 and is awaiting advisor review. Refresh preserves the submission. Standard selection controls and the review button are disabled for the submitted semester, preventing another submission through this form. Pending-plan Remove/Cancel controls remain available as separate permitted actions; leave them untouched here.

| Execution field | Value |
|---|---|
| Actual result | Submission success message; semester 1 Pending with MATH 1300, MATH 2200 and MATH 2250 (9 credits). Standard selection is locked; Remove and Cancel controls are visible. Data deviation: Actual A initial: MATH 1300/2200/2250, 3 courses/9 credits; planned COMP 1201 + MATH 2250, 2 courses/6 credits. Remaining: Confirm refresh persistence and repeat submission prevention through the Pending form. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-04.png](../screenshots/UAT/UAT-04.png) |

### UAT-05 — View submission status

| Field | Detail |
|---|---|
| UAT ID | UAT-05 |
| Actor | Student |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Find the current submission state after navigating away and signing in again. |
| Relevant wireframe component | W2/W4: submitted plan, Home, Messages navigation. |
| Preconditions | UAT-04 completed; only A has been submitted. |
| Test data | A Pending; E1/E2, 6 credits. |

**Exact browser steps**

1. Click **Home** and read **Latest semester plan**.
2. Click **Messages** and find the **Year 1 semester 1 plan** entry.
3. Click **Sign out**, open `/login`, enter the Student credentials, and click **Sign in**.
4. Click **Plan Courses**, choose **Year 1 semester 1**, and inspect its status and selected courses.

**Expected result:** Home shows A Pending, 2 courses, 6 credits, and a waiting-for-review message. Messages identifies the same semester as Pending. Signing in again preserves A and its selection; no decision is implied before the Advisor acts.

| Execution field | Value |
|---|---|
| Actual result | No screenshot or supplied observation establishes the originally required Pending Home/Messages and sign-out/sign-in workflow. Later decision Messages are corroborating navigation evidence only. Data deviation: Actual A initial: MATH 1300/2200/2250, 3 courses/9 credits; planned COMP 1201 + MATH 2250, 2 courses/6 credits. Remaining: Confirm Pending Home/Messages summary (actual 3 courses/9 credits) and selection retained after sign-out/sign-in. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | NOT EXECUTED / UNVERIFIED |
| Proposed review disposition | Unverified required workflow |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | None for the required workflow |

### UAT-19 — Advisor login (execute after UAT-05, before UAT-06)

| Field | Detail |
|---|---|
| UAT ID | UAT-19 |
| Objective | Verify Advisor login, identity and isolated persistent session. |
| Original workflow covered | Supporting Advisor authentication for WF3 Review and Approve Course Plan |
| Actor | Advisor |
| Wireframe component | Advisor identity/navigation in panel 3; shared login form is outside the original wireframe |
| Preconditions | UAT-05 complete; A Pending; separate Advisor profile/private session signed out; Student window stays open |
| Test data | [Advisor test account] / [Advisor test password]; invalid password [invalid Advisor test password] |

**Exact browser steps**

1. In the isolated Advisor window open `http://127.0.0.1:5002/login`.
2. Enter [Advisor test account] in **Username**, `[invalid Advisor test password]` in **Password**, and click **Sign in**.
3. Check the login error, then enter [Advisor test account] / `[Advisor test password]` and click **Sign in**.
4. Inspect **Advisor workspace**, Home, Dr. Williams and the **Advisor Review** sidebar link. Click **Profile** and check Username supplied for the Advisor test account and Role **Advisor administrator**.
5. Click **Home** and refresh. Confirm the Advisor session remains active. Refresh Student **Home** in its separate window and confirm it still shows the Student identity. Continue with UAT-06 in the Advisor window.

**Expected result:** Invalid credentials show **Incorrect username or password**. Valid login opens Advisor Home at `/app`, with Advisor navigation and no Degree Progress or Plan Courses sidebar links. It does not automatically open the review queue. Refresh retains the Advisor session, and the separate Student session is unaffected. If Student identity changes, stop and correct profile isolation before making decisions.

| Execution field | Value |
|---|---|
| Actual result | Advisor Review shows Dr. Williams and Advisor navigation, with no Student planning/progress links. This is authenticated-state evidence, not a capture of login attempts. Data deviation: No demonstrated course-data deviation for this case; unobserved inputs are not claimed executed. Remaining: Confirm incorrect-login denial, valid Advisor Home destination and refresh preserving independent Student/Advisor sessions. |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-05.png](../screenshots/UAT/UAT-05.png) |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |

### UAT-06 — Advisor reviews the submitted plan

| Field | Detail |
|---|---|
| UAT ID | UAT-06 |
| Actor | Advisor |
| Original workflow covered | WF3 — Review and Approve Course Plan (Advisor); Student status/feedback supports WF2 |
| Objective | Inspect the correct Student's submission and credit load before deciding. |
| Relevant wireframe component | W3: Student Plans, student summary, Selected Courses table. |
| Preconditions | UAT-05 and UAT-19 completed; A Pending; Advisor signed in in its separate browser profile. |
| Test data | Advisor demo account; Student identity recorded during setup; A; E1/E2. |

**Exact browser steps**

1. Confirm the separate Advisor window shows Dr. Williams and Advisor workspace after UAT-19.
2. Click **Advisor Review** in the sidebar.
3. Find the card matching the recorded Student identity and **Year 1 semester 1**.
4. Inspect student ID, program, submitted date, Pending status, course count, each course row, prerequisites, and **Total requested credits**.
5. Locate **Comments (optional)**, its 0/500 counter, **Approve Plan**, **Reject Plan**, and **Request Changes**. Do not click a decision yet.

**Expected result:** The Advisor sees A in the queue with the correct Student identity, Computer Science program, submission date matching execution, E1/E2, 2 courses, and 6 total credits. All three decision controls are present. Reading the card leaves the plan Pending. Match by Student plus semester because the queue may contain other students.

| Execution field | Value |
|---|---|
| Actual result | Advisor Review shows the correct Student identity/ID/program, October 27 submission date, semester 1 Pending, MATH 1300/2200/2250, 3 courses and 9 credits, comments counter and all three decision controls. Reading the card leaves it Pending. Actual data satisfies the review objective with the documented substitution. Data deviation: Actual A initial: MATH 1300/2200/2250, 3 courses/9 credits; planned COMP 1201 + MATH 2250, 2 courses/6 credits. Remaining: No remaining outcome check for this review objective with substituted data. Separate-profile setup/login attempts remain unverified under UAT-18/19; table contrast issue UI-01 remains open. |
| Defect ID if applicable | UI-01; impact/retest unconfirmed |
| Status | PASS |
| Proposed review disposition | Verified complete review objective with substituted data |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-05.png](../screenshots/UAT/UAT-05.png) |

### UAT-07 — Request changes and deliver feedback

| Field | Detail |
|---|---|
| UAT ID | UAT-07 |
| Actor | Advisor (Student verifies delivery in the named Student steps) |
| Original workflow covered | WF3 — Review and Approve Course Plan (Advisor); Student status/feedback supports WF2 |
| Objective | Return a plan with clear revision instructions that the Student can read. |
| Relevant wireframe component | W3: Comments and Request Changes; W4/W5: feedback and returned plan. |
| Preconditions | UAT-06 completed; A still Pending. |
| Test data | Feedback: `Replace MATH 2250 with ENGL 1000, then resubmit.` |

**Exact browser steps**

1. In the Advisor's A card, enter the exact feedback above into **Comments (optional)**. Observe the character counter.
2. Click **Request Changes** and read the confirmation; refresh **Advisor Review**.
3. Click Advisor **Messages** and locate the Student/A decision.
4. In the Student window click **Messages**, refreshing if already there, and locate A.
5. Read the feedback and click **Review and update plan**. Inspect the semester, status, selected courses, and available actions.

**Expected result:** Advisor confirmation says changes were requested. A disappears from the Pending queue and appears in Advisor Messages as Changes Requested with the entered feedback. The Student sees the same status/feedback and opens editable A with E1/E2 preselected. **Cancel Plan** is absent for Changes Requested; the instruction to update and resubmit is visible. No approval or rejection has occurred.

| Execution field | Value |
|---|---|
| Actual result | Advisor Messages and Student Plan Courses show Changes Requested for semester 1 with identical feedback: "Replace MATH 2250 with ENGL 1000, then resubmit." Original three Mathematics selections remain selected in the editable form; update/resubmit instruction is visible and Cancel is absent. Data deviation: Actual A initial: MATH 1300/2200/2250, 3 courses/9 credits; planned COMP 1201 + MATH 2250, 2 courses/6 credits. Remaining: Confirm Advisor action confirmation, removal from Pending queue, and Student Messages delivery (Student Plan Courses delivery is established). |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-07-request-changes.png](../screenshots/UAT/UAT-07-request-changes.png); [UAT-07-student-feedback.png](../screenshots/UAT/UAT-07-student-feedback.png) |

### UAT-08 — Modify and resubmit the returned plan

| Field | Detail |
|---|---|
| UAT ID | UAT-08 |
| Actor | Student (Advisor verifies the queue in the named Advisor steps) |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Apply the requested change and return the revised selection for review. |
| Relevant wireframe component | W2/W5: editable selection, Review Plan, resubmission; W3: revised queue card. |
| Preconditions | UAT-07 completed; Student viewing editable A with E1/E2 selected. |
| Test data | Keep E1; replace E2 with E3; revised total 6 credits. |

**Exact browser steps**

1. In Student **Plan Courses** for A, uncheck MATH 2250 and check ENGL 1000, scrolling the list as necessary.
2. Click **Review Selected Courses** and confirm COMP 1201 plus ENGL 1000 and 6 credits.
3. Click **Resubmit Plan for Advisor Review** and inspect the resulting status and selected-course list.
4. Click Student **Messages** and inspect A's current update.
5. In the Advisor window click **Advisor Review**, refresh, and inspect the Student/A card.

**Expected result:** A returns to Pending with exactly E1/E3. The old request-changes feedback is cleared on resubmission; Messages reflects the current Pending state rather than promising immutable feedback history. Advisor queue contains one A card for this Student with the revised courses and 6 credits, ready for another decision. Capture the previous feedback in UAT-07 before this step replaces it.

| Execution field | Value |
|---|---|
| Actual result | Advisor Pending queue shows revised semester 1: ENGL 1000, MATH 1300 and MATH 2200; 3 courses, 9 credits. MATH 2250 was replaced. Empty Advisor comments input is visible; it does not independently prove stored feedback was cleared. Data deviation: Actual revised A: MATH 1300/2200 + ENGL 1000, 3 courses/9 credits; planned COMP 1201 + ENGL 1000, 2 courses/6 credits. B/C data otherwise matches the plan where shown. Exact executed feedback is recorded above; no feedback deviation is inferred. Remaining: Confirm Student Pending state and review total for the actual 3-course/9-credit revision, current Pending Messages with prior feedback cleared, and exactly one revised Advisor queue entry after refresh. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-08-resubmitted.png](../screenshots/UAT/UAT-08-resubmitted.png) |

### UAT-09 — Approve the revised plan

| Field | Detail |
|---|---|
| UAT ID | UAT-09 |
| Actor | Advisor (Student verifies delivery in the named Student steps) |
| Original workflow covered | WF3 — Review and Approve Course Plan (Advisor); Student status/feedback supports WF2 |
| Objective | Approve the revised plan and let the Student see the decision. |
| Relevant wireframe component | W3: Comments and Approve; W2/W4: plan status and Messages. |
| Preconditions | UAT-08 completed; revised A Pending. |
| Test data | A; E1/E3; feedback `Revised selection approved.` |

**Exact browser steps**

1. In Advisor **Advisor Review**, find the Student/A card and confirm E1/E3.
2. Enter `Revised selection approved.` into its **Comments (optional)** and click **Approve Plan**.
3. Read the confirmation and refresh the review queue. Click Advisor **Messages** and inspect A.
4. In the Student window click **Messages** and read A's status/feedback.
5. Click **Plan Courses**, choose A, and inspect the selected courses and editing controls. Refresh once.

**Expected result:** “Plan approved.” appears and A leaves the Pending queue. Both actors see Approved and the exact feedback. Student A retains E1/E3 and remains Approved after refresh. Course checkboxes/review button are locked; Pending-only Remove buttons are absent. **Cancel Plan** remains available because the current implementation permits cancellation of Approved plans; do not cancel until UAT-14.

| Execution field | Value |
|---|---|
| Actual result | Student semester 1 is Approved; feedback: "Revised selection approved." ENGL 1000, MATH 1300 and MATH 2200 remain selected (9 credits); standard selection is locked, Remove absent and Cancel available. Student Messages in UAT-11 also shows this approval/feedback. Data deviation: Actual revised A: MATH 1300/2200 + ENGL 1000, 3 courses/9 credits; planned COMP 1201 + ENGL 1000, 2 courses/6 credits. B/C data otherwise matches the plan where shown. Exact executed feedback is recorded above; no feedback deviation is inferred. Remaining: Confirm Advisor action confirmation and Advisor Approved feedback/queue removal; Student refresh persistence. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-09-approved.png](../screenshots/UAT/UAT-09-approved.png); [UAT-11-rejected.png](../screenshots/UAT/UAT-11-rejected.png) |

### UAT-10 — Submit a separate plan for rejection

| Field | Detail |
|---|---|
| UAT ID | UAT-10 |
| Actor | Student |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Submit a different semester without altering the approved plan. |
| Relevant wireframe component | W2: semester, selection, review, submit. |
| Preconditions | UAT-09 completed; A Approved; B has no plan. |
| Test data | B = Year 1 semester 2; E2 only, 3 credits. |

**Exact browser steps**

1. Click Student **Plan Courses** and choose **Year 1 semester 2**.
2. Select only MATH 2250; click **Review Selected Courses** and confirm one course, 3 credits.
3. Click **Submit Plan for Advisor Review** and inspect B's status/list.
4. Choose **Year 1 semester 1** to inspect A, then switch back to **Year 1 semester 2**.

**Expected result:** B is Pending with only E2; A remains Approved with E1/E3. Switching semesters displays the selected semester's own plan and status without mixing the two selections.

| Execution field | Value |
|---|---|
| Actual result | Student semester 2 submission success and Pending state with only MATH 2250, Industrial Statistics, 3 credits. Data deviation: Actual revised A: MATH 1300/2200 + ENGL 1000, 3 courses/9 credits; planned COMP 1201 + ENGL 1000, 2 courses/6 credits. B/C data otherwise matches the plan where shown. Exact executed feedback is recorded above; no feedback deviation is inferred. Remaining: Confirm switching between semesters preserves each separate selection/status; later UAT-11 supports retained approval, not every switch. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-10-second-plan.png](../screenshots/UAT/UAT-10-second-plan.png) |

### UAT-11 — Reject the separate plan

| Field | Detail |
|---|---|
| UAT ID | UAT-11 |
| Actor | Advisor (Student verifies delivery in the named Student steps) |
| Original workflow covered | WF3 — Review and Approve Course Plan (Advisor); Student status/feedback supports WF2 |
| Objective | Reject B and communicate the reason to the Student. |
| Relevant wireframe component | W3: Comments and Reject; W4/W5: rejected status and revision option. |
| Preconditions | UAT-10 completed; B Pending. |
| Test data | B; feedback `Plan rejected for this UAT scenario; choose a different course mix.` |

**Exact browser steps**

1. In the Advisor window click **Advisor Review**, refresh, and find the Student's **Year 1 semester 2** card containing only MATH 2250.
2. Enter the exact feedback above into that card's **Comments (optional)** and click **Reject Plan**.
3. Read the confirmation, refresh the queue, then inspect B in Advisor **Messages**.
4. In the Student window click **Messages** and inspect B's status and feedback.
5. Click B's **Review and update plan** link; inspect the editable course selection and **Cancel Plan** control without using either yet.

**Expected result:** “Plan rejected.” appears; B leaves the Pending queue. Both actors see Rejected with the exact reason. Student B is editable for resubmission and cancellation is available. A's approval remains unchanged. Leave B Rejected for UAT-15.

| Execution field | Value |
|---|---|
| Actual result | Student Messages shows semester 2 Rejected with feedback: "Plan rejected for this UAT scenario; choose a different course mix." Semester 1 remains Approved with its approval feedback. Data deviation: Actual revised A: MATH 1300/2200 + ENGL 1000, 3 courses/9 credits; planned COMP 1201 + ENGL 1000, 2 courses/6 credits. B/C data otherwise matches the plan where shown. Exact executed feedback is recorded above; no feedback deviation is inferred. Remaining: Confirm Advisor rejection confirmation/feedback and queue removal; Student rejected plan editability and Cancel availability. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-11-rejected.png](../screenshots/UAT/UAT-11-rejected.png) |

### UAT-12 — Submit a pending plan for cancellation checks

| Field | Detail |
|---|---|
| UAT ID | UAT-12 |
| Actor | Student (Advisor verifies the queue in the named Advisor steps) |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Prepare a Pending plan through normal browser submission. |
| Relevant wireframe component | W2: semester, selection, review, submit; W3: queue. |
| Preconditions | UAT-11 completed; C has no plan. |
| Test data | C = Year 1 semester 3; E1/E2, 6 credits. |

**Exact browser steps**

1. Click Student **Plan Courses**, choose **Year 1 semester 3**, and select COMP 1201 and MATH 2250.
2. Click **Review Selected Courses**, verify 6 credits, and click **Submit Plan for Advisor Review**.
3. Inspect C's Pending status and its selected-course list.
4. In the Advisor window click **Advisor Review**, refresh, and find the Student/C card; make no decision.

**Expected result:** C is Pending with E1/E2 and is visible to the Advisor with 6 credits. A remains Approved and B remains Rejected. C stays Pending for UAT-13 and UAT-16.

| Execution field | Value |
|---|---|
| Actual result | Advisor Review shows semester 3 Pending with COMP 1201 and MATH 2250, 2 courses and 6 credits. Data deviation: Actual revised A: MATH 1300/2200 + ENGL 1000, 3 courses/9 credits; planned COMP 1201 + ENGL 1000, 2 courses/6 credits. B/C data otherwise matches the plan where shown. Exact executed feedback is recorded above; no feedback deviation is inferred. Remaining: Confirm Student Pending view and that A Approved/B Rejected were unchanged during this submission. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-12-pending-plan.png](../screenshots/UAT/UAT-12-pending-plan.png) |

### UAT-13 — Remove a course from a Pending plan and protect the last course

| Field | Detail |
|---|---|
| UAT ID | UAT-13 |
| Actor | Student (Advisor verifies the queue in the named Advisor steps) |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Adjust a submitted Pending plan without leaving an empty plan. |
| Relevant wireframe component | W2/W5: selected-course removal; submitted-plan Remove is an implementation extension. |
| Preconditions | UAT-12 completed; C Pending with E1/E2. |
| Test data | Remove E2; retain E1, 3 credits. |

**Exact browser steps**

1. In Student **Plan Courses**, choose C and click **Remove** beside MATH 2250 in **Selected courses for Year 1 semester 3**.
2. Dismiss the browser confirmation with **Cancel** and verify both courses remain.
3. Click the same **Remove** again and accept the confirmation with **OK**.
4. Read the confirmation and inspect the remaining course and available removal action. Refresh.
5. Refresh Advisor **Advisor Review** and inspect C's course table and total.

**Expected result:** Dismissing the dialog changes nothing. Confirming removes only E2 and shows “Course removed from the submitted plan.” C stays Pending with E1 and 3 credits. The remaining course has no Remove button and displays “Cancel the plan to remove its last course.” Advisor queue reflects E1/3 credits after refresh.

| Execution field | Value |
|---|---|
| Actual result | "Course removed from the submitted plan." appears. Semester 3 stays Pending with only COMP 1201, 3 credits. No Remove button for the final course; "Cancel the plan to remove its last course." is visible. Data deviation: No demonstrated course-data deviation for this case; unobserved inputs are not claimed executed. Remaining: Confirm dismissing Remove changed nothing and refreshed Advisor queue showed COMP 1201/3 credits. Final-course UI guard is established; no forged removal request is claimed. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-13-course-removed.png](../screenshots/UAT/UAT-13-course-removed.png) |

### UAT-14 — Cancel an Approved plan

| Field | Detail |
|---|---|
| UAT ID | UAT-14 |
| Actor | Student |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Cancel A using the implemented permission for Approved plans. |
| Relevant wireframe component | W5: cancellation extension to panel 2. |
| Preconditions | UAT-09 approval retained; A Approved; UAT-12/13 completed. |
| Test data | A; Approved → Cancelled. |

**Exact browser steps**

1. Click Student **Plan Courses**, choose A, and confirm its current status is Approved.
2. Click **Cancel Plan** and dismiss the confirmation with **Cancel**; verify A remains Approved with E1/E3.
3. Click **Cancel Plan** again and accept the confirmation with **OK**.
4. Read the success message; refresh and inspect status, selected courses, and available actions.
5. Click **Messages** and find A's status.

**Expected result:** Dismissing cancellation leaves approval unchanged. Confirming shows “Semester plan cancelled. You can edit it and resubmit.” A becomes Cancelled and remains so after refresh; Messages also shows Cancelled. The planning screen clears the active selection, permits a new choice, and hides Cancel Plan. Previous feedback may remain attached to the cancelled record; it must not make the current status appear Approved.

| Execution field | Value |
|---|---|
| Actual result | Cancellation success; semester 1 Cancelled; "Revised selection approved." retained as feedback. Zero courses selected; new-selection instruction and eligible unchecked choice are visible; Cancel absent. Data deviation: Actual revised A: MATH 1300/2200 + ENGL 1000, 3 courses/9 credits; planned COMP 1201 + ENGL 1000, 2 courses/6 credits. B/C data otherwise matches the plan where shown. Exact executed feedback is recorded above; no feedback deviation is inferred. Remaining: Confirm dismissing cancellation preserved approval, refresh persisted Cancelled, and Messages showed Cancelled. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-14-approved-cancelled.png](../screenshots/UAT/UAT-14-approved-cancelled.png) |

### UAT-15 — Cancel a Rejected plan

| Field | Detail |
|---|---|
| UAT ID | UAT-15 |
| Actor | Student |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Cancel B instead of resubmitting the rejected selection. |
| Relevant wireframe component | W5: cancellation extension to returned plan. |
| Preconditions | UAT-11 rejection retained; B Rejected. |
| Test data | B; Rejected → Cancelled. |

**Exact browser steps**

1. Click Student **Plan Courses** and choose B; confirm Rejected and its rejection feedback.
2. Click **Cancel Plan** and accept the confirmation with **OK**.
3. Read the success message, refresh, and inspect the status, selection count, and actions.
4. Click **Messages** and find B's entry.

**Expected result:** B becomes Cancelled and persists after refresh. No active courses are selected; a new selection is possible and Cancel Plan is absent. Messages reports Cancelled. A's cancellation and C's Pending state are unaffected. Retained rejection feedback does not override the current Cancelled status.

| Execution field | Value |
|---|---|
| Actual result | Cancellation success; semester 2 Cancelled; rejection feedback retained exactly. Zero courses selected, new selection possible and Cancel absent. Data deviation: Actual revised A: MATH 1300/2200 + ENGL 1000, 3 courses/9 credits; planned COMP 1201 + ENGL 1000, 2 courses/6 credits. B/C data otherwise matches the plan where shown. Exact executed feedback is recorded above; no feedback deviation is inferred. Remaining: Confirm refresh/Messages Cancelled and A Cancelled/C Pending unchanged. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-16-pending-cancelled.png](../screenshots/UAT/UAT-16-pending-cancelled.png) |

### UAT-16 — Cancel a Pending plan and remove it from the review queue

| Field | Detail |
|---|---|
| UAT ID | UAT-16 |
| Actor | Student (Advisor verifies the queue in the named Advisor steps) |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Withdraw C before the Advisor makes a decision. |
| Relevant wireframe component | W5: Cancel Plan; W3: Pending review queue. |
| Preconditions | UAT-13 completed; C Pending with E1; no Advisor decision on C. |
| Test data | C; Pending → Cancelled. |

**Exact browser steps**

1. Click Student **Plan Courses**, choose C, and confirm Pending with only COMP 1201.
2. Click **Cancel Plan** and accept the confirmation with **OK**.
3. Read the success message and refresh; inspect the Cancelled banner, selection count, and available actions.
4. Click Student **Messages** and inspect C's status.
5. In the Advisor window click **Advisor Review**, refresh, and look for the Student/C card.

**Expected result:** C becomes Cancelled, the active selection clears, and no repeat cancellation control appears. Student Messages shows Cancelled. The Student/C card is absent from the refreshed Pending queue, so it cannot be reviewed there. Other students' Pending submissions, if any, remain available.

| Execution field | Value |
|---|---|
| Actual result | Cancellation success; semester 3 Cancelled; zero selected courses; new-selection instruction and eligible unchecked choice visible; repeat Cancel absent. Data deviation: No demonstrated course-data deviation for this case; unobserved inputs are not claimed executed. Remaining: Confirm Student Messages Cancelled, removal from refreshed Advisor Pending queue and preservation of other students if present. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-15-rejected-cancelled.png](../screenshots/UAT/UAT-15-rejected-cancelled.png) |

### UAT-17 — Start a new plan after cancellation

| Field | Detail |
|---|---|
| UAT ID | UAT-17 |
| Actor | Student (Advisor verifies the queue in the named Advisor steps) |
| Original workflow covered | WF2 — Plan Semester Course Selections (Student), including cancellation/resubmission; queue checks support WF3 |
| Objective | Submit a fresh selection for the same semester after withdrawing its previous plan. |
| Relevant wireframe component | W2/W5: new selection after cancellation, review and submit; W3: queue. |
| Preconditions | UAT-16 completed; C Cancelled with no active selection. |
| Test data | C; E3 only, 3 credits. |

**Exact browser steps**

1. Click Student **Plan Courses**, choose C, and confirm no course is selected.
2. Select only ENGL 1000 and click **Review Selected Courses**.
3. Confirm ENGL 1000 and 3 credits, then click **Resubmit Plan for Advisor Review** (the implemented label on the cancelled-plan screen).
4. Inspect the resulting Pending status and selected-course list; refresh once.
5. In the Advisor window click **Advisor Review**, refresh, and inspect the Student/C card.

**Expected result:** C's current plan is Pending with only E3 and 3 credits; the previously cancelled E1 selection does not reappear. Advisor queue contains one active Pending C card for this Student with E3. The screen describes this as a brand new plan even though the action label says Resubmit. Historical Cancelled entries may remain in Messages. Do not infer database identifiers from the browser or require deletion of history.

| Execution field | Value |
|---|---|
| Actual result | After cancellation, semester 3 shows successful submission and a new Pending selection containing only ENGL 1000, Academic Writing, 3 credits. Old COMP 1201/MATH 2250 selection is absent. Data deviation: No demonstrated course-data deviation for this case; unobserved inputs are not claimed executed. Remaining: Confirm Student refresh persistence and exactly one active new Advisor queue entry after refresh with ENGL 1000/3 credits. Historical Cancelled Messages entries are permitted, not a required additional check. |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-17-new-plan.png](../screenshots/UAT/UAT-17-new-plan.png) |

### UAT-20 — Browser-visible role and signed-out restrictions (execute last)

| Field | Detail |
|---|---|
| UAT ID | UAT-20 |
| Objective | Verify browser role restrictions and signed-out access denial. |
| Original workflow covered | Role separation supporting WF1/WF2 Student and WF3 Advisor |
| Actor | Student (Advisor checks use the isolated Advisor window in steps 4–6) |
| Wireframe component | Different Student navigation in panels 1–2 and Advisor navigation in panel 3; access-denied pages are supporting implementation |
| Preconditions | UAT-17 complete; both role sessions authenticated and isolated; A/B Cancelled, new C Pending with E3 |
| Test data | Direct URLs /admin, /app?tab=plan-courses and /app?tab=degree-progress; no plan IDs or request tampering |

**Exact browser steps**

1. In Student **Home**, confirm **Degree Progress** and **Plan Courses** links exist and **Advisor Review** is absent.
2. In that Student window type `http://127.0.0.1:5002/admin` directly into the address bar and load it.
3. Record the response. Return by typing `http://127.0.0.1:5002/app?tab=home`; confirm Student Home still opens.
4. In the Advisor window confirm **Advisor Review** exists while **Degree Progress** and **Plan Courses** sidebar links are absent.
5. In the Advisor address bar load `http://127.0.0.1:5002/app?tab=plan-courses`, then `http://127.0.0.1:5002/app?tab=degree-progress`. Inspect the content after each load.
6. Click **Advisor Review** and verify the Student/C Pending card still contains only ENGL 1000, 3 credits. Make no decision.
7. In the Student window click **Sign out**. Type `http://127.0.0.1:5002/app` in the address bar and load it afresh (do not rely on a cached Back page). Inspect the response, then click **Return to Login**.
8. In the Advisor window click **Sign out**, then directly load `http://127.0.0.1:5002/admin`. Inspect the response and click **Return to Login**.

**Expected result:** Student direct access to `/admin` is denied with **You are not authorized to access this resource** (HTTP 403; the browser can display JSON, not a custom denial dashboard). No queue or review controls are exposed. Advisor attempts to use Student-only tab query values render **Advisor Home** at `/app`, because unsupported tabs fall back to Home; they do not display a Student planning/progress screen and do not promise HTTP 403. The valid Advisor queue remains accessible with unchanged C. After sign-out, direct `/app` and `/admin` loads show the implemented **401 Unauthorized / Session Expired** page with **Return to Login**. No plan state changes occur.

This case demonstrates these specific browser restrictions only. It does not test forged POSTs, all API permissions, or another Student's ownership. Do not mark those as manually passed by inference.

| Execution field | Value |
|---|---|
| Actual result | 401 Unauthorized / Session Expired page with Return to Login, plus an empty login screen. User attributes these to signed-out access restriction. No Student /admin 403 or Advisor restricted-tab fallback is demonstrated. Data deviation: No demonstrated course-data deviation for this case; unobserved inputs are not claimed executed. Remaining: Confirm logged-in Student direct /admin 403, Advisor Student-tab fallback, unchanged queue, and fresh protected-page denial after each role signed out (which actor/URL for each). |
| Status | EXECUTED - PARTIALLY VERIFIED |
| Proposed review disposition | Partially verified; complete case remains unconfirmed |
| Tester | Cameron Ramesar (explicit user confirmation) |
| Execution date | 27 October 2026 (user-confirmed) |
| Screenshot evidence reference | [UAT-20-access-denied.png](../screenshots/UAT/UAT-20-access-denied.png); [UAT-20-logged-out.png](../screenshots/UAT/UAT-20-logged-out.png) |
| Defect ID if applicable | No confirmed functional mismatch/retest; see issue log |

## Record actual results and evidence

For every case, record the observed outcome, actual screenshot filename, core-objective coverage, remaining checks, tester and actual execution date. Use **PASS** only when all required acceptance outcomes are verified; **EXECUTED - PARTIALLY VERIFIED** when the primary workflow outcome is observed but planned substeps remain unverified; **FAIL** only for an observed mismatch; and **NOT EXECUTED / UNVERIFIED** when no adequate observation establishes that the workflow occurred. Automated pytest results do not count as manual UAT results.

Create the run evidence directory specified in the run record when capturing screenshots. Each planned filename in a case is relative to that directory; replace it with the actual saved reference. Only the linked existing files in completed evidence-reference rows count as evidence; any suggested capture name elsewhere is not evidence. Capture the semester, identity, course/credit totals, status and exact feedback together where possible; add numbered images for long screens. Capture confirmation dialogs before dismissing/accepting them when needed. Do not expose passwords, cookies or unrelated personal data. Preserve feedback evidence from UAT-07 before UAT-08 clears it.


## Issues and acceptance

- **DATA-01 ? historical display discrepancy:** original UAT-02 shows the prior category total of 120 against a 93-credit degree total. The owner later approved the fictional 36/18/12/18/9 allocation (93 total), which is implemented and covered by the retained 751-pass run. A new human Degree Progress capture/refresh check remains pending; the old image is not relabelled.
- **UI-01 ? historical contrast observation:** old Advisor captures show low-contrast course details. Contrast CSS and automated browser checks were corrected in the later build; human browser readability acceptance remains pending. UAT-06's review-state Pass is not a readability/accessibility sign-off.
- No observed functional state-transition mismatch or UAT failure is recorded. Missing substeps are evidence gaps, not hidden defects or fabricated failures.
- Actual end states evidenced: A Cancelled, B Cancelled, C newly Pending with ENGL 1000/3 credits; signed-out denial and login screen captured. The exact new-plan Advisor queue and both actor-specific logout URLs remain unverified.

## Prompt 15 readiness

Prompt 14 evidence reconciliation is complete with explicit limitations. **Ready to enter Prompt 15 - Final Quality Audit with these open items**, not ready for unconditional acceptance or final submission sign-off. Audit must retain the incomplete-case dispositions and review DATA-01/UI-01. Tested commit, exact disposable database and browser/version are not supplied; no setup execution is inferred from instructions. No application code, test runs, remotes, deployment or final PDF were changed/generated.

See the [20-case summary and totals](uat-final-report.md) and [all 19 screenshot mappings](uat-evidence-review.md). Original execution instructions above are retained as planned steps, not claims that every step was performed.

## Tester clarification - 27 October 2026

Cameron Ramesar reconfirmed the screenshot-supported outcomes on 27 October. The clarification did not establish logged-in Student `/admin` 403, Advisor restricted-tab fallback or every refresh check. This later reporting correction changes classification, not observations: **1 Pass / 0 Fail / 18 Executed - Partially Verified / 1 Not Executed - Unverified**. See [targeted supplemental evidence and exact remaining conditions](uat-supplemental-evidence.md). Evidence for one substep does not automatically create a full Pass.

## Prompt 15 independent audit disposition ? 27 October 2026

The [27 October final quality audit](../final-quality-audit.md) recorded the then-current three-state **1 Pass / 0 Fail / 19 Not Run** disposition. This was an earlier reporting convention and is superseded by the present four-way classification; the audit itself was not rerun. It also recorded low contrast in old Advisor/Approved screenshots. The fictional 93-credit allocation was approved later; current-build human UAT-01 and readability acceptance remain outstanding.

Separate disposable audit probes reproduced issues later addressed in the corrected source. They are source/isolated-probe findings, not manual UAT failures. The historical 715/735 runs remain distinct from the latest corrected-build result of 751 passed with one warning; neither supplies missing browser substeps. The audit stopped without publication or PDF generation at that time.


## Prompt 16 evidence-mapping correction ? 27 October 2026

Visual PDF review found the two cancellation filenames describe the opposite cases: `UAT-15-rejected-cancelled.png` actually shows Year 1 semester 3 Cancelled (UAT-16), while `UAT-16-pending-cancelled.png` shows Year 1 semester 2 Cancelled with retained rejection feedback (UAT-15). References above are corrected to the visible content. Original image bytes/names, planned steps, expected outcomes and observed cancellation states remain unchanged. Current classification is **1 Pass / 0 Fail / 18 Executed - Partially Verified / 1 Not Executed - Unverified**. Filename order does not establish execution chronology; no additional refresh, unaffected-semester or queue outcome is inferred.
