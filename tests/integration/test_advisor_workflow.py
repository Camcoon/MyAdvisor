"""Real-auth advisor/cross-workflow coverage traced to the approved IT plan.

Reuse F2's per-case database, separate cookie jars and fresh-session snapshots.
No authentication, service, repository or request handler is mocked.
"""

from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib.parse import urlencode, urlsplit

import jwt
import pytest

pytestmark = pytest.mark.integration

ADVISOR_API = "/api/advisor/plans"
STUDENT_API = "/api/semester-plans"
T1 = "Year 1 semester 1"
DECISIONS = {
    "approve": ("Approved", "Plan approved."),
    "reject": ("Rejected", "Plan rejected."),
    "request_changes": (
        "Changes Requested",
        "Changes requested. The student can revise and resubmit this plan.",
    ),
}
TRANSPORTS = ["json", "form", "api", "named-api"]


class ReviewForms(HTMLParser):
    """Extract the actual queue's review targets, excluding navigation/scripts."""

    def __init__(self, html):
        super().__init__()
        self.ids = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        path = urlsplit(attrs.get("action", "")).path
        if tag == "form" and path.startswith("/admin/review/"):
            assert attrs.get("method", "").lower() == "post"
            self.ids.append(int(path.rsplit("/", 1)[1]))


def queue(client, expected_ids):
    page = client.get("/admin")
    assert page.status_code == 200
    assert page.headers["content-type"].startswith("text/html")
    assert ReviewForms(page.text).ids == expected_ids
    response = client.get(ADVISOR_API)
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert [row["id"] for row in response.json()] == expected_ids
    return page, response.json()


def review(client, plan_id, decision, feedback="", transport="json"):
    payload = {"decision": decision, "feedback": feedback}
    if transport in ("json", "form"):
        return client.post(
            f"/admin/review/{plan_id}",
            **{("data" if transport == "form" else "json"): payload},
        )
    suffix = "review"
    if transport == "named-api":
        suffix = decision.replace("_", "-")
        payload.pop("decision")
    return client.post(f"{ADVISOR_API}/{plan_id}/{suffix}", json=payload)


def review_response(client, response, transport, decision=None, error=None, code=422):
    if transport in ("json", "form"):
        assert response.status_code == 303, response.text
        assert urlsplit(response.headers["location"]).path == "/admin"
        page = client.get(response.headers["location"])
        assert page.status_code == 200
        assert (error or DECISIONS[decision][1]) in page.text
    elif error:
        assert response.status_code == code, response.text
        detail = response.json()["detail"]
        if isinstance(detail, dict):
            assert detail == {
                "code": {422: "invalid_plan", 409: "plan_conflict", 404: "not_found"}[code],
                "message": error,
            }
        else:
            # Schema validation (e.g. feedback >500) precedes service validation.
            assert isinstance(detail, list) and detail
            assert detail[0]["loc"] == ["body", "feedback"]
            assert detail[0]["type"] == "string_too_long"
    else:
        assert response.status_code == 200, response.text
        assert response.json()["status"] == DECISIONS[decision][0]


def assert_only_review_changed(env, before, plan_id, decision, feedback):
    expected = {
        **before,
        "semesterplan": [
            {
                **row,
                "status": DECISIONS[decision][0],
                "advisor_id": env.ids["a1"],
                "advisor_feedback": feedback.strip(),
            } if row["id"] == plan_id else row
            for row in before["semesterplan"]
        ],
    }
    assert env.snapshot() == expected


