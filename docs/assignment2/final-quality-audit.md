# MyAdvisor — final quality audit

> **Approved-allocation update ? 27 October 2026:** [Current correction record](reports/degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.

## Current post-approval disposition

F05/DATA-01 is resolved for configured/seeded fictional data and the observed local requirement rows: 36 + 18 + 12 + 18 + 9 = 93. The dedicated local migration was a no-op because the database already matched. Existing database byte hashes could not be read due to a file lock; no equality claim is made. Affected selection: 46 passed; full run: **751 passed, one warning, zero failures/errors/skips, exit 0**, with 74 unchanged app/test hashes. Historical 735/284 and old marked/Runner/UAT evidence remain separate.

Public main is now edc71e8d8fadecc6c2d173eeddce1a66360a6126 and contains the earlier exported JSON and 735-build source. F02's old JSON-404 observation is historical. The revised degree code/JSON, current raw evidence/reports and original UAT/Runner PNGs remain unpublished. Current publication and retest gates are recorded in [the completion checklist](completion-review-2026-10-27/remaining-actions.md). F09/F15 remain open; F13 exact oracles are implemented but new Runner execution is pending. Human UAT remains 1 Pass / 0 Fail / 19 Not Run, with 18 partial cases and UAT-05 unverified. No replacement PDF has been generated.



## Current correction disposition ? 27 October 2026

**This addendum supersedes historical open/source-unchanged statements below only for the verified corrections.** See the [correction report](reports/audit-correction-report.md) for actual commands, source hashes, raw output and deployment decisions. No Critical finding was verified; **F01 is fixed locally**, F07/F08 are fixed locally, and F06 passes automated computed-style checks with fresh human acceptance pending. High F02/F03 publication and F04 manual completion remain open; **F05 is pending project-owner approval**, with curriculum values unchanged. The owner confirms these are fictional demonstration requirements, not official university curriculum.

Final corrected-build checks: **284 targeted passed** and **735 complete-suite passed**, each with 1 warning, zero failures/errors/skips and exit 0. All 70 recorded application/test source hashes remain unchanged after execution. Complete-run membership is 113 unit / 214 integration / 408 other nodes; no new separate marked selection is claimed. New regressions cover wrong-role HTML denials before writes, full unchanged-DB snapshots, runtime engine foreign keys, invalid/valid registration and actual template contrast including hover.

Historical Postman 90 requests / 470 assertions and UAT **1 Pass / 0 Fail / 19 Not Run** remain historical, with all 19 UAT images preserved. **New-build Postman/manual retesting is pending**: [exact instructions](reports/correction-retest-guide.md). F09/F15 remain open deployment-security decisions; no live settings or secrets were inspected. The [publication plan](reports/repository-publication-plan.md) requires later approval; wrong origin is unchanged and no content was pushed.

The existing **139-page PDF is preserved unchanged and stale for this corrected build**. It was created after the historical audit below; D1's historical Missing classification is superseded by the assembly checklist, not a new readiness claim. **No revised PDF generated; not submission-ready.**

---

## Preserved Prompt 15 audit (earlier build)

**Audit date:** 27 October 2026 (America/La_Paz). **Decision:** material issues remain; **not ready for final PDF generation or submission sign-off**. No grade is assigned. No application/test source, degree requirements, Git history, remote, or existing screenshot was changed. No final PDF was generated.

The independent review found substantial implemented and tested functionality, but also reproduced an authorization bypass that allows an Advisor to create and approve their own plan. Passing all existing tests does not close that defect. The published repository also lacks the required Postman JSON and current manual/API evidence.

## Requirements source and audit scope

The student supplied the official Assignment 2 text during this audit. Its wording and four **25%** rubric components are preserved in the [brief source record](official-assignment-brief.md), with attribution. Root [ASSIGNMENT.md](../../ASSIGNMENT.md) explicitly describes Assignment 1; its different weights and historical Judge scores are not used to grade Assignment 2. The two linked Google test-plan documents could not be retrieved; their detailed template contents remain **Not verified**. No additional requirements are invented from them.

Audited working root: the nested `Assignment 2/` directory containing this document's `app/`, `tests/`, and `docs/`. Its local HEAD is `679b9250c13f38a2f97ed4e6d08a325fe48219d3`, with substantial pre-existing modified/untracked Assignment 2 work; its origin is `Camcoon/MyAdvisor`. The separate `myadvisor-upload-yfjf6d9s/` working checkout is not assumed to be GitHub's current committed content.

The GitHub connector independently resolved [MyAdvisorWithTests](https://github.com/Camcoon/MyAdvisorWithTests) as public, default branch `main`, and inspected commit [864386fe10fa5e61869e07500d84e51ff7e46b9b](https://github.com/Camcoon/MyAdvisorWithTests/commit/864386fe10fa5e61869e07500d84e51ff7e46b9b). Its complete recursive tree has 430 entries, including 343 file blobs; it was not truncated. The [remote snapshot](evidence/audit/github-snapshot.json) and [local comparison](evidence/audit/local-remote-comparison.json) retain the inspected paths/hashes. All **67 published top-level application and test files** match the working files by Git blob hash, allowing CRLF/LF normalization. Before this audit's corrections, 329 published files matched and 14 differed, primarily reports/plans and four login YAML definitions. This establishes code-file parity, not the historical build used for each screenshot.

Methods: read source, test plans, reports and retained logs/XML; inspect the original wireframe and all 31 execution PNGs (19 UAT, 6 pytest, 6 Postman); compare public files; scan text for secrets without disclosing candidate values; run the static Postman validator; independently run the existing full pytest suite; reproduce specific defects only in disposable databases. No live deployment, manual browser sequence, Postman runtime, concurrency, or PostgreSQL run was performed.

## Official rubric compliance

The following IDs are **audit labels**, not invented official rubric IDs. Wording and weights come from the supplied brief. Satisfied means supported within the stated local scope, not unconditional acceptance of every feature.

| Audit label | Official component / requirement | Weight | Classification | Evidence and marking risk |
|---|---|---:|---|---|
| I1 | Appropriate views implemented to facilitate minimum viable feature set | Implementation 25% | Partially satisfied | WF1–WF3 views and workflows exist; WF1 requirements discrepancy and Advisor table readability remain open (F05/F06). |
| I2 | Authorization implemented | Same component | Partially satisfied | Real role/ownership guards work for JSON and Advisor routes; HTML Student actions allow an Advisor to submit and self-approve (F01). |
| I3 | Views follow REST API conventions | Same component | Satisfied | Resource-based JSON paths, GET reads, POST creation with 201/Location, PUT replacement, DELETE cancellation/removal, structured 401/403/404/409/422 responses. Named Advisor POST actions are documented; legacy HTML forms use redirects. This does not close I2. |
| P1 | Appropriate unit testing of modules in isolation | Test Plans 25% | Satisfied | UT-01–23 specify repository doubles, inputs, independent arithmetic, negative cases and boundaries. |
| P2 | Integration tests covers main functionality of the application | Same component | Partially satisfied | IT-01–20 cover main Student/Advisor interactions and persistence. HTML Advisor-to-Student mutation denial and actual engine FK configuration are missing from the planned scope (F01/F07). |
| P3 | UAT’s give reasonable tasks/success criteria that can be completed/validated by the user | Same component | Satisfied | Three original wireframe panels mapped to concrete browser tasks; 17 original cases plus 3 supporting authentication/access cases. Steps and expected outcomes are executable. Template-specific formatting remains Not verified. |
| T1 | Tests implemented according to test plans | Test Implementation 25% | Partially satisfied | Every UT/IT group has source coverage, with explicit unit/integration boundaries. This is strong implementation traceability, but source-derived oracles leave F01/F05/F07 uncovered; manual execution is incomplete. |
| T2 | Unit & Integration tests are runnable via the CLI | Same component | Satisfied | Existing marked-run screenshots and independent complete-suite execution, exit 0. All 113 unit and 194 integration nodes occur in the new full-run XML. |
| T3 | All postman test scripts implemented for API testing | Same component | Satisfied locally | 90 requests, 93 compiled script blocks, all 15 JSON API operations; meaningful state/read-back/error assertions. F13 qualifies calculation completeness. |
| T4 | Postman collection runnable | Same component | Partially satisfied | Local v2.1 JSON plus existing successful Runner evidence. Required JSON is absent from published main (F02); a remote clone cannot follow the import instructions as published. |
| R1 | Screenshots of passing unit and integration tests | Test Reporting 25% | Satisfied | Six readable original screenshots support 113/194 marked runs with one warning each. These six are also published. |
| R2 | Screenshots of passing collection run on postman | Same component | Partially satisfied | Six local readable captures cover requests 01–90 and the same completed 470-assertion run. None is published in the inspected remote tree (F03). |
| R3 | Completed User Acceptance Test report | Same component | Partially satisfied | Detailed honest execution/report records exist; 1 Pass, 18 partial cases, 1 unverified case. Completion/acceptance remains outstanding (F04). |
| D1 | Submit 1 PDF document containing the listed deliverables | Final deliverable; no separate weight specified | Missing | Assignment 2 single-PDF package has not been produced, intentionally under this instruction. Existing `docs/report.pdf` and `docs/report.md` are Assignment 1 materials, not the required A2 compilation. |

No component subtotal or fabricated numerical grade follows from these classifications. Biggest marking risks affect Authorization, runnable published API tests, completed UAT reporting, and the final package.

## Implementation and workflow verification

Primary sources: [service](../../app/services/advising_service.py), [repository](../../app/repositories/advising.py), [models](../../app/models/advising.py), [JSON routes](../../app/routers/advising_api.py), [HTML Student routes](../../app/routers/user_home.py), [Advisor routes](../../app/routers/admin_home.py), [authentication](../../app/dependencies/auth.py), and [API contracts](api.md).

| Requested check | Verified behavior / qualification | Disposition |
|---|---|---|
| Student authentication | Password verification, signed cookie login, subject/expiry/signature validation and current database identity; real-login integration cases. | Satisfied in automated scope; manual login sequence partial |
| Advisor authentication | Existing `admin` role, same login service, separate test clients/cookie jars. | Satisfied in automated scope; manual login sequence partial |
| Role authorization | Student/Advisor JSON guards use current DB role, not JWT role claim; Student `/admin` denied 403. HTML Student mutation actions use only AuthDep. | Partially satisfied — F01 |
| User ownership | Student identity taken from cookie; foreign/missing plan IDs return identical 404; unauthorized writes preserve committed data. | Satisfied for tested Student operations |
| Degree calculations | Completed and in-progress sets summed separately; remaining=max(total−completed−in-progress,0); progress=rounded completed/total, capped at 100. Category earned uses completed only. | Arithmetic satisfied; requirement semantics partial — F05 |
| Completed/in-progress courses | Academic records and activity shown; both tracked states blocked from selection; only completed prerequisites count. | Satisfied within recorded data |
| Course eligibility/prerequisites | All comma-separated codes must be completed; missing/unknown codes named. Empty prerequisites eligible. Same service feeds HTML/JSON. | Satisfied within supported rule; no semester-offering guarantee claimed |
| Semester plan creation/submission | Nine exact semesters, trimming, nonempty unique existing eligible course IDs, atomic plan/link creation, 201+Location for new API resource. | Satisfied for Student; F01 allows wrong actor through HTML |
| Advisor review | Shared global Pending queue; identity/program, date, courses and totals. No assignment-specific Advisor ownership rule is specified. | Functional scope satisfied; readability defect F06 |
| Request Changes | Pending→Changes Requested; trimmed feedback/reviewer stored; editable Student return. | Satisfied in automated scope; manual substeps partial |
| Student resubmission | Rejected/Changes Requested→Pending, same ID, replaced course links, new submission time, previous feedback/reviewer cleared. | Satisfied in automated scope; manual reset/refresh checks partial |
| Approval / rejection | Pending→Approved or Rejected only; all three decisions permit optional feedback; raw 500-char limit; repeat/non-Pending review rejected; conditional DB status update prevents stale review overwrites. | Satisfied for legitimate Student plans; F01 permits self-created Advisor plan |
| Feedback persistence/visibility | Owned Student Plan Courses/Messages and Advisor decisions expose current feedback; cancellation retains it; resubmission intentionally clears it. | Satisfied for current feedback; immutable historical review log is not claimed or required |
| Cancellation | Only owned Pending/Approved/Rejected plans cancel; history/course links retained; Changes Requested/Cancelled denied; replacement gets new ID. | Satisfied in tested Student scope |
| Course removal | Owned Pending only; selection membership checked; cannot remove final course. | Satisfied in automated scope; manual dismissal/queue checks partial |
| State transitions | Submission blocked for existing Pending/Approved; returned plan resubmits; Cancelled allows new plan. Tests exercise allowed and rejected transitions. | Satisfied sequential scope; concurrency not established |
| Database persistence | Fresh request/session reads, separate logged-in clients, constraints/rollback tests; create/resubmit recover from forced failure. Actual default SQLite engine leaves FK enforcement off. | Partially satisfied — F07 |
| Existing Assignment 1 functionality | Original views, login/register, profiles, navigation, wireframe and diagrams retained; legacy tests remain and passed in full run. Invalid registration email returns 500. | Partially satisfied — F08; no blanket live regression sign-off |

### Degree credit investigation — DATA-01 / F05

**Classification: Unresolved requirements issue.** The contradictory configured/displayed values are verified; a particular corrected total is not established by an authoritative degree specification. There is no evidence to call the discrepancy intended overlap.

- `DEFAULT_TOTAL_CREDITS=93` in the service and `DegreeProgram.total_credits=93` in the model. `ensure_demo_data()` inserts the program with 93 and inserts category requirements **36+18+18+24+24=120**. Existing records are not automatically reconciled when already present.
- `DegreeRequirement` stores an independent `(program_id, category, required_credits)` row. `Course.category` is a **single string**. `earned_by_category` credits each completed course to that one exact category. There is no many-category mapping, cross-category credit allocation, overlap configuration, or documented double-counting policy.
- Overall progress reads `program.total_credits`; category rows independently read `required_credits`. Neither calculation reconciles the other. Thus the implementation can show 100% overall while some mandatory-looking category requirements remain unmet. No graduation-complete business rule is implemented or inferred here.
- Seed catalogue: 26 courses × 3 credits = 78; none has category Additional Requirements. This is demonstrably a demo catalogue, not evidence that the application can fulfill every configured category. Do not mistake that limitation for a separate officially specified full-curriculum feature.
- The original wireframe shows **120 total credits** and four drawn category denominators totaling **96** (36+18+18+24). It does not establish the five-category 120-credit configuration or authoritative overlap semantics. Its remaining card also illustrates a different in-progress treatment. Existing local plans explicitly document the implemented formulas; the drawing cannot alone justify changing them.
- Screenshot [UAT-02](screenshots/UAT/UAT-02.png) verifies 6 completed, 3 in progress, 84 remaining, total 93, 6%; category earned values total 6 and required values total 120. Arithmetic is reproducible; consistency of degree requirements is unresolved.

**Effect on WF1:** the Student cannot confidently reconcile remaining overall credits with category obligations. The current tests assert configured behavior, so they do not validate curriculum correctness. Obtain an authoritative program requirement or a written project-owner decision explaining additive/overlapping/independent semantics. Then specify approved values/allocation rules, update configuration/calculation only as justified, and revise corresponding test expectations. Preserve original UAT planning data and record any approved change as a new revision; do not silently rewrite old expected/actual results. No requirement values were changed in this audit.

## Test planning and automated assertions

[Unit plan](test-plans/unit-test-plan.md), [integration plan](test-plans/integration-test-plan.md), [UAT plan](test-plans/uat-test-plan.md), and [traceability matrix](reports/requirements-test-traceability.md) were inspected against source and the original wireframe. R01–R15, UT-01–23, IT-01–20 and W1–W5 are local planning labels. Parameter variants are not additional requirements or separate UAT cases.

Strengths verified:

- Unit fixture replaces repository constructors with autospecced doubles and a nonfunctional session; Engine connection guard prevents accidental DB use. Tests assert literal expected arithmetic, exact validation outcomes, and absence/presence of repository calls. UT-23 uses real local hashing/JWT signing; the retained mocked login test checks only redirect orchestration, correctly described as a companion.
- Integration F2 uses a fresh in-memory SQLite database per variant, real Argon2 login and JWT validation, separate role cookie jars, fresh Sessions for full-table snapshots, isolated lifespan and guards against connecting to other engines. It restores overrides/settings and disposes the engine. Forced rollback cases prove unchanged committed state and reuse the same recovered Session for a successful write.
- API files verify response allowlists/privacy, errors and headers, ownership, denied-write read-back, strict ID/payload validation, current DB role overrides, review decision/feedback and state persistence. Legacy tests that override an admin dependency do not independently prove authorization; separate real-auth suites supply that evidence.
- Boundary/negative inputs include zero denominators, empty records, over-credit caps, duplicates, unknown/in-progress prerequisites, invalid semesters and IDs, foreign ownership, absent/malformed/expired credentials, feedback lengths 499/500/501 and whitespace before trimming, forbidden state changes, SQL uniqueness and forced transaction failure.
- Postman has 90 ordered requests and 93 script blocks across five folders; all 15 JSON operations map to actual routes. Password/token variables are blank on export, IDs are discovered dynamically, local URL is constrained, redirects/cookie jars are disabled, explicit Student/Advisor/other cookies preserve actor separation, and failed assertions stop the chain. Repeat runs choose an available semester and retain two cancelled plans plus a new isolation Student; repeatable does not mean leaving no history.

Limits that passing tests do not close:

- There is no negative test for an Advisor POSTing to the HTML Student plan actions. The plan even acknowledges AuthDep-only behavior; that accurately describes implementation but omits a role requirement (F01).
- Both isolated calculation fixtures and Postman checks validate configured arithmetic, without an independent degree requirement oracle (F05). Postman request 19 checks percentage range, not the exact completed/total formula; catalogue discovery mostly trusts `eligible` from the server. Unit/integration prerequisite tests supply independent expected eligibility, but the collection alone is narrower than a full business-rule proof (F13).
- Test SQLite foreign keys are explicitly enabled; ordinary application SQLite connections do not enable them (F07). Passing constraint tests cannot establish default runtime enforcement.
- Postman requests 87–89 verify cookie-clearing responses and clear token variables; request 90 sends an empty Cookie header. This establishes denial without a cookie, **not revocation of an issued JWT**. Current reports correctly disclose that limit; a stolen pre-logout JWT remains a separate untested lifecycle concern until expiry.
- API read-back is meaningful persistence evidence, but does not establish disk restart, multi-user races, production/PostgreSQL behavior, browser JavaScript behavior or accessibility. Full-suite total includes 408 additional unmarked tests; it is not 715 isolated unit tests. No line/branch coverage percentage was measured.

### Verified execution totals and provenance

| Record | Result | Audit interpretation |
|---|---|---|
| Existing marked Unit screenshots, 26 Oct | 113 passed, 602 deselected, 1 warning, 6.23s | Visually verified; raw latest marked-run export/tester/commit absent. Earlier 113/408-deselected log/XML is historical. |
| Existing marked Integration screenshots, 26 Oct | 194 passed, 521 deselected, 1 warning, 30.52s | Visually verified; complete latest marked raw export absent. Earlier 59-test Student log is historical. |
| Earlier full-suite user record | 715 passed, 1 warning, 56.83s | Attributed historical result, not independently reconstructed from marked screenshots. |
| **Independent audit full-suite rerun, 27 Oct** | **715 passed, 0 failures/errors/skips, 1 warning, 76.25s; exit 0** | New retained [text output](evidence/audit/pytest-output.txt), [JUnit XML](evidence/audit/pytest-results.xml), [run metadata and source hashes](evidence/audit/pytest-run.json). Includes 113 unit nodes, 194 integration nodes and 408 other nodes; no separate marked rerun is claimed. |
| Existing Postman Runner, 27 Oct | 90 requests, 470 assertions passed, 0 assertion failures, 0 execution errors, 1 iteration | Six visually inspected captures of one run; user-confirmed date/local server. No Runner result export/tested build archive. No audit runtime rerun. |
| Static Postman validator during audit | Exit 0: JSON, 90 requests, 93 scripts compile, 15 API operations | Definition validation only; not runtime, external-schema validation or a new pass count. |

The new full command was `.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider --basetemp=<unique temporary directory>/pytest-base --junitxml=docs/assignment2/evidence/audit/pytest-results.xml`. The unique parent was newly created, so pytest could not delete an existing user directory. A separate unused bootstrap SQLite URI and test signing key were supplied to that process; bootstrap DB was not created. Unit/integration fixtures used disposable databases. Source hashes identify this run's files; remote code parity is established separately. No historical screenshot is presented as evidence of this new execution. The known `StarletteDeprecationWarning` concerning TestClient/httpx remains visible; dependencies were not changed.

## Manual UAT: independent review of all 20 cases

The original wireframe, [execution sheet](reports/uat-execution.md), [final report](reports/uat-final-report.md), [19-image mapping](reports/uat-evidence-review.md) and [supplemental checklist](reports/uat-supplemental-evidence.md) agree on **1 Pass / 0 Fail / 19 Not Run**. Of those Not Run entries, **18 are partially verified** and UAT-05 lacks its required workflow evidence. This convention is explained, although “incomplete” is clearer than “unattempted.” An evidence gap is not an observed functional failure.

Tester **Cameron Ramesar** and execution **27 October 2026** are supported by the prior Prompt 14 records explicitly attributing confirmation to the user; they are not inferred from the seeded account. Review/submission cards corroborate the date. The original confirmation conversation is not separately archived here, and exact times, browser/version, database path and tested commit remain unverified. The audit did not personally execute the browser sequence.

| Case | Independently visible evidence and remaining limitation | Classification retained |
|---|---|---|
| UAT-01 | `UAT-02.png`: 6/3/84/93, 6%, category rows and activity. Refresh and DATA-01 disposition absent. | Not Run — partial |
| UAT-02 | `UAT-03.png`: math search, all departments, three eligible Mathematics courses. Semester/code/title/combined/no-match/clear outcomes absent. | Not Run — partial |
| UAT-03 | `UAT-03/04`: three checked courses/count 3; later locked ineligible rows. Empty selection, pre-submit restriction attempts, count sequence, review/Back outcomes absent. | Not Run — partial |
| UAT-04 | `UAT-04.png`: submission success and Pending three-course selection; Remove/Cancel visible. Refresh/duplicate attempt absent. | Not Run — partial |
| UAT-05 | No matching Pending Home/Messages and logout/relogin evidence. Later decision Messages do not establish this case. | Not Run — unverified |
| UAT-06 | `UAT-05.png`: correct Student/program, Pending semester, codes, three-course/9-credit total and three decisions. Data substitution documented. Titles/row credits/prerequisites have severe contrast limitations. | Pass for recorded review objective only; F06 prevents usability sign-off |
| UAT-07 | Both `UAT-07` images show Changes Requested and matching replacement feedback, original three choices editable. Advisor confirmation, refreshed queue removal and Student Messages delivery absent. | Not Run — partial |
| UAT-08 | `UAT-08-resubmitted.png`: revised ENGL 1000/MATH 1300/MATH 2200 Pending, 9 credits. Student review/Pending Messages/reset feedback and unique refreshed queue entry absent. Blank Advisor textarea is not stored-feedback proof. | Not Run — partial |
| UAT-09 | `UAT-09-approved.png` and UAT-11 Messages: Approved and “Revised selection approved.” Retained revised courses. Advisor confirmation/queue and refresh absent; approval explanatory text also low contrast. | Not Run — partial |
| UAT-10 | `UAT-10-second-plan.png`: separate semester 2 Pending with MATH 2250, 3 credits. Bidirectional semester switching/preservation absent. | Not Run — partial |
| UAT-11 | `UAT-11-rejected.png`: semester 2 Rejected with exact reason; semester 1 approval retained. Advisor confirmation/queue and rejected-plan editability absent. | Not Run — partial |
| UAT-12 | `UAT-12-pending-plan.png`: Advisor semester 3 Pending with COMP 1201/MATH 2250, 6 credits. Student view and unchanged A/B check absent. | Not Run — partial |
| UAT-13 | `UAT-13-course-removed.png`: success, Pending COMP 1201 only, last-course guard. Dismissal-without-change and refreshed Advisor view absent. | Not Run — partial |
| UAT-14 | `UAT-14-approved-cancelled.png`: A Cancelled, approval feedback retained, zero selection/new choice. Dismissal, refresh and Messages absent. | Not Run — partial |
| UAT-15 | `UAT-16-pending-cancelled.png`: B Cancelled, rejection feedback retained, zero selection. Refresh/Messages and unaffected other semesters absent. | Not Run — partial |
| UAT-16 | `UAT-15-rejected-cancelled.png`: C Cancelled, zero selection, no repeat Cancel. Messages, refreshed queue withdrawal and unaffected students absent. | Not Run — partial |
| UAT-17 | `UAT-17-new-plan.png`: new C Pending with ENGL 1000 only, 3 credits. Refresh and exactly one new Advisor queue entry absent. | Not Run — partial |
| UAT-18 | `UAT-01.png`: authenticated Student Home and empty latest-plan state. Wrong/valid login attempts, all-semester baseline and session refresh absent. | Not Run — partial |
| UAT-19 | `UAT-05.png`: Advisor identity/navigation and populated review. Wrong/valid login attempts and independent-session refresh absent. | Not Run — partial |
| UAT-20 | `UAT-20-access-denied.png`: 401 Session Expired page; `UAT-20-logged-out.png`: empty login. No logged-in Student `/admin` 403, Advisor tab fallback, or actor-specific fresh logout URL evidence. | Not Run — partial |

**Executed-data deviation:** original A planned COMP 1201+MATH 2250 (2 courses/6 credits); actual A used MATH 1300+MATH 2200+MATH 2250 (3/9), then replaced MATH 2250 with ENGL 1000 (still 3/9). Original planned expectations remain in place and the actual substitution is explicitly documented. It supports positive selection/submission/revision, but all three initial Mathematics courses have no prerequisites, so it does not prove the planned nonempty-prerequisite selection path. Do not silently substitute this run for the original case or label that difference a functional failure.

The 401 image shows a signed-out/session-expired presentation, **not HTTP 403 for a logged-in Student**. No network-status capture is embedded; the displayed 401 label alone is not transport-level proof. Automated tests separately establish actual HTTP statuses. Current reports make the proper distinction. No original UAT result was upgraded by this audit.

## Final deliverables inventory

These classifications assess available content and published availability separately. Final assembly is still necessary for every required PDF section.

| Requested artifact | Classification | Actual evidence / outstanding work |
|---|---|---|
| 1. Student name and ID | Partially satisfied | Cameron Ramesar is recorded. `12345678` is seeded application data, not verified submission identity. Supply/confirm the real student ID privately for the final PDF cover. |
| 2. Project Description | Satisfied | MyAdvisor description and WF1–WF3 in [Assignment 1 report source](../report.md); reuse relevant content in A2. |
| 3. Original Use Case Diagram | Satisfied | [UML PNG](../diagrams/use-case.png), JSON/PlantUML source present; reviewed against Student/Advisor workflows. |
| 4. Entity Relationship Diagram | Satisfied | Seven-entity Mermaid ERD embedded in `docs/report.md`, including plan/course joins and program requirements; requires legible rendering in final PDF. |
| 5. Original Assignment 1 Wireframe | Satisfied | [Three-panel original](../wireframes/Three-Panel%20Student%20Advisor%20Dashboard%20Mockup.png), independently viewed; original illustrative values must not be presented as executed values. |
| 6. UAT Test Plan | Satisfied | Plan plus 20-case execution companion, wireframe mappings and recorded data deviation. Linked course-template contents Not verified. |
| 7. Unit Test Plan | Satisfied | UT-01–23 with isolation, inputs, expected results, boundaries and source mapping. |
| 8. Integration Test Plan | Partially satisfied | IT-01–20 substantive; extend scope for the newly verified role/FK gaps. Historical statuses now clearly identified. |
| 9. Test Implementation Evidence | Satisfied locally | Top-level test files, JSON routes, traceability and retained/new execution outputs; add concise representative implementation evidence to PDF. |
| 10. Unit Testing Results | Satisfied | Three original marked screenshots, historical text/XML, new full-run unit nodes. |
| 11. Integration Testing Results | Satisfied | Three original marked screenshots, historical Student log, new full-run integration nodes. |
| 12. Postman Collection | Partially satisfied | Local [v2.1 JSON](postman/MyAdvisor-Assignment2.postman_collection.json) exists and validates; **Missing from public main**. YAML is not the required JSON export. |
| 13. Postman Runner Results | Partially satisfied | Six local screenshots support the one run; **Missing from public main**. A machine-readable Runner export is useful but not expressly required by the brief. |
| 14. Manual UAT Execution Results | Partially satisfied | 20-case record and 19 images; remaining expected outcomes unverified; all UAT PNGs absent remotely. |
| 15. Test Reports | Partially satisfied | Detailed current local reports exist; published reports are stale; completed UAT report requirement remains open. |
| 16. GitHub Repository Link | Satisfied | User-specified repository resolves; README clone target corrected locally. Original A1 report retains its historical MyAdvisor link; final A2 PDF must use MyAdvisorWithTests. |
| 17. Final Single-PDF Deliverable | Missing | No A2 compilation/cover exists. Do not use the old A1 PDF as a completed A2 deliverable. Generation deliberately deferred. |

The supplied Assignment 2 brief does not separately require a new deployment/video or transcript grade. Existing A1 deployment assertions, credentials and Judge scorecard are historical context; they are not a verified current deployment or an Assignment 2 grade. Do not append unrelated historical grade claims as this audit's conclusion.

## Findings register

Severity describes impact/marking risk; it is not a grade. **No Critical finding is verified.** Open functional fixes below require a separate authorized correction step; no application fix or retest is claimed here.

| ID | Severity | Rubric area | File / evidence | Description and why it matters | Proposed smallest fix | Status |
|---|---|---|---|---|---|---|
| F01 | **High** | Implementation — Authorization; Test Plans/Implementation | `app/routers/user_home.py`; [reproduction](evidence/audit/authorization-reproduction.json) | Advisor JSON submit returns 403, but HTML POST `/app/plan` returns 303 and stores an Advisor-owned Pending plan; the same Advisor's approve API returns 200 and stores Approved. UI hiding does not enforce role separation. | Apply existing StudentDep to HTML submit/remove/cancel actions; add real-auth wrong-role/unknown-role no-write tests. A defensive prohibition on reviewing own plans may also be considered, but it is not a substitute for the Student entry-point guard. | **Open — reproduced; application unchanged** |
| F02 | **High** | Test Implementation; final API deliverable | [Published postman directory](https://github.com/Camcoon/MyAdvisorWithTests/tree/864386fe10fa5e61869e07500d84e51ff7e46b9b/docs/assignment2/postman); snapshot | Required `MyAdvisor-Assignment2.postman_collection.json` is absent remotely. The local static validator also needs that missing file. A marker cloning main cannot import the promised export. | Include the existing sanitized local v2.1 JSON in the reviewed submission commit; verify it is retrievable and imports. Do not substitute YAML. | **Open — publication requires user instruction** |
| F03 | **High** | Test Reporting; repository readiness | Remote snapshot; local comparison | Published main has six pytest images but no UAT PNGs, no Postman Runner PNGs, no current evidence matrix/inventory/traceability/supplemental sheet, and older versions of the five reports/progress/plans. | Publish the reviewed current docs/evidence together after corrections; verify every remote link. | **Open — local work is not published** |
| F04 | **High** | Test Reporting — Completed UAT report | `reports/uat-execution.md`, `uat-final-report.md`, supplemental checklist | Only one complete-case Pass; 18 partial cases and one unverified workflow. Refresh, navigation, login/logout and role substeps cannot be inferred from state screenshots. | Personally execute missing case-specific checks with actual dates/data/browser/build, record expected vs actual, preserve old evidence, and resolve or accept defects explicitly. | **Open — incomplete acceptance** |
| F05 / DATA-01 | **High** | Implementation WF1; Test Plans/Reporting | Service/model seed configuration; UAT-02; original wireframe | Verified 93 overall versus 120 category requirements; single-category course allocation supplies no overlap explanation. Correct curriculum values remain unspecified, affecting trustworthy progress guidance. | Obtain an authoritative degree/project requirement decision; then make only justified configuration/calculation and test/documentation changes. | **Open — unresolved requirements issue, values unchanged** |
| F06 / UI-01 | Medium | Implementation views; UAT | `advisor_dashboard.html`, `app.css`, UAT-05/08/12; UAT-09 | Advisor table body details are almost white on near-white; UAT-09 approval explanatory text is dark on dark green. Existence/text rendering tests miss readability. The A1 blanket high-contrast description is not supported by these captures. | Inspect computed table/theme variables and style order; scope dark table text/hover text to `.course-review-table`, resolve the approved-notice paragraph cascade, then capture fresh browser evidence. No WCAG ratio is claimed without measurement. | **Open — visually verified; current-browser retest needed** |
| F07 | Medium | Persistence; integration fidelity | `app/database.py`; [SQLite reproduction](evidence/audit/sqlite-integrity-reproduction.json) | Actual application SQLite engine reports FK PRAGMA 0 and commits an orphan PlanCourse in a fresh file. Integration fixture enables FK=ON, so its constraint passes do not describe default runtime enforcement. Service validation still protects normal tested selections; this is not proof of a user-facing arbitrary-row exploit. | Enable SQLite FK enforcement on every app connection and test the real engine factory/configuration; retain existing forced-constraint tests. | **Open — reproduced; no DB/source change** |
| F08 | Medium | Supporting A1 functionality; input/error handling | `app/routers/register.py`, `auth_service.py`; [registration reproduction](evidence/audit/registration-reproduction.json) | Anonymous malformed email reaches internal RegularUserCreate validation, yields generic HTTP 500, and leaves DB unchanged. Browser email validation is not a server error contract. | Validate form data at the request boundary or catch validation errors and return a useful 422/form message; add a no-write invalid-email regression. | **Open — reproduced** |
| F09 | Medium | Security — browser writes | `security.py`, HTML mutation forms/routes | Production auth cookie is SameSite=None; no CSRF token/Origin enforcement was found. Cross-site form POSTs have no explicit application-level CSRF check. Actual exploitability depends on browser/deployment cookie policy; no exploit was executed. | If cross-site cookies are unnecessary, use an appropriate same-site policy; add token or validated Origin protection to authenticated writes and negative tests. Review GET logout separately. | **Open — verified missing control; deployment impact conditional** |
| F10 | Medium | Test Reporting — provenance | Old marked/Runner/UAT records; new `evidence/audit/` | Historical screenshots do not identify their executed commit/DB/browser completely. New full rerun now has XML/log/exit/source hashes and matches published app/test files, but cannot retroactively attest old Postman/UAT runs. | Record build and environment on new executions; preserve each run independently. Do not relabel old screenshots with a new build. | **Partly addressed — fresh pytest evidence added; historical limits remain** |
| F11 | Medium | Final deliverables | Existing A1 report/PDF; artifact inventory | No compiled A2 PDF or verified real submission ID. Seeded `12345678` must not be used as identity evidence. | Confirm real ID, assemble all required A2 sections and readable screenshots after material issues close; perform final PDF review when authorized. | **Open — assembly deferred by user instruction** |
| F12 | Low | Documentation consistency/setup | README; Postman README; plans; evidence inventory | Clone instructions led to starter repo; Postman README said runtime pending despite recorded execution; historical H3 described current HTML 401 as 200; inventory called UAT-06 partial; two R-level mappings omitted proper cancellation/logout request ranges or UAT-06 Pass. | Correct verified statements and add current/historical pointers without changing original test inputs/oracles. | **Corrected locally in audit; remote still stale** |
| F13 | Low | API test assertion completeness | Postman request 19; collection scripts | Percentage range assertions would accept an incorrect in-range progress/category percentage; request 20 discovery alone trusts returned eligibility. Other pytest tests cover literal formulas and known prerequisites, so this is a collection coverage limit rather than evidence those formulas currently fail. | Add exact independently calculated percentage/category assertions and a known completed-prerequisite positive check in a later collection revision; rerun and retain new Runner results. | **Open — tests retained unchanged** |
| F14 | Low | Code/repository quality | Published `comp3613a1/`, `runlog*.txt`; `.gitignore` | Full older A1 tree and historical run logs duplicate the app and confuse execution targets. `.gitignore` protects `.env`, `.venv`, caches and `database.db`, but not every possible temp SQLite file or environment variant. | Keep top-level target explicit (README corrected); review archival/removal of redundant files; add narrow temp-DB/env patterns that preserve required evidence. No recursive deletion was performed. | **Open cleanup suggestion; target clarified** |
| F15 | Medium | Security configuration | `.env.example`, `app/config.py`, startup/login | Committed example uses a known placeholder signing key; app falls back to it without a production-strength check. Demo credentials are intentionally public. No private credential leak was found, and no production use of the placeholder is established. | Reject placeholder/weak keys in production, use a generated runtime secret, verify deployment configuration privately, and keep demo accounts confined to demo data. | **Open configuration risk; production state Not verified** |
| F16 | Low | Test Reporting/dependency maintenance | Existing screenshots and new pytest log | One TestClient/httpx deprecation remains. It is disclosed and does not fail assertions; hiding it or automatically upgrading dependencies would invalidate evidence expectations. | Retain warning in reports; evaluate a compatible dependency update separately and rerun affected suites if changed. | **Open, disclosed** |

## Security and code-quality disposition

Verified positive controls: password hashing, JWT signature/expiry/subject checks, HttpOnly cookies and production Secure flag, DB-resolved roles, response allowlists excluding password hashes, owner-specific Student data, parameterized SQLModel queries, strict API input schemas and sanitized domain/database errors. Advisor role is intentionally `admin`; a shared Pending queue is specified locally, so missing per-Advisor student allocation is not fabricated as a defect.

The complete remote tree contains no `.env`, populated SQLite database, Python environment/cache directory, or JWT-like token file. Published collection definition variables and local JSON password/token fields are blank; global YAML has `values: []`. Text scans on public-path local files found no JWT patterns, private-key headers, recognizable GitHub/OpenAI token patterns or credential-bearing PostgreSQL URLs. The four historical run logs contain no JWTs, Argon2 hash markers or credential-bearing DB URLs. Public files matched locally except the documented differences; remote Student/Advisor login YAMLs were checked directly and use variable placeholders. Inspected screenshots reveal no passwords/session tokens. This is a scoped audit, not a guarantee that arbitrary binary contents or every kind of private information are absent.

Demo passwords and the example secret are public development defaults, not established leaked private credentials. Their runtime suitability remains F15. Personal name/student-number placeholders visible in UAT are demo profile data; do not infer the real ID. Existing database/log files were not published or deleted by this audit. No secrets were copied into the audit outputs.

Architecture mostly separates routes, service rules and repositories. Existing demo setup performs direct session operations in the service, and AuthService queries its program through the repository session; these are layering inconsistencies, not a reason to rewrite working workflows. No broad refactoring is recommended for submission. No broken in-app route was established by this review; comprehensive keyboard, screen-reader, mobile, external CDN and current deployed-link checks remain unverified. The visually established contrast issues are defects; wider accessibility checks are suggestions, not invented rubric mandates.

## Changes made and verification impact

Documentation-only corrections: README project/clone target and isolated CLI commands; current Postman execution status; plan current/historical banners; resolved H3 statement; R05/R06 UAT-06 disposition and R09/R12 request ranges; one stale inventory mapping; and an explicit contrast/audit qualification in the historical A1 report. Added official brief source, this audit, GitHub snapshot/comparison, three isolated reproduction records, and new full-suite output/XML/source metadata. Unit/integration report and progress addenda point to the new run without replacing historical evidence. Original planned UAT inputs/expected results and all tests remain unchanged. Collection JSON SHA-256 remains `409cffa7540cd73880d74139f77346cdb47d06a18d9ae8e1b11cf70ef2c44b6d`.

Static documentation verification checked 24 Markdown files, rendered them with markdown-it-py CommonMark/table support, resolved 679 local references with no missing target, decoded all 31 execution PNGs, confirmed 20 unique UAT IDs and their 1/0/19 dispositions, and verified zero app/test source changes since the successful full run. The collection hash is unchanged. See the [validation record](evidence/audit/documentation-checks.json); the final progress-record link adds one further local reference after that snapshot. These are documentation checks, not a PDF export or browser test.

Functional corrections have **not** been applied. The smallest recommended F01 correction is explicit above; approval for application changes is deferred until the user requests that correction work. This audit stops after reporting, as requested.

If corrections are authorized later:

| Change | Required affected checks / evidence |
|---|---|
| HTML Student role guards | Add Advisor/unknown-role form submit/remove/cancel denial with unchanged DB, retain legitimate Student tests; rerun Student integration/API security and complete pytest with a fresh safe basetemp. Existing Postman 15–17/31–50 and review 51–77 are relevant regressions, but new HTML-denial requests/tests are needed. Retest UAT-18–20 plus affected submission/removal/cancellation paths. |
| Degree requirements/formulas | Unit UT-01–03, IT-02, progress API tests and Postman 19; refresh UAT-01 with approved requirement oracle. Catalogue/eligibility tests also need retesting if course allocation/data changes. |
| Advisor/approval CSS | Existing rendered-screen tests and complete pytest; browser UAT-06/08/09/12 with fresh captures and computed contrast checks. API behavior is unchanged in intent, but old images cannot prove the styling fix. |
| SQLite FK configuration | Actual-engine integrity/startup/legacy-schema and IT-19/20, all affected persistence suites and full pytest; regress relevant Postman submission/review/cancellation. Retest affected UAT lifecycle cases if runtime behavior changes. |
| Registration, CSRF, cookie or secret validation | Appropriate invalid-input/auth/browser-write regressions and full pytest. Postman 01–18, mutations 22–86 and logout 87–90 may require updates/reruns. UAT-18–20 and authenticated browser writes require fresh evidence. |

Any future source/collection change needs its own dated results; this audit's successful rerun does not pre-approve it.

## Final readiness and personal checklist

**Satisfied:** substantial WF1–WF3 implementation, isolated unit planning/implementation, broad real-auth integration, CLI execution, original diagrams/wireframe, local v2.1 collection/scripts and readable passing automated screenshots. **Partial:** authorization, trustworthy WF1 requirement semantics, completed UAT, published API/evidence package and final deliverable assembly. **Missing from published submission:** required Postman JSON, UAT screenshots, Postman Runner screenshots and latest reconciled audit/report artifacts. **Missing final artifact:** the A2 single PDF, intentionally not generated.

Necessary actions, in priority order:

1. Authorize a small correction for **F01** and agree the legitimate role behavior; require regression tests and fresh results.
2. Obtain/approve an authoritative **93-versus-120** degree requirement decision. Do not pick a number merely to make a test pass.
3. Resolve the Advisor table/approval-text readability issue and the reproduced SQLite/registration defects; review security configuration/CSRF controls in their actual deployment context. Record accepted exceptions explicitly where appropriate.
4. Personally complete the missing UAT substeps in the [existing supplemental checklist](reports/uat-supplemental-evidence.md), recording actual date, environment/build and observed outcomes. In particular capture logged-in Student `/admin` denial, Advisor tab fallback, valid/invalid login, actor-specific fresh logout checks, refresh/persistence and queue/feedback changes. Preserve the three-course data deviation.
5. Review and publish the sanitized JSON, current documents and all required screenshots to **MyAdvisorWithTests/main** when ready; verify the remote clone, collection import and evidence links. No push/commit/history change was made here.
6. Confirm your real submission name/ID and retrieve/check any required course-template details. Then authorize PDF generation and review every required section/image at readable size. **Do not generate the final PDF yet.**

This audit is complete as an independent review. The submission remains **not ready** while these material findings are unresolved.


## Prompt 16 evidence-mapping correction ? 27 October 2026

Visual PDF review found the two cancellation filenames describe the opposite cases: `UAT-15-rejected-cancelled.png` actually shows Year 1 semester 3 Cancelled (UAT-16), while `UAT-16-pending-cancelled.png` shows Year 1 semester 2 Cancelled with retained rejection feedback (UAT-15). References above are corrected to the visible content. Original image bytes/names, planned steps, expected outcomes, observed cancellation states and all case statuses remain unchanged: **1 Pass / 0 Fail / 19 Not Run**. Filename order does not establish execution chronology. No additional refresh, unaffected-semester or queue outcome is inferred. This is a documentation mapping correction, not a new browser execution or functional retest.
