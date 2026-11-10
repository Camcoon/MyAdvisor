"""Build the lecturer-ordered A2 review candidate without touching old PDFs.

Only retained evidence is used. No application tests or manual cases are run.
"""
from pathlib import Path
import sys, re, json, hashlib, html, textwrap, ast, io
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import build_submission as b
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, NextPageTemplate, Table, TableStyle, Image, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from PIL import Image as PILImage
import pymupdf as fitz

H=Path(__file__).resolve().parent
R=H.parents[1]
V=H/'final-review'
V.mkdir(exist_ok=True)
OUT=H/'COMP3613_Assignment2_MyAdvisor_Final_2026-11-05.pdf'
REPO='https://github.com/Camcoon/MyAdvisorWithTests'
COLL='docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json'
STAMP='5 November 2026'
UAT_DIR=H/'screenshots/UAT'
UAT_STATUSES={'PASS':8,'FAIL':0,'EXECUTED - PARTIALLY VERIFIED':12,'NOT EXECUTED':0}
S=b.story
W=b.W
LW=landscape(A4)[0]-2*b.M
for key in ['body','cell']:
    b.styles[key].fontSize=9
    b.styles[key].leading=12.3
b.styles['th'].fontSize=8.7
b.styles['th'].leading=12
b.styles['h1'].fontSize=19
b.styles['h1'].leading=24
b.styles['h2'].spaceBefore=7
b.styles['code'].fontName='Courier'
b.styles['code'].fontSize=8
b.styles['code'].leading=10.4
b.styles['caption'].fontSize=8.5
figures=[]
page_map=[]

def read(path): return b.read(path)
def p(t,style='body'): b.p(t,style)
def h(t,level=1,toc=True): b.heading(t,level,toc)
def page(title=None,kind='Portrait',level=0,toc=True):
    S.extend([NextPageTemplate(kind),PageBreak()])
    if title: h(title,level,toc)
def table(rows,widths=None,header=True):
    rows=[[str(v) for v in row] for row in rows]
    compact=rows[0][0] in ['Finding','Case','Lecturer deliverable (exact wording)']
    if rows[0][0]=='Lecturer deliverable (exact wording)' and OUT.exists():
        with fitz.open(OUT) as prior: oldtoc=prior.get_toc()
        prefixes=['1.','2.','3.','4.','5.','6.','6.1 ','6.2 ','6.3 ','7.','7.1 ','7.2 ','7.3 ','7.4 ','8.','8.1 ','8.2 ','8.3 ']
        for row,prefix in zip(rows[1:],prefixes):
            number=next((pg for _,title,pg in oldtoc if title.startswith(prefix)),None)
            if number: row[1]='**Page '+str(number)+'.** '+row[1]
    cell=b.styles['cell'] if not compact else ParagraphStyle('compact',parent=b.styles['cell'],fontSize=8.5,leading=11.3)
    data=[[Paragraph(b.inline(v),b.styles['th'] if header and i==0 else cell) for v in row] for i,row in enumerate(rows)]
    widths=widths or ([W*.25,W*.75] if len(rows[0])==2 else [W/len(rows[0])]*len(rows[0]))
    t=Table(data,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT',splitByRow=1,splitInRow=0)
    pad=3 if compact else 5
    cmds=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
      ('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cbd8df'))]
    if header:cmds += [('BACKGROUND',(0,0),(-1,0),b.NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,b.LIGHT])]
    else:cmds += [('BACKGROUND',(0,0),(0,-1),b.LIGHT)]
    t.setStyle(TableStyle(cmds));S.extend([t,Spacer(1,8)])
def note(path): b.source_note(path)
def md(t): b.markdown(t,H,False)
def code(t):
    # Actual code excerpts only; use preformatted text with no synthetic output.
    lines=t.rstrip().splitlines()
    for line in lines:
        assert len(line)<115,('oversize code line',line)
    S.append(Paragraph('<br/>'.join(html.escape(x).replace(' ','&#160;') for x in lines),b.styles['code']))
def source_link(path,label=None):
    return '['+(label or path)+']('+REPO+'/blob/main/'+path.replace(' ','%20')+')'
def fields(spec):
    # Field values may themselves contain vertical bars (status alternatives).
    result={}
    for line in spec.splitlines():
        if line.startswith('| ') and not line.startswith('|---'):
            k,_,v=line.strip().strip('|').strip().partition(' | ')
            result[k.strip()]=v.strip()
    return result
def figure(path,number,title,caption,kind='Landscape',crop=None,maxh=None,detail=None):
    path=Path(path)
    main=title in ['4. Entity Relationship Diagram','5. Application Wireframe']
    page(title,kind,0 if main else 1,main)
    img=PILImage.open(path)
    original_size=img.size
    if crop: img=img.crop(crop)
    iw,ih=img.size
    width=LW if kind=='Landscape' else W
    height=maxh or (landscape(A4)[1]-160 if kind=='Landscape' else A4[1]-190)
    scale=min(width/iw,height/ih)
    stream=io.BytesIO();img.save(stream,format='PNG');stream.seek(0)
    S.append(Image(stream,width=iw*scale,height=ih*scale,hAlign='CENTER'))
    S.append(Spacer(1,7))
    if detail:
        strip=PILImage.open(path).crop(detail)
        st=io.BytesIO();strip.save(st,format='PNG');st.seek(0)
        ds=width/strip.width
        S.append(Image(st,width=width,height=strip.height*ds,hAlign='CENTER'))
        S.append(Spacer(1,7))
    p('**Figure '+number+'.** '+caption,'caption')
    figures.append({'number':number,'path':str(path.relative_to(R)).replace('\\','/'),
        'crop':crop,'detail_crop':detail,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'original_pixels':original_size,'display_points':[round(iw*scale,2),round(ih*scale,2)]})
    b.sources.add(path.resolve())

def snippet(path,func,start=0,end=None):
    t=read(path);node=next(n for n in ast.walk(ast.parse(t)) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==func)
    lines=t.splitlines()[node.lineno-1:node.end_lineno]
    return '\n'.join(lines[start:end])

class KeyedERD(Flowable):
    """Readable vector view of the original ERD; PKs verified in real models."""
    def __init__(self,src):
        super().__init__();self.width=LW;self.height=420;self.src=src
    def draw(self):
        c=self.canv
        boxes={'DEGREE_PROGRAM':(0,300,180),'DEGREE_REQUIREMENT':(0,100,180),
            'USER':(265,264,194),'COURSE':(265,20,194),
            'SEMESTER_PLAN':(550,270,205),'PLAN_COURSE':(550,160,205),'STUDENT_COURSE':(550,0,205)}
        data={n:fs.strip().splitlines() for n,fs in re.findall(r'  (\w+) \{(.*?)\n  \}',self.src,re.S)}
        routes=[([(180,339),(265,339)],'enrolls 0..1 : 0..*',(183,348)),
          ([(90,300),(90,185)],'defines 1 : 0..*',(96,238)),
          ([(459,397),(550,397)],'creates 1 : 0..*',(463,405)),
          ([(459,361),(550,361)],'reviews 0..1 : 0..*',(461,349)),
          ([(459,285),(500,285),(500,85),(550,85)],'completes 1 : 0..*',(463,265)),
          ([(459,100),(550,100)],'appears 1 : 0..*',(463,110)),
          ([(459,151),(480,151),(480,195),(550,195)],'appears 1 : 0..*',(482,204)),
          ([(653,270),(653,230)],'contains 1 : 0..*',(659,254))]
        for pts,label,pos in routes:
            c.setStrokeColor(b.GRAY);c.setLineWidth(.8)
            q=c.beginPath();q.moveTo(*pts[0])
            for pt in pts[1:]:q.lineTo(*pt)
            c.drawPath(q);c.setFont('Body',7.4);c.setFillColor(b.TEAL);c.drawString(*pos,label)
        for name,(x,y,w) in boxes.items():
            fs=data[name];height=25+len(fs)*15
            c.setFillColor(colors.white);c.setStrokeColor(b.TEAL);c.roundRect(x,y,w,height,3,fill=1,stroke=1)
            c.setFillColor(b.NAVY);c.rect(x,y+height-23,w,23,fill=1,stroke=0)
            c.setFillColor(colors.white);c.setFont('Body-Bold',9);c.drawString(x+7,y+height-15,name)
            c.setFillColor(b.NAVY);c.setFont('Body',9)
            for i,f in enumerate(fs):
                f=re.sub(r'".*?"','',f).strip()
                if f=='int id':f+=' PK'
                c.drawString(x+7,y+height-37-i*15,f)

class Doc(BaseDocTemplate):
    def afterFlowable(self,f):
        if hasattr(f,'bookmark'):
            self.canv.bookmarkPage(f.bookmark)
            self.canv.addOutlineEntry(f.getPlainText(),f.bookmark,f.toclevel,False)
            self.notify('TOCEntry',(f.toclevel,f.getPlainText(),self.page,f.bookmark))
            page_map.append({'title':f.getPlainText(),'page':self.page,'level':f.toclevel+1})
