import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import inspect
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select
from starlette.requests import Request

from app.database import get_session, upgrade_existing_schema
from app.dependencies.auth import is_admin_dep
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
from app.repositories.user import UserRepository
from app.routers import admin_home, templates
from app.services.advising_service import SEMESTER_OPTIONS, AdvisingService
from app.services.auth_service import AuthService


@pytest.fixture
def advising_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        program = DegreeProgram(name="Computer Science", total_credits=93)
        student = User(
            username="student",
            email="student@example.com",
            password="hashed-password",
            role="regular_user",
            name="Test Student",
            student_number="12345678",
        )
        advisor = User(
            username="advisor",
            email="advisor@example.com",
            password="hashed-password",
            role="admin",
            name="Test Advisor",
        )
        session.add_all([program, student, advisor])
        session.commit()
        session.refresh(program)
        session.refresh(student)
        session.refresh(advisor)
        student.degree_program = program.id

        completed_course = Course(
            code="COMP 1100",
            title="Foundations",
            credits=3,
            category="Core Courses",
            department="Computer Science",
        )
        eligible_course = Course(
            code="COMP 2000",
            title="Next Course",
            credits=3,
            prerequisite_text="COMP 1100",
            category="Core Courses",
            department="Computer Science",
        )
        in_progress_course = Course(
            code="MATH 1000",
            title="Current Mathematics",
            credits=3,
            category="General Education",
            department="Mathematics",
        )
        session.add_all([completed_course, eligible_course, in_progress_course])
        session.add(
            DegreeRequirement(
                program_id=program.id,
                category="Core Courses",
                required_credits=30,
            )
        )
        session.commit()
        for course in (completed_course, eligible_course, in_progress_course):
            session.refresh(course)
        session.add_all(
            [
                StudentCourse(
                    student_id=student.id,
                    course_id=completed_course.id,
                    completion_status="Completed",
                    grade="A",
                ),
                StudentCourse(
                    student_id=student.id,
                    course_id=in_progress_course.id,
                    completion_status="In Progress",
                    grade="",
                ),
            ]
        )
        session.commit()
        yield session, student, advisor, completed_course, eligible_course, in_progress_course
    engine.dispose()


def test_degree_progress_uses_completed_and_in_progress_course_records(advising_session):
    session, student, _, _, _, _ = advising_session

    dashboard = AdvisingService(session).get_student_dashboard(
        student.id, "Year 1 semester 1"
    )

    assert dashboard["completed_credits"] == 3
    assert dashboard["in_progress_credits"] == 3
    assert dashboard["remaining_credits"] == 87
    assert dashboard["total_credits"] == 93
    assert dashboard["category_progress"] == [
        {
            "category": "Core Courses",
            "earned": 3,
            "required": 30,
            "remaining": 27,
            "percent": 10,
        }
    ]
    assert [item["status"] for item in dashboard["activity"]] == [
        "In Progress",
        "Completed",
    ]


def test_plan_submission_review_request_and_student_resubmission(advising_session):
    session, student, advisor, _, eligible_course, _ = advising_session
    service = AdvisingService(session)

    plan = service.submit_plan(
        student.id,
        [eligible_course.id],
        "Year 1 semester 2",
    )
    service.review_plan(
        plan.id,
        "request_changes",
        "Please choose a different section.",
        advisor.id,
    )
    pending_review = service.get_advisor_dashboard(advisor.id)
    assert pending_review == []
    assert plan.status == "Changes Requested"
    assert plan.advisor_feedback == "Please choose a different section."
    assert service.repo.get_plan_for_student(
        student.id, "Year 1 semester 2"
    ).status == "Changes Requested"

    replacement = Course(
        code="MATH 2000",
        title="Elective",
        credits=3,
        category="Electives",
        department="Mathematics",
    )
    session.add(replacement)
    session.commit()
    session.refresh(replacement)
    resubmitted = service.submit_plan(
        student.id,
        [replacement.id],
        "Year 1 semester 2",
    )

    assert resubmitted.id == plan.id
    assert resubmitted.status == "Pending"
    assert resubmitted.advisor_feedback == ""
    assert [
        row.course_id for row in service.repo.get_plan_courses(resubmitted.id)
    ] == [replacement.id]


