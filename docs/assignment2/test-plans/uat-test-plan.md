# MyAdvisor Assignment 2 — User Acceptance Test Plan

> **Approved-allocation update ? 27 October 2026:** [Current correction record](../reports/degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.

## Current approved Degree Progress oracle

For a new corrected-build execution of UAT-01, use Core 3/36 (33 remaining, 8%), General Education 3/18 (15, 17%), Electives 0/12, Major 0/18, Additional 0/9; category requirements total 93. Overall remains 6 completed / 3 in progress / 84 remaining / 93 required / 6%. Read the fictional-data notice, verify activity and compare after refresh. The earlier 120-credit baseline below is the preserved historical plan version; it is superseded for this new execution, not rewritten as an earlier observation. Use [the new blank UAT-01 record](../reports/degree-progress-retest.md), preserve original `screenshots/UAT/UAT-02.png`, and retain the original remaining conditions for the other 19 cases. No new manual result has been recorded.



**Correction-stage supplement ? 27 October 2026:** original IDs, inputs and expected outcomes below are retained. [Additional correction coverage](../reports/requirements-test-traceability.md) documents focused HTML role, actual-engine integrity, registration and contrast regressions. [Actual corrected-build results](../reports/audit-correction-report.md) are separate from historical marked/manual runs. [Required browser/API retests](../reports/correction-retest-guide.md) remain pending; no expected outcome has been promoted to an observation. F05 curriculum values are unchanged pending owner approval.

**Current execution disposition (5 November 2026 application date; local captures 4 November 2026, UTC−04:00):** **8 Pass / 0 Fail / 12 Executed - Partially Verified / 0 Not Executed** across the 20-case execution companion, based on 55 new UAT screenshots. PASS: UAT-04, UAT-05, UAT-06, UAT-10, UAT-14, UAT-15, UAT-16, UAT-17. Partially verified: UAT-01, UAT-02, UAT-03, UAT-07, UAT-08, UAT-09, UAT-11, UAT-12, UAT-13, UAT-18, UAT-19, UAT-20. The previous 3 November disposition (1 Pass / 18 Partial / 1 Not Executed) is retained as history in the [archived execution record](../reports/historical-2026-10-27/uat-execution-27oct2026.md). Preparation-stage Not Run fields below are historical. See the [current execution companion](../reports/uat-execution.md), [final UAT report](../reports/uat-final-report.md) and [evidence matrix](../reports/uat-evidence-review.md). Original planned inputs/expected results remain unchanged. Four screenshot pairs are byte-identical (UAT-01 refresh, UAT-18 refresh, UAT-19 refresh, UAT-20 role-separated 401), so those refresh/separate-role substeps remain partial. The captures show the planned two-course execution: A COMP 1201 + MATH 2250 (2 courses/6 credits), revised A COMP 1201 + ENGL 1000 (2/6), B MATH 2250 (1/3), C COMP 1201 + MATH 2250 then COMP 1201 only, and replacement C ENGL 1000 only (1/3). Degree Progress categories total 93 (3/36, 3/18, 0/12, 0/18, 0/9).

Prepared: 26 October 2026. Version: 1.1. Original preparation state: **all cases Not Run**; see the current execution disposition above.

## Execution companion and accuracy review — 26 October 2026

Use the [manual execution sheet and detailed browser walkthrough](../reports/uat-execution.md) for case-level observations. It preserves UAT-01–17 and adds UAT-18 Student login, UAT-19 Advisor login, and UAT-20 demonstrable browser role restrictions. Its physical case order is the execution order: UAT-18, UAT-01–05, UAT-19, UAT-06–17, UAT-20. Current case status is recorded in the execution companion; partial execution is not labeled Not Run.

Reviewed against the original wireframe, current HTML interfaces/navigation/login, workflow routes, authentication/error handling, seed data and plan transitions, and project documentation. Existing workflow expectations remain applicable. The companion replaces the generic setup below for final execution: it supplies exact commands for a fresh disposable SQLite database and dedicated local port 5002, seeded credentials, browser-profile isolation, evidence/result fields and failure/retry instructions. Its URLs and preconditions take precedence over this plan's port-5000 examples. Do not execute both documents as separate test runs.

The companion records these source-review qualifications: category requirements total 120 versus degree total 93; resubmission clears previous feedback; cancellation retains history; the cancelled-plan submit label says Resubmit despite creating a new plan; Advisor Student-tab requests fall back to Advisor Home, while Student direct `/admin` access is denied. These are inspected expectations/acceptance concerns, not observed manual results. Login and browser role separation are supporting controls outside the three drawn workflow panels. No application changes or manual UAT execution were performed during this review.
## Purpose and basis

Verify that a Student can understand degree progress, choose eligible courses, submit and revise semester plans, see advisor decisions, and cancel plans where permitted; and that an Advisor can review submissions and request changes, approve, or reject them. All execution is manual through the browser. This document records planned expectations from source inspection, not observed execution results.

Original Assignment 1 reference: [Three-Panel Student Advisor Dashboard Mockup](../../wireframes/Three-Panel%20Student%20Advisor%20Dashboard%20Mockup.png).

| Reference | Original wireframe component | Current browser equivalent |
|---|---|---|
| W1 | Panel 1: Track Degree Progress (Student); Overall Progress, four credit cards, Requirement Breakdown, Recent Activity | **Degree Progress**; Overall progress, Completed, In progress, Remaining, Total required, Requirement breakdown, Recent course activity |
| W2 | Panel 2: Plan Semester Course Selections (Student); semester dropdown, search, department filter, course checkboxes, Selected Courses, Next, Review Plan, Submit | **Plan Courses**; Semester, Search by code or course name, All departments, course checkboxes, selection count, Review Selected Courses, Back to course selection, Submit Plan for Advisor Review |
| W3 | Panel 3: Review and Approve Course Plan (Advisor); Student Plans, student summary, selected-course table, Comments (optional), Approve, Reject, Request Changes | **Advisor Review**; Student plan review, student summary, Selected courses, Comments (optional), Approve Plan, Reject Plan, Request Changes |
| W4 | Student Messages navigation in panels 1–2; feedback implied by panel 3 decisions | **Messages** and Plan Courses status/feedback; Home latest-plan summary |
| W5 | Extension of panel 2 planning and panel 3 decision workflow; cancellation/resubmission controls are not drawn explicitly | **Cancel Plan**, browser confirmation, editable returned plan, Resubmit Plan for Advisor Review |

Implementation references: [student template](../../../app/templates/myadvisor_dashboard.html), [advisor template](../../../app/templates/advisor_dashboard.html), [navigation](../../../app/templates/authenticated-base.html), [workflow rules and demo data](../../../app/services/advising_service.py), [student routes](../../../app/routers/user_home.py), and [advisor routes](../../../app/routers/admin_home.py). Labels and sample values in the original mockup are illustrative: use the actual seeded course codes, semesters, and degree totals below.

## Manual execution setup

- Use an already running, disposable test instance with the existing demo data. Default local base URL is `http://127.0.0.1:5000`; substitute the actual test URL everywhere if different. Do not reset a populated database to run this plan. Environment/data preparation is a prerequisite, outside these browser cases.
- Student account: `bob` / `bobpass` (regular_user). Advisor account: `admin` / `adminpass` (admin). These are documented demo credentials; use the supplied test equivalents if changed. Confirm the Student's displayed name and student ID before matching an Advisor queue card.
- Use separate browser profiles or a normal window and a private window to isolate Student and Advisor sessions. JavaScript must be enabled. Keep both sessions open and refresh after the other actor acts.
- Start with no existing plans for A = `Year 1 semester 1`, B = `Year 1 semester 2`, and C = `Year 1 semester 3`. If those semesters are already occupied, obtain an equivalent prepared test account/instance before execution; do not cancel unrelated plans. Do not modify academic records during the sequence.
- Record the environment: Base URL: ___; build/commit: ___; browser/version: ___; OS: ___; Student identity/ID: ___; Advisor identity: ___; execution date/time zone: ___. Do not include passwords in screenshots.
- Run UAT-01 through UAT-17 in order. A follows submission → changes requested → resubmission → approval → cancellation. B follows submission → rejection → cancellation. C follows submission → pending-course removal → cancellation → new submission. Courses may be reused across these semesters under the current implementation; approval does not itself record academic completion.
- Navigation convention: click the named sidebar link. If the sidebar is collapsed, click **Toggle sidebar** first. For a semester change, choose the exact **Semester** option and wait for the page to reload; unsent selections are not assumed to survive that reload.

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

## Test cases

### UAT-01 — View degree progress

| Field | Detail |
|---|---|
| UAT ID | UAT-01 |
| Actor | Student |
| Objective | Understand completed, current, and remaining degree requirements. |
| Relevant wireframe component | W1: Overall Progress, credit cards, Requirement Breakdown, Recent Activity. |
| Preconditions | Manual setup and baseline confirmed; Student window signed out. |
| Test data | Student demo account; baseline progress and category values above. |

**Exact browser steps**

1. Open `http://127.0.0.1:5000/login` in the Student window.
2. Enter `bob` in **Username**, `bobpass` in **Password**, and click **Sign in**.
3. Click **Degree Progress** in the sidebar.
4. Read Overall progress, all four credit cards, every Requirement breakdown row, and Recent course activity. Capture the displayed values.
5. Refresh the page and compare the values again.

**Expected result:** Student workspace opens. Credits are 6 completed, 3 in progress, 84 remaining, and 93 required; overall progress is 6 / 93 (6%). Breakdown matches the baseline and distinguishes completed from in-progress courses. Recent activity shows the three recorded courses with their correct statuses. Refresh preserves the values. Record the category-total inconsistency noted above for acceptance review.

| Execution field | Value |
|---|---|
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-01-degree-progress.png` (not captured) |

### UAT-02 — Browse, search, and filter available courses

| Field | Detail |
|---|---|
| UAT ID | UAT-02 |
| Actor | Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-02-course-filters.png`, `UAT-02-no-results.png` (not captured) |

### UAT-03 — Select only eligible courses and review the selection

| Field | Detail |
|---|---|
| UAT ID | UAT-03 |
| Actor | Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-03-eligibility.png`, `UAT-03-review.png` (not captured) |

### UAT-04 — Submit semester plan A

| Field | Detail |
|---|---|
| UAT ID | UAT-04 |
| Actor | Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-04-submitted-pending.png` (not captured) |

### UAT-05 — View submission status

| Field | Detail |
|---|---|
| UAT ID | UAT-05 |
| Actor | Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-05-home-status.png`, `UAT-05-messages.png` (not captured) |

### UAT-06 — Advisor reviews the submitted plan

| Field | Detail |
|---|---|
| UAT ID | UAT-06 |
| Actor | Advisor |
| Objective | Inspect the correct Student's submission and credit load before deciding. |
| Relevant wireframe component | W3: Student Plans, student summary, Selected Courses table. |
| Preconditions | UAT-05 completed; A Pending; separate Advisor window signed out. |
| Test data | Advisor demo account; Student identity recorded during setup; A; E1/E2. |

**Exact browser steps**

1. In the Advisor window open `http://127.0.0.1:5000/login`, enter `admin` / `adminpass`, and click **Sign in**.
2. Click **Advisor Review** in the sidebar.
3. Find the card matching the recorded Student identity and **Year 1 semester 1**.
4. Inspect student ID, program, submitted date, Pending status, course count, each course row, prerequisites, and **Total requested credits**.
5. Locate **Comments (optional)**, its 0/500 counter, **Approve Plan**, **Reject Plan**, and **Request Changes**. Do not click a decision yet.

**Expected result:** The Advisor sees A in the queue with the correct Student identity, Computer Science program, submission date matching execution, E1/E2, 2 courses, and 6 total credits. All three decision controls are present. Reading the card leaves the plan Pending. Match by Student plus semester because the queue may contain other students.

| Execution field | Value |
|---|---|
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-06-advisor-review.png` (not captured) |

### UAT-07 — Request changes and deliver feedback

| Field | Detail |
|---|---|
| UAT ID | UAT-07 |
| Actor | Advisor, then Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-07-advisor-decision.png`, `UAT-07-student-feedback.png` (not captured) |

### UAT-08 — Modify and resubmit the returned plan

| Field | Detail |
|---|---|
| UAT ID | UAT-08 |
| Actor | Student, then Advisor |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-08-resubmitted.png`, `UAT-08-revised-advisor-card.png` (not captured) |

### UAT-09 — Approve the revised plan

| Field | Detail |
|---|---|
| UAT ID | UAT-09 |
| Actor | Advisor, then Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-09-approved.png`, `UAT-09-student-approved.png` (not captured) |

### UAT-10 — Submit a separate plan for rejection

| Field | Detail |
|---|---|
| UAT ID | UAT-10 |
| Actor | Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-10-second-semester.png` (not captured) |

### UAT-11 — Reject the separate plan

| Field | Detail |
|---|---|
| UAT ID | UAT-11 |
| Actor | Advisor, then Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-11-rejected.png`, `UAT-11-student-rejection.png` (not captured) |

### UAT-12 — Submit a pending plan for cancellation checks

| Field | Detail |
|---|---|
| UAT ID | UAT-12 |
| Actor | Student, then Advisor |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-12-pending-c.png` (not captured) |

### UAT-13 — Remove a course from a Pending plan and protect the last course

| Field | Detail |
|---|---|
| UAT ID | UAT-13 |
| Actor | Student, then Advisor |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-13-last-course.png`, `UAT-13-advisor-updated.png` (not captured) |

### UAT-14 — Cancel an Approved plan

| Field | Detail |
|---|---|
| UAT ID | UAT-14 |
| Actor | Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-14-approved-cancelled.png` (not captured) |

### UAT-15 — Cancel a Rejected plan

| Field | Detail |
|---|---|
| UAT ID | UAT-15 |
| Actor | Student |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-15-rejected-cancelled.png` (not captured) |

### UAT-16 — Cancel a Pending plan and remove it from the review queue

| Field | Detail |
|---|---|
| UAT ID | UAT-16 |
| Actor | Student, then Advisor |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-16-pending-cancelled.png`, `UAT-16-queue-withdrawn.png` (not captured) |

### UAT-17 — Start a new plan after cancellation

| Field | Detail |
|---|---|
| UAT ID | UAT-17 |
| Actor | Student, then Advisor |
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
| Actual result | Not executed. |
| Pass/Fail/Not Run | Not Run |
| Tester | — |
| Date | — |
| Evidence filename | Planned: `UAT-17-new-plan.png`, `UAT-17-advisor-new-plan.png` (not captured) |

## Recording results and acceptance review

- After executing each case, replace **Actual result** with observed behavior and set **Pass/Fail/Not Run** to Pass or Fail. Enter the tester's name, actual execution date, and filenames of evidence actually captured. The filenames above are suggestions only; no files currently exist as execution evidence from this task.
- If a prerequisite fails or the environment/data is unavailable, leave dependent cases **Not Run** and explain the blocker in Actual result. Do not label an unattempted case Fail or Pass. Record defects with UAT ID, Student/semester, expected versus observed behavior, reproduction steps, and screenshot references.
- Capture status, semester, selection/credit totals, feedback, and confirmation dialogs where relevant. Use suffixes such as `-01`, `-02` for additional screenshots; avoid unrelated personal information. Evidence storage location: ___ (record before running).
- All 17 cases must be executed and their expected outcomes met for full workflow acceptance, with no unresolved defect preventing a required Student or Advisor task. Review the category-total inconsistency explicitly before acceptance; matching the seeded values alone does not resolve it. Any accepted exception needs a named reviewer and written rationale.
- End state if the full sequence succeeds: A Cancelled, B Cancelled, C Pending with E3. No cleanup is performed by this plan; preserve this state until evidence review is complete.

| Review record | Value |
|---|---|
| Passed / Failed / Not Run | 0 / 0 / 17 |
| Outstanding defects / accepted exceptions | Not yet assessed; see source/data inconsistency above. |
| Acceptance decision | Pending execution and review. |
| Reviewer | — |
| Review date | — |


## Current execution reconciliation — 5 November 2026

The original planned inputs, expected results and preparation-stage summaries above are historical and preserved. Current authoritative [UAT execution](../reports/uat-execution.md) records **8 Pass / 0 Fail / 12 Executed - Partially Verified / 0 Not Executed** across 20 cases, based on 55 new screenshots and the 5 November 2026 application date (local captures 4 November 2026, UTC−04:00). PASS: UAT-04, UAT-05, UAT-06, UAT-10, UAT-14, UAT-15, UAT-16, UAT-17. The remaining 12 cases have genuine primary-workflow evidence but missing substeps, not observed defects. Four before/after pairs are byte-identical, so refresh/separate-role checks remain partial.

The captures show the planned two-course execution: A COMP 1201 + MATH 2250 (2 courses/6 credits), revised A COMP 1201 + ENGL 1000 (2/6), B MATH 2250 (1/3), C COMP 1201 + MATH 2250 then COMP 1201 only, and replacement C ENGL 1000 only (1/3). Degree Progress categories total 93 (3/36, 3/18, 0/12, 0/18, 0/9). Exact substitutions, remaining substeps and evidence references are in the [final report](../reports/uat-final-report.md), [evidence matrix](../reports/uat-evidence-review.md) and [execution companion](../reports/uat-execution.md). Historical marked runs remain 113 unit and 194 integration; the latest corrected-build full run is 751 passed, one warning. Historical Postman remains 90 requests/470 assertions passed; the revised collection has not been rerun. No automated or browser workflow was rerun for this documentation update.
