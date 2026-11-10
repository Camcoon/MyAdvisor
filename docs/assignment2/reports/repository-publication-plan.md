# Safe publication review — MyAdvisorWithTests

> **Approved-allocation update ? 27 October 2026:** [Current correction record](degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


Prepared **27 October 2026**. **Plan only: no commit, push, fetch into this repository, remote change, deletion or history rewrite performed.**

## Verified repository state

- Intended public repository: **https://github.com/Camcoon/MyAdvisorWithTests**, default branch `main`.
- Read-only GitHub recheck: `main` remains at **864386fe10fa5e61869e07500d84e51ff7e46b9b**, the same complete tree retained in [audit snapshot](../evidence/audit/github-snapshot.json). Therefore the snapshot's missing exported JSON/UAT/Runner screenshots and stale reports remain applicable. The tree is not assumed to include new local corrections.
- Working source: nested `Assignment 2` directory containing `manage.py`, `app/` and `tests/`. Local branch: **assignment-2-testing**. Local HEAD before these corrections: **679b9250c13f38a2f97ed4e6d08a325fe48219d3**.
- `origin` fetch/push both point to **https://github.com/Camcoon/MyAdvisor.git**, not the intended submission repository. **Do not push this branch to origin.**
- The working tree already contained modified/untracked A2 application/test/documentation work before this request, and the nested `comp3613a1` entry is dirty. Preserve it. New correction files are also uncommitted. Use the correction evidence directory's saved Git status and publication manifest for the actual reviewed scope.

The local branch and the upload repository have different histories. Do not force-push, merge unrelated histories or rewrite origin to make them appear identical. The older upload checkout is not automatically the latest source.

## Reviewable publication scope

Use an explicit file allowlist, not `git add .` or a recursive workspace copy. Review current application/test changes, the corrected README/setup, test plans/reports/audit/progress, exported Postman JSON and validator/instructions, all genuine evidence images, historical run records and new correction evidence together. Preserve original design artifacts and genuine Assignment 1 sources already present remotely.

Essential additions/updates include:

1. `app/routers/user_home.py`, `app/routers/register.py`, `app/database.py`, `app/static/css/app.css` and focused regression sources, along with prior implemented API/test files that the working tree has not committed locally.
2. `docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json`, with **blank exported passwords/tokens**; its scripts and structure are retained.
3. Current `docs/assignment2/reports/`, plans, audit, progress, final checklist and retest/publication instructions. Historical test reports need their corrected-build qualification, not replacement of old observations.
4. All 19 original UAT PNGs and six Runner captures, plus six original pytest PNGs and later genuine retest evidence when personally captured. Preserve the corrected UAT-15/UAT-16 filename mapping.
5. Fresh correction logs/XML/source-hash metadata. Review intentionally failing pre-fix and browser-environment records as history, not the final test outcome.

**Hold the existing 139-page PDF from final publication/sign-off:** it is a preserved pre-correction artifact, not a PDF of this modified build. Do not regenerate it during this task. A later approved compilation must use fresh results and actual manual/API retests.

Exclude normal/private databases (`database.db`, any `.db`/`.sqlite`/`.sqlite3` and journal/WAL files), `.env` variants containing private settings, virtual environments, caches, browser profiles, local dependency assets, PDF render/extracted-text scratch, Postman cookie jars/environments with populated credentials, and raw private transcripts. Do not include `.git/`, `.agents/`, `.codex/` or the duplicate `comp3613a1/` tree in an overlay. Existing public `.env.example`/demo test constants are not private secrets, but F15's production-fallback risk remains open.

The generated publication review manifest lists candidate files/hashes and scoped secret-scan results. It is not a blanket guarantee about all repository bytes, ignored files or Git history. Review the actual staged diff again before a later commit.

## Proposed synchronization sequence — requires explicit later approval

1. Review the correction report, successful raw logs/XML, owner decision for F05, fresh Postman/UAT results and security deployment decisions. Keep this working checkout intact.
2. With approval, create a **fresh separate checkout of MyAdvisorWithTests/main** in a new named directory. Verify its remote and current main SHA; create a review branch from that SHA. This avoids altering this checkout's wrong origin or carrying its unrelated history.
3. Overlay **only the reviewed allowlisted additions/updates** from the working source. No bulk deletion, mirroring with deletion, or copying of `.git`/nested checkouts. Inspect every changed file and ensure original artifacts remain.
4. Recheck public-file/credential scans, collection variable defaults and `git diff --check`. Stage explicit paths; inspect the complete staged diff and file list. Exclude the stale PDF and every private/temporary file. Record the candidate commit/source hash relationship.
5. Run the relevant checks from that prepared checkout and verify the exported collection imports. Browser contrast checks require Node, Chromium and the pinned CSS assets described in the correction report; missing prerequisites produce explicit skips, not fabricated passes. Verify successful retained output and preserve actual skips/warnings.
6. With explicit publication approval, commit the reviewed scope and push the **review branch to MyAdvisorWithTests**; preferably open a reviewable PR. Do not force-push. If main changed, review/rebase the isolated review branch rather than overwriting remote changes.
7. After approval/merge, verify the JSON, all evidence images and current reports are retrievable on the new published SHA. Verify a clean clone and collection import. Then authorize the revised PDF after material acceptance issues are resolved or explicitly dispositioned.

No command to change remotes or publish is executed by this plan. Publication is still **F02/F03 open** until reviewed content actually exists on the intended remote.
