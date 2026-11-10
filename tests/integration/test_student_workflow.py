"""Student portions of IT-01–04, IT-06–12, IT-14–15 and IT-18.

Advisor review transitions are fixture preconditions, not advisor test coverage.
Every negative case compares committed state using independent SQLModel sessions.
"""

from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlencode, urlsplit

import jwt
import pytest

pytestmark = pytest.mark.integration

T1 = "Year 1 semester 1"
T2 = "Year 1 semester 2"
PLAN_API = "/api/semester-plans"
STATUSES = ["Pending", "Approved", "Rejected", "Changes Requested", "Cancelled"]


class CourseInputs(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.courses = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "input" and attrs.get("name") == "course_ids":
            self.courses[int(attrs["value"])] = attrs


def submit(client, ids, courses=("c3", "c4"), semester=T1, **extra):
    # Encode repeated course_ids keys explicitly (httpx 0.28 form handling).
    return client.post(
        "/app/plan",
        content=urlencode(
            {
                "semester_name": semester,
                "course_ids": [ids.get(key, key) for key in courses],
                **extra,
            },
            doseq=True,
        ),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def redirected_page(client, response, message):
    assert response.status_code == 303, response.text
    location = urlsplit(response.headers["location"])
    assert location.path == "/app"
    assert parse_qs(location.query)["tab"] == ["plan-courses"]
    page = client.get(response.headers["location"])
    assert page.status_code == 200
    assert message in page.text
    return page


@pytest.mark.it("IT-01")
def test_student_login_cookie_and_logout(student_env):
    before = student_env.snapshot()
    client = student_env.client()
    response = client.post(
        "/login", data={"username": "s1", "password": "student-integration-password"}
    )
    assert response.status_code == 303
    assert urlsplit(response.headers["location"]).path == "/app"
    cookie = response.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=lax" in cookie
    assert "secure" not in cookie
    dashboard = client.get(response.headers["location"])
    assert dashboard.status_code == 200
    assert "Private profile s1" in dashboard.text
    assert "Private profile s2" not in dashboard.text
    assert client.get("/api/degree-progress").status_code == 200
    logout = client.get("/logout")
    assert logout.status_code == 303
    assert urlsplit(logout.headers["location"]).path == "/login"
    assert "access_token" not in client.cookies
    assert client.get("/app").status_code == 401
    assert client.get("/api/degree-progress").status_code == 401
    assert student_env.snapshot() == before


@pytest.mark.it("IT-01")
@pytest.mark.parametrize(
    "username,password",
    [
        ("s1", "incorrect-password"),
        ("unknown", "student-integration-password"),
    ],
    ids=["wrong-password", "unknown-user"],
)
def test_bad_credentials_never_authenticate(student_env, username, password):
    client = student_env.client()
    before = student_env.snapshot()
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 303
    assert urlsplit(response.headers["location"]).path == "/login"
    assert (
        "Incorrect username or password"
        in client.get(response.headers["location"]).text
    )
    assert "access_token" not in client.cookies
    assert client.get("/app").status_code == 401
    assert student_env.snapshot() == before


@pytest.mark.it("IT-02")
def test_degree_progress_through_authenticated_html_and_json(student):
    env, client = student.env, student.client
    before = env.snapshot()
    response = client.get("/app", params={"tab": "degree-progress", "semester": T1})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    for text in (
        "Computer Science",
        "3 / 93 credits (3%)",
        "3 / 30 credits",
        "27 remaining",
    ):
        assert text in response.text
    assert "Private profile s2" not in response.text
    assert "Feb 2023" not in response.text
    response = client.get("/api/degree-progress")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert {
        key: body[key]
        for key in (
            "total_credits",
            "completed_credits",
            "in_progress_credits",
            "remaining_credits",
            "progress_percent",
        )
    } == {
        "total_credits": 93,
        "completed_credits": 3,
        "in_progress_credits": 3,
        "remaining_credits": 87,
        "progress_percent": 3,
    }
    assert body["category_progress"] == [
        {
            "category": "Core Courses",
            "earned": 3,
            "required": 30,
            "remaining": 27,
            "percent": 10,
        }
    ]
    assert [row["id"] for row in body["completed"]] == [env.ids["c1"]]
    assert [row["id"] for row in body["in_progress"]] == [env.ids["c2"]]
    assert env.snapshot() == before


@pytest.mark.it("IT-03")
def test_available_courses_use_completed_prerequisites_and_tracked_status(student):
    env, client = student.env, student.client
    before = env.snapshot()
    response = client.get("/api/courses")
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    courses = {row["id"]: row for row in response.json()}
    expected = {
        "c1": (False, "Already completed"),
        "c2": (False, "Already in progress"),
        "c3": (True, "Eligible"),
        "c4": (True, "Eligible"),
        "c5": (False, "Missing prerequisite(s): MATH 9999"),
    }
    assert len(courses) == len(expected)
    page = client.get("/app", params={"tab": "plan-courses", "semester": T1})
    assert page.status_code == 200
    inputs = CourseInputs(page.text).courses
    for key, (eligible, reason) in expected.items():
        row = courses[env.ids[key]]
        assert (row["eligible"], row["eligibility_reason"]) == (eligible, reason)
        assert ("disabled" not in inputs[env.ids[key]]) == eligible
    assert env.snapshot() == before


@pytest.mark.it("IT-03")
@pytest.mark.it("IT-04")
@pytest.mark.parametrize(
    "semester",
    [f"Year {year} semester {term}" for year in range(1, 4) for term in range(1, 4)],
)
def test_valid_submission_persists_courses_and_can_be_retrieved(student, semester):
    env, client = student.env, student.client
    response = submit(client, env.ids, semester=f"  {semester}  ")
    page = redirected_page(
        client, response, "Semester plan submitted for advisor review."
    )
    saved = env.snapshot()
    assert len(saved["semesterplan"]) == 1
    plan = saved["semesterplan"][0]
    assert plan["student_id"] == env.ids["s1"]
    assert plan["semester_name"] == semester
    assert plan["status"] == "Pending"
    assert plan["advisor_id"] is None and plan["advisor_feedback"] == ""
    assert isinstance(plan["submitted_at"], datetime)
    assert env.courses(plan["id"]) == [env.ids["c3"], env.ids["c4"]]
    assert len(saved["plancourse"]) == 2
    inputs = CourseInputs(page.text).courses
    assert {cid for cid, attrs in inputs.items() if "checked" in attrs} == {
        env.ids["c3"],
        env.ids["c4"],
    }
    # A second, independently logged-in client proves persistence across clients.
    second = env.login()
    result = second.get(f"{PLAN_API}/{plan['id']}")
    assert result.status_code == 200
    body = result.json()
    assert body["id"] == plan["id"] and body["status"] == "Pending"
    assert body["semester_name"] == semester
    assert [row["id"] for row in body["courses"]] == [env.ids["c3"], env.ids["c4"]]
    assert second.get(PLAN_API).json() == [body]
    assert env.snapshot() == saved


@pytest.mark.it("IT-14")
@pytest.mark.parametrize(
    "semester",
    [
        "",
        " ",
        "Fall 2026",
        "Year 0 semester 1",
        "Year 4 semester 1",
        "Year 1 semester 4",
        "year 1 semester 1",
    ],
)
def test_invalid_semester_rejects_without_writes(student, semester):
    env, client = student.env, student.client
    before = env.snapshot()
    redirected_page(
        client,
        submit(client, env.ids, semester=semester),
        "Choose a valid year and semester before submitting a plan.",
    )
    assert env.snapshot() == before


@pytest.mark.it("IT-14")
@pytest.mark.parametrize(
    "courses,message",
    [
        ((), "Select at least one course"),
        (("c3", "c3"), "A course may only appear once"),
        ((999999,), "Course ID 999999 is no longer available"),
        (("c1",), "COMP 1100: Already completed"),
        (("c2",), "MATH 1000: Already in progress"),
        (("c5",), "Missing prerequisite(s): MATH 9999"),
        (("c3", 999999), "Course ID 999999 is no longer available"),
        (("c3", "c5"), "Missing prerequisite(s): MATH 9999"),
    ],
)
def test_duplicate_missing_or_ineligible_courses_are_atomic_rejections(
    student, courses, message
):
    env, client = student.env, student.client
    before = env.snapshot()
    redirected_page(client, submit(client, env.ids, courses=courses), message)
    assert env.snapshot() == before


@pytest.mark.it("IT-15")
@pytest.mark.parametrize("status", ["Pending", "Approved"])
def test_active_plan_blocks_duplicate_but_allows_different_semester(student, status):
    env, client = student.env, student.client
    env.seed_plan(status=status, courses=("c3",))
    before = env.snapshot()
    redirected_page(
        client,
        submit(client, env.ids, courses=("c4",)),
        "A plan for this semester is already under review or approved.",
    )
    assert env.snapshot() == before
    redirected_page(
        client,
        submit(client, env.ids, courses=("c4",), semester=T2),
        "Semester plan submitted for advisor review.",
    )
    plans = env.snapshot()["semesterplan"]
    assert len(plans) == 2
    assert plans[0] == before["semesterplan"][0]
    assert plans[1]["semester_name"] == T2 and plans[1]["status"] == "Pending"
    assert env.courses(plans[1]["id"]) == [env.ids["c4"]]


@pytest.mark.parametrize(
    "status",
    [
        pytest.param("Changes Requested", marks=pytest.mark.it("IT-06")),
        pytest.param("Rejected", marks=pytest.mark.it("IT-07")),
    ],
)
def test_resubmission_reuses_plan_and_replaces_old_selection(student, status):
    env, client = student.env, student.client
    plan_id = env.seed_plan(status=status, courses=("c3",))
    before = env.plan(plan_id)
    messages = client.get("/app?tab=messages")
    assert messages.status_code == 200 and "Private feedback for s1" in messages.text
    redirected_page(
        client,
        submit(client, env.ids, courses=("c4",)),
        "Semester plan submitted for advisor review.",
    )
    plan = env.plan(plan_id)
    assert len(env.snapshot()["semesterplan"]) == 1
    assert plan["id"] == plan_id and plan["status"] == "Pending"
    assert plan["advisor_id"] is None and plan["advisor_feedback"] == ""
    assert plan["submitted_at"] > before["submitted_at"]
    assert env.courses(plan_id) == [env.ids["c4"]]
    result = client.get(f"{PLAN_API}/{plan_id}")
    assert result.status_code == 200
    assert result.json()["advisor_feedback"] == ""
    assert [row["id"] for row in result.json()["courses"]] == [env.ids["c4"]]


@pytest.mark.it("IT-14")
@pytest.mark.parametrize("status", ["Rejected", "Changes Requested"])
def test_invalid_resubmission_preserves_review_and_old_courses(student, status):
    env, client = student.env, student.client
    env.seed_plan(status=status, courses=("c3",))
    before = env.snapshot()
    redirected_page(
        client,
        submit(client, env.ids, courses=("c4", "c5")),
        "Missing prerequisite(s): MATH 9999",
    )
    assert env.snapshot() == before


@pytest.mark.it("IT-08")
@pytest.mark.parametrize("status", ["Pending", "Approved", "Rejected"])
def test_allowed_cancellation_retains_history_and_replacement_gets_new_id(
    student, status
):
    env, client = student.env, student.client
    plan_id = env.seed_plan(status=status)
    old = env.plan(plan_id)
    links = env.snapshot()["plancourse"]
    page = redirected_page(
        client,
        client.post(f"/app/plan/{plan_id}/cancel"),
        "Semester plan cancelled. You can edit it and resubmit.",
    )
    assert env.plan(plan_id) == {**old, "status": "Cancelled"}
    assert env.snapshot()["plancourse"] == links
    assert all(
        "checked" not in attrs for attrs in CourseInputs(page.text).courses.values()
    )
    assert "Selected courses for" not in page.text
    redirected_page(
        client,
        submit(client, env.ids, courses=("c4",)),
        "Semester plan submitted for advisor review.",
    )
    plans = env.snapshot()["semesterplan"]
    assert len(plans) == 2
    assert plans[0] == {**old, "status": "Cancelled"}
    assert plans[1]["id"] != plan_id and plans[1]["status"] == "Pending"
    assert env.courses(plan_id) == [env.ids["c3"], env.ids["c4"]]
    assert env.courses(plans[1]["id"]) == [env.ids["c4"]]


@pytest.mark.it("IT-09")
@pytest.mark.parametrize("status", ["Changes Requested", "Cancelled"])
def test_cancellation_rejected_for_forbidden_status(student, status):
    env, client = student.env, student.client
    plan_id = env.seed_plan(status=status)
    before = env.snapshot()
    redirected_page(
        client,
        client.post(f"/app/plan/{plan_id}/cancel"),
        "Only pending, rejected, or approved plans can be cancelled.",
    )
    assert env.snapshot() == before


@pytest.mark.it("IT-10")
def test_pending_plan_can_remove_course_but_keeps_last_course(student):
    env, client = student.env, student.client
    plan_id = env.seed_plan()
    plan = env.plan(plan_id)
    redirected_page(
        client,
        client.post(f"/app/plan/{plan_id}/courses/{env.ids['c4']}/remove"),
        "Course removed from the submitted plan.",
    )
    assert env.courses(plan_id) == [env.ids["c3"]]
    assert env.plan(plan_id) == plan
    before = env.snapshot()
    redirected_page(
        client,
        client.post(f"/app/plan/{plan_id}/courses/{env.ids['c3']}/remove"),
        "Cancel the semester plan to remove its last course.",
    )
    assert env.snapshot() == before


@pytest.mark.it("IT-10")
@pytest.mark.parametrize("status", STATUSES[1:])
def test_course_removal_rejected_for_non_pending_plan(student, status):
    env, client = student.env, student.client
    plan_id = env.seed_plan(status=status)
    before = env.snapshot()
    redirected_page(
        client,
        client.post(f"/app/plan/{plan_id}/courses/{env.ids['c4']}/remove"),
        "Only courses in pending plans can be removed.",
    )
    assert env.snapshot() == before


@pytest.mark.it("IT-11")
def test_other_students_plan_and_private_data_are_inaccessible(student):
    env, client = student.env, student.client
    foreign_id = env.seed_plan(actor="s2")
    before = env.snapshot()
    owner = env.login("s2")
    own_response = owner.get(f"{PLAN_API}/{foreign_id}")
    assert own_response.status_code == 200
    assert own_response.json()["advisor_feedback"] == "Private feedback for s2"
    assert client.get(PLAN_API).json() == []
    for tab in ("degree-progress", "messages", "plan-courses"):
        page = client.get("/app", params={"tab": tab, "student_id": env.ids["s2"]})
        assert page.status_code == 200
        for private_text in (
            "Private profile s2",
            "Private feedback for s2",
            "Feb 2023",
        ):
            assert private_text not in page.text
    # Foreign and nonexistent IDs have the same non-disclosing JSON response.
    foreign = client.get(f"{PLAN_API}/{foreign_id}")
    missing = client.get(f"{PLAN_API}/999999")
    assert foreign.status_code == missing.status_code == 404
    assert foreign.json() == missing.json()
    for url in (
        f"/app/plan/{foreign_id}/cancel",
        f"/app/plan/{foreign_id}/courses/{env.ids['c4']}/remove",
    ):
        redirected_page(client, client.post(url), "Plan not found.")
    for method, url, payload in (
        ("PUT", f"{PLAN_API}/{foreign_id}/courses", {"course_ids": [env.ids["c4"]]}),
        ("DELETE", f"{PLAN_API}/{foreign_id}", None),
        ("DELETE", f"{PLAN_API}/{foreign_id}/courses/{env.ids['c4']}", None),
    ):
        response = client.request(method, url, json=payload)
        assert response.status_code == 404
        assert response.json() == foreign.json()
    assert env.snapshot() == before
    # Ignore client-supplied identity and use the real login cookie.
    redirected_page(
        client,
        submit(client, env.ids, student_id=env.ids["s2"]),
        "Semester plan submitted for advisor review.",
    )
    plans = env.snapshot()["semesterplan"]
    assert len(plans) == 2
    assert plans[0] == before["semesterplan"][0]
    assert plans[1]["student_id"] == env.ids["s1"]
    assert env.courses(foreign_id) == [env.ids["c3"], env.ids["c4"]]
    assert len(owner.get(PLAN_API).json()) == 1
    assert len(client.get(PLAN_API).json()) == 1


@pytest.mark.it("IT-12")
@pytest.mark.parametrize(
    "token_case", ["missing", "malformed", "expired", "signature", "missing-user"]
)
def test_protected_student_requests_deny_invalid_auth_without_writes(
    student_env, token_case
):
    from app.config import get_settings

    env = student_env
    plan_id = env.seed_plan()
    before = env.snapshot()
    client = env.client()
    settings = get_settings()
    if token_case != "missing":
        claims = {
            "sub": str(env.ids["s1"]),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        key = settings.secret_key
        if token_case == "expired":
            claims["exp"] = datetime(2000, 1, 1, tzinfo=timezone.utc)
        elif token_case == "signature":
            key = "incorrect-student-test-signing-key-32-bytes"
        elif token_case == "missing-user":
            claims["sub"] = "999999"
        token = (
            "not-a-token"
            if token_case == "malformed"
            else jwt.encode(claims, key, algorithm=settings.jwt_algorithm)
        )
        client.cookies.set("access_token", token)
    requests = [
        ("GET", "/app", {}),
        ("GET", "/api/degree-progress", {}),
        ("GET", "/api/courses", {}),
        ("GET", PLAN_API, {}),
        ("GET", f"{PLAN_API}/{plan_id}", {}),
        (
            "POST",
            "/app/plan",
            {"data": {"semester_name": T2, "course_ids": env.ids["c3"]}},
        ),
        ("POST", f"/app/plan/{plan_id}/cancel", {}),
        ("POST", f"/app/plan/{plan_id}/courses/{env.ids['c4']}/remove", {}),
        (
            "POST",
            PLAN_API,
            {"json": {"semester_name": T2, "course_ids": [env.ids["c3"]]}},
        ),
        (
            "PUT",
            f"{PLAN_API}/{plan_id}/courses",
            {"json": {"course_ids": [env.ids["c4"]]}},
        ),
        ("DELETE", f"{PLAN_API}/{plan_id}", {}),
        ("DELETE", f"{PLAN_API}/{plan_id}/courses/{env.ids['c4']}", {}),
    ]
    for method, url, kwargs in requests:
        response = client.request(method, url, **kwargs)
        assert response.status_code == 401, (method, url, response.text)
        assert "Private feedback" not in response.text
        assert "Private profile" not in response.text
        if url.startswith("/api/"):
            assert response.json() == {"detail": "Could not validate credentials"}
        else:
            assert "Return to Login" in response.text
        assert env.snapshot() == before


@pytest.mark.it("IT-18")
@pytest.mark.parametrize(
    "case",
    [
        "course-text",
        "mixed-courses",
        "cancel-path",
        "remove-plan-path",
        "remove-course-path",
    ],
)
def test_invalid_form_or_path_types_return_422_without_writes(student, case):
    env, client = student.env, student.client
    plan_id = env.seed_plan()
    before = env.snapshot()
    if case in ("course-text", "mixed-courses"):
        courses = ("abc",) if case == "course-text" else ("c3", "abc")
        response = submit(client, env.ids, courses=courses, semester=T2)
    else:
        path = {
            "cancel-path": "/app/plan/abc/cancel",
            "remove-plan-path": f"/app/plan/abc/courses/{env.ids['c4']}/remove",
            "remove-course-path": f"/app/plan/{plan_id}/courses/abc/remove",
        }[case]
        response = client.post(path)
    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    assert env.snapshot() == before


@pytest.mark.it("IT-18")
@pytest.mark.parametrize("case", ["missing-cancel", "missing-remove", "absent-course"])
def test_missing_plan_or_course_warns_without_writes(student, case):
    env, client = student.env, student.client
    plan_id = env.seed_plan()
    before = env.snapshot()
    path, message = {
        "missing-cancel": ("/app/plan/999999/cancel", "Plan not found."),
        "missing-remove": (
            f"/app/plan/999999/courses/{env.ids['c4']}/remove",
            "Plan not found.",
        ),
        "absent-course": (
            f"/app/plan/{plan_id}/courses/{env.ids['c1']}/remove",
            "That course is not part of this plan.",
        ),
    }[case]
    redirected_page(client, client.post(path), message)
    assert env.snapshot() == before
