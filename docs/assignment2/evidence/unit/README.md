# Unit execution evidence

Run started: 26 October 2026, 22:38:26 UTC−04:00 (America/La_Paz).
Baseline HEAD: `679b9250c13f38a2f97ed4e6d08a325fe48219d3`, with existing local changes and the unit implementation uncommitted. This SHA identifies the base, not a committed snapshot of the tested working tree.

Command, from the repository root (the directory containing `pyproject.toml`):

```text
python -m pytest -m unit -v -p no:cacheprovider --junitxml=docs/assignment2/evidence/unit/results.xml
```

Result: **113 passed, 408 deselected, 1 warning in 1.98s**, exit code 0.
JUnit records 113 tests, 0 failures, 0 errors, 0 skips. The warning is an existing Starlette TestClient dependency deprecation during collection. No integration test bodies were run.

Artifacts: [verbose per-variant results](pytest-output.txt), [JUnit XML](results.xml), [updated plan](../../test-plans/unit-test-plan.md). The verbose results retain every selected node ID and its actual outcome. All expected assertions passed, with no failure tracebacks. UT identifiers appear in function names (`test_UT_01_…` through `test_UT_23_…`), and each parameterized variant has a separate node/result. The retained E12 login-routing test is a UT-20 companion.

Environment:

| Component | Version |
|---|---|
| Platform | Windows, win32 |
| Python | 3.14.0 |
| pytest | 9.1.1 |
| pytest-asyncio | 1.4.0 |
| SQLModel | 0.0.42 |
| FastAPI | 0.141.1 |
| PyJWT | 2.14.0 |
| pwdlib | 0.3.1 |

Isolation: in-memory SQLModel objects, autospecced repository doubles and a nonfunctional session; unit fixtures fail on SQLAlchemy connection attempts. Auth orchestration patches collaborators where imported. Cryptography tests use real local hashing/signing with test-only values and a fixed JWT clock. No production database, running server, network, or persistence assertions are used.

Existing coverage was inspected before adding tests. SQLite service/API, migration and template tests remain intact and deselected. The existing mocked direct login test retains its assertions and now uses the registered `unit` marker. No application changes or defect fixes were needed. UT-22 documents the current role-denial contract (403); authentication failures remain 401. Database reset/commit behavior and cookie delivery remain integration concerns.

Default discovery is scoped to `tests/` to exclude the nested historical checkout. The unit marker is registered in `pyproject.toml`. The cache provider was disabled because the workspace's existing `.pytest_cache` directory is inaccessible; this does not alter test selection or assertions.