def footer(c,d):
    width,height=c._pagesize
    if d.page>1:
        c.setFillColor(b.GRAY);c.setFont('Body',8)
        c.drawString(b.M,height-25,'MYADVISOR  |  COMP 3613  |  ASSIGNMENT 2')
        c.setStrokeColor(colors.HexColor('#ccd9df'));c.line(b.M,height-32,width-b.M,height-32)
    c.setFont('Body',7.5);c.setFillColor(b.GRAY)
    c.drawString(b.M,22,STAMP+'  |  Evidence qualified; acceptance incomplete')
    c.drawRightString(width-b.M,22,str(d.page))

def preflight():
    identity=re.search(r'add my name ([^\n]+?) and my Student ID (\d+)',read('docs/transcripts/current-report-export.md'))
    assert identity
    name,sid=identity.groups()
    with fitz.open(R/'docs/report.pdf') as d:
        assert all(x in d[0].get_text() for x in (name,sid))
        original=d.extract_image(29)
        (V/'original-erd.png').write_bytes(original['image'])
    m=json.loads(read(H/'evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.json'))
    changed=[f for f,s in m['source_sha256'].items() if hashlib.sha256((R/f).read_bytes()).hexdigest()!=s]
    assert not changed,changed
    assert m['run_id']=='full-20261028T015858Z-e5cbdcfb' and m['exit_code']==0 and m['source_unchanged_during_run']
    for path,count in [('evidence/audit/pytest-results.xml',715),('evidence/corrections-2026-10-27/full-20261027T193800Z-7227960f.xml',735),('evidence/corrections-2026-10-27/targeted-20261027T193352Z-b6385978.xml',284),('evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.xml',751)]:
        root=ET.fromstring(read(H/path));assert len(root.findall('.//testcase'))==count
        assert not any(root.findall('.//'+k) for k in ('failure','error','skipped'))
    coll=json.loads(read(COLL))
    assert hashlib.sha256((R/COLL).read_bytes()).hexdigest()=='6f1a8d297bb5bc4b510963b7a244b7376d60d96531edcaa59c1840f169cad4d3'
    def walk(items):
        for it in items:
            if 'item' in it:yield from walk(it['item'])
            else:yield it
    req=list(walk(coll['item']));assert len(req)==90
    assert coll['info']['schema'].endswith('/v2.1.0/collection.json')
    remote=json.loads((H/'completion-review-2026-10-27/remote-tree.json').read_text(encoding='utf-8'))
    remote_paths=[x['path'] for x in remote['tree']]
    assert COLL in remote_paths
    uat=read(H/'reports/uat-execution.md');uc=b.cases(uat,'UAT');assert len(uc)==20
    status=[fields(t.split('| Execution field |')[1]).get('Status') for _,t in uc]
    for label,count in UAT_STATUSES.items():
        got=sum(1 for s in status if s==label or (label=='NOT EXECUTED' and s and s.startswith('NOT EXECUTED')))
        assert got==count,(label,got,status)
    assert all(s in UAT_STATUSES or s.startswith('NOT EXECUTED') for s in status),status
    uat_images=sorted(UAT_DIR.glob('*.png'));assert len(uat_images)==55,len(uat_images)
    referenced=set()
    for _,t in uc:
        ref=fields(t.split('| Execution field |')[1]).get('Screenshot evidence reference','')
        for fn in re.findall(r'screenshots/UAT/([^/)]+\.png)',ref):
            assert (UAT_DIR/fn).exists(),fn
            referenced.add(fn)
    assert referenced=={f.name for f in uat_images},sorted({f.name for f in uat_images}-referenced)
    return name,sid,coll,req,uc,m,remote

