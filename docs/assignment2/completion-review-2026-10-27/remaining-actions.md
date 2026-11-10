# Final submission completion review — 27 October 2026

**Not submission-ready. No push, commit, remote change, destructive operation or PDF replacement was performed.** This review incorporates the owner's allocation approval received during this conversation. The earlier [verification snapshot](verification.json) describes the state **before** that new correction; it is not a claim that current source still matches the 735-pass build.

## Prioritized remaining actions

| Priority | Action | Current state / completion condition |
|---|---|---|
| 1 | Approved fictional degree correction | **Implemented.** 36/18/12/18/9 totals 93; the overall requirement and course catalogue/prerequisites/academic records are preserved. Affected selection: 46 passed. Complete regression: **751 passed, one warning**, no failures/errors/skips, exit 0. Existing local database already matches: apply was a no-op. New UAT-01 acceptance still required. |
| 2 | Corrected-build manual UAT | **Pending.** Prioritize restrictions and login, then Pending Home/Messages/relogin, refresh/persistence and Advisor queue updates. Exact work below and in the linked retest guide. Record actual tester/date/build/URL and screenshots. |
| 3 | Revised Postman execution | **Pending.** Import revision `2026.10.27-degree93`; requests 19/20 changed. Rerun all 90 sequential requests plus the separately documented HTML/registration checks. Retain real screenshots and export; do not reuse the old 470 count. |
| 4 | Reporting evidence | **Partial.** New raw 751-run evidence is retained; earlier separate marked screenshots show 113 unit / 194 integration for an older build. Capture new marked-unit/integration terminal screenshots if the final reports are to show the new selections. Preserve old screenshots and label each run. |
| 5 | Safe publication | **Requires approval.** Public main already has the earlier corrected source/tests and original exported JSON. The new degree code/JSON, current reports, 19 UAT images, six Runner images and correction evidence remain unpublished. Prepare an explicit reviewed overlay from the evidence checkout into the correct publication checkout; details below. |
| 6 | Security and external limitations | **Open.** F09 CSRF/Origin enforcement and GET logout; F15 production signing-key fallback/runtime verification. Keep F10 historical provenance, F14 duplicate tree/cleanup, F16 deprecation, and inaccessible lecturer template specifics disclosed. Decide security disposition without claiming a deployed fix. |
| 7 | Final PDF replacement | **Deferred until preceding evidence/publication work is resolved.** Keep the eight lecturer sections in the approved order. Update source/build/results, collection version, live repository links and concise limitations. Rebuild to a new filename, validate, visually review and only then replace the final PDF. Preserve the reviewed candidate. |

The [degree correction report](../reports/degree-requirement-correction.md) records the implementation, exact oracles, real regression results and database limitations. The [new UAT-01 sheet](../reports/degree-progress-retest.md) is explicitly blank.

## Verified Git state and current publication facts

| Checkout | Branch / HEAD | Origin | State on inspection |
|---|---|---|---|
| `Assignment 2` (evidence/source) | `assignment-2-testing`, `679b9250c13f38a2f97ed4e6d08a325fe48219d3` | `https://github.com/Camcoon/MyAdvisor.git` | Modified and untracked A2 work; nested `comp3613a1` gitlink is dirty. Do not push from this checkout. |
| `myadvisor-upload-yfjf6d9s` | `main`, `edc71e8d8fadecc6c2d173eeddce1a66360a6126` | `https://github.com/Camcoon/MyAdvisorWithTests.git` | Clean when inspected; unchanged by this task. Its tree exactly matches public main. |

