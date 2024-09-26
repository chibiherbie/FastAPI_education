from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    username: str
    name: str


class UserRequestAdd(BaseUser):
    password: str


class UserAdd(BaseUser):
    hashed_password: str


class User(BaseUser):
    id: int
