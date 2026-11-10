# MyAdvisor final UAT report

**Current reconciliation — 5 November 2026 application date (local captures 4 November 2026, UTC−04:00).** Tester: **Cameron Ramesar**. This report replaces the earlier 27 October 2026 UAT disposition with the evidence from **55 new UAT screenshots**. No application code, pytest run, Postman run or manual workflow was rerun for this documentation update. The earlier report is preserved verbatim in [the historical 27 October record](historical-2026-10-27/uat-final-report-27oct2026.md).

**Full-case totals: 8 PASS / 0 FAIL / 12 EXECUTED - PARTIALLY VERIFIED / 0 NOT EXECUTED (20 cases).**

| Status | Count | Cases |
|---|---:|---|
| PASS | 8 | UAT-04, UAT-05, UAT-06, UAT-10, UAT-14, UAT-15, UAT-16, UAT-17 |
| EXECUTED - PARTIALLY VERIFIED | 12 | UAT-01, UAT-02, UAT-03, UAT-07, UAT-08, UAT-09, UAT-11, UAT-12, UAT-13, UAT-18, UAT-19, UAT-20 |
| FAIL | 0 | — |
| NOT EXECUTED | 0 | — |

The tester personally executed the workflows and supplied the captures. Every case has genuine screen evidence for its primary workflow. A PASS requires the complete documented outcome, including the specific refresh, dismissal, queue or separate-session check; the existence of a plausibly named screenshot is not sufficient when it duplicates another file.

Scope: WF1 Degree Progress, WF2 Plan Semester Course Selections, WF3 Advisor Review; supporting authentication, cancellation and replacement. [Original plan](../test-plans/uat-test-plan.md), [detailed execution companion](uat-execution.md), [55-image evidence matrix](uat-evidence-review.md).

## Corrected actual data

The new screenshots show the planned two-course selections, not the earlier three-course Mathematics execution:

| Plan | Courses | Load | Outcome |
|---|---|---|---|
| A initial (Year 1 semester 1) | COMP 1201 Object-Oriented Programming; MATH 2250 Industrial Statistics | 2 courses / 6 credits | Pending → Changes Requested → revised |
| A revised | COMP 1201; ENGL 1000 Academic Writing | 2 courses / 6 credits | Pending → Approved → Cancelled |
| B (Year 1 semester 2) | MATH 2250 only | 1 course / 3 credits | Pending → Rejected → Cancelled |
| C (Year 1 semester 3) | COMP 1201 + MATH 2250, then COMP 1201 only | 2 / 6 then 1 / 3 | Pending → course removed → Cancelled |
| C replacement | ENGL 1000 only | 1 course / 3 credits | New Pending plan |

Degree Progress shows completed 6, in progress 3, remaining 84, total required 93 and overall 6/93 (6%). Categories are Core 3/36, General Education 3/18, Electives 0/12, Major Requirements 0/18, Additional Requirements 0/9 — **93 total**, resolving the earlier 120-credit display mismatch in this capture. Recent activity shows MATH 1200 and COMP 1101 Completed (Nov 2026) and COMP 1600 In Progress.

Application-rendered Student and Advisor dates are **Nov 05, 2026**; local file timestamps are 4 November 2026, 20:13–21:21, UTC−04:00. This is recorded as one execution session with a server/application clock difference, not two runs.

## Actual outcomes against preserved expectations

