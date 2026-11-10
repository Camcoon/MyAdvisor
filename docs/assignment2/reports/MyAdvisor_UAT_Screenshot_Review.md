# MyAdvisor UAT Screenshot Review — Updated Evidence Set

## Scope and integrity

Evidence supplied as `UAT-Screenshots.zip`: **55 PNG files**, representing **51 distinct image byte sequences**, covering IDs **UAT-01–UAT-20**. This is visual evidence review, not a fresh execution of the application, and it is not proof by itself that every multi-step test was executed. Preserve earlier October evidence separately; the Advisor Review screenshots in this ZIP display **Submitted Nov 05, 2026** (possibly server/UTC-local date difference). Confirm the actual execution date with the tester instead of assuming it is October 27.

## File-to-case review

| Case | Principal screenshots | Visually demonstrated | Additional evidence or observation to confirm |
|---|---|---|---|
| UAT-01 | `UAT-01-degree-progress.png`; `UAT-01-after-refresh.png` | 6 completed, 3 in progress, 84 remaining, 93 required, categories 36/18/12/18/9, recent activity | The two files are byte-identical: the refresh action cannot be independently established by screenshots; ask tester whether refresh occurred. |
| UAT-02 | `UAT-02-search.png`; `UAT-02-department.png`; `UAT-02-no-results.png` | Code search COMP 1201, Mathematics-only filter, no-result state | Confirm title search, combined filters, nine semester choices and Clear Filters behavior if performed. |
| UAT-03 | `UAT-03-empty-selection.png`; `UAT-03-ineligible-courses.png`; `UAT-03-review-two-courses.png`; `UAT-03-selection-preserved.png` | Zero selected, ineligible course labels, review of COMP 1201 + MATH 2250 = 6 credits | Confirm attempted empty-selection advance, the actual click restrictions, and the 2-to-1-to-2 sequence. |
| UAT-04 | `UAT-04-submission-success.png`; `UAT-04-pending-after-refresh.png` | Successful Pending 2-course submission and saved selection | Confirm refresh and repeat-submission prevention steps. |
| UAT-05 | `UAT-05-home-pending.png`; `UAT-05-messages-pending.png`; `UAT-05-after-relogin.png` | **New evidence for previously unverified case:** Pending semester 1 on Home and Messages, plus Pending plan displayed in later screenshot | Confirm actual sign-out/sign-in occurred between screenshots. If tester confirms, reassess as Pass; do not retain Not Executed solely from old evidence. |
| UAT-06 | `UAT-06-advisor-pending-review.png` | Advisor sees Pending Semester 1 with COMP 1201 and MATH 2250, 6 credits, student details, decision actions | Strong visual support for primary full review objective. |
| UAT-07 | `UAT-07-advisor-feedback.png`; `UAT-07-student-message.png`; `UAT-07-editable-plan.png` | Changes Requested with same feedback across roles; returned plan editable | Confirm successful queue removal/refresh; not photographed separately. |
| UAT-08 | `UAT-08-revised-review.png`; `UAT-08-resubmitted-pending.png`; `UAT-08-advisor-revised-queue.png` | COMP 1201 + ENGL 1000, 6 credits, resubmitted Pending and Advisor queue | Confirm previous feedback reset in current Messages if required. |
| UAT-09 | `UAT-09-advisor-approved.png`; `UAT-09-student-approved-message.png`; `UAT-09-approved-after-refresh.png` | Both roles show Approved and matching feedback; approved course selection retained | Confirm queue removal, refresh and lock actions if required. |
| UAT-10 | `UAT-10-semester2-pending.png`; `UAT-10-semester1-still-approved.png` | Semester 2 MATH 2250 Pending; Semester 1 remains Approved | Main outcome supported. |
| UAT-11 | `UAT-11-advisor-rejected.png`; `UAT-11-student-rejected.png`; `UAT-11-rejected-editable.png` | Rejected with reason visible to both roles; editable returned plan | Confirm refreshed queue removal if required. |
| UAT-12 | `UAT-12-student-pending.png`; `UAT-12-advisor-pending.png` | Semester 3 Pending with COMP 1201 + MATH 2250 = 6 credits in both roles | Main outcome supported. |
| UAT-13 | `UAT-13-one-course-remaining.png`; `UAT-13-advisor-updated.png` | Removal confirmation, only COMP 1201 remains, Advisor sees 3 credits, last-course guard displayed | No `UAT-13-removal-dismissed.png` in ZIP. Ask whether Cancel in first confirmation was tested and observed to leave two courses. |
| UAT-14 | `UAT-14-cancellation-dismissed.png`; `UAT-14-approved-cancelled.png`; `UAT-14-messages-cancelled.png` | Approved unchanged after dismissed dialog (state shown), then Cancelled; Messages reflects cancellation | Confirm dialog was dismissed before first screenshot; state and final outcomes supported. |
| UAT-15 | `UAT-15-rejected-cancelled.png`; `UAT-15-messages-cancelled.png` | Previously rejected Semester 2 becomes Cancelled and appears in Messages | Main outcome supported. |
| UAT-16 | `UAT-16-pending-cancelled.png`; `UAT-16-messages-cancelled.png`; `UAT-16-advisor-queue-cleared.png` | Pending Semester 3 becomes Cancelled; Messages show Cancelled; Advisor queue empty | Main outcome supported. |
| UAT-17 | `UAT-17-new-selection-review.png`; `UAT-17-new-pending-plan.png`; `UAT-17-advisor-new-plan.png` | New Semester 3 Pending ENGL 1000 3 credits; Advisor sees the new active plan | Main outcome supported. |
| UAT-18 | `UAT-18-invalid-login.png`; `UAT-18-home.png`; `UAT-18-baseline.png` | Incorrect credentials message; authenticated Student Home before plans | Home/baseline images are byte-identical; initial other-semester checks and refresh action need tester confirmation. |
| UAT-19 | `UAT-19-invalid-login.png`; `UAT-19-advisor-home.png`; `UAT-19-after-refresh.png` | Incorrect credentials message and authenticated Advisor Home | Advisor Home/after-refresh images are byte-identical; actual refresh and independent sessions need tester confirmation. |
| UAT-20 | `UAT-20-student-403.png`; `UAT-20-advisor-plan-fallback.png`; `UAT-20-advisor-progress-fallback.png`; `UAT-20-student-401.png`; `UAT-20-advisor-401.png` | Student forbidden-response JSON (`detail: You are not authorized to access this resource`); Advisor Home from restricted Student tab URLs; styled 401 signed-out screen | `student-403` image doesn't visibly show numeric status code, so confirm actual 403 via browser DevTools/Network or server log. Student 401 and Advisor 401 images are byte-identical: cannot independently attribute each to separate logout sessions; get actual actor/URL confirmation. |

## Exact duplicate pairs (SHA-256-identical bytes)

1. `UAT-01-after-refresh.png` = `UAT-01-degree-progress.png`
2. `UAT-18-baseline.png` = `UAT-18-home.png`
3. `UAT-19-after-refresh.png` = `UAT-19-advisor-home.png`
4. `UAT-20-advisor-401.png` = `UAT-20-student-401.png`

Duplicate bytes are not proof of misrepresentation. They do mean the screenshots alone cannot establish distinct moments or actors.

## Recommended documentation action

Update `docs/assignment2/reports/uat-execution.md`, `docs/assignment2/reports/uat-final-report.md`, the evidence matrix, and the final PDF with the **new corrected-build UAT evidence**. Distinguish positive observed outcomes from action-specific checks requiring tester confirmation. Reassess UAT-05 as no longer unexecuted; its Home/Messages evidence is now present. Preserve historic evidence, don't fabricate a full 20/20 Pass total, and ask only the specific missing confirmations before finalizing statuses. After updating, visually verify the PDF while retaining the lecturer-mandated deliverables order and earlier Postman provenance.
