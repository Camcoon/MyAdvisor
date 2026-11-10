"""Workflow 2 HTTP integration tests with real auth, services and database writes."""

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event, text
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from app import database
from app.main import app
from app.models.advising import Course, PlanCourse, SemesterPlan, StudentCourse
from app.models.user import User
from app.repositories.advising import AdvisingRepository
from app.schemas.advising import SemesterPlanResponse
from app.services.advising_service import SEMESTER_OPTIONS
from app.utilities.security import create_access_token

BASE = "/api/semester-plans"
SEMESTER = "Year 1 semester 2"
STATUSES = ["Pending", "Approved", "Rejected", "Changes Requested", "Cancelled"]
REQUESTS = [
    ("GET", BASE, None),
    ("GET", BASE + "/{id}", None),
    ("POST", BASE, {"semester_name": SEMESTER, "course_ids": [3]}),
    ("PUT", BASE + "/{id}/courses", {"course_ids": [3]}),
    ("DELETE", BASE + "/{id}/courses/5", None),
    ("DELETE", BASE + "/{id}", None),
]


@pytest.fixture
def plan_client(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _record):
        connection.execute("PRAGMA foreign_keys=ON")

    SQLModel.metadata.create_all(engine)
    monkeypatch.setattr(database, "engine", engine)
    with Session(engine) as session:
        session.add_all(
            [
                User(
                    id=i,
                    username=f"private-user-{i}",
                    email=f"private-{i}@example.com",
                    password="private-hash",
                    role=role,
                )
                for i, role in [
                    (1, "regular_user"),
                    (2, "regular_user"),
                    (3, "admin"),
                    (4, "unknown"),
                ]
            ]
        )
        session.add_all(
            [
                Course(
                    id=i,
                    code=f"COMP {i}000",
                    title=f"Course {i}",
                    prerequisite_text=prereq,
                )
                for i, prereq in [
                    (1, ""),
                    (2, ""),
                    (3, "COMP 1000"),
                    (4, "COMP 2000, UNKNOWN 9999"),
                    (5, ""),
                ]
            ]
        )
        session.commit()
        session.add_all(
            [
                StudentCourse(student_id=1, course_id=1, completion_status="Completed"),
                StudentCourse(
                    student_id=1, course_id=2, completion_status="In Progress"
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
    authenticate(client)
    try:
        yield client, engine
    finally:
        client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
        engine.dispose()


def authenticate(client, student_id=1):
    client.cookies.set(
        "access_token",
        create_access_token({"sub": str(student_id), "role": "regular_user"}),
    )


def seed_plan(engine, status="Pending", student_id=1, course_ids=(3, 5)):
    with Session(engine) as session:
        plan = AdvisingRepository(session).create_plan(
            student_id, course_ids, semester_name=SEMESTER
        )
        plan.status = status
        plan.advisor_id = 3
        plan.advisor_feedback = "Choose an alternative."
        plan.submitted_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
        session.add(plan)
        session.commit()
        return plan.id


def snapshot(engine):
    with Session(engine) as session:
        return {
            "plans": [
                row.model_dump()
                for row in session.exec(
                    select(SemesterPlan).order_by(SemesterPlan.id)
                ).all()
            ],
            "courses": [
                row.model_dump()
                for row in session.exec(
                    select(PlanCourse).order_by(PlanCourse.id)
                ).all()
            ],
        }


def assert_error(response, status, code=None):
    assert response.status_code == status, response.text
    assert response.headers["content-type"] == "application/json"
    assert "location" not in response.headers
    if code:
        assert response.json()["detail"]["code"] == code
        assert isinstance(response.json()["detail"]["message"], str)


@pytest.mark.parametrize("semester", SEMESTER_OPTIONS)
def test_submit_valid_semesters_persists_eligible_courses(plan_client, semester):
    client, engine = plan_client
    response = client.post(
        BASE,
        json={"semester_name": f"  {semester}  ", "course_ids": [3, 5]},
        params={"student_id": 2},
        headers={"X-Student-ID": "2"},
    )
    assert response.status_code == 201
    assert response.headers["cache-control"] == "no-store"
    body = response.json()
    assert set(body) == set(SemesterPlanResponse.model_fields)
    assert body["status"] == "Pending"
    assert body["semester_name"] == semester
    assert body["advisor_feedback"] == ""
    assert [course["id"] for course in body["courses"]] == [3, 5]
    assert "private-" not in response.text
    assert client.get(response.headers["location"]).json() == body
    saved = snapshot(engine)
    assert len(saved["plans"]) == 1
    assert saved["plans"][0]["student_id"] == 1
    assert [row["course_id"] for row in saved["courses"]] == [3, 5]


def test_list_is_owned_newest_first_and_includes_cancelled_history(plan_client):
    client, engine = plan_client
    assert client.get(BASE).json() == []
    old_id = seed_plan(engine, "Cancelled")
    seed_plan(engine, student_id=2)
    new_id = seed_plan(engine, "Changes Requested")
    response = client.get(BASE, params={"student_id": 2}, headers={"X-Student-ID": "2"})
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert [row["id"] for row in response.json()] == [new_id, old_id]
    assert response.json()[1]["status"] == "Cancelled"
    assert response.json()[0]["advisor_feedback"] == "Choose an alternative."
    assert client.get(f"{BASE}/{new_id}").json() == response.json()[0]


@pytest.mark.parametrize("method,path,payload", REQUESTS)
@pytest.mark.parametrize(
    "identity,status", [(None, 401), ("malformed", 401), (999, 401), (3, 403), (4, 403)]
)
def test_every_endpoint_requires_current_student_role(
    plan_client, method, path, payload, identity, status
):
    client, engine = plan_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    client.cookies.clear()
    if identity == "malformed":
        client.cookies.set("access_token", "invalid-cookie")
    elif identity is not None:
        authenticate(client, identity)
    response = client.request(
        method, path.format(id=plan_id), json=payload, headers={"Accept": "text/html"}
    )
    assert_error(response, status)
    assert snapshot(engine) == before


@pytest.mark.parametrize("method,path,payload", [REQUESTS[i] for i in [1, 3, 4, 5]])
@pytest.mark.parametrize("foreign", [True, False])
def test_foreign_and_missing_plans_are_indistinguishable(
    plan_client, method, path, payload, foreign
):
    client, engine = plan_client
    foreign_id = seed_plan(engine, student_id=2)
    before = snapshot(engine)
    response = client.request(
        method, path.format(id=foreign_id if foreign else 999), json=payload
    )
    assert_error(response, 404, "not_found")
    assert response.json()["detail"]["message"] == "Plan not found."
    assert snapshot(engine) == before


@pytest.mark.parametrize(
    "changes,message",
    [
        ({"semester_name": "Fall 2026"}, "valid year and semester"),
        ({"semester_name": "Year 4 semester 1"}, "valid year and semester"),
        ({"semester_name": "Year 1 semester 0"}, "valid year and semester"),
        ({"semester_name": ""}, "valid year and semester"),
        ({"course_ids": [3, 3]}, "only appear once"),
        ({"course_ids": [3, 999]}, "no longer available"),
        ({"course_ids": [1]}, "Already completed"),
        ({"course_ids": [2]}, "Already in progress"),
        ({"course_ids": [4]}, "COMP 2000, UNKNOWN 9999"),
    ],
)
def test_invalid_submission_has_no_database_side_effects(plan_client, changes, message):
    client, engine = plan_client
    before = snapshot(engine)
    response = client.post(
        BASE, json={"semester_name": SEMESTER, "course_ids": [3], **changes}
    )
    assert_error(response, 422, "invalid_plan")
    assert message in response.json()["detail"]["message"]
    assert snapshot(engine) == before


@pytest.mark.parametrize(
    "changes",
    [
        {"course_ids": []},
        {"course_ids": None},
        {"course_ids": "3"},
        {"course_ids": ["3"]},
        {"course_ids": [True]},
        {"course_ids": [3.0]},
        {"course_ids": [0]},
        {"course_ids": [-1]},
        {"course_ids": [None]},
        {"course_ids": [2**63]},
        {"semester_name": None},
        {"semester_name": 1},
        {"student_id": 2},
        {"status": "Approved"},
        {"advisor_id": 3},
        {"advisor_feedback": "Approved"},
    ],
)
def test_request_schema_rejects_invalid_types_and_server_owned_fields(
    plan_client, changes
):
    client, engine = plan_client
    response = client.post(
        BASE, json={"semester_name": SEMESTER, "course_ids": [3], **changes}
    )
    assert_error(response, 422)
    assert snapshot(engine) == {"plans": [], "courses": []}


@pytest.mark.parametrize("method", ["POST", "PUT"])
def test_missing_or_malformed_json_is_structured_422(plan_client, method):
    client, engine = plan_client
    plan_id = seed_plan(engine, "Rejected")
    path = BASE if method == "POST" else f"{BASE}/{plan_id}/courses"
    before = snapshot(engine)
    for options in [
        {},
        {"json": {}},
        {"content": "{", "headers": {"Content-Type": "application/json"}},
    ]:
        assert_error(client.request(method, path, **options), 422)
    assert snapshot(engine) == before


@pytest.mark.parametrize("identifier", ["abc", "0", "-1", str(2**63)])
def test_invalid_resource_identifiers_return_json_422(plan_client, identifier):
    client, engine = plan_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    assert_error(client.get(f"{BASE}/{identifier}"), 422)
    assert_error(client.delete(f"{BASE}/{plan_id}/courses/{identifier}"), 422)
    assert snapshot(engine) == before


@pytest.mark.parametrize("status", STATUSES)
@pytest.mark.parametrize("method", ["POST", "PUT"])
def test_submission_and_revision_preserve_status_transitions(
    plan_client, status, method
):
    client, engine = plan_client
    plan_id = seed_plan(engine, status)
    before = snapshot(engine)
    path = BASE if method == "POST" else f"{BASE}/{plan_id}/courses"
    payload = {"course_ids": [5]}
    if method == "POST":
        payload["semester_name"] = SEMESTER
    response = client.request(method, path, json=payload)
    if status in {"Rejected", "Changes Requested"}:
        assert response.status_code == 200
        assert response.json()["id"] == plan_id
        assert response.json()["status"] == "Pending"
        assert response.json()["advisor_feedback"] == ""
        assert [row["id"] for row in response.json()["courses"]] == [5]
        after = snapshot(engine)
        assert len(after["plans"]) == 1
        assert after["plans"][0]["advisor_id"] is None
        assert after["plans"][0]["submitted_at"] > before["plans"][0]["submitted_at"]
        assert [row["course_id"] for row in after["courses"]] == [5]
    elif status == "Cancelled" and method == "POST":
        assert response.status_code == 201
        assert response.json()["id"] != plan_id
        assert response.json()["status"] == "Pending"
        assert snapshot(engine)["plans"][0] == before["plans"][0]
        assert len(snapshot(engine)["plans"]) == 2
    else:
        assert_error(response, 409, "plan_conflict")
        assert snapshot(engine) == before


@pytest.mark.parametrize("course_ids", [[], [5, 5], [3, 999], [1], [2], [4]])
@pytest.mark.parametrize("method", ["POST", "PUT"])
def test_failed_resubmission_preserves_courses_status_and_feedback(
    plan_client, course_ids, method
):
    client, engine = plan_client
    plan_id = seed_plan(engine, "Changes Requested")
    before = snapshot(engine)
    payload = {"course_ids": course_ids}
    path = f"{BASE}/{plan_id}/courses"
    if method == "POST":
        payload["semester_name"] = SEMESTER
        path = BASE
    assert_error(client.request(method, path, json=payload), 422)
    assert snapshot(engine) == before


def test_revision_cannot_change_semester_or_target_an_older_plan(plan_client):
    client, engine = plan_client
    old_id = seed_plan(engine, "Rejected")
    new_id = seed_plan(engine, "Changes Requested")
    before = snapshot(engine)
    assert_error(
        client.put(f"{BASE}/{old_id}/courses", json={"course_ids": [5]}),
        409,
        "plan_conflict",
    )
    assert_error(
        client.put(
            f"{BASE}/{new_id}/courses",
            json={"course_ids": [5], "semester_name": "Year 3 semester 3"},
        ),
        422,
    )
    assert snapshot(engine) == before


def test_resubmission_rechecks_current_prerequisite_eligibility(plan_client):
    client, engine = plan_client
    plan_id = seed_plan(engine, "Rejected")
    with Session(engine) as session:
        record = session.exec(
            select(StudentCourse).where(StudentCourse.course_id == 1)
        ).one()
        record.completion_status = "In Progress"
        session.add(record)
        session.commit()
    before = snapshot(engine)
    response = client.put(f"{BASE}/{plan_id}/courses", json={"course_ids": [3]})
    assert_error(response, 422, "invalid_plan")
    assert "COMP 1000" in response.json()["detail"]["message"]
    assert snapshot(engine) == before


@pytest.mark.parametrize("status", STATUSES)
def test_course_removal_only_from_pending_plans(plan_client, status):
    client, engine = plan_client
    plan_id = seed_plan(engine, status)
    before = snapshot(engine)
    response = client.delete(f"{BASE}/{plan_id}/courses/5")
    if status == "Pending":
        assert response.status_code == 200
        assert response.json()["status"] == "Pending"
        assert [row["id"] for row in response.json()["courses"]] == [3]
        after = snapshot(engine)
        assert after["plans"] == before["plans"]
        assert [row["course_id"] for row in after["courses"]] == [3]
        assert_error(client.delete(f"{BASE}/{plan_id}/courses/3"), 409, "plan_conflict")
        assert snapshot(engine) == after
    else:
        assert_error(response, 409, "plan_conflict")
        assert snapshot(engine) == before


def test_removing_a_course_not_in_plan_returns_404(plan_client):
    client, engine = plan_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    assert_error(client.delete(f"{BASE}/{plan_id}/courses/1"), 404, "not_found")
    assert snapshot(engine) == before


@pytest.mark.parametrize("status", STATUSES)
def test_cancellation_rules_preserve_history(plan_client, status):
    client, engine = plan_client
    plan_id = seed_plan(engine, status)
    before = snapshot(engine)
    response = client.delete(f"{BASE}/{plan_id}")
    if status in {"Pending", "Rejected", "Approved"}:
        assert response.status_code == 200
        assert response.json()["status"] == "Cancelled"
        after = snapshot(engine)
        assert after["courses"] == before["courses"]
        assert after["plans"] == [{**before["plans"][0], "status": "Cancelled"}]
        assert client.get(f"{BASE}/{plan_id}").json() == response.json()
        assert_error(client.delete(f"{BASE}/{plan_id}"), 409, "plan_conflict")
        assert snapshot(engine) == after
    else:
        assert_error(response, 409, "plan_conflict")
        assert snapshot(engine) == before


@pytest.mark.parametrize("operation", ["create", "revise", "remove", "cancel"])
def test_database_failures_roll_back_entire_mutation(plan_client, operation):
    client, engine = plan_client
    plan_id = (
        None
        if operation == "create"
        else seed_plan(engine, "Rejected" if operation == "revise" else "Pending")
    )
    before = snapshot(engine)
    trigger = {
        "create": "BEFORE INSERT ON plancourse WHEN NEW.course_id = 5",
        "revise": "BEFORE INSERT ON plancourse WHEN NEW.course_id = 5",
        "remove": "BEFORE DELETE ON plancourse",
        "cancel": "BEFORE UPDATE ON semesterplan",
    }[operation]
    with engine.begin() as connection:
        connection.execute(
            text(
                f"CREATE TRIGGER fail_write {trigger} BEGIN SELECT RAISE(ABORT, 'private database details'); END"
            )
        )
    if operation == "create":
        response = client.post(
            BASE, json={"semester_name": SEMESTER, "course_ids": [3, 5]}
        )
    elif operation == "revise":
        response = client.put(f"{BASE}/{plan_id}/courses", json={"course_ids": [3, 5]})
    elif operation == "remove":
        response = client.delete(f"{BASE}/{plan_id}/courses/5")
    else:
        response = client.delete(f"{BASE}/{plan_id}")
    assert_error(response, 409, "plan_conflict")
    assert "private database details" not in response.text
    assert snapshot(engine) == before
    with engine.begin() as connection:
        connection.execute(text("DROP TRIGGER fail_write"))
    # A fresh request succeeds after the failure is removed.
    assert (
        client.post(
            BASE, json={"semester_name": "Year 2 semester 1", "course_ids": [3]}
        ).status_code
        == 201
    )


def test_database_operational_error_returns_json_without_partial_plan(plan_client):
    client, engine = plan_client
    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TRIGGER broken_schema BEFORE INSERT ON plancourse "
                "BEGIN SELECT * FROM private_missing_table; END"
            )
        )
    response = client.post(BASE, json={"semester_name": SEMESTER, "course_ids": [3]})
    assert_error(response, 503, "database_unavailable")
    assert "private_missing_table" not in response.text
    assert snapshot(engine) == {"plans": [], "courses": []}


def test_html_forms_and_api_share_the_same_plans(plan_client):
    client, engine = plan_client
    response = client.post(
        "/app/plan", data={"semester_name": SEMESTER, "course_ids": [3, 5]}
    )
    assert response.status_code == 303
    plan_id = client.get(BASE).json()[0]["id"]
    response = client.post(f"/app/plan/{plan_id}/courses/5/remove")
    assert response.status_code == 303
    assert [row["id"] for row in client.get(f"{BASE}/{plan_id}").json()["courses"]] == [
        3
    ]
    # Invalid form submissions continue to flash and redirect rather than return API JSON.
    assert (
        client.post(
            "/app/plan", data={"semester_name": SEMESTER, "course_ids": [3, 3]}
        ).status_code
        == 303
    )
    assert client.post(f"/app/plan/{plan_id}/cancel").status_code == 303
    assert client.get(f"{BASE}/{plan_id}").json()["status"] == "Cancelled"
    assert (
        client.post(
            BASE, json={"semester_name": SEMESTER, "course_ids": [5]}
        ).status_code
        == 201
    )
    dashboard = client.get("/app", params={"semester": SEMESTER, "tab": "plan-courses"})
    assert dashboard.status_code == 200
    assert "text/html" in dashboard.headers["content-type"]
    assert len(snapshot(engine)["plans"]) == 2


def test_openapi_documents_resources_and_request_allowlists(plan_client):
    client, _ = plan_client
    schema = client.get("/openapi.json").json()
    for method, path, _ in REQUESTS:
        path = path.replace("{id}", "{plan_id}").replace(
            "/courses/5", "/courses/{course_id}"
        )
        operation = schema["paths"][path][method.lower()]
        assert "200" in operation["responses"] or "201" in operation["responses"]
    request = schema["components"]["schemas"]["SemesterPlanRequest"]
    assert request["additionalProperties"] is False
    assert set(request["properties"]) == {"semester_name", "course_ids"}