@pytest.mark.asyncio
async def test_json_request_changes_includes_decision_and_feedback(advising_session):
    session, student, advisor, _, eligible_course, _ = advising_session
    service = AdvisingService(session)
    plan = service.submit_plan(
        student.id,
        [eligible_course.id],
        "Year 1 semester 1",
    )
    get_request = Request(
        {
            "type": "http",
            "method": "GET",
            "scheme": "http",
            "path": "/admin",
            "server": ("testserver", 80),
            "headers": [],
            "query_string": b"",
            "app": app,
            "session": {},
        }
    )
    rendered = templates.TemplateResponse(
        request=get_request,
        name="advisor_dashboard.html",
        context={
            "user": advisor,
            "plans": service.get_advisor_dashboard(advisor.id),
            "active_tab": "advisor-review",
        },
    ).body.decode()
    assert "selectedDecision" in rendered
    assert "decision," in rendered
    assert 'feedback: form.elements.namedItem("feedback").value' in rendered

    payload = json.dumps(
        {
            "decision": "request_changes",
            "feedback": "Please choose another course.",
        }
    ).encode()

    async def receive():
        return {
            "type": "http.request",
            "body": payload,
            "more_body": False,
        }

    request = Request(
        {
            "type": "http",
            "method": "POST",
            "scheme": "http",
            "path": f"/admin/review/{plan.id}",
            "raw_path": f"/admin/review/{plan.id}".encode(),
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
            "root_path": "",
            "query_string": b"",
            "headers": [(b"content-type", b"application/json")],
            "app": app,
            "session": {},
        },
        receive,
    )

    response = await admin_home.review_plan(
        request=request,
        user=advisor,
        db=session,
        plan_id=plan.id,
    )

    session.refresh(plan)
    assert response.status_code == 303
    assert plan.status == "Changes Requested"
    assert plan.advisor_feedback == "Please choose another course."


def test_request_changes_json_http_route(advising_session):
    session, student, advisor, _, eligible_course, _ = advising_session
    plan = AdvisingService(session).submit_plan(
        student.id,
        [eligible_course.id],
        "Year 1 semester 1",
    )

    def override_session():
        yield session

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[is_admin_dep] = lambda: advisor
    client = TestClient(app, follow_redirects=False)
    try:
        response = client.post(
            f"/admin/review/{plan.id}",
            json={
                "decision": "request_changes",
                "feedback": "Please choose another course.",
            },
        )
    finally:
        client.close()
        app.dependency_overrides.pop(get_session, None)
        app.dependency_overrides.pop(is_admin_dep, None)

    session.refresh(plan)
    assert response.status_code == 303
    assert plan.status == "Changes Requested"
    assert plan.advisor_feedback == "Please choose another course."


def test_plan_validation_blocks_ineligible_courses_and_duplicate_plans(advising_session):
    session, student, _, _, eligible_course, in_progress_course = advising_session
    service = AdvisingService(session)

    with pytest.raises(ValueError, match="MATH 1000: Already in progress"):
        service.submit_plan(
            student.id, [in_progress_course.id], "Year 1 semester 1"
        )

    plan = service.submit_plan(
        student.id, [eligible_course.id], "Year 1 semester 1"
    )
    with pytest.raises(ValueError, match="already under review"):
        service.submit_plan(
            student.id, [eligible_course.id], "Year 1 semester 1"
        )

    assert plan.status == "Pending"
    assert len(session.exec(select(SemesterPlan)).all()) == 1


def test_semester_options_cover_three_years_and_summer_terms(advising_session):
    session, student, _, _, _, _ = advising_session
    dashboard = AdvisingService(session).get_student_dashboard(student.id)

    assert dashboard["semester_options"] == [
        f"Year {year} semester {semester}"
        for year in range(1, 4)
        for semester in range(1, 4)
    ]
    assert dashboard["semester_options"][2] == "Year 1 semester 3"
    assert dashboard["semester_options"][5] == "Year 2 semester 3"
    assert dashboard["semester_options"][8] == "Year 3 semester 3"
    assert "Fall 2026" not in dashboard["semester_options"]


