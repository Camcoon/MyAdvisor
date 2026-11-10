"""Independent oracles for the owner-approved fictional degree allocation."""

import pytest

from app.demo_requirements import DEMO_REQUIREMENTS, DEMO_TOTAL_CREDITS
from app.models.advising import DegreeRequirement, StudentCourse

pytestmark = pytest.mark.unit


def test_approved_configuration_totals_exactly_93():
    assert dict(DEMO_REQUIREMENTS) == {
        "Core Courses": 36, "General Education": 18, "Electives": 12,
        "Major Requirements": 18, "Additional Requirements": 9,
    }
    assert len(DEMO_REQUIREMENTS) == len(dict(DEMO_REQUIREMENTS)) == 5
    assert sum(credits for _, credits in DEMO_REQUIREMENTS) == DEMO_TOTAL_CREDITS == 93


@pytest.mark.parametrize("duplicate", [False, True])
def test_approved_category_progress_counts_each_completed_course_once(advising, duplicate):
    # Explicit approved values, independent of the configuration under test.
    approved = [("Core Courses", 36), ("General Education", 18), ("Electives", 12),
                ("Major Requirements", 18), ("Additional Requirements", 9)]
    advising.repo.list_degree_requirements.return_value = [
        DegreeRequirement(id=20+i, program_id=10, category=category, required_credits=credits)
        for i, (category, credits) in enumerate(approved)
    ]
    records = [StudentCourse(student_id=1, course_id=cid, completion_status=status)
               for cid, status in [(101, "Completed"), (102, "Completed"), (103, "In Progress")]]
    if duplicate:
        records.append(StudentCourse(student_id=1, course_id=101, completion_status="Completed"))
    advising.repo.get_completed_courses.return_value = records
    result = advising.service.get_student_dashboard(1)
    assert [result[k] for k in ("completed_credits", "in_progress_credits", "remaining_credits",
                                "total_credits", "progress_percent")] == [6, 3, 84, 93, 6]
    assert result["category_progress"] == [
        {"category": "Core Courses", "earned": 3, "required": 36, "remaining": 33, "percent": 8},
        {"category": "General Education", "earned": 3, "required": 18, "remaining": 15, "percent": 17},
        {"category": "Electives", "earned": 0, "required": 12, "remaining": 12, "percent": 0},
        {"category": "Major Requirements", "earned": 0, "required": 18, "remaining": 18, "percent": 0},
        {"category": "Additional Requirements", "earned": 0, "required": 9, "remaining": 9, "percent": 0},
    ]
    assert sum(row["earned"] for row in result["category_progress"]) == result["completed_credits"]
