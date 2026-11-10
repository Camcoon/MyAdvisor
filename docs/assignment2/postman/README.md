# MyAdvisor Postman collection

> **Approved-allocation update ? 27 October 2026:** [Current correction record](../reports/degree-requirement-correction.md) supersedes earlier allocation-pending statements and the 735-build attribution for the changed source. Approved fictional category requirements are Core 36, General Education 18, Electives 12, Major 18, Additional 9 (total 93), not official UWI requirements. Historical results/images and synthetic test fixtures below remain preserved. New Postman/manual acceptance remains pending; no old screenshot is relabelled as this build.


Current evidence status, 27 October 2026: **90 requests executed, 470 assertions passed, zero assertion failures and zero execution errors, one iteration**, supported by the supplied Runner captures and user confirmation. See the [Postman test report](../reports/postman-test-report.md) for evidence and provenance limits. This audit did not rerun Postman/Newman.

The creation-stage static checks below are historical. The collection description's execution-pending wording also describes that earlier stage; the linked report is authoritative for the recorded runtime outcome. The JSON definition has not been changed by this documentation correction.

Finalization checks parsed the JSON, compiled all 93 JavaScript scripts across
90 requests and collection hooks, checked declared request variables and cookie
settings, and compared every method/path with actual FastAPI router declarations.
All 15 implemented JSON API operations are covered. These are static artifact
checks; no server requests or Postman assertions were executed. This includes
structural checks, not validation against a downloaded Postman JSON Schema.

On 26 October 2026, neither Postman nor Newman was found on PATH. No Postman
process was running, and the usual per-user/Program Files Postman executables
and npm Newman shim were absent. Node.js is available; the Newman module is not.
The global npm listing reported a missing per-user npm directory. This inventory
does not rule out a portable installation elsewhere or the Postman web app.

The Prompt 11 source is the collection beside this README:
`docs/assignment2/postman/MyAdvisor-Assignment2.postman_collection.json`.
There was no `postman/MyAdvisor-A2.postman_collection.json` in this checkout.
Keep this existing filename as the single maintained collection.

## Prepare the local app

Run commands from the repository directory containing `manage.py`. Use the
existing project virtual environment and local configuration described in the
[project README](../../../README.md). Use a disposable local database: this
collection writes real records through the existing application services.

Use a **new PowerShell terminal** and change to the project directory containing
`manage.py` (the nested `Assignment 2` directory in this workspace). Use the
commands below to create a new SQLite file in a unique temporary directory and
override the database configuration for this terminal only. Do not reuse the
normal application's server. Port 5001 keeps this server separate from port 5000.
If 5001 is occupied, choose another unused port and update `base_url` to match.

```powershell
$postmanRunDir = Join-Path ([System.IO.Path]::GetTempPath()) ("MyAdvisor-A2-Postman-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $postmanRunDir -ErrorAction Stop | Out-Null
$postmanDbPath = Join-Path $postmanRunDir 'postman.sqlite3'
$env:DATABASE_URI = 'sqlite:///' + $postmanDbPath.Replace('\', '/')
$env:ENV = 'postman'
$env:SECRET_KEY = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
Write-Host "Disposable Postman database: $postmanDbPath"
.\.venv\Scripts\python.exe manage.py init --no-drop
if ($LASTEXITCODE -ne 0) { throw 'Disposable database initialization failed; stop here.' }
.\.venv\Scripts\python.exe manage.py run --host 127.0.0.1 --port 5001
```

Keep this terminal open for the run. The environment overrides apply to both
commands and take precedence over `.env`; no `.env` file is edited. The generated
signing key exists only in this terminal, and no existing database is reset.
The collection restricts `base_url` to HTTP `localhost` or `127.0.0.1` with an
explicit port; that restriction cannot verify which database a server uses.
Confirm the initialization output names the unique SQLite path above before
running. Do not point this collection at an original-data or production server.

Adjust the virtual-environment path if yours is elsewhere. Do not use the plain
`init` command on data you need; its default behavior drops tables. Confirm
local configuration points to the intended database before initializing.
`init --no-drop` creates missing tables and seeds demo data; it does not reset
an existing account's password or role.

Required fixtures:

- One Student account with database role `regular_user`. Seeded `bob` has local
  demo password `bobpass`. It needs two eligible courses and at least one
  course blocked specifically by **missing prerequisites**. The seeded
  catalogue and Bob's academic records satisfy these requirements.
- One Advisor account with database role `admin`. Seeded `admin` has local demo
  password `adminpass`. There is no separate `advisor` role or bearer login API.
- At least one of the nine supported semesters whose latest Student plan is
  absent or Cancelled. The collection chooses one automatically, without
  cancelling pre-existing active plans. Use a fresh local student/database if
  all semesters have active plans.
- ID `2147483647` must be absent from the local course and plan tables. This
  reserved test value exercises unknown-resource errors; it is not a fixture ID.

The collection registers a fresh, independent Student via `/register` on every
run. Its generated username, email and password are used only for ownership
checks. No elevated account is registered or created by the collection.

## Import and configure

1. Open Postman Desktop, or use the Postman web app with its Desktop Agent so
   requests can reach localhost.
2. Select **Import**, choose
   `MyAdvisor-Assignment2.postman_collection.json`, and import the collection.
3. Open the collection's **Variables** tab. Set local values as follows. Keep
   credentials local; do not publish or share populated collection exports.

| Variable | Local value |
| --- | --- |
| `base_url` | `http://127.0.0.1:5001`, with no trailing slash, for the isolated server above |
| `student_username` | `bob`, or your prepared Student username |
| `student_password` | Your Student password; `bobpass` for unchanged demo data |
| `advisor_username` | `admin`, or your existing Advisor username |
| `advisor_password` | Your Advisor password; `adminpass` for unchanged demo data |

Password values are intentionally blank in the supplied JSON. Set them only in
your local Postman values and mark them sensitive where supported. Select
**No environment** and use no Runner data file. A collection pre-request hook
pins substitutions to the same collection values used by assertions, preventing
an environment/global value from substituting another role or plan ID.
No separate environment template is necessary; all inputs are declared as
collection variables. Do not sync or share populated values.

Leave generated variables blank. The first request resets run state and creates
independent Student credentials. Successful login requests capture the real
`access_token` response cookie into `student_token`, `advisor_token` and
`other_token`. Catalogue and plan responses populate `course_a_id`,
`course_b_id`, `blocked_course_id`, `semester_name`, `plan_id`, `old_plan_id` and
`advisor_id`. The allowlisted Advisor users response supplies the three distinct
account IDs. `prerequisite_course_id` and `prerequisite_reason` identify an
actual unmet-prerequisite case; `baseline_plans` records the pre-run history.

Every request disables automatic redirects and the cookie jar using its
protocol settings. Login assertions inspect the actual 303 and issued cookie.
API requests send the appropriate explicit `Cookie: access_token=...` header.
Unauthenticated requests send no token. This prevents an Advisor login from
silently replacing the Student identity, or browser cookies contaminating 401
checks. Keep these per-request settings when importing or editing requests.

## Run locally

1. Keep the local server running.
2. Select the collection, then **Run collection**.
3. Select **all 90 requests**, retaining their original order across all five
   folders. Use **one iteration**, no data file and no parallel execution.
4. Enable **Stop run if an error occurs** for script/network errors if available.
   Assertion scripts also stop subsequent requests after a failed assertion.
5. Turn off **Keep variable values** / **Persist variables** in Runner if your
   version offers it. Runtime variables remain available during the run; this
   avoids retaining captured cookies afterward. Start the run and inspect each
   assertion in the Runner results. Stop and fix
   any failure; do not count skipped or unexecuted requests as passing.
6. Record the actual requests executed, assertion totals, failures, run date,
   local URL and any fixture/configuration issues. Save a Runner result export
   or screenshots supported by your Postman version as execution evidence.
   Remove cookies, passwords and account details before sharing evidence.

A complete successful execution must execute all 90 requests, reach
**90 - No cookie after logout is denied**, and have zero failed assertions or
script/network errors. The HTML login/register/logout endpoints legitimately
return 303 redirects; their assertions verify redirect and cookie outcomes
instead of attempting to parse nonexistent JSON bodies.
Individual **Send** requests do not execute the dependency chain; select the
complete collection in Runner. If a failure interrupts the chain, inspect the
created plan using the normal app. A Pending plan left by a failed run may need
normal Student cancellation before retrying. Start each retry from request 01;
never reuse stale dynamic IDs or tokens manually.

