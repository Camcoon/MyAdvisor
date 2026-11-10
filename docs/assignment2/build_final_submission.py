"""Build the final, lecturer-ordered MyAdvisor Assignment 2 submission PDF.

Documentation only. Existing evidence is reused; no application code, tests,
UAT, Postman runs or remote state are changed.
"""
from pathlib import Path
import sys, re, json, hashlib, html, ast, io, os
from datetime import date
from urllib.parse import unquote

H = Path(__file__).resolve().parent
R = H.parents[1]
sys.path.insert(0, str(H / '.pdf-tools'))
import build_submission as b
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, NextPageTemplate, Table, TableStyle, Image, Flowable,
    KeepTogether, HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from PIL import Image as PILImage
import pymupdf as fitz

OUT = H / 'COMP3613_Assignment2_SUBMISSION_corrected.pdf'
TMP = H / '.submission_build_tmp.pdf'
REPO = 'https://github.com/Camcoon/MyAdvisorWithTests'
COLL = 'docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json'
PREPARED = '4 November 2026'
COMMIT = '847e39a9cc6340e51bcc05c9864f75f8457021c1'
UAT_DIR = H / 'screenshots/UAT'
TOTAL_PAGES = None
S = []
bookmarks = []
figures = []
TOC_ENTRIES = []
PAGE_MAP = {}
HEAD = 'MyAdvisor  |  COMP 3613 Assignment 2'
FOOT = 'Cameron Ramesar  |  816044668'

# ---- typography -----------------------------------------------------------
for key, size, leading in [('body', 9.7, 13.6), ('small', 8.2, 11.2),
                           ('cell', 8.7, 11.8), ('th', 8.7, 11.8),
                           ('code', 8.0, 10.6), ('caption', 8.2, 11.6)]:
    b.styles[key].fontSize = size
    b.styles[key].leading = leading
b.styles['h1'].fontSize = 20
b.styles['h1'].leading = 25
b.styles['h2'].fontSize = 13
b.styles['h2'].leading = 17
b.styles['h3'].fontSize = 10.6
b.styles['h3'].leading = 14
b.styles['h1'].spaceAfter = 8
b.styles['h2'].spaceBefore = 9
b.styles['h2'].spaceAfter = 6

EXTRA = {
    'kicker': ParagraphStyle('kicker', parent=b.styles['small'], fontName='Body-Bold',
                             fontSize=8.4, leading=11, textColor=b.TEAL),
    'cover_uni': ParagraphStyle('cover_uni', parent=b.styles['body'], fontName='Body-Bold',
                                fontSize=10.5, leading=14, textColor=b.NAVY),
    'cover_course': ParagraphStyle('cover_course', parent=b.styles['body'], fontName='Body-Bold',
                                   fontSize=12.5, leading=16, textColor=b.TEAL),
    'cover_title': ParagraphStyle('cover_title', parent=b.styles['h1'], fontSize=40,
                                  leading=46, spaceBefore=4, spaceAfter=2),
    'cover_sub': ParagraphStyle('cover_sub', parent=b.styles['body'], fontSize=12,
                                leading=16, textColor=b.GRAY),
    'caption_center': ParagraphStyle('caption_center', parent=b.styles['caption'],
                                     alignment=1, spaceBefore=2),
    'toc0': ParagraphStyle('toc0', fontName='Body-Bold', fontSize=9.6, leading=17,
                           spaceBefore=3, textColor=b.NAVY),
    'toc1': ParagraphStyle('toc1', fontName='Body', fontSize=8.8, leading=14,
                           leftIndent=16, textColor=b.GRAY),
    'stat': ParagraphStyle('stat', parent=b.styles['cell'], fontName='Body-Bold',
                           fontSize=8.8, leading=11.4, textColor=b.NAVY),
}
b.styles.update({k: v for k, v in EXTRA.items() if k not in b.styles})

def p(text, style='body'):
    S.append(b.para(text, style))

def h(text, level=0, toc=True):
    obj = b.para(text, ['h1', 'h2', 'h3'][min(level, 2)])
    if toc:
        obj.toclevel = min(level, 1)
        obj.bookmark = 'section-' + str(len(bookmarks))
        bookmarks.append(text)
        TOC_ENTRIES.append((obj.toclevel, text, obj.bookmark))
        S.append(obj)
        if level == 0:
            S.append(HRFlowable(width='100%', thickness=1.1, color=b.TEAL,
                                spaceBefore=0, spaceAfter=9))
    else:
        S.append(obj)

def new_page(title=None, level=0, kind='Portrait', toc=True):
    S.extend([NextPageTemplate(kind), PageBreak()])
    if title:
        h(title, level, toc)

def table(rows, widths=None, header=True, font_size=None, pad=4, repeat=1):
    rows = [[str(v) for v in row] for row in rows]
    cell = b.styles['cell']
    if font_size:
        cell = ParagraphStyle('cellx', parent=cell, fontSize=font_size,
                              leading=font_size * 1.34)
    th = ParagraphStyle('thx', parent=b.styles['th'],
                        fontSize=(font_size or b.styles['th'].fontSize),
                        leading=(font_size or b.styles['th'].fontSize) * 1.34)
    data = [[Paragraph(b.inline(v), th if header and i == 0 else cell)
             for v in row] for i, row in enumerate(rows)]
    widths = widths or ([b.W * .25, b.W * .75] if len(rows[0]) == 2
                        else [b.W / len(rows[0])] * len(rows[0]))
    t = Table(data, colWidths=widths, repeatRows=repeat if header else 0,
              hAlign='LEFT', splitByRow=1, splitInRow=0)
    cmds = [('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), pad),
            ('BOTTOMPADDING', (0, 0), (-1, -1), pad),
            ('LINEBELOW', (0, 0), (-1, -1), .3, colors.HexColor('#cbd8df'))]
    if header:
        cmds += [('BACKGROUND', (0, 0), (-1, 0), b.NAVY),
                 ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, b.LIGHT])]
    else:
        cmds += [('BACKGROUND', (0, 0), (0, -1), b.LIGHT)]
    t.setStyle(TableStyle(cmds))
    S.extend([t, Spacer(1, 7)])

def code_block(text):
    lines = text.rstrip().splitlines()
    for line in lines:
        assert len(line) < 116, ('oversize code line', line)
    S.append(Paragraph('<br/>'.join(html.escape(x).replace(' ', '&#160;')
                                    for x in lines), b.styles['code']))
    S.append(Spacer(1, 5))

def fields(spec):
    result = {}
    for line in spec.splitlines():
        if line.startswith('| ') and not line.startswith('|---'):
            k, _, v = line.strip().strip('|').strip().partition(' | ')
            result[k.strip()] = v.strip()
    return result

def figure(path, number, caption, kind='Portrait', maxh=None, crop=None, newpage=True):
    if newpage:
        S.extend([NextPageTemplate(kind), PageBreak()])
    elif kind != 'Portrait':
        raise ValueError('only portrait figures can flow inline')
    path = Path(path)
    img = PILImage.open(path)
    if crop:
        img = img.crop(crop)
    iw, ih = img.size
    width = b.W if kind == 'Portrait' else landscape(A4)[0] - 2 * b.M
    height = maxh or ((A4[1] - 210) if kind == 'Portrait'
                      else (landscape(A4)[1] - 160))
    scale = min(width / iw, height / ih)
    stream = io.BytesIO()
    img.convert('RGB').save(stream, format='PNG')
    stream.seek(0)
    S.append(Image(stream, width=iw * scale, height=ih * scale, hAlign='CENTER'))
    S.append(Spacer(1, 7))
    p('**Figure ' + number + '.** ' + caption, 'caption')
    figures.append({'number': number, 'path': str(path.relative_to(R)).replace('\\', '/'),
                    'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'original_pixels': [iw, ih],
                    'display_points': [round(iw * scale, 1), round(ih * scale, 1)]})

def snippet(path, func, start=0, end=None):
    text = (R / path).read_text(encoding='utf-8-sig')
    node = next(n for n in ast.walk(ast.parse(text))
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == func)
    lines = text.splitlines()[node.lineno - 1:node.end_lineno]
    return '\n'.join(lines[start:end])

