# New Degree Progress acceptance record — not executed

This is a blank corrected-build record for **UAT-01**, separate from all historical observations. Do not fill actual results from automated tests. Use the current approved fictional-data build and a new isolated database as described in [correction-retest-guide.md](correction-retest-guide.md).

| Field | Value |
|---|---|
| Tester | Not recorded |
| Actual execution date/time/timezone | Not recorded |
| Browser/version, OS and URL | Not recorded |
| Source build/manifest and database | Not recorded |
| Case status | **Not Run — manual verification pending** |
| Actual result / evidence | Not recorded |

1. Sign in as the seeded Student in its own browser profile. Open Degree Progress.
2. Verify 6 completed, 3 in progress, 84 remaining, 93 required and 6% completed.
3. Verify Core 3/36, remaining 33, 8%; General Education 3/18, remaining 15, 17%; Electives 0/12, remaining 12, 0%; Major 0/18, remaining 18, 0%; Additional 0/9, remaining 9, 0%.
4. Confirm category requirements total 93. Category remaining totals 87 because in-progress credits are excluded there; overall remaining is 84. Completed courses each contribute to one category only.
5. Read the fictional coursework notice and recent course activity. Capture a new image, for example `RETEST-<actual-date>-UAT-01-degree-before-refresh.png`.
6. Refresh; record the action and compare all values/activity. Capture `RETEST-<actual-date>-UAT-01-degree-after-refresh.png`.
7. Complete the Student session persistence check under UAT-18: sign out/sign in and confirm the same values. Record it against that case as well.

Preserve `screenshots/UAT/UAT-02.png`, the earlier Degree Progress screenshot, and the historical 1 Pass / 0 Fail / 19 Not Run report. A successful new UAT-01 result does not pass other cases. Record an attempted mismatch as Fail and retain any later retest separately. No new screenshot or human result is supplied by this template.