def test_plan_submission_rejects_legacy_semester_names(advising_session):
    session, student, _, _, eligible_course, _ = advising_session

    with pytest.raises(ValueError, match="valid year and semester"):
        AdvisingService(session).submit_plan(
            student.id, [eligible_course.id], "Fall 2026"
        )


def test_plan_submission_names_the_missing_prerequisite(advising_session):
    session, student, _, _, _, _ = advising_session
    service = AdvisingService(session)
    course = Course(
        code="COMP 3000",
        title="Advanced Topics",
        credits=3,
        prerequisite_text="COMP 1100, MATH 9999",
        category="Electives",
        department="Computer Science",
    )
    session.add(course)
    session.commit()
    session.refresh(course)

    assert service.get_course_availability(student.id)[course.id] == (
        False,
        "Missing prerequisite(s): MATH 9999",
    )
    with pytest.raises(
        ValueError,
        match=r"COMP 3000: Missing prerequisite\(s\): MATH 9999\.",
    ):
        service.submit_plan(student.id, [course.id], "Year 1 semester 1")


def test_student_can_remove_submitted_course_cancel_and_resubmit_plan(advising_session):
    session, student, advisor, _, eligible_course, _ = advising_session
    service = AdvisingService(session)
    second_course = Course(
        code="MATH 2000",
        title="Elective",
        credits=3,
        category="Electives",
        department="Mathematics",
    )
    session.add(second_course)
    session.commit()
    session.refresh(second_course)

    plan = service.submit_plan(
        student.id,
        [eligible_course.id, second_course.id],
        "Year 1 semester 1",
    )
    returned_plan = service.remove_submitted_course(
        student.id,
        plan.id,
        second_course.id,
    )

    assert returned_plan.id == plan.id
    assert [
        item.course_id for item in service.repo.get_plan_courses(plan.id)
    ] == [eligible_course.id]
    with pytest.raises(ValueError, match="last course"):
        service.remove_submitted_course(student.id, plan.id, eligible_course.id)
    with pytest.raises(ValueError, match="Plan not found"):
        service.cancel_plan(advisor.id, plan.id)

    cancelled = service.cancel_plan(student.id, plan.id)
    assert cancelled.status == "Cancelled"
    assert service.get_advisor_dashboard(advisor.id) == []
    assert len(service.repo.get_plan_courses(plan.id)) == 1
    cancelled_dashboard = service.get_student_dashboard(
        student.id, "Year 1 semester 1"
    )
    assert cancelled_dashboard["selected_course_ids"] == set()
    assert cancelled_dashboard["planned_courses"] == []
    assert cancelled_dashboard["can_edit_plan"] is True

    resubmitted = service.submit_plan(
        student.id,
        [second_course.id],
        "Year 1 semester 1",
    )
    assert resubmitted.id != plan.id
    assert resubmitted.status == "Pending"
    assert plan.status == "Cancelled"
    assert [
        item.course_id for item in service.repo.get_plan_courses(resubmitted.id)
    ] == [second_course.id]

    service.review_plan(resubmitted.id, "approve", "", advisor.id)
    approved_plan_id = resubmitted.id
    with pytest.raises(ValueError, match="pending plans"):
        service.remove_submitted_course(student.id, approved_plan_id, second_course.id)
    approved = service.cancel_plan(student.id, approved_plan_id)
    assert approved.status == "Cancelled"
    assert service.get_student_dashboard(student.id, "Year 1 semester 1")[
        "selected_course_ids"
    ] == set()

    replacement_plan = service.submit_plan(
        student.id,
        [eligible_course.id],
        "Year 1 semester 1",
    )
    assert replacement_plan.id != approved_plan_id
    assert replacement_plan.status == "Pending"
    assert service.repo.get_plan_by_id(approved_plan_id).status == "Cancelled"