@pytest.mark.it("IT-03")
@pytest.mark.it("IT-04")
def test_advisor_queue_receives_real_student_submission_and_only_pending_plans(student):
    env, client = student.env, student.client
    advisor = env.login("a1")
    before = env.snapshot()
    queue(advisor, [])
    assert env.snapshot() == before
    for status in ("Approved", "Rejected", "Changes Requested", "Cancelled"):
        env.seed_plan(status=status, actor="s2")
    other_pending = env.seed_plan(actor="s2", courses=("c3",))
    response = client.post(
        "/app/plan",
        content=urlencode(
            {"semester_name": T1, "course_ids": [env.ids["c3"], env.ids["c4"]]},
            doseq=True,
        ),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 303
    location = response.headers["location"]
    assert urlsplit(location).path == "/app"
    assert "Semester plan submitted for advisor review." in client.get(location).text
    plan = env.snapshot()["semesterplan"][-1]
    assert plan["student_id"] == env.ids["s1"] and plan["status"] == "Pending"
    assert plan["advisor_id"] is None and plan["advisor_feedback"] == ""
    assert env.courses(plan["id"]) == [env.ids["c3"], env.ids["c4"]]
    saved = env.snapshot()
    page, rows = queue(advisor, [other_pending, plan["id"]])
    for text in ("TEST-s1", "TEST-s2", "Computer Science", "COMP 2000", "MATH 2000"):
        assert text in page.text
    row = rows[1]
    assert row["student"]["id"] == env.ids["s1"]
    assert row["program"]["total_credits"] == 93
    assert [course["id"] for course in row["courses"]] == env.courses(plan["id"])
    assert env.snapshot() == saved


@pytest.mark.it("IT-05")
@pytest.mark.it("IT-06")
@pytest.mark.it("IT-11")
@pytest.mark.parametrize("transport", TRANSPORTS)
@pytest.mark.parametrize("decision", DECISIONS)
@pytest.mark.parametrize("feedback", ["", "  Please choose another course.  "])
def test_advisor_decision_persists_and_student_receives_only_own_feedback(
    student, transport, decision, feedback
):
    env, client = student.env, student.client
    advisor, other_student = env.login("a1"), env.login("s2")
    plan_id = env.seed_plan()
    other_id = env.seed_plan(actor="s2")
    before = env.snapshot()
    queue(advisor, [plan_id, other_id])
    response = review(advisor, plan_id, decision, feedback, transport)
    review_response(advisor, response, transport, decision=decision)
    assert_only_review_changed(env, before, plan_id, decision, feedback)
    queue(advisor, [other_id])
    own = client.get(f"{STUDENT_API}/{plan_id}")
    assert own.status_code == 200
    assert own.json()["status"] == DECISIONS[decision][0]
    assert own.json()["advisor_feedback"] == feedback.strip()
    messages = client.get("/app?tab=messages")
    assert messages.status_code == 200
    assert DECISIONS[decision][0] in messages.text
    if feedback:
        assert feedback.strip() in messages.text
    assert "Private feedback for s2" not in messages.text
    private_page = other_student.get("/app?tab=messages")
    assert private_page.status_code == 200
    assert "Private feedback for s2" in private_page.text
    assert "Please choose another course." not in private_page.text
    assert other_student.get(f"{STUDENT_API}/{plan_id}").status_code == 404
    # Reads and rendering must leave the decision, history and every link intact.
    assert_only_review_changed(env, before, plan_id, decision, feedback)


@pytest.mark.parametrize(
    "first_decision",
    [
        pytest.param("request_changes", marks=pytest.mark.it("IT-06")),
        pytest.param("reject", marks=pytest.mark.it("IT-07")),
    ],
)
@pytest.mark.it("IT-04")
@pytest.mark.parametrize("transport", ["json", "form", "api"])
def test_student_resubmits_reviewed_plan_and_advisor_reviews_replacement(
    student, first_decision, transport
):
    env, client = student.env, student.client
    advisor = env.login("a1")
    plan_id = env.seed_plan(courses=("c3",))
    old = env.plan(plan_id)
    before = env.snapshot()
    feedback = "  Choose another course.  "
    response = review(advisor, plan_id, first_decision, feedback, transport)
    review_response(advisor, response, transport, decision=first_decision)
    assert_only_review_changed(env, before, plan_id, first_decision, feedback)
    queue(advisor, [])
    messages = client.get("/app?tab=messages")
    assert messages.status_code == 200
    assert "Choose another course." in messages.text
    reviewed = env.snapshot()
    response = client.post(
        "/app/plan", data={"semester_name": T1, "course_ids": env.ids["c4"]}
    )
    assert response.status_code == 303
    page = client.get(response.headers["location"])
    assert page.status_code == 200
    assert "Semester plan submitted for advisor review." in page.text
    plan = env.plan(plan_id)
    assert plan == {
        **old, "status": "Pending", "advisor_id": None, "advisor_feedback": "",
        "submitted_at": plan["submitted_at"],
    }
    assert plan["submitted_at"] > old["submitted_at"]
    saved = env.snapshot()
    assert len(saved["semesterplan"]) == 1
    assert len(saved["plancourse"]) == 1
    assert env.courses(plan_id) == [env.ids["c4"]]
    for table in saved.keys() - {"semesterplan", "plancourse"}:
        assert saved[table] == reviewed[table]
    _, rows = queue(advisor, [plan_id])
    assert rows[0]["advisor_id"] is None and rows[0]["advisor_feedback"] == ""
    assert [course["id"] for course in rows[0]["courses"]] == [env.ids["c4"]]
    # A fresh advisor login must see the replacement and can approve the same ID.
    advisor = env.login("a1")
    response = review(advisor, plan_id, "approve", "Revised plan approved.", transport)
    review_response(advisor, response, transport, decision="approve")
    assert_only_review_changed(env, saved, plan_id, "approve", "Revised plan approved.")
    queue(advisor, [])
    final = client.get(f"{STUDENT_API}/{plan_id}")
    assert final.status_code == 200
    assert final.json()["status"] == "Approved"
    assert final.json()["advisor_feedback"] == "Revised plan approved."
    assert [course["id"] for course in final.json()["courses"]] == [env.ids["c4"]]
    messages = client.get("/app?tab=messages")
    assert messages.status_code == 200 and "Revised plan approved." in messages.text
    assert "Choose another course." not in messages.text


@pytest.mark.it("IT-08")
def test_cancelled_plan_leaves_advisor_queue_and_replacement_returns(student):
    env, client = student.env, student.client
    advisor = env.login("a1")
    plan_id = env.seed_plan()
    queue(advisor, [plan_id])
    before = env.snapshot()
    response = client.post(f"/app/plan/{plan_id}/cancel")
    assert response.status_code == 303
    assert "Semester plan cancelled." in client.get(response.headers["location"]).text
    assert env.plan(plan_id) == {**before["semesterplan"][0], "status": "Cancelled"}
    assert env.snapshot()["plancourse"] == before["plancourse"]
    queue(advisor, [])
    response = client.post(
        "/app/plan", data={"semester_name": T1, "course_ids": env.ids["c4"]}
    )
    assert response.status_code == 303
    plans = env.snapshot()["semesterplan"]
    assert len(plans) == 2 and plans[1]["id"] != plan_id
    assert plans[0]["status"] == "Cancelled" and plans[1]["status"] == "Pending"
    assert env.courses(plans[1]["id"]) == [env.ids["c4"]]
    saved = env.snapshot()
    queue(advisor, [plans[1]["id"]])
    assert env.snapshot() == saved


@pytest.mark.it("IT-16")
@pytest.mark.parametrize(
    "body,status,detail",
    [
        ("{", 400, "Invalid JSON request body."),
        ("[]", 422, "The review payload must be a JSON object."),
        ("null", 422, "The review payload must be a JSON object."),
        ('"approve"', 422, "The review payload must be a JSON object."),
        ("{}", 422, "decision"),
        ('{"decision":""}', 422, "decision"),
        ('{"decision":12}', 422, "decision"),
        ('{"decision":"approve","feedback":null}', 422, "Feedback must be a string."),
        ('{"decision":"approve","feedback":[]}', 422, "Feedback must be a string."),
        ('{"decision":"approve","feedback":12}', 422, "Feedback must be a string."),
    ],
)
def test_invalid_review_json_is_rejected_before_writes(student_env, body, status, detail):
    env = student_env
    advisor, plan_id = env.login("a1"), env.seed_plan()
    before = env.snapshot()
    response = advisor.post(
        f"/admin/review/{plan_id}", content=body,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == status
    if detail == "decision":
        assert response.json()["detail"][0]["loc"] == ["body", "decision"]
        assert response.json()["detail"][0]["type"] == "missing"
    else:
        assert response.json() == {"detail": detail}
    assert env.snapshot() == before


@pytest.mark.it("IT-16")
def test_noninteger_review_path_is_rejected_without_writes(student_env):
    env = student_env
    advisor = env.login("a1")
    env.seed_plan()
    before = env.snapshot()
    response = review(advisor, "abc", "approve")
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "plan_id"]
    assert env.snapshot() == before


@pytest.mark.it("IT-17")
@pytest.mark.parametrize("transport", ["json", "form", "api"])
@pytest.mark.parametrize("decision", ["invalid", "Approve", "approved", " "])
def test_unknown_decision_is_rejected_without_writes(student_env, transport, decision):
    env = student_env
    advisor, plan_id = env.login("a1"), env.seed_plan()
    before = env.snapshot()
    response = review(advisor, plan_id, decision, "Must not persist", transport)
    review_response(
        advisor, response, transport, error="Choose approve, reject, or request changes."
    )
    assert env.snapshot() == before


@pytest.mark.it("IT-17")
@pytest.mark.parametrize("transport", ["json", "form", "api"])
@pytest.mark.parametrize("decision", DECISIONS)
@pytest.mark.parametrize("length", [499, 500])
def test_feedback_at_limit_is_accepted(student_env, transport, decision, length):
    env = student_env
    advisor, plan_id = env.login("a1"), env.seed_plan()
    before = env.snapshot()
    feedback = "x" * length
    response = review(advisor, plan_id, decision, feedback, transport)
    review_response(advisor, response, transport, decision=decision)
    assert_only_review_changed(env, before, plan_id, decision, feedback)


@pytest.mark.it("IT-17")
@pytest.mark.parametrize("transport", TRANSPORTS)
@pytest.mark.parametrize("decision", DECISIONS)
@pytest.mark.parametrize("feedback", ["x" * 501, " " * 501], ids=["text", "spaces"])
def test_feedback_over_limit_is_rejected_before_trimming(
    student_env, transport, decision, feedback
):
    env = student_env
    advisor, plan_id = env.login("a1"), env.seed_plan()
    before = env.snapshot()
    response = review(advisor, plan_id, decision, feedback, transport)
    review_response(
        advisor, response, transport,
        error="Advisor feedback must be 500 characters or fewer.",
    )
    assert env.snapshot() == before


@pytest.mark.it("IT-17")
@pytest.mark.parametrize("transport", TRANSPORTS)
@pytest.mark.parametrize("decision", DECISIONS)
def test_already_reviewed_plan_cannot_be_reviewed_again(student_env, transport, decision):
    env = student_env
    advisor, plan_id = env.login("a1"), env.seed_plan()
    first = review(advisor, plan_id, "approve", "Original review", transport)
    review_response(advisor, first, transport, decision="approve")
    before = env.snapshot()
    response = review(advisor, plan_id, decision, "Overwrite attempt", transport)
    review_response(
        advisor, response, transport, error="Only pending plans can be reviewed.", code=409
    )
    assert env.snapshot() == before


@pytest.mark.it("IT-17")
@pytest.mark.parametrize("transport", ["json", "form", "api"])
@pytest.mark.parametrize("status", ["Approved", "Rejected", "Changes Requested", "Cancelled"])
def test_nonpending_status_rejects_review(student_env, transport, status):
    env = student_env
    advisor, plan_id = env.login("a1"), env.seed_plan(status=status)
    before = env.snapshot()
    response = review(advisor, plan_id, "approve", "Overwrite attempt", transport)
    review_response(
        advisor, response, transport, error="Only pending plans can be reviewed.", code=409
    )
    assert env.snapshot() == before


@pytest.mark.it("IT-17")
@pytest.mark.parametrize("transport", ["json", "form", "api"])
def test_missing_plan_rejects_review(student_env, transport):
    env = student_env
    advisor = env.login("a1")
    env.seed_plan()
    before = env.snapshot()
    response = review(advisor, 999999, "approve", transport=transport)
    review_response(advisor, response, transport, error="Plan not found.", code=404)
    assert env.snapshot() == before


def advisor_requests(plan_id):
    """Every protected advisor read/write route with otherwise valid input."""
    yield "GET", "/admin", {}
    yield "GET", ADVISOR_API, {}
    yield "GET", f"{ADVISOR_API}/{plan_id}", {}
    for decision in DECISIONS:
        payload = {"decision": decision, "feedback": "Unauthorized review"}
        for encoding in ("json", "data"):
            yield "POST", f"/admin/review/{plan_id}", {encoding: payload}
        yield "POST", f"{ADVISOR_API}/{plan_id}/review", {"json": payload}
        yield "POST", f"{ADVISOR_API}/{plan_id}/{decision.replace('_', '-')}", {
            "json": {"feedback": "Unauthorized review"}
        }


@pytest.mark.it("IT-13")
def test_students_cannot_access_advisor_queue_or_decisions(student):
    env, client = student.env, student.client
    plan_id = env.seed_plan(actor="s2")
    before = env.snapshot()
    for method, url, kwargs in advisor_requests(plan_id):
        response = client.request(method, url, **kwargs)
        assert response.status_code == 403, (method, url, response.text)
        assert response.json() == {"detail": "You are not authorized to access this resource"}
        assert "Private profile s2" not in response.text
        assert "Private feedback for s2" not in response.text
        assert env.snapshot() == before


@pytest.mark.it("IT-12")
@pytest.mark.parametrize("token_case", ["missing", "malformed", "expired", "signature", "missing-user"])
def test_advisor_endpoints_deny_unauthenticated_and_invalid_tokens(student_env, token_case):
    from app.config import get_settings

    env = student_env
    plan_id = env.seed_plan(actor="s2")
    before = env.snapshot()
    client = env.client()
    if token_case != "missing":
        settings = get_settings()
        claims = {
            "sub": str(env.ids["a1"]),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        key = settings.secret_key
        if token_case == "expired":
            claims["exp"] = datetime(2000, 1, 1, tzinfo=timezone.utc)
        elif token_case == "signature":
            key = "incorrect-advisor-test-signing-key-32-bytes"
        elif token_case == "missing-user":
            claims["sub"] = "999999"
        token = "not-a-token" if token_case == "malformed" else jwt.encode(
            claims, key, algorithm=settings.jwt_algorithm
        )
        client.cookies.set("access_token", token)
    for method, url, kwargs in advisor_requests(plan_id):
        response = client.request(method, url, **kwargs)
        assert response.status_code == 401, (method, url, response.text)
        if url.startswith("/api/"):
            assert response.json() == {"detail": "Could not validate credentials"}
        else:
            assert "Return to Login" in response.text
        for private_text in ("Private profile s2", "Private feedback for s2", "TEST-s2"):
            assert private_text not in response.text
        assert env.snapshot() == before
