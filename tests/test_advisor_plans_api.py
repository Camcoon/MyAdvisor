"""Workflow 3 integration coverage using real cookie auth and persisted reviews."""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event, text
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from app import database
from app.main import app
from app.models.advising import Course, DegreeProgram, PlanCourse, SemesterPlan
from app.models.user import User
from app.repositories.advising import AdvisingRepository
from app.schemas.advising import AdvisorPlanResponse
from app.services.advising_errors import PlanValidationError
from app.services.advising_service import AdvisingService
from app.utilities.security import create_access_token

BASE = "/api/advisor/plans"
DECISIONS = {
    "approve": "Approved",
    "reject": "Rejected",
    "request_changes": "Changes Requested",
}
ACTIONS = ["review", "approve", "reject", "request-changes"]
OPERATIONS = [("GET", "", None), ("GET", "/{id}", None)] + [
    ("POST", f"/{{id}}/{action}", {"decision": "approve"} if action == "review" else {})
    for action in ACTIONS
]


@pytest.fixture
def advisor_client(monkeypatch):
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _record):
        connection.execute("PRAGMA foreign_keys=ON")

    SQLModel.metadata.create_all(engine)
    monkeypatch.setattr(database, "engine", engine)
    with Session(engine) as session:
        session.add(DegreeProgram(id=1, name="Computer Science", total_credits=93))
        session.commit()
        session.add_all([
            User(
                id=i, username=f"user-{i}", email=f"private-{i}@example.com",
                password="private-password-hash", role=role, name=f"Person {i}",
                student_number=f"STU-{i}" if i in (1, 2) else None,
                degree_program=1 if i == 1 else None,
            )
            for i, role in [(1, "regular_user"), (2, "regular_user"),
                            (3, "admin"), (4, "unknown"), (5, "admin")]
        ])
        session.add_all([
            Course(id=1, code="COMP 1000", title="Foundations"),
            Course(id=2, code="COMP 2000", title="Algorithms",
                   prerequisite_text="COMP 1000"),
        ])
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


def authenticate(client, user_id=3, role="regular_user"):
    # The database role must take precedence over even an opposing JWT claim.
    client.cookies.set(
        "access_token", create_access_token({"sub": str(user_id), "role": role})
    )


def seed_plan(engine, status="Pending", student_id=1, submitted_at=None):
    with Session(engine) as session:
        plan = AdvisingRepository(session).create_plan(
            student_id, [1, 2], semester_name="Year 1 semester 2"
        )
        plan.status = status
        if status != "Pending":
            plan.advisor_id = 5
            plan.advisor_feedback = "Original decision."
        if submitted_at is not None:
            plan.submitted_at = submitted_at
        session.add(plan)
        session.commit()
        return plan.id


def snapshot(engine):
    with Session(engine) as session:
        return {
            "plans": [row.model_dump() for row in session.exec(
                select(SemesterPlan).order_by(SemesterPlan.id)
            ).all()],
            "courses": [row.model_dump() for row in session.exec(
                select(PlanCourse).order_by(PlanCourse.id)
            ).all()],
        }


def assert_error(response, status, code=None):
    assert response.status_code == status, response.text
    assert response.headers["content-type"] == "application/json"
    assert "location" not in response.headers
    if code:
        assert response.json()["detail"]["code"] == code
        assert response.headers["cache-control"] == "no-store"


def test_queue_and_detail_reuse_dashboard_data_without_account_secrets(advisor_client):
    client, engine = advisor_client
    assert client.get(BASE).json() == []
    newer = seed_plan(engine, submitted_at=datetime(2026, 2, 1, tzinfo=timezone.utc))
    older = seed_plan(engine, student_id=2,
                      submitted_at=datetime(2026, 1, 1, tzinfo=timezone.utc))
    history = [seed_plan(engine, state) for state in
               ["Approved", "Rejected", "Changes Requested", "Cancelled"]]
    before = snapshot(engine)
    response = client.get(BASE, params={"advisor_id": 5, "student_id": 2})
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    plans = response.json()
    assert [plan["id"] for plan in plans] == [older, newer]
    with Session(engine) as session:
        queue = AdvisingService(session).get_advisor_dashboard(3)
        assert [item["plan"].id for item in queue] == [older, newer]
    for plan in plans:
        AdvisorPlanResponse.model_validate(plan)
        assert set(plan) == {
            "id", "semester_name", "status", "submitted_at", "advisor_feedback",
            "courses", "advisor_id", "student", "program",
        }
        assert set(plan["student"]) == {"id", "name", "username", "student_number"}
        assert [course["id"] for course in plan["courses"]] == [1, 2]
        assert "private-" not in str(plan)
        assert "password" not in str(plan)
        detail = client.get(f"{BASE}/{plan['id']}")
        assert detail.status_code == 200
        assert detail.json() == plan
    assert plans[0]["program"] is None
    assert plans[1]["program"]["name"] == "Computer Science"
    for plan_id in history:
        # Reading history is allowed; only pending plans can receive decisions.
        assert client.get(f"{BASE}/{plan_id}").status_code == 200
    assert snapshot(engine) == before


