from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from jwt.exceptions import InvalidTokenError

from app.config import get_settings
from app.dependencies.session import SessionDep
from app.models.user import User
from app.repositories.user import UserRepository


async def get_current_user(request:Request, db:SessionDep)->User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    token = request.cookies.get("access_token")

    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(
            token,
            get_settings().secret_key,
            algorithms=[get_settings().jwt_algorithm],
            options={"require": ["exp", "sub"]},
        )
        subject = payload["sub"]
        # Subjects issued by the existing login service are positive database IDs.
        if (
            not isinstance(subject, str)
            or not subject.isascii()
            or not subject.isdecimal()
            or len(subject) > 19
            or not 0 < int(subject) <= 2**63 - 1
        ):
            raise credentials_exception
        user_id = int(subject)
    except (InvalidTokenError, TypeError, ValueError, OverflowError):
        raise credentials_exception from None

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)

    if user is None:
        raise credentials_exception
    return user

async def is_logged_in(request: Request, db:SessionDep):
    try:
        await get_current_user(request, db)
        return True
    except HTTPException as exc:
        if exc.status_code != status.HTTP_401_UNAUTHORIZED:
            raise
        return False

IsUserLoggedIn = Annotated[bool, Depends(is_logged_in)]
AuthDep = Annotated[User, Depends(get_current_user)]

async def is_admin(user: User):
    return user.role == "admin"

def require_roles(*roles: str):
    """Authorize against the current database role, never a token role claim."""
    async def check_role(user: AuthDep):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this resource",
            )
        return user

    return check_role


is_admin_dep = require_roles("admin")

AdminDep = Annotated[User, Depends(is_admin_dep)]

StudentDep = Annotated[User, Depends(require_roles("regular_user"))]
