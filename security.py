from enum import auto
import re
import select
from urllib.error import HTTPError
from warnings import deprecated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.types import DependencyCacheKey
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import date, datetime, timedelta, timezone

import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str)->str:
    print(type(password), repr(password))
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expire
    token = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token