@pytest.mark.parametrize("method,suffix,payload", OPERATIONS)
@pytest.mark.parametrize("credential", ["missing", "malformed", "expired", "deleted"])
def test_all_operations_require_valid_cookie(advisor_client, method, suffix, payload,
                                             credential):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    client.cookies.clear()
    if credential == "malformed":
        client.cookies.set("access_token", "not-a-token")
    elif credential == "deleted":
        authenticate(client, 999, "admin")
    elif credential == "expired":
        client.cookies.set("access_token", create_access_token(
            {"sub": "3"}, expires_delta=timedelta(minutes=-5)
        ))
    response = client.request(method, BASE + suffix.format(id=plan_id), json=payload,
                              headers={"Accept": "text/html"})
    assert_error(response, 401)
    assert snapshot(engine) == before


@pytest.mark.parametrize("method,suffix,payload", OPERATIONS)
@pytest.mark.parametrize("user_id", [1, 2, 4])
def test_students_and_unknown_roles_cannot_read_or_decide(advisor_client, method,
                                                         suffix, payload, user_id):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    authenticate(client, user_id, "admin")
    response = client.request(method, BASE + suffix.format(id=plan_id), json=payload)
    assert_error(response, 403)
    assert snapshot(engine) == before


def test_role_revocation_applies_to_existing_advisor_cookie(advisor_client):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    assert client.get(BASE).status_code == 200
    with Session(engine) as session:
        user = session.get(User, 3)
        user.role = "regular_user"
        session.add(user)
        session.commit()
    assert_error(client.get(BASE), 403)
    assert_error(client.post(f"{BASE}/{plan_id}/approve", json={}), 403)
    assert snapshot(engine)["plans"][0]["status"] == "Pending"


@pytest.mark.parametrize("decision,status", DECISIONS.items())
@pytest.mark.parametrize("generic", [False, True])
def test_decisions_persist_authenticated_advisor_and_trimmed_feedback(
    advisor_client, decision, status, generic
):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    action = "review" if generic else decision.replace("_", "-")
    payload = {"feedback": "  Please review the course load.  "}
    if generic:
        payload["decision"] = decision
    response = client.post(f"{BASE}/{plan_id}/{action}", json=payload,
                           params={"advisor_id": 5}, headers={"X-Advisor-ID": "5"})
    assert response.status_code == 200, response.text
    assert response.headers["cache-control"] == "no-store"
    assert response.json()["status"] == status
    assert response.json()["advisor_id"] == 3
    assert response.json()["advisor_feedback"] == "Please review the course load."
    after = snapshot(engine)
    assert after["courses"] == before["courses"]
    assert after["plans"] == [{**before["plans"][0], "status": status,
                               "advisor_id": 3,
                               "advisor_feedback": "Please review the course load."}]
    assert client.get(BASE).json() == []
    assert client.get(f"{BASE}/{plan_id}").json() == response.json()
    authenticate(client, 1)
    student_plan = client.get(f"/api/semester-plans/{plan_id}")
    assert student_plan.json()["status"] == status
    assert student_plan.json()["advisor_feedback"] == "Please review the course load."
    assert "advisor_id" not in student_plan.json()


@pytest.mark.parametrize("action", ACTIONS)
@pytest.mark.parametrize("feedback", ["", " ", "é" * 500])
def test_optional_feedback_and_exact_limit(advisor_client, action, feedback):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    payload = {"feedback": feedback}
    if action == "review":
        payload["decision"] = "approve"
    response = client.post(f"{BASE}/{plan_id}/{action}", json=payload)
    assert response.status_code == 200
    assert response.json()["advisor_feedback"] == feedback.strip()
    assert snapshot(engine)["plans"][0]["advisor_feedback"] == feedback.strip()