| Case | New screenshot-supported outcome | Remaining unverified substep(s) | Status |
|---|---|---|---|
| UAT-01 | Degree totals, correct 93-credit categories and recent activity are visible. | The "after refresh" file is byte-identical to the initial image, so reload persistence is not independently proven. | EXECUTED - PARTIALLY VERIFIED |
| UAT-02 | COMP 1201 code search, Mathematics department filter and no-match/Clear Filters message are visible. | Title search, semester switching, combined filters and the catalogue after Clear Filters are not captured. | EXECUTED - PARTIALLY VERIFIED |
| UAT-03 | Empty selection, ineligible messages, two-course review (6 credits) and preserved selection are visible. | Zero-selection click prevention, the exact planned ineligible examples, and 0 → 2 → 1 → 2 counts are not captured. | EXECUTED - PARTIALLY VERIFIED |
| UAT-04 | Submission success; distinct after-refresh Pending state with locked selection. | None for the documented outcome. | PASS |
| UAT-05 | Pending Home (2 courses/6 credits), Pending Messages and distinct post-relogin Pending Plan. | None for the documented outcome. | PASS |
| UAT-06 | Correct Student identity/ID/program, Submitted Nov 05 2026, A Pending, two courses/6 credits, comments counter and all three decisions. | None for the review objective; human contrast acceptance is not a case substep. | PASS |
| UAT-07 | Advisor Messages, Student Messages and editable returned plan show the exact change request. | Advisor action confirmation and Pending-queue removal are not captured. | EXECUTED - PARTIALLY VERIFIED |
| UAT-08 | Revised Student Pending, revised review (6 credits) and revised Advisor queue are visible. | Current Pending Messages with prior feedback cleared is not captured. | EXECUTED - PARTIALLY VERIFIED |
| UAT-09 | Advisor Approved message, Student Approved after reload and Student Approved message are visible. | Advisor action confirmation and queue removal are not captured. | EXECUTED - PARTIALLY VERIFIED |
| UAT-10 | A remains Approved; B is Pending with only MATH 2250 (1 course/3 credits). | None for the separate-plan objective. | PASS |
| UAT-11 | Advisor rejection, Student rejection and editable rejected B are visible with the exact feedback. | Advisor action confirmation and queue removal are not captured. | EXECUTED - PARTIALLY VERIFIED |
| UAT-12 | Advisor and Student show C Pending with COMP 1201 + MATH 2250 (6 credits). | A Approved and B Rejected are not co-visible with this C state. | EXECUTED - PARTIALLY VERIFIED |
| UAT-13 | Removal success; C Pending with COMP 1201 only; Advisor total 1 course/3 credits; final-course guard. | The Remove-confirmation dismissal/no-change state is not captured. | EXECUTED - PARTIALLY VERIFIED |
| UAT-14 | A Cancelled with feedback retained; dismissal keeps A Approved; Messages shows A CANCELLED, B REJECTED, C PENDING. | None for the documented outcome. | PASS |
| UAT-15 | B Cancelled with rejection feedback retained; Messages shows A/B CANCELLED and C PENDING. | None for the documented outcome. | PASS |
| UAT-16 | C Cancelled with zero selection; Messages shows all three CANCELLED; Advisor queue "All caught up". | None for the documented outcome. | PASS |
| UAT-17 | New C review and Pending with ENGL 1000 only; exactly one active Advisor card at 3 credits. | None for the documented outcome. | PASS |
| UAT-18 | Invalid-credential denial and empty Student Home baseline are visible. | Empty A/B/C Plan Courses, empty Messages and independent refresh are not captured; refresh file is identical. | EXECUTED - PARTIALLY VERIFIED |
| UAT-19 | Invalid-credential denial and Advisor Home/identity/navigation are visible. | Independent refresh and simultaneous separate Student/Advisor sessions are not captured; refresh file is identical. | EXECUTED - PARTIALLY VERIFIED |
| UAT-20 | Logged-in Student 403 JSON, Advisor plan/progress fallbacks and one signed-out 401 page are visible. | Separate Student and Advisor post-logout checks are not independently established; the 401 files are identical. | EXECUTED - PARTIALLY VERIFIED |

## Duplicate captures

Four "after" images are byte-identical to their baselines and are not treated as independent proof:

| Pair | SHA-256 |
|---|---|
| `UAT-01-degree-progress.png` = `UAT-01-after-refresh.png` | `6D9BBB95D76E65CE127A6C0DE8ED879AD533F141C188F71FEF6BD6DD322E0DD2` |
| `UAT-18-baseline.png` = `UAT-18-home.png` | `599424290DB0DD8079D36EEF90B624A15A1EC55637E5A96BC37ED13C3A04036A` |
| `UAT-19-advisor-home.png` = `UAT-19-after-refresh.png` | `AE469C9DC5B70FF803F9B1A52432D625CB7F61289A521E7C64FBC2D25868326C` |
| `UAT-20-student-401.png` = `UAT-20-advisor-401.png` | `67052C79456AAF8B19A4B12CC136E9CE333CCAE7FEA508A8B6F13CF278A26E52` |

