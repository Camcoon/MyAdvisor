# COMP 3613 Assignment 2 — Final Lecturer Deliverables Checklist

Final PDF: [COMP3613_Assignment2_MyAdvisor_Final.pdf](COMP3613_Assignment2_MyAdvisor_Final.pdf)

**57 pages**, reduced from 139. Reviewed 3 November 2026. The original 139-page PDF remains unchanged and the prior 57-page final is preserved in `final-review/previous-final-before-restructuring.pdf`. The eight numbered sections follow the requested order; the contents page is unnumbered as a section and appears on physical page 2.

**Submission-ready: NO.** Document assembly and review are complete; the open requirements and findings below remain unresolved. “Included” describes the PDF content, not successful acceptance of the application.

| Lecturer deliverable (exact wording and order) | PDF page(s) | Disposition |
|---|---:|---|
| 1. Name & ID | 1 | Included: Cameron Ramesar, 816044668; verified against the retained statement and Assignment 1 cover. |
| 2. Project Description | 3 | Included: purpose/problem, Student/Advisor, WF1–WF3, technologies and Assignment 2 scope. |
| 3. Use Case Diagram | 4 | Included: actual Assignment 1 diagram; original pixels verified. |
| 4. Entity Relationship Diagram | 5–6 | Included: original ERD plus readable vector keys/relationships from the actual model/source. |
| 5. Application Wireframe | 7–10 | Included: original complete image plus three enlarged workflow panels. |
| 6. Test Plans | 11–31 | Included; plan expectations are separated from execution reports. Google template-specific details remain unverified. |
| User Acceptance Tests Plan | 11–22 | Included: UAT-01–20; objectives/scope, actors/environment, wireframe references, preconditions, steps, data and expected results. |
| Unit Tests | 23–26 | Included: UT-01–23, isolated components, inputs/outputs and positive/negative/boundary strategy. |
| Integration Tests | 27–31 | Included: IT-01–20, real authentication/database/Student–Advisor scenarios and correction supplement. |
| 7. Implementation | 32–35 | Included; publication limitations are explicit. |
| Link to repository | 32 | Clickable intended repository works. Current corrected implementation/evidence publication is incomplete. |
| Unit Tests | 32 | Included: actual pytest files, fixtures/mocks, functions and actual code example. |
| Integration Tests | 33 | Included: TestClient, isolated SQLite/session boundaries, real actor/auth checks and actual workflow excerpt. |
| API Tests (Postman collection exported to JSON in repository) | 34–35 | Current degree93 v2.1 JSON is attached locally. Public main contains the earlier export revision; publishing the updated revision remains outstanding. |
| 8. Reports | 36–51 | Included with historical/corrected-build attribution and warning disclosure. |
| Unit Tests Report (screenshot of test results) | 36–39 | Genuine screenshots on 37–39; enlarged 113-pass terminal result on 39. |
| Integration Tests Report (screenshot of test results) | 40–44 | Genuine screenshots on 41–43; enlarged 194-pass terminal result on 43. Supporting full-suite evidence on 44. |
| Postman Collection Run report screenshot | 45–51 | Genuine Runner screenshots on 46–51; 90 requests, 470 assertions passed, 0 observed assertion failures and 0 execution errors. |

## Final verification

