"""Seed/migration regressions preserve academic and advising history."""

import sqlite3

import pytest
from sqlmodel import Session, select

from app.models.advising import DegreeProgram, DegreeRequirement
from app.services.advising_service import AdvisingService

pytestmark = pytest.mark.integration
APPROVED = {"Core Courses": 36, "General Education": 18, "Electives": 12,
            "Major Requirements": 18, "Additional Requirements": 9}
LEGACY = {"Core Courses": 36, "General Education": 18, "Electives": 18,
          "Major Requirements": 24, "Additional Requirements": 24}


def legacy_requirements(env):
    with Session(env.engine) as session:
        core = session.exec(select(DegreeRequirement)).one()
        core.required_credits = 36
        session.add(core)
        session.add_all(DegreeRequirement(program_id=env.ids["program"], category=category,
                                          required_credits=credits)
                        for category, credits in LEGACY.items() if category != "Core Courses")
        session.commit()


@pytest.mark.parametrize("status", ["Pending", "Approved", "Rejected", "Changes Requested", "Cancelled"])
def test_existing_allocation_migrates_without_touching_history(student_env, status):
    env = student_env
    legacy_requirements(env)
    env.seed_plan(status=status)
    before = env.snapshot()
    with Session(env.engine) as session:
        service = AdvisingService(session)
        preview = service.sync_demo_requirements()
        assert sum(item["changed"] for item in preview) == 3
        assert env.snapshot() == before
        service.sync_demo_requirements(apply=True)
    after = env.snapshot()
    assert {name: rows for name, rows in before.items() if name != "degreerequirement"} == {
        name: rows for name, rows in after.items() if name != "degreerequirement"
    }
    assert [(r["id"], r["program_id"], r["category"]) for r in before["degreerequirement"]] == [
        (r["id"], r["program_id"], r["category"]) for r in after["degreerequirement"]
    ]
    assert {r["category"]: r["required_credits"] for r in after["degreerequirement"]} == APPROVED
    with Session(env.engine) as session:
        assert not any(item["changed"] for item in AdvisingService(session).sync_demo_requirements(apply=True))
    assert env.snapshot() == after
    response = env.login().get("/api/degree-progress")
    assert response.status_code == 200
    data = response.json()
    assert (data["completed_credits"], data["in_progress_credits"], data["remaining_credits"], data["total_credits"]) == (3, 3, 87, 93)
    assert {r["category"]: r["required"] for r in data["category_progress"]} == APPROVED
    assert next(r for r in data["category_progress"] if r["category"] == "Core Courses")["percent"] == 8


@pytest.mark.parametrize("variant", ["custom-credits", "extra-category", "custom-total", "missing-program"])
def test_unfamiliar_degree_data_is_rejected_without_writes(student_env, variant):
    env = student_env
    legacy_requirements(env)
    with Session(env.engine) as session:
        if variant == "custom-credits":
            row = session.exec(select(DegreeRequirement).where(DegreeRequirement.category == "Electives")).one()
            row.required_credits = 15
        elif variant == "extra-category":
            row = DegreeRequirement(program_id=env.ids["program"], category="Custom Category", required_credits=3)
        else:
            row = session.get(DegreeProgram, env.ids["program"])
            if variant == "custom-total":
                row.total_credits = 120
            else:
                row.name = "Independent Programme"
        session.add(row)
        session.commit()
    before = env.snapshot()
    with Session(env.engine) as session, pytest.raises(ValueError):
        AdvisingService(session).sync_demo_requirements(apply=True)
    assert env.snapshot() == before


def test_fresh_demo_seed_and_authenticated_progress_use_approved_requirements(student_env, student_password_hash):
    from app.models.user import User

    env = student_env
    # Preserve the independent Core=30 fixture; create the actual demo alongside it.
    with Session(env.engine) as session:
        old_program = session.get(DegreeProgram, env.ids["program"])
        old_program.name = "Independent Test Programme"
        bob = User(username="bob", email="bob@example.com", password=student_password_hash,
                   role="regular_user")
        session.add_all([old_program, bob])
        session.commit()
        AdvisingService(session).ensure_demo_data()
        bob_id = bob.id
    before = env.snapshot()
    with Session(env.engine) as session:
        AdvisingService(session).ensure_demo_data()
        bob = session.get(User, bob_id)
        rows = session.exec(select(DegreeRequirement).where(DegreeRequirement.program_id == bob.degree_program)).all()
        assert {r.category: r.required_credits for r in rows} == APPROVED
        assert sum(r.required_credits for r in rows) == 93
    assert env.snapshot() == before
    client = env.login("bob")
    response = client.get("/api/degree-progress")
    assert response.status_code == 200
    data = response.json()
    assert [data[k] for k in ("completed_credits", "in_progress_credits", "remaining_credits", "total_credits", "progress_percent")] == [6, 3, 84, 93, 6]
    assert sum(row["earned"] for row in data["category_progress"]) == 6
    assert {r["category"]: (r["earned"], r["remaining"], r["percent"]) for r in data["category_progress"]} == {
        "Core Courses": (3, 33, 8), "General Education": (3, 15, 17),
        "Electives": (0, 12, 0), "Major Requirements": (0, 18, 0), "Additional Requirements": (0, 9, 0),
    }
    html = client.get("/app?tab=degree-progress")
    assert html.status_code == 200
    assert "not official UWI programme requirements" in html.text
    catalogue = client.get("/api/courses").json()
    assert next(course for course in catalogue if course["code"] == "COMP 1201")["eligible"] is True