def test_rejected_plan_can_be_cancelled_and_replaced(advising_session):
    session, student, advisor, _, eligible_course, _ = advising_session
    service = AdvisingService(session)
    first_plan = service.submit_plan(
        student.id, [eligible_course.id], "Year 1 semester 1"
    )
    service.review_plan(first_plan.id, "reject", "Please start over.", advisor.id)

    cancelled = service.cancel_plan(student.id, first_plan.id)
    assert cancelled.status == "Cancelled"
    second_plan = service.submit_plan(
        student.id,
        [eligible_course.id],
        "Year 1 semester 1",
    )

    assert second_plan.id != first_plan.id
    assert first_plan.status == "Cancelled"
    assert second_plan.status == "Pending"
    assert (
        service.repo.get_plan_for_student(student.id, "Year 1 semester 1").id
        == second_plan.id
    )


def test_pending_plan_course_controls_render(advising_session):
    session, student, _, _, eligible_course, _ = advising_session
    service = AdvisingService(session)
    second_course = Course(
        code="MATH 2000",
        title="Elective",
        credits=3,
        category="Electives",
        department="Mathematics",
    )
    session.add(second_course)
    session.commit()
    session.refresh(second_course)
    plan = service.submit_plan(
        student.id,
        [eligible_course.id, second_course.id],
        "Year 1 semester 1",
    )
    dashboard = service.get_student_dashboard(student.id, "Year 1 semester 1")
    availability = service.get_course_availability(student.id)
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "scheme": "http",
            "path": "/app",
            "server": ("testserver", 80),
            "headers": [],
            "query_string": b"",
            "app": app,
            "session": {},
        }
    )

    response = templates.TemplateResponse(
        request=request,
        name="myadvisor_dashboard.html",
        context={
            "user": student,
            "dashboard": dashboard,
            "active_tab": "plan-courses",
            "catalog_items": [
                {
                    "course": course,
                    "eligible": availability[course.id][0],
                    "eligibility_message": availability[course.id][1],
                }
                for course in dashboard["courses"]
            ],
            "departments": sorted(
                {course.department for course in dashboard["courses"]}
            ),
        },
    )

    html = response.body.decode()
    assert "plan-status-alert" in html
    assert "alert-info" in html
    assert "Pending · Year 1 semester 1" in html
    assert f"/app/plan/{plan.id}/cancel" in html
    assert f"/app/plan/{plan.id}/courses/{eligible_course.id}/remove" in html
    assert "Cancel Plan" in html
    assert "Remove COMP 2000 from the submitted plan" in html

    plan.status = "Rejected"
    session.add(plan)
    session.commit()
    rejected_response = templates.TemplateResponse(
        request=request,
        name="myadvisor_dashboard.html",
        context={
            "user": student,
            "dashboard": dashboard,
            "active_tab": "plan-courses",
            "catalog_items": [
                {
                    "course": course,
                    "eligible": availability[course.id][0],
                    "eligibility_message": availability[course.id][1],
                }
                for course in dashboard["courses"]
            ],
            "departments": sorted(
                {course.department for course in dashboard["courses"]}
            ),
        },
    )
    assert "Cancel Plan" in rejected_response.body.decode()

    plan.status = "Approved"
    session.add(plan)
    session.commit()
    approved_response = templates.TemplateResponse(
        request=request,
        name="myadvisor_dashboard.html",
        context={
            "user": student,
            "dashboard": dashboard,
            "active_tab": "plan-courses",
            "catalog_items": [
                {
                    "course": course,
                    "eligible": availability[course.id][0],
                    "eligibility_message": availability[course.id][1],
                }
                for course in dashboard["courses"]
            ],
            "departments": sorted(
                {course.department for course in dashboard["courses"]}
            ),
        },
    )
    assert "Cancel Plan" in approved_response.body.decode()