| Requested check | Result |
|---|---|
| Generate the new PDF | Complete; final file reopens successfully, 57 pages. |
| Open and visually inspect every page | Complete: all 57 rendered pages reviewed; full-size detail checks on ERD, table and mandatory results; per-page log in final-review/page-review.csv. |
| Check all required deliverables against lecturer list | Complete review; current local Postman revision and outstanding publication/acceptance gates are distinguished above. |
| Three mandatory testing report screenshots present/readable | Yes: unit page 39, integration page 43 and Postman pages 46–51. Genuine originals retained; no synthetic screenshots. |
| All diagrams included | Yes: use case page 4, original/keyed ERD pages 5–6, original/enlarged wireframe pages 7–10. |
| Contents, headings and page numbers | Verified against bookmarks, printed contents entries and numbered page footers. No out-of-margin words or empty pages detected. |
| Evidence and counts accurate | Historical marked runs 113/194 and full runs 715/735 are separated from the latest corrected-build result: 751 passed, 1 warning, 0 failures/errors/skips, 122.67s, exit 0. Retained text/XML/metadata checked; run membership counts are not added as separate executions. |
| Correspondence to final corrected implementation | All 74 app/test source hashes match the retained 751-pass run. Historical marked, Runner and UAT screenshots remain tied to earlier builds; fresh corrected-build manual UAT and revised Postman execution remain outstanding. |
| Exported Postman JSON available in repository | An earlier collection revision is on public main. Current degree93 revision is local only; owner publication is pending. |
| No secrets/passwords/authentication-token values | Scoped PDF and attachment text scans pass; displayed and attached screenshots visually reviewed. Password constants are redacted in attached text copies; exact sanitized collection bytes are preserved. No deployment/private DB credentials copied. |
| Unresolved requirements/findings disclosed | Yes: Appendix B, page 55; full audit/correction records attached. Submission readiness remains NO. |
| Existing PDF preserved until verification | Yes: original 139-page COMP3613_Assignment2_MyAdvisor.pdf hash unchanged. Verified candidate copied to the separate requested Final filename. |

## Repository and template verification

- Repository: https://github.com/Camcoon/MyAdvisorWithTests — latest retained read-only snapshot identifies public main commit `edc71e8d8fadecc6c2d173eeddce1a66360a6126`.
- Current local collection: `docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json`, revision 2026.10.27-degree93; SHA-256 `6f1a8d297bb5bc4b510963b7a244b7376d60d96531edcaa59c1840f169cad4d3`.
- Public main has an earlier export revision at the same path; the current degree93 revision is local and is attached to this PDF. The historical 90-request/470-assertion Runner evidence applies to the earlier revision; no current-revision run is claimed.
- Main contains A2 API/tests and six pytest PNGs; corrected app/CSS files, correction tests/browser harness, Runner/UAT images and current evidence are unpublished. The local origin names Camcoon/MyAdvisor, a different repository. No publication or remote changes were made.
- Lecturer Google Docs edit/text-export requests were inaccessible. Exact template headings, extra fields, sign-offs and formatting are unverified. Existing plans and explicitly supplied fields were used; no template content was invented.

## Unresolved requirements and audit findings

- **F02/F03:** publish the revised degree93 JSON, current corrected source and evidence to the intended repository, then verify the published revision. This task does not publish.
- **F04:** UAT is **1 Pass / 0 Fail / 18 Executed - Partially Verified / 1 Not Executed - Unverified**. UAT-05 remains unverified; corrected-build manual acceptance is pending.
- **F05 / DATA-01:** owner-approved fictional allocation 36/18/12/18/9 totals 93 and is implemented/regression-tested. New human UAT-01 capture/refresh and deployed-data checks remain pending. No authoritative UWI curriculum is claimed.
- F10/F13: historical screenshots remain tied to older builds; current Postman independent oracles are implemented but the revised collection is not run. Duplicate tree/logs remain; one TestClient/httpx warning remains. New raw regression evidence does not certify PostgreSQL, races, production sessions, or human usability.
- **F09/F15:** CSRF/trusted-origin design and production signing-key disposition remain open; no deployed security certification or live exploit claim.
- **F01/F07/F08:** fixes are regression-tested locally but unpublished and still require the documented new browser/API evidence. **F06:** computed contrast passes locally; human readability acceptance remains pending.
- **F12/F14/F16:** remote documentation is older; duplicate-tree cleanup is suggested; one disclosed Starlette/httpx deprecation remains.
- External template-specific requirements are unverified. These limitations prevent a submission-ready declaration.

Supporting UAT summary: pages 52–54. Findings: page 55. Traceability: page 56. Lecturer checklist inside PDF: page 57. All 19 original UAT images, six pytest screenshots and six Runner screenshots are preserved as PDF attachments with the supporting reports and 751-run artifacts.

Final PDF SHA-256: `b3854c0f7474a2ba8b67b95718bb8389ac35934d9c72fc529557cbc194f039c0`.
Verification record: `final-review/validation-report.json`; page review: `final-review/page-review.csv`.
