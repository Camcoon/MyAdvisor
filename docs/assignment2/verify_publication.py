"""Verify the published MyAdvisor repository and save a concise verification record.

Read-only. No application code, tests or remote state is changed.
"""
from pathlib import Path
import io, json, re, hashlib, urllib.request, urllib.parse
from datetime import datetime, timezone

H = Path(__file__).resolve().parent
R = H.parents[1]
REPO = 'Camcoon/MyAdvisorWithTests'
API = f'https://api.github.com/repos/{REPO}'
RAW = f'https://raw.githubusercontent.com/{REPO}/main/'
BLOB = f'https://github.com/{REPO}/blob/main/'
COLL = 'docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json'

def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers={'User-Agent': 'MyAdvisor-submission-check'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(), dict(r.headers)

def head(url):
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'MyAdvisor-submission-check'})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status
    except Exception as e:
        return getattr(e, 'code', str(e))

status, body, _ = fetch(API)
meta = json.loads(body)
branch_status, branch_body, _ = fetch(API + '/branches/main')
branch = json.loads(branch_body)
commit = branch['commit']['sha']
tree_status, tree_body, _ = fetch(API + f'/git/trees/{commit}?recursive=1')
tree = json.loads(tree_body)
paths = {x['path'] for x in tree['tree']}

required = [
    'app/main.py', 'app/demo_requirements.py', 'app/models/advising.py',
    'app/services/advising_service.py', 'app/routers/user_home.py', 'app/routers/admin_home.py',
    'tests/unit/test_advising.py', 'tests/unit/test_auth.py',
    'tests/integration/test_student_workflow.py', 'tests/integration/test_advisor_workflow.py',
    'tests/integration/test_database_integrity.py',
    COLL,
    'docs/assignment2/test-plans/uat-test-plan.md',
    'docs/assignment2/test-plans/unit-test-plan.md',
    'docs/assignment2/test-plans/integration-test-plan.md',
    'docs/assignment2/reports/uat-execution.md',
    'docs/assignment2/reports/unit-test-report.md',
    'docs/assignment2/reports/integration-test-report.md',
    'docs/assignment2/reports/postman-test-report.md',
    'docs/report.md', 'README.md', 'docs/diagrams/use-case.png',
    'docs/wireframes/Three-Panel Student Advisor Dashboard Mockup.png',
]
missing = [p for p in required if p not in paths]

# The 55 screenshots named in the current UAT execution record must be published.
uat_md = (H/'reports/uat-execution.md').read_text(encoding='utf-8-sig')
uat_refs = sorted(set(re.findall(r'screenshots/UAT/([^/)]+\.png)', uat_md)))
remote_uat = {p.split('/')[-1] for p in paths if p.startswith('docs/assignment2/screenshots/UAT/')}
missing_uat = [f for f in uat_refs if f not in remote_uat]

# Compare key text files with the local working tree, ignoring CRLF/LF differences.
compare = ['app/demo_requirements.py', COLL, 'docs/assignment2/reports/uat-execution.md',
           'docs/assignment2/test-plans/uat-test-plan.md']
same = {}
for p in compare:
    s, data, _ = fetch(RAW + urllib.parse.quote(p))
    remote = data.decode('utf-8-sig').replace('\r\n', '\n')
    local = (R/p).read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    same[p] = (s == 200 and remote == local)

# Published collection structure and approved allocation.
s, cbody, _ = fetch(RAW + urllib.parse.quote(COLL))
coll = json.loads(cbody)
def walk(items):
    for it in items:
        if 'item' in it:
            yield from walk(it['item'])
        else:
            yield it
requests = list(walk(coll['item']))
_, demobody, _ = fetch(RAW + 'app/demo_requirements.py')
demo = demobody.decode('utf-8-sig')

report = {
    'repository': f'https://github.com/{REPO}',
    'verified_utc': datetime.now(timezone.utc).isoformat(),
    'http': {'repository': status, 'main_branch': branch_status, 'tree': tree_status,
             'collection_link': head(BLOB + COLL), 'repository_blob_link': head(f'https://github.com/{REPO}')},
    'commit': commit,
    'tree_entries': len(paths),
    'required_paths_present': not missing,
    'missing_required_paths': missing,
    'uat_screenshots_referenced': len(uat_refs),
    'uat_screenshots_published': all(f in remote_uat for f in uat_refs),
    'missing_uat_screenshots': missing_uat,
    'published_uat_files': len(remote_uat),
    'key_files_identical_to_local_ignoring_line_endings': same,
    'collection': {
        'schema': coll['info']['schema'],
        'version': coll['info'].get('version'),
        'requests': len(requests),
        'same_as_local_ignoring_line_endings': same[COLL],
    },
    'approved_allocation': {
        'total_93': 'DEMO_TOTAL_CREDITS = 93' in demo,
        'core_36': '("Core Courses", 36)' in demo,
        'general_education_18': '("General Education", 18)' in demo,
        'electives_12': '("Electives", 12)' in demo,
        'major_18': '("Major Requirements", 18)' in demo,
        'additional_9': '("Additional Requirements", 9)' in demo,
    },
    'verified': False,
}
report['verified'] = bool(
    status == 200 and branch_status == 200 and tree_status == 200
    and not missing and not missing_uat and all(same.values())
    and coll['info']['schema'].endswith('/v2.1.0/collection.json')
    and len(requests) == 90 and all(report['approved_allocation'].values())
    and report['http']['collection_link'] == 200
)
(H/'final_submission_verification.json').write_text(
    json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(report, indent=2, ensure_ascii=False))
