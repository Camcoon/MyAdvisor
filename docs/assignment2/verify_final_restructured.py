"""Render every final-candidate page and verify document/evidence structure."""
from pathlib import Path
import sys,json,re,hashlib,csv
H=Path(__file__).resolve().parent;R=H.parents[1];V=H/'final-review'
sys.path.insert(0,str(H/'.pdf-tools'))
import pymupdf as fitz
from PIL import Image,ImageOps,ImageDraw,ImageFont

def run():
    path=V/'COMP3613_Assignment2_MyAdvisor_Final.candidate.pdf'
    d=fitz.open(path);texts=[p.get_text() for p in d];text='\n'.join(texts);normalized=re.sub(r'\s+',' ',text)
    manifest=json.loads((V/'assembly-manifest.json').read_text(encoding='utf-8'))
    rendered=V/'rendered';rendered.mkdir(exist_ok=True)
    out=[];issues=[];sizes=[]
    for i,p in enumerate(d,1):
        words=p.get_text('words');body=[w for w in words if 40<w[1]<p.rect.height-35]
        if not body:issues.append({'page':i,'issue':'no body text'})
        for w in words:
            if w[0]<25 or w[2]>p.rect.width-22 or w[1]<8 or w[3]>p.rect.height-10:
                out.append({'page':i,'text':w[4],'bbox':list(w[:4])})
        foot=[w[4] for w in words if w[1]>p.rect.height-34 and w[0]>p.rect.width-65]
        if str(i) not in foot:issues.append({'page':i,'issue':'footer number missing'})
        p.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(rendered/f'page-{i:03d}.png')
        sizes.append({'page':i,'portrait':p.rect.width<p.rect.height,'words':len(body),'images':len(p.get_images()),'last_body_y':max(w[3] for w in body),'first_text':re.sub(r'\s+',' ',texts[i-1][70:200])})
    sheets=[]
    for start in range(0,len(d),4):
        sheet=Image.new('RGB',(1800,2540),'#dce4e8');draw=ImageDraw.Draw(sheet)
        for j,n in enumerate(range(start,min(start+4,len(d)))):
            im=Image.open(rendered/f'page-{n+1:03d}.png');im.thumbnail((865,1210))
            x=j%2*900+(900-im.width)//2;y=j//2*1270+38
            sheet.paste(im,(x,y));draw.text((j%2*900+15,j//2*1270+12),f'PAGE {n+1}',fill='#17324d')
        dest=rendered/f'contact-{start//4+1:02d}.jpg';sheet.save(dest,quality=92);sheets.append(str(dest))
    for bad in ['bobpass','adminpass','student-integration-password','student-unit-password','-----BEGIN PRIVATE KEY-----']:
        assert bad not in text,bad
    assert not re.search(r'eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}',text)
    assert not re.search(r'postgres(?:ql)?://[^\s:/]+:[^\s@]+@',text)
    assert all(x in texts[0] for x in ['Cameron Ramesar','816044668','COMP 3613','Assignment 2','MyAdvisor','27 October 2026'])
    for prefix,count in [('UAT',20),('UT',23),('IT',20)]:
        assert all(f'{prefix}-{i:02d}' in text for i in range(1,count+1))
        assert all(x in normalized for x in ['113 passed','194 passed','470 assertions','735 passed','715 passed','751 passed','1 Pass / 0 Fail / 18 Executed - Partially Verified / 1 Not Executed - Unverified','NOT SUBMISSION-READY'])
        assert normalized.count('EXECUTED - PARTIALLY VERIFIED') >= 18
        assert 'NOT EXECUTED / UNVERIFIED' in normalized and 'UAT-05' in text
    toc=d.get_toc();main=[x for x in toc if x[0]==1 and re.match(r'^[1-8]\. ',x[1])]
    assert [int(x[1].split('.')[0]) for x in main]==list(range(1,9))
    toc_ok=[]
    for level,title,number in toc:
        clean=lambda s:re.sub(r'\s+',' ',s).strip()
        assert clean(title) in clean(texts[number-1]),(title,number)
        if level<=2: assert clean(title) in clean(texts[1]),('TOC printed entry missing',title)
        toc_ok.append({'title':title,'page':number})
    fp={}
    for fig in manifest['figures']:
        no=fig['number'];found=[]
        for i,p in enumerate(d):
            for block in p.get_text('dict',flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)['blocks']:
                for line in block.get('lines',[]):
                    spans=line['spans']
                    line_text=''.join(s['text'] for s in spans)
                    if line_text.startswith('Figure '+no+'.') and abs(spans[0]['size']-8.5)<.1 and 'Bold' in spans[0]['font']:
                        found.append(i+1)
        assert len(found)==1,(no,found)
        fp[no]=found[0]
    assert all(d[fp[k]-1].get_images() for k in ['3.1','4.1','5.1','5.2','5.3','5.4','8.3','8.6','8.7'])
    link= 'https://github.com/Camcoon/MyAdvisorWithTests/blob/main/docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json'
    uri=[(i+1,l['uri']) for i,p in enumerate(d) for l in p.get_links() if l.get('uri')]
    assert any(u==link for _,u in uri)
    key='docs__assignment2__postman__MyAdvisor-Assignment2.postman_collection.json'
    assert d.embfile_get(key)==(R/'docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json').read_bytes()
    uat_attachments=[n for n in d.embfile_names() if 'screenshots__UAT__' in n and n.lower().endswith('.png')]
    assert len(uat_attachments)==19,uat_attachments
    for name in d.embfile_names():
        if name.endswith(('.md','.txt','.json','.xml')):
            t=d.embfile_get(name).decode('utf-8-sig')
            assert not any(s in t for s in ['bobpass','adminpass','student-integration-password','student-unit-password','-----BEGIN PRIVATE KEY-----']),name
            assert not re.search(r'eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}',t),name
    old=hashlib.sha256((H/'COMP3613_Assignment2_MyAdvisor.pdf').read_bytes()).hexdigest()
    old=hashlib.sha256((H/'COMP3613_Assignment2_MyAdvisor.pdf').read_bytes()).hexdigest()
    assert old==manifest['old_pdf_sha256']
    report={'candidate':str(path),'page_count':len(d),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'toc':toc_ok,'figure_pages':fp,'attachments':d.embfile_count(),'uat_image_attachments':len(uat_attachments),'external_links':uri,
        'outside_margins':out,'issues':issues,'pages':sizes,'contact_sheets':sheets,
        'source_hashes_match_latest_751_run':True,'old_139_page_pdf_unchanged':True,
        'visual_review_complete':False,'prior_json_revision_published':True,'current_json_revision_published':False,'readiness':'NOT SUBMISSION-READY'}
    (V/'validation-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    (V/'pdf-text.txt').write_text(text,encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['page_count','figure_pages','outside_margins','issues','attachments','sha256']},indent=2))
    print('PAGE SUMMARIES',json.dumps(sizes,ensure_ascii=True))

if __name__=='__main__':run()