def build():
    name,sid,coll,req,uc,meta,remote=preflight()
    specifications=json.loads((V/'specifications.json').read_text(encoding='utf-8'))
    erd=re.search(r'```mermaid\n(erDiagram.*?)```',read('docs/report.md'),re.S).group(1)
    # Cover is Section 1. The unnumbered contents does not shift lecturer sections.
    h('1. Cover Page',0)
    S.append(Spacer(1,60));p('COMP 3613','h2');p('Assignment 2','h2')
    S.append(Spacer(1,12))
    S.append(Paragraph('MyAdvisor',ParagraphStyle('cover',parent=b.styles['h1'],fontSize=38,leading=47)))
    p('Project, Test Plans, Implementation and Reports','h2')
    S.append(Spacer(1,30))
    table([['Student name',name],['University ID',sid],['Submission date',STAMP],['Repository','['+REPO+']('+REPO+')']],header=False)
    p('**Readiness: NOT SUBMISSION-READY.** The document is restructured and evidence is included; repository publication, acceptance and other material findings remain unresolved. See Appendix B.')
    p('Identity verified against the retained student statement and Assignment 1 cover. The eight-digit Student ID in the original wireframe and browser evidence is demonstration data.','small')
    p('This report distinguishes planned outcomes, historical executions and corrected-build regression evidence. It does not certify unperformed tests.','small')

    page('Table of Contents',toc=False)
    p('Physical PDF page numbers include the cover. The eight numbered sections follow the lecturer’s deliverables; supporting material follows in appendices.','small')
    toc=TableOfContents()
    toc.levelStyles=[ParagraphStyle('toc0',fontName='Body',fontSize=10,leading=16,spaceBefore=5,textColor=b.NAVY),
        ParagraphStyle('toc1',fontName='Body',fontSize=9,leading=14,leftIndent=15,textColor=b.GRAY)]
    S.append(toc)

    page('2. Project Description')
    p('MyAdvisor is a coursework prototype for Student–Advisor academic planning. It brings degree progress, prerequisite-aware course selection and plan decisions into connected workspaces, addressing the difficulty of reconciling completed work, current courses and proposed semester choices across separate records.')
    table([['Workflow / user','Purpose and implemented behavior'],
      ['WF1: Track Degree Progress — Student','View completed, in-progress and remaining credits; overall progress; requirement categories; recent academic activity.'],
      ['WF2: Plan Semester Course Selections — Student','Search/filter the catalogue, inspect eligibility, review and submit selections, read feedback, revise returned plans, remove permitted courses and cancel/replace plans.'],
      ['WF3: Review and Approve Course Plans — Advisor','Inspect the shared Pending queue and Student/course details; Approve, Reject or Request Changes, with optional feedback.']],[W*.31,W*.69])
    p('Students use Home, Degree Progress, Plan Courses, Messages and Profile. Advisors use their own Home/Profile and Advisor Review. Student identity comes from the authenticated account; Advisor decisions update a plan’s status, reviewer and feedback. Semesters use the nine fixed Year 1–3 / semester 1–3 options, with semester 3 designated summer.')
    table([['Technology','Role'],['Python / FastAPI / Pydantic','HTTP application, request validation and JSON APIs.'],['SQLModel / SQLAlchemy / SQLite','Models, repository persistence and isolated local tests. The Render blueprint targets PostgreSQL; no production database test is claimed.'],['Jinja2 / Bootstrap / AdminLTE / JavaScript','Rendered Student/Advisor pages and selection/review interactions.'],['pwdlib / PyJWT / signed cookies','Password verification, signed login token, current-role and ownership checks.'],['pytest / TestClient / mocks / Postman','Isolated unit decisions, integrated HTTP/database checks and automated API collection.']],[W*.36,W*.64])
    p('**Assignment 2 scope.** Extends the Assignment 1 workflows with explicit JSON API contracts, unit/integration plans and pytest implementations, a 90-request Postman collection, manual UAT specifications and execution records, screenshots and traceability. The owner-approved fictional degree/category allocation is 36/18/12/18/9 (93 total), not an authoritative UWI curriculum. The 55 new UAT captures record the corrected 93-credit display and the planned two-course execution; four before/after pairs are byte-identical, so those refresh/separate-role substeps remain partial.')
    note('docs/report.md; app/models; app/routers; docs/assignment2/api.md')

    page('3. Use Case Diagram')
    img=R/'docs/diagrams/use-case.png';im=PILImage.open(img);scale=min(W/im.width,475/im.height)
    S.append(Image(str(img),width=im.width*scale,height=im.height*scale))
    p('**Figure 3.1.** Original Assignment 1 MyAdvisor use case diagram, reproduced from `docs/diagrams/use-case.png` without redrawing.','caption')
    figures.append({'number':'3.1','path':'docs/diagrams/use-case.png','crop':None,'source_sha256':hashlib.sha256(img.read_bytes()).hexdigest()});b.sources.add(img.resolve())
    p('The Student tracks degree progress, plans semester selections, views the catalogue and cancels semester plans. The Advisor reviews course plans and can request changes. Catalogue viewing is included in the planning/review workflows; Request Changes extends review. These are the original diagram’s actors and relationships. Authentication supports their implementation and is tested separately.')

    figure(V/'original-erd.png','4.1','4. Entity Relationship Diagram','Original MyAdvisor ERD image extracted losslessly from Assignment 1 `docs/report.pdf`, page 3 (image 29). The readable keyed rendering follows.','Portrait',maxh=600)
    p('A program defines requirements and optionally enrolls users. A Student creates plans and has course records; an optional Advisor reviews each plan. PLAN_COURSE joins plans to courses; STUDENT_COURSE joins users to academic course records. All seven id fields are primary keys. Unique pairs constrain program/category, student/course and plan/course. The password field names stored data; no value is printed.','small')
    page('4.1 Readable entity keys and relationships','Landscape',1)
    S.append(KeyedERD(erd))
    p('**Figure 4.2.** Enlarged vector rendering of the same original seven-entity Mermaid ERD. All original fields/relationships are retained; PK labels are added from `app/models/user.py` and `app/models/advising.py`. FK fields retain their original names. Numeric edge labels state source:target cardinality; “appears” abbreviates “appears_in”.','caption')
    figures.append({'number':'4.2','source':'docs/report.md Mermaid + app/models','vector':True})

    figure(R/'docs/wireframes/Three-Panel Student Advisor Dashboard Mockup.png','5.1','5. Application Wireframe','Original three-panel Assignment 1 wireframe, unmodified. W1: Student Degree Progress; W2: Student Semester Planning; W3: Advisor Plan Review. Sample credits, dates, course labels and the eight-digit ID are illustrative, not execution results.','Landscape')
    wf=R/'docs/wireframes/Three-Panel Student Advisor Dashboard Mockup.png'
    # Original panels are enlarged, never reconstructed or AI-generated.
    for n,(a,z,label) in enumerate([(0,510,'W1 — Student Degree Progress'),(516,1020,'W2 — Student Semester Planning'),(1032,1536,'W3 — Advisor Plan Review')],2):
        figure(wf,'5.'+str(n),'5.'+str(n-1)+' Wireframe detail: '+label,'Enlarged crop of the original panel. W1 maps to UAT-01; W2 to UAT-02–05 and UAT-08–17; W3 to UAT-06–11 and queue checks. Login and cancellation extensions are documented in the plan.','Portrait',(a,0,z,930),maxh=640)

    page('6. Test Plans')
    h('6.1 User Acceptance Test Plan')
    p('**Objective and scope.** Verify that Students can understand degree progress and complete eligible semester planning, and Advisors can review and return decisions. These are planned browser tasks and expected outcomes. Actual results and latest statuses appear only in Appendix A; automated executions appear in Section 8.')
    p('**Template access.** Both lecturer Google Docs templates were requested through their edit and text-export URLs on 27 October 2026; the tool reported them inaccessible. Their exact headings, extra fields, sign-offs and formatting are **unverified**, and are not invented. This section adapts the retained plans to the fields explicitly required in the supplied brief. [Test Plans template](https://docs.google.com/document/d/1YQPB1vPS0SFb6tIUAxmxrSUIsj-d6u98USWzvMi4mJs/edit); [User Acceptance Tests Plan template](https://docs.google.com/document/d/1LIPdWA39zJCuzTgSkwTKjnaqi8Yn9STFZckn4MBsf48/edit).')
    table([['Plan control','Specification'],['Actors','Student (regular_user), Advisor (admin); separate browser profiles to isolate cookies.'],['Environment','Prepared disposable SQLite database; current local app; JavaScript enabled; planned base URL http://127.0.0.1:5002. Record actual URL, build/source hashes, browser/version, OS, date/time zone and tester at execution. Existing historic browser/build details are incomplete.'],['Preparation','Use the existing safe setup in reports/uat-execution.md and the corrected-build retest guide. Do not reset an existing database. Confirm empty A/B/C semesters and expected demo identities. Use supplied account credentials privately; no password values appear here.'],['Execution order','UAT-18 → UAT-01–05 → UAT-19 → UAT-06–17 → UAT-20. Numeric IDs are retained.'],['References','W1/W2/W3 are the panels in Figures 5.2/5.3/5.4. W4 means Student Messages/feedback; W5 means cancellation/resubmission extensions to W2/W3, not additional original panels.'],['Recording and completion','Record observed outcome, actual evidence filename, deviation and remaining checks. Pass only when the complete required outcome is observed. Classify observed primary outcomes with incomplete substeps as Executed - Partially Verified; use Not Executed / Unverified only when no adequate observation establishes the workflow; record Fail only for an observed mismatch.']],[W*.25,W*.75])
    h('6.1.1 Planned UAT data and baseline',2,False)
    table([['Symbol / item','Planned data'],['A / B / C','Year 1 semester 1 / Year 1 semester 2 / Year 1 semester 3.'],['E1 / E2 / E3','COMP 1201 Object-Oriented Programming (requires completed COMP 1101) / MATH 2250 Industrial Statistics / ENGL 1000 Academic Writing. Each is 3 credits; E2/E3 have no prerequisites.'],['Academic records','COMP 1101 and MATH 1200 Completed, 3 credits each; COMP 1600 In Progress, 3 credits. COMP 2100 is blocked because COMP 1600 is not completed.'],['Degree / categories','93 required; 6 completed; 3 in progress; 84 remaining; 6% completed. Core 3/36 (33 remaining), General Education 3/18 (15), Electives 0/18 (18), Major 0/24 (24), Additional 0/24 (24). Category denominator total 120 was in the original plan; the owner-approved current fictional allocation is 36/18/12/18/9 = 93.']],[W*.25,W*.75])
    p('The table preserves the original planned baseline and expectations. The owner-approved fictional allocation is Core 36, General Education 18, Electives 12, Major 18, Additional 9 (93 total). The 55 new captures show the planned two-course execution: A COMP 1201 + MATH 2250 (2 courses/6 credits), revised A COMP 1201 + ENGL 1000 (2/6), B MATH 2250 (1/3), C COMP 1201 + MATH 2250 then COMP 1201 only, and replacement C ENGL 1000 only (1/3). Degree Progress categories now total 93 (3/36, 3/18, 0/12, 0/18, 0/9).','small')
    for entry in sorted(specifications['UAT'],key=lambda x:x['title'][:6]):
        title,spec=entry['title'],entry['spec'];d=fields(spec)
        steps=re.search(r'\*\*Exact browser steps\*\*\s*(.*?)\n\*\*Expected result:\*\*',spec,re.S).group(1)
        expected=spec.split('**Expected result:**',1)[1].strip()
        steps=' '.join(x.strip() for x in steps.strip().splitlines() if x.strip())
        h(title,2,False)
        rows=[['Field — '+title[:6],'Planned specification'],
          ['Actor / wireframe',d['Actor']+'; '+d.get('Relevant wireframe component',d.get('Wireframe component',''))],
          ['Objective',d['Objective']],['Preconditions',d['Preconditions']],['Test data',d['Test data']],
          ['Steps',steps],['Expected result',expected]]
        table(rows,[W*.20,W*.80])
    note('docs/assignment2/test-plans/uat-test-plan.md; reports/uat-execution.md (planned fields only)')

    page('6.2 Unit Test Plan',level=1)
    p('**Objective.** Verify business decisions in isolation from HTTP, templates and persistence. Test the real AdvisingService with autospecced repository doubles and in-memory SQLModel objects; reject accidental database connections. AuthService orchestration uses mocked repository/security collaborators. UT-23 exercises real local cryptography with controlled time and test-only settings, without database or network access.')
    p('**Components.** AdvisingService dashboard totals, prerequisite eligibility, semester/selection validation, submission delegation, plan edit/review/cancel/removal rules; AuthService; current-user/role dependencies; password/JWT utilities. UT-01–23 identify specifications, not counts of parameterized executions.')
    h('6.2.1 F1 fixture and test design',2,False)
    table([['Fixture / design','Planned specification'],['Actors / terms','S1 Student id 1; S2 independent Student; A1 Advisor. T1=Year 1 semester 1; T2=Year 1 semester 2.'],['Courses','C1 id101 COMP 1100, Core; C2 id102 MATH 1000, General Education; C3 id103 COMP 2000, Core, requires C1; C4 id104 MATH 2000, Electives, no prerequisite; C5 id105 COMP 3000, requires C1 and unknown MATH 9999. Each is 3 credits.'],['Default state','C1 Completed; C2 In Progress; C3/C4 untracked; 93-credit degree; Core requirement 30; empty plan history. Cases override explicitly. F1 is synthetic test data, distinct from the browser seed.'],['Positive / negative / boundary','Positive: eligible selections and legal decisions. Negative: invalid terms, duplicates, missing/foreign resources, bad identity. Boundary: zero totals, cap at 100%, duplicate records, last remaining course and 0/499/500/501 raw feedback characters.'],['Oracle','Literal independently expected values and exact repository calls/no calls. Never mock the method under test or derive the expected answer by calling it. No observed outcomes are included in the tables below.']],[W*.26,W*.74])
    case_matrix(specifications['UT'],'Unit')
    note('docs/assignment2/test-plans/unit-test-plan.md; tests/unit/test_advising.py; tests/unit/test_auth.py')

    page('6.3 Integration Test Plan',level=1)
    p('**Objective and boundary.** Join real FastAPI routes/dependencies, form/JSON parsing, real cookie/JWT authentication, services, repositories and SQLModel persistence. Exercise Student/Advisor workflows and database rollback. IT-19/20 deliberately reach database failures directly because service validation rejects those inputs before SQL.')
    table([['Setup / coverage','Planned specification'],['F2 data','Reuse F1 course/degree meanings but resolve generated row IDs. Seed two Students S1/S2 and Advisor A1, real password hashes, C1 Completed/C2 In Progress for S1, distinctive S2-only records/feedback, and independent plan state per variant.'],['Isolation','Fresh per-case SQLite engine (StaticPool, check_same_thread=False), metadata and foreign keys enabled. New Session per HTTP request and per persistence check. Separate Student/Advisor cookie jars; follow_redirects=False.'],['Startup and cleanup','Rebind test engine/session dependencies and startup/recovery initialization so normal/private DBs cannot be touched. Do not replace authentication, handlers, business methods or CRUD. Close clients/sessions, restore overrides/lifespan/settings and dispose engine.'],['Coverage','Real login/logout; invalid credentials/tokens; current DB roles; course eligibility; Student submission and persistence; Advisor queue and decisions; feedback/resubmission; removal/cancellation/replacement; ownership/privacy; invalid schemas, constraints and atomic rollback.'],['Current contracts','Unauthenticated protected HTML/JSON: 401; authenticated wrong-role guard: 403. HTML business errors: 303 + warning flash. Strict JSON APIs use documented 401/403/404/409/422 semantics. Historical H3/HTTP-200 plan wording is obsolete and adapted below.'],['Limits','SQLite and local HTTP do not prove PostgreSQL, production cookies/CSRF, concurrency or human usability. Current runtime-engine and corrected browser-style tests supplement, rather than replace, F2.']],[W*.26,W*.74])
    case_matrix(specifications['IT'],'Integration')
    h('6.3.1 Corrected-build supplemental plan',2,False)
    p('The retained correction plan adds HTML Student-role denials, actual application SQLite engine enforcement, malformed registration email and computed table/Approved-notice contrast. Expect 403 and unchanged full database snapshots for admin/unknown-role HTML mutations; 422 and no registration writes for malformed email; IntegrityError for orphan links on separately pooled application-engine connections; and readable contrast in normal/hover/Approved states. Manual browser and full Postman retests are still planned, not executed results.')
    note('docs/assignment2/test-plans/integration-test-plan.md; reports/correction-retest-guide.md; tests/integration/test_audit_corrections.py; test_contrast_regression.py')

    page('7. Implementation')
    h('7.1 GitHub Repository')
    p('Repository: ['+REPO+']('+REPO+'). Default branch **main**. The latest retained read-only snapshot identifies commit `edc71e8d8fadecc6c2d173eeddce1a66360a6126` and a complete 442-entry tree.')
    p('**Publication is incomplete.** Main contains the earlier exported Postman JSON and prior application/test work; this workspace has a newer approved-allocation collection revision, current UAT reports and additional evidence that still require the owner’s manual publication. This task does not push or change remotes.')
    table([['Artifact','Repository / local verification'],['Unit implementation',source_link('tests/unit/test_advising.py')+' and '+source_link('tests/unit/test_auth.py')+' are present on main.'],['Integration implementation',source_link('tests/integration/test_student_workflow.py')+', '+source_link('tests/integration/test_advisor_workflow.py')+' and '+source_link('tests/integration/test_database_integrity.py')+' are present. Later allocation/correction work remains local.'],['Postman JSON','Current local `'+COLL+'` is v2.1, 90 requests, revision 2026.10.27-degree93. Its SHA-256 is `6f1a8d297bb5bc4b510963b7a244b7376d60d96531edcaa59c1840f169cad4d3`. Public main has the earlier JSON revision; the new revision is not yet published.'],['Execution evidence','Historical marked-run screenshots and UAT/Runner images are retained locally and embedded in this PDF. The latest corrected-build pytest output/XML/source metadata are attached.']],[W*.26,W*.74])
    h('7.2 Unit Test Implementation')
    p('pytest markers select unit tests with `-m unit`. `tests/unit/conftest.py` patches repository constructors where AdvisingService imports them, supplies autospecced doubles/in-memory model objects, and guards database connections. It preserves the real service logic and tracks mutation calls. `test_advising.py` implements UT-01–19; `test_auth.py` implements UT-20–23. An existing mocked login companion is also in the historical selection.')
    p('The functions under test include get_student_dashboard, prerequisite_ok, get_course_availability, submit_plan, review_plan, cancel_plan, remove_submitted_course, authenticate_user, get_current_user, the role guard and password/JWT utilities. Parameterization covers legal/illegal status matrices and raw feedback-length boundaries. UT-23 uses real hashing/signing; credentials and tokens are never printed here.')
    h('7.2.1 Actual unit implementation example',2,False)
    code(snippet('tests/unit/test_advising.py','test_UT_09_empty_selection'))
    p('Verbatim test from `tests/unit/test_advising.py`. `no_submission` asserts that neither create_plan nor resubmit_plan was called. This checks both the error and early short-circuit behavior; Section 6 contains the plan and Section 8 contains observed execution.','small')

    page('7.3 Integration Test Implementation',level=1)
    p('FastAPI/Starlette TestClient sends real requests through the application. `tests/integration/conftest.py` creates a fresh SQLite engine and schema per case, enables foreign keys, isolates startup/recovery, overrides request sessions and opens independent actor clients. Real password hashing, JWT decoding, current database role lookup, request parsing, services and CRUD remain active. Teardown restores app settings/overrides and closes database resources.')
    table([['Test file','Actual implementation'],['tests/integration/test_student_workflow.py','Student login/cookies/logout, progress/catalogue, form and JSON submission, committed state, ownership/privacy, validation, removal, cancellation and same-ID resubmission.'],['tests/integration/test_advisor_workflow.py','Real Student-to-Advisor queue delivery; decisions through form, generic JSON and named JSON actions; feedback; resubmission and replacement; authorization and validation boundaries.'],['tests/integration/test_database_integrity.py','Real uniqueness/foreign-key constraints and rollback for failed create/resubmit; fresh-session checks of committed state.'],['tests/integration/test_audit_corrections.py','18 additional variants: 12 HTML role denials, 3 malformed-email no-write cases, valid/duplicate registration, and 2 actual engine-integrity cases.'],['tests/integration/test_contrast_regression.py','2 additional variants use the rendered templates and pinned CSS in Chromium; normal/hover table and Approved explanatory text contrast. Browser harness is tests/browser/contrast_probe.cjs.']],[W*.43,W*.57])
    h('7.3.1 Actual workflow implementation example',2,False)
    code(snippet('tests/integration/test_advisor_workflow.py','test_cancelled_plan_leaves_advisor_queue_and_replacement_returns',0,12))
    p('Verbatim opening of the cancellation/queue/replacement test. A real Student cancels a Pending plan, a fresh database snapshot verifies Cancelled status and retained links, and the real Advisor queue becomes empty. The remainder submits a replacement and verifies the new Pending plan. No browser UAT conclusion is inferred.','small')
    p('Separate S1/S2/A1 clients check missing/invalid/expired tokens, current roles, Student denial from Advisor operations and concealment of foreign plans. Negative tests compare committed snapshots after denied writes. `tests/test_advising_api.py`, `test_semester_plans_api.py`, `test_advisor_plans_api.py` and `test_api_security.py` provide additional API/regression coverage in the full suite.')

    page('7.4 API Test Implementation — Postman',level=1)
    p('**Current local collection:** '+coll['info']['name']+'. **Format:** Postman Collection v2.1.0. **Path:** `'+COLL+'`. Revision 2026.10.27-degree93; SHA-256 `6f1a8d297bb5bc4b510963b7a244b7376d60d96531edcaa59c1840f169cad4d3`. It contains 90 requests and strengthened independent oracles for the approved allocation.')
    p('**Publication status:** ['+COLL+']('+REPO+'/blob/main/'+COLL+') resolves to the earlier exported JSON revision. The current degree93 revision is local and remains to be published by the owner. The historical 90-request/470-assertion Runner evidence below is tied to the earlier revision; the current collection has not been rerun.')
    table([['Ordered request group','Requests','Coverage'],['01 Readiness and real cookie authentication','01–12 (12)','Health; anonymous access; malformed cookie; bad/valid Student and Advisor login; independent Student registration/login.'],['02 Role boundaries, progress and catalogue','13–21 (9)','Role denials; response privacy; progress; dynamic eligible/blocked course discovery; free-semester selection.'],['03 Student plan lifecycle and validation','22–50 (29)','Empty/duplicate/unknown/ineligible/invalid submissions; persistence; foreign ownership; duplicate active plan; Pending removal and last-course protection.'],['04 Advisor decisions and resubmission','51–76 (26)','Queue/detail, invalid decisions/shapes, 500/501-character feedback, change request, same-ID resubmission, reject and approve.'],['05 Cancellation, history and logout','77–90 (14)','Preserved approval, cancellation/history/new-ID replacement, queue cleanup, actor logout and no-cookie denial.']],[W*.32,W*.18,W*.50])
    p('**Authentication/cookies.** Login captures each actor’s access_token into separate collection variables. Requests send the intended actor’s Cookie explicitly; the prescribed run disables automatic cookie-jar and redirect handling. HttpOnly cookies are server controls; exported password/token values are blank. Populate run-only credentials privately on a disposable instance. Do not use a normal/private database.')
    p('**Dynamic state.** Collection variables include base_url, actor tokens, discovered course IDs, selected semester and generated plan IDs. Scripts validate response status/schema/privacy, select eligible data, assert persisted decisions and read back after denials. Request 01 initializes run state. Execute one iteration in the original 01–90 order; later requests depend on earlier state.')
    p('**Positive/negative coverage.** Valid operations are paired with expected 401/403/404/409/422 denials, malformed JSON/IDs, spoofed fields, foreign resources, illegal status transitions and feedback boundaries. Static validation parses 90 requests, compiles 93 JavaScript script blocks and covers all 15 JSON operations; static success is distinct from Runner execution.')
    note('docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json; postman/validate_collection.cjs; docs/assignment2/api.md')
    page('7.4.1 API endpoint coverage',level=2,toc=False)
    table([['Method','Implemented JSON endpoint'],['GET','/api/degree-progress'],['GET','/api/courses'],['GET / POST','/api/semester-plans'],['GET / DELETE','/api/semester-plans/{plan_id}'],['PUT','/api/semester-plans/{plan_id}/courses'],['DELETE','/api/semester-plans/{plan_id}/courses/{course_id}'],['GET','/api/advisor/plans'],['GET','/api/advisor/plans/{plan_id}'],['POST','/api/advisor/plans/{plan_id}/review'],['POST','/api/advisor/plans/{plan_id}/approve'],['POST','/api/advisor/plans/{plan_id}/reject'],['POST','/api/advisor/plans/{plan_id}/request-changes'],['GET','/api/users']],[W*.24,W*.76])
    p('The combined GET/POST and GET/DELETE rows each represent two operations: **15 JSON operations** in total. GET /health, POST /login, POST /register and GET /logout provide supporting readiness/session operations. HTML mutation denials and corrected registration behavior require supplemental new-build requests; the historical collection run does not attest them.')
    h('7.4.2 Actual collection-script excerpt',2,False)
    r=next(x for x in req if x['name'].startswith('49 '))
    p(r['name'])
    lines=next(x['script']['exec'] for x in r['event'] if x['listen']=='test')
    short=[]
    for line in lines[:11]:
        # Preserve exact lines, omit whole oversized lines instead of reformatting code.
        if len(line)<110:short.append(line)
        else:break
    if short: code('\n'.join(short))
    p('Contiguous verbatim opening excerpt. The complete current collection is attached. The degree93 revision strengthens request 19/20 oracles; the new assertions passed static validation but have not been run in Postman. No new Runner pass is claimed.','small')

    page('8. Test Reports')
    p('Results below are observed executions, kept separate from Section 6 expectations. No pytest, Postman or browser UAT was rerun for this documentation correction. Historical marked-run and Runner screenshots remain tied to their earlier executions.')
    table([['Execution','Verified actual result','Build / evidence qualification'],['Historical unit-marker run','113 passed; 602 deselected; 1 warning; 6.23s','26 Oct terminal screenshots; earlier source/build.'],['Historical integration-marker run','194 passed; 521 deselected; 1 warning; 30.52s','26 Oct terminal screenshots; earlier source/build.'],['Historical full regression','715 passed; 1 warning; 76.25s; exit 0','27 Oct pre-correction audit text/XML.'],['Intermediate corrected regression','735 passed; 1 warning; 58.11s; exit 0','27 Oct run; superseded by later allocation correction.'],['Latest corrected full regression','751 passed; 1 warning; 122.67s; exit 0','28 Oct retained text/XML and 74 source hashes; zero failures/errors/skips.'],['Historical Postman Runner','90 requests; 470 assertions passed; 0 assertion failures; 0 execution errors','27 Oct earlier JSON revision; 1 iteration; 10s 697ms; current JSON was not rerun.'],['Manual UAT (4-5 Nov 2026)','8 Pass / 0 Fail / 12 Executed - Partially Verified / 0 Not Executed','55 new browser captures; build/URL/DB metadata not retained. Four byte-identical duplicate pairs limit refresh/separate-role claims.']],[W*.23,W*.37,W*.40])
    p('**Counts are not additive across runs.** The historical 715-item suite contains 113 unit + 194 integration + 408 other nodes; the 735-item run contains 113 + 214 + 408. The latest 751-item run contains 116 unit + 227 integration + 408 other nodes. These are membership counts in complete runs, not separately executed marked selections.')
    h('8.1 Unit Test Report')
    p('**Objective:** demonstrate isolated service/authentication rules and repository delegation. **Environment:** Windows/win32; repository .venv; Python 3.14.0; pytest 9.1.1; pluggy 1.6.0; anyio 4.15.1; pytest-asyncio 1.4.0; pyproject.toml. The historical screenshots do not establish a complete dependency lock or exact source/build identifier.')
    p('**Actual command** (from the start capture; run from the repository root):')
    code('$base = Join-Path $env:LOCALAPPDATA "MyAdvisor-A2-Pytest"\n.\\.venv\\Scripts\\python.exe -m pytest tests -m unit -v --basetemp="$base\\unit"')
    p('**Observed summary:** 715 collected, 113 selected, 602 deselected; **113 passed, 1 warning in 6.23s**. Genuine final-result Figure 8.3 follows. No numeric exit code is visible, so none is invented. The latest marked scrollback/XML is incomplete; earlier retained unit XML and the full audit records provide separate supporting evidence.')
    p('**Warning and conclusion:** StarletteDeprecationWarning reports deprecated httpx use with starlette.testclient and suggests httpx2. It is a dependency-maintenance warning, not a failed assertion. The selected run passed its tested cases; it does not establish full UAT, production security or a corrected-build marked rerun.')
    for i,f in enumerate(sorted((H/'screenshots/Unit').glob('*.png')),1):
        figure(f,'8.'+str(i),'8.1 Unit terminal evidence — '+('completed result' if i==3 else 'run capture '+str(i)),f'Genuine terminal capture `{f.name}`; 26 October 2026. '+('Full image plus enlarged original result strip: 113 passed, 602 deselected, 1 warning in 6.23s.' if i==3 else 'Unmodified actual command/environment or passed variants; the final result is in Figure 8.3.')+' Historical source attribution remains qualified.','Landscape',maxh=340 if i==3 else None,detail=(720,1018,1450,1043) if i==3 else None)

    page('8.2 Integration Test Report',level=1)
    p('**Objective:** verify that real authentication, role/ownership dependencies, HTTP parsing, Student/Advisor workflows and database persistence work together. Components include TestClient, FastAPI, services/repositories and per-case SQLModel/SQLite with independent request sessions; database-only cases reach real constraints and rollback.')
    p('**Environment:** Windows/win32, Python 3.14.0, pytest 9.1.1, pluggy 1.6.0, anyio 4.15.1, pytest-asyncio 1.4.0 and pyproject.toml in the repository .venv. Separate actor clients perform real login and cookie handling. Exact latest marked dependency inventory/source hash and numeric exit-code record are missing.')
    p('**Actual command** (same writable temporary base defined in the unit start capture):')
    code('.\\.venv\\Scripts\\python.exe -m pytest tests -m integration -v --basetemp="$base\\integration"')
    p('**Observed summary:** 715 collected, 194 selected, 521 deselected; **194 passed, 1 warning in 30.52s**. Figure 8.6 shows the genuine terminal summary. The warning is the same disclosed TestClient/httpx deprecation. Latest complete marked text/XML is missing; a retained 59-pass Student-only run is narrower and is not substituted for 194.')
    p('**Coverage/conclusion:** queue receipt, approve/reject/request-changes decisions, feedback delivery, same-ID resubmission, removal, allowed/forbidden cancellation, replacement history, cross-user privacy, missing/invalid authentication, validation and fresh-session state assertions. All selected cases passed, but SQLite does not establish PostgreSQL, concurrency, deployed CSRF protection or human acceptance. The 20 correction variants were added later; their full-suite results are reported separately.')
    for i,f in enumerate(sorted((H/'screenshots/Integration').glob('*.png')),4):
        figure(f,'8.'+str(i),'8.2 Integration terminal evidence — '+('completed result' if i==6 else 'run capture '+str(i-3)),f'Genuine terminal capture `{f.name}`; 26 October 2026. '+('Full image plus enlarged original result strip: 194 passed, 521 deselected, 1 warning in 30.52s.' if i==6 else 'Unmodified real Advisor/Student integration variants; final summary in Figure 8.6.')+' Historical source attribution remains qualified.','Landscape',maxh=340 if i==6 else None,detail=(720,1018,1450,1043) if i==6 else None)

    page('8.2.1 Supporting full-suite and corrected-build regression',level=2,toc=False)
    p('**Historical support:** `evidence/audit/pytest-output.txt`, `pytest-results.xml` and `pytest-run.json` retain **715 passed, 0 failures/errors/skips, 1 warning, 76.25s, exit 0**. This run includes both historical marked groups; it is not additive to them.')
    p('**Intermediate corrected run:** `evidence/corrections-2026-10-27/full-20261027T193800Z-7227960f.*` retains **735 passed, 1 warning, 58.11s, exit 0**. This is superseded by the later approved-allocation run. Earlier targeted correction evidence is 284 passed, 1 warning, 86.42s; it overlaps its full run.')
    p('**Latest corrected-build full run:** `evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.*` retains **751 passed, 0 failures/errors/skips, 1 warning, 122.67s, exit 0**. Its 116 unit / 227 integration / 408 other nodes are memberships in that single complete run. The metadata contains 74 application/test SHA-256 entries, all checked against the current files during preflight.')
    p('**Actual full-run command** from retained metadata (absolute paths abbreviated with bracketed location placeholders; original command remains in the attachment):')
    code('python -m pytest tests -q -p no:cacheprovider\n  --basetemp=[unique disposable path] --junitxml=[retained full-run XML]')
    p('**Verbatim latest retained final text line, not a screenshot:**')
    code('751 passed, 1 warning in 122.67s')
    p('Corrected environment metadata records FastAPI 0.141.1, SQLModel 0.0.42, SQLAlchemy 2.0.54, PyJWT 2.14.0, pwdlib 0.3.1 and SQLite 3.50.4. Runs used fresh writable temporary directories and no normal/private database; the unused bootstrap database was not created.')
    p('F01 HTML Student-role guards, F07 actual SQLite connection foreign keys and F08 registration boundary validation are fixed and covered locally. F06 computed contrast checks pass: normal table 14.81:1; hovered row 13.73:1; Approved paragraph 6.56:1. Human readability acceptance and corrected-build Postman/UAT checks remain pending. Old screenshots have not been relabelled as corrected-build proof.')
    note('docs/assignment2/reports/degree-requirement-correction.md; evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.json')

    page('8.3 Postman Collection Run Report',level=1)
    p('**Collection:** MyAdvisor - COMP 3613 Assignment 2, v2.1 export. **Objective:** exercise all 15 JSON operations and supporting real login/registration/logout through the dependent Student/Advisor plan lifecycle, including negative status/role/ownership requests.')
    table([['Execution detail','Observed / qualified value'],['Evidence date','27 October 2026, user-confirmed; Runner displays 01:25:19 AM without an independent time-zone record.'],['Environment','Postman Collection Runner; UI shows environment none / No Environment; 1 iteration, duration 10s 697ms and average response time 29ms. Prescribed local isolated SQLite-backed setup is documented, but exact actual server URL, DB path, Postman version and tested build were not retained.'],['Requests / assertions','90 requests executed; **470 assertions passed**; **zero observed assertion failures**; **zero execution errors**. Six genuine captures collectively show requests 01–90; rows cut at scroll boundaries are not reconstructed.'],['Authentication/authorization','Separate Student/Advisor/independent Student login; expected anonymous and wrong-role denials; foreign ownership concealment and no-write read-back; response privacy.'],['Workflow scenarios','Progress/catalogue, invalid/valid submission, Pending queue, feedback limits, request changes/resubmit, reject/approve, immutable states, removal/cancellation/history/replacement and logout.'],['Conclusion','The recorded historical iteration passed its assertions. The corrected local build requires a new complete collection run and supplemental HTML/registration checks. A passing historical run does not establish the revised collection or close F09/F15.']],[W*.27,W*.73])
    p('The following are genuine historical Runner captures, not generated terminal text or reconstructed results. They show execution of the earlier collection revision, not the current degree93 JSON.')
    post=sorted((H/'postman/Postman Screenshots').glob('*.png'))
    for i,f in enumerate(post+[H/'screenshots/postman-results.png'],7):
        figure(f,'8.'+str(i),'8.3 Postman Runner evidence — '+str(i-6),f'Genuine Runner capture `{f.name}`. Visible summary: 470 assertions, 0 errors, 1 iteration, 10s 697ms. The sequence collectively covers 90 requests; this is historical evidence. Unchanged crop of the run-results area; original file attached.','Portrait',(480,85,1430,1110))

    page('Appendix A — UAT Execution Summary')
    p('**Current UAT disposition (5 November 2026 application date; local captures 4 November 2026, UTC−04:00): 8 Pass / 0 Fail / 12 Executed - Partially Verified / 0 Not Executed.** Tester: Cameron Ramesar. This replaces the earlier 27 October disposition, which is preserved in the [historical execution record](historical-2026-10-27/uat-execution-27oct2026.md). PASS: UAT-04, UAT-05, UAT-06, UAT-10, UAT-14, UAT-15, UAT-16, UAT-17. Partially verified: UAT-01, UAT-02, UAT-03, UAT-07, UAT-08, UAT-09, UAT-11, UAT-12, UAT-13, UAT-18, UAT-19, UAT-20. No case failed and none is wholly unexecuted. The screenshots are new manual browser evidence; no pytest, Postman or browser workflow was rerun for this PDF update.')
    p('**Observed execution data:** A used COMP 1201 + MATH 2250 (2 courses / 6 credits); revised A used COMP 1201 + ENGL 1000 (2 / 6); B used MATH 2250 (1 / 3); C used COMP 1201 + MATH 2250 then COMP 1201 only; replacement C used ENGL 1000 only (1 / 3). Degree Progress categories are 3/36, 3/18, 0/12, 0/18 and 0/9 (93 total), with 6 completed, 3 in progress, 84 remaining, 93 required and 6%. Application-rendered dates are Nov 05, 2026. Actual outcomes, filenames and incomplete substeps are listed below; all 55 supplied UAT images are reproduced in A.2 and attached to the PDF.')
    p('**Duplicate limitation:** four before/after pairs are byte-identical and therefore do not independently prove persistence or separate-role checks: `UAT-01-degree-progress.png` = `UAT-01-after-refresh.png` (SHA-256 `6D9BBB95…`); `UAT-18-baseline.png` = `UAT-18-home.png` (`59942429…`); `UAT-19-advisor-home.png` = `UAT-19-after-refresh.png` (`AE469C9D…`); `UAT-20-student-401.png` = `UAT-20-advisor-401.png` (`67052C79…`). File bytes are preserved; no separate capture is invented.','small')
    rows=[['Case','Latest status','Observed evidence / remaining conditions']]
    for title,body in sorted(uc):
        d=fields(body.split('| Execution field |')[1]);actual=d['Actual result'];status=d['Status']
        observed=actual.split('Data deviation:',1)[0].strip()
        remaining=actual.split('Remaining:',1)[1].strip() if 'Remaining:' in actual else ''
        actual=observed+(' Remaining: '+remaining if remaining else '')
        evidence=d.get('Screenshot evidence reference','')
        evidence=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',evidence)
        if status=='PASS':coverage='Main workflow executed: yes. Core acceptance objective: fully demonstrated for this documented review case. '
        elif status.startswith('NOT EXECUTED'):coverage='Main workflow execution: not established. Core acceptance objective: not demonstrated. '
        else:coverage='Main workflow executed: yes. Core acceptance objective: partially demonstrated; remaining planned checks are not verified. '
        rows.append([title[:6],status,coverage+actual+' Evidence: '+evidence])
    table(rows,[W*.12,W*.24,W*.64])
    p('Historical 27 October UAT images and the earlier image-mapping correction are retained in the archived execution record; they are not reused as evidence for the 5 November outcomes. Browser/version, exact URL/database and build metadata for the new session were not retained, so the evidence is dated but not build-certified.','small')

    h('A.2 UAT screenshot evidence (55 captures)',2)
    p('Each supplied PNG is reproduced below in filename order. The case identifier, state and current disposition are shown in the caption; the original file is attached with matching bytes. These are screen observations, not proof of unperformed steps.','small')
    case_titles={
      '01':'Degree Progress','02':'Course catalogue search and filters','03':'Course selection and ineligible states',
      '04':'Submit semester plan','05':'Pending plan after Home/Messages/relogin','06':'Advisor pending review',
      '07':'Request changes and feedback','08':'Revise and resubmit','09':'Approve revised plan','10':'Separate semester plans',
      '11':'Reject plan','12':'Advisor review of another plan','13':'Remove course from submitted plan',
      '14':'Cancel approved plan','15':'Cancel rejected plan','16':'Cancel pending plan','17':'Replacement plan',
      '18':'Student login and empty baseline','19':'Advisor login and home','20':'Role restrictions and sign-out'}
    status_by={t[:6]:fields(body.split('| Execution field |')[1])['Status'] for t,body in uc}
    uat_files=sorted(UAT_DIR.glob('*.png'))
    hash_groups={}
    for f in uat_files: hash_groups.setdefault(hashlib.sha256(f.read_bytes()).hexdigest(),[]).append(f.name)
    for i,f in enumerate(uat_files,1):
        m=re.match(r'UAT-(\d{2})-(.+)\.png',f.name)
        cid,slug=m.group(1),m.group(2).replace('-',' ')
        digest=hashlib.sha256(f.read_bytes()).hexdigest()
        others=[n for n in hash_groups[digest] if n!=f.name]
        duplicate=' Byte-identical to `'+'`, `'.join(others)+'`; not independent evidence.' if others else ''
        S.extend([NextPageTemplate('Landscape'),PageBreak()])
        img=PILImage.open(f);iw,ih=img.size
        width=LW;height=landscape(A4)[1]-195
        scale=min(width/iw,height/ih)
        stream=io.BytesIO();img.save(stream,format='PNG');stream.seek(0)
        S.append(Image(stream,width=iw*scale,height=ih*scale,hAlign='CENTER'))
        S.append(Spacer(1,7))
        p(f'**Figure A.{i}.** `{f.name}` — UAT-{cid} {case_titles[cid]}: {slug}. Status: **{status_by["UAT-"+cid]}**. Saved 4 November 2026 (UTC−04:00); application date shown as 5 November 2026. Original bytes attached.{duplicate}','caption')
        figures.append({'number':'A.'+str(i),'path':str(f.relative_to(R)).replace('\\','/'),'crop':None,
            'detail_crop':None,'source_sha256':digest,'original_pixels':[iw,ih],
            'display_points':[round(iw*scale,2),round(ih*scale,2)]})
        b.sources.add(f.resolve())

    page('Appendix B — Findings and Readiness')
    p('**Not submission-ready.** The lecturer-aligned structure and genuine evidence are included, but repository publication, revised Postman execution, manual UAT substeps and security/configuration decisions remain outstanding. Historical screenshots and Runner results are not presented as current-build results.')
    rows=[['Finding','Current verified disposition'],
    ['F01 High — HTML role bypass','Fixed locally; real-auth no-write regression variants pass in the corrected full suite. Supplemental browser/Postman HTML checks remain pending.'],
    ['F02 High — revised Postman publication','Earlier JSON revision exists on GitHub. Current degree93 JSON is local, static-validated and not Runner-tested; publish the reviewed revision manually.'],
    ['F03 High — current publication','New allocation code, revised JSON, current reports and UAT/Runner evidence still require owner publication. No push was made for this documentation task.'],
    ['F04 High - manual UAT','8 Pass / 0 Fail / 12 Executed - Partially Verified / 0 Not Executed from 55 new captures. Every case has a genuine primary-workflow screen, but refresh, queue-removal, feedback-reset, empty-baseline and separate-role substeps remain partial; four before/after pairs are byte-identical.'],
    ['F05 Resolved - fictional degree allocation','Owner-approved 36/18/12/18/9 categories total 93 and are covered by the latest 751-pass run and the new UAT-01 capture (3/36, 3/18, 0/12, 0/18, 0/9). The UAT-01 refresh image is byte-identical to the initial image, so persistence is not independently shown; deployed-data checks remain pending. No official UWI curriculum claim.'],
    ['F06 Medium — contrast','Corrected source passes retained automated normal/hover/Approved contrast checks. Human browser readability acceptance remains pending; low-contrast screenshots are historical.'],
    ['F07 Medium — runtime SQLite FKs','Corrected application connections enforce FKs and latest regression evidence passes. Existing private database integrity and PostgreSQL behavior are unverified.'],
    ['F08 Medium — malformed email','Corrected boundary returns controlled 422/no-write behavior in retained regression evidence. New browser/Postman checks remain pending.'],
      ['F09 Medium — CSRF','Open. No explicit CSRF token/Origin check on authenticated form writes; production cookie configured SameSite=None; logout remains GET. No live exploit executed. Deployment design/trusted-origin decision and regressions required.'],
    ['F10 Medium - historical provenance','Latest corrected pytest has retained text/XML and 74 matching application/test hashes. The 55 new UAT images are dated 4-5 November 2026 but the session build/URL/database metadata was not retained. Historical marked/Runner screenshots remain tied to earlier builds.'],
    ['F11 Medium - identity / assembly','Identity verified; this revised lecturer-ordered PDF is assembled and checked. Other readiness items remain open.'],
    ['F12 Low - documentation','Local reports contain the current 8/12/0/0 UAT classification, the 55-image matrix and 751-run facts; remote documentation may remain older until owner publication.'],
    ['F13 Low — Postman runtime evidence','Revised JSON contains stronger independent allocation oracles and passes static validation. A new complete Runner execution is pending.'],
      ['F14 Low — repository cleanup','Open suggestion. Duplicate nested Assignment 1 tree and old logs can confuse execution targets. Use top-level app/tests; no deletion made.'],
      ['F15 Medium — signing-key config','Open. Blueprint requests generated production key, but live runtime was not verified. Settings permit fallback to public example key without a production-strength guard. No private secret leak or actual production use is established.'],
      ['F16 Low — warning','Open/disclosed. One Starlette/httpx deprecation; selected assertions pass. Dependency changes require separate regression evidence.']]
    table(rows,[W*.32,W*.68])
    p('No secrets, password values or authentication-token values are intentionally reproduced. Private database/deployment credentials were neither opened nor copied. Attached source excerpts and text evidence are scanned for known password constants, JWT patterns, private-key headers and credential-bearing URLs; original screenshots are visually reviewed. This is a scoped document check, not a certification of the deployed service.')

    page('Appendix C — Compact Requirements Traceability')
    p('R01–R15 are existing local traceability IDs, not invented lecturer requirements. “Mapped” denotes scope; execution is governed by the qualified reports in Section 8 and Appendix A. The full retained matrix is attached.')
    trace=[['Requirement','Unit / integration plan','UAT / Postman requests'],
    ['R01 Degree totals/categories','UT-01–03; IT-02','UAT-01; PM19. Approved 93-credit allocation; new UAT-01 and revised PM19 execution pending.'],
      ['R02 Completed-only prerequisites','UT-04–06,11; IT-03,14','UAT-02–03; PM20,25.'],
      ['R03 Valid nine semester choices','UT-07–08; IT-14','UAT-02,04,10,12; PM21,26,31.'],
      ['R04 Nonempty/unique eligible selection','UT-09–11; IT-03,14,19','UAT-03–04; PM22–25,27–31.'],
      ['R05 Plan lifecycle and duplicates','UT-12–13,17; IT-05–07,15,17','UAT-04–12; PM39–40,61–80.'],
      ['R06 Advisor decisions / Pending review','UT-14–15,17; IT-05–07,13,17','UAT-06–09,11,20; PM51–78.'],
      ['R07 Optional/500-character feedback','UT-14,16; IT-05–07,16–17','UAT-07–09,11; PM54–60,61,63,69,70,74.'],
      ['R08 Returned-plan same-ID resubmission','UT-12–13; IT-06–07','UAT-08; PM65–68,72.'],
      ['R09 Removal / last-course protection','UT-19; IT-10–11,18','UAT-13; PM36,48–50.'],
      ['R10 Cancellation/history/replacement','UT-18; IT-08–09','UAT-14–17; PM37,64,78–86.'],
      ['R11 Ownership/privacy/role isolation','UT-22; IT-02,11–13','UAT-20; PM13–18,33–38,42–47,81.'],
      ['R12 Authentication/logout','UT-20–23; IT-01,12–13','UAT-18–20; PM02–12,87–90.'],
      ['R13 Persistence / atomic rollback','UT delegation; IT-03–08,19–20','Lifecycle UAT/PM read-backs; fresh DB assertions.'],
      ['R14 Validation/no partial writes','UT-08–11,15–17; IT-14–20','PM22–30,39–47,54–60,71,75–79.'],
      ['R15 Public JSON API contracts','Additional API/security pytest files','All 15 JSON operations in PM01–90; Section 7.4.1.']]
    table(trace,[W*.35,W*.30,W*.35])
    p('Correction supplement: F01/F06/F07/F08 regression checks and the later approved-allocation cases are included in the 751-pass complete run. The 116 unit / 227 integration / 408 other figures are membership counts, not new separate marked executions.')

    page('Appendix D — Lecturer Deliverables Checklist')
    p('This checklist preserves the lecturer’s deliverable wording and order. Page references are filled from the final PDF’s verified bookmarks in the accompanying checklist. “Included” describes document content; outstanding implementation/publication/acceptance requirements remain explicit.')
    table([['Lecturer deliverable (exact wording)','Location / disposition'],['Name & ID','Section 1 — verified name/ID.'],['Project Description','Section 2 — included.'],['Use Case Diagram','Section 3, Figure 3.1 — original included.'],['Entity Relationship Diagram','Section 4, Figures 4.1–4.2 — original and readable keys included.'],['Application Wireframe','Section 5, Figures 5.1–5.4 — original and three enlarged panels included.'],['Test Plans','Section 6 — plans only; external template details unverified.'],['User Acceptance Tests Plan','6.1 — UAT-01–20 with actors, preconditions, data, steps, expected results.'],['Unit Tests','6.2 — UT-01–23 specifications and isolation/boundary strategy.'],['Integration Tests','6.3 — IT-01–20 specifications and corrected-build supplement.'],['Implementation','Section 7.'],['Link to repository','7.1 — clickable intended repository; corrected publication incomplete.'],['Unit Tests','7.2 — actual pytest files, fixtures/mocks and code example.'],['Integration Tests','7.3 — TestClient, isolated DB, actors/auth and workflow example.'],['API Tests (Postman collection exported to JSON in repository)','7.4 — current degree93 JSON is attached. Public main has an earlier export revision; the revised local file remains unpublished and its Runner execution is pending.'],['Reports','Section 8.'],['Unit Tests Report (screenshot of test results)','8.1, Figures 8.1–8.3 — genuine 113-pass marked run.'],['Integration Tests Report (screenshot of test results)','8.2, Figures 8.4–8.6 — genuine 194-pass marked run.'],['Postman Collection Run report screenshot','8.3, Figures 8.7–8.12 — genuine 90-request, 470-pass Runner evidence.']],[W*.53,W*.47])
    p('**Incomplete requirements / readiness:** publish the revised JSON/current code and evidence; execute the revised Postman collection; complete the UAT substeps left partial (refresh persistence, queue removal, cleared feedback, empty A/B/C baselines, separate post-logout role checks) and record build/URL/database metadata; decide CSRF and production signing-key policy; retain historical provenance and one deprecation warning; confirm inaccessible template details. The document is therefore **not submission-ready**.')
    p('**Supporting files:** use the PDF Attachments panel for all 55 UAT screenshots, original unit/integration/Runner screenshots, exported JSON, complete UAT records, plans, traceability, full audits and genuine test logs/XML/source hashes. Appendix A.2 reproduces the same 55 UAT images as visible evidence. Attachments do not replace repository publication.','small')

    doc=Doc(str(OUT),pagesize=A4,leftMargin=b.M,rightMargin=b.M,topMargin=49,bottomMargin=39,
        title='COMP 3613 Assignment 2 — MyAdvisor',author=name,subject='Lecturer-ordered report; evidence qualified; acceptance incomplete')
    for kind,size in [('Portrait',A4),('Landscape',landscape(A4))]:
        ww,hh=size
        doc.addPageTemplates(PageTemplate(kind,[Frame(b.M,39,ww-2*b.M,hh-88,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=footer,pagesize=size))
    doc.multiBuild(S)
    manifest={'candidate':str(OUT.relative_to(R)).replace('\\','/'),'created_utc':datetime.now(timezone.utc).isoformat(),
        'identity':{'name':name,'id':sid,'sources':['docs/transcripts/current-report-export.md','docs/report.pdf']},
        'source_hashes_match_latest_751_run':True,'latest_run_source_files':len(meta['source_sha256']),
        'remote_head':remote['commit'],'remote_tree_sha':remote['sha'],'remote_collection_present':COLL in [x['path'] for x in remote['tree']],
        'template_contents_verified':False,'figures':figures,'uat_screenshot_count':len(list(UAT_DIR.glob('*.png'))),
        'uat_status_counts':UAT_STATUSES,
        'sources':[{'path':str(x.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in sorted(b.sources)],
        'old_pdf_sha256':hashlib.sha256((H/'COMP3613_Assignment2_MyAdvisor.pdf').read_bytes()).hexdigest()}
    (V/'assembly-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    attach_evidence()
    with fitz.open(OUT) as d:
        print(json.dumps({'candidate':str(OUT),'pages':len(d),'toc':d.get_toc(),'attachments':d.embfile_count(),
            'uat_visible_figures':sum(1 for x in figures if x['number'].startswith('A.')),
            'uat_status_counts':UAT_STATUSES},ensure_ascii=True,indent=2))

def case_matrix(entries,kind):
    rows=[['Case / planned inputs and setup' if kind=='Unit' else 'Case / planned input and procedure','Expected output (not an observed result)']]
    for e in entries:
        d=fields(e['spec']);cid=d['Test ID']
        expected=d['Expected Result']
        # Explicit current-contract adaptations, never invented execution outcomes.
        if cid=='UT-22':expected='Missing/invalid/unresolved identity raises HTTP 401; valid identity resolves the repository user. Current require_roles denies regular_user at the Advisor guard with 403 and returns admin. Test the current database role, independently of a token role claim.'
        if cid=='IT-01':expected=expected.replace('protected access denied under H3','protected HTML/JSON access denied with HTTP 401')
        if cid=='IT-12':expected='Protected HTML and JSON requests return HTTP 401 for missing/malformed/expired/wrong-signature/nonexistent-user tokens, with no private data and no database writes. This replaces the obsolete H3/HTTP-200 expectation.'
        if cid=='IT-13':expected='Authenticated Student access to Advisor queue/review returns HTTP 403. No queue/private data or status/feedback/advisor/course-link changes. This replaces obsolete H3/HTTP-200 wording.'
        left='**'+e['title']+'**<br/>' if False else '**'+e['title']+'**\n'
        left+='**Component:** '+d['Source Function or Endpoint']+'\n'
        left+='**Preconditions:** '+d['Preconditions']+'\n'
        left+='**Inputs:** '+d['Test Data']+'\n'
        if kind=='Integration':left+='**Procedure:** '+d['Test Steps']
        rows.append([left,expected])
    table(rows,[W*.56,W*.44])
    if kind=='Unit':p('Current role-contract clarification for UT-22 is adapted from the actual require_roles implementation (401 identity / 403 wrong role). Other original inputs/oracles are retained. E01/E06/E07/E08 references denote existing database-backed baseline tests in tests/test_advising_service.py; their original planning notes avoid duplicate coverage.','small')
    else:p('IT-01/12/13 explicitly use the current 401/403 contract in place of historical H3. The original source documents remain attached unchanged. These adaptations are planned expectations, not new observations.','small')

def attach_evidence():
    paths=[R/COLL,H/'test-plans/uat-test-plan.md',H/'test-plans/unit-test-plan.md',H/'test-plans/integration-test-plan.md',
        H/'reports/uat-execution.md',H/'reports/uat-final-report.md',H/'reports/uat-evidence-review.md',H/'reports/uat-supplemental-evidence.md',H/'reports/requirements-test-traceability.md',H/'PROGRESS.md',
        H/'final-quality-audit.md',H/'reports/audit-correction-report.md',H/'reports/correction-retest-guide.md',
        H/'reports/repository-publication-plan.md',H/'reports/unit-test-report.md',H/'reports/integration-test-report.md',H/'reports/postman-test-report.md',
        H/'reports/historical-2026-10-27/uat-execution-27oct2026.md',H/'reports/historical-2026-10-27/uat-final-report-27oct2026.md',
        H/'reports/historical-2026-10-27/uat-evidence-review-27oct2026.md',H/'reports/historical-2026-10-27/uat-supplemental-evidence-27oct2026.md']
    paths+=list((H/'screenshots').rglob('*.png'))+list((H/'postman/Postman Screenshots').glob('*.png'))
    for folder,pattern in [(H/'evidence/audit','pytest-*'),(H/'evidence/corrections-2026-10-27','full-20261027T193800Z-7227960f.*'),(H/'evidence/corrections-2026-10-27','targeted-20261027T193352Z-b6385978.*'),(H/'evidence/degree-requirements-2026-10-27','full-20261028T015858Z-e5cbdcfb.*')]:
        paths+=list(folder.glob(pattern))
    paths += [H/'evidence/corrections-2026-10-27/verified-summary.json',H/'evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.json',H/'completion-review-2026-10-27/remote-tree.json']
    paths=sorted(set(paths))
    assert len(list(UAT_DIR.glob('*.png')))==55
    known=['bobpass','adminpass','student-integration-password','student-unit-password']
    attach=[]
    with fitz.open(OUT) as d:
        for f in paths:
            data=f.read_bytes()
            if f.suffix in ('.md','.txt','.json','.xml'):
                t=data.decode('utf-8-sig')
                for s in known:t=t.replace(s,'[test password redacted]')
                # Collection values are already blank; no token value is added.
                assert not re.search(r'eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}',t)
                assert '-----BEGIN PRIVATE KEY-----' not in t
                assert not re.search(r'postgres(?:ql)?://[^\s:/]+:[^\s@]+@',t)
                data=t.encode('utf-8')
            rel=str(f.relative_to(R)).replace('\\','/')
            name=rel.replace('/','__')
            d.embfile_add(name,data,filename=f.name,ufilename=f.name,desc=rel+(' — password constants redacted' if data!=f.read_bytes() else ' — original bytes'))
            attach.append({'name':name,'source':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'original_bytes':data==f.read_bytes()})
        d.saveIncr()
    # Preserve exact collection bytes (including original final newline) as required.
    with fitz.open(OUT) as d:
        key=COLL.replace('/','__')
        if d.embfile_get(key)!=(R/COLL).read_bytes():
            d.embfile_upd(key,buffer=(R/COLL).read_bytes(),desc=COLL+' — exact original sanitized export')
            d.saveIncr()
            for a in attach:
                if a['name']==key:a.update(bytes=(R/COLL).stat().st_size,sha256=hashlib.sha256((R/COLL).read_bytes()).hexdigest(),original_bytes=True)
    (V/'attachments-manifest.json').write_text(json.dumps(attach,indent=2),encoding='utf-8')

if __name__=='__main__':build()