@pytest.mark.parametrize(
    ("status", "alert_class", "notice_text"),
    [
        ("Pending", "alert-info", "This plan is awaiting advisor review."),
        ("Approved", "alert-success", "This plan has been approved."),
        ("Changes Requested", "alert-warning", "Update the selection below to resubmit."),
        ("Rejected", "alert-warning", "Update the selection below to resubmit."),
        ("Cancelled", "alert-warning plan-status-cancelled", "Start a new course selection below for this semester."),
    ],
)
def test_plan_status_notice_is_rendered_with_high_contrast(
    advising_session, status, alert_class, notice_text
):
    session, student, _, _, _, _ = advising_session
    session.add(
        SemesterPlan(
            student_id=student.id,
            semester_name="Year 1 semester 1",
            status=status,
            advisor_feedback=(
                "Do another course" if status == "Changes Requested" else ""
            ),
        )
    )
    session.commit()
    service = AdvisingService(session)
    dashboard = service.get_student_dashboard(student.id, "Year 1 semester 1")
    availability = service.get_course_availability(student.id)
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "scheme": "http",
            "path": "/app",
            "server": ("testserver", 80),
            "headers": [],
            "query_string": b"",
            "app": app,
            "session": {},
        }
    )
    response = templates.TemplateResponse(
        request=request,
        name="myadvisor_dashboard.html",
        context={
            "user": student,
            "dashboard": dashboard,
            "active_tab": "plan-courses",
            "catalog_items": [
                {
                    "course": course,
                    "eligible": availability[course.id][0],
                    "eligibility_message": availability[course.id][1],
                }
                for course in dashboard["courses"]
            ],
            "departments": sorted(
                {course.department for course in dashboard["courses"]}
            ),
        },
    )

    html = response.body.decode()
    assert "plan-status-alert" in html
    for class_name in alert_class.split():
        assert class_name in html
    assert f"{status} · Year 1 semester 1" in html
    assert notice_text in html
    if status in {"Approved", "Rejected"}:
        assert 'class="btn btn-sm btn-cancel-plan"' in html
    if status == "Changes Requested":
        assert "Advisor feedback: Do another course" in html


def test_demo_seed_creates_wireframe_catalog_and_is_idempotent(advising_session):
    session, student, _, _, _, _ = advising_session
    service = AdvisingService(session)
    student.username = "bob"
    student.student_number = None
    session.add(student)
    # This seed scenario uses the known demo Core=36 baseline. The shared
    # calculation fixture's custom Core=30 is intentionally retained elsewhere.
    requirement = session.exec(select(DegreeRequirement)).one()
    requirement.required_credits = 36
    session.add(requirement)
    session.commit()

    service.ensure_demo_data()
    service.ensure_demo_data()

    courses = service.repo.list_courses()
    course_codes = {course.code for course in courses}
    assert course_codes >= {
        "COMP 2604",
        "COMP 2605",
        "COMP 2606",
        "COMP 2611",
        "MATH 2250",
        "COMP 1201",
        "COMP 1601",
        "COMP 2201",
        "COMP 2301",
        "COMP 2501",
        "COMP 2700",
        "COMP 2800",
        "COMP 3001",
        "COMP 3100",
        "COMP 3200",
        "MATH 1300",
        "MATH 2200",
        "STAT 2000",
        "ENGL 1000",
        "PHYS 1100",
    }
    assert len(courses) == len(course_codes)
    availability = service.get_course_availability(student.id)
    eligible_codes = {
        course.code
        for course in courses
        if availability[course.id][0]
    }
    assert {
        "COMP 1201",
        "MATH 1300",
        "MATH 2200",
        "STAT 2000",
        "ENGL 1000",
        "PHYS 1100",
    } <= eligible_codes
    assert len(service.repo.list_degree_requirements(student.degree_program)) == 5
    assert not session.exec(select(SemesterPlan)).all()
    assert not session.exec(select(PlanCourse)).all()
    dashboard = service.get_student_dashboard(student.id)
    assert dashboard["current_plan"] is None
    assert dashboard["planned_courses"] == []


def test_student_registration_stores_profile_and_default_degree(advising_session):
    session, _, _, _, _, _ = advising_session

    student = AuthService(UserRepository(session)).register_user(
        "new-student",
        "new-student@example.com",
        "test-password",
        name="New Student",
        student_number="STU-0002",
    )

    assert student.name == "New Student"
    assert student.student_number == "STU-0002"
    assert student.degree_program is not None


def test_workflow_templates_parse():
    template_dir = Path(__file__).resolve().parents[1] / "app" / "templates"
    templates = Environment(loader=FileSystemLoader(str(template_dir)))

    templates.get_template("myadvisor_dashboard.html")
    templates.get_template("advisor_dashboard.html")
    templates.get_template("register.html")