@pytest.mark.parametrize("action", ACTIONS)
@pytest.mark.parametrize("feedback", ["x" * 501, " " * 501, None, 10, [], {}, True])
def test_invalid_feedback_cannot_mutate_plan(advisor_client, action, feedback):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    payload = {"feedback": feedback}
    if action == "review":
        payload["decision"] = "approve"
    assert_error(client.post(f"{BASE}/{plan_id}/{action}", json=payload), 422)
    assert snapshot(engine) == before


@pytest.mark.parametrize("decision", ["", "APPROVE", "Approved", "cancel",
                                      "request-changes", " approve ", None, 1, [], {}])
def test_invalid_decisions_are_rejected(advisor_client, decision):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    response = client.post(f"{BASE}/{plan_id}/review", json={"decision": decision})
    assert_error(response, 422, "invalid_plan" if isinstance(decision, str) else None)
    assert snapshot(engine) == before


@pytest.mark.parametrize("action", ACTIONS)
@pytest.mark.parametrize("extra", ["advisor_id", "student_id", "status", "advisor_feedback"])
def test_server_owned_fields_are_rejected(advisor_client, action, extra):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    payload = {extra: "spoofed"}
    if action == "review":
        payload["decision"] = "approve"
    assert_error(client.post(f"{BASE}/{plan_id}/{action}", json=payload), 422)
    assert snapshot(engine) == before


@pytest.mark.parametrize("action", ACTIONS)
@pytest.mark.parametrize("body", [None, "{", "[]", '"approve"', "null"])
def test_missing_or_malformed_json(advisor_client, action, body):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    response = client.post(f"{BASE}/{plan_id}/{action}", content=body,
                           headers={"Content-Type": "application/json"})
    assert_error(response, 422)
    assert snapshot(engine) == before


def test_review_requires_decision_and_action_routes_cannot_override_it(advisor_client):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    assert_error(client.post(f"{BASE}/{plan_id}/review", json={}), 422)
    assert_error(client.post(f"{BASE}/{plan_id}/approve",
                             json={"decision": "reject"}), 422)
    assert snapshot(engine) == before
    assert client.post(f"{BASE}/{plan_id}/request-changes", json={}).status_code == 200
    assert snapshot(engine)["plans"][0]["advisor_feedback"] == ""


@pytest.mark.parametrize("action", ACTIONS)
@pytest.mark.parametrize("state", ["Approved", "Rejected", "Changes Requested", "Cancelled"])
def test_no_longer_pending_plans_cannot_be_reviewed(advisor_client, action, state):
    client, engine = advisor_client
    plan_id = seed_plan(engine, state)
    before = snapshot(engine)
    payload = {"decision": "approve"} if action == "review" else {}
    assert_error(client.post(f"{BASE}/{plan_id}/{action}", json=payload),
                 409, "plan_conflict")
    assert snapshot(engine) == before


def test_another_advisor_cannot_overwrite_a_completed_review(advisor_client):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    assert client.post(f"{BASE}/{plan_id}/approve", json={}).status_code == 200
    before = snapshot(engine)
    authenticate(client, 5)
    assert_error(client.post(f"{BASE}/{plan_id}/reject", json={"feedback": "No"}),
                 409, "plan_conflict")
    assert snapshot(engine) == before


@pytest.mark.parametrize("method,suffix,payload", OPERATIONS[1:])
def test_missing_plans_return_json_404(advisor_client, method, suffix, payload):
    client, _ = advisor_client
    assert_error(client.request(method, BASE + suffix.format(id=999), json=payload),
                 404, "not_found")


@pytest.mark.parametrize("method,suffix,payload", OPERATIONS[1:])
@pytest.mark.parametrize("plan_id", ["0", "-1", "abc", str(2**63)])
def test_invalid_plan_ids(advisor_client, method, suffix, payload, plan_id):
    client, _ = advisor_client
    assert_error(client.request(method, BASE + suffix.format(id=plan_id), json=payload),
                 422)


