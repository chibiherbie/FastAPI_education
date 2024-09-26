from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str
    username: str
    name: str


class UserRequestAdd(BaseUser):
    password: str


class UserAdd(BaseUser):
    hashed_password: str


class User(BaseUser):
    id: int
