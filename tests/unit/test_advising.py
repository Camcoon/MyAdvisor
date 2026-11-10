"""Isolated implementation of planned UT-01 through UT-19.

Existing SQLite-backed scenarios in test_advising_service.py are retained;
these variants verify service decisions and repository delegation only.
"""
import pytest

from app.models.advising import PlanCourse, SemesterPlan, StudentCourse
from app.services.advising_service import SEMESTER_OPTIONS

pytestmark = pytest.mark.unit
T1 = "Year 1 semester 1"
STATUSES = ["Pending", "Approved", "Rejected", "Changes Requested", "Cancelled"]
DECISIONS = [("approve", "Approved"), ("reject", "Rejected"), ("request_changes", "Changes Requested")]


def plan(status="Pending", student_id=1):
    return SemesterPlan(id=50, student_id=student_id, semester_name=T1, status=status)


def no_submission(advising):
    advising.repo.create_plan.assert_not_called()
    advising.repo.resubmit_plan.assert_not_called()


def test_UT_01_degree_totals_and_category(advising):
    result = advising.service.get_student_dashboard(1, T1)
    assert tuple(result[k] for k in ("completed_credits", "in_progress_credits", "remaining_credits", "total_credits", "progress_percent")) == (3, 3, 87, 93, 3)
    assert result["category_progress"] == [dict(category="Core Courses", earned=3, required=30, remaining=27, percent=10)]


@pytest.mark.parametrize("has_program", [True, False], ids=["configured-program", "missing-program"])
def test_UT_02_empty_record(advising, has_program):
    advising.repo.get_completed_courses.return_value = []
    if not has_program:
        advising.repo.get_degree_program.return_value = None
    result = advising.service.get_student_dashboard(1)
    assert tuple(result[k] for k in ("completed_credits", "in_progress_credits", "remaining_credits", "total_credits", "progress_percent")) == (0, 0, 93, 93, 0)
    assert result["category_progress"] == ([dict(category="Core Courses", earned=0, required=30, remaining=30, percent=0)] if has_program else [])


@pytest.mark.parametrize("variant,total,required,completed,ongoing,remaining,percent,earned,category_percent", [
    ("over-credit", 6, 6, [101, 103, 105], [102], 0, 100, 9, 100),
    ("zero-total", 0, 30, [101], [], 0, 0, 3, 10),
    ("zero-category", 93, 0, [101], [], 90, 3, 3, 0),
    ("duplicate-record", 93, 30, [101, 101], [], 90, 3, 3, 10),
], ids=lambda value: value if isinstance(value, str) else None)
def test_UT_03_progress_boundaries(advising, variant, total, required, completed, ongoing, remaining, percent, earned, category_percent):
    advising.repo.get_degree_program.return_value.total_credits = total
    advising.repo.list_degree_requirements.return_value[0].required_credits = required
    advising.repo.get_completed_courses.return_value = [
        StudentCourse(student_id=1, course_id=cid, completion_status=status)
        for ids, status in [(completed, "Completed"), (ongoing, "In Progress")]
        for cid in ids
    ]
    result = advising.service.get_student_dashboard(1)
    assert result["completed_credits"] == earned
    assert result["in_progress_credits"] == len(ongoing) * 3
    assert result["remaining_credits"] == remaining
    assert result["progress_percent"] == percent
    assert result["category_progress"][0] == dict(category="Core Courses", earned=earned, required=required, remaining=max(required-earned, 0), percent=category_percent)


@pytest.mark.parametrize("target,prerequisites,completed", [
    (103, "COMP 1100", {101}), (104, "", {101}),
    (105, " COMP 1100, MATH 1000 ", {101, 102}),
    (105, " , COMP 1100, , ", {101}),
], ids=["single", "none", "multiple-padded", "blank-tokens"])
def test_UT_04_satisfied_prerequisites(advising, target, prerequisites, completed):
    advising.courses[target-101].prerequisite_text = prerequisites
    advising.repo.get_completed_course_ids.return_value = completed
    assert advising.service.prerequisite_ok(1, target) is True
    assert advising.service.get_course_availability(1)[target] == (True, "Eligible")


@pytest.mark.parametrize("prerequisites,missing", [
    ("MATH 1000", "MATH 1000"),
    ("COMP 1100, MATH 9999", "MATH 9999"),
    (" , COMP 1100, , MATH 9999, ", "MATH 9999"),
], ids=["in-progress", "unknown-code", "blank-tokens"])
def test_UT_05_missing_prerequisites(advising, prerequisites, missing):
    advising.courses[2].prerequisite_text = prerequisites
    assert advising.service.prerequisite_ok(1, 103) is False
    assert advising.service.get_course_availability(1)[103] == (False, f"Missing prerequisite(s): {missing}")


