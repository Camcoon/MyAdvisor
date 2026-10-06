from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str
    role: str = ""
    name: str = ""
    student_number: str | None = Field(default=None, index=True, unique=True)
    degree_program: int | None = Field(
        default=None,
        foreign_key="degreeprogram.id",
        index=True,
    )


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)