@pytest.mark.parametrize("state", ["Approved", "Cancelled"])
def test_stale_read_cannot_overwrite_a_newer_status(advisor_client, monkeypatch, state):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    original = AdvisingRepository.get_plan_by_id

    def read_then_change_status(repo, resource_id):
        stale_plan = original(repo, resource_id)
        # Deterministically simulate a competing commit after the service read.
        with Session(engine) as session:
            current = session.get(SemesterPlan, resource_id)
            current.status = state
            current.advisor_id = 5
            current.advisor_feedback = "Committed by another request."
            session.add(current)
            session.commit()
        return stale_plan

    monkeypatch.setattr(AdvisingRepository, "get_plan_by_id", read_then_change_status)
    assert_error(client.post(f"{BASE}/{plan_id}/reject", json={"feedback": "Stale"}),
                 409, "plan_conflict")
    stored = snapshot(engine)["plans"][0]
    assert stored["status"] == state
    assert stored["advisor_id"] == 5
    assert stored["advisor_feedback"] == "Committed by another request."


@pytest.mark.parametrize("operational", [False, True])
def test_database_errors_roll_back_and_hide_internal_details(advisor_client, operational):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    statement = ("SELECT * FROM private_missing_table;" if operational
                 else "SELECT RAISE(ABORT, 'private database details');")
    with engine.begin() as connection:
        connection.execute(text(
            "CREATE TRIGGER fail_review BEFORE UPDATE ON semesterplan "
            f"BEGIN {statement} END"
        ))
    response = client.post(f"{BASE}/{plan_id}/approve", json={"feedback": "Approved"})
    assert_error(response, 503 if operational else 409,
                 "database_unavailable" if operational else "plan_conflict")
    assert "private" not in response.text
    assert snapshot(engine) == before
    with engine.begin() as connection:
        connection.execute(text("DROP TRIGGER fail_review"))
    assert client.post(f"{BASE}/{plan_id}/approve", json={}).status_code == 200


@pytest.mark.parametrize("json_form", [False, True])
@pytest.mark.parametrize("decision,status", DECISIONS.items())
def test_original_dashboard_and_review_forms_remain_compatible(
    advisor_client, json_form, decision, status
):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    dashboard = client.get("/admin")
    assert dashboard.status_code == 200
    assert "text/html" in dashboard.headers["content-type"]
    assert f'action="http://testserver/admin/review/{plan_id}"' in dashboard.text
    payload = {"decision": decision, "feedback": "  Form feedback  "}
    response = client.post(f"/admin/review/{plan_id}",
                           **({"json": payload} if json_form else {"data": payload}))
    assert response.status_code == 303
    assert response.headers["location"].endswith("/admin")
    stored = snapshot(engine)["plans"][0]
    assert (stored["status"], stored["advisor_id"], stored["advisor_feedback"]) == (
        status, 3, "Form feedback"
    )
    assert client.get(BASE).json() == []
    assert "All caught up" in client.get("/admin").text
    # A stale HTML submission still flashes a warning and redirects.
    assert client.post(f"/admin/review/{plan_id}", data=payload).status_code == 303
    assert snapshot(engine)["plans"][0] == stored


@pytest.mark.parametrize("payload", [
    {"decision": "approve", "feedback": "x" * 501},
    {"decision": "invalid", "feedback": ""},
])
def test_existing_form_service_validation_remains_in_force(advisor_client, payload):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    response = client.post(f"/admin/review/{plan_id}", data=payload)
    assert response.status_code == 303
    assert snapshot(engine) == before
    with Session(engine) as session, pytest.raises(PlanValidationError):
        AdvisingService(session).review_plan(plan_id, advisor_id=3, **payload)


def test_students_cannot_use_original_review_route(advisor_client):
    client, engine = advisor_client
    plan_id = seed_plan(engine)
    before = snapshot(engine)
    authenticate(client, 1, "admin")
    assert client.get("/admin").status_code == 403
    for decision in DECISIONS:
        assert client.post(f"/admin/review/{plan_id}", data={
            "decision": decision, "feedback": "Student attempt"
        }).status_code == 403
    assert snapshot(engine) == before


def test_openapi_documents_advisor_resources_and_allowlists(advisor_client):
    client, _ = advisor_client
    schema = client.get("/openapi.json").json()
    for method, suffix, _ in OPERATIONS:
        operation = schema["paths"][BASE + suffix.replace("{id}", "{plan_id}")][
            method.lower()
        ]
        assert "200" in operation["responses"]
    models = schema["components"]["schemas"]
    for name in ["PlanFeedbackRequest", "PlanReviewRequest"]:
        assert models[name]["additionalProperties"] is False
        assert models[name]["properties"]["feedback"]["maxLength"] == 500
    assert set(models["PlanReviewRequest"]["properties"]) == {"feedback", "decision"}
    assert "advisor_id" in models["AdvisorPlanResponse"]["properties"]
