# Targeted supplemental UAT evidence and status changes

> **Approved-allocation update ? 27 October 2026:** [Current correction record](degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


> **Superseded for current UAT disposition — 5 November 2026 application date (local captures 4 November 2026, UTC−04:00).** This document records the 28 October–3 November evidence position and is retained as history. Current UAT results are **8 PASS / 0 FAIL / 12 EXECUTED - PARTIALLY VERIFIED / 0 NOT EXECUTED** from 55 new screenshots, documented in the [final UAT report](uat-final-report.md), [execution companion](uat-execution.md) and [evidence matrix](uat-evidence-review.md). Its gaps are not erased; the same limitations that remain unverified are carried forward there.

**Corrected-build qualification ? 28 October 2026:** these UAT observations are historical and do not establish retesting of the corrected build. The latest corrected-build full pytest run is **751 passed, 1 warning, no failures/errors/skips**. The historical Postman run remains 90 requests / 470 assertions passed; the revised collection has not been rerun. Automated results do not replace manual evidence.

Reporting classification updated 3 November 2026 from the existing tester-confirmed observations and screenshots. No UAT workflow was rerun and no new observation was added.

## Confirmed clarification and current disposition

The tester reconfirms the existing observations for UAT-07/08/09/11/13/14/15/16/17 and UAT-20. Student Messages and Plan Courses approval with "Revised selection approved." is established, as are the previously recorded request-changes/rejection feedback, revised Pending queue, course removal, three cancellation states and replacement ENGL 1000 Pending plan (3 credits). These observations remain in the execution sheet and evidence matrix.

The clarification supplied no result for logged-in Student `/admin` HTTP 403, Advisor restricted-tab fallback, or repeated checks after refresh. At that 3 November stage they remained **unverified**, not failed or passed. Totals at that stage were **1 Pass / 0 Fail / 18 Executed - Partially Verified / 1 Not Executed - Unverified**: UAT-06 Pass, 18 partially verified cases, and UAT-05 without adequate evidence of its required Pending/relogin workflow. Missing evidence is not a defect. This paragraph is retained as history; the current 5 November position is in the superseding note above.

## Exactly which status entries could change

Each row below identifies the remaining evidence needed to upgrade its current disposition. Supply a case-specific observed result (including actual actor, semester, actions and outcome), with existing/new screenshot references where available. No additional screenshot is assumed to exist. Supplemental evidence for one substep updates that narrative only; it does not automatically pass the full case. If an attempted required outcome mismatches its preserved expectation, record Fail with the actual mismatch and evidence, then record any retest separately.

A = Year 1 semester 1; B = Year 1 semester 2; C = Year 1 semester 3. Existing initial A used MATH 1300/2200/2250 (9 credits); revised A used MATH 1300/2200/ENGL 1000 (9 credits). The original two-course expectations remain preserved with this execution deviation disclosed.

| Status entry | Specific supplemental results still needed | Potential status change |
|---|---|---|
| UAT-01 | Confirm totals/activity after refresh and observe the approved 93-credit allocation in a new build. The historical image shows the earlier 120-credit categories. | Executed - Partially Verified to Pass only when all required outcomes are established. |
| UAT-02 | Confirm semester switching, code and title searches, department and combined filters, no-match search and Clear Filters outcomes. | Executed - Partially Verified to Pass only when all required outcomes are established. |
| UAT-03 | Confirm empty-selection prevention, pre-submission ineligible controls, actual count changes, review total and Back preserving choices; actual A selected three Mathematics courses. | Executed - Partially Verified to Pass only when all required outcomes are established. |
| UAT-04 | Confirm refresh persistence and repeat submission prevention through the Pending form. | Executed - Partially Verified to Pass only when all required outcomes are established. |
| UAT-05 | Obtain adequate observation of the Pending Home/Messages state and selection retained after sign-out/sign-in. | Not Executed / Unverified until observed; then classify as partial or Pass based on coverage. |
| UAT-07 | Confirm Advisor action confirmation, removal from Pending queue, and Student Messages delivery (Student Plan Courses delivery is established). | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-08 | Confirm Student Pending state and review total for the actual 3-course/9-credit revision, current Pending Messages with prior feedback cleared, and exactly one revised Advisor queue entry after refresh. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-09 | Confirm Advisor action confirmation and Advisor Approved feedback/queue removal; Student refresh persistence. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-10 | Confirm switching between semesters preserves each separate selection/status; later UAT-11 supports retained approval, not every switch. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-11 | Confirm Advisor rejection confirmation/feedback and queue removal; Student rejected plan editability and Cancel availability. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-12 | Confirm Student Pending view and that A Approved/B Rejected were unchanged during this submission. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-13 | Confirm dismissing Remove changed nothing and refreshed Advisor queue showed COMP 1201/3 credits. Final-course UI guard is established; no forged removal request is claimed. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-14 | Confirm dismissing cancellation preserved approval, refresh persisted Cancelled, and Messages showed Cancelled. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-15 | Confirm refresh/Messages Cancelled and A Cancelled/C Pending unchanged. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-16 | Confirm Student Messages Cancelled, removal from refreshed Advisor Pending queue and preservation of other students if present. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-17 | Confirm Student refresh persistence and exactly one active new Advisor queue entry after refresh with ENGL 1000/3 credits. Historical Cancelled Messages entries are permitted, not a required additional check. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-18 | Confirm incorrect-login denial, valid-login destination, initial empty Messages/all A/B/C semesters and refresh retaining session. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-19 | Confirm incorrect-login denial, valid Advisor Home destination and refresh preserving independent Student/Advisor sessions. | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |
| UAT-20 | Confirm logged-in Student direct /admin 403, Advisor Student-tab fallback, unchanged queue, and fresh protected-page denial after each role signed out (which actor/URL for each). | Executed - Partially Verified to Pass only when all listed required outcomes are established; otherwise retain partial/unverified status. |

UAT-06 already passes the documented review objective with actual substituted data. It does not require a new refresh check or proof of invalid login to retain that disposition. New contradictory evidence could require reassessment; UI-01 remains an open usability concern.

For UAT-20 specifically, proof of Student 403 alone or Advisor fallback alone only verifies that substep. Full Pass also needs the remaining actor/URL-specific fresh signed-out loads and unchanged queue. The 401 screen is not evidence of the logged-in 403 result.

## Capture timing and preservation

Distinguish a tester's confirmation of an October 27 action from a newly executed supplemental check. Record the actual execution date for any new check; do not backdate it or label it an original capture. A screenshot after refresh needs a case-specific action/result record identifying that refresh; a state image alone does not establish the action. Historical decision/cancellation checks may need a fresh isolated sequence because A/B are now Cancelled and C has a replacement Pending plan. Do not infer earlier Pending or Approved behavior from the later state, or reset the existing evidence database merely to fill gaps. No new manual run or database reset is performed by this reporting update.

DATA-01 (120 category credits versus degree 93) and UI-01 (Advisor table contrast) remain disclosed. No accepted exception, fix or retest has been supplied. The reports are ready as inputs to Prompt 15 Final Quality Audit with open items; no acceptance sign-off is claimed.
