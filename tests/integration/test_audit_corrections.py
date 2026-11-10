"""Focused regressions for verified final-audit defects; real auth and F2 DB."""

from urllib.parse import urlencode

import pytest
from sqlmodel import Session

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("role", ["admin", "unrecognized-role"])
@pytest.mark.parametrize("owner", ["s1", "a1"], ids=["student-plan", "legacy-advisor-plan"])
@pytest.mark.parametrize("operation", ["submit", "remove", "cancel"])
def test_nonstudent_html_mutations_are_forbidden_without_writes(
    student_env, role, owner, operation
):
    """An authentic Advisor cookie cannot become a Student form credential.

    Include legacy wrong-role-owned plans: ownership alone previously permitted
    removal/cancellation, just as AuthDep permitted Advisor-owned creation.
    Changing the DB role after login also checks that the cookie role is ignored.
    """
    from app.models.user import User

    env = student_env
    client = env.login("a1")
    plan_id = env.seed_plan(actor=owner)
    if role != "admin":
        with Session(env.engine) as session:
            account = session.get(User, env.ids["a1"])
            account.role = role
            session.add(account)
            session.commit()
    before = env.snapshot()
    if operation == "submit":
        response = client.post(
            "/app/plan",
            content=urlencode({
                "course_ids": env.ids["c4"],
                "semester_name": "Year 1 semester 2",
            }),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    elif operation == "remove":
        response = client.post(f"/app/plan/{plan_id}/courses/{env.ids['c4']}/remove")
    else:
        response = client.post(f"/app/plan/{plan_id}/cancel")
    assert response.status_code == 403
    assert response.json() == {"detail": "You are not authorized to access this resource"}
    assert env.snapshot() == before


@pytest.mark.parametrize("email", ["not-an-email", "student@", "<invalid>"])
def test_invalid_registration_email_is_controlled_and_does_not_write(student_env, email):
    env = student_env
    before = env.snapshot()
    response = env.client().post("/register", data={
        "username": "invalid-email-student",
        "email": email,
        "password": "local-regression-only-password",
        "name": "Registration validation test",
        "student_number": "REG-INVALID",
    })
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(error["loc"] == ["body", "email"] for error in detail)
    assert env.snapshot() == before


def test_valid_registration_still_creates_a_student_and_handles_duplicates(student_env):
    from app.models.user import User

    env = student_env
    client = env.client()
    data = {
        "username": "registration-regression",
        "email": "registration-regression@example.com",
        "password": "local-regression-only-password",
        "name": "New Student",
        "student_number": "REG-VALID",
    }
    response = client.post("/register", data=data)
    assert response.status_code == 303
    assert response.headers["location"].endswith("/login")
    with Session(env.engine) as session:
        from sqlmodel import select
        account = session.exec(select(User).where(User.username == data["username"])).one()
        assert account.role == "regular_user"
        assert account.email == data["email"]
        assert account.student_number == "REG-VALID"
        assert account.degree_program is not None
    before_duplicate = env.snapshot()
    duplicate = client.post("/register", data=data)
    assert duplicate.status_code == 303
    assert duplicate.headers["location"].endswith("/register")
    assert env.snapshot() == before_duplicate


@pytest.mark.parametrize("missing_reference", ["plan", "course"])
def test_application_engine_enforces_foreign_keys_and_retains_valid_links(
    tmp_path, monkeypatch, missing_reference
):
    """Use the real application engine factory, not the F2 FK-on fixture."""
    from sqlalchemy.exc import IntegrityError
    from sqlmodel import select

    from app import database
    from app.models.advising import Course, DegreeProgram, PlanCourse, SemesterPlan
    from app.models.user import User

    engine = database.create_app_engine(
        "sqlite:///" + (tmp_path / "runtime-fk.sqlite3").as_posix(),
        pool_size=2, max_overflow=1,
    )
    try:
        monkeypatch.setattr(database, "engine", engine)
        database.create_db_and_tables()
        # Two simultaneous leases force two distinct underlying connections.
        with engine.connect() as first, engine.connect() as second:
            assert first.connection.driver_connection is not second.connection.driver_connection
            assert first.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
            assert second.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
        with Session(engine) as session:
            program = DegreeProgram(name="Foreign-key regression program")
            session.add(program)
            session.flush()
            account = User(
                username="fk-student", email="fk-student@example.com",
                password="unused-test-hash", role="regular_user", degree_program=program.id,
            )
            course = Course(code="FK 1000", title="Foreign-key regression course")
            session.add_all([account, course])
            session.flush()
            plan = SemesterPlan(student_id=account.id)
            session.add(plan)
            session.flush()
            valid = PlanCourse(plan_id=plan.id, course_id=course.id)
            session.add(valid)
            session.commit()
            plan_id, course_id, link_id = plan.id, course.id, valid.id
        with Session(engine) as session:
            session.add(PlanCourse(
                plan_id=999999 if missing_reference == "plan" else plan_id,
                course_id=999999 if missing_reference == "course" else course_id,
            ))
            with pytest.raises(IntegrityError):
                session.commit()
            session.rollback()
        with Session(engine) as session:
            links = session.exec(select(PlanCourse)).all()
            assert [(link.id, link.plan_id, link.course_id) for link in links] == [
                (link_id, plan_id, course_id)
            ]
        engine.dispose()
        # Recreated pool connections must also receive the runtime policy.
        with engine.connect() as connection:
            assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
    finally:
        engine.dispose()
