"""F2: real auth and request sessions; no startup seeding or external database IO."""

from contextlib import ExitStack, asynccontextmanager
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from pwdlib import PasswordHash
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

PASSWORD = "student-integration-password"
T1 = "Year 1 semester 1"
OLD_SUBMISSION = datetime(2020, 1, 1, tzinfo=timezone.utc)


@pytest.fixture(scope="session")
def student_password_hash():
    # Real Argon2, once per run; never import the app before isolation is installed.
    return PasswordHash.recommended().hash(PASSWORD)


class StudentEnvironment:
    def __init__(self, app, engine, stack, ids, models):
        self.app = app
        self.engine = engine
        self.stack = stack
        self.ids = ids
        self.models = models

    def client(self):
        # Enter the patched lifespan and close every cookie jar before teardown.
        return self.stack.enter_context(TestClient(self.app, follow_redirects=False))

    def login(self, actor="s1"):
        client = self.client()
        response = client.post("/login", data={"username": actor, "password": PASSWORD})
        assert response.status_code == 303
        assert response.headers["location"].endswith("/app")
        assert "access_token" in client.cookies
        return client

    def snapshot(self):
        """Read all tables through a fresh identity map, including auth/seed data."""
        with Session(self.engine) as session:
            return {
                model.__tablename__: [
                    row.model_dump()
                    for row in session.exec(select(model).order_by(model.id)).all()
                ]
                for model in self.models
            }

    def seed_plan(self, status="Pending", actor="s1", courses=("c3", "c4")):
        from app.models.advising import PlanCourse, SemesterPlan

        with Session(self.engine) as session:
            plan = SemesterPlan(
                student_id=self.ids[actor],
                semester_name=T1,
                status=status,
                advisor_id=self.ids["a1"],
                advisor_feedback=f"Private feedback for {actor}",
                submitted_at=OLD_SUBMISSION,
            )
            session.add(plan)
            session.flush()
            plan_id = plan.id
            session.add_all(
                PlanCourse(plan_id=plan_id, course_id=self.ids[key]) for key in courses
            )
            session.commit()
            return plan_id

    def plan(self, plan_id):
        state = self.snapshot()
        return next(row for row in state["semesterplan"] if row["id"] == plan_id)

    def courses(self, plan_id):
        return sorted(
            row["course_id"]
            for row in self.snapshot()["plancourse"]
            if row["plan_id"] == plan_id
        )


@pytest.fixture
def student_env(monkeypatch, tmp_path, student_password_hash):
    clear_settings_after = False
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def foreign_keys(connection, _record):
        connection.execute("PRAGMA foreign_keys=ON")

    try:
        with monkeypatch.context() as patches:
            # Fail before connecting, even if startup/recovery uses a stale engine.
            for method_name in ("connect", "raw_connection"):
                original = getattr(Engine, method_name)

                def guarded(bind, *args, _original=original, **kwargs):
                    assert bind is engine, (
                        "Student tests may only connect to their isolated engine"
                    )
                    return _original(bind, *args, **kwargs)

                patches.setattr(Engine, method_name, guarded)

            # Set environment AND cached settings before importing app/database.
            # The app's bootstrap engine is lazy and is never allowed to connect.
            bootstrap_uri = f"sqlite:///{(tmp_path / 'unused-bootstrap.db').as_posix()}"
            test_settings = {
                "database_uri": bootstrap_uri,
                "secret_key": "student-integration-only-signing-key-32-bytes",
                "env": "integration",
                "jwt_algorithm": "HS256",
                "jwt_access_token_expires": 30,
            }
            for key, value in test_settings.items():
                patches.setenv(key.upper(), str(value))
            from app.config import get_settings

            clear_settings_after = get_settings.cache_info().currsize == 0
            settings = get_settings()
            for key, value in test_settings.items():
                patches.setattr(settings, key, value)

            from app import database
            from app.main import app
            from app.models.advising import (
                Course,
                DegreeProgram,
                DegreeRequirement,
                PlanCourse,
                SemesterPlan,
                StudentCourse,
            )
            from app.models.user import User

            patches.setattr(database, "engine", engine)
            SQLModel.metadata.create_all(engine)
            ids = {}
            with Session(engine) as session:
                program = DegreeProgram(name="Computer Science", total_credits=93)
                session.add(program)
                session.flush()
                ids["program"] = program.id
                session.add(
                    DegreeRequirement(
                        program_id=program.id,
                        category="Core Courses",
                        required_credits=30,
                    )
                )
                for actor, role in (
                    ("s1", "regular_user"),
                    ("s2", "regular_user"),
                    ("a1", "admin"),
                ):
                    user = User(
                        username=actor,
                        email=f"{actor}@example.com",
                        password=student_password_hash,
                        role=role,
                        name=f"Private profile {actor}",
                        student_number=f"TEST-{actor}",
                        degree_program=program.id,
                    )
                    session.add(user)
                    session.flush()
                    ids[actor] = user.id
                for key, code, category, prerequisites in (
                    ("c1", "COMP 1100", "Core Courses", ""),
                    ("c2", "MATH 1000", "General Education", ""),
                    ("c3", "COMP 2000", "Core Courses", "COMP 1100"),
                    ("c4", "MATH 2000", "Electives", ""),
                    ("c5", "COMP 3000", "Electives", "COMP 1100, MATH 9999"),
                ):
                    course = Course(
                        code=code,
                        title=f"Course {code}",
                        credits=3,
                        category=category,
                        prerequisite_text=prerequisites,
                    )
                    session.add(course)
                    session.flush()
                    ids[key] = course.id
                session.add_all(
                    [
                        StudentCourse(
                            student_id=ids["s1"],
                            course_id=ids["c1"],
                            completion_status="Completed",
                            grade="A",
                            completed_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
                        ),
                        StudentCourse(
                            student_id=ids["s1"],
                            course_id=ids["c2"],
                            completion_status="In Progress",
                            grade="",
                        ),
                        StudentCourse(
                            student_id=ids["s2"],
                            course_id=ids["c4"],
                            completion_status="Completed",
                            grade="B",
                            completed_at=datetime(2023, 2, 1, tzinfo=timezone.utc),
                        ),
                    ]
                )
                session.commit()

            def isolated_session():
                with Session(engine) as session:
                    yield session

            @asynccontextmanager
            async def isolated_lifespan(_app):
                # No demo initializer. Recovery still uses database.engine above.
                assert database.engine is engine
                yield

            # Restore the original mapping object and lifespan even after failure.
            patches.setattr(
                app, "dependency_overrides", {database.get_session: isolated_session}
            )
            patches.setattr(app.router, "lifespan_context", isolated_lifespan)
            with ExitStack() as stack:
                env = StudentEnvironment(
                    app,
                    engine,
                    stack,
                    ids,
                    (
                        User,
                        DegreeProgram,
                        DegreeRequirement,
                        Course,
                        StudentCourse,
                        SemesterPlan,
                        PlanCourse,
                    ),
                )
                assert env.snapshot()["semesterplan"] == []
                assert env.snapshot()["plancourse"] == []
                yield env
                assert not (tmp_path / "unused-bootstrap.db").exists()
    finally:
        engine.dispose()
        # If this fixture first populated the cache, restore its empty state.
        # Existing cached settings have their original fields restored by patches.
        if clear_settings_after:
            get_settings.cache_clear()


@pytest.fixture
def student(student_env):
    return SimpleNamespace(env=student_env, client=student_env.login())
