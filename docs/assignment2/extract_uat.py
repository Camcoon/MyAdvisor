import re, io, json
from pathlib import Path
H = Path(__file__).resolve().parent
t = (H/'reports/uat-execution.md').read_text(encoding='utf-8-sig')
out = []
for m in re.finditer(r'^### (UAT-\d{2})[^\n]*\n(.*?)(?=^### UAT-\d{2}|^## |\Z)', t, re.M|re.S):
    cid, body = m.group(1), m.group(2)
    def f(k):
        mm = re.search(r'\| ' + re.escape(k) + r' \| ([^\n]*)', body)
        return mm.group(1).strip() if mm else ''
    out.append({'case': cid, 'title': re.search(r'^### (UAT-\d{2} . [^\n]*)', m.group(0), re.M).group(1),
                'status': f('Status'), 'actual': f('Actual result'), 'refs': f('Screenshot evidence reference')})
(H/'final-review/uat_extract.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
print('written', len(out))
