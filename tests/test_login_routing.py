from starlette.requests import Request
import pytest

from app import main
from app.routers import login


@pytest.mark.unit
async def test_admin_login_redirects_to_home(monkeypatch):
    """UT-20 companion: retain E12's mocked login redirect coverage."""
    class FakeUserRepository:
        def __init__(self, db):
            pass

        def get_by_username(self, username):
            return type("User", (), {"role": "admin"})()

    class FakeAuthService:
        def __init__(self, user_repo):
            pass

        def authenticate_user(self, username, password):
            return "access-token"

    monkeypatch.setattr(login, "UserRepository", FakeUserRepository)
    monkeypatch.setattr(login, "AuthService", FakeAuthService)

    request = Request(
        {
            "type": "http",
            "method": "POST",
            "scheme": "http",
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
            "root_path": "",
            "path": "/login",
            "raw_path": b"/login",
            "query_string": b"",
            "headers": [],
            "app": main.app,
        }
    )

    response = await login.login_action_ajax(
        db=None,
        request=request,
        username="admin",
        password="password",
    )

    assert response.status_code == 303
    assert response.headers["location"] == str(request.url_for("user_home_view"))
