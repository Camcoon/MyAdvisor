"""Documentation-only A2 assembly; reads existing plans, reports and evidence.

Run from the repository root with .venv/Scripts/python.exe
docs/assignment2/build_submission.py. PDF libraries may be installed in .pdf-tools.
Original artifacts and application/test sources are never written.
"""
from pathlib import Path
import sys, re, json, hashlib, html, textwrap, xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE / '.pdf-tools'))
from PIL import Image as PILImage
from markdown_it import MarkdownIt
from reportlab.pdfgen import canvas
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, NextPageTemplate, Table, TableStyle, Image, KeepTogether, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = HERE / 'COMP3613_Assignment2_MyAdvisor.pdf'
REVIEW = HERE / 'pdf-review'
REVIEW.mkdir(exist_ok=True)
NAVY = colors.HexColor('#17324d')
TEAL = colors.HexColor('#087d87')
LIGHT = colors.HexColor('#eef4f7')
GRAY = colors.HexColor('#52616b')
RED = colors.HexColor('#8f342b')
PW, PH = A4
M = 43
W = PW - 2*M
for name, filename in [('Body','DejaVuSans.ttf'),('Body-Bold','DejaVuSans-Bold.ttf'),
                       ('Body-Italic','DejaVuSans-Oblique.ttf'),('Body-BoldItalic','DejaVuSans-BoldOblique.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(ROOT/'vendor/fonts'/filename)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Body-Bold', italic='Body-Italic', boldItalic='Body-BoldItalic')
styles = {
 'body': ParagraphStyle('body',fontName='Body',fontSize=9.2,leading=13,spaceAfter=6,textColor=NAVY,splitLongWords=True),
 'small': ParagraphStyle('small',fontName='Body',fontSize=8,leading=11,spaceAfter=5,textColor=GRAY,splitLongWords=True),
 'cell': ParagraphStyle('cell',fontName='Body',fontSize=8.4,leading=11.6,spaceAfter=0,textColor=NAVY,splitLongWords=True),
 'th': ParagraphStyle('th',fontName='Body-Bold',fontSize=8.4,leading=11.6,textColor=colors.white),
 'h1': ParagraphStyle('h1',fontName='Body-Bold',fontSize=20,leading=26,spaceAfter=13,textColor=NAVY,keepWithNext=True),
 'h2': ParagraphStyle('h2',fontName='Body-Bold',fontSize=13,leading=18,spaceBefore=12,spaceAfter=8,textColor=TEAL,keepWithNext=True),
 'h3': ParagraphStyle('h3',fontName='Body-Bold',fontSize=10,leading=14,spaceBefore=10,spaceAfter=6,textColor=NAVY,keepWithNext=True),
 'caption': ParagraphStyle('caption',fontName='Body',fontSize=8.4,leading=12,spaceAfter=6,textColor=GRAY),
 'code': ParagraphStyle('code',fontName='Body',fontSize=7.5,leading=10.5,spaceAfter=6,backColor=LIGHT,borderPadding=7,textColor=NAVY),
}
md = MarkdownIt('commonmark').enable('table')
sources = set()
references = []
images = []
story = []
headings = []

def read(p):
    p = (ROOT/p).resolve() if not isinstance(p, Path) else p.resolve()
    sources.add(p)
    return p.read_text(encoding='utf-8-sig')

def redact(s):
    # These are demo passwords, but submission text deliberately exposes none.
    for value in ('bobpass','adminpass','student-integration-password','student-unit-password'):
        s=s.replace(value, '[test password redacted]')
    return s.replace('\x00','')

def inline(s, base=HERE):
    s=redact(s)
    # Parse genuine Markdown inline tokens; preserve external links only.
    toks=md.parseInline(s)[0].children or []
    out=[]; link_stack=[]
    for t in toks:
        if t.type=='text': out.append(html.escape(t.content))
        elif t.type=='code_inline': out.append('<font color="#355c70">'+html.escape(t.content)+'</font>')
        elif t.type=='strong_open': out.append('<b>')
        elif t.type=='strong_close': out.append('</b>')
        elif t.type=='em_open': out.append('<i>')
        elif t.type=='em_close': out.append('</i>')
        elif t.type in ('softbreak','hardbreak'): out.append('<br/>')
        elif t.type=='link_open':
            url=t.attrGet('href')
            if url.startswith(('https://','http://')):
                out.append('<a href="'+html.escape(url,quote=True)+'" color="#087d87">');link_stack.append(True)
            else:
                from urllib.parse import unquote
                target=(base/unquote(url.split('#')[0])).resolve()
                if url.split('#')[0]: references.append((str(base),url,target.exists()))
                link_stack.append(False)
        elif t.type=='link_close':
            if link_stack.pop():out.append('</a>')
        elif t.type=='image': out.append(html.escape(t.content)+' (original evidence reproduced in this document)')
    return ''.join(out)

def para(s, style='body', base=HERE):
    return Paragraph(inline(s,base),styles[style])

def p(s,style='body'): story.append(para(s,style))

def heading(s,level=0,toc=True):
    obj=para(s, ['h1','h2','h3'][min(level,2)])
    if toc:
        obj.toclevel=min(level,1); obj.bookmark='section-'+str(len(headings));headings.append(s)
    story.append(obj)

def section(s):
    story.extend([NextPageTemplate('Portrait'),PageBreak()]); heading(s)

def table(rows, widths=None, base=HERE, header=True):
    n=len(rows[0]); widths=widths or ([W*.25,W*.75] if n==2 else [W/n]*n)
    data=[[para(cell,'th' if header and i==0 else 'cell',base) for cell in row] for i,row in enumerate(rows)]
    tab=Table(data,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT',splitByRow=1,splitInRow=1)
    commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
              ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
              ('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cbd8df'))]
    if header: commands += [('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT])]
    else: commands += [('BACKGROUND',(0,0),(0,-1),LIGHT)]
    tab.setStyle(TableStyle(commands));story.extend([tab,Spacer(1,8)])

def markdown(s,base=HERE, skip_title=True):
    tokens=md.parse(redact(s));i=0;list_depth=0
    while i<len(tokens):
        t=tokens[i]
        if t.type=='heading_open':
            text=tokens[i+1].content
            if not(skip_title and t.tag=='h1'): heading(text,2,False)
            i+=3;continue
        if t.type=='paragraph_open':
            content=tokens[i+1].content
            if not content.startswith('!['):
                story.append(para(('• ' if list_depth else '')+content,base=base))
            i+=3;continue
        if t.type in ('bullet_list_open','ordered_list_open'):list_depth+=1
        elif t.type in ('bullet_list_close','ordered_list_close'):list_depth-=1
        elif t.type in ('fence','code_block'):
            code=t.content
            if t.info=='mermaid': p('The original Mermaid ERD is rendered in Section 5.','small')
            else:
                for block in [code.splitlines()[j:j+28] for j in range(0,len(code.splitlines()),28)]:
                    text='<br/>'.join(html.escape(x).replace(' ','&#160;') for x in block)
                    story.append(Paragraph(text,styles['code']))
        elif t.type=='table_open':
            rows=[];i+=1
            while tokens[i].type!='table_close':
                if tokens[i].type=='tr_open':
                    row=[];i+=1
                    while tokens[i].type!='tr_close':
                        if tokens[i].type=='inline':row.append(tokens[i].content)
                        i+=1
                    rows.append(row)
                i+=1
            if len(rows[0])<=4: table(rows,base=base)
            else:
                # Wide source matrices become readable vertical records without losing fields.
                for row in rows[1:]:
                    heading(row[0],2,False)
                    table([['Field','Recorded detail']]+[[k,v] for k,v in zip(rows[0][1:],row[1:])],base=base)
        i+=1

def source_note(path): p('Source: `'+str(path).replace('\\','/')+'`.','small')

def extract_section(text,title):
    pattern=r'^## '+re.escape(title)+r'\s*\n(.*?)(?=^## |\Z)'
    m=re.search(pattern,text,re.M|re.S)
    return m.group(1) if m else ''

def cases(text,prefix):
    return re.findall(r'^### ('+prefix+r'-\d{2}[^\n]*)\n(.*?)(?=^### '+prefix+r'-\d{2}|^## |\Z)',text,re.M|re.S)

def table_rows(text):
    return [line.strip().strip('|').split(' | ') for line in text.splitlines() if line.startswith('|') and not re.match(r'^\|[- :|]+\|\s*$',line)]

class Plate(Flowable):
    def __init__(self,path,caption,crop=None,portrait=False):
        Flowable.__init__(self); self.path=path;self.caption=caption;self.crop=crop
        size=A4 if portrait else landscape(A4)
        self.width=size[0]-2*M;self.height=size[1]-144
    def draw(self):
        from reportlab.lib.utils import ImageReader
        img=PILImage.open(self.path)
        if self.crop: img=img.crop(self.crop)
        iw,ih=img.size; w=self.width;h=self.height-34
        scale=min(w/iw,h/ih)
        dw,dh=iw*scale,ih*scale
        self.canv.drawImage(ImageReader(img),(w-dw)/2,34+(h-dh)/2,dw,dh,mask='auto')
        cap=para(self.caption,'caption');cap.wrap(w,40);cap.drawOn(self.canv,0,0)

def plate(path,title,caption,crop=None,portrait=False):
    path=path.resolve(); assert path.exists(),path
    sources.add(path); images.append({'path':str(path.relative_to(ROOT)).replace('\\','/'),'title':title,'crop':crop})
    story.extend([NextPageTemplate('Portrait' if portrait else 'Landscape'),PageBreak()]);heading(title,2,False)
    story.append(Plate(path,caption,crop,portrait))

class ERD(Flowable):
    """Vector transcription of the genuine seven-entity Mermaid source."""
    def __init__(self,src):
        Flowable.__init__(self);self.src=src;self.width=landscape(A4)[0]-86;self.height=450
    def draw(self):
        c=self.canv; positions={'USER':(250,278),'DEGREE_PROGRAM':(0,278),'DEGREE_REQUIREMENT':(0,54),
          'SEMESTER_PLAN':(500,278),'COURSE':(250,54),'STUDENT_COURSE':(500,54),'PLAN_COURSE':(500,165)}
        fields={name:body.strip().splitlines() for name,body in re.findall(r'  (\w+) \{(.*?)\n  \}',self.src,re.S)}
        # Fixed compact boxes retain every field; longer status strings appear in the legend.
        sizes={name:(224,28+len(fs)*11) for name,fs in fields.items()}
        # Explicit elbow routes avoid hiding relationships behind intervening boxes.
        routes=[([(224,321),(250,321)],'enrolls',(225,328)),
          ([(112,278),(112,126)],'defines',(119,204)),
          ([(474,355),(500,355)],'creates',(474,363)),
          ([(474,305),(500,305)],'reviews',(474,298)),
          ([(420,278),(420,258),(486,258),(486,100),(500,100)],'completes',(425,247)),
          ([(474,100),(500,100)],'appears_in',(460,87)),
          ([(390,159),(390,198),(500,198)],'appears_in',(398,204)),
          ([(612,278),(612,237)],'contains',(619,254))]
        for points,label,(lx,ly) in routes:
            c.setStrokeColor(colors.HexColor('#8aa8b8'));c.setLineWidth(.8)
            path=c.beginPath();path.moveTo(*points[0])
            for point in points[1:]:path.lineTo(*point)
            c.drawPath(path)
            c.setFillColor(TEAL);c.setFont('Body',5.8);c.drawString(lx,ly,label)
        for name,fs in fields.items():
            x,y=positions[name];w,h=sizes[name]
            c.setFillColor(colors.white);c.setStrokeColor(TEAL);c.roundRect(x,y,w,h,4,fill=1,stroke=1)
            c.setFillColor(NAVY);c.rect(x,y+h-21,w,21,fill=1,stroke=0)
            c.setFillColor(colors.white);c.setFont('Body-Bold',8);c.drawString(x+7,y+h-14,name)
            c.setFillColor(NAVY);c.setFont('Body',7.1)
            for idx,f in enumerate(fs):
                f=re.sub(r'".*?"','',f).strip()
                c.drawString(x+7,y+h-34-idx*11,f)

class SubmissionDoc(BaseDocTemplate):
    def afterFlowable(self,flowable):
        if hasattr(flowable,'bookmark'):
            self.canv.bookmarkPage(flowable.bookmark)
            self.canv.addOutlineEntry(flowable.getPlainText(),flowable.bookmark,flowable.toclevel,False)
            self.notify('TOCEntry',(flowable.toclevel,flowable.getPlainText(),self.page,flowable.bookmark))

def footer(c,d):
    w,h=c._pagesize
    if d.page>1:
        c.setFont('Body',8);c.setFillColor(GRAY);c.drawString(M,h-25,'MYADVISOR  |  COMP 3613 — ASSIGNMENT 2')
        c.setStrokeColor(colors.HexColor('#ccd9df'));c.line(M,h-32,w-M,h-32)
    c.setFont('Body',7.5);c.setFillColor(GRAY)
    c.drawString(M,22,'27 October 2026  •  Evidence reviewed; acceptance incomplete')
    c.drawRightString(w-M,22,str(d.page))

def build():
    # Preflight: counts and identity come from genuine retained materials.
    transcript=read('docs/transcripts/current-report-export.md')
    identity=re.search(r'add my name ([^\n]+?) and my Student ID (\d+)',transcript)
    assert identity, 'Explicit student identity statement missing'
    student_name,student_id=identity.groups()
    xml=ET.parse(HERE/'evidence/audit/pytest-results.xml')
    nodes=xml.findall('.//testcase');assert len(nodes)==715
    assert not xml.findall('.//failure') and not xml.findall('.//error')
    audit=read(HERE/'final-quality-audit.md')
    brief=read(HERE/'official-assignment-brief.md')
    read(HERE/'PROGRESS.md')
    uat=read(HERE/'reports/uat-execution.md')
    uat_cases=cases(uat,'UAT');assert len(uat_cases)==20
    statuses=[re.search(r'\| Pass/Fail/Not Run \| (Pass|Fail|Not Run) \|',b).group(1) for _,b in uat_cases]
    assert {s:statuses.count(s) for s in set(statuses)}=={'Pass':1,'Not Run':19}
    ut=read(HERE/'test-plans/unit-test-plan.md');it=read(HERE/'test-plans/integration-test-plan.md')
    assert len(cases(ut,'UT'))==23 and len(cases(it,'IT'))==20
    original=read('docs/report.md')
    erd=re.search(r'```mermaid\n(erDiagram.*?)```',original,re.S).group(1)
    (REVIEW/'original-erd.mmd').write_text(erd,encoding='utf-8')

    cover=para('1. Cover page','small');cover.toclevel=0;cover.bookmark='cover';story.append(cover)
    story.append(Spacer(1,58));p('COMP 3613 — ASSIGNMENT 2','h2')
    story.append(Spacer(1,15))
    story.append(Paragraph('MyAdvisor',ParagraphStyle('cover',parent=styles['h1'],fontSize=38,leading=46)))
    p('Implementation, Test Planning and Verified Test Reporting','h2')
    story.append(Spacer(1,36))
    table([['Submission detail','Verified value'],['Student name',student_name],['University ID',student_id],
           ['Submission document date','27 October 2026'],['Repository','https://github.com/Camcoon/MyAdvisorWithTests']])
    p('Readiness: **NOT SUBMISSION-READY — material audit issues remain open.**')
    p('This is the requested single-PDF compilation of the implemented project and retained evidence. It does not certify acceptance. UAT: 1 Pass, 0 Fail, 19 Not Run, including 18 partially verified cases. No application code or test results were regenerated.')
    p('Identity source: explicit student statement in the retained Assignment 1 report-export transcript, corroborated by the original PDF cover. The eight-digit ID displayed in demo screens is seeded data. University/campus and full course title are omitted because the reviewed assignment materials do not verify their wording.','small')
    section('2. Table of contents')
    p('The numbered page footer is the PDF page number, including the cover. Section 1 is the cover on page 1. Landscape evidence pages continue the same numbering.','small')
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc0',fontName='Body',fontSize=10,leading=17,spaceBefore=4,textColor=NAVY),ParagraphStyle('toc1',fontName='Body',fontSize=9,leading=14,leftIndent=14,textColor=GRAY)]
    story.append(toc)
    section('3. Project description')
    p('MyAdvisor supports academic advising through three connected workflows: WF1 — Track Degree Progress (Student); WF2 — Plan Semester Course Selections (Student); and WF3 — Review and Approve Course Plans (Advisor). Students inspect recorded academic progress, select eligible courses and submit semester plans. Advisors review a shared Pending queue and return a decision and optional feedback.')
    p('Assignment 1 established the Student and Advisor dashboards, degree/program and course models, three-panel wireframe, prerequisite checks, plan submission, decisions, cancellation and resubmission. Assignment 2 adds explicit JSON API contracts, authenticated role and ownership boundaries, isolated unit tests, real-authentication integration tests, a 90-request Postman collection, manual acceptance records and cross-method traceability. The original artifacts remain intact.')
    table([['Actor','Implemented functionality'],['Student (regular_user)','Login; Home, Degree Progress, Plan Courses, Messages and Profile; course search/filter and prerequisite eligibility; review/submit selections; revise returned plans; remove Pending courses; cancel permitted plans and create replacements.'],['Advisor (admin)','Login; Advisor workspace and shared Pending queue; inspect Student/program/course totals; Approve, Reject or Request Changes with optional feedback.']])
    p('Plans use nine fixed Year 1–3 / semester 1–3 options; semester 3 is summer. Pending and Approved block duplicate active submissions; Changes Requested and Rejected are resubmitted under the same ID. Cancellation permits Pending, Approved and Rejected, retains history and allows a fresh plan ID. The current authorization defect affecting HTML mutations is detailed in Section 11.')
    table([['Layer','Verified technology / purpose'],['Backend','Python; FastAPI; Pydantic request/response validation; SQLModel/SQLAlchemy persistence; SQLite in retained local tests.'],['Frontend','Jinja2 HTML templates; Bootstrap/AdminLTE navigation; CSS and JavaScript selection/review controls.'],['Authentication','Password hashing with pwdlib/Argon2; signed JWT login cookie; current database role and ownership checks.'],['Verification','pytest 9.1.1; FastAPI/Starlette TestClient; mocks/autospec; isolated SQLite; Postman Collection Runner and v2.1 JSON export.']])
    source_note('docs/report.md; app/models; app/routers; tests; docs/assignment2/api.md')
    heading('3.1 Evidence and audit review',1)
    p('The official Assignment 2 wording is the student-supplied brief retained in official-assignment-brief.md, with four equally weighted components: Implementation, Test Plans, Test Implementation and Test Reporting (25% each). The assessment is weighted 15%. Both linked Google templates remain inaccessible on this review; no unverified template requirement is invented. The Assignment 1 rubric and historical competency scores are excluded.')
    p('No Critical finding is verified. Open High findings F01–F05 concern authorization, published collection/evidence availability, incomplete UAT and degree requirements. The PDF assembly portion of F11 is addressed here; verified identity was recovered from original materials. This does not close the five High findings.')

    section('4. Use case diagram')
    p('The original UML diagram below is reproduced from docs/diagrams/use-case.png. Student use cases cover progress, selection, submission and cancellation; Advisor use cases cover review and decisions. The diagram is an Assignment 1 design artifact, not an execution result.')
    imagepath=ROOT/'docs/diagrams/use-case.png';sources.add(imagepath)
    im=PILImage.open(imagepath);iw,ih=im.size
    story.append(Image(str(imagepath),width=W,height=W*ih/iw))
    p('Figure 4.1. Genuine Assignment 1 Use Case Diagram.','caption')
    p('Course selection and submission depend on eligibility checks; the Advisor reviews the selected courses before approval/rejection/change requests. Resubmission returns a revised plan to the same review workflow. Login supports both actors; hiding navigation is not sufficient authorization, as the audit demonstrates.')

    section('5. Entity relationship diagram')
    p('The seven-entity ERD in the original report matches the current SQLModel entities and foreign keys. The next landscape page renders that genuine Mermaid source as vector boxes; the relationship table retains its exact cardinalities and labels. No invented entities or changed degree requirements are introduced.')
    table([['Relationship from original ERD','Meaning'],['DEGREE_PROGRAM o|--o{ USER : enrolls','A User may have zero or one program; a program can have many Users.'],['DEGREE_PROGRAM ||--o{ DEGREE_REQUIREMENT : defines','Each requirement belongs to one program.'],['USER ||--o{ SEMESTER_PLAN : creates','Each plan has one Student creator.'],['USER o|--o{ SEMESTER_PLAN : reviews','A plan may have zero or one assigned Advisor; a User may review many plans.'],['USER ||--o{ STUDENT_COURSE : completes','Academic record joins a Student and a course, with status/grade/date.'],['COURSE ||--o{ STUDENT_COURSE : appears_in','Each academic record refers to one course.'],['COURSE ||--o{ PLAN_COURSE : appears_in','Each selected-plan row refers to one course.'],['SEMESTER_PLAN ||--o{ PLAN_COURSE : contains','PlanCourse implements the plan/course association.']])
    p('StudentCourse has a unique (student_id, course_id) pair; PlanCourse has a unique (plan_id, course_id) pair; DegreeRequirement is unique by (program_id, category). Plan status is Pending, Approved, Rejected, Changes Requested or Cancelled. The runtime SQLite foreign-key enforcement gap remains F07; declared relationships do not prove runtime enforcement.')
    story.extend([NextPageTemplate('Landscape'),PageBreak()]);heading('Figure 5.1. Original seven-entity ERD',2,False);story.append(ERD(erd))
    p('Vector rendering of docs/report.md Mermaid source; all fields retained. Connecting lines indicate related boxes; exact cardinalities and relationship names are in the preceding table. Quoted status/semester constraints are explained there.','caption')

    section('6. Original wireframe and implemented interface')
    p('The original three-panel Assignment 1 wireframe is preserved below. Panel 1 becomes Degree Progress; panel 2 becomes Plan Courses, selection count and Review Selected Courses; panel 3 becomes Advisor Review with Approve Plan, Reject Plan and Request Changes. Home and Messages expose the latest plan and decision feedback. Cancellation and revision extend the original workflow and are tested explicitly.')
    p('The wireframe’s example 120-credit totals and calendar-year labels are illustrative design data. Executed screens use the current 93-credit degree and nine fixed semester labels. The discrepancy between 93 degree credits and 120 category credits remains unresolved; it is not justified by the mockup.')
    wire=ROOT/'docs/wireframes/Three-Panel Student Advisor Dashboard Mockup.png'
    plate(wire,'Figure 6.1. Original Assignment 1 wireframe','Original complete three-panel image. Source: docs/wireframes/Three-Panel Student Advisor Dashboard Mockup.png.')
    # Individual panels enlarge original pixels only; original is always retained.
    for j in range(3):
        plate(wire,f'Figure 6.{j+2}. Wireframe panel {j+1} — enlarged original detail','Unmodified pixel excerpt of the original wireframe, enlarged for readability; illustrative values are not observed test results.',(j*512,0,(j+1)*512,1024),portrait=True)

    section('7. Test planning')
    p('Detailed specifications below preserve the genuine case IDs, inputs, steps and expected outcomes. Plan preparation records and current execution reports have different dates. Historical Not Run fields are not used as the latest result. Original case inputs remain distinct from the actual three-course UAT substitution. Local R/UT/IT identifiers are project traceability labels, not official rubric IDs.')
    heading('7.1 User Acceptance Test Plan',1)
    source_note('docs/assignment2/test-plans/uat-test-plan.md; reports/uat-execution.md')
    read(HERE/'test-plans/uat-test-plan.md')
    for title in ['Purpose and basis','Accuracy review of the UAT plan']:
        markdown(extract_section(uat,title),HERE/'reports',False)
    baseline=uat[uat.index('### Test data baseline'):uat.index('## Verified screenshot evidence')]
    markdown(baseline,HERE/'reports',False)
    p('Planned setup: disposable SQLite, dedicated local port 5002, separate Student/Advisor browser profiles and JavaScript enabled. Existing databases must not be reset. Exact actual browser, database path, build and base URL were not supplied. Test account secrets are deliberately omitted. A/B/C mean Year 1 semesters 1/2/3. Execution order: UAT-18, UAT-01–05, UAT-19, UAT-06–17, UAT-20.')
    for title,body in uat_cases:
        heading(title,2,False)
        planned=body.split('| Execution field |')[0]
        markdown(planned,HERE/'reports',False)
    for number,label,source,txt,prefix,fixture in [
        ('7.2','Unit Test Plan','test-plans/unit-test-plan.md',ut,'UT',['Shared rule interpretation','Objective and isolation strategy','F1 — in-memory fixture vocabulary']),
        ('7.3','Integration Test Plan','test-plans/integration-test-plan.md',it,'IT',['Shared rule interpretation','Objective and integration boundary','F2 — isolated SQLModel environment and data','HTTP response and persistence oracles'])]:
        story.append(PageBreak());heading(number+'. '+label,1);source_note('docs/assignment2/'+source)
        p('The following are the original specifications. Historical planning statements about absent API routes or HTML/200 authorization are superseded by the current API and report evidence in Sections 8–11. Planned inputs and expected-result text remain verbatim; the original plan’s out-of-date execution fields and proposed evidence filenames are excluded from these specification tables. Current execution mappings follow in Section 9.')
        for title in fixture:
            heading(title,2,False);markdown(extract_section(txt,title),HERE/'test-plans',False)
        if prefix=='UT':
            heading('Existing baseline tests E01–E12 used by both plans',2,False)
            markdown(extract_section(ut,'Existing coverage reviewed before planning'),HERE/'test-plans',False)
        for title,body in cases(txt,prefix):
            heading(title,2,False)
            rows=table_rows(body)
            rows=[r for r in rows if r[0].strip() not in ('Actual Result','Status','Evidence Reference')]
            table(rows,base=HERE/'test-plans')
            if prefix=='IT' and title.startswith(('IT-12','IT-13')):
                p('Current contract clarification: historical H3/HTTP-200 text in the preserved expectation above is superseded. Current unauthenticated HTML/JSON requests return 401; logged-in wrong-role requests guarded by the role dependency return 403. Current execution evidence is in Section 9.2; the separate HTML Student-mutation role gap remains F01.','small')

    section('8. Test implementation')
    heading('8.1 Environment and CLI',1)
    p('Retained marked-run screenshots show Windows/win32, Python 3.14.0, pytest 9.1.1, pluggy 1.6.0, anyio 4.15.1 and pytest-asyncio 1.4.0 in the repository .venv. Historical unit metadata records FastAPI 0.141.1, SQLModel 0.0.42, PyJWT 2.14.0 and pwdlib 0.3.1; those versions are not independently visible in the later marked screenshots. CLI marker selection is configured in pyproject.toml.')
    p('The full audit run retains its command, exit code 0 and source hashes. Marked runs use a writable --basetemp under LOCALAPPDATA after an earlier Windows temp-directory issue. This PDF task does not rerun pytest, Postman or browser cases.')
    heading('8.2 Unit implementation and independent oracles',1)
    p('tests/unit/conftest.py supplies in-memory model objects, autospecced repository doubles and guards against accidental connection access. UT-01–19 exercise the real AdvisingService while observing repository delegation; UT-20–23 cover authentication orchestration, database-resolved roles, hashing and JWT contracts. Real cryptography in UT-23 remains isolated from persistence. Literal arithmetic expected values prevent a test from merely repeating the service formula.')
    code=read('tests/unit/test_advising.py');snippet=code[code.index('def test_UT_01_'):code.index('@pytest.mark.parametrize')]
    markdown('```python\n'+textwrap.fill('',80)+snippet+'```',ROOT,False)
    source_note('tests/unit/test_advising.py: test_UT_01_degree_totals_and_category (verbatim)')
    heading('8.3 Integration implementation and database isolation',1)
    p('The F2 fixture creates a fresh sqlite:// engine with StaticPool and check_same_thread=False, imports all models, creates metadata and explicitly enables foreign keys. Requests use real authentication, handlers, services, repositories and fresh Sessions. Separate TestClient cookie jars model Student S1, Student S2 and Advisor A1. Startup, recovery engine and dependency overrides are isolated; teardown restores them and disposes the engine. Snapshot comparisons in fresh identity maps verify committed state and unchanged state after denials. IT-19/20 reach real constraints and rollback below service validation.')
    fixture=read('tests/integration/conftest.py')
    start=fixture.index('    def snapshot(self):');end=fixture.index('    def seed_plan(',start)
    markdown('```python\n'+textwrap.dedent(fixture[start:end])+'```',ROOT,False)
    source_note('tests/integration/conftest.py: StudentEnvironment.snapshot (verbatim)')
    p('F07 limits fidelity: the fixture turns foreign keys on, whereas the actual application SQLite engine was reproduced with PRAGMA 0. SQLite test success does not establish PostgreSQL behavior, concurrent submission protection, production settings or UI usability.')
    heading('8.4 Authentication, authorization and boundaries',1)
    p('Tests cover valid and invalid login, malformed/expired/missing tokens, current DB roles, separate identities, foreign-plan concealment, read-back after forbidden writes and Student denial from Advisor operations. JSON APIs have 401/403/404/409/422 contracts and response allowlists. Positive cases cover valid eligible courses and 500-character feedback; negative/boundary cases include empty/duplicate/missing courses, unfinished prerequisites, zero denominators, over-credit caps, wrong semesters, invalid fields, 501-character feedback, non-Pending review, last-course removal and forbidden cancellation states. The suite misses the HTML Advisor submission/self-approval path reproduced in F01.')
    heading('8.5 Postman Collection Runner strategy',1)
    p('The genuine v2.1 JSON collection has 90 sequential requests across readiness/authentication (12), role/progress/catalogue (9), Student lifecycle/validation (29), Advisor decisions/resubmission (26) and cancellation/history/logout (14). Student, Advisor and independent Student identity variables are kept separate; dynamic course and plan IDs support read-back assertions. Run one iteration in original order against the disposable instance. Exported password and token variables are blank. A static validator compiles 93 script blocks and covers all 15 JSON operations; compilation is distinct from the recorded Runner execution.')
    source_note('docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json; postman/validate_collection.cjs')
    heading('8.6 Test-script example from the actual collection',1)
    coll=json.loads(read(HERE/'postman/MyAdvisor-Assignment2.postman_collection.json'))
    def flatten(items):
        for item in items:
            if 'item' in item:yield from flatten(item['item'])
            else:yield item
    reqs=list(flatten(coll['item']));assert len(reqs)==90
    request=next(r for r in reqs if r['name'].startswith('49 '))
    p(request['name'])
    for ev in request.get('event',[]):
        if ev['listen']=='test':
            lines=ev['script']['exec']
            # A concise contiguous verbatim excerpt; the complete real script stays in JSON.
            markdown('```javascript\n'+'\n'.join(lines[:11])+'\n```',HERE/'postman',False)
            p('Verbatim opening excerpt from request 49; the full script remains in the genuine exported collection. No synthetic example or execution result is introduced.','small')

    section('9. Test reporting')
    table([['Recorded run','Actual outcome','Provenance'],['Unit selection','113 passed; 602 deselected; 1 warning','26 Oct; 6.23s; 3 terminal captures'],['Integration selection','194 passed; 521 deselected; 1 warning','26 Oct; 30.52s; 3 terminal captures'],['Full pytest suite','715 passed; no failures/errors; 1 warning','27 Oct independent audit; 76.25s; exit 0; text/XML/hashes'],['Postman Runner','90 requests; 470 assertions passed; 0 assertion failures / execution errors; 1 iteration','27 Oct; 10s 697ms; 6 genuine captures'],['Manual UAT','1 Pass; 0 Fail; 19 Not Run','27 Oct; 18 partial cases + 1 unverified; 19 captures']],widths=[W*.22,W*.40,W*.38])
    p('The full pytest total includes the marked selections: 113 unit + 194 integration + 408 other collected nodes = 715. These overlapping results must not be added across runs. Zero observed automated failures does not negate the independent audit defects or incomplete UAT.')
    for label,report,folder in [('9.1 Unit Testing Results','unit-test-report.md','Unit'),('9.2 Integration Testing Results','integration-test-report.md','Integration')]:
        story.extend([NextPageTemplate('Portrait'),PageBreak()]);heading(label,1)
        report_text=read(HERE/'reports'/report)
        # Retain detailed scope, execution, function mappings, warnings and conclusions.
        report_text=report_text.split('## Cross-method reporting reconciliation')[0]
        markdown(report_text,HERE/'reports')
        for i,path in enumerate(sorted((HERE/'screenshots'/folder).glob('*.png')),1):
            plate(path,f'Figure {label[:3]}.{i}. {folder} terminal evidence',f'Original terminal screenshot: {path.name}. Capture date 26 October 2026. The reported warning and selected/deselected counts are retained.')
    story.extend([NextPageTemplate('Portrait'),PageBreak()]);heading('9.3 Complete Automated Test Suite',1)
    p('Prompt 15 independently executed the existing complete suite on 27 October 2026: **715 passed, 0 failures, 0 errors, 0 skips, 1 warning in 76.25 seconds; exit code 0**. JUnit contains 715 testcase nodes. The recorded source-hash inventory identifies the audited local code; historical screenshots do not acquire this provenance retroactively. All 113 marked unit and 194 marked integration nodes occur within the audit XML.')
    source_note('docs/assignment2/evidence/audit/pytest-output.txt; pytest-results.xml; pytest-run.json')
    output=read(HERE/'evidence/audit/pytest-output.txt')
    # A verbatim text extract is labelled as text, never a fabricated terminal capture.
    p('Verbatim retained terminal text (the audit did not capture a full-suite screenshot):','small')
    output=output.replace(str(ROOT), '[repository root]')
    markdown('```text\n'+output+'\n```',HERE/'evidence/audit',False)
    p('The warning is Starlette’s deprecated httpx TestClient transport. Retained earlier user-reported 715 passes in 56.83s and historical 113-pass/408-deselected and 59-Student-integration logs remain separate executions. No line/branch coverage percentage was measured.')
    story.extend([NextPageTemplate('Portrait'),PageBreak()]);heading('9.4 Postman API Results',1)
    post=read(HERE/'reports/postman-test-report.md')
    markdown(post,HERE/'reports')
    for i,path in enumerate([HERE/'screenshots/postman-results.png']+sorted((HERE/'postman/Postman Screenshots').glob('*.png')),1):
        plate(path,f'Figure 9.4.{i}. Genuine Postman Runner evidence',f'Original {path.name}. Completed 27 October 2026: 470 passing assertions, 0 errors, 1 iteration. Scroll captures collectively cover requests 01–90; partly clipped edge rows are not reconstructed.')
    story.extend([NextPageTemplate('Portrait'),PageBreak()]);heading('9.5 Manual UAT Results',1)
    p('Tester Cameron Ramesar explicitly confirmed execution and all 19 captures on 27 October 2026. The finalized execution sheet is authoritative: **1 Pass / 0 Fail / 19 Not Run**. Not Run means complete-case result remains unverified: 18 cases have observed partial results and UAT-05 lacks its required Pending/relogin workflow evidence. No expected outcome is counted as observed. UAT-06 passes only the recorded review objective with substituted data, not UI usability acceptance.')
    p('Actual initial plan A: MATH 1300 + MATH 2200 + MATH 2250, 3 courses / 9 credits. Revised A: MATH 1300 + MATH 2200 + ENGL 1000, still 3 / 9. The planned A was COMP 1201 + MATH 2250, 2 / 6; revised planned A was COMP 1201 + ENGL 1000. Initial Mathematics choices have no prerequisites and therefore do not establish the intended nonempty-prerequisite positive path. This is a documented data deviation, not an invented failure.')
    p('Prompt 16 visual correction: the filenames of the two cancellation captures are reversed relative to their content. UAT-16-pending-cancelled.png shows semester B Cancelled with rejection feedback and supports case UAT-15. UAT-15-rejected-cancelled.png shows semester C Cancelled and supports case UAT-16. The image bytes/names are unchanged; references are corrected in the current sheet/report/matrix. No chronology or remaining substep is inferred from filenames, and totals are unchanged.')
    summary=[['Case','Recorded status','Evidence disposition']]
    for title,body in sorted(uat_cases):
        case=title[:6];status=re.search(r'\| Pass/Fail/Not Run \| (.*?) \|',body).group(1)
        summary.append([case,status,'Review objective verified with substituted data' if status=='Pass' else ('Required workflow unverified' if case=='UAT-05' else 'Partially verified; required substeps remain')])
    table(summary,widths=[W*.16,W*.17,W*.67])
    source_note('docs/assignment2/reports/uat-execution.md; uat-final-report.md; uat-supplemental-evidence.md')
    read(HERE/'reports/uat-final-report.md');read(HERE/'reports/uat-supplemental-evidence.md');read(HERE/'reports/uat-evidence-review.md')
    for title,body in sorted(uat_cases):
        heading(title,2,False)
        execution=body.split('| Execution field |')[1]
        markdown('| Execution field |'+execution,HERE/'reports',False)
    p('Signed-out/session-expired 401 presentation and login page do not establish logged-in Student /admin 403 or Advisor restricted-tab fallback. Refresh/persistence, queue uniqueness/removal, login attempts, actor-specific logout and feedback-reset substeps remain unverified where listed. Browser/version, actual URL, exact DB and tested build are not supplied. No manual retest or unconditional acceptance is claimed.')
    captions={
      'UAT-01.png':'Student Home: authenticated state only (UAT-18 partial).',
      'UAT-02.png':'Degree Progress: 6 completed, 3 in progress, 84 remaining, 93 required; category total discrepancy visible (UAT-01 partial).',
      'UAT-03.png':'Mathematics search and three eligible selections, 9 credits (UAT-02/03 partial).',
      'UAT-04.png':'Successful three-course submission and Pending plan A (UAT-04 partial).',
      'UAT-05.png':'Advisor review objective: actual three-course/9-credit plan A (UAT-06 Pass; UAT-19 partial). Original table contrast defect remains visible.',
      'UAT-07-request-changes.png':'Advisor-side Changes Requested feedback (UAT-07 partial).',
      'UAT-07-student-feedback.png':'Student sees matching change-request feedback and editable selections (UAT-07 partial).',
      'UAT-08-resubmitted.png':'Revised plan A Pending with ENGL 1000/MATH 1300/MATH 2200, 9 credits (UAT-08 partial).',
      'UAT-09-approved.png':'Approved plan A and revised-selection feedback (UAT-09 partial). Original low-contrast explanatory text retained.',
      'UAT-10-second-plan.png':'Semester B Pending with MATH 2250, 3 credits (UAT-10 partial).',
      'UAT-11-rejected.png':'Messages show semester B rejection reason and retained A approval (UAT-11 partial).',
      'UAT-12-pending-plan.png':'Advisor sees plan C with COMP 1201/MATH 2250, 6 credits (UAT-12 partial).',
      'UAT-13-course-removed.png':'Pending C reduced to COMP 1201, 3 credits; final-course UI guard visible (UAT-13 partial).',
      'UAT-14-approved-cancelled.png':'Approved A cancelled, feedback retained, selection cleared (UAT-14 partial).',
      'UAT-15-rejected-cancelled.png':'Semester C Cancelled and selection cleared (case UAT-16 partial); original filename is misleading.',
      'UAT-16-pending-cancelled.png':'Semester B Cancelled, rejection feedback retained, selection cleared (case UAT-15 partial); original filename is misleading.',
      'UAT-17-new-plan.png':'New C Pending after cancellation, ENGL 1000 only, 3 credits (UAT-17 partial).',
      'UAT-20-access-denied.png':'Session Expired / 401 UI; does not establish logged-in Student 403 (UAT-20 partial).',
      'UAT-20-logged-out.png':'Empty login page after signed-out flow; actor-specific URL checks remain unverified (UAT-20 partial).'}
    for i,path in enumerate(sorted((HERE/'screenshots/UAT').glob('*.png')),1):
        plate(path,f'Figure 9.5.{i}. {path.stem}',captions[path.name]+' Source: '+path.name+'. Captured 27 October 2026; demo identity shown, not submission ID.',portrait=PILImage.open(path).height>1400)
        # Tall browser captures get a focused excerpt at landscape width.
        iw,ih=PILImage.open(path).size
        if ih>1400:
            plate(path,f'Figure 9.5.{i}a. Enlarged original workflow detail','Pixel excerpt only; the preceding full original is preserved. '+captions[path.name],(240,200,1920,min(ih,1250)))

    section('10. Requirements traceability')
    trace=read(HERE/'reports/requirements-test-traceability.md')
    markdown(trace,HERE/'reports')
    heading('10.1 Requirement-level matrix R01–R14',1)
    markdown(extract_section(ut,'Requirements-to-test traceability'),HERE/'test-plans',False)
    heading('10.2 R15 public JSON contracts',1)
    p('R15 is the later public-schema/allowlist/OpenAPI requirement. API-07/08 mappings are retained in evidence/workflow1-api.md; Postman response-contract checks include requests 18–20, 32 and 52. It has no direct manual browser schema case and does not create additional UT/IT/UAT results.')
    read(HERE/'evidence/workflow1-api.md')

    section('11. Defects, limitations and audit disposition')
    p('No Critical finding was verified. F01–F05 remain High and open. The following register reproduces the audit findings and proposed fixes; proposed fixes are not implemented or retested in this PDF task. Functional defects are independent of the 715 passing automated tests.')
    register=extract_section(audit,'Findings register')
    register=re.sub(r'^\| F11 \|.*$', '| F11 | Medium | Final deliverables | Original PDF cover; retained student transcript; current A2 PDF | Prompt 15 lacked a compiled A2 PDF and verified identity; Prompt 16 recovered the real identity and assembled this document. | Complete final document checks; retain open High findings and incomplete UAT. | **Partly addressed — identity and local assembly verified; readiness blocked by F01–F05** |',register,flags=re.M)
    markdown(register,HERE,False)
    heading('11.1 Submission identity and PDF assembly update',1)
    p('F11 is partly addressed: this PDF compiles the A2 materials and the genuine Assignment 1 report-export transcript explicitly supplies the real student name and ID used on the cover; original PDF cover corroboration is recorded in validation. The audit’s earlier request to supply an unknown real ID is therefore superseded by recovered evidence. This update does not close the open authorization, UAT, requirements or publication issues.')
    heading('11.2 Environment problems, corrections and retests',1)
    p('The Windows pytest temporary-directory/cache issue is an execution-environment problem. Marked screenshots demonstrate successful --basetemp runs; the audit’s fresh safe-basetemp, cache-disabled full run independently passed with exit 0. Historical HTML 401 handler behavior was corrected before the audit; retained integration evidence verifies current 401 status. Documentation errors F12 were corrected locally and are still stale on the published commit. None is misrepresented as a newly fixed application defect.')
    p('By contrast, F01 authorization bypass, F07 default-engine foreign keys, F08 malformed registration email and F06 contrast are reproduced application defects. No functional fix or successful retest for them is recorded. F05/DATA-01 is an unresolved requirement: degree total 93 versus categories 36+18+18+24+24=120, with each course stored under one category and no supported overlap/allocation rule. An authoritative curriculum/project decision is required before changing values.')
    heading('11.3 Audit reproduction records (not new UAT failures)',1)
    for name in ['authorization-reproduction.json','sqlite-integrity-reproduction.json','registration-reproduction.json']:
        heading(name,2,False)
        record=json.loads(read(HERE/'evidence/audit'/name))
        table([['Recorded field','Actual audit observation']]+[[k,str(v)] for k,v in record.items()])
    p('All 19 UAT screenshots preserve observed states. Incomplete checks remain Not Run, no missing evidence is silently replaced, and original low-contrast pixels remain visible. Wider accessibility, mobile behavior, PostgreSQL, concurrency and live deployment are unverified. Original screenshot build/environment attribution remains incomplete (F10). Exported passwords/tokens are blank; credentials and session data are excluded from submission prose.')
    heading('11.4 Official rubric status at assembly',1)
    rubric=extract_section(audit,'Official rubric compliance')
    rubric=re.sub(r'^\| D1 \|.*$', '| D1 | Submit 1 PDF document containing the listed deliverables | Final deliverable; no separate weight specified | Compiled locally; acceptance blocked | Prompt 16 produced the requested single A2 PDF with original artifacts, detailed plans, implementation, results and disclosed limitations. Completed UAT and material audit issues remain unresolved. |',rubric,flags=re.M)
    markdown(rubric,HERE,False)
    p('Assembly update to the historical table: D1 now has a single PDF at the requested path; content/readability checks are recorded in final-submission-checklist.md. Completed UAT, published collection/evidence and authorization remain partial. No numerical grade is inferred. F11 identity/assembly is partly addressed, not a blanket readiness sign-off.')

    section('12. Conclusion')
    p('MyAdvisor implements the original Student progress/planning and Advisor review workflows and adds substantial automated/API verification. Retained marked evidence shows 113 unit and 194 integration passes; the independently retained complete run shows 715 passes with one warning. The actual Postman iteration executed 90 requests and passed 470 assertions with no assertion failures or execution errors.')
    p('Manual evidence demonstrates submission, change requests, revision, approval, rejection, removal, cancellation and replacement states, but complete-case UAT remains 1 Pass, 0 Fail and 19 Not Run. The three-course Mathematics deviation and every documented incomplete check are preserved. Open High audit findings and missing published materials prevent submission-ready or full-acceptance claims. This PDF makes the work reviewable and does not resolve those issues.')
    section('13. References and GitHub repository')
    p('Submission repository: [Camcoon/MyAdvisorWithTests](https://github.com/Camcoon/MyAdvisorWithTests). Public main was rechecked read-only at commit 864386fe10fa5e61869e07500d84e51ff7e46b9b. Local source root is the nested Assignment 2 directory; its origin still points to Camcoon/MyAdvisor, and its working tree includes pre-existing modifications/untracked work. No commit, push, remote change or deployment was performed.')
    refs=[
      ('Assignment 2 brief and four-component marking rubric','docs/assignment2/official-assignment-brief.md','Student-supplied official text retained 27 October 2026; no claim of an independent university download.'),
      ('Original Assignment 1 report and artifacts','docs/report.md; docs/report.pdf; docs/diagrams/use-case.png; docs/wireframes/Three-Panel Student Advisor Dashboard Mockup.png','Original diagram/wireframe preserved; original Mermaid ERD rendered without model changes.'),
      ('Verified submission identity','docs/transcripts/current-report-export.md (11 October 2026), explicit Student statement; docs/report.pdf cover','Real ID used only from this evidence, never from seeded application data.'),
      ('Detailed test plans','docs/assignment2/test-plans/uat-test-plan.md; unit-test-plan.md; integration-test-plan.md','Original inputs/oracles and UT/IT identifiers preserved.'),
      ('Automated and API reports','docs/assignment2/reports/unit-test-report.md; integration-test-report.md; postman-test-report.md','Dated retained runs and evidence qualifications.'),
      ('Final UAT records','docs/assignment2/reports/uat-execution.md; uat-final-report.md; uat-evidence-review.md; uat-supplemental-evidence.md','Authoritative 1/0/19 totals, actual observations and remaining conditions.'),
      ('Evidence inventory and traceability','docs/assignment2/reports/evidence-inventory.md; requirements-test-traceability.md','Screenshot paths/case mapping and WF1–WF3 / R-level coverage.'),
      ('Prompt 15 audit and retained outputs','docs/assignment2/final-quality-audit.md; evidence/audit/pytest-output.txt; pytest-results.xml; pytest-run.json; three reproduction JSONs','Open defects, current full-suite execution and source hashes.'),
      ('Collection and API contracts','docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json; postman/README.md; postman/validate_collection.cjs; api.md','90 actual request definitions; v2.1 JSON; runtime and static results kept distinct.'),
      ('Actual implementation','app/models, app/routers, app/services, app/repositories, app/dependencies; tests/unit and tests/integration','Concise examples reproduced from real files; no application or test source edits.'),
    ]
    table([['Reference','Source and use']]+[[a,b+' — '+c] for a,b,c in refs])
    p('Course-linked templates (access attempted again 27 October 2026; contents inaccessible, not used as verified substantive sources):')
    p('[Test Plans template](https://docs.google.com/document/d/1YQPB1vPS0SFb6tIUAxmxrSUIsj-d6u98USWzvMi4mJs/edit) and [User Acceptance Tests Plan template](https://docs.google.com/document/d/1LIPdWA39zJCuzTgSkwTKjnaqi8Yn9STFZckn4MBsf48/edit). Check any additional course-specific template instructions personally before submission.')
    heading('13.1 Evidence and submission availability',1)
    p('All original execution PNGs are embedded above: 3 Unit, 3 Integration, 6 Postman and 19 UAT. The full-suite raw text is embedded as labelled text; no full-suite screenshot exists. Local linked evidence is checked during assembly; references describe repository-relative source files, not attachments required to read the PDF. Required JSON/current evidence are absent or stale on the rechecked public commit. The final checklist records what remains to publish after correction and review.')
    p('Required final artifact: `docs/assignment2/COMP3613_Assignment2_MyAdvisor.pdf`. Checklist: `docs/assignment2/final-submission-checklist.md`. Validation artifacts and source/image manifest: `docs/assignment2/pdf-review/`.')

    bad=[(b,u) for b,u,ok in references if not ok]
    assert not bad, 'Missing referenced files: '+str(bad)
    doc=SubmissionDoc(str(OUT),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=48,bottomMargin=39,
        title='COMP 3613 Assignment 2 — MyAdvisor',author='Cameron Ramesar',subject='Evidence-based academic submission; acceptance incomplete')
    for name,size in [('Portrait',A4),('Landscape',landscape(A4))]:
        w,h=size
        doc.addPageTemplates(PageTemplate(id=name,pagesize=size,frames=[Frame(M,39,w-2*M,h-87,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id=name)],onPage=footer))
    doc.multiBuild(story)
    manifest={'pdf':str(OUT.relative_to(ROOT)).replace('\\','/'),'date':'2026-10-27','uat':{'Pass':1,'Fail':0,'Not Run':19,'partially_verified':18},
      'automated':{'unit_passed':113,'unit_deselected':602,'integration_passed':194,'integration_deselected':521,'full_passed':715,'warnings_per_run':1},
      'postman':{'requests':90,'passed_assertions':470,'assertion_failures':0,'execution_errors':0,'iterations':1},
      'checked_local_references':len(references),'missing_references':bad,'images':images,
      'source_files':[{'path':str(s.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(s.read_bytes()).hexdigest()} for s in sorted(sources)],
      'readiness':'NOT SUBMISSION-READY; F01–F05 remain High and open'}
    (REVIEW/'assembly-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'pdf':str(OUT),'bytes':OUT.stat().st_size,'images':len(images),'checked_references':len(references)},indent=2))

if __name__=='__main__':build()
