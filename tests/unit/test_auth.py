"""UT-20–UT-23: credential orchestration, identity guards and local crypto."""
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock, create_autospec

import jwt
import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app.dependencies import auth
from app.models.user import User
from app.repositories.user import UserRepository
from app.services import auth_service
from app.utilities import security

pytestmark = pytest.mark.unit


@pytest.fixture
def credentials(monkeypatch, student):
    repo = create_autospec(UserRepository, instance=True, spec_set=True)
    repo.get_by_username.return_value = student
    verify = Mock(return_value=True)
    token = Mock(return_value="test-token-sentinel")
    monkeypatch.setattr(auth_service, "verify_password", verify)
    monkeypatch.setattr(auth_service, "create_access_token", token)
    return SimpleNamespace(service=auth_service.AuthService(repo), repo=repo,
                           verify=verify, token=token)


def test_UT_20_authentication_success(credentials):
    assert credentials.service.authenticate_user("student", "test-password") == "test-token-sentinel"
    credentials.repo.get_by_username.assert_called_once_with("student")
    credentials.verify.assert_called_once_with(plaintext_password="test-password", encrypted_password="stored-hash")
    credentials.token.assert_called_once_with(data={"sub": "1", "role": "regular_user"})


@pytest.mark.parametrize("missing_user", [True, False], ids=["unknown-username", "wrong-password"])
def test_UT_21_authentication_failure(credentials, missing_user):
    if missing_user:
        credentials.repo.get_by_username.return_value = None
    credentials.verify.return_value = False
    assert credentials.service.authenticate_user("student", "wrong-password") is None
    credentials.repo.get_by_username.assert_called_once_with("student")
    credentials.token.assert_not_called()
    if missing_user:
        credentials.verify.assert_not_called()
    else:
        credentials.verify.assert_called_once_with(plaintext_password="wrong-password", encrypted_password="stored-hash")


@pytest.fixture
def identity(monkeypatch, student):
    repo = create_autospec(UserRepository, instance=True, spec_set=True)
    repo.get_by_id.return_value = student
    constructor = Mock(return_value=repo)
    decoder = Mock(return_value={"sub": "1", "role": "regular_user"})
    settings = SimpleNamespace(secret_key="unit-test-key", jwt_algorithm="HS256")
    monkeypatch.setattr(auth, "UserRepository", constructor)
    monkeypatch.setattr(auth.jwt, "decode", decoder)
    monkeypatch.setattr(auth, "get_settings", lambda: settings)
    return SimpleNamespace(repo=repo, constructor=constructor, decoder=decoder, settings=settings)


def request(cookie=True):
    return Request({"type": "http", "headers": [(b"cookie", b"access_token=test-cookie")] if cookie else []})


@pytest.mark.parametrize("case", ["missing-cookie", "invalid-token", "missing-user"])
async def test_UT_22_identity_failures(identity, case):
    if case == "invalid-token":
        identity.decoder.side_effect = jwt.InvalidTokenError("invalid test token")
    elif case == "missing-user":
        identity.repo.get_by_id.return_value = None
    with pytest.raises(HTTPException) as exc:
        await auth.get_current_user(request(case != "missing-cookie"), object())
    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"
    if case == "missing-cookie":
        identity.decoder.assert_not_called()
    if case != "missing-user":
        identity.constructor.assert_not_called()
    else:
        identity.repo.get_by_id.assert_called_once_with(1)


@pytest.mark.parametrize("role,user_id", [("regular_user", 1), ("admin", 3)])
async def test_UT_22_valid_identity_and_admin_guard(identity, student, role, user_id):
    student.role = role
    student.id = user_id
    # A token role claim cannot upgrade the role returned by the repository.
    identity.decoder.return_value = {"sub": str(user_id), "role": "admin"}
    session = object()
    user = await auth.get_current_user(request(), session)
    assert user is student
    identity.constructor.assert_called_once_with(session)
    identity.repo.get_by_id.assert_called_once_with(user_id)
    identity.decoder.assert_called_once_with("test-cookie", "unit-test-key", algorithms=["HS256"], options={"require": ["exp", "sub"]})
    if role == "admin":
        assert await auth.is_admin_dep(user) is student
    else:
        with pytest.raises(HTTPException) as exc:
            await auth.is_admin_dep(user)
        assert exc.value.status_code == 403


def test_UT_23_password_hash_contract():
    password = "unit-test-password-only"
    hashed = security.encrypt_password(password)
    assert isinstance(hashed, str)
    assert hashed != password
    assert security.verify_password(password, hashed) is True
    assert security.verify_password("wrong-password", hashed) is False


def test_UT_23_jwt_claims_expiry_and_input_unchanged(monkeypatch):
    fixed = datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc)

    class FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            assert tz == timezone.utc
            return fixed

    key = "unit-test-only-signing-key-at-least-32-bytes"
    monkeypatch.setattr(security, "datetime", FixedDatetime)
    monkeypatch.setattr(security, "get_settings", lambda: SimpleNamespace(secret_key=key, jwt_algorithm="HS256"))
    claims = {"sub": "1", "role": "regular_user"}
    token = security.create_access_token(claims, expires_delta=timedelta(minutes=5))
    # Verify the real signature; compare expiration to the fixed clock instead
    # of the host clock, so this test remains reproducible after the fixed date.
    decoded = jwt.decode(token, key, algorithms=["HS256"], options={"verify_exp": False})
    assert decoded == {"sub": "1", "role": "regular_user", "exp": int((fixed + timedelta(minutes=5)).timestamp())}
    assert claims == {"sub": "1", "role": "regular_user"}
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, "different-test-key-at-least-32-bytes", algorithms=["HS256"], options={"verify_exp": False})
