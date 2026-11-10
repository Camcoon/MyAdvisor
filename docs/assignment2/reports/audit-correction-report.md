# Verified audit corrections and remaining submission work

> **Approved-allocation update ? 27 October 2026:** [Current correction record](degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


**27 October 2026 (America/La_Paz).** The user authorized bounded corrections after reviewing the 139-page PDF. **F01, F07 and F08 are corrected and regression-tested locally. F06 is corrected and passes automated browser-computed contrast checks; fresh human/browser evidence remains pending.** No curriculum values, deployment settings, Git remotes or published content were changed. No PDF was regenerated.

## Correction disposition

| Finding | Actual correction and evidence | Current disposition |
|---|---|---|
| **F01 High — HTML role bypass** | Reused existing `StudentDep` on HTML submit, course removal and cancellation, before handler/service execution. Twelve real-auth regressions cover admin/unknown current DB roles, Student-owned/legacy Advisor-owned plans, and all three actions. Each requires HTTP 403 and equality of all committed fixture tables. | **Fixed locally; fresh manual/Postman HTML checks pending.** Existing legacy wrong-role-owned records, if any, were not inspected or deleted. |
| **F06 Medium — contrast** | Explicit light-panel table foreground/background and hover/striped variables; white Approved-notice paragraph/small text override. Actual rendered HTML with the pinned Bootstrap/AdminLTE cascade is measured in Chromium, including forced row hover. Normal table 14.81:1, hovered row 13.73:1, Approved paragraph 6.56:1. | **Code corrected; automated browser checks pass. Human UAT/readability acceptance still pending.** No old image relabelled as corrected. No blanket accessibility-conformance claim. |
| **F07 Medium — runtime SQLite FKs** | Application engine factory attaches a SQLite-only connection hook before any connection use, sets foreign keys on and restores driver autocommit mode. Real factory/schema tests force separate pooled connections, reject orphan plan/course references, preserve a valid link and verify newly pooled connections after disposal. | **Fixed locally for new application SQLite connections.** No existing private DB opened/repaired; no PostgreSQL or historical-orphan claim. Restart an old process to use the updated engine. |
| **F08 Medium — registration 500** | Request-boundary `EmailStr` form validation returns 422 for malformed email before registration persistence. Three invalid-email variants compare unchanged full DB snapshots; valid Student creation and duplicate handling are also verified. | **Fixed locally.** Browser native email validation and new server-response evidence still need the supplemental checks. |
| **F05 High / DATA-01** | User confirms this is a coursework prototype, without an authoritative university curriculum document. Owner directs a 93-credit, non-overlapping fictional demonstration breakdown, with proposed numbers requiring approval first. | **Pending owner decision/approval. Existing 93/120 values unchanged.** No approved allocation or new curriculum result is claimed. |
| **F02/F03 High — publication** | Correct remote main rechecked; local missing JSON/images/current reports exist but remain unpublished. Safe explicit-scope synchronization plan prepared. | **Open. No push, commit, remote change or deletion.** |
| **F04 High — UAT completion** | Historical observations and original 19 images preserved; missing conditions converted to exact new-build browser instructions. | **Open. Historical 1 Pass / 0 Fail / 19 Not Run; corrected-build manual run pending.** |
| **F09/F15 Medium — security deployment** | Source and deployment blueprint reviewed; decisions/unknowns below. | **Open; review is not a verified production fix.** |

The original Prompt 15 findings remain a historical audit of the earlier build. This dated record supersedes its open/unchanged-source statements only for the corrections above.

## Application/test files changed in this correction task

- [user_home.py](../../../app/routers/user_home.py): three Student-only mutation dependencies; shared Student/Advisor Home remains authenticated as before.
- [database.py](../../../app/database.py): small application-engine factory and SQLite connection policy. PostgreSQL URI normalization and existing pool configuration retained.
- [register.py](../../../app/routers/register.py): typed request-boundary email validation; existing service/repository registration flow retained.
- [app.css](../../../app/static/css/app.css): scoped Advisor-table colors and Approved explanatory text.
- [test_audit_corrections.py](../../../tests/integration/test_audit_corrections.py): **18 new integration variants** (12 authorization, 3 invalid registration, 1 valid/duplicate registration, 2 runtime-engine integrity).
- [test_contrast_regression.py](../../../tests/integration/test_contrast_regression.py) and [contrast_probe.cjs](../../../tests/browser/contrast_probe.cjs): **2 new integration variants** measuring computed normal/hover text contrast in real rendered templates, with no live user session in Chromium.
- [run_correction_checks.py](../run_correction_checks.py): reproducible recording of isolated targeted/full/optional marked runs. It never initializes the normal application database or records signing-key values.

No existing test assertion or expected outcome was weakened. Original source changes from earlier prompts remain in the working tree; the list above identifies this task's application/test scope. Documentation addenda, retest/publication instructions and evidence records were also added/updated.

## Genuine new execution evidence

All records below live under [corrections-2026-10-27](../evidence/corrections-2026-10-27/), separately from historical `evidence/audit`, marked screenshots and original UAT/Runner images.

| Run | Actual result | Retained record |
|---|---|---|
| F01 pre-fix demonstration | **12 failed, 4 deselected, 1 warning**, 3.93s; pytest exit 1. These new requirements failed against AuthDep-only routes. | [Raw output](../evidence/corrections-2026-10-27/f01-before-ae8767c2.txt), [XML](../evidence/corrections-2026-10-27/f01-before-ae8767c2.xml), metadata alongside. |
| Initial affected tests | **282 passed, 1 warning**, 47.42s; exit 0. Before adding the two computed-style tests and final annotation cleanup. | [Raw output](../evidence/corrections-2026-10-27/targeted-cf752b27.txt), XML/metadata alongside. |
| Initial browser harness attempts | **2 failed** per attempt due to renderer timeouts inside the tool sandbox; not observed app contrast failures. A pipe transport and then loopback transport were tried. | [First environment failure](../evidence/corrections-2026-10-27/contrast-833f7e57.txt), [second environment failure](../evidence/corrections-2026-10-27/contrast-29709f52.txt). |
| Focused browser retest | **2 passed, 1 warning**, 3.26s; exit 0, with renderer able to run outside the tool sandbox. Actual normal/hover ratios and CSS hashes recorded. | [Raw measured output](../evidence/corrections-2026-10-27/contrast-4ddabb8e.txt), XML/metadata alongside. |
| **Final targeted correction suite** | **284 passed, 0 failures/errors/skips, 1 warning**, **86.42s; exit 0**. | [Output](../evidence/corrections-2026-10-27/targeted-20261027T193352Z-b6385978.txt), [XML](../evidence/corrections-2026-10-27/targeted-20261027T193352Z-b6385978.xml), [command/source hashes](../evidence/corrections-2026-10-27/targeted-20261027T193352Z-b6385978.json). |
| **Final complete pytest suite** | **735 passed, 0 failures/errors/skips, 1 warning**, **58.11s; exit 0**. | [Output](../evidence/corrections-2026-10-27/full-20261027T193800Z-7227960f.txt), [XML](../evidence/corrections-2026-10-27/full-20261027T193800Z-7227960f.xml), [command/environment/source hashes](../evidence/corrections-2026-10-27/full-20261027T193800Z-7227960f.json). |

The new complete result is **715 existing + 20 new variants = 735**. Its XML contains **113 unit nodes, 214 integration nodes and 408 other nodes**. These are membership counts within the complete run, **not separately executed new marked selections**. Historical marked results remain 113/602-deselected and 194/521-deselected for the old 715-item collection. Targeted/full selections overlap and must not be summed.

Final runs recorded hashes for **70 application/test files**, unchanged during execution and independently rechecked afterward. Every run used a unique writable `--basetemp`, disabled pytest cache and configured an unused disposable bootstrap DB; final metadata confirms that bootstrap file was not created. Real fixture DBs and the runtime-engine probe use their own fresh memory/temp databases. No original/private database was initialized, reset or migrated.

Reproduce from the project root:

```powershell
.\.venv\Scripts\python.exe docs/assignment2/run_correction_checks.py targeted
.\.venv\Scripts\python.exe docs/assignment2/run_correction_checks.py full
```

The runner saves the actual child pytest commands, timestamps, exit code, output, XML, environment/package versions and source hashes. In this managed tool environment Chromium's renderer required execution outside the tool sandbox; this was environment access, not an application change. Browser fixtures strip scripts and replace stylesheet links in place with local copies of the **exact pinned** Bootstrap 5.3.8 and AdminLTE 4.10.0 CSS plus current app CSS, retaining stylesheet order and real template styles. Bootstrap integrity is checked. There are no user cookies in the browser profile. Chrome reported `156.0.8078.48`; Node reported `v24.19.0`. This is automated template verification, not manual UAT.

For optional browser prerequisites, install Node/Chromium separately as appropriate and place the following **public pinned CSS** files under locally ignored `docs/assignment2/.browser-assets/`:

```powershell
New-Item -ItemType Directory -Force docs/assignment2/.browser-assets | Out-Null
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css' -OutFile docs/assignment2/.browser-assets/bootstrap.min.css
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/admin-lte@4.10.0/dist/css/adminlte.min.css' -OutFile docs/assignment2/.browser-assets/adminlte.min.css
```

Browser tests explicitly skip if Node/Chromium/CSS are unavailable; **neither final recorded run skipped them**. Pinned downloaded CSS hashes are in the focused measured output. No browser tool/dependency was added to application requirements. Scoped Ruff checks on changed Python files and the runner passed; Node syntax and changed-file whitespace checks passed. The existing Starlette/httpx deprecation remains the one pytest warning (F16), not a failed assertion.

## F07 implementation basis

SQLite needs foreign-key enforcement enabled for each connection, including schema creation. The hook follows SQLAlchemy's documented connection-event pattern and temporarily sets autocommit only while emitting the PRAGMA, restoring it afterward; it also accommodates Python versions without the driver attribute. The event is attached only to the application-created SQLite engine rather than globally affecting unrelated test engines. [SQLAlchemy SQLite foreign-key documentation](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support).

## F09 CSRF review and deployment decision

Verified source: production login cookies remain `SameSite=None`, `Secure`, `HttpOnly`; local cookies use Lax. No CSRF token or Origin enforcement is implemented on authenticated form writes; logout remains a GET action. The F01 role fix does not prevent cross-site requests made as an otherwise legitimate Student/Advisor. No live CSRF exploit or production cookie configuration was exercised.

**Decision for this bounded correction:** do not silently assume whether the deployment must support an embedded/cross-site client, and do not introduce a broad forms/API protection rewrite. F09 stays open. Before closing it, confirm trusted external origin(s), proxy handling and whether cross-site cookies are necessary; select a CSRF token or strict trusted-Origin design and assess same-site cookie hardening. SameSite alone is generally an additional layer and does not protect a state-changing GET such as logout. [OWASP CSRF guidance](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#defense-in-depth-techniques).

Required later security regressions: legitimate same-origin writes still succeed; cross-origin/missing-or-invalid CSRF credentials cannot mutate any row; no cookie/token leaks; documented proxy-origin handling; login/logout behavior; intended embedded-client flow if one exists. Do not treat current local HTTP tests as proof of production protection.

## F15 signing-key review and deployment decision

`render.yaml` specifies `ENV=production` and `SECRET_KEY` with `generateValue: true`. This proves intended blueprint configuration, **not the current service's runtime value or that the blueprint was used**. Settings still allow fallback to the public example key without a production-strength guard. No deployed secret was read, printed, rotated or changed.

**Decision:** F15 remains open until the deployment owner privately verifies a non-placeholder randomly generated runtime key and the chosen production startup policy. Add/review fail-fast rejection of example/weak/missing production keys in a later scoped security change, with settings/startup/login tests and affected API/UAT reruns. Account for session invalidation if rotating a live signing key. Public demo credentials/test constants do not establish a leaked private secret; keep them confined to demonstration environments. No claim of production security is made.

## F05 owner clarification — no curriculum modification

The owner explicitly confirms no authoritative university programme document is available. Existing values must be described as **fictional coursework demonstration data**, not official University of the West Indies requirements. The owner directs a proposed 93-credit total and five non-overlapping categories; proposed replacement numbers were presented in chat for approval. **Approval remains pending, and the seed, model defaults, tests, database and historical report/screenshot values are unchanged.**

Approval must specify the final category allocation and apply only to a new version of demo data. Then evaluate seed/data migration for existing demonstration databases separately; do not reset private/evidence DBs or silently modify previously retained observations. Update independent configured/category oracles, strengthen Postman request 19's exact percentages/category expectations, rerun affected pytest and collection checks, capture new UAT-01 category rows and version the related plans/reports/traceability. Keep the old three-course evidence and original wireframe illustrative totals intact. If only category denominators change, overall baseline 6 completed / 3 in progress / 84 remaining / 93 required remains unchanged; category remaining/percentages must be recalculated from the approved values. F13 assertion-depth work is not silently performed before this decision.

## Manual/API evidence and publication still required

Use [exact browser and Postman retest guide](correction-retest-guide.md) for the 19 historical missing conditions plus changed-build checks. All 20 original UAT cases are mapped; no observed partial success discarded or promoted to Pass. Human checks cover valid/invalid login, persistent/independent sessions, Student 403/Advisor fallback, F01 denied HTML writes, plan lifecycle/queue/feedback reset, table hover/text and Approved paragraph readability, registration validation and both signed-out URLs. No new result fields are filled by these instructions.

Rerun the **entire 90-request collection** on a separate disposable corrected-build server. Add separately recorded supplemental HTML denial/invalid-email requests because the historical collection does not cover those operations. Current static validator still passes: **90 requests, 93 script blocks compile, all 15 JSON operations**; this is not a new Runner pass. The existing 470-pass iteration and all old screenshots retain their original build/provenance limits.

[Repository publication plan](repository-publication-plan.md) explains the unrelated histories and wrong local origin. Use a fresh review checkout/branch and explicit reviewed overlay **only after approval**, with candidate manifest, staged-diff/secret review and no force-push. Existing A2 work and new files remain uncommitted. The existing PDF is stale for this source; its hash was checked unchanged. No new final PDF generation is authorized in this task.

## Readiness

The safe, reproduced functional corrections are implemented and tested locally. **Not ready for a submission-ready revised PDF:** F05 owner approval/implementation, new Postman/UAT evidence, publication F02/F03, incomplete UAT F04 and security deployment dispositions remain. F10 historical build attribution, F13 assertion depth, F14 cleanup and F16 warning remain disclosed; F11 identity/local assembly was previously addressed, but that PDF is now historical. Preserve the prior audit/results separately and update only with actually executed new evidence.
