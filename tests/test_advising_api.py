"""Student JSON endpoints using real cookie auth, services and isolated SQLite."""

from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from app import database
from app.main import app
from app.models.advising import Course, DegreeProgram, DegreeRequirement, StudentCourse
from app.models.user import User
from app.schemas.advising import CourseSelectionResponse, DegreeProgressResponse
from app.services.advising_service import AdvisingService
from app.utilities.security import create_access_token

ENDPOINTS = ["/api/degree-progress", "/api/courses"]
COURSE_FIELDS = {
    "id",
    "code",
    "title",
    "credits",
    "category",
    "department",
    "prerequisite_text",
}


@pytest.fixture
def api_client(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    # Recovery must also stay on the isolated database. Do not run demo startup.
    monkeypatch.setattr(database, "engine", engine)
    with Session(engine) as session:
        session.add(DegreeProgram(id=1, name="Test Degree", total_credits=30))
        session.add(
            DegreeRequirement(
                program_id=1,
                category="Core Courses",
                required_credits=12,
            )
        )
        for user_id, role in [
            (1, "regular_user"),
            (2, "regular_user"),
            (3, "admin"),
            (4, "unknown"),
        ]:
            session.add(
                User(
                    id=user_id,
                    username=f"private-user-{user_id}",
                    email=f"private-{user_id}@example.com",
                    password="private-password-hash",
                    name=f"Private Name {user_id}",
                    student_number=f"private-number-{user_id}",
                    role=role,
                    degree_program=1 if user_id == 1 else None,
                )
            )
        for course_id, code, prerequisites in [
            (1, "COMP 1000", ""),
            (2, "COMP 2000", "COMP 1000"),
            (3, "COMP 3000", "COMP 1000"),
            (4, "COMP 4000", "COMP 1000, COMP 2000, UNKNOWN 9999"),
            (5, "MATH 1000", ""),
        ]:
            session.add(
                Course(
                    id=course_id,
                    code=code,
                    title=f"Course {course_id}",
                    credits=3,
                    prerequisite_text=prerequisites,
                    category="Core Courses",
                )
            )
        session.add_all(
            [
                StudentCourse(
                    student_id=1, course_id=1, completion_status="Completed", grade="A"
                ),
                StudentCourse(
                    student_id=1, course_id=2, completion_status="In Progress", grade=""
                ),
                StudentCourse(
                    student_id=2, course_id=5, completion_status="Completed", grade="B"
                ),
            ]
        )
        session.commit()

    def isolated_session():
        with Session(engine) as session:
            yield session

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[database.get_session] = isolated_session
    client = TestClient(app, follow_redirects=False)
    try:
        yield client, engine
    finally:
        client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
        engine.dispose()


def login(client, user_id=1, **claims):
    client.cookies.set(
        "access_token", create_access_token({"sub": str(user_id), **claims})
    )


def test_degree_progress_structure_calculations_and_privacy(api_client):
    client, engine = api_client
    login(client)
    response = client.get("/api/degree-progress")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.headers["cache-control"] == "no-store"
    body = response.json()
    assert set(body) == set(DegreeProgressResponse.model_fields)
    assert DegreeProgressResponse.model_validate(body).model_dump(mode="json") == body
    assert body["program"] == {"id": 1, "name": "Test Degree", "total_credits": 30}
    assert {
        key: body[key]
        for key in [
            "total_credits",
            "completed_credits",
            "in_progress_credits",
            "remaining_credits",
            "progress_percent",
        ]
    } == {
        "total_credits": 30,
        "completed_credits": 3,
        "in_progress_credits": 3,
        "remaining_credits": 24,
        "progress_percent": 10,
    }
    assert body["category_progress"] == [
        {
            "category": "Core Courses",
            "earned": 3,
            "required": 12,
            "remaining": 9,
            "percent": 25,
        }
    ]
    assert [course["id"] for course in body["completed"]] == [1]
    assert [course["id"] for course in body["in_progress"]] == [2]
    assert set(body["completed"][0]) == COURSE_FIELDS
    assert "private-" not in response.text
    assert "grade" not in response.text
    with Session(engine) as session:
        dashboard = AdvisingService(session).get_student_dashboard(1)
        for key in [
            "completed_credits",
            "in_progress_credits",
            "remaining_credits",
            "progress_percent",
            "category_progress",
        ]:
            assert body[key] == dashboard[key]


def test_catalogue_structure_and_prerequisite_eligibility(api_client):
    client, _ = api_client
    login(client)
    response = client.get("/api/courses")
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    rows = response.json()
    assert [row["code"] for row in rows] == [
        "COMP 1000",
        "COMP 2000",
        "COMP 3000",
        "COMP 4000",
        "MATH 1000",
    ]
    for row in rows:
        assert set(row) == COURSE_FIELDS | {"eligible", "eligibility_reason"}
        CourseSelectionResponse.model_validate(row)
    assert [(row["eligible"], row["eligibility_reason"]) for row in rows] == [
        (False, "Already completed"),
        (False, "Already in progress"),
        (True, "Eligible"),
        (False, "Missing prerequisite(s): COMP 2000, UNKNOWN 9999"),
        (True, "Eligible"),
    ]
    assert "private-" not in response.text


@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_identity_cannot_be_selected_by_query_or_header(api_client, endpoint):
    client, _ = api_client
    login(client)
    expected = client.get(endpoint).json()
    response = client.get(
        endpoint, params={"student_id": 2}, headers={"X-Student-ID": "2"}
    )
    assert response.status_code == 200
    assert response.json() == expected
    login(client, 2)
    other = client.get(endpoint).json()
    if endpoint.endswith("degree-progress"):
        assert [course["id"] for course in other["completed"]] == [5]
        assert other["in_progress"] == []
        assert other["program"] is None
    else:
        assert other[0]["eligible"] is True
        assert other[-1]["eligibility_reason"] == "Already completed"


@pytest.mark.parametrize("endpoint", ENDPOINTS)
@pytest.mark.parametrize("cookie", [None, "malformed", "deleted-user", "expired"])
def test_unauthenticated_requests_return_json_401(api_client, endpoint, cookie):
    client, _ = api_client
    if cookie == "deleted-user":
        login(client, 999)
    elif cookie == "expired":
        client.cookies.set(
            "access_token",
            create_access_token({"sub": "1"}, expires_delta=timedelta(minutes=-1)),
        )
    elif cookie:
        client.cookies.set("access_token", cookie)
    response = client.get(endpoint, headers={"Accept": "text/html"})
    assert response.status_code == 401
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"detail": "Could not validate credentials"}
    assert "location" not in response.headers


