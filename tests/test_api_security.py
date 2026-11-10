"""Exercise real cookie verification and role guards against an isolated database."""

from copy import copy
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings
from app.database import get_session
from app.main import app
from app.models.user import User
from app.routers import api_router
from app.utilities.security import create_access_token, encrypt_password


@pytest.fixture
def security_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for user_id, role in [(1, "admin"), (2, "regular_user"), (3, "unknown")]:
            session.add(User(
                id=user_id,
                username=f"user{user_id}",
                email=f"user{user_id}@example.com",
                password=encrypt_password("test-password"),
                role=role,
            ))
        session.commit()

    def isolated_session():
        with Session(engine) as session:
            yield session

    previous_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_session] = isolated_session
    # No lifespan: the production startup seeds its own database.
    client = TestClient(app, follow_redirects=False)
    try:
        yield client, engine
    finally:
        client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)
        engine.dispose()


def signed_claims(claims, **kwargs):
    settings = get_settings()
    return jwt.encode(
        claims,
        kwargs.get("key", settings.secret_key),
        algorithm=kwargs.get("algorithm", settings.jwt_algorithm),
    )


def invalid_cookie(case):
    future = datetime.now(timezone.utc) + timedelta(minutes=5)
    claims = {"sub": "1", "exp": future}
    if case == "malformed":
        return "not-a-jwt"
    if case == "signature":
        return signed_claims(claims, key="incorrect-test-signing-key-with-32-bytes")
    if case == "algorithm":
        return signed_claims(claims, algorithm="HS512", key="x" * 64)
    if case == "expired":
        claims["exp"] = datetime.now(timezone.utc) - timedelta(minutes=5)
    elif case == "missing-exp":
        del claims["exp"]
    elif case == "invalid-exp":
        claims["exp"] = None
    elif case == "missing-sub":
        del claims["sub"]
    else:
        claims["sub"] = {
            "deleted-user": "999",
            "empty-sub": "",
            "non-numeric-sub": "admin",
            "integer-sub": 1,
            "null-sub": None,
            "object-sub": {"id": 1},
            "negative-sub": "-1",
            "oversized-sub": "9" * 100,
        }.get(case, "1")
    return signed_claims(claims)


@pytest.mark.parametrize("accept", ["application/json", "text/html"])
@pytest.mark.parametrize("case", [
    "missing", "malformed", "signature", "algorithm", "expired", "missing-exp",
    "invalid-exp", "missing-sub", "deleted-user", "empty-sub", "non-numeric-sub",
    "integer-sub", "null-sub", "object-sub", "negative-sub", "oversized-sub",
])
def test_invalid_authentication_is_json_401(security_client, case, accept):
    client, _ = security_client
    if case != "missing":
        client.cookies.set("access_token", invalid_cookie(case))
    response = client.get("/api/users", headers={"Accept": accept})
    assert response.status_code == 401
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"detail": "Could not validate credentials"}
    assert "location" not in response.headers


@pytest.mark.parametrize("user_id", [2, 3])
def test_non_admin_cannot_enumerate_users(security_client, user_id):
    client, _ = security_client
    # An admin claim must never override the current database role.
    client.cookies.set("access_token", create_access_token({"sub": str(user_id), "role": "admin"}))
    response = client.get("/api/users")
    assert response.status_code == 403
    assert response.json() == {"detail": "You are not authorized to access this resource"}
    assert "user1@example.com" not in response.text


def test_admin_response_only_exposes_allowlisted_fields(security_client):
    client, _ = security_client
    client.cookies.set("access_token", create_access_token({"sub": "1", "role": "regular_user"}))
    response = client.get("/api/users")
    assert response.status_code == 200
    assert sorted(response.json(), key=lambda row: row["id"]) == [
        {"id": i, "username": f"user{i}", "email": f"user{i}@example.com"}
        for i in [1, 2, 3]
    ]
    assert "set-cookie" not in response.headers


def test_role_changes_take_effect_with_existing_cookie(security_client):
    client, engine = security_client
    client.cookies.set("access_token", create_access_token({"sub": "1", "role": "admin"}))
    assert client.get("/api/users").status_code == 200
    with Session(engine) as session:
        user = session.get(User, 1)
        user.role = "regular_user"
        session.add(user)
        session.commit()
    assert client.get("/api/users").status_code == 403


def test_api_router_protects_new_routes_by_default(security_client):
    _client, _ = security_client
    # Use the same inherited router dependencies without modifying the live router.
    probe = FastAPI()
    probe.dependency_overrides[get_session] = app.dependency_overrides[get_session]
    probe_router = copy(api_router)
    probe_router.routes = []

    @probe_router.get("/probe")
    def protected():
        return {"ok": True}

    probe.include_router(probe_router)
    with TestClient(probe) as probe_client:
        assert probe_client.get("/api/probe").status_code == 401
        probe_client.cookies.set("access_token", create_access_token({"sub": "2"}))
        assert probe_client.get("/api/probe").status_code == 200


@pytest.mark.parametrize("user_id", [1, 2])
def test_html_login_cookie_supports_api_and_dashboard(security_client, user_id):
    client, _ = security_client
    assert client.get("/login").status_code == 200
    response = client.post("/login", data={
        "username": f"user{user_id}", "password": "test-password",
    })
    assert response.status_code == 303
    assert response.headers["location"].endswith("/app")
    cookie = response.headers["set-cookie"].lower()
    assert "httponly" in cookie
    assert "samesite=" in cookie
    assert "access_token" in client.cookies
    dashboard = client.get("/app")
    assert dashboard.status_code == 200
    assert dashboard.headers["content-type"].startswith("text/html")
    assert client.get("/api/users").status_code == (200 if user_id == 1 else 403)
    assert client.get("/admin").status_code == (200 if user_id == 1 else 403)
    assert client.get("/logout").status_code == 303
    assert client.get("/api/users").status_code == 401


def test_html_invalid_login_and_unauthenticated_dashboard(security_client):
    client, _ = security_client
    response = client.post("/login", data={"username": "user1", "password": "wrong"})
    assert response.status_code == 303
    assert response.headers["location"].endswith("/login")
    assert "access_token" not in client.cookies
    response = client.get("/app")
    assert response.status_code == 401
    assert response.headers["content-type"].startswith("text/html")
    assert "Return to Login" in response.text
