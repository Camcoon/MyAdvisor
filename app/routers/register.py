from typing import Annotated

from fastapi import Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from app.dependencies import SessionDep
from app.repositories.user import UserRepository
from app.services.auth_service import AuthService
from app.utilities.flash import flash

from . import router, templates


# View route (loads the page)
@router.get("/register", response_class=HTMLResponse)
async def register_view(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="register.html",
    )

# Action route (performs an action)
@router.post('/register', response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
def signup_user(
    request: Request,
    db: SessionDep,
    username: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    name: str = Form(default=""),
    student_number: str = Form(default=""),
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    try:
        auth_service.register_user(
            username,
            email,
            password,
            name=name,
            student_number=student_number,
        )
        flash(request, "Registration completed! Sign in now!")
        return RedirectResponse(url=request.url_for("login_view"), status_code=status.HTTP_303_SEE_OTHER)
    except IntegrityError:
        flash(request, "Username, email, or student ID already exists.", "danger")
        return RedirectResponse(url=request.url_for("register_view"), status_code=status.HTTP_303_SEE_OTHER)
