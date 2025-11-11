from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Protocol
import re


app = FastAPI()    

class LoginRequest(BaseModel):
    email: str = Field(default="", description="사용자 이메일")
    password: str = Field(default="", description="사용자 비밀번호", max_length=20, min_length=8)

EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
PW_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$')

def is_valid_email(email: str):
    if not EMAIL_RE.fullmatch(email):
        raise HTTPException(status_code=400, detail="Invalid email payload")


def is_valid_password(pw: str):
    if not PW_RE.fullmatch(pw):
        raise HTTPException(status_code=400, detail="Invalid email payload")


def is_valid_login_request(req: LoginRequest):
    is_valid_email(req.email)
    is_valid_password(req.password)


def authenticate_user(email: str, password: str) -> None|dict:
    # 대충 DB에서 검색 로직
    # 검색해서 있으면 정보 딕션너리 반환
    # 없으면 None을 반환

    return None

@app.post("/login")
async def login(loginRequest: LoginRequest):
    # 형식 검증: 솔직히 이건 프런트의 몫이다.
    is_valid_login_request(loginRequest)

    user_data = authenticate_user(loginRequest.email, loginRequest.password)
    # 디비에서 이메일 검색
    if user_data is None:
        return HTTPException(status_code=403, detail="fail login")

    return user_data