@pytest.mark.parametrize("target,reason", [(101, "Already completed"), (102, "Already in progress"), (999999, None)])
def test_UT_06_tracked_and_unknown_courses(advising, target, reason):
    assert advising.service.prerequisite_ok(1, target) is False
    availability = advising.service.get_course_availability(1)
    if reason is None:
        assert target not in availability
    else:
        assert availability[target] == (False, reason)


@pytest.mark.parametrize("semester", [f"Year {y} semester {s}" for y in (1, 2, 3) for s in (1, 2, 3)] + [f"  {T1}  "])
def test_UT_07_semesters(advising, semester):
    assert SEMESTER_OPTIONS == ("Year 1 semester 1", "Year 1 semester 2", "Year 1 semester 3", "Year 2 semester 1", "Year 2 semester 2", "Year 2 semester 3", "Year 3 semester 1", "Year 3 semester 2", "Year 3 semester 3")
    assert advising.service.submit_plan(1, [103], semester) is advising.repo.create_plan.return_value
    advising.repo.create_plan.assert_called_once_with(1, [103], semester_name=semester.strip())
    advising.repo.resubmit_plan.assert_not_called()


@pytest.mark.parametrize("semester", ["", "   ", "Fall 2026", "Year 0 semester 1", "Year 4 semester 1", "Year 1 semester 4", "Year 1 Semester 1"])
def test_UT_08_invalid_semesters(advising, semester):
    with pytest.raises(ValueError, match="^Choose a valid year and semester before submitting a plan\\.$"):
        advising.service.submit_plan(1, [103], semester)
    no_submission(advising)
    advising.repo.list_courses.assert_not_called()


def test_UT_09_empty_selection(advising):
    with pytest.raises(ValueError, match="^Select at least one course for the semester plan\\.$"):
        advising.service.submit_plan(1, [], T1)
    no_submission(advising)
    advising.repo.list_courses.assert_not_called()
    advising.repo.get_completed_course_ids.assert_not_called()
    advising.repo.get_completed_courses.assert_not_called()


@pytest.mark.parametrize("selection", [[103, 103], [103, 104, 103]])
def test_UT_10_duplicate_selection(advising, selection):
    with pytest.raises(ValueError, match="^A course may only appear once in a semester plan\\.$"):
        advising.service.submit_plan(1, selection, T1)
    no_submission(advising)


@pytest.mark.parametrize("selection,message", [
    ([103, 999999], "Course ID 999999 is no longer available."),
    ([101], "COMP 1100: Already completed."),
    ([102], "MATH 1000: Already in progress."),
    ([105], "COMP 3000: Missing prerequisite(s): MATH 9999."),
])
def test_UT_11_selection_aborts_without_writes(advising, selection, message):
    with pytest.raises(ValueError) as exc:
        advising.service.submit_plan(1, selection, T1)
    assert str(exc.value) == message
    no_submission(advising)


@pytest.mark.parametrize("status", [None] + STATUSES)
def test_UT_12_submission_status_table(advising, status):
    existing = plan(status) if status else None
    advising.repo.get_plan_for_student.return_value = existing
    if status in {"Pending", "Approved"}:
        with pytest.raises(ValueError, match="already under review or approved"):
            advising.service.submit_plan(1, [103, 104], T1)
        no_submission(advising)
    elif status in {"Rejected", "Changes Requested"}:
        assert advising.service.submit_plan(1, [103, 104], T1) is advising.repo.resubmit_plan.return_value
        advising.repo.resubmit_plan.assert_called_once_with(existing, [103, 104])
        advising.repo.create_plan.assert_not_called()
    else:
        assert advising.service.submit_plan(1, [103, 104], T1) is advising.repo.create_plan.return_value
        advising.repo.create_plan.assert_called_once_with(1, [103, 104], semester_name=T1)
        advising.repo.resubmit_plan.assert_not_called()
    advising.repo.get_plan_for_student.assert_called_once_with(1, T1)


@pytest.mark.parametrize("status", [None] + STATUSES)
def test_UT_13_dashboard_selection_and_edit(advising, status):
    advising.repo.get_plan_for_student.return_value = plan(status) if status else None
    advising.repo.get_plan_courses.return_value = [PlanCourse(id=60, plan_id=50, course_id=103)]
    result = advising.service.get_student_dashboard(1, T1)
    assert result["can_edit_plan"] is (status in {"Rejected", "Changes Requested", "Cancelled"})
    selected = status is not None and status != "Cancelled"
    assert result["selected_course_ids"] == ({103} if selected else set())
    assert result["planned_courses"] == ([advising.courses[2]] if selected else [])
    if not selected:
        advising.repo.get_plan_courses.assert_not_called()


