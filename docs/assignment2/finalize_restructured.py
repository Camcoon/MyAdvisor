"""Promote only the inspected candidate and write the lecturer checklist."""
from pathlib import Path
import sys,json,re,hashlib,csv,io
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;R=H.parents[1];V=H/'final-review'
sys.path.insert(0,str(H/'.pdf-tools'))
import pymupdf as fitz
from PIL import Image

def main():
    candidate=V/'COMP3613_Assignment2_MyAdvisor_Final.candidate.pdf'
    final=H/'COMP3613_Assignment2_MyAdvisor_Final.pdf'
    result=json.loads((V/'validation-report.json').read_text(encoding='utf-8'))
    digest=hashlib.sha256(candidate.read_bytes()).hexdigest()
    assert digest==result['sha256']
    assert result['page_count']==57 and not result['outside_margins'] and not result['issues']
    assert result['uat_image_attachments']==19 and result['source_hashes_match_latest_751_run']
    meta=json.loads((H/'evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.json').read_text())
    assert len(meta['source_sha256'])==74
    assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in meta['source_sha256'].items())
    manifest=json.loads((V/'assembly-manifest.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((H/'COMP3613_Assignment2_MyAdvisor.pdf').read_bytes()).hexdigest()==manifest['old_pdf_sha256']
    with fitz.open(candidate) as d:
        original=fitz.open(R/'docs/report.pdf')
        embedded=original.extract_image(27)
        actual=Image.open(io.BytesIO(embedded['image'])).convert('RGB')
        png=Image.open(R/'docs/diagrams/use-case.png').convert('RGB')
        assert actual.size==png.size and actual.tobytes()==png.tobytes()
        original.close()
        snippets=['\n'.join(p.get_text() for p in d)]
        for name in d.embfile_names():
            if name.endswith(('.md','.txt','.json','.xml')):snippets.append(d.embfile_get(name).decode('utf-8-sig'))
        for text in snippets:
            for pattern in [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{25,}',r'github_pat_[A-Za-z0-9_]{25,}',r'sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{30,}',r'eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}',r'postgres(?:ql)?://[^\s:/]+:[^\s@]+@']:
                assert not re.search(pattern,text),pattern
        checklist_text=d[56].get_text()
        for n in [1,3,4,5,7,11,23,27,32,33,34,36,40,45]:assert 'Page '+str(n)+'.' in checklist_text
    if final.exists() and hashlib.sha256(final.read_bytes()).hexdigest()!=digest:
        backup=V/'previous-final-before-restructuring.pdf'
        assert not backup.exists(),'Preserve existing backup; review before replacement.'
        backup.write_bytes(final.read_bytes())
    final.write_bytes(candidate.read_bytes())
    assert hashlib.sha256(final.read_bytes()).hexdigest()==digest
    with fitz.open(final) as d:
        assert len(d)==57 and d.embfile_count()>=56
        assert sum(1 for n in d.embfile_names() if 'screenshots__UAT__' in n and n.lower().endswith('.png'))==19
        assert all(p.get_text().strip() for p in d)
    result.update(final_pdf=str(final.relative_to(R)).replace('\\','/'),final_sha256=digest,
        visual_review_complete=True,visually_reviewed_pages=list(range(1,58)),
        full_resolution_detail_reviews=[6,24,39,43,46,50,52,53,54,55],original_uat_images_visually_reviewed=19,
        known_password_and_token_scans_pass=True,original_use_case_pixels_match_assignment1=True,
        latest_751_source_hashes_verified=True,final_reopened=True,verified_utc=datetime.now(timezone.utc).isoformat())
    (V/'validation-report.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    with (V/'page-review.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['page','visual_review','note'])
        for n in range(1,58):
            figs=[k for k,v in result['figure_pages'].items() if v==n]
            w.writerow([n,'Reviewed','Layout, heading/footer and visible content checked; '+('figures '+','.join(figs) if figs else 'tables/text checked')+'. This is document review, not application acceptance.'])
    checklist=f'''# COMP 3613 Assignment 2 — Final Lecturer Deliverables Checklist

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

Final PDF SHA-256: `{digest}`.
Verification record: `final-review/validation-report.json`; page review: `final-review/page-review.csv`.
'''
    checklist_path=H/'COMP3613_Assignment2_MyAdvisor_Final_Checklist.md'
    checklist_path.write_text(checklist,encoding='utf-8')
    print(json.dumps({'final_pdf':str(final),'pages':57,'bytes':final.stat().st_size,'checklist':str(checklist_path),'sha256':digest,'old_pdf_unchanged':True,'submission_ready':False},indent=2))

if __name__=='__main__':main()
