from pathlib import Path
import sys,re,json,hashlib
H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path.insert(0,str(H/'.pdf-tools'))
import pymupdf as fitz
from PIL import Image
def cases(t,p):
 return re.findall(r'^### ('+p+r'-\d{2}[^\n]*)\n(.*?)(?=^### '+p+r'-\d{2}|^## |\Z)',t,re.M|re.S)
out={}
for p,f in [('UAT','reports/uat-execution.md'),('UT','test-plans/unit-test-plan.md'),('IT','test-plans/integration-test-plan.md')]:
 t=(H/f).read_text(encoding='utf-8-sig')
 cs=cases(t,p)
 out[p]=[{'title':a,'spec':b.split('| Execution field |')[0] if p=='UAT' else '\n'.join(x for x in b.splitlines() if not any(y in x for y in ['Actual Result','Evidence Reference','| Status |']))} for a,b in cs]
(H/'final-review/specifications.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
for f in ['COMP3613_Assignment2_MyAdvisor.pdf','../report.pdf']:
 d=fitz.open(H/f)
 print(f,len(d),'pages',d.get_toc()[:30])
 if 'report.pdf' in f:
  print('ORIGINAL COVER',d[0].get_text()[:1000])
  for n,p in enumerate(d):
   if any(x in p.get_text() for x in ['DEGREE_PROGRAM','Use case','Use Case','Wireframe']): print('original diagram candidate',n+1,p.get_text()[:120])
for f in [R/'docs/diagrams/use-case.png',*list((R/'docs/wireframes').glob('*.png')),*list((H/'screenshots/Unit').glob('*.png')),*list((H/'screenshots/Integration').glob('*.png')),H/'screenshots/postman-results.png',*list((H/'postman/Postman Screenshots').glob('*.png'))]:
 print('IMAGE',str(f.relative_to(R)),Image.open(f).size)
meta=json.loads((H/'evidence/corrections-2026-10-27/full-20261027T193800Z-7227960f.json').read_text())
print('SOURCE MISMATCHES',[p for p,h in meta['source_sha256'].items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h])
for p in ['UT','IT']:
 print(p,'case fields',sorted(set(re.findall(r'^\| ([^|]+) \|',out[p][0]['spec'],re.M))))
