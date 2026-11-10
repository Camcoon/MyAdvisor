from collections.abc import Sequence
from datetime import datetime, timezone

from sqlmodel import Session, select, update

from app.models.advising import (
    Course,
    DegreeProgram,
    DegreeRequirement,
    PlanCourse,
    SemesterPlan,
    StudentCourse,
)


class AdvisingRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_courses(self) -> list[Course]:
        return self.db.exec(select(Course).order_by(Course.code)).all()

    def get_course_by_id(self, course_id: int) -> Course | None:
        return self.db.get(Course, course_id)

    def get_degree_program(self, program_id: int | None) -> DegreeProgram | None:
        if program_id is None:
            return None
        return self.db.get(DegreeProgram, program_id)

    def get_degree_program_by_name(self, name: str) -> DegreeProgram | None:
        return self.db.exec(
            select(DegreeProgram).where(DegreeProgram.name == name)
        ).first()

    def list_degree_requirements(self, program_id: int) -> list[DegreeRequirement]:
        return self.db.exec(
            select(DegreeRequirement)
            .where(DegreeRequirement.program_id == program_id)
            .order_by(DegreeRequirement.id)
        ).all()

    def save_degree_requirements(self, requirements: Sequence[DegreeRequirement]) -> None:
        """Persist only requirement rows, atomically, without reseeding other tables."""
        try:
            self.db.add_all(requirements)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def get_completed_courses(self, student_id: int) -> list[StudentCourse]:
        return self.db.exec(
            select(StudentCourse)
            .where(StudentCourse.student_id == student_id)
            .order_by(StudentCourse.completed_at.desc(), StudentCourse.id.desc())
        ).all()

    def get_completed_course_ids(self, student_id: int) -> set[int]:
        return {
            item.course_id
            for item in self.get_completed_courses(student_id)
            if item.completion_status.lower() == "completed"
        }

    def get_plan_for_student(
        self,
        student_id: int,
        semester_name: str | None = None,
    ) -> SemesterPlan | None:
        statement = select(SemesterPlan).where(SemesterPlan.student_id == student_id)
        if semester_name is not None:
            statement = statement.where(SemesterPlan.semester_name == semester_name)
        return self.db.exec(
            statement.order_by(SemesterPlan.id.desc()).limit(1)
        ).first()

    def list_student_plans(self, student_id: int) -> list[SemesterPlan]:
        return self.db.exec(
            select(SemesterPlan)
            .where(SemesterPlan.student_id == student_id)
            .order_by(SemesterPlan.submitted_at.desc(), SemesterPlan.id.desc())
        ).all()

    def list_all_plans(self) -> list[SemesterPlan]:
        return self.db.exec(
            select(SemesterPlan).order_by(
                SemesterPlan.submitted_at.desc(),
                SemesterPlan.id.desc(),
            )
        ).all()

    def get_plan_courses(self, plan_id: int) -> list[PlanCourse]:
        return self.db.exec(
            select(PlanCourse).where(PlanCourse.plan_id == plan_id).order_by(PlanCourse.id)
        ).all()

    def remove_plan_course(self, plan_course: PlanCourse) -> None:
        self.db.delete(plan_course)
        self.db.commit()

    def cancel_plan(self, plan: SemesterPlan) -> SemesterPlan:
        plan.status = "Cancelled"
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def create_plan(
        self,
        student_id: int,
        course_ids: Sequence[int],
        *,
        semester_name: str,
    ) -> SemesterPlan:
        plan = SemesterPlan(
            student_id=student_id,
            semester_name=semester_name,
            status="Pending",
        )
        try:
            self.db.add(plan)
            self.db.flush()
            self.db.add_all(
                PlanCourse(plan_id=plan.id, course_id=course_id)
                for course_id in course_ids
            )
            self.db.commit()
            self.db.refresh(plan)
            return plan
        except Exception:
            self.db.rollback()
            raise

    def resubmit_plan(
        self,
        plan: SemesterPlan,
        course_ids: Sequence[int],
    ) -> SemesterPlan:
        try:
            for plan_course in self.get_plan_courses(plan.id):
                self.db.delete(plan_course)
            self.db.flush()
            self.db.add_all(
                PlanCourse(plan_id=plan.id, course_id=course_id)
                for course_id in course_ids
            )
            plan.status = "Pending"
            plan.advisor_id = None
            plan.advisor_feedback = ""
            plan.submitted_at = datetime.now(timezone.utc)
            self.db.add(plan)
            self.db.commit()
            self.db.refresh(plan)
            return plan
        except Exception:
            self.db.rollback()
            raise

    def update_plan(
        self,
        plan: SemesterPlan,
        *,
        status: str,
        feedback: str,
        advisor_id: int,
        expected_status: str,
    ) -> SemesterPlan | None:
        """Save a review only if the persisted status still matches the read."""
        try:
            result = self.db.execute(
                update(SemesterPlan)
                .where(
                    SemesterPlan.id == plan.id,
                    SemesterPlan.status == expected_status,
                )
                .values(status=status, advisor_feedback=feedback, advisor_id=advisor_id)
                .execution_options(synchronize_session=False)
            )
            if result.rowcount != 1:
                self.db.rollback()
                return None
            self.db.commit()
            self.db.refresh(plan)
            return plan
        except Exception:
            self.db.rollback()
            raise

    def list_pending_plans(self) -> list[SemesterPlan]:
        return self.db.exec(
            select(SemesterPlan)
            .where(SemesterPlan.status == "Pending")
            .order_by(SemesterPlan.submitted_at, SemesterPlan.id)
        ).all()

    def get_plan_by_id(self, plan_id: int) -> SemesterPlan | None:
        return self.db.get(SemesterPlan, plan_id)
