"""F1 fixtures: real in-memory models, autospecced repositories, no persistence."""
from types import SimpleNamespace
from unittest.mock import create_autospec

import pytest
from sqlalchemy.engine import Engine

from app.models.advising import Course, DegreeProgram, DegreeRequirement, StudentCourse
from app.models.user import User
from app.repositories.advising import AdvisingRepository
from app.repositories.user import UserRepository
from app.services import advising_service


@pytest.fixture(autouse=True)
def forbid_database_connections(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unit tests must not open database connections")
    monkeypatch.setattr(Engine, "connect", forbidden)


@pytest.fixture
def student():
    return User(id=1, username="student", email="student@example.com",
                password="stored-hash", role="regular_user", degree_program=10)


@pytest.fixture
def advising(monkeypatch, student):
    repo = create_autospec(AdvisingRepository, instance=True, spec_set=True)
    users = create_autospec(UserRepository, instance=True, spec_set=True)
    monkeypatch.setattr(advising_service, "AdvisingRepository", lambda db: repo)
    monkeypatch.setattr(advising_service, "UserRepository", lambda db: users)
    service = advising_service.AdvisingService(object())  # No usable session.
    courses = [
        Course(id=101, code="COMP 1100", title="Programming I"),
        Course(id=102, code="MATH 1000", title="Mathematics I", category="General Education"),
        Course(id=103, code="COMP 2000", title="Programming II", prerequisite_text="COMP 1100"),
        Course(id=104, code="MATH 2000", title="Mathematics II", category="Electives"),
        Course(id=105, code="COMP 3000", title="Advanced Computing",
               prerequisite_text="COMP 1100, MATH 9999"),
    ]
    repo.list_courses.return_value = courses
    repo.get_course_by_id.side_effect = lambda cid: next((c for c in courses if c.id == cid), None)
    repo.get_completed_courses.return_value = [
        StudentCourse(id=1, student_id=1, course_id=101, completion_status="Completed", grade="A"),
        StudentCourse(id=2, student_id=1, course_id=102, completion_status="In Progress"),
    ]
    repo.get_completed_course_ids.return_value = {101}
    repo.get_degree_program.return_value = DegreeProgram(id=10, name="Computer Science", total_credits=93)
    repo.list_degree_requirements.return_value = [
        DegreeRequirement(id=20, program_id=10, category="Core Courses", required_credits=30)
    ]
    repo.list_student_plans.return_value = []
    repo.get_plan_for_student.return_value = None
    repo.get_plan_courses.return_value = []
    users.get_by_id.return_value = student
    return SimpleNamespace(service=service, repo=repo, users=users, courses=courses)
