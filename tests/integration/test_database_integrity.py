"""IT-19/20 deliberately reach real database failures past service validation."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

pytestmark = pytest.mark.integration


@pytest.mark.it("IT-19")
@pytest.mark.parametrize("violation", ["duplicate-plan-course", "duplicate-student-course", "foreign-key"])
def test_database_constraints_preserve_committed_records(student_env, violation):
    from app.models.advising import PlanCourse, StudentCourse

    env = student_env
    plan_id = env.seed_plan(courses=("c3",))
    before = env.snapshot()
    with Session(env.engine) as session:
        if violation == "duplicate-student-course":
            row = StudentCourse(student_id=env.ids["s1"], course_id=env.ids["c1"])
        else:
            row = PlanCourse(
                plan_id=plan_id,
                course_id=999999 if violation == "foreign-key" else env.ids["c3"],
            )
        session.add(row)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
        assert session.get(PlanCourse, before["plancourse"][0]["id"]) is not None
    assert env.snapshot() == before


@pytest.mark.it("IT-20")
@pytest.mark.parametrize("operation", ["create", "resubmit"])
def test_failed_plan_transaction_rolls_back_all_changes_and_session_is_reusable(
    student_env, operation
):
    from app.models.advising import SemesterPlan
    from app.repositories.advising import AdvisingRepository

    env = student_env
    plan_id = env.seed_plan(status="Rejected", courses=("c3",)) if operation == "resubmit" else None
    before = env.snapshot()
    with Session(env.engine) as session:
        repo = AdvisingRepository(session)
        with pytest.raises(IntegrityError):
            if operation == "create":
                repo.create_plan(
                    env.ids["s1"], [env.ids["c4"], env.ids["c4"]],
                    semester_name="Year 1 semester 1",
                )
            else:
                repo.resubmit_plan(
                    session.get(SemesterPlan, plan_id), [env.ids["c4"], env.ids["c4"]]
                )
        # The repository must have rolled back, without a test-side rollback.
        assert env.snapshot() == before
        assert session.is_active
        # A successful write through the SAME session proves transaction recovery.
        recovered = repo.create_plan(
            env.ids["s1"], [env.ids["c4"]], semester_name="Year 1 semester 2"
        )
        recovered_id = recovered.id
    after = env.snapshot()
    assert len(after["semesterplan"]) == len(before["semesterplan"]) + 1
    assert len(after["plancourse"]) == len(before["plancourse"]) + 1
    assert env.courses(recovered_id) == [env.ids["c4"]]
    if plan_id is not None:
        assert env.plan(plan_id) == before["semesterplan"][0]
        assert env.courses(plan_id) == [env.ids["c3"]]
