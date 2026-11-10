"""Database table models.

Import every table model here so ``SQLModel.metadata.create_all`` sees them.
"""

from app.models.advising import (
    Course,
    DegreeProgram,
    DegreeRequirement,
    PlanCourse,
    SemesterPlan,
    StudentCourse,
)
from app.models.user import User

__all__ = [
    "Course",
    "DegreeProgram",
    "DegreeRequirement",
    "PlanCourse",
    "SemesterPlan",
    "StudentCourse",
    "User",
]