class KeyedERD(Flowable):
    """Readable vector view of the original Mermaid ERD, with PK labels."""
    def __init__(self, src):
        super().__init__()
        self.width = landscape(A4)[0] - 2 * b.M
        self.height = 420
        self.src = src

    def draw(self):
        c = self.canv
        boxes = {'DEGREE_PROGRAM': (0, 300, 180), 'DEGREE_REQUIREMENT': (0, 100, 180),
                 'USER': (265, 264, 194), 'COURSE': (265, 20, 194),
                 'SEMESTER_PLAN': (550, 270, 205), 'PLAN_COURSE': (550, 160, 205),
                 'STUDENT_COURSE': (550, 0, 205)}
        data = {n: fs.strip().splitlines()
                for n, fs in re.findall(r'  (\w+) \{(.*?)\n  \}', self.src, re.S)}
        routes = [([(180, 339), (265, 339)], 'enrolls 0..1 : 0..*', (183, 348)),
                  ([(90, 300), (90, 185)], 'defines 1 : 0..*', (96, 238)),
                  ([(459, 397), (550, 397)], 'creates 1 : 0..*', (463, 405)),
                  ([(459, 361), (550, 361)], 'reviews 0..1 : 0..*', (461, 349)),
                  ([(459, 285), (500, 285), (500, 85), (550, 85)], 'completes 1 : 0..*', (463, 265)),
                  ([(459, 100), (550, 100)], 'appears 1 : 0..*', (463, 110)),
                  ([(459, 151), (480, 151), (480, 195), (550, 195)], 'appears 1 : 0..*', (482, 204)),
                  ([(653, 270), (653, 230)], 'contains 1 : 0..*', (659, 254))]
        for pts, label, pos in routes:
            c.setStrokeColor(b.GRAY)
            c.setLineWidth(.8)
            q = c.beginPath()
            q.moveTo(*pts[0])
            for pt in pts[1:]:
                q.lineTo(*pt)
            c.drawPath(q)
            c.setFont('Body', 7.4)
            c.setFillColor(b.TEAL)
            c.drawString(*pos, label)
        for name, (x, y, w) in boxes.items():
            fs = data[name]
            height = 25 + len(fs) * 15
            c.setFillColor(colors.white)
            c.setStrokeColor(b.TEAL)
            c.roundRect(x, y, w, height, 3, fill=1, stroke=1)
            c.setFillColor(b.NAVY)
            c.rect(x, y + height - 23, w, 23, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont('Body-Bold', 9)
            c.drawString(x + 7, y + height - 15, name)
            c.setFillColor(b.NAVY)
            c.setFont('Body', 9)
            for i, f in enumerate(fs):
                f = re.sub(r'".*?"', '', f).strip()
                if f == 'int id':
                    f += ' PK'
                c.drawString(x + 7, y + height - 37 - i * 15, f)

class TOC(Flowable):
    """Static contents page with right-aligned page numbers and dot leaders.

    reportlab's TableOfContents paints the page number at the paragraph start
    with this runtime, so the title is overpainted; this flowable draws the
    leader explicitly and keeps the entry geometry stable across passes.
    """

    def __init__(self, entries, pages):
        super().__init__()
        self.entries = list(entries)
        self.pages = dict(pages)
        self.width = b.W
        self.height = 6 + sum(17.5 if lvl == 0 else 14.2 for lvl, _, _ in self.entries)

    def draw(self):
        c = self.canv
        y = self.height - 4
        for level, text, key in self.entries:
            top = level == 0
            lead = 17.5 if top else 14.2
            y -= lead
            font = 'Body-Bold' if top else 'Body'
            size = 9.9 if top else 8.9
            x = 0 if top else 18
            page = str(self.pages.get(key, ''))
            c.setFont(font, size)
            c.setFillColor(b.NAVY if top else b.GRAY)
            c.drawString(x, y + 3, text)
            tw = c.stringWidth(text, font, size)
            pw = c.stringWidth(page, font, size)
            start = x + tw + 5
            stop = self.width - pw - 5
            if stop > start:
                dot = c.stringWidth(' .', font, size)
                n = int((stop - start) / dot)
                if n > 0:
                    c.setFillColor(colors.HexColor('#a9bcc7'))
                    c.setFont('Body', size)
                    c.drawString(start, y + 3, ' .' * n)
            c.setFont(font, size)
            c.setFillColor(b.NAVY if top else b.GRAY)
            c.drawRightString(self.width, y + 3, page)
            if key:
                c.linkRect('', key, (x, y, self.width, y + lead), relative=1,
                           thickness=0)


class Doc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark'):
            self.canv.bookmarkPage(flowable.bookmark)
            self.canv.addOutlineEntry(flowable.getPlainText(), flowable.bookmark,
                                      flowable.toclevel, False)
            PAGE_MAP[flowable.bookmark] = self.page

def cover_bg(c, d):
    w, h = c._pagesize
    c.setFillColor(b.NAVY)
    c.rect(0, h - 78, w, 78, fill=1, stroke=0)
    c.setFillColor(b.TEAL)
    c.rect(0, h - 82, w, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Body-Bold', 9.5)
    c.drawString(b.M, h - 31, 'THE UNIVERSITY OF THE WEST INDIES')
    c.setFont('Body', 9)
    c.drawString(b.M, h - 50, 'COMP 3613  ·  ASSIGNMENT 2')
    c.setFont('Body', 8)
    c.drawRightString(w - b.M, h - 50, 'FINAL SUBMISSION DOCUMENT')

def footer(c, d):
    w, h = c._pagesize
    if d.page > 1:
        c.setFillColor(b.GRAY)
        c.setFont('Body', 7.6)
        c.drawString(b.M, h - 27, HEAD)
        c.drawRightString(w - b.M, h - 27, FOOT)
        c.setStrokeColor(colors.HexColor('#ccd9df'))
        c.line(b.M, h - 33, w - b.M, h - 33)
        c.line(b.M, 34, w - b.M, 34)
        c.drawString(b.M, 22, 'Final submission document  ·  ' + PREPARED)
        page = 'Page ' + str(d.page)
        if TOTAL_PAGES:
            page += ' of ' + str(TOTAL_PAGES)
        c.drawRightString(w - b.M, 22, page)

def cover_story():
    kicker = b.para('1. Name & ID', 'kicker')
    kicker.toclevel = 0
    kicker.bookmark = 'section-cover'
    bookmarks.append('1. Name & ID')
    TOC_ENTRIES.append((0, '1. Name & ID', 'section-cover'))
    S.append(kicker)
    S.append(Spacer(1, 4))
    p('The University of the West Indies', 'cover_uni')
    p('COMP 3613  ·  Assignment 2', 'cover_course')
    S.append(Spacer(1, 18))
    p('MyAdvisor', 'cover_title')
    p('Student–Advisor degree planning and course approval system', 'cover_sub')
    S.append(Spacer(1, 24))
    table([
        ['Student name', 'Cameron Ramesar'],
        ['University ID', '816044668'],
        ['Project', 'MyAdvisor'],
        ['Repository', '[' + REPO + '](' + REPO + ')'],
        ['Document prepared', PREPARED],
    ], widths=[b.W * .27, b.W * .73], header=False)
    S.append(Spacer(1, 6))
    p('**Approved fictional coursework configuration — 93 credits**', 'h3')
    table([
        ['Requirement category', 'Credits'],
        ['Core Courses', '36'],
        ['General Education', '18'],
        ['Electives', '12'],
        ['Major Requirements', '18'],
        ['Additional Requirements', '9'],
        ['**Total**', '**93**'],
    ], widths=[b.W * .62, b.W * .38])
    p('The 93-credit configuration is approved fictional coursework demonstration data. It is not official UWI curriculum data.', 'small')
    p('This document presents the Assignment 2 project description, use case diagram, entity relationship diagram, application wireframe, test plans, implementation evidence, test reports and UAT summary.', 'small')

def toc_story(pages):
    new_page('Contents', toc=False)
    p('Page numbers refer to the printed pages of this document. The eight lecturer-required sections are followed by the UAT execution summary and two appendices.', 'small')
    S.append(Spacer(1, 8))
    S.append(TOC(TOC_ENTRIES, pages))

def project_description():
    new_page('2. Project Description')
    p('MyAdvisor is a web-based academic planning prototype built for the COMP 3613 Assignment 2 coursework. It helps a Student understand degree progress, choose an eligible semester plan, and receive an Advisor decision in one connected workflow. The system addresses the difficulty of reconciling completed courses, in-progress courses and proposed selections across separate records, and of communicating plan decisions without a shared review queue.')
    p('The Student role (`regular_user`) owns degree progress and semester plans. The Advisor role (`admin`) reviews the shared Pending queue and records a decision. Student identity comes from the authenticated account, not from a submitted identifier; Advisor decisions update the plan status, reviewer and feedback.')
    table([
        ['Workflow', 'Purpose and implemented behaviour'],
        ['WF1 — Track Degree Progress (Student)',
         'View overall progress; completed, in-progress and remaining credits; requirement categories; recent academic activity.'],
        ['WF2 — Plan Semester Course Selections (Student)',
         'Search and filter the catalogue; inspect eligibility; select courses; review and submit a plan; read feedback; revise, remove permitted courses and cancel or replace plans.'],
        ['WF3 — Review and Approve Course Plans (Advisor)',
         'Inspect the Pending queue, Student and course details; approve, reject or request changes with optional feedback.'],
    ], widths=[b.W * .31, b.W * .69])
    p('Semesters use the nine fixed Year 1–3 / semester 1–3 options, with semester 3 designated summer. Only Pending plans appear in Advisor Review. Pending and Approved plans lock standard selection; Rejected and Changes Requested plans are editable. Cancellation is allowed for Pending, Rejected and Approved plans and is absent for Changes Requested and Cancelled plans.')
    h('2.1 Technologies and architecture', 1, False)
    table([
        ['Technology', 'Role in the implementation'],
        ['Python 3.14, FastAPI, Pydantic', 'HTTP application, request validation and JSON API contracts.'],
        ['SQLModel, SQLAlchemy, SQLite', 'Models, repository persistence and isolated local test databases.'],
        ['Jinja2, Bootstrap/AdminLTE, JavaScript', 'Server-rendered Student and Advisor pages; selection, review and confirmation interactions.'],
        ['pwdlib, PyJWT, signed cookies', 'Password verification, signed login token, current-role and ownership checks.'],
        ['pytest, TestClient, Postman', 'Isolated unit decisions, integrated HTTP/database checks and the automated API collection.'],
    ], widths=[b.W * .34, b.W * .66])
    p('The application uses a layered structure: routers handle HTTP and template/JSON responses, services hold business rules, repositories own persistence, and SQLModel models define the data contract. Templates render the Student and Advisor workspaces. JSON endpoints expose the same service layer used by the browser workflows.')
    p('**Assignment 2 scope.** The assignment extends the Assignment 1 workflows with explicit JSON API contracts, unit and integration test plans and pytest implementations, a 90-request Postman collection, manual UAT specifications and execution records, screenshots, reports and requirements traceability.')
    h('2.2 Approved credit configuration', 1, False)
    table([
        ['Requirement category', 'Approved credits'],
        ['Core Courses', '36'],
        ['General Education', '18'],
        ['Electives', '12'],
        ['Major Requirements', '18'],
        ['Additional Requirements', '9'],
        ['**Total**', '**93**'],
    ], widths=[b.W * .58, b.W * .42])
    p('This 36/18/12/18/9 allocation is fictional coursework demonstration data approved for the project. It is not an official UWI curriculum or a claim about any real programme.')
    h('2.3 Scope, assumptions and boundaries', 1, False)
    table([
        ['Aspect', 'Project decision'],
        ['Data', 'All accounts, courses, programmes, grades and credit values are fictional demonstration data. They do not describe a real UWI programme or student record.'],
        ['Runtime', 'The application runs locally against SQLite. No production deployment, hosting or live user data is part of this submission.'],
        ['Authentication', 'Login uses the starter session cookie with a signed token; role checks read the current database role at request time.'],
        ['Planning rules', 'Nine fixed Year 1–3 semester options; one active Pending or Approved plan per semester; Rejected and Changes Requested plans are revised and resubmitted under the same plan ID.'],
        ['Out of scope', 'Official curriculum validation, production security hardening, mobile layout review, concurrent multi-user operation and PostgreSQL behaviour. Appendix A records these limits.'],
    ], widths=[b.W * .17, b.W * .83])

def use_case():
    new_page('3. Use Case Diagram')
    p('The original Assignment 1 use case diagram defines the project actors and use cases. It is reproduced without redrawing. The Student tracks degree progress, plans semester course selections, views the catalogue and cancels semester plans. The Advisor reviews course plans and can request changes. Catalogue viewing is included in the planning and review workflows; Request Changes extends review. Authentication supports these workflows and is tested separately.')
    figure(R / 'docs/diagrams/use-case.png', '3.1',
           'Original Assignment 1 MyAdvisor use case diagram, reproduced from `docs/diagrams/use-case.png` without redrawing.',
           'Portrait', maxh=440, newpage=False)
    p('**Actors.** Student (`regular_user`) and Advisor (`admin`). **Included use cases.** View Course Catalogue is included by Plan Semester Course Selections and Review Course Plans because both workflows need course details. **Extending use case.** Request Changes extends Review Course Plans when the Advisor needs more information before a decision. Registration and login are supporting authentication paths, not part of WF1–WF3.')

def erd(erd_src):
    new_page('4. Entity Relationship Diagram')
    p('The original seven-entity ERD defines DegreeProgram, DegreeRequirement, User, Course, SemesterPlan, PlanCourse and StudentCourse. A programme defines requirements and optionally enrols users; a Student creates plans and has course records; an optional Advisor reviews each plan. PlanCourse joins plans to courses, and StudentCourse joins users to academic course records.')
    table([
        ['Relationship (original Mermaid)', 'Reads as'],
        ['`DEGREE_PROGRAM o|--o{ USER : enrolls`', 'A user has zero or one programme; a programme can enrol many users.'],
        ['`DEGREE_PROGRAM ||--o{ DEGREE_REQUIREMENT : defines`', 'Each requirement belongs to exactly one programme.'],
        ['`USER ||--o{ SEMESTER_PLAN : creates`', 'Each plan has exactly one Student creator.'],
        ['`USER o|--o{ SEMESTER_PLAN : reviews`', 'A plan has zero or one reviewing Advisor; an Advisor can review many plans.'],
        ['`USER ||--o{ STUDENT_COURSE : completes`', 'An academic record joins one Student to one course with status, grade and date.'],
        ['`COURSE ||--o{ STUDENT_COURSE : appears_in`', 'Each academic record refers to exactly one course.'],
        ['`COURSE ||--o{ PLAN_COURSE : appears_in`', 'Each selected-plan row refers to exactly one course.'],
        ['`SEMESTER_PLAN ||--o{ PLAN_COURSE : contains`', 'PlanCourse implements the plan-to-course association.'],
    ], widths=[b.W * .47, b.W * .53], font_size=8.3)
    p('All seven `id` fields are primary keys. Unique pairs constrain programme/category, student/course and plan/course. Foreign-key fields retain their original names. The password field names stored data; no password value is reproduced.')
    figure(H / 'final-review/original-erd.png', '4.1',
           'Original MyAdvisor ERD image extracted losslessly from the Assignment 1 report (`docs/report.pdf`, page 3). The readable keyed rendering follows in Figure 4.2.',
           'Portrait', maxh=600)
    p('All seven `id` fields are primary keys. Unique pairs constrain programme/category, student/course and plan/course. Foreign-key fields retain their original names. The password field names stored data; no password value is reproduced.')
    new_page('4.1 Readable entity keys and relationships', 1, 'Landscape')
    S.append(KeyedERD(erd_src))
    S.append(Spacer(1, 2))
    p('**Figure 4.2.** Enlarged vector rendering of the same original seven-entity Mermaid ERD. All original fields and relationships are retained; PK labels are added from `app/models/user.py` and `app/models/advising.py`. Numeric edge labels state source:target cardinality; “appears” abbreviates “appears_in”.', 'caption')
    figures.append({'number': '4.2', 'source': 'docs/report.md Mermaid + app/models', 'vector': True})

def wireframe():
    new_page('5. Application Wireframe')
    p('The original Assignment 1 three-panel wireframe is reproduced unmodified. W1 is the Student Degree Progress view, W2 is Student Semester Planning, and W3 is Advisor Plan Review. Sample credits, dates, course labels and the eight-digit Student ID in the mockup are illustrative, not execution results.')
    table([
        ['Wireframe region', 'Implemented surface', 'Related evidence'],
        ['W1 — Degree Progress', 'Student Degree Progress: overall progress, credit cards, requirement breakdown and recent activity.', 'UAT-01, UAT-18'],
        ['W2 — Semester Planning', 'Plan Courses: catalogue search and filters, eligibility, selection count, Review Selected Courses and Submit Plan.', 'UAT-02–05, UAT-08–17'],
        ['W3 — Advisor Review', 'Advisor workspace: shared Pending queue, Student and credit details, Approve, Reject and Request Changes.', 'UAT-06–11'],
        ['W4 — Messages (extension)', 'Student and Advisor Messages showing decisions and feedback; not a separate wireframe panel.', 'UAT-07, UAT-08, UAT-11'],
        ['W5 — Cancellation (extension)', 'Cancellation, replacement and resubmission controls added to W2/W3 during the build.', 'UAT-14–17'],
    ], widths=[b.W * .24, b.W * .56, b.W * .20], font_size=8.3)
    p('**Reading the wireframe against the implementation.** The mockup fixed the information architecture rather than a pixel-perfect layout. The implemented Student pages add session-aware navigation, an explicit selection counter, a review-and-submit step and status-aware actions. The Advisor page adds the shared Pending queue and the decision form used by WF3. Where the mockup shows illustrative 120-credit totals and calendar-year labels, the implemented screens show the approved 93-credit configuration and the nine fixed Year 1–3 semester labels.')
    figure(R / 'docs/wireframes/Three-Panel Student Advisor Dashboard Mockup.png', '5.1',
           'Original three-panel Assignment 1 wireframe, unmodified. W1: Student Degree Progress; W2: Student Semester Planning; W3: Advisor Plan Review.',
           'Landscape', maxh=430)
    wf = R / 'docs/wireframes/Three-Panel Student Advisor Dashboard Mockup.png'
    for n, (a, z, label) in enumerate([
            (0, 510, 'W1 — Student Degree Progress'),
            (516, 1020, 'W2 — Student Semester Planning'),
            (1032, 1536, 'W3 — Advisor Plan Review')], 2):
        figure(wf, '5.' + str(n), 'Wireframe detail: ' + label +
               '. Enlarged crop of the original panel. W1 maps to UAT-01; W2 to UAT-02–05 and UAT-08–17; W3 to UAT-06–11. Login, cancellation and resubmission extensions are documented in Section 6.1.',
               'Portrait', maxh=655, crop=(a, 0, z, 930))
    p('W4 denotes Student Messages and feedback; W5 denotes the cancellation and resubmission extensions to W2/W3. Neither is an additional original wireframe panel.', 'small')

def uat_plan(uc):
    new_page('6. Test Plans')
    h('6.1 User Acceptance Test Plan', 1)
    p('**Objective and scope.** Verify that Students can understand degree progress and complete eligible semester planning, and that Advisors can review and return decisions. The tables below record the planned browser tasks and expected outcomes. Observed results and statuses are reported separately in Section 9; automated executions are reported in Section 8.')
    table([
        ['Plan control', 'Specification'],
        ['Actors', 'Student (`regular_user`) and Advisor (`admin`); separate browser profiles to isolate cookies.'],
        ['Environment', 'Prepared disposable SQLite database; current local application; JavaScript enabled; base URL `http://127.0.0.1:5002`.'],
        ['Preparation', 'Use the safe local setup in the UAT execution record; do not reset an existing database. Confirm empty A/B/C semesters and the expected demo identities.'],
        ['Execution order', 'UAT-18 → UAT-01–05 → UAT-19 → UAT-06–17 → UAT-20. Numeric identifiers are retained.'],
        ['References', 'W1/W2/W3 are the panels in Figures 5.2/5.3/5.4. W4 means Student Messages/feedback; W5 means the cancellation/resubmission extensions to W2/W3.'],
        ['Recording', 'Record the observed outcome, actual evidence filename, deviation and remaining checks. PASS only when the complete required outcome is observed; observed primary outcomes with incomplete substeps are Executed — Partially Verified; FAIL only for an observed mismatch.'],
    ], widths=[b.W * .23, b.W * .77])
    h('6.1.1 Planned UAT data and baseline', 2, False)
    table([
        ['Item', 'Planned value'],
        ['Semesters A / B / C', 'Year 1 semester 1 / Year 1 semester 2 / Year 1 semester 3.'],
        ['Courses E1 / E2 / E3', 'COMP 1201 Object-Oriented Programming (requires completed COMP 1101); MATH 2250 Industrial Statistics; ENGL 1000 Academic Writing. Each is 3 credits; E2 and E3 have no prerequisites.'],
        ['Academic record', 'COMP 1101 and MATH 1200 Completed, 3 credits each; COMP 1600 In Progress, 3 credits. COMP 2100 is blocked because COMP 1600 is not completed.'],
        ['Degree requirements', 'Core Courses 36; General Education 18; Electives 12; Major Requirements 18; Additional Requirements 9; total 93 credits.'],
        ['Baseline totals', '6 completed; 3 in progress; 84 remaining; 93 required; 6% overall progress.'],
        ['Category progress', 'Core 3/36 (33 remaining); General Education 3/18 (15 remaining); Electives 0/12; Major Requirements 0/18; Additional Requirements 0/9.'],
    ], widths=[b.W * .24, b.W * .76])
    p('The seeded demo identities (Cameron Ramesar, Student ID `12345678`, Dr. Williams) and the 36/18/12/18/9 allocation are fictional coursework data. The author’s University ID is 816044668 and is shown on the cover.', 'small')
    for title, spec in sorted(uc, key=lambda x: x[0][:6]):
        d = fields(spec)
        steps = re.search(r'\*\*Exact browser steps\*\*\s*(.*?)\n\*\*Expected result:\*\*', spec, re.S).group(1)
        expected = spec.split('**Expected result:**', 1)[1].strip()
        # The execution record appends an observed-results table after each case's
        # expected result. Keep the planned expectation in the plan and leave the
        # observed results, statuses and evidence to Section 9.
        expected = re.split(r'\r?\n\s*\| Execution field\b', expected)[0].strip()
        steps = '\n'.join(x.strip() for x in steps.strip().splitlines() if x.strip())
        if title.startswith('UAT-01'):
            expected = ('Student workspace opens. Credits are 6 completed, 3 in progress, 84 remaining, '
                        'and 93 required; overall progress is 6/93 (6%). The category breakdown is Core 3/36 '
                        '(33 remaining), General Education 3/18 (15 remaining), Electives 0/12, Major '
                        'Requirements 0/18 and Additional Requirements 0/9. Recent activity shows the three '
                        'recorded courses with their correct statuses. Refresh preserves the values.')
        h(title, 2, False)
        table([
            ['Field', 'Planned specification'],
            ['Actor / wireframe', d.get('Actor', '') + '; ' + d.get('Wireframe component', d.get('Relevant wireframe component', ''))],
            ['Objective', d.get('Objective', '')],
            ['Preconditions', d.get('Preconditions', '')],
            ['Test data', d.get('Test data', '')],
            ['Procedure', steps],
            ['Expected result', expected],
        ], widths=[b.W * .18, b.W * .82], font_size=8.4, pad=3)

def case_matrix(entries, kind):
    h('6.2 Unit Test Plan' if kind == 'Unit' else '6.3 Integration Test Plan', 1)
    if kind == 'Unit':
        p('**Objective and boundary.** Verify business decisions in isolation from HTTP, templates and persistence. The tests exercise the real `AdvisingService` with autospecced repository doubles and in-memory SQLModel objects, and reject accidental database connections. `AuthService` orchestration uses mocked repository/security collaborators. UT-23 exercises real local cryptography with controlled time and test-only settings, without database or network access.')
        p('**Components.** AdvisingService dashboard totals, prerequisite eligibility, semester and selection validation, submission delegation, plan edit/review/cancel/removal rules; AuthService; current-user/role dependencies; password and JWT utilities. UT-01–23 identify specifications, not counts of parameterized executions.')
        table([
            ['Fixture / design', 'Planned specification'],
            ['Actors / terms', 'S1 Student id 1; S2 independent Student; A1 Advisor. T1 = Year 1 semester 1; T2 = Year 1 semester 2.'],
            ['Courses', 'C1 id101 COMP 1100, Core; C2 id102 MATH 1000, General Education; C3 id103 COMP 2000, Core, requires C1; C4 id104 MATH 2000, Electives, no prerequisite; C5 id105 COMP 3000, requires C1 and unknown MATH 9999. Each is 3 credits.'],
            ['Default state', 'C1 Completed; C2 In Progress; C3/C4 untracked; 93-credit degree; Core requirement 36; empty plan history. Cases override explicitly. F1 is synthetic test data, distinct from the browser seed.'],
            ['Positive / negative / boundary', 'Positive: eligible selections and legal decisions. Negative: invalid terms, duplicates, missing/foreign resources, bad identity. Boundary: zero totals, cap at 100%, duplicate records, last remaining course and 0/499/500/501 raw feedback characters.'],
            ['Oracle', 'Literal independently expected values and exact repository calls/no calls. The method under test is never mocked and the expected answer is not derived by calling it. Observed outcomes are not included in these plan tables.'],
        ], widths=[b.W * .25, b.W * .75])
    else:
        p('**Objective and boundary.** Join real FastAPI routes and dependencies, form/JSON parsing, real cookie/JWT authentication, services, repositories and SQLModel persistence. Exercise Student and Advisor workflows and database rollback. IT-19/20 intentionally reach database failures directly because service validation rejects those inputs before SQL.')
        table([
            ['Setup / coverage', 'Planned specification'],
            ['F2 data', 'Reuse F1 course/degree meanings but resolve generated row IDs. Seed two Students S1/S2 and Advisor A1, real password hashes, C1 Completed/C2 In Progress for S1, distinctive S2-only records/feedback, and independent plan state per variant.'],
            ['Isolation', 'Fresh per-case SQLite engine (StaticPool, check_same_thread=False), metadata and foreign keys enabled. New Session per HTTP request and per persistence check. Separate Student/Advisor cookie jars; follow_redirects=False.'],
            ['Startup and cleanup', 'Rebind test engine/session dependencies and startup/recovery initialization so normal/private databases cannot be touched. Do not replace authentication, handlers, business methods or CRUD. Close clients/sessions, restore overrides/lifespan/settings and dispose the engine.'],
            ['Coverage', 'Real login/logout; invalid credentials/tokens; current database roles; course eligibility; Student submission and persistence; Advisor queue and decisions; feedback/resubmission; removal/cancellation/replacement; ownership/privacy; invalid schemas, constraints and atomic rollback.'],
            ['Current contracts', 'Unauthenticated protected HTML/JSON: 401. Authenticated wrong-role guard: 403. HTML business errors: 303 plus a warning flash. Strict JSON APIs use documented 401/403/404/409/422 semantics.'],
        ], widths=[b.W * .25, b.W * .75])
    if kind == 'Unit':
        p('**Contract note.** UT-22 is adapted to the current 401/403 role contract. E01/E06/E07/E08 references denote existing database-backed baseline tests in `tests/test_advising_service.py`; their planning notes avoid duplicate coverage.', 'small')
    else:
        p('**Contract note.** IT-01/12/13 use the current 401/403 contract in place of the historical H3 wording. The original source documents remain unchanged; these are planned expectations, not new observations.', 'small')
    rows = [['Case / planned inputs and setup' if kind == 'Unit' else 'Case / planned input and procedure',
             'Expected output (not an observed result)']]
    for entry in entries:
        d = fields(entry['spec'])
        cid = d['Test ID']
        expected = d['Expected Result']
        if cid == 'UT-22':
            expected = ('Missing/invalid/unresolved identity raises HTTP 401; valid identity resolves the '
                        'repository user. The current `require_roles` guard denies `regular_user` at the Advisor '
                        'guard with 403 and returns `admin`. Test the current database role independently of a '
                        'token role claim.')
        if cid == 'IT-01':
            expected = expected.replace('protected access denied under H3',
                                        'protected HTML/JSON access denied with HTTP 401')
        if cid == 'IT-12':
            expected = ('Protected HTML and JSON requests return HTTP 401 for missing, malformed, expired, '
                        'wrong-signature or nonexistent-user tokens, with no private data and no database writes.')
        if cid == 'IT-13':
            expected = ('Authenticated Student access to the Advisor queue and review operations returns HTTP 403. '
                        'No queue/private data or status/feedback/advisor/course-link changes.')
        left = ('**' + entry['title'] + '**\n'
                '**Component:** ' + d.get('Source Function or Endpoint', '') + '\n'
                '**Preconditions:** ' + d.get('Preconditions', '') + '\n'
                '**Inputs:** ' + d.get('Test Data', '') + '\n'
                '**Procedure:** ' + d.get('Test Steps', ''))
        rows.append([left, expected])
    table(rows, widths=[b.W * .56, b.W * .44], font_size=8.3, pad=3)

def implementation(coll):
    new_page('7. Implementation')
    h('7.1 GitHub Repository', 1)
    p('Repository: [' + REPO + '](' + REPO + '). Default branch **main**. The published repository was verified on ' + PREPARED + ' at commit `' + COMMIT + '`; the repository, tree and required file links returned HTTP 200.')
    table([
        ['Artifact', 'Published location', 'Verification'],
        ['Application source', '`app/`', 'Current FastAPI application, models, services, repositories and routers are present.'],
        ['93-credit configuration', '`app/demo_requirements.py`', 'Core 36; General Education 18; Electives 12; Major 18; Additional 9; total 93.'],
        ['Unit tests', '`tests/unit/`', '`test_advising.py` and `test_auth.py` are present.'],
        ['Integration tests', '`tests/integration/`', 'Student, Advisor, database-integrity, audit-correction and contrast test files are present.'],
        ['Postman collection', '`docs/assignment2/postman/`', '`MyAdvisor-Assignment2.postman_collection.json` v2.1.0; 90 requests; revision `2026.10.27-degree93`.'],
        ['UAT screenshots', '`docs/assignment2/screenshots/UAT/`', 'All 55 case-level captures referenced by the execution record are present.'],
        ['Test plans', '`docs/assignment2/test-plans/`', 'UAT, unit and integration plans are present.'],
        ['Reports', '`docs/assignment2/reports/`', 'UAT, unit, integration and Postman reports are present.'],
        ['Project documentation', '`README.md`; `docs/report.md`; `docs/diagrams/`; `docs/wireframes/`', 'Project documentation, use case diagram and wireframe are present.'],
    ], widths=[b.W * .22, b.W * .38, b.W * .40], font_size=8.3)
    p('The published repository is the source of record for the application, tests, plans, reports, screenshots and exported Postman JSON. The 93-credit values are fictional coursework demonstration data, not official UWI curriculum data.')

    h('7.2 Unit Tests', 1)
    p('The unit suite is selected with `-m unit`. `tests/unit/conftest.py` patches repository constructors where `AdvisingService` imports them, supplies autospecced doubles and in-memory model objects, and guards database connections. The real service logic is preserved and mutation calls are tracked. `tests/unit/test_advising.py` implements UT-01–19; `tests/unit/test_auth.py` implements UT-20–23.')
    p('Functions under test include `get_student_dashboard`, `prerequisite_ok`, `get_course_availability`, `submit_plan`, `review_plan`, `cancel_plan`, `remove_submitted_course`, `authenticate_user`, `get_current_user`, the role guard and the password/JWT utilities. Parameterization covers legal and illegal status matrices and raw feedback-length boundaries. UT-23 uses real hashing and signing; credentials and tokens are not printed.')
    p('**Actual unit implementation example.** The following is a verbatim test from `tests/unit/test_advising.py`; it asserts both the empty-selection error and the early short-circuit behaviour.', 'small')
    code_block(snippet('tests/unit/test_advising.py', 'test_UT_09_empty_selection'))
    p('Source: [tests/unit/test_advising.py](' + REPO + '/blob/main/tests/unit/test_advising.py); [tests/unit/test_auth.py](' + REPO + '/blob/main/tests/unit/test_auth.py).', 'small')

    h('7.3 Integration Tests', 1)
    p('FastAPI and Starlette `TestClient` send real requests through the application. `tests/integration/conftest.py` creates a fresh SQLite engine and schema per case, enables foreign keys, isolates startup/recovery, overrides request sessions and opens independent actor clients. Real password hashing, JWT decoding, current database role lookup, request parsing, services and CRUD remain active. Teardown restores application settings and overrides and closes database resources.')
    table([
        ['Test file', 'Actual implementation'],
        ['`tests/integration/test_student_workflow.py`', 'Student login/cookies/logout, progress/catalogue, form and JSON submission, committed state, ownership/privacy, validation, removal, cancellation and same-ID resubmission.'],
        ['`tests/integration/test_advisor_workflow.py`', 'Real Student-to-Advisor queue delivery; decisions through form, generic JSON and named JSON actions; feedback; resubmission and replacement; authorization and validation boundaries.'],
        ['`tests/integration/test_database_integrity.py`', 'Real uniqueness and foreign-key constraints and rollback for failed create/resubmit; fresh-session checks of committed state.'],
        ['`tests/integration/test_audit_corrections.py`', 'Additional role-denial, malformed-email, registration and application-engine integrity variants.'],
        ['`tests/integration/test_contrast_regression.py`', 'Rendered-template contrast variants for normal, hover and Approved states.'],
    ], widths=[b.W * .40, b.W * .60], font_size=8.3)
    p('**Actual workflow implementation example.** The following is a verbatim opening of the cancellation, queue and replacement test. A real Student cancels a Pending plan, a fresh database snapshot verifies the Cancelled status and retained links, and the real Advisor queue becomes empty. The remainder submits a replacement and verifies the new Pending plan.', 'small')
    code_block(snippet('tests/integration/test_advisor_workflow.py',
                       'test_cancelled_plan_leaves_advisor_queue_and_replacement_returns', 0, 12))
    p('Source: [student workflow](' + REPO + '/blob/main/tests/integration/test_student_workflow.py); [advisor workflow](' + REPO + '/blob/main/tests/integration/test_advisor_workflow.py); [database integrity](' + REPO + '/blob/main/tests/integration/test_database_integrity.py).', 'small')

    h('7.4 API Tests — Postman', 1)
    p('**Collection:** ' + coll['info']['name'] + '. **Format:** Postman Collection v2.1.0. **Repository path:** `' + COLL + '`. **Published JSON:** [' + COLL + '](' + REPO + '/blob/main/' + COLL + '). The link was verified on ' + PREPARED + ' and returned HTTP 200.')
    p('The collection contains **90 ordered requests** in five folders. It covers all 15 implemented JSON API operations and supporting health, login, registration and logout calls. The published revision is `2026.10.27-degree93` and uses the approved 93-credit allocation. Request 01 initializes run variables; later requests depend on earlier state, so the collection is executed once in the original 01–90 order.')
    table([
        ['Ordered request group', 'Requests', 'Coverage'],
        ['01 Readiness and real cookie authentication', '01–12 (12)', 'Health; anonymous access; malformed cookie; bad/valid Student and Advisor login; independent Student registration/login.'],
        ['02 Role boundaries, progress and catalogue', '13–21 (9)', 'Role denials; response privacy; progress; dynamic eligible/blocked course discovery; free-semester selection.'],
        ['03 Student plan lifecycle and validation', '22–50 (29)', 'Empty, duplicate, unknown, ineligible and invalid submissions; persistence; foreign ownership; duplicate active plan; Pending removal and last-course protection.'],
        ['04 Advisor decisions and resubmission', '51–76 (26)', 'Queue/detail; invalid decisions and shapes; 500/501-character feedback; change request; same-ID resubmission; reject and approve.'],
        ['05 Cancellation, history and logout', '77–90 (14)', 'Preserved approval; cancellation/history/new-ID replacement; queue cleanup; actor logout and no-cookie denial.'],
    ], widths=[b.W * .31, b.W * .16, b.W * .53], font_size=8.3)
    p('**Authentication.** Login requests capture each actor’s `access_token` into separate collection variables. Requests send the intended actor’s Cookie explicitly; the prescribed run disables automatic cookie-jar and redirect handling. Exported password and token values are blank. Run-only credentials must be supplied privately on a disposable local instance.')
    p('**Positive and negative testing.** Valid operations are paired with expected 401/403/404/409/422 denials, malformed JSON and path IDs, spoofed fields, foreign resources, illegal status transitions and feedback boundaries. Read-back checkpoints verify that invalid or forbidden operations do not change the protected plan. Dynamic variables carry the base URL, actor tokens, discovered course IDs, selected semester and generated plan IDs.')
    p('**Workflow coverage.** WF1 uses request 19 for degree calculations and privacy. WF2 uses catalogue and eligibility (20), semester choice and invalid input (21–30), persisted submission (31–32), duplicate/state/ownership guards (33–47), removal and last-course checks (48–50), revision and returned status (63–72), and cancellation/history/replacement (78–86). WF3 covers queue/detail (51–53), malformed or invalid review/feedback/identity (54–60), requests for changes and feedback (61–68), rejection at the 500-character boundary (69–72), approval and state guards (73–77).')
    p('The historical Runner result in Section 8.3 (90 requests, 470 assertions, zero failures, zero execution errors) belongs to the earlier exported collection revision. The published degree93 revision passed static validation but has not been rerun in Postman. No new Runner pass is claimed.', 'small')

def reports():
    new_page('8. Reports')
    p('The results below are observed executions and are kept separate from the planned outcomes in Section 6. No pytest, Postman or browser UAT was rerun to prepare this document.')
    table([
        ['Execution', 'Verified result', 'Build / evidence qualification'],
        ['Historical unit-marker run', '113 passed; 602 deselected; 1 warning; 6.23 s', '26 October 2026 terminal screenshots; earlier source/build.'],
        ['Historical integration-marker run', '194 passed; 521 deselected; 1 warning; 30.52 s', '26 October 2026 terminal screenshots; earlier source/build.'],
        ['Historical Postman Runner', '90 requests; 470 assertions passed; 0 assertion failures; 0 execution errors', '27 October 2026; earlier exported collection revision; one iteration; 10 s 697 ms.'],
        ['Latest full pytest regression', '751 passed; 1 warning; 0 failures/errors/skips; 122.67 s; exit 0', '28 October 2026; retained text/XML and 74 source hashes.'],
        ['Manual UAT', '8 Pass; 12 Executed — Partially Verified; 0 Fail; 0 Not Executed', '4–5 November 2026; 55 case-level browser captures.'],
    ], widths=[b.W * .25, b.W * .42, b.W * .33], font_size=8.3)
    p('Counts are not additive across runs. The historical 715-item full suite contains 113 unit + 194 integration + 408 other nodes; the 751-item run contains 116 unit + 227 integration + 408 other nodes. These are membership counts in complete runs, not separately executed marked selections.', 'small')

    h('8.1 Unit Test Report', 1)
    p('**Objective.** Demonstrate isolated service and authentication rules and repository delegation. **Environment:** Windows/win32; repository `.venv`; Python 3.14.0; pytest 9.1.1; pluggy 1.6.0; anyio 4.15.1; pytest-asyncio 1.4.0; `pyproject.toml`.')
    p('**Actual command** (from the retained start capture, run from the repository root):')
    code_block('$base = Join-Path $env:LOCALAPPDATA "MyAdvisor-A2-Pytest"\n.\\.venv\\Scripts\\python.exe -m pytest tests -m unit -v --basetemp="$base\\unit"')
    p('**Observed summary:** 715 collected, 113 selected, 602 deselected; **113 passed, 1 warning in 6.23 s**. Figure 8.3 shows the genuine completed result. The warning is a `StarletteDeprecationWarning` about `httpx` use with `starlette.testclient`; it is a dependency-maintenance warning, not a failed assertion.')
    unit = sorted((H / 'screenshots/Unit').glob('*.png'))
    unit_caps = [
        'Retained start capture: command, environment, collection totals and early passing tests. 26 October 2026.',
        'Retained later capture: later UT variants and the warning text. 26 October 2026.',
        'Completed unit result: **113 passed, 602 deselected, 1 warning in 6.23 s**. 26 October 2026.',
    ]
    for i, f in enumerate(unit, 1):
        figure(f, '8.' + str(i), unit_caps[i - 1] + ' Original terminal capture published as `' + f.name + '`.',
               'Landscape', maxh=425)

    new_page('8.2 Integration Test Report', 1)
    p('**Objective.** Verify that real authentication, role/ownership dependencies, HTTP parsing, Student/Advisor workflows and database persistence work together. Components include `TestClient`, FastAPI, services and repositories, and per-case SQLModel/SQLite with independent request sessions; database-only cases reach real constraints and rollback. **Environment:** Windows/win32; Python 3.14.0; pytest 9.1.1; pluggy 1.6.0; anyio 4.15.1; pytest-asyncio 1.4.0; repository `.venv`.')
    p('**Actual command** (same writable temporary base defined in the unit start capture):')
    code_block('.\\.venv\\Scripts\\python.exe -m pytest tests -m integration -v --basetemp="$base\\integration"')
    p('**Observed summary:** 715 collected, 194 selected, 521 deselected; **194 passed, 1 warning in 30.52 s**. Figure 8.6 shows the genuine completed result. The warning is the same disclosed TestClient/httpx deprecation. The selected cases cover queue receipt, approve/reject/request-changes decisions, feedback delivery, same-ID resubmission, removal, allowed and forbidden cancellation, replacement history, cross-user privacy, missing/invalid authentication, validation and fresh-session state assertions.')
    integration = sorted((H / 'screenshots/Integration').glob('*.png'))
    int_caps = [
        'Retained start capture: command, environment, queue receipt, Advisor lifecycle and Student variants. 26 October 2026.',
        'Retained later capture: Advisor validation, feedback boundaries and repeated-review variants. 26 October 2026.',
        'Completed integration result: **194 passed, 521 deselected, 1 warning in 30.52 s**. 26 October 2026.',
    ]
    for i, f in enumerate(integration, 4):
        figure(f, '8.' + str(i), int_caps[i - 4] + ' Original terminal capture published as `' + f.name + '`.',
               'Landscape', maxh=425)

    new_page('8.2.1 Latest verified full-suite regression', 2, toc=False)
    p('The latest verified complete pytest regression is separate from the historical marked runs. It contains **751 passed, 1 warning, and zero failures, errors or skips in 122.67 s**, exit code 0. The retained run metadata records 116 unit / 227 integration / 408 other nodes as membership in one complete run, not as new separate marked executions.')
    table([
        ['Measure', 'Verified value'],
        ['Passed', '751'],
        ['Failed / errors / skipped', '0 / 0 / 0'],
        ['Warnings', '1 (Starlette/httpx deprecation)'],
        ['Duration', '122.67 s'],
        ['Exit code', '0'],
        ['Retained evidence', '`docs/assignment2/evidence/degree-requirements-2026-10-27/full-20261028T015858Z-e5cbdcfb.*`'],
        ['Source hashes', '74 application/test SHA-256 entries, checked against the current files'],
    ], widths=[b.W * .30, b.W * .70], font_size=8.5)
    p('**Actual full-run command** from the retained metadata (absolute paths abbreviated):')
    code_block('python -m pytest tests -q -p no:cacheprovider\n  --basetemp=[unique disposable path] --junitxml=[retained full-run XML]')
    p('**Verbatim retained final text line, not a screenshot:**')
    code_block('751 passed, 1 warning in 122.67s')
    p('The run used a fresh writable temporary directory and did not touch a normal or private database. Corrected-build environment metadata records FastAPI 0.141.1, SQLModel 0.0.42, SQLAlchemy 2.0.54, PyJWT 2.14.0, pwdlib 0.3.1 and SQLite 3.50.4.')

    h('8.3 Postman Collection Run Report', 1)
    p('**Collection:** MyAdvisor - COMP 3613 Assignment 2, v2.1 export. **Objective:** exercise all 15 JSON operations and supporting real login, registration and logout through the dependent Student/Advisor plan lifecycle, including negative status, role and ownership requests.')
    table([
        ['Execution detail', 'Observed / qualified value'],
        ['Evidence date', '27 October 2026 (user-confirmed; the Runner clock shows 01:25:19 AM without an independent time-zone record).'],
        ['Environment', 'Postman Collection Runner; environment none; 1 iteration; duration 10 s 697 ms; average response time 29 ms.'],
        ['Requests / assertions', '**90 requests executed**; **470 assertions passed**; **zero observed assertion failures**; **zero execution errors**.'],
        ['Authentication / authorization', 'Separate Student, Advisor and independent Student logins; expected anonymous and wrong-role denials; foreign ownership concealment and no-write read-back; response privacy.'],
        ['Workflow scenarios', 'Progress/catalogue; invalid and valid submission; Pending queue; feedback limits; request changes and resubmit; reject and approve; immutable states; removal, cancellation, history, replacement and logout.'],
        ['Conclusion', 'The recorded historical iteration passed its assertions. The published degree93 revision passed static validation but has not been rerun in Postman.'],
    ], widths=[b.W * .27, b.W * .73], font_size=8.2, pad=3)
    p('The captures below are genuine historical Runner views of the earlier exported collection revision. They show the same completed run across overlapping scroll positions, not six separate runs. They are not presented as execution of the current degree93 JSON.')
    post = [H / 'postman/Postman Screenshots/Screenshot 2026-10-27 012608.png',
            H / 'postman/Postman Screenshots/Screenshot 2026-10-27 012839.png',
            H / 'screenshots/postman-results.png']
    post_caps = [
        'Runner capture: requests 01–19 visible; authentication, role boundaries and progress. Completed summary shows 470 assertions and zero errors.',
        'Runner capture: requests 72–90 visible; approved-state guards, cancellation/history, replacement and logout. The same completed summary is visible.',
        'Additional summary view of requests 72–90 and the completed run: 90 requests, 470 assertions, zero assertion failures and zero execution errors.',
    ]
    for i, f in enumerate(post, 7):
        figure(f, '8.' + str(i), post_caps[i - 7] + ' Historical collection revision; 27 October 2026.',
               'Landscape', maxh=425)

def uat_summary():
    extract = json.loads((H / 'final-review/uat_extract.json').read_text(encoding='utf-8'))
    meta = {
        'UAT-01': ('WF1', 'Degree progress totals and category breakdown', 'Refresh persistence is not independently captured (byte-identical pair).'),
        'UAT-02': ('WF2', 'Catalogue search and filters', 'Title search, semester switching, combined filters and the clear-filter state are not captured.'),
        'UAT-03': ('WF2', 'Eligibility and selection review', 'Zero-selection prevention and the full count sequence are not captured; ineligible examples differ from the plan.'),
        'UAT-04': ('WF2', 'Submit plan A', 'None for the documented outcome.'),
        'UAT-05': ('WF2', 'Submission status after navigation and relogin', 'None for the documented outcome.'),
        'UAT-06': ('WF3', 'Advisor pending review', 'None for the documented outcome.'),
        'UAT-07': ('WF3 / WF2', 'Request changes and feedback', 'Advisor action confirmation and removal from the Pending queue are not captured.'),
        'UAT-08': ('WF2 / WF3', 'Revise and resubmit', 'Current Pending Messages with cleared prior feedback is not captured.'),
        'UAT-09': ('WF3 / WF2', 'Approve revised plan', 'Advisor action confirmation and queue removal are not captured.'),
        'UAT-10': ('WF2', 'Separate semester plan', 'None for the documented outcome.'),
        'UAT-11': ('WF3 / WF2', 'Reject separate plan', 'Advisor action confirmation and queue removal are not captured.'),
        'UAT-12': ('WF2 / WF3', 'Pending plan for cancellation', 'A Approved and B Rejected are not co-visible with the C state.'),
        'UAT-13': ('WF2 / WF3', 'Remove course and protect the last course', 'The remove-confirmation dismissal/no-change state is not captured.'),
        'UAT-14': ('WF2', 'Cancel Approved plan', 'None for the documented outcome.'),
        'UAT-15': ('WF2', 'Cancel Rejected plan', 'None for the documented outcome.'),
        'UAT-16': ('WF2 / WF3', 'Cancel Pending plan and clear the queue', 'None for the documented outcome.'),
        'UAT-17': ('WF2 / WF3', 'Start a new plan after cancellation', 'None for the documented outcome.'),
        'UAT-18': ('Login', 'Student login and clean-run baseline', 'Empty A/B/C Plan Courses and Messages baselines are not captured; the Home refresh pair is byte-identical.'),
        'UAT-19': ('Login / WF3', 'Advisor login', 'The refresh pair is byte-identical; a simultaneous separate Student session is not captured.'),
        'UAT-20': ('Login / security', 'Role and signed-out restrictions', 'The Student and Advisor signed-out checks share one byte-identical 401 image.'),
    }
    new_page('9. UAT Execution Summary')
    p('The latest manual UAT execution used **55 case-level browser screenshots covering all 20 cases**. The tester was Cameron Ramesar; the application date shown in the captures is 5 November 2026, and the local files were saved on 4 November 2026 (UTC−04:00). No browser workflow, pytest run or Postman run was rerun to prepare this summary.')
    table([
        ['Result', 'Count', 'Cases'],
        ['**PASS**', '**8**', 'UAT-04, UAT-05, UAT-06, UAT-10, UAT-14, UAT-15, UAT-16, UAT-17'],
        ['**EXECUTED — PARTIALLY VERIFIED**', '**12**', 'UAT-01, UAT-02, UAT-03, UAT-07, UAT-08, UAT-09, UAT-11, UAT-12, UAT-13, UAT-18, UAT-19, UAT-20'],
        ['**FAIL**', '**0**', '—'],
        ['**NOT EXECUTED**', '**0**', '—'],
    ], widths=[b.W * .29, b.W * .10, b.W * .61], font_size=8.7)
    p('The 12 partially verified cases are **not failures**. Each has genuine execution evidence demonstrating its principal workflow; the remaining supplementary checks listed below were not captured or are not independently proven. No case is wholly unexecuted.')
    p('**Observed execution data.** Plan A used COMP 1201 + MATH 2250 (2 courses/6 credits); revised A used COMP 1201 + ENGL 1000 (2/6); B used MATH 2250 (1/3); C used COMP 1201 + MATH 2250 and then COMP 1201 only; replacement C used ENGL 1000 only (1/3). Degree Progress categories total 93 (3/36, 3/18, 0/12, 0/18, 0/9), with 6 completed, 3 in progress, 84 remaining, 93 required and 6%.')
    h('9.1 Results matrix', 1, False)
    p('**PASS — complete required outcome observed.**', 'small')
    pass_rows = [['Case', 'Workflow', 'Scenario', 'Shots']]
    part_rows = [['Case', 'Workflow', 'Scenario', 'Shots', 'Remaining supplementary checks']]
    for rec in sorted(extract, key=lambda r: r['case']):
        cid = rec['case']
        status = rec['status'].strip().strip('|').strip()
        wf, scenario, remaining = meta[cid]
        shots = len(re.findall(r'\.png', rec['refs']))
        if status == 'PASS':
            pass_rows.append([cid, wf, scenario, str(shots)])
        else:
            part_rows.append([cid, wf, scenario, str(shots), remaining])
    table(pass_rows, widths=[b.W * .12, b.W * .14, b.W * .62, b.W * .12], font_size=8.4)
    p('**EXECUTED — PARTIALLY VERIFIED — principal workflow demonstrated; supplementary checks unconfirmed.**', 'small')
    table(part_rows, widths=[b.W * .10, b.W * .15, b.W * .33, b.W * .09, b.W * .33], font_size=8.2, pad=3)
    p('Four before/after pairs are byte-identical and therefore do not independently prove persistence or separate-role checks: UAT-01 degree progress/refresh, UAT-18 baseline/home, UAT-19 Advisor home/refresh, and UAT-20 Student/Advisor signed-out 401. The original files are preserved and are not presented as independent captures.', 'small')

    h('9.2 Evidence index', 1, False)
    p('The complete 55-screenshot set is published in the repository at `docs/assignment2/screenshots/UAT/`. The table lists the case-level files referenced by the execution record; the folder also retains byte-identical renamed copies used for presentation, and no original file was deleted or modified.', 'small')
    idx = [['Case', 'Published case-level evidence files']]
    for rec in sorted(extract, key=lambda r: r['case']):
        names = re.findall(r'screenshots/UAT/([^/)]+\.png)', rec['refs'])
        idx.append([rec['case'], '\n'.join('`' + n + '`' for n in names)])
    table(idx, widths=[b.W * .11, b.W * .89], font_size=7.7, pad=2)

    h('9.3 Representative screenshots', 1, False)
    p('The following captures are representative examples of the 55-image evidence set. Each caption states the case status. The complete set remains published in the repository; the PDF does not duplicate all 55 images in order to keep the submission compact and readable.', 'small')
    reps = [
        ('UAT-01-degree-progress.png', 'UAT-01 — View degree progress', 'EXECUTED — PARTIALLY VERIFIED',
         'Degree Progress shows 6 completed, 3 in progress, 84 remaining and 93 required, with the corrected category breakdown 3/36, 3/18, 0/12, 0/18 and 0/9. Refresh persistence is not independently captured (duplicate pair).'),
        ('UAT-04.png', 'UAT-04 — Submit semester plan A', 'PASS',
         'Plan A is Pending with COMP 1201 + MATH 2250 (2 courses/6 credits); the after-refresh capture shows the same Pending state and locked selection form.'),
        ('UAT-06-advisor-pending-review.png', 'UAT-06 — Advisor reviews the submitted plan', 'PASS',
         'Advisor Review shows the Student summary, Year 1 semester 1, PENDING, COMP 1201 + MATH 2250, 2 courses/6 credits and the Approve/Reject/Request Changes controls.'),
        ('UAT-07-request-changes.png', 'UAT-07 — Request changes and deliver feedback', 'EXECUTED — PARTIALLY VERIFIED',
         'Advisor feedback is recorded for plan A; the Student sees the same feedback and the plan remains editable. Advisor action confirmation and queue removal are not captured.'),
        ('UAT-13-course-removed.png', 'UAT-13 — Remove a course and protect the last course', 'EXECUTED — PARTIALLY VERIFIED',
         'Plan C remains Pending with COMP 1201 only (1 course/3 credits), and the final-course guard is visible. The remove-confirmation dismissal state is not captured.'),
        ('UAT-14-approved-cancelled.png', 'UAT-14 — Cancel an Approved plan', 'PASS',
         'Plan A is Cancelled with the prior approval feedback retained and zero selected; the dismissed-confirmation capture still shows A Approved.'),
        ('UAT-17-new-plan.png', 'UAT-17 — Start a new plan after cancellation', 'PASS',
         'After cancellation, plan C is replaced with a new Pending plan containing ENGL 1000 only (1 course/3 credits); the Advisor queue shows the replacement.'),
        ('UAT-20-student-403.png', 'UAT-20 — Role and signed-out restrictions', 'EXECUTED — PARTIALLY VERIFIED',
         'A logged-in Student receives the 403 JSON authorization response for an Advisor/admin resource. The separate Student and Advisor signed-out checks share one byte-identical 401 image.'),
    ]
    for i, (fname, label, status, caption) in enumerate(reps, 1):
        f = UAT_DIR / fname
        kind = 'Portrait' if PILImage.open(f).size[1] / PILImage.open(f).size[0] > 0.85 else 'Landscape'
        # The UAT-20 403 capture is almost entirely empty dark background; crop only
        # that empty area for legibility. The published original file is unchanged.
        crop, note = None, ''
        if fname == 'UAT-20-student-403.png':
            crop = (0, 0, 560, 104)
            note = ' Shown as a cropped detail: the unused dark background is omitted for legibility and the original capture is unchanged.'
        figure(f, '9.' + str(i), label + ' — status: **' + status + '**. ' + caption +
               ' Original capture `' + fname + '`; application date 5 November 2026 (local capture 4 November 2026).' + note,
               kind, maxh=(640 if kind == 'Portrait' else 420), crop=crop)

def limitations():
    new_page('Appendix A — Testing Limitations and Future Improvements')
    p('This appendix records the material limitations that qualify the evidence. It is not a second audit and does not change the academic deliverables. The project is complete as an academic submission; production deployment readiness is a separate question and is not claimed.')
    table([
        ['Area', 'Verified limitation', 'Effect on this submission'],
        ['UAT supplementary checks', '12 cases have genuine principal-workflow evidence but unverified supplementary checks: refresh persistence (duplicate pairs), empty A/B/C baselines, Advisor confirmation/queue removal, remove-confirmation dismissal, combined search/filter states, and separate post-logout role checks.', '12 cases are classified Executed — Partially Verified, not Pass and not Fail. The principal workflows are demonstrated.'],
        ['Postman runtime evidence', 'The 90-request / 470-assertion Runner result belongs to the earlier exported collection revision. The published degree93 revision passed static validation but has not been rerun in Postman.', 'The historical Runner evidence is reported as historical. No new Runner pass is claimed for the revised collection.'],
        ['CSRF protection', 'No explicit CSRF token or Origin check was added to authenticated form writes; the production cookie is configured with SameSite=None and logout remains a GET request. No live exploit was executed.', 'Production security hardening remains a review item. It does not prevent academic submission, and no production certification is claimed.'],
        ['Production signing key', 'The deployment blueprint requests a generated production key, but the live runtime configuration was not independently verified; settings still permit fallback to the public example key.', 'A production deployment must verify a strong, private signing key before use. No production key is reproduced in this document.'],
        ['Historical build provenance', 'The unit, integration and Postman screenshots are genuine but tied to earlier source/build executions. The UAT session retained dated captures but not complete browser/version, URL, database path or build metadata.', 'The evidence supports the reported results but is not a cryptographic certification of every tested revision.'],
        ['Database and deployment scope', 'Automated tests use isolated SQLite. PostgreSQL behaviour, concurrency, load, production cookies and deployed CSRF behaviour were not independently exercised.', 'The results establish the coursework application and its local workflows, not production-scale behaviour.'],
        ['Dependency warning', 'One Starlette/httpx deprecation warning appears in the unit and integration runs. It is a dependency-maintenance warning, not a failed assertion.', 'All selected assertions passed; a future dependency upgrade should be regression-tested.'],
    ], widths=[b.W * .18, b.W * .50, b.W * .32], font_size=8.2, pad=3)
    p('**Future improvements.** Complete the remaining UAT supplementary checks and record the session build/URL/database metadata; rerun the published degree93 Postman collection and archive the new Runner result; add and test CSRF/Origin protection for authenticated form writes; verify the production signing-key configuration and remove the public-key fallback in production; exercise the application against PostgreSQL and concurrent requests; and complete a human readability review of the accessible contrast states.')
    p('**Readiness statement.** The document contains every lecturer-required section and the genuine evidence needed for academic assessment. The limitations above are disclosed so that the report does not overstate production security or complete verification. They are not submission blockers for the coursework deliverables.')

def checklist():
    new_page('Appendix B — Submission Checklist')
    p('This checklist distinguishes the required PDF content, repository publication and disclosed testing limitations. It describes the academic submission, not production deployment readiness.')
    table([
        ['Required PDF content', 'Status'],
        ['1. Name & ID', 'Included — professional cover page, Cameron Ramesar, 816044668'],
        ['2. Project Description', 'Included — purpose, roles, WF1–WF3, technologies, 93-credit configuration'],
        ['3. Use Case Diagram', 'Included — original diagram, Figure 3.1'],
        ['4. Entity Relationship Diagram', 'Included — original ERD and readable keyed rendering, Figures 4.1–4.2'],
        ['5. Application Wireframe', 'Included — original three-panel wireframe and three enlarged panels, Figures 5.1–5.4'],
        ['6. Test Plans', 'Included — 6.1 UAT, 6.2 Unit, 6.3 Integration'],
        ['7. Implementation', 'Included — 7.1 repository, 7.2 unit, 7.3 integration, 7.4 Postman'],
        ['8. Reports', 'Included — 8.1 Unit, 8.2 Integration, 8.2.1 full regression, 8.3 Postman'],
        ['UAT execution summary', 'Included — Section 9, 8 Pass / 12 Partial / 0 Fail / 0 Not Executed'],
        ['Testing limitations', 'Disclosed — Appendix A'],
        ['**Required PDF content**', '**Included — no missing lecturer-required section**'],
        ['**Repository publication**', '**Verified — commit `' + COMMIT + '`; required paths, 55 UAT captures and 90-request degree93 JSON present**'],
        ['**Additional testing limitations**', '**Disclosed — Appendix A**'],
        ['**Academic submission**', '**Ready**'],
        ['**Production deployment readiness**', '**Not claimed**'],
    ], widths=[b.W * .34, b.W * .66], font_size=8.4)
    p('**Link verification.** Repository: ' + REPO + ' (HTTP 200). The published Postman collection JSON is linked from Section 7.4 and returned HTTP 200. Verified on ' + PREPARED + '.', 'small')
    p('**Evidence integrity.** The original unit, integration, Postman and UAT images were reused without modification. No application code, test, UAT or Postman result was rerun or fabricated for this document. Password constants and authentication-token values are not reproduced.', 'small')

def build_story(pages=None):
    global S, bookmarks, figures, TOC_ENTRIES
    S = []
    bookmarks = []
    figures = []
    TOC_ENTRIES = []
    uc = b.cases((H / 'reports/uat-execution.md').read_text(encoding='utf-8-sig'), 'UAT')
    coll = json.loads((R / COLL).read_text(encoding='utf-8-sig'))
    erd_src = re.search(r'```mermaid\n(erDiagram.*?)```',
                        (R / 'docs/report.md').read_text(encoding='utf-8-sig'), re.S).group(1)
    cover_story()
    cover_part = S
    S = []
    project_description()
    use_case()
    erd(erd_src)
    wireframe()
    uat_plan(uc)
    case_matrix(json.loads((H / 'final-review/specifications.json').read_text(encoding='utf-8'))['UT'], 'Unit')
    case_matrix(json.loads((H / 'final-review/specifications.json').read_text(encoding='utf-8'))['IT'], 'Integration')
    implementation(coll)
    reports()
    uat_summary()
    limitations()
    checklist()
    body_part = S
    S = cover_part
    toc_story(pages or {})
    S.extend(body_part)
    return S

def build_pdf(path, pages=None, total=None):
    global TOTAL_PAGES, PAGE_MAP
    TOTAL_PAGES = total
    PAGE_MAP = {}
    story = build_story(pages)
    doc = Doc(str(path), pagesize=A4, leftMargin=b.M, rightMargin=b.M,
              topMargin=51, bottomMargin=42,
              title='COMP 3613 Assignment 2 — MyAdvisor',
              author='Cameron Ramesar', subject='Final assignment submission',
              keywords='MyAdvisor, COMP 3613, Assignment 2, test plans, UAT, Postman')
    for kind, size, top in [('Cover', A4, 95), ('Portrait', A4, 51),
                            ('Landscape', landscape(A4), 51)]:
        ww, hh = size
        on_page = cover_bg if kind == 'Cover' else footer
        doc.addPageTemplates(PageTemplate(kind, [
            Frame(b.M, 42, ww - 2 * b.M, hh - top - 42, leftPadding=0,
                  rightPadding=0, topPadding=0, bottomPadding=0)],
            onPage=on_page, pagesize=size))
    doc.multiBuild(story)
    return dict(PAGE_MAP)

def main():
    # Converge the contents page numbers: the entry geometry is fixed, so the
    # page map stabilises after the second pass.
    pages, total = {}, None
    for _ in range(4):
        recorded = build_pdf(TMP, pages, total)
        with fitz.open(TMP) as d:
            count = len(d)
        if count == total and recorded == pages:
            break
        pages, total = recorded, count
    os.replace(TMP, OUT)
    with fitz.open(OUT) as d:
        toc = d.get_toc()
        pages_out = len(d)
    print(json.dumps({'pdf': str(OUT), 'pages': pages_out, 'bytes': OUT.stat().st_size,
                      'sha256': hashlib.sha256(OUT.read_bytes()).hexdigest(),
                      'toc': toc, 'figures': len(figures), 'map': pages}, indent=2))

if __name__ == '__main__':
    main()