@pytest.mark.parametrize("decision,status", DECISIONS)
@pytest.mark.parametrize("feedback", ["  Review note  ", ""], ids=["trimmed-note", "empty"])
def test_UT_14_advisor_decisions(advising, decision, status, feedback):
    pending = plan()
    advising.repo.get_plan_by_id.return_value = pending
    assert advising.service.review_plan(50, decision, feedback, 3) is advising.repo.update_plan.return_value
    advising.repo.update_plan.assert_called_once_with(pending, status=status, feedback=feedback.strip(), advisor_id=3, expected_status="Pending")


@pytest.mark.parametrize("decision", ["", "APPROVE", "cancel", "unknown"])
def test_UT_15_invalid_decision(advising, decision):
    with pytest.raises(ValueError, match="^Choose approve, reject, or request changes\\.$"):
        advising.service.review_plan(50, decision, "Note", 3)
    advising.repo.update_plan.assert_not_called()
    advising.repo.get_plan_by_id.assert_not_called()


@pytest.mark.parametrize("decision,status", DECISIONS)
@pytest.mark.parametrize("feedback", ["", "x"*499, "x"*500, "x"*501, " "*501, " " + "x"*499 + " "], ids=["0", "499", "500", "501", "501-spaces", "501-padded"])
def test_UT_16_feedback_raw_length(advising, decision, status, feedback):
    pending = plan()
    advising.repo.get_plan_by_id.return_value = pending
    if len(feedback) > 500:
        with pytest.raises(ValueError, match="^Advisor feedback must be 500 characters or fewer\\.$"):
            advising.service.review_plan(50, decision, feedback, 3)
        advising.repo.update_plan.assert_not_called()
        advising.repo.get_plan_by_id.assert_not_called()
    else:
        assert advising.service.review_plan(50, decision, feedback, 3) is advising.repo.update_plan.return_value
        advising.repo.update_plan.assert_called_once_with(pending, status=status, feedback=feedback.strip(), advisor_id=3, expected_status="Pending")


@pytest.mark.parametrize("status", [None, "Approved", "Rejected", "Changes Requested", "Cancelled"])
def test_UT_17_review_requires_pending_plan(advising, status):
    advising.repo.get_plan_by_id.return_value = plan(status) if status else None
    with pytest.raises(ValueError) as exc:
        advising.service.review_plan(50, "approve", "Note", 3)
    assert str(exc.value) == ("Only pending plans can be reviewed." if status else "Plan not found.")
    advising.repo.update_plan.assert_not_called()


@pytest.mark.parametrize("status,owner", [(s, 1) for s in STATUSES] + [("Pending", 2), (None, 1)])
def test_UT_18_cancellation_matrix(advising, status, owner):
    existing = plan(status, owner) if status else None
    advising.repo.get_plan_by_id.return_value = existing
    if owner == 1 and status in {"Pending", "Approved", "Rejected"}:
        assert advising.service.cancel_plan(1, 50) is advising.repo.cancel_plan.return_value
        advising.repo.cancel_plan.assert_called_once_with(existing)
    else:
        with pytest.raises(ValueError) as exc:
            advising.service.cancel_plan(1, 50)
        assert str(exc.value) == ("Plan not found." if owner != 1 or status is None else "Only pending, rejected, or approved plans can be cancelled.")
        advising.repo.cancel_plan.assert_not_called()


@pytest.mark.parametrize("status,owner,links,target,message", [
    ("Pending", 1, [103, 104], 104, None),
    ("Pending", 1, [103], 103, "Cancel the semester plan to remove its last course."),
    ("Pending", 1, [103, 104], 105, "That course is not part of this plan."),
    *[(s, 1, [103, 104], 104, "Only courses in pending plans can be removed.") for s in STATUSES if s != "Pending"],
    ("Pending", 2, [103, 104], 104, "Plan not found."),
    (None, 1, [103, 104], 104, "Plan not found."),
])
def test_UT_19_remove_course_matrix(advising, status, owner, links, target, message):
    existing = plan(status, owner) if status else None
    advising.repo.get_plan_by_id.return_value = existing
    items = [PlanCourse(id=60+i, plan_id=50, course_id=cid) for i, cid in enumerate(links)]
    advising.repo.get_plan_courses.return_value = items
    if message:
        with pytest.raises(ValueError) as exc:
            advising.service.remove_submitted_course(1, 50, target)
        assert str(exc.value) == message
        advising.repo.remove_plan_course.assert_not_called()
    else:
        assert advising.service.remove_submitted_course(1, 50, target) is existing
        advising.repo.remove_plan_course.assert_called_once_with(items[1])
