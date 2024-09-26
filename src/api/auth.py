from datetime import datetime, timezone, timedelta

import jwt
from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.db import async_session_maker
from src.repositories.users import UsersRepository
from src.shemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c81816sad34dasd93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= ({"exp": expire})  # to_encode.update(...)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/register')
async def register_user(
        data: UserRequestAdd,
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, name=data.name, username=data.username)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except IntegrityError:
            return HTTPException(409, 'Пользователь с таким email уже существует.')

    return {"status": "OK"}


@router.post('/login')
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    # hashed_password = pwd_context.hash(data.password)
    # new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, name=data.name, username=data.username)
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='Пользователь с таким email не существует')
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Пароль не верный')
        access_token = create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {"access_token": access_token}