## Sequence and assertions

| Folder | Coverage |
| --- | --- |
| 01 | Health; no-cookie 401 on Student, Advisor and user-list APIs; malformed cookie; failed login; successful Student/Advisor cookie login; independent Student registration/login |
| 02 | Student denial from Advisor/user APIs; Advisor denial from Student APIs; admin user response allowlist; degree progress calculations/privacy; catalogue eligibility; dynamic course/semester discovery |
| 03 | Empty, duplicate, unknown, missing-prerequisite and incorrectly typed selections; invalid semester, malformed JSON and spoofed identity; read-back of unchanged history after invalid submissions; 201 submission and Location; persisted detail; cross-student GET/PUT/DELETE/list isolation; identical foreign/missing 404; pending conflicts; invalid path ID; every Advisor detail/action denied to Student; unchanged Pending plan after denials; course removal and last-course conflict |
| 04 | Shared Pending queue and Advisor detail; missing plan; invalid review data; exact feedback validation at 501 characters, positive 500-character boundary; spoofed reviewer and action overrides; read-back of unchanged/unassigned Pending plan after invalid reviews; generic review and all three dedicated decision URLs; trimmed feedback and reviewer attribution; queue removal; Student visibility; PUT and POST resubmission with same ID and cleared feedback/reviewer; rejection, approval and repeat-review conflicts |
| 05 | Approved cancellation; cancellation conflict; retained Student/Advisor history; cancelled review conflict; new plan ID after cancellation; Pending cancellation; final list/queue checks; logout cookie deletion and subsequent no-cookie 401 |

Assertions check exact expected status codes, JSON content types, error details
and domain error codes where applicable, cache prevention for personalized
advising responses, response allowlists, selected course IDs, statuses, saved
feedback and authenticated reviewer attribution. Negative cases must return
their expected 401/403/404/409/422; an arbitrary error is not a passing result.
Authorization errors check the exact detail; schema failures check the expected
field and validation type. Successful nested course and plan representations
check required fields and types. Advisor responses for the target plan check
the dynamically discovered Student ID as well as username. A fourth read-back
checkpoint confirms forbidden edits/reviews retained the Approved status and
feedback. The Postman collection cannot inspect database rows directly; these
checkpoints verify persisted API-visible state, complementing the existing
integration tests' independent database snapshots.

All implemented JSON API operations in [the API reference](../api.md), including
`GET /api/users`, appear in the collection. HTML UI workflows, simulated database
outages, concurrency races, token expiry, role changes and production database
behavior remain outside this sequential collection's scope. Logout deletes the
browser cookie; this application does not revoke already issued JWTs. The final
401 verifies absence of the deleted cookie, not server-side token revocation.

## Data retained after execution

A successful run adds one independent Student account and two Cancelled plans
belonging to the configured primary Student. Plan course rows and advisor
feedback remain as history by design. Existing active plans are not used as
test targets. Repeated runs retain additional history/accounts; there is no API
for deleting those records. Use a disposable local database for clean fixtures.

At the end, captured login-token variables and the generated isolation-account
password are cleared. Failed runs can leave
tokens and active plans in local state. Do not export populated variables as a
shared artifact. Record actual results only after executing this collection;
creation and static checks do not establish runtime success.

After collecting your results, stop this disposable server with **Ctrl+C** and
close its PowerShell terminal to discard the environment overrides. The unique
temporary database can be retained for failure investigation. No automatic
database deletion, production cleanup or record-reset operation is performed.

## Repeat the static artifact checks (optional)

From the project directory containing `manage.py`:

```powershell
node docs/assignment2/postman/validate_collection.cjs
```

This uses Node's standard library only and reads the collection and route source.
It does not execute requests, change a database, rerun pytest, or generate test
reports. Expected static counts: **90 requests, 93 scripts, 15 JSON API operations**.

For any new run, use the isolation and import instructions above and retain its own dated results. Existing Runner screenshots describe the recorded October 27 run; they do not prove a newly changed collection or application passed. Manual acceptance remains incomplete in the [UAT report](../reports/uat-final-report.md).