@pytest.mark.parametrize("endpoint", ENDPOINTS)
@pytest.mark.parametrize("user_id", [3, 4])
def test_only_database_student_role_is_authorized(api_client, endpoint, user_id):
    client, _ = api_client
    login(client, user_id, role="regular_user")
    response = client.get(endpoint)
    assert response.status_code == 403
    assert response.json() == {
        "detail": "You are not authorized to access this resource"
    }


@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_role_change_revokes_access_with_existing_cookie(api_client, endpoint):
    client, engine = api_client
    login(client)
    assert client.get(endpoint).status_code == 200
    with Session(engine) as session:
        student = session.get(User, 1)
        student.role = "admin"
        session.add(student)
        session.commit()
    assert client.get(endpoint).status_code == 403


def test_empty_catalogue_and_no_program(api_client):
    client, engine = api_client
    with Session(engine) as session:
        for record in session.exec(select(StudentCourse)).all():
            session.delete(record)
        for course in session.exec(select(Course)).all():
            session.delete(course)
        session.commit()
    login(client, 2)
    assert client.get("/api/courses").json() == []
    body = client.get("/api/degree-progress").json()
    assert body["program"] is None
    assert body["total_credits"] == body["remaining_credits"] == 93
    assert (
        body["completed_credits"]
        == body["in_progress_credits"]
        == body["progress_percent"]
        == 0
    )
    assert body["category_progress"] == body["completed"] == body["in_progress"] == []


def test_response_schema_rejects_invalid_progress(api_client):
    client, _ = api_client
    login(client)
    body = client.get("/api/degree-progress").json()
    for field, value in [("completed_credits", -1), ("progress_percent", 101)]:
        with pytest.raises(ValidationError):
            DegreeProgressResponse.model_validate({**body, field: value})


@pytest.mark.parametrize("required, percent", [(0, 0), (3, 100)])
def test_progress_zero_denominators_and_caps(api_client, required, percent):
    client, engine = api_client
    with Session(engine) as session:
        program = session.get(DegreeProgram, 1)
        program.total_credits = required
        requirement = session.exec(select(DegreeRequirement)).one()
        requirement.required_credits = required
        session.add_all([program, requirement])
        session.commit()
    login(client)
    response = client.get("/api/degree-progress")
    assert response.status_code == 200
    body = response.json()
    assert body["remaining_credits"] == 0
    assert body["progress_percent"] == percent
    assert body["category_progress"][0]["remaining"] == 0
    assert body["category_progress"][0]["percent"] == percent


def test_html_dashboard_is_preserved(api_client):
    client, _ = api_client
    login(client)
    response = client.get("/app")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Test Degree" in response.text


def test_openapi_declares_validated_response_models(api_client):
    client, _ = api_client
    schema = client.get("/openapi.json").json()
    progress = schema["paths"]["/api/degree-progress"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]
    assert progress["$ref"].endswith("/DegreeProgressResponse")
    courses = schema["paths"]["/api/courses"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]
    assert courses["type"] == "array"
    assert courses["items"]["$ref"].endswith("/CourseSelectionResponse")