def test_sqlite_backup_retains_committed_wal_data_and_refuses_missing_source(tmp_path):
    from app.demo_migration import backup_sqlite_database

    source = tmp_path / "existing.sqlite3"
    with sqlite3.connect(source) as connection:
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("CREATE TABLE preserved (id INTEGER PRIMARY KEY, detail TEXT)")
        connection.execute("INSERT INTO preserved VALUES (1, 'decision-history')")
        connection.commit()
        backup = backup_sqlite_database("sqlite:///" + source.as_posix(), tmp_path / "backups")
        with sqlite3.connect(backup) as copied:
            assert copied.execute("SELECT * FROM preserved").fetchall() == [(1, "decision-history")]
    missing = tmp_path / "missing.sqlite3"
    with pytest.raises(ValueError, match="refusing to create"):
        backup_sqlite_database("sqlite:///" + missing.as_posix(), tmp_path / "backups")
    assert not missing.exists()


@pytest.mark.parametrize("fail_backup", [False, True])
def test_backed_up_migration_preserves_existing_file_database(tmp_path, monkeypatch, fail_backup):
    from sqlmodel import SQLModel, create_engine

    from app import demo_migration
    from app.models.advising import Course, PlanCourse, SemesterPlan, StudentCourse
    from app.models.user import User

    path = tmp_path / "existing-demo.sqlite3"
    uri = "sqlite:///" + path.as_posix()
    engine = create_engine(uri)
    SQLModel.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            program = DegreeProgram(name="Computer Science", total_credits=93)
            session.add(program)
            session.flush()
            student = User(username="preserved", email="preserved@example.com", password="existing-hash",
                           role="regular_user", degree_program=program.id)
            advisor = User(username="reviewer", email="reviewer@example.com", password="existing-hash", role="admin")
            course = Course(code="KEEP 1000", title="Keep the custom catalogue", category="Core Courses")
            session.add_all([student, advisor, course])
            session.flush()
            plan = SemesterPlan(student_id=student.id, advisor_id=advisor.id, status="Approved",
                                advisor_feedback="Keep this actual decision")
            session.add(plan)
            session.flush()
            session.add_all([
                PlanCourse(plan_id=plan.id, course_id=course.id),
                StudentCourse(student_id=student.id, course_id=course.id, completion_status="Completed"),
                *(DegreeRequirement(program_id=program.id, category=c, required_credits=n)
                  for c, n in LEGACY.items()),
            ])
            session.commit()
            before = demo_migration.table_fingerprints(session)
            preview = demo_migration.migrate_demo_requirements(session, uri, tmp_path / "backups", apply=False)
            assert preview["applied"] is False
            assert not (tmp_path / "backups").exists()
            if fail_backup:
                def unavailable(*args, **kwargs):
                    raise OSError("Backup unavailable")
                monkeypatch.setattr(demo_migration, "backup_sqlite_database", unavailable)
                with pytest.raises(OSError, match="Backup unavailable"):
                    demo_migration.migrate_demo_requirements(session, uri, tmp_path / "backups", apply=True)
                assert demo_migration.table_fingerprints(session) == before
            else:
                result = demo_migration.migrate_demo_requirements(session, uri, tmp_path / "backups", apply=True)
                assert result["applied"] is True and result["other_tables_unchanged"] is True
                assert result["before"] == before
                with sqlite3.connect(result["backup"]) as backup:
                    assert dict(backup.execute("SELECT category, required_credits FROM degreerequirement")) == LEGACY
                    assert backup.execute("SELECT advisor_feedback FROM semesterplan").fetchone()[0] == "Keep this actual decision"
                assert demo_migration.migrate_demo_requirements(session, uri, tmp_path / "backups", apply=True)["applied"] is False
    finally:
        engine.dispose()