def test_favicon_is_served_from_application_root():
    response = TestClient(app).get("/favicon.svg")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert b"<svg" in response.content


@pytest.mark.parametrize(
    ("tab", "heading"),
    [
        ("home", "Home"),
        ("degree-progress", "Degree Progress"),
        ("plan-courses", "Plan Courses"),
        ("messages", "Messages"),
        ("profile", "Profile"),
    ],
)
def test_student_navigation_renders_requested_tabs(advising_session, tab, heading):
    session, student, _, _, _, _ = advising_session
    service = AdvisingService(session)
    dashboard = service.get_student_dashboard(student.id)
    availability = service.get_course_availability(student.id)
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "scheme": "http",
            "path": "/app",
            "server": ("testserver", 80),
            "headers": [],
            "query_string": b"",
            "app": app,
            "session": {},
        }
    )
    response = templates.TemplateResponse(
        request=request,
        name="myadvisor_dashboard.html",
        context={
            "user": student,
            "dashboard": dashboard,
            "active_tab": tab,
            "catalog_items": [
                {
                    "course": course,
                    "eligible": availability[course.id][0],
                    "eligibility_message": availability[course.id][1],
                }
                for course in dashboard["courses"]
            ],
            "departments": sorted(
                {course.department for course in dashboard["courses"]}
            ),
        },
    )

    html = response.body.decode()
    for label in ("Home", "Degree Progress", "Plan Courses", "Messages", "Profile"):
        assert label in html
    assert f"<h1 class=\"page-title mb-1\">\n        {heading}" in html
    assert 'rel="icon" type="image/svg+xml"' in html
    assert 'rel="icon" type="image/svg+xml"' in html
    assert "favicon.svg" in html
    assert 'class="app-sidebar shadow"' in html
    assert 'data-sidebar-toggle' in html
    assert 'class="header-account-name fw-semibold"' in html
    assert "window.adminlte.PushMenu.getOrCreateInstance(sidebar)" in html
    assert 'href="https://cdn.jsdelivr.net/npm/admin-lte@4.10.0/dist/css/adminlte.min.css"' in html
    assert 'href="https://cdn.jsdelivr.net/npm/overlayscrollbars@2.11.0/styles/overlayscrollbars.min.css"' in html
    assert 'aria-current="page"' in html
    assert "<p>Advisor Review</p>" not in html
    if tab == "home":
        assert "Latest semester plan" in html
        assert "Stay on track" in html
        assert "Overall progress" not in html
        assert 'aria-labelledby="progress-heading"' not in html
    if tab == "degree-progress":
        assert "Overall progress" in html
        assert "Requirement breakdown" in html
        assert "Latest semester plan" not in html
    if tab == "plan-courses":
        for semester in SEMESTER_OPTIONS:
            assert f'<option value="{semester}"' in html
        assert "Semester 3 is the summer semester." in html
    if tab == "messages":
        assert "No advisor updates yet" in html
        assert "Plan Courses" in html
    if tab == "plan-courses":
        assert "Review Selected Courses" in html
        assert "Submit Plan for Advisor Review" in html
        assert 'class="panel-card plan-courses mt-4"' in html
        assert ".course-row.is-hidden { display: none !important; }" in html


def test_admin_navigation_includes_advisor_review(advising_session):
    _, _, advisor, _, _, _ = advising_session
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "scheme": "http",
            "path": "/admin",
            "server": ("testserver", 80),
            "headers": [],
            "query_string": b"",
            "app": app,
            "session": {},
        }
    )
    response = templates.TemplateResponse(
        request=request,
        name="advisor_dashboard.html",
        context={
            "user": advisor,
            "plans": [],
            "active_tab": "advisor-review",
        },
    )

    html = response.body.decode()
    assert "Advisor Review" in html
    assert "Check for New Plans" in html
    assert "Degree Progress" not in html
    assert "Plan Courses" not in html
    assert 'aria-current="page"' in html


