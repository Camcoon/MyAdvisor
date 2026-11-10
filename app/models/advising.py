from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class DegreeProgram(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    total_credits: int = 93


class DegreeRequirement(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("program_id", "category"),)

    id: int | None = Field(default=None, primary_key=True)
    program_id: int = Field(foreign_key="degreeprogram.id", index=True)
    category: str
    required_credits: int


class Course(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    title: str
    credits: int = 3
    prerequisite_text: str = Field(default="")
    category: str = Field(default="Core Courses")
    department: str = Field(default="Computer Science")


class StudentCourse(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("student_id", "course_id"),)

    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.id", index=True)
    course_id: int = Field(foreign_key="course.id", index=True)
    completion_status: str = Field(default="Completed")
    grade: str = Field(default="A")
    completed_at: datetime | None = None


class SemesterPlan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.id", index=True)
    advisor_id: int | None = Field(default=None, foreign_key="user.id")
    semester_name: str = Field(default="Year 1 semester 1")
    status: str = Field(default="Pending")
    advisor_feedback: str = Field(default="")
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PlanCourse(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("plan_id", "course_id"),)

    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="semesterplan.id", index=True)
    course_id: int = Field(foreign_key="course.id", index=True)
