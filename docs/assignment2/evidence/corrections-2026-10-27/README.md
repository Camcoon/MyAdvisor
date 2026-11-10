# Audit-correction evidence — 27 October 2026

These are new isolated executions, separate from original screenshots and Prompt 15 evidence. See the [correction report](../../reports/audit-correction-report.md) for scope, source changes and remaining decisions. No normal/private database was initialized or changed.

| Record prefix | Actual result / interpretation |
|---|---|
| `f01-before-ae8767c2` | 12 failures, 4 deselected, 1 warning, exit 1: new role-denial regressions reproduce the original defect. |
| `targeted-cf752b27` | 282 passed, 1 warning, exit 0: intermediate corrected source, before browser variants/final cleanup. |
| `contrast-833f7e57` | 2 failed: initial browser-pipe renderer timeout inside the tool sandbox. |
| `contrast-29709f52` | 2 failed: loopback browser renderer still timed out inside that sandbox. |
| `contrast-4ddabb8e` | 2 passed, 1 warning, exit 0: dedicated browser outside the tool sandbox; actual normal/hover/Approved contrast ratios retained in output. |
| `targeted-20261027T193352Z-b6385978` | **284 passed, 1 warning, 86.42s, exit 0; zero failures/errors/skips.** Final affected tests. |
| `full-20261027T193800Z-7227960f` | **735 passed, 1 warning, 58.11s, exit 0; zero failures/errors/skips.** Final full suite. |

Each execution has genuine `.txt` output, JUnit `.xml` and `.json` metadata alongside it. The final metadata records exact commands, fresh writable `--basetemp`, environment versions and **70 unchanged application/test source hashes**. Complete XML membership is 113 unit / 214 integration / 408 other nodes; no new separately marked run is claimed. Targeted selections overlap the full suite. The warning is the existing Starlette/httpx deprecation.

[verified-summary.json](verified-summary.json) independently reconciles final XML and metadata. [validation-review.json](validation-review.json) records the final source/evidence/link checks. [publication-review.json](publication-review.json) is a candidate overlay manifest and scoped secret-pattern review, not a commit or whole-history guarantee. Saved Git status/remotes describe the dirty local checkout; they do not publish anything.

Preserve the intentionally failing pre-fix and browser-environment records. They are distinguished from final passing executions. No manual UAT or Postman runtime run was performed here. Historical 19 UAT images, marked pytest images, Runner images and the old 139-page PDF remain unchanged; none proves the newly modified build. Use the [manual/API retest instructions](../../reports/correction-retest-guide.md) for missing evidence.
