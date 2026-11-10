
from sqlmodel import select

from app.models.advising import DegreeProgram
from app.repositories.user import UserRepository
from app.schemas.user import RegularUserCreate
from app.utilities.security import (
    create_access_token,
    encrypt_password,
    verify_password,
)


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, username: str, password: str) -> str | None:
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(plaintext_password=password, encrypted_password=user.password):
            return None
        access_token = create_access_token(data={"sub": f"{user.id}", "role": user.role})
        return access_token

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        name: str = "",
        student_number: str = "",
    ):
        program = self.user_repo.db.exec(
            select(DegreeProgram).where(DegreeProgram.name == "Computer Science")
        ).first()
        if program is None:
            raise RuntimeError("The default degree program has not been configured.")
        new_user = RegularUserCreate(
            username=username, 
            email=email,
            name=name.strip(),
            student_number=student_number.strip() or None,
            degree_program=program.id,
            password=encrypt_password(password)
        )
        return self.user_repo.create(new_user)
