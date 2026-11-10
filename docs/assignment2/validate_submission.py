"""Open, inspect, render every page, and record document-level checks."""
from pathlib import Path
import sys,json,re,hashlib,subprocess,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE/'.pdf-tools'))
import pymupdf as fitz
from PIL import Image,ImageOps,ImageDraw

def main():
    pdf=HERE/'COMP3613_Assignment2_MyAdvisor.pdf'
    review=HERE/'pdf-review'; rendered=review/'rendered';rendered.mkdir(exist_ok=True)
    doc=fitz.open(pdf)
    text='\n'.join(page.get_text() for page in doc)
    manifest=json.loads((review/'assembly-manifest.json').read_text(encoding='utf-8'))
    pages=[];issues=[];outs=[];image_pages=[]
    for i,page in enumerate(doc,1):
        words=page.get_text('words')
        body=[w for w in words if 34<w[1]<page.rect.height-32]
        if not body:issues.append({'page':i,'issue':'no body text'})
        for w in words:
            if w[0]<20 or w[2]>page.rect.width-18 or w[1]<7 or w[3]>page.rect.height-10:
                outs.append({'page':i,'word':w[4],'bbox':list(w[:4])})
        footer_words=[w[4] for w in words if w[1]>page.rect.height-35 and w[0]>page.rect.width-65]
        if str(i) not in footer_words:issues.append({'page':i,'issue':'footer page number not found'})
        path=rendered/f'page-{i:03d}.png'
        page.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(path)
        blocks=page.get_text('dict')['blocks']
        font_sizes=[span['size'] for b in blocks if 'lines' in b for line in b['lines'] for span in line['spans']]
        pages.append({'page':i,'width':page.rect.width,'height':page.rect.height,'words':len(words),
                      'images':len(page.get_images()),'minimum_text_points':round(min(font_sizes),2) if font_sizes else None})
        if page.get_images(): image_pages.append(i)
    # Four sufficiently large page thumbnails per contact sheet; full renders retained.
    sheets=[]
    for start in range(0,len(doc),4):
        sheet=Image.new('RGB',(1300,1860),'#d6e0e5');draw=ImageDraw.Draw(sheet)
        for j,n in enumerate(range(start,min(start+4,len(doc)))):
            image=Image.open(rendered/f'page-{n+1:03d}.png')
            image.thumbnail((620,875))
            x=(j%2)*650+(650-image.width)//2;y=(j//2)*930+30
            sheet.paste(image,(x,y));draw.text((j%2*650+20,j//2*930+10),f'PAGE {n+1}',fill='#17324d')
        sp=rendered/f'contact-{start//4+1:02d}.jpg';sheet.save(sp,quality=90);sheets.append(str(sp.relative_to(ROOT)).replace('\\','/'))
    original=fitz.open(ROOT/'docs/report.pdf');cover=original[0].get_text()
    transcript=(ROOT/'docs/transcripts/current-report-export.md').read_text(encoding='utf-8')
    identity=re.search(r'add my name ([^\n]+?) and my Student ID (\d+)',transcript)
    assert identity and all(value in cover for value in identity.groups()),'Original PDF identity mismatch'
    assert all(value in doc[0].get_text() for value in identity.groups()),'Submission cover identity mismatch'
    audit=json.loads((HERE/'evidence/audit/pytest-run.json').read_text())
    changed=[]
    for name,digest in audit['source_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:changed.append(name)
    assert not changed,'Source changed since successful audit run: '+str(changed)
    current=hashlib.sha256((HERE/'postman/MyAdvisor-Assignment2.postman_collection.json').read_bytes()).hexdigest()
    assert current=='409cffa7540cd73880d74139f77346cdb47d06a18d9ae8e1b11cf70ef2c44b6d'
    assert all((ROOT/item['path']).exists() for item in manifest['source_files'])
    assert '1 Pass / 0 Fail / 19 Not Run' in text
    for n in range(1,21):assert f'UAT-{n:02}' in text
    for n in range(1,24):assert f'UT-{n:02}' in text
    for n in range(1,21):assert f'IT-{n:02}' in text
    for bad in ['bobpass','adminpass','student-integration-password','-----BEGIN PRIVATE KEY-----']:
        assert bad not in text,'Secret/demo password appears in PDF text'
    assert not re.search(r'eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}',text)
    toc=doc.get_toc()
    toc_checks=[]
    for level,title,page_no in toc:
        normalized=' '.join(doc[page_no-1].get_text().split())
        ok=' '.join(title.split()) in normalized
        toc_checks.append({'title':title,'page':page_no,'destination_has_title':ok})
        if not ok:issues.append({'page':page_no,'issue':'outline title mismatch','title':title})
    xml=ET.parse(HERE/'evidence/audit/pytest-results.xml')
    node_names=[n.attrib for n in xml.findall('.//testcase')]
    status=subprocess.run(['git','status','--short'],cwd=ROOT,capture_output=True,text=True).stdout
    (review/'working-tree-status.txt').write_text(status,encoding='utf-8')
    from urllib.parse import unquote
    broken=[];ref_count=0;md_count=0
    for path in HERE.rglob('*.md'):
        if '.pdf-tools' in path.parts or 'pdf-review' in path.parts:continue
        md_count+=1
        for url in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if url.startswith(('http://','https://','mailto:','#')):continue
            target=(path.parent/unquote(url.split('#')[0])).resolve()
            ref_count+=1
            if not target.exists():broken.append({'document':str(path.relative_to(ROOT)),'target':url})
    assert not broken, 'Missing source-document references: '+str(broken)
    report={'pdf':str(pdf.relative_to(ROOT)).replace('\\','/'),'pages':len(doc),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
      'opens':True,'encrypted':doc.is_encrypted,'rendered_pages':len(pages),'page_details':pages,'image_pages':image_pages,
      'blank_or_footer_issues':issues,'out_of_page_words':outs,'outline_checks':toc_checks,'contact_sheets':sheets,
      'original_cover_identity_confirmed':True,'audit_source_hashes_unchanged':not changed,'checked_audit_source_files':len(audit['source_sha256']),
      'collection_sha256_unchanged':current,'full_suite_junit_tests':len(node_names),'junit_failures':len(xml.findall('.//failure')),
      'junit_errors':len(xml.findall('.//error')),'secrets_text_scan':'No demo passwords/JWT/private-key markers found; original images require visual review.',
      'missing_local_references':manifest['missing_references'],'readiness':'Not submission-ready: F01–F05 open',
      'source_markdown_files_checked':md_count,'source_markdown_local_references_checked':ref_count,'broken_source_document_references':broken,
      'visual_review':'PENDING human-style visual inspection of rendered contact sheets and full-size pages by the agent'}
    (review/'validation-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    (review/'pdf-text.txt').write_text(text,encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['pages','opens','rendered_pages','blank_or_footer_issues','out_of_page_words','checked_audit_source_files','missing_local_references']},indent=2))

if __name__=='__main__':main()