@pytest.mark.parametrize(
    ("tab", "expected_content"),
    [
        ("home", "Plans awaiting your review"),
        ("messages", "Your plan review decisions"),
        ("profile", "Advisor profile"),
    ],
)
def test_admin_workspace_tabs_show_advisor_data(
    advising_session,
    tab,
    expected_content,
):
    session, student, advisor, _, eligible_course, _ = advising_session
    service = AdvisingService(session)
    completed_plan = service.submit_plan(
        student.id,
        [eligible_course.id],
        "Year 1 semester 1",
    )
    service.review_plan(
        completed_plan.id,
        "approve",
        "Approved after review.",
        advisor.id,
    )
    service.submit_plan(
        student.id,
        [eligible_course.id],
        "Year 1 semester 2",
    )
    advisor_dashboard = service.get_advisor_overview(advisor.id)
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "scheme": "http",
            "path": "/app",
            "server": ("testserver", 80),
            "headers": [],
            "query_string": b"",
            "app": app,
            "session": {},
        }
    )

    response = templates.TemplateResponse(
        request=request,
        name="myadvisor_dashboard.html",
        context={
            "user": advisor,
            "dashboard": None,
            "advisor_dashboard": advisor_dashboard,
            "active_tab": tab,
            "catalog_items": [],
            "departments": [],
        },
    )
    html = response.body.decode()

    assert expected_content in html
    assert "Degree Progress" not in html
    assert "<p>Plan Courses</p>" not in html
    assert "<p>Advisor Review</p>" in html
    assert "Advisor · advisor@example.com" in html
    if tab == "home":
        assert "registered student accounts" in html
        assert "Plans awaiting your review" in html
        assert "student@example.com" not in html
    elif tab == "messages":
        assert "Approved after review." in html
        assert "Test Student · Year 1 semester 1 plan" in html
    else:
        assert "Advisor administrator" in html
        assert "plans reviewed by you" in html


def test_existing_database_upgrade_adds_wireframe_fields_without_losing_records():
    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.exec_driver_sql(
            "CREATE TABLE user (id INTEGER PRIMARY KEY, username VARCHAR, "
            "email VARCHAR, password VARCHAR, role VARCHAR)"
        )
        connection.exec_driver_sql(
            "CREATE TABLE course (id INTEGER PRIMARY KEY, code VARCHAR, "
            "title VARCHAR, credits INTEGER, prerequisite_text VARCHAR, category VARCHAR)"
        )
        connection.exec_driver_sql(
            "CREATE TABLE studentcourse (id INTEGER PRIMARY KEY, student_id INTEGER, "
            "course_id INTEGER, completion_status VARCHAR, grade VARCHAR)"
        )
        connection.exec_driver_sql(
            "CREATE TABLE semesterplan (id INTEGER PRIMARY KEY, student_id INTEGER, "
            "advisor_id INTEGER, semester_name VARCHAR, status VARCHAR, advisor_feedback VARCHAR)"
        )
        connection.exec_driver_sql(
            "CREATE TABLE plancourse (id INTEGER PRIMARY KEY, plan_id INTEGER, course_id INTEGER)"
        )
        connection.exec_driver_sql(
            "INSERT INTO user VALUES (1, 'legacy', 'legacy@example.com', 'hash', 'regular_user')"
        )
        connection.exec_driver_sql(
            "INSERT INTO semesterplan VALUES (1, 1, NULL, 'Fall 2026', 'Pending', '')"
        )

    SQLModel.metadata.create_all(engine)
    upgrade_existing_schema(engine)
    upgrade_existing_schema(engine)

    columns = {
        table: {column["name"] for column in inspect(engine).get_columns(table)}
        for table in ("user", "course", "studentcourse", "semesterplan")
    }
    with engine.connect() as connection:
        username = connection.exec_driver_sql(
            "SELECT username FROM user WHERE id = 1"
        ).scalar_one()
        timestamp = connection.exec_driver_sql(
            "SELECT submitted_at FROM semesterplan WHERE id = 1"
        ).scalar_one()

    assert username == "legacy"
    assert timestamp is not None
    assert {"name", "student_number", "degree_program"} <= columns["user"]
    assert "department" in columns["course"]
    assert "completed_at" in columns["studentcourse"]
    assert "submitted_at" in columns["semesterplan"]
    engine.dispose()