The [public repository](https://github.com/Camcoon/MyAdvisorWithTests) is public and its default branch is main. The complete, untruncated [saved remote tree](remote-tree.json) has **442 entries**, tree `99a1ff1fa222feea3ea34778753bd8b610b87da5`. Before the approved allocation correction, all 70 app/test hashes in both checkouts matched the 735-run source manifest; every corresponding public blob matched the publication checkout. The new correction intentionally changes that build; use its separate 74-file source manifest.

The [exported JSON on GitHub](https://github.com/Camcoon/MyAdvisorWithTests/blob/main/docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json) **is present**, blob `d707ec4ae9f349219f0a546769c5505a096862b9`. It matches the historical collection SHA-256 `409cffa7540cd73880d74139f77346cdb47d06a18d9ae8e1b11cf70ef2c44b6d`. Thus the older candidate's 404/missing-JSON statements are stale. **The new revision**, SHA-256 `6f1a8d297bb5bc4b510963b7a244b7376d60d96531edcaa59c1840f169cad4d3`, is local only and needs approved publication.

Public main has no original UAT PNGs, Runner captures or correction-run evidence. Its UAT report still says **0 Pass / 20 Not Run**. The evidence checkout correctly retains **1 Pass / 19 Not Run** with the qualification below. Do not copy the public report over the reconciled local one. Git shell network access failed in this environment; read-only GitHub connector inspection supplied the current remote evidence. No successful local fetch/push connectivity test is claimed.

## Safe Git publication steps

1. Preserve both existing checkouts and PDFs. Use the clean `myadvisor-upload-yfjf6d9s` checkout, whose remote is already correct. No remote change is needed and the unrelated source history must not be force-pushed or merged into it.
2. Review the explicit [publication candidates](publication-candidates.json) with current SHA-256 values. The list is a review aid, **not approval to copy/stage/publish**, and must be refreshed after later evidence or PDF changes. Reconcile superseded findings in current documents and preserve historical findings as dated history. The initial pre-approval manifest is separate from the updated manifest.
3. Immediately before a later approved publication, recheck remote main and local status. If main has moved, inspect those commits before overlaying. Create a local review branch from the verified current main; preserve independent remote changes.
4. Overlay only approved relative paths: the narrow new app/test/CLI/template/runner changes, revised JSON and documentation, genuine historical and new evidence. Review source and destination hashes and diffs. Never mirror with deletion or recursively copy the workspace. Preserve remote-only artifacts.
5. Exclude `.git`, private `.env` variants, databases/WAL/journals, `.local-db-backups/`, virtual environments, caches, profiles, populated Postman tokens/cookie jars/environments, private transcripts, downloaded browser assets, render scratch and the duplicate `comp3613a1` tree from the overlay. Retain required genuine evidence files. Do not delete the existing duplicate tree during this task.
6. Verify current code/test/collection hashes; run appropriate checks in the prepared checkout and confirm collection import. Review every candidate's credential/personal-data content before staging. Source hashes alone are not a secret scan. The runner's old-PDF dependency has been made optional, so an absent pre-correction PDF no longer prevents it from recording a test run; browser prerequisites remain explicit.
7. Stage explicit reviewed paths, then inspect `git diff --cached --name-status`, the entire staged diff, `git diff --cached --check`, and status. No `git add .`. Include no unreviewed file. Record the exact commit/branch/target proposed for approval.
8. **Stop for explicit publication approval.** Only after approval: commit the reviewed files, perform a dry-run push, then push the named review branch to `Camcoon/MyAdvisorWithTests` and review/merge without force. A dry run does not grant publication approval.
9. Verify the published branch/commit contains the revised JSON, all required images, accurate reports and raw results. Check the default branch after merge and verify every final PDF repository link. Test importing the actual published JSON. Then complete the final PDF verification gate.

Safe read-only commands from the workspace root:

```powershell
git -C '.\Assignment 2' remote -v
git -C '.\Assignment 2' status --short --branch
git -C '.\myadvisor-upload-yfjf6d9s' remote -v
git -C '.\myadvisor-upload-yfjf6d9s' status --short --branch
git -C '.\myadvisor-upload-yfjf6d9s' log -2 --oneline
```

No staging, commit, branch/remote change, fetch, push or deletion was executed here.

## UAT status and exact remaining human checks

**Historical fully passed:** UAT-06, with documented substituted three-course/9-credit data. **Partially verified:** UAT-01–04 and UAT-07–20 (18 cases). **Required workflow unverified:** UAT-05. The retained three-state report is therefore **1 Pass / 0 Fail / 19 Not Run**. No new manual case has been passed by this correction.

Use a new disposable corrected-build instance, separate Student/Advisor profiles and new dated images. A/B/C mean Year 1 semesters 1/2/3. New planned inputs are A = COMP 1201 + MATH 2250; revised A = COMP 1201 + ENGL 1000; B = MATH 2250; C initially COMP 1201 + MATH 2250. Historical A actually used three courses/9 credits; preserve that deviation.

| Cases / priority | Required observations |
|---|---|
| UAT-18/19 — login | Try invalid then valid credentials for each role; verify error/no entry and correct destination/navigation. Check initial empty Student Messages/A/B/C views and refresh. Refresh independent profiles to prove identities do not cross. |
| UAT-20 — access | Signed-in Student directly opens `/admin`: actual HTTP 403. Advisor opens `/app?tab=plan-courses` and `/app?tab=degree-progress`: Advisor Home fallback and unchanged queue. After each actor signs out, freshly type its protected URL (`/app` for Student, `/admin` for Advisor): 401 Session Expired / Return to Login. Browser Back is insufficient. |
| Supplemental F01/F08 | While A is Pending, Advisor's POST `/app/plan`, course remove, and cancel must each return 403; read back unchanged Student plan/queue. Invalid-email server submission returns 422 without creation; native invalid email, valid registration and duplicates remain controlled. |
| UAT-01 — new data | Recapture corrected Degree Progress and activity before/after refresh using the exact 93-credit oracle in the new UAT-01 sheet. Keep original `UAT-02.png`. |
| UAT-04/05 — persistence | Submit A once, refresh, confirm locked ordinary editing/no duplicate. Before an Advisor decision, record Pending Home and Messages counts/credits, sign out/in, then open A and compare selection/status. This missing early workflow cannot be proved with later decision screenshots. |
| UAT-07/08/09/11 — queues/feedback | Record each Advisor decision confirmation, matching Student/Advisor feedback, and removal from refreshed Pending queue. After changes/resubmission, Student Pending/Messages must clear old feedback and exactly one revised A must appear after Advisor refresh. Approval/rejection and edit/Cancel states must persist after Student refresh. |
| UAT-10/12/13 — independent semesters/removal | Switch A↔B and inspect retained states; submit C while A/B stay unchanged. Dismiss then confirm removal; C retains only one course/3 credits and final-course protection. Advisor refresh must show the reduced C selection. |
| UAT-14/15/16/17 — cancellation/replacement | Dismiss then confirm cancellation where specified; refresh Student views/Messages and verify retained approval/rejection feedback and zero active selection. Withdraw Pending C from refreshed Advisor queue; keep unrelated plans unchanged if such plans actually exist. Submit fresh C with ENGL 1000; refresh to prove persistence and exactly one active new queue entry. |
| UAT-02/03 — catalogue/selection | Check nine semesters, code/title search, department/combined filters, no match/Clear Filters, empty selection, completed/in-progress/missing prerequisite disabled controls, exact 0→2→1→2 count/review credits and Back preserving choices. |
| UAT-06/09 — readability | Read current Advisor table normal/hover text and Approved explanatory paragraph. Historical UAT-06 Pass does not verify changed CSS. |

The [complete ordered retest guide](../reports/correction-retest-guide.md) supplies click-level steps and supplemental requests for all 20 cases. Preserve the corrected historical image mapping: `UAT-15-rejected-cancelled.png` supports case **UAT-16**, and `UAT-16-pending-cancelled.png` supports case **UAT-15**. Missing evidence stays unverified; an observed mismatch is a failure with its own retest record.

## Postman cases to rerun

Run the **entire 90-request revised collection**, one iteration, in its existing order on another disposable database; it is state-dependent. 01–18 cover login/cookies/registration/roles; **19–21** cover the approved progress/category and catalogue/prerequisite oracles; 22–50 cover validation/ownership/creation/removal; 51–77 cover review/feedback/resubmission/guards; 78–86 cover cancellation/history/replacement/queues; 87–90 cover logout/denial. Add the separately recorded HTML denial/registration checks above because the 90-request JSON does not cover them. Keep old and new collection hashes/results separate and export no credentials.

## Security findings and limitations still open

- **F09:** production cookie source uses `SameSite=None`, Secure and HttpOnly; no authenticated-write CSRF token or Origin enforcement is implemented, and logout is a GET. Role guards do not close this. Trusted origins/cross-site requirements and a scoped protection design need a decision and real regressions. No live exploit or deployed fix was tested.
- **F15:** settings may fall back to the public example signing key without a production-strength guard. Render's blueprint asks for a generated key but does not prove the actual deployed runtime value. Privately verify runtime configuration and address weak/missing/example keys; never disclose the real key. No rotation/deployment change was made.
- **F10/F13/F14/F16:** historical build provenance remains qualified; new Postman independent oracles are implemented but not run; duplicate tree and logs remain; the single TestClient/httpx warning remains. New raw regression evidence does not certify PostgreSQL, races, production sessions, or human usability.
- Two lecturer Google template contents were previously inaccessible and remain unverified. Confirm any template-specific fields before final replacement. The supplied eight-section order stays fixed.

## PDF preservation and replacement gate

Both `final-review/COMP3613_Assignment2_MyAdvisor_Final.candidate.pdf` and `COMP3613_Assignment2_MyAdvisor_Final.pdf` are **57 pages**, SHA-256 `e26ab1fe95ab668a2bbf46871493ce82821bccd41e58aa22440dcd26d7d37acd`. Initial inspection confirmed 56 embedded attachments, 56 links, and all **31** original execution PNGs byte-identical to their attachments: 19 UAT, six pytest, six Runner. No original image was modified.

The generator/finalizer still contain old hard-coded remote SHA/404 assertions, the old collection hash and 735-build checks. Update those inputs and current result references before a rebuild; do not bypass validation or relabel old screenshots. Build a separate replacement, reopen it, verify section order, cover identity, current raw count/status references, attachments, link destinations, readable diagrams/screenshots, and limitations, then compare preserved originals. Promote only after successful review; retain the old candidate.

## Actions only the owner must perform

1. Personally execute and record the remaining browser UAT, especially restrictions/login, UAT-05, refresh/queue/feedback checks and corrected Degree Progress images. Provide actual observations and new evidence without overwriting originals.
2. Run the revised Postman JSON in Runner, retain actual totals/screenshots and export, and record the supplemental HTML/registration checks. Capture genuine terminal screenshots for updated marked unit/integration reports if required for current-build reporting.
3. Confirm lecturer template details that cannot be accessed here. Privately verify deployed signing-key configuration and give the intended cross-site/trusted-origin requirements or a documented security disposition.
4. Review the final publication file list/diff and explicitly approve the intended repository, branch and scope before any push. No remote change is necessary.
5. Review the regenerated replacement after the evidence/publication gates close and personally upload the verified single PDF through the university's required channel.

The allocation decision is already approved and does not need to be requested again. Technical reconciliation, evidence integration, publication preparation and the eventual verified PDF build remain agent work within the authorized scope; no assignment-ready claim is justified yet.

For genuine updated unit/integration terminal screenshots, run these reporting selections from the source project root and capture the completed output and command. Keep the retained raw logs/XML/metadata. Their actual results, warnings or skips must be reported, rather than copying the 751-run membership counts into a claimed separate execution:

```powershell
.\.venv\Scripts\python.exe docs/assignment2/run_correction_checks.py unit --evidence-dir docs/assignment2/evidence/degree-requirements-2026-10-27
.\.venv\Scripts\python.exe docs/assignment2/run_correction_checks.py integration --evidence-dir docs/assignment2/evidence/degree-requirements-2026-10-27
```

Evidence indexes: [new full-run verification](verification-after-allocation.json), [pre-approval verification](verification.json), [current publication manifest](publication-candidates.json), [pre-approval candidate manifest](publication-candidates-before-allocation.json). These records are scoped checks and preserve their historical versions.