No other screenshots share a hash. The four pairs remain in the evidence set and PDF attachments; their captions disclose the duplication.

## Automated results (separate evidence, not rerun)

- **Latest corrected-build full pytest run:** **751 passed, 1 warning, 0 failures/errors/skips**, exit 0; 116 unit / 227 integration / 408 other nodes are memberships in that single run.
- **Historical marked runs:** Unit **113 passed / 602 deselected / 1 warning**; Integration **194 passed / 521 deselected / 1 warning**. These are earlier runs and overlap the full suite; they are not additive.
- **Historical Postman Runner:** **90 requests, 470 assertions passed, 0 assertion failures, 0 execution errors, 1 iteration**, using the earlier collection revision. The revised degree93 collection was not rerun.
- Automated results do not supply any missing manual substep. No UAT case is marked PASS because of pytest or Postman.

## Issues and acceptance

- **No observed UAT failure.** The 12 partial cases have evidence gaps, not contradicted outcomes. Nothing in the new set establishes a regression.
- **DATA-01 (display) is resolved in UAT-01.** The new capture's categories total 93. The historical 120-credit screenshot and its description remain preserved in the archived 27 October matrix and the old PDF.
- **UI-01 (contrast) is not re-certified.** The new captures render Advisor table text, but no contrast measurement or accessibility review was performed. UAT-06's PASS is a review-objective result, not an accessibility sign-off.
- **Remaining UAT evidence gaps:** UAT-01 refresh; UAT-02 title/combined/Clear Filters; UAT-03 empty-selection prevention and count sequence; UAT-07/09/11 action confirmation and queue removal; UAT-08 cleared-feedback Messages; UAT-12 co-visible A/B states; UAT-13 confirmation dismissal; UAT-18 empty A/B/C and refresh; UAT-19 separate sessions and refresh; UAT-20 separate post-logout checks.
- **Not an acceptance certificate.** The pass count reflects the documented UAT outcomes only. It does not certify production security, accessibility, deployment or unpreserved environments.

## Unresolved submission requirements

1. **Evidence gaps above** remain the only UAT-specific blockers to a higher pass count; they are not application failures.
2. **Automated/Postman provenance:** the 751-pass run and 90-request/470-assertion Runner evidence are historical. No fresh pytest or Postman run was made for this update, and the revised Postman collection remains unexecuted.
3. **Repository publication:** the current local collection and evidence were not pushed or republished. The repository link in the PDF therefore still points to the previously published revision.
4. **Historical UAT originals absent:** no 27 October UAT screenshot folder or original UAT PNGs were found. The 27 October reports are preserved, but the original images cannot be re-embedded; no substitute image was fabricated.
5. **Unchanged open engineering/security decisions:** CSRF/trusted-origin design, production signing-key disposition and deployment verification remain outside this UAT update and are not resolved by these screenshots.

## Historical record

The prior 27 October 2026 disposition (**1 Pass / 0 Fail / 18 Executed - Partially Verified / 1 Not Executed - Unverified**, 19 images, three-course Mathematics data) is retained in:

- [uat-final-report-27oct2026.md](historical-2026-10-27/uat-final-report-27oct2026.md)
- [uat-execution-27oct2026.md](historical-2026-10-27/uat-execution-27oct2026.md)
- [uat-evidence-review-27oct2026.md](historical-2026-10-27/uat-evidence-review-27oct2026.md)
- [uat-supplemental-evidence-27oct2026.md](historical-2026-10-27/uat-supplemental-evidence-27oct2026.md)

Those records are superseded for current reporting, not deleted or rewritten. The original 57-page PDF and the earlier final PDF also remain unchanged.